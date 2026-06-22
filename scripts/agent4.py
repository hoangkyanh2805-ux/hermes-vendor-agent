"""
Agent 4 - CRM Sync Agent
Always-running HTTP server on port 3001.
Listens to EspoCRM webhook events and syncs state to Google Sheet + Telegram.

Endpoints:
  POST /webhook/espo/lead-create      Lead.create
  POST /webhook/espo/status-change    Contact.fieldUpdate.status
  POST /webhook/espo/opportunity      Opportunity.create
  POST /webhook/espo/commission       Contact.fieldUpdate.total_earn
"""

import os, json, time, hmac, hashlib, logging, threading, urllib.request, urllib.parse, base64
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timezone
from pathlib import Path
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

PORT = int(os.environ.get("AGENT4_PORT", "3001"))
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
SHEET_ID = os.environ["GOOGLE_SHEET_ID"]
SA_FILE = os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE", "/root/.hermes/mcm-vendor-sa.json")
ESPO_SECRET = os.environ.get("ESPO_WEBHOOK_SECRET", "")
AFFILIATE_BASE_URL = os.environ.get("AFFILIATE_BASE_URL", "https://mcmvendor.com/ref")
AGENT1_STATE = "/root/.hermes/agent1_state.json"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("agent4")

COL = {
    "lead_id": 0, "name": 1, "telegram_username": 2, "source": 3,
    "channel": 4, "score": 5, "path": 6, "status": 7,
    "onboard_day": 8, "last_contact": 9, "last_post": 10,
    "refer_this_week": 11, "refer_last_week": 12,
    "total_earn": 13, "rank": 14, "notes": 15,
}
COL_LETTER = {v: chr(65 + v) for v in COL.values()}  # 0→A, 1→B...


# --- Google Sheets ---
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
    token = get_token()
    range_enc = urllib.parse.quote("Affiliate Master!A2:P")
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{range_enc}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    resp = urllib.request.urlopen(req, timeout=15)
    return json.loads(resp.read()).get("values", [])

def sheets_update_cell(row_num, col_letter, value):
    token = get_token()
    range_enc = urllib.parse.quote(f"Affiliate Master!{col_letter}{row_num}")
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{range_enc}?valueInputOption=RAW"
    body = json.dumps({"values": [[value]]}).encode()
    req = urllib.request.Request(url, data=body, method="PUT")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    try:
        urllib.request.urlopen(req, timeout=15)
    except Exception as e:
        log.error(f"sheets_update error: {e}")

def sheets_append_row(row_values):
    token = get_token()
    range_enc = urllib.parse.quote("Affiliate Master!A1")
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{range_enc}:append?valueInputOption=RAW&insertDataOption=INSERT_ROWS"
    body = json.dumps({"values": [row_values]}).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    try:
        urllib.request.urlopen(req, timeout=15)
    except Exception as e:
        log.error(f"sheets_append_row error: {e}")

def sheets_append_log(affiliate_id, action, detail, success=True):
    token = get_token()
    range_enc = urllib.parse.quote("Activity Log!A1")
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{range_enc}:append?valueInputOption=RAW&insertDataOption=INSERT_ROWS"
    now = datetime.now(timezone.utc).isoformat()
    body = json.dumps({"values": [[
        f"LOG-{int(time.time())}", affiliate_id, "Agent4", action,
        detail, now, str(success).upper(), ""
    ]]}).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    try:
        urllib.request.urlopen(req, timeout=15)
    except Exception as e:
        log.error(f"append_log error: {e}")


# --- Telegram ---
def tg_send(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": chat_id, "text": text, "parse_mode": "Markdown"
    }).encode()
    try:
        resp = urllib.request.urlopen(url, data=data, timeout=10)
        return json.loads(resp.read())
    except Exception as e:
        log.error(f"tg_send error to {chat_id}: {e}")
        return None


# --- Sheet helpers ---
def find_row_by_username(rows, username):
    """Return (row_index_0based, row) or (None, None)."""
    username = username.lstrip("@").lower()
    for i, row in enumerate(rows):
        idx = COL["telegram_username"]
        if idx < len(row) and row[idx].lstrip("@").lower() == username:
            return i, row
    return None, None

def find_row_by_lead_id(rows, lead_id):
    for i, row in enumerate(rows):
        if len(row) > 0 and row[0] == lead_id:
            return i, row
    return None, None

def get_chat_id(username):
    p = Path(AGENT1_STATE)
    if p.exists():
        state = json.loads(p.read_text())
        if username in state:
            return state[username].get("chat_id", f"@{username}")
    return f"@{username}"

def gen_lead_id():
    return f"AFF-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{int(time.time()) % 1000:03d}"


# --- Event handlers ---
def _unwrap(payload):
    """EspoCRM sends webhook payload as a list — unwrap to dict."""
    if isinstance(payload, list):
        return payload[0] if payload else {}
    return payload

def _get_custom(payload, field):
    """Try camelCase, c-prefixed camelCase, and snake_case variants for EspoCRM custom fields."""
    c = field[0].upper() + field[1:]
    for key in [field, f"c{c}", f"c_{field}", field.lower()]:
        if payload.get(key):
            return payload[key]
    return ""

def handle_lead_create(payload):
    """Lead created in EspoCRM → ensure in Sheet + welcome to group."""
    payload = _unwrap(payload)
    log.info(f"lead-create payload keys: {list(payload.keys())[:15]}")
    name = payload.get("name", "").strip()
    username = _get_custom(payload, "telegramUsername").strip().lstrip("@")
    source = _get_custom(payload, "source") or payload.get("source", "espocrm")
    channel = _get_custom(payload, "channel")

    if not username:
        log.warning("lead-create: no telegram_username in payload")
        return

    rows = sheets_read()
    row_idx, existing = find_row_by_username(rows, username)

    if existing:
        log.info(f"lead-create: {username} already in Sheet at row {row_idx + 2}, skipping append")
        return

    lead_id = gen_lead_id()
    now_str = datetime.now(timezone.utc).isoformat()
    new_row = [lead_id, name, f"@{username}", source, channel, "", "", "New", "0", now_str, "", "0", "0", "0", "", ""]
    sheets_append_row(new_row)
    log.info(f"lead-create: appended {username} as {lead_id}")

    chat_id = get_chat_id(username)
    if chat_id:
        tg_send(chat_id, f"Chào {name or username}! Bạn đã được thêm vào hệ thống MCM Vendor. Affiliate manager sẽ liên hệ bạn sớm nhất!")

    sheets_append_log(lead_id, "lead_created_from_espo", f"source={source}")


def handle_status_change(payload):
    """Contact status changed in EspoCRM."""
    payload = _unwrap(payload)
    username = payload.get("telegramUsername", payload.get("telegram_username", "")).strip().lstrip("@")
    new_status = payload.get("status", "")
    name = payload.get("name", username)

    if not username or not new_status:
        log.warning(f"status-change: missing username or status in payload")
        return

    rows = sheets_read()
    row_idx, row = find_row_by_username(rows, username)
    if row is None:
        log.warning(f"status-change: {username} not found in Sheet")
        return

    row_num = row_idx + 2
    old_status = row[COL["status"]] if len(row) > COL["status"] else ""

    if new_status == old_status:
        return

    sheets_update_cell(row_num, "H", new_status)
    log.info(f"status-change: {username} {old_status}→{new_status}")

    chat_id = get_chat_id(username)
    lead_id = row[0] if row else username

    if new_status == "Active" and old_status in ("New", "Onboarding"):
        tracking_link = f"{AFFILIATE_BASE_URL}/{username}"
        msg = (
            f"🎉 Tài khoản của bạn đã được kích hoạt!\n\n"
            f"Link affiliate của bạn:\n`{tracking_link}`\n\n"
            f"Dashboard: https://mcmvendor.com/affiliate\n"
            f"Mỗi lead qua link này = commission cho bạn. Bắt đầu chia sẻ ngay nhé!"
        )
        tg_send(chat_id, msg)
        sheets_append_log(lead_id, "status_changed", f"New→Active, link={tracking_link}")

    elif new_status == "VIP":
        msg = (
            f"⭐ Chúc mừng {name}! Bạn đã lên *VIP*!\n\n"
            f"Bạn sẽ nhận được:\n"
            f"• Commission rate cao hơn\n"
            f"• Priority support\n"
            f"• Kế hoạch scale 21 kênh riêng\n\n"
            f"Mình sẽ gửi lộ trình VIP cho bạn trong 24h."
        )
        tg_send(chat_id, msg)
        sheets_append_log(lead_id, "status_changed", "Active→VIP")

    elif new_status == "Churned":
        sheets_append_log(lead_id, "status_changed", f"{old_status}→Churned")


def handle_opportunity(payload):
    """Opportunity created = referral converted → update commission + notify."""
    payload = _unwrap(payload)
    affiliate_username = payload.get("affiliateUsername", payload.get("telegramUsername", "")).strip().lstrip("@")
    amount = float(payload.get("amount", payload.get("commissionAmount", 0)) or 0)
    opp_name = payload.get("name", "")

    if not affiliate_username:
        log.warning("opportunity: no affiliateUsername in payload")
        return

    rows = sheets_read()
    row_idx, row = find_row_by_username(rows, affiliate_username)
    if row is None:
        log.warning(f"opportunity: {affiliate_username} not found in Sheet")
        return

    row_num = row_idx + 2
    lead_id = row[0]

    # Update refer_this_week (+1)
    try:
        refer_this_week = int(row[COL["refer_this_week"]] or 0) + 1
    except (ValueError, IndexError):
        refer_this_week = 1
    sheets_update_cell(row_num, "L", refer_this_week)

    # Update total_earn
    try:
        total_earn = float(row[COL["total_earn"]] or 0) + amount
    except (ValueError, IndexError):
        total_earn = amount
    sheets_update_cell(row_num, "N", round(total_earn, 2))

    # Update last_contact
    sheets_update_cell(row_num, "J", datetime.now(timezone.utc).isoformat())

    # Notify affiliate
    if amount > 0:
        name = row[COL["name"]] if len(row) > COL["name"] else affiliate_username
        chat_id = get_chat_id(affiliate_username)
        msg = (
            f"💰 Bạn vừa có referral mới!\n"
            f"Commission: +${amount:.2f}\n"
            f"Tổng tích lũy: ${total_earn:.2f}\n"
            f"Refer tuần này: {refer_this_week} lead"
        )
        tg_send(chat_id, msg)

    sheets_append_log(lead_id, "opportunity_created", f"amount=${amount:.2f}, opp={opp_name}")
    log.info(f"opportunity: {affiliate_username} +${amount:.2f}, total={total_earn:.2f}")


def handle_commission(payload):
    """Contact.fieldUpdate.total_earn → sync commission to Sheet."""
    payload = _unwrap(payload)
    username = payload.get("telegramUsername", payload.get("telegram_username", "")).strip().lstrip("@")
    new_total = payload.get("total_earn", payload.get("value"))

    if not username or new_total is None:
        return

    try:
        new_total = float(new_total)
    except (ValueError, TypeError):
        log.warning(f"commission: invalid total_earn value: {new_total}")
        return

    rows = sheets_read()
    row_idx, row = find_row_by_username(rows, username)
    if row is None:
        return

    row_num = row_idx + 2
    sheets_update_cell(row_num, "N", round(new_total, 2))
    lead_id = row[0]
    sheets_append_log(lead_id, "commission_synced", f"total_earn=${new_total:.2f}")
    log.info(f"commission: {username} total_earn synced to ${new_total:.2f}")


# --- HTTP Handler ---
ROUTES = {
    "/webhook/espo/lead-create": handle_lead_create,
    "/webhook/espo/status-change": handle_status_change,
    "/webhook/espo/opportunity": handle_opportunity,
    "/webhook/espo/commission": handle_commission,
}

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        log.info(f"{self.client_address[0]} {fmt % args}")

    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status":"ok","agent":"agent4"}')
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        # Optional secret verification
        if ESPO_SECRET:
            sig = self.headers.get("X-Espo-Signature", "")
            expected = hmac.new(ESPO_SECRET.encode(), body, hashlib.sha256).hexdigest()
            if not hmac.compare_digest(sig, expected):
                self.send_response(401)
                self.end_headers()
                log.warning(f"Invalid signature from {self.client_address[0]}")
                return

        handler_fn = ROUTES.get(self.path)
        if not handler_fn:
            self.send_response(404)
            self.end_headers()
            return

        try:
            payload = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')

        # Process in background thread so we return 200 immediately
        threading.Thread(target=handler_fn, args=(payload,), daemon=True).start()


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    log.info(f"Agent 4 listening on port {PORT}")
    server.serve_forever()
