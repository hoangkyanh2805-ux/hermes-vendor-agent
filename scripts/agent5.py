"""
Agent 5 - Project Monitor Agent
Cron:
  0 13 * * *   → daily report (8PM UTC+7)
  0 14 * * 5   → weekly summary (9PM UTC+7 Friday)
Usage: agent5.py [report|weekly]
"""

import os, sys, json, time, logging, subprocess, urllib.request, urllib.parse, base64
from datetime import datetime, timezone, timedelta
from pathlib import Path
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
SHEET_ID = os.environ["GOOGLE_SHEET_ID"]
SA_FILE = os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE", "/root/.hermes/mcm-vendor-sa.json")
ROUTER_KEY = os.environ["OPENAI_API_KEY"]
ROUTER_URL = os.environ.get("OPENAI_BASE_URL", "http://127.0.0.1:20128/v1")
HIEP_CHAT_ID = int(os.environ.get("ADMIN_CHAT_ID", "672890533"))
MODEL = "kr/claude-sonnet-4.5"
REPO_DIR = "/root/hermes-vendor-agent"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("agent5")


# --- Telegram ---
def tg_send(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode()
    try:
        resp = urllib.request.urlopen(url, data=data, timeout=10)
        return json.loads(resp.read())
    except Exception as e:
        log.error(f"tg_send error: {e}")
        return None


# --- LLM ---
def llm(prompt, max_tokens=300):
    data = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "stream": False,
    }).encode()
    req = urllib.request.Request(f"{ROUTER_URL}/chat/completions", data=data)
    req.add_header("Authorization", f"Bearer {ROUTER_KEY}")
    req.add_header("Content-Type", "application/json")
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        r = json.loads(resp.read())
        return r["choices"][0]["message"]["content"].strip()
    except Exception as e:
        log.error(f"llm error: {e}")
        return None


# --- Google Sheets (minimal — only reads) ---
def get_token():
    with open(SA_FILE) as f:
        sa = json.load(f)
    header = base64.urlsafe_b64encode(json.dumps({"alg": "RS256", "typ": "JWT"}).encode()).rstrip(b"=")
    now = int(time.time())
    claim = json.dumps({
        "iss": sa["client_email"],
        "scope": "https://www.googleapis.com/auth/spreadsheets",
        "aud": "https://oauth2.googleapis.com/token",
        "exp": now + 3600, "iat": now,
    })
    payload_b = base64.urlsafe_b64encode(claim.encode()).rstrip(b"=")
    key = serialization.load_pem_private_key(sa["private_key"].encode(), password=None)
    sig_input = header + b"." + payload_b
    sig = base64.urlsafe_b64encode(key.sign(sig_input, padding.PKCS1v15(), hashes.SHA256())).rstrip(b"=")
    jwt = (sig_input + b"." + sig).decode()
    data = urllib.parse.urlencode({"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": jwt}).encode()
    resp = urllib.request.urlopen("https://oauth2.googleapis.com/token", data=data, timeout=10)
    return json.loads(resp.read())["access_token"]

def sheets_read():
    try:
        token = get_token()
        range_enc = urllib.parse.quote("Affiliate Master!A2:P")
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{range_enc}"
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Bearer {token}")
        resp = urllib.request.urlopen(req, timeout=15)
        return json.loads(resp.read()).get("values", [])
    except Exception as e:
        log.error(f"sheets_read error: {e}")
        return []


# --- System checks ---
def check_service(name, user=False):
    """Returns 'active', 'inactive', or 'unknown'."""
    try:
        cmd = ["systemctl", "--user", "is-active", name] if user else ["systemctl", "is-active", name]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        return r.stdout.strip()
    except Exception:
        return "unknown"

def check_http(url):
    """Returns True if endpoint responds 200."""
    try:
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req, timeout=3)
        return resp.status == 200
    except Exception:
        return False

def get_disk_usage():
    try:
        r = subprocess.run(["df", "-h", "/"], capture_output=True, text=True, timeout=5)
        lines = r.stdout.strip().split("\n")
        if len(lines) >= 2:
            parts = lines[1].split()
            return parts[4] if len(parts) > 4 else "?"  # e.g. "45%"
    except Exception:
        pass
    return "?"

def get_mem_usage():
    try:
        r = subprocess.run(["free", "-m"], capture_output=True, text=True, timeout=5)
        lines = r.stdout.strip().split("\n")
        if len(lines) >= 2:
            parts = lines[1].split()
            if len(parts) >= 3:
                used = int(parts[2])
                total = int(parts[1])
                pct = round(used / total * 100) if total else 0
                return f"{pct}%"
    except Exception:
        pass
    return "?"

def get_today_commits():
    """Returns list of commit messages pushed today."""
    try:
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        r = subprocess.run(
            ["git", "-C", REPO_DIR, "log", f"--after={today} 00:00", "--pretty=format:%s"],
            capture_output=True, text=True, timeout=10
        )
        lines = [l.strip() for l in r.stdout.strip().split("\n") if l.strip()]
        return lines
    except Exception:
        return []

def get_recent_errors(lines=20):
    """Read last N lines of hermes-gateway journal for errors."""
    try:
        r = subprocess.run(
            ["journalctl", "-u", "hermes-gateway", "-n", str(lines), "--no-pager", "-q"],
            capture_output=True, text=True, timeout=10
        )
        errors = [l for l in r.stdout.split("\n") if "error" in l.lower() or "failed" in l.lower()]
        return errors[:5]
    except Exception:
        return []


# --- SOP progress ---
SOP_CHECKS = [
    # (description, check_fn)
    ("Repo + folder structure",          lambda: (Path(REPO_DIR) / "scripts").exists()),
    (".env.example + .gitignore",        lambda: (Path(REPO_DIR) / ".env.example").exists()),
    ("Google Sheet created",             lambda: bool(os.environ.get("GOOGLE_SHEET_ID"))),
    ("Telegram Bot configured",          lambda: bool(os.environ.get("TELEGRAM_BOT_TOKEN"))),
    ("Agent 1: capture + qualify",       lambda: (Path(REPO_DIR) / "scripts/agent1.py").exists()),
    ("Agent 2: D1-D7 scripts",           lambda: all((Path(REPO_DIR) / f"prompts/onboard-d{d}.txt").exists() for d in range(1, 8))),
    ("Agent 2: cron deployed",           lambda: _cron_has("run-agent2")),
    ("Agent 3: 3-cron checklist+report", lambda: (Path(REPO_DIR) / "scripts/agent3.py").exists()),
    ("Agent 3: cron deployed",           lambda: _cron_has("run-agent3")),
    ("Agent 4: CRM sync server",         lambda: (Path(REPO_DIR) / "scripts/agent4.py").exists()),
    ("Agent 4: service active",          lambda: check_service("mcm-agent4") == "active"),
    ("Agent 5: monitor deployed",        lambda: (Path(REPO_DIR) / "scripts/agent5.py").exists()),
]

def _cron_has(keyword):
    try:
        r = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=5)
        return keyword in r.stdout
    except Exception:
        return False

def compute_progress():
    done = sum(1 for _, fn in SOP_CHECKS if _safe_check(fn))
    return done, len(SOP_CHECKS)

def _safe_check(fn):
    try:
        return fn()
    except Exception:
        return False


# --- Sheet stats ---
def get_sheet_stats(rows):
    statuses = {}
    total_earn = 0
    flagged = 0
    top_user, top_count = "", 0
    from datetime import date

    for row in rows:
        if len(row) < 8:
            continue
        status = row[7].strip() if len(row) > 7 else ""
        statuses[status] = statuses.get(status, 0) + 1

        try:
            earn = float(row[13]) if len(row) > 13 and row[13] else 0
            total_earn += earn
        except ValueError:
            pass

        try:
            refer = int(row[11]) if len(row) > 11 and row[11] else 0
            username = row[2].lstrip("@") if len(row) > 2 else ""
            if refer > top_count:
                top_count = refer
                top_user = username
        except ValueError:
            pass

        last_post_str = row[10].strip() if len(row) > 10 else ""
        if last_post_str:
            try:
                lp = date.fromisoformat(last_post_str[:10])
                if (date.today() - lp).days >= 3:
                    flagged += 1
            except Exception:
                pass

    active = statuses.get("Active", 0) + statuses.get("VIP", 0)
    return {
        "total": len(rows),
        "active": active,
        "statuses": statuses,
        "total_earn": round(total_earn, 2),
        "top_user": top_user,
        "top_count": top_count,
        "flagged": flagged,
    }


# --- Report ---
def build_daily_report():
    now = datetime.now(timezone.utc)
    # UTC+7
    local = now + timedelta(hours=7)
    days_vn = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
    day_name = days_vn[local.weekday()]
    date_str = local.strftime("%d/%m/%Y")

    hermes_ok = check_service("hermes-gateway", user=True) == "active"
    agent4_ok = check_http("http://localhost:3001/health")
    agent1_ok = check_http("http://localhost:3000/health")
    disk = get_disk_usage()
    mem = get_mem_usage()

    def status_icon(ok): return "✅" if ok else "❌"

    commits = get_today_commits()
    errors = get_recent_errors()

    rows = sheets_read()
    stats = get_sheet_stats(rows)
    done, total_steps = compute_progress()
    progress_pct = round(done / total_steps * 100)

    commit_lines = "\n".join(f"  • {c}" for c in commits) if commits else "  (không có commit)"
    error_lines = "\n".join(f"  ⚠️ {e}" for e in errors) if errors else "  Không có lỗi"

    report = f"""━━━━━━━━━━━━━━━━━━━━━━
MCM BUILD — {day_name} {date_str}
━━━━━━━━━━━━━━━━━━━━━━
Agent 1 (Capture):    {status_icon(agent1_ok)}
Agent 2 (Onboard):    {status_icon(_cron_has("run-agent2"))}
Agent 3 (Daily Loop): {status_icon(_cron_has("run-agent3"))}
Agent 4 (CRM Sync):   {status_icon(agent4_ok)}
Agent 5 (Monitor):    {status_icon(True)}
Hermes Gateway:       {status_icon(hermes_ok)}

Tiến độ: {done}/{total_steps} bước ({progress_pct}%)
VPS: Disk {disk} | RAM {mem}

Affiliate: {stats['active']} active / {stats['total']} total
Commission: ${stats['total_earn']}
Top: @{stats['top_user']} ({stats['top_count']} refer)
Cần chú ý: {stats['flagged']} người không hoạt động 3+ ngày

Commit hôm nay: {len(commits)}
{commit_lines}

Lỗi gần đây:
{error_lines}
━━━━━━━━━━━━━━━━━━━━━━"""
    return report


def build_weekly_report(rows):
    now = datetime.now(timezone.utc) + timedelta(hours=7)
    week_str = now.strftime("Tuần %W/%Y")
    stats = get_sheet_stats(rows)

    try:
        r = subprocess.run(
            ["git", "-C", REPO_DIR, "log", "--since=7 days ago", "--pretty=format:%s"],
            capture_output=True, text=True, timeout=10
        )
        week_commits = [l.strip() for l in r.stdout.strip().split("\n") if l.strip()]
    except Exception:
        week_commits = []

    done, total_steps = compute_progress()

    summary_prompt = f"""
Tong ket tuan MCM Vendor:
- {done}/{total_steps} buoc SOP hoan thanh
- {stats['active']} affiliate dang active
- Commission tich luy: ${stats['total_earn']}
- Top affiliate: @{stats['top_user']} ({stats['top_count']} refer)
- {len(week_commits)} commits trong tuan

Viet 2-3 cau nhan xet tuan: diem tot nhat, diem can cai thien, de xuat tuan toi.
Ngan gon, thiet thuc.
"""
    insight = llm(summary_prompt, max_tokens=200) or "(lỗi sinh insight)"

    commit_lines = "\n".join(f"  • {c}" for c in week_commits[:10]) if week_commits else "  (không có commit)"

    report = f"""━━━━━━━━━━━━━━━━━━━━━━
MCM WEEKLY — {week_str}
━━━━━━━━━━━━━━━━━━━━━━
SOP: {done}/{total_steps} bước ({round(done/total_steps*100)}%)
Commits: {len(week_commits)}
{commit_lines}

Affiliate: {stats['active']} active | {stats['total']} total
Commission tích lũy: ${stats['total_earn']}
Flagged: {stats['flagged']} người cần chú ý

{insight}
━━━━━━━━━━━━━━━━━━━━━━"""
    return report


# --- Entry point ---
if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "report"

    if mode == "report":
        msg = build_daily_report()
        tg_send(HIEP_CHAT_ID, msg)
        log.info("Daily report sent to Hiep")

    elif mode == "weekly":
        rows = sheets_read()
        msg = build_weekly_report(rows)
        tg_send(HIEP_CHAT_ID, msg)
        log.info("Weekly report sent to Hiep")

    else:
        log.error(f"Unknown mode: {mode}. Use report|weekly")
        sys.exit(1)
