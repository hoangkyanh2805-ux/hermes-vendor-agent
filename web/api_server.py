"""
MCM Web Server — serves dashboard with live Sheet data + landing page
Port: 3003
Usage: python web/api_server.py
Endpoints:
  GET /            → dashboard.html with live data injected
  GET /dashboard   → same
  GET /landing     → landing.html (static)
  GET /api/stats   → JSON stats from Google Sheet
  GET /health      → ok
"""

import os, json, time, re, base64, logging, urllib.request, urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from datetime import datetime, timezone, date, timedelta
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

PORT       = int(os.environ.get("MCM_WEB_PORT", "3003"))
SHEET_ID   = os.environ["GOOGLE_SHEET_ID"]
SA_FILE    = os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE", "/root/.hermes/mcm-vendor-sa.json")
WEB_DIR    = Path(__file__).parent
CACHE_TTL  = 300  # 5 min — don't hammer Sheets API

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("mcm-web")

_cache: dict = {"data": None, "ts": 0}


# ── Google Sheets auth (same as agent5.py) ────────────────────────────────────

def get_token():
    with open(SA_FILE) as f:
        sa = json.load(f)
    header  = base64.urlsafe_b64encode(json.dumps({"alg": "RS256", "typ": "JWT"}).encode()).rstrip(b"=")
    now     = int(time.time())
    claim   = json.dumps({
        "iss": sa["client_email"],
        "scope": "https://www.googleapis.com/auth/spreadsheets",
        "aud": "https://oauth2.googleapis.com/token",
        "exp": now + 3600, "iat": now,
    })
    payload_b = base64.urlsafe_b64encode(claim.encode()).rstrip(b"=")
    key       = serialization.load_pem_private_key(sa["private_key"].encode(), password=None)
    sig_input = header + b"." + payload_b
    sig       = base64.urlsafe_b64encode(key.sign(sig_input, padding.PKCS1v15(), hashes.SHA256())).rstrip(b"=")
    jwt       = (sig_input + b"." + sig).decode()
    data      = urllib.parse.urlencode({"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": jwt}).encode()
    resp      = urllib.request.urlopen("https://oauth2.googleapis.com/token", data=data, timeout=10)
    return json.loads(resp.read())["access_token"]

def sheets_read():
    token    = get_token()
    range_enc = urllib.parse.quote("Affiliate Master!A2:P")
    url      = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{range_enc}"
    req      = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    resp     = urllib.request.urlopen(req, timeout=15)
    return json.loads(resp.read()).get("values", [])


# ── Stats builder ─────────────────────────────────────────────────────────────

def build_stats(rows):
    """Compute KPI stats and leaderboard from Sheet rows."""
    total      = len(rows)
    active     = 0
    total_earn = 0.0
    refer_sum  = 0
    new_this_week = 0
    leaderboard   = []

    today = date.today()
    week_ago = today - timedelta(days=7)

    for row in rows:
        def safe(i, d=""):
            return row[i].strip() if len(row) > i and row[i] else d

        status = safe(7)
        if status in ("Active", "VIP"):
            active += 1

        try:
            total_earn += float(safe(13, "0"))
        except ValueError:
            pass

        try:
            refer_this_week = int(safe(11, "0"))
            refer_sum += refer_this_week
        except ValueError:
            refer_this_week = 0

        # Count new this week from lead_id: AFF-YYYYMMDD-XXX
        lead_id = safe(0)
        m = re.search(r"AFF-(\d{8})-", lead_id)
        if m:
            try:
                joined = date.fromisoformat(m.group(1)[:4] + "-" + m.group(1)[4:6] + "-" + m.group(1)[6:8])
                if joined >= week_ago:
                    new_this_week += 1
            except Exception:
                pass

        username = safe(2).lstrip("@") or "unknown"
        leaderboard.append({"handle": f"@{username}", "score": refer_this_week, "status": status})

    # Sort leaderboard by refer_this_week desc
    leaderboard.sort(key=lambda x: -x["score"])

    return {
        "total":         total,
        "active":        active,
        "total_earn":    round(total_earn, 2),
        "refer_sum":     refer_sum,
        "new_this_week": new_this_week,
        "leaderboard":   leaderboard[:5],
    }


# ── Cached fetch ──────────────────────────────────────────────────────────────

def get_stats():
    now = time.time()
    if _cache["data"] and now - _cache["ts"] < CACHE_TTL:
        return _cache["data"]
    try:
        rows = sheets_read()
        data = build_stats(rows)
        _cache["data"] = data
        _cache["ts"]   = now
        log.info(f"Sheet refreshed: {data['total']} affiliates, ${data['total_earn']} earn")
        return data
    except Exception as e:
        log.error(f"get_stats error: {e}")
        return _cache["data"]  # return stale if available


# ── HTML injection ────────────────────────────────────────────────────────────

def inject_dashboard(html: str, s: dict) -> str:
    """
    Surgically replace hardcoded values in the bundled JS string.
    Targets specific 'label: X, value: Y' patterns — safest approach
    since the JS is embedded inside an escaped string.
    """
    total      = s["total"]
    earn       = s["total_earn"]
    active     = s["active"]
    refer_sum  = s["refer_sum"]
    new_week   = s["new_this_week"]

    # KPI cards — replace value and sub fields within each object
    # Pattern: label: 'X', value: 'OLD'   →   label: 'X', value: 'NEW'
    def replace_stat(label, new_value, new_sub=None):
        nonlocal html
        # Replace value
        pattern = rf"(label: '{re.escape(label)}', value: )'[^']*'"
        repl    = rf"\g<1>'{new_value}'"
        html    = re.sub(pattern, repl, html)
        # Replace sub if provided
        if new_sub is not None:
            sub_pattern = rf"(label: '{re.escape(label)}'(?:[^}}]{{0,200}})sub: )'[^']*'"
            html = re.sub(sub_pattern, rf"\g<1>'{new_sub}'", html)

    replace_stat("Valid Joins",      str(total),           f"+{new_week} this week")
    replace_stat("Commission (est)", f"${earn:.2f}",        "this month")
    replace_stat("Posts",            str(refer_sum),        f"+{refer_sum} this week")
    replace_stat("Days Active",      str(active),           f"{active} active")

    # Leaderboard — replace handle and score in each ranked entry
    lb   = s["leaderboard"]
    for i, entry in enumerate(lb):
        rank_str = f"#{i+1}"
        handle   = entry["handle"]
        score    = str(entry["score"])
        done_js  = "true" if entry["score"] > 0 else "false"

        # Replace handle (look for rank pattern then handle on same object)
        # Each object: { rank: '#N', handle: '@old', score: 'X/Y', done: bool, me: bool }
        old_rank_pattern = rf"(rank: '{re.escape(rank_str)}', handle: )'@[^']*'"
        html = re.sub(old_rank_pattern, rf"\g<1>'{handle}'", html)

        old_score_pattern = rf"(rank: '{re.escape(rank_str)}'(?:[^}}]{{0,100}})score: )'[^']*'"
        html = re.sub(old_score_pattern, rf"\g<1>'{score}/week'", html)

        old_done_pattern = rf"(rank: '{re.escape(rank_str)}'(?:[^}}]{{0,150}})done: )(?:true|false)"
        html = re.sub(old_done_pattern, rf"\g<1>{done_js}", html)

    return html


# ── HTTP handler ──────────────────────────────────────────────────────────────

class Handler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        log.info(f"{self.address_string()} {fmt % args}")

    def send_html(self, html: str):
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, obj: dict):
        body = json.dumps(obj, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0]

        if path in ("/", "/dashboard", "/dashboard.html"):
            try:
                html  = (WEB_DIR / "dashboard.html").read_text(encoding="utf-8")
                stats = get_stats()
                if stats:
                    html = inject_dashboard(html, stats)
                self.send_html(html)
            except Exception as e:
                log.error(f"dashboard serve error: {e}")
                self.send_error(500, str(e))

        elif path in ("/landing", "/landing.html"):
            try:
                html = (WEB_DIR / "landing.html").read_text(encoding="utf-8")
                self.send_html(html)
            except Exception as e:
                self.send_error(500, str(e))

        elif path == "/api/stats":
            stats = get_stats()
            if stats:
                self.send_json(stats)
            else:
                self.send_error(503, "Sheet unavailable")

        elif path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")

        else:
            self.send_error(404)


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    log.info(f"MCM Web Server on port {PORT}")
    log.info(f"  Dashboard: http://localhost:{PORT}/")
    log.info(f"  Landing:   http://localhost:{PORT}/landing")
    log.info(f"  Stats API: http://localhost:{PORT}/api/stats")
    server.serve_forever()
