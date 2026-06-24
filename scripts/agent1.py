"""
Agent 1 - Capture Agent
Webhook server: POST /webhook/capture
Flow: receive lead -> Q1 -> Q2 -> score -> write sheet -> welcome -> trigger agent2
"""

import os, sys, json, time, threading, logging, urllib.request, urllib.parse, subprocess
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64

# --- Config ---
PORT = 3000
# AFFILIATE_BOT_TOKEN = dedicated bot for affiliates (2-bot setup).
# If not set, falls back to TELEGRAM_BOT_TOKEN (shared bot — Hermes routing issues apply).
BOT_TOKEN = os.environ.get("AFFILIATE_BOT_TOKEN") or os.environ["TELEGRAM_BOT_TOKEN"]
ADMIN_CHAT_ID = int(os.environ.get("ADMIN_CHAT_ID", "672890533"))
SHEET_ID = os.environ["GOOGLE_SHEET_ID"]
SA_FILE = os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE", "/root/.hermes/mcm-vendor-sa.json")
ROUTER_KEY = os.environ["OPENAI_API_KEY"]
ROUTER_URL = os.environ.get("OPENAI_BASE_URL", "http://127.0.0.1:20128/v1")
MODEL = "kr/claude-sonnet-4.5"
STATE_FILE = "/root/.hermes/agent1_state.json"
FORM_LINK = os.environ.get("AFFILIATE_FORM_URL", "https://t.me/hiephoang47")
AFFILIATE_BASE_URL = os.environ.get("AFFILIATE_BASE_URL", "https://mcm-vendor.com/go")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("agent1")


BOT_INTRO = """MCM Vendor Bot online.

Minh ho tro affiliate qua Telegram:
- Nhan lead tu form va hoi 2 cau qualify
- Cham Hot/Warm/Cold bang 9Router
- Ghi lead vao Google Sheet
- Gui lo trinh Fast Track hoac Nurture
- Sau do Agent 2/3/4/5 se onboarding, checklist, report, CRM sync va monitor

Neu ban muon bat dau lai phan qualify, hay gui form lead hoac tra loi khi bot dang hoi Q1/Q2."""


def get_state_question(state, name):
    stage = state.get("stage")
    if stage == "q1_sent":
        return get_prompt("Q1", name=name)
    if stage == "q2_sent":
        return get_prompt("Q2")
    return BOT_INTRO


# --- State management ---
def load_state():
    if Path(STATE_FILE).exists():
        return json.loads(Path(STATE_FILE).read_text())
    return {}

def save_state(state):
    Path(STATE_FILE).write_text(json.dumps(state, indent=2, ensure_ascii=False))

def get_lead_state(username):
    return load_state().get(username)

def set_lead_state(username, data):
    state = load_state()
    state[username] = data
    save_state(state)

def clear_lead_state(username):
    state = load_state()
    if username in state:
        chat_id = state[username].get("chat_id")
        # Keep chat_id so Agent 2/3 can still find the user
        state[username] = {"chat_id": chat_id, "stage": "done"} if chat_id else {}
        if not chat_id:
            state.pop(username, None)
    save_state(state)


# --- Telegram ---
def tg_send(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}).encode()
    try:
        resp = urllib.request.urlopen(url, data=data, timeout=10)
        return json.loads(resp.read())
    except Exception as e:
        log.error(f"tg_send error: {e}")
        return None

def tg_get_updates(offset=0):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={offset}&timeout=5"
    try:
        resp = urllib.request.urlopen(url, timeout=10)
        return json.loads(resp.read()).get("result", [])
    except Exception:
        return []


# --- Google Sheets ---
def get_gsheet_token():
    with open(SA_FILE) as f:
        sa = json.load(f)
    header = base64.urlsafe_b64encode(json.dumps({"alg": "RS256", "typ": "JWT"}).encode()).rstrip(b"=")
    now = int(time.time())
    claim = json.dumps({"iss": sa["client_email"], "scope": "https://www.googleapis.com/auth/spreadsheets",
                        "aud": "https://oauth2.googleapis.com/token", "exp": now + 3600, "iat": now})
    payload = base64.urlsafe_b64encode(claim.encode()).rstrip(b"=")
    key = serialization.load_pem_private_key(sa["private_key"].encode(), password=None)
    sig_input = header + b"." + payload
    sig = base64.urlsafe_b64encode(key.sign(sig_input, padding.PKCS1v15(), hashes.SHA256())).rstrip(b"=")
    jwt = (sig_input + b"." + sig).decode()
    data = urllib.parse.urlencode({"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": jwt}).encode()
    resp = urllib.request.urlopen("https://oauth2.googleapis.com/token", data=data, timeout=10)
    return json.loads(resp.read())["access_token"]

def sheets_append(tab, values):
    token = get_gsheet_token()
    range_enc = urllib.parse.quote(f"{tab}!A1")
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{range_enc}:append?valueInputOption=RAW&insertDataOption=INSERT_ROWS"
    body = json.dumps({"values": [values]}).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    try:
        urllib.request.urlopen(req, timeout=15)
        return True
    except Exception as e:
        log.error(f"sheets_append error: {e}")
        return False


# --- LLM Scoring ---
def score_lead(q1, q2):
    prompt_file = Path(__file__).parent.parent / "prompts" / "qualify.txt"
    score_template = ""
    if prompt_file.exists():
        content = prompt_file.read_text(encoding="utf-8")
        start = content.find("## SCORE_PROMPT")
        end = content.find("\n---", start + 1)
        score_template = content[start + len("## SCORE_PROMPT"):end].strip()

    system_prompt = score_template.replace("{{q1_answer}}", q1).replace("{{q2_answer}}", q2)

    data = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": system_prompt}],
        "max_tokens": 100
    }).encode()
    req = urllib.request.Request(f"{ROUTER_URL}/chat/completions", data=data)
    req.add_header("Authorization", f"Bearer {ROUTER_KEY}")
    req.add_header("Content-Type", "application/json")

    try:
        resp = urllib.request.urlopen(req, timeout=20)
        raw = resp.read().decode()
        # Handle SSE streaming
        if raw.startswith("data:"):
            content = ""
            for line in raw.split("\n"):
                line = line.strip()
                if line.startswith("data:") and line != "data: [DONE]":
                    chunk = json.loads(line[5:].strip())
                    delta = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
                    content += delta
        else:
            r = json.loads(raw)
            content = r["choices"][0]["message"]["content"]

        # Extract JSON from content
        start = content.find("{")
        end = content.rfind("}") + 1
        if start >= 0:
            return json.loads(content[start:end])
    except Exception as e:
        log.error(f"score_lead error: {e}")

    return {"score": "Warm", "path": "nurture", "channel": "none"}


# --- Prompt helpers ---
def get_prompt(key, **kwargs):
    prompt_file = Path(__file__).parent.parent / "prompts" / "qualify.txt"
    if not prompt_file.exists():
        return f"[prompt {key} not found]"
    content = prompt_file.read_text(encoding="utf-8")
    start = content.find(f"## {key}")
    if start < 0:
        return f"[prompt {key} not found]"
    end = content.find("\n---", start + 1)
    text = content[start + len(f"## {key}"):end].strip() if end > 0 else content[start + len(f"## {key}"):].strip()
    for k, v in kwargs.items():
        text = text.replace("{{" + k + "}}", str(v))
    return text


# --- Lead ID generator ---
def gen_lead_id():
    return f"AFF-{datetime.now().strftime('%Y%m%d')}-{int(time.time()) % 10000:04d}"


# --- Complete lead flow (runs in background thread) ---
def process_lead(lead):
    username = lead["telegram_username"].lstrip("@")
    # chat_id: payload > pre-stored by Hermes (user messaged bot first) > fallback @username string
    existing = get_lead_state(username)
    chat_id = (lead.get("chat_id") or
               (existing.get("chat_id") if existing else None) or
               lead["telegram_username"])
    name = lead["name"]

    log.info(f"Processing lead: {username}")

    # Stage: waiting for Q1 reply
    set_lead_state(username, {**lead, "stage": "q1_sent", "chat_id": chat_id})

    # Send Q1
    q1_text = get_prompt("Q1", name=name)
    tg_send(chat_id, q1_text)
    log.info(f"Q1 sent to {username}")


def finalize_lead(username, q1, q2):
    state = get_lead_state(username)
    if not state:
        return
    chat_id = state.get("chat_id", f"@{username}")
    name = state.get("name", username)
    source = state.get("source", "unknown")

    log.info(f"Scoring lead {username}: q1={q1[:20]} q2={q2[:20]}")
    result = score_lead(q1, q2)
    score = result.get("score", "Warm")
    path = result.get("path", "nurture")
    channel = result.get("channel", "none")
    lead_id = gen_lead_id()
    now = datetime.now(timezone.utc).isoformat()

    log.info(f"Score: {score} path={path} channel={channel}")

    # Write to Affiliate Master
    sheets_append("Affiliate Master", [
        lead_id, name, f"@{username}", source, channel,
        score, path, "Onboarding", 0, now, "", 0, 0, 0, "", ""
    ])

    # Log activity
    sheets_append("Activity Log", [
        f"LOG-{int(time.time())}", lead_id, "Agent1", "webhook_received",
        f"source={source}, score={score}", now, "TRUE", ""
    ])

    # Send welcome
    prompt_key = f"WELCOME_{path.upper()}"
    welcome = get_prompt(prompt_key, name=name)
    tg_send(chat_id, welcome)
    log.info(f"Welcome sent to {username} (path={path})")

    # Fast Start Kit: tracking link + copy-paste post template per channel
    tracking_link = f"{AFFILIATE_BASE_URL}/{username}"
    kit_key = f"FAST_START_KIT_{channel.upper()}" if channel != "none" else "FAST_START_KIT_NONE"
    fast_kit = get_prompt(kit_key, name=name, tracking_link=tracking_link)
    if not fast_kit or fast_kit.startswith("[prompt"):
        fast_kit = get_prompt("FAST_START_KIT_NONE", name=name, tracking_link=tracking_link)
    if fast_kit and not fast_kit.startswith("[prompt"):
        tg_send(chat_id, fast_kit)
        log.info(f"Fast Start Kit ({kit_key}) sent to {username}")

    # Trigger Agent 2 D1 immediately — don't wait for the 8AM cron
    try:
        trigger_data = {"username": username, "chat_id": str(chat_id), "name": name,
                        "channel": channel, "score": score}
        trigger_file = f"/root/.hermes/agent2_trigger_{username}.json"
        Path(trigger_file).write_text(json.dumps(trigger_data))
        a2_script = str(Path(__file__).parent / "agent2.py")
        subprocess.Popen([sys.executable, a2_script, "--immediate", trigger_file],
                         env=os.environ.copy())
        log.info(f"Agent 2 D1 triggered immediately for {username}")
    except Exception as e:
        log.error(f"Failed to trigger agent2 immediately: {e}")

    clear_lead_state(username)


# --- Telegram polling for replies ---
_tg_offset = 0

def telegram_poll_loop():
    global _tg_offset
    log.info("Telegram polling started")
    while True:
        try:
            updates = tg_get_updates(_tg_offset)
            for upd in updates:
                _tg_offset = upd["update_id"] + 1
                msg = upd.get("message", {})
                if not msg:
                    continue
                user = msg.get("from", {})
                username = user.get("username", "")
                chat_id = msg["chat"]["id"]
                text = msg.get("text", "").strip()

                if not text:
                    continue

                state = get_lead_state(username) if username else None
                name = user.get("first_name") or user.get("last_name") or username or "bạn"

                if text.startswith("/"):
                    command = text.split()[0].lower()
                    if command in ("/start", "/help"):
                        tg_send(chat_id, get_state_question(state, name) if state else BOT_INTRO)
                    elif command == "/sethome":
                        tg_send(chat_id, "Agent 1 da nhan /sethome. Neu Hermes Gateway dang chay, gateway se luu home channel cho cron/report.")
                    else:
                        tg_send(chat_id, "Minh ho tro /start va /help. Neu ban dang o flow qualify, hay tra loi cau hoi hien tai nhe.")
                    continue

                stage = state.get("stage") if state else None

                if stage == "q1_sent":
                    set_lead_state(username, {**state, "stage": "q2_sent", "q1": text, "chat_id": chat_id})
                    tg_send(chat_id, get_prompt("Q2"))
                    log.info(f"Q2 sent to {username}")

                elif stage == "q2_sent":
                    q1 = state.get("q1", "")
                    set_lead_state(username, {**state, "stage": "scoring"})
                    threading.Thread(target=finalize_lead, args=(username, q1, text), daemon=True).start()

                else:
                    # New visitor — save chat_id, send form link (never bot intro)
                    if username:
                        existing = get_lead_state(username) or {}
                        set_lead_state(username, {**existing, "chat_id": chat_id, "stage": "new"})
                    tg_send(chat_id,
                        f"Chào bạn! 👋 Để tham gia affiliate MCM Vendor (XAUUSD signal), "
                        f"vui lòng liên hệ admin: {FORM_LINK}\n\n"
                        f"Hoặc điền form đăng ký để nhận link affiliate và hoa hồng ngay!")
                    log.info(f"New visitor {username or chat_id} — saved chat_id, sent form link")

        except Exception as e:
            log.error(f"Poll error: {e}")
        time.sleep(2)


# --- Webhook HTTP server ---
class WebhookHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        log.info(fmt % args)

    def do_GET(self):
        if self.path == "/health":
            body = json.dumps({"status": "ok", "agent": "agent1-capture", "version": "1.0.0"}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            payload = json.loads(body)
        except Exception:
            self.send_response(400)
            self.end_headers()
            return

        # Hermes forwards Telegram replies here (no polling conflict)
        if self.path == "/webhook/telegram":
            username = payload.get("username", "")
            text = payload.get("text", "").strip()
            chat_id = payload.get("chat_id")
            if not username or not text or not chat_id:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "missing username/text/chat_id"}).encode())
                return
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            state = get_lead_state(username)
            if not state:
                self.wfile.write(json.dumps({"status": "ignored", "reason": "no state"}).encode())
                return
            stage = state.get("stage")
            if stage == "q1_sent":
                set_lead_state(username, {**state, "stage": "q2_sent", "q1": text, "chat_id": chat_id})
                tg_send(chat_id, get_prompt("Q2"))
                log.info(f"Q2 sent to {username} (via hermes forward)")
                self.wfile.write(json.dumps({"status": "q2_sent"}).encode())
            elif stage == "q2_sent":
                q1 = state.get("q1", "")
                set_lead_state(username, {**state, "stage": "scoring"})
                threading.Thread(target=finalize_lead, args=(username, q1, text), daemon=True).start()
                log.info(f"Scoring started for {username} (via hermes forward)")
                self.wfile.write(json.dumps({"status": "scoring"}).encode())
            else:
                self.wfile.write(json.dumps({"status": "ignored", "stage": stage}).encode())
            return

        if self.path != "/webhook/capture":
            self.send_response(404)
            self.end_headers()
            return

        # Validate required fields
        required = ["name", "telegram_username", "source"]
        if not all(payload.get(f) for f in required):
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "missing required fields"}).encode())
            return

        # Respond immediately (< 30s SLA = ack fast, process in background)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "accepted", "message": "Lead received"}).encode())

        # Process in background
        threading.Thread(target=process_lead, args=(payload,), daemon=True).start()
        log.info(f"Lead accepted: {payload.get('telegram_username')} source={payload.get('source')}")


if __name__ == "__main__":
    # 2-bot mode: if AFFILIATE_BOT_TOKEN is set, agent1 polls its own bot
    # and does NOT rely on Hermes gateway for routing.
    # Single-bot mode: Hermes gateway polls, forwards via POST /webhook/telegram.
    if os.environ.get("AFFILIATE_BOT_TOKEN"):
        log.info("2-bot mode: starting Telegram polling for affiliate bot")
        threading.Thread(target=telegram_poll_loop, daemon=True).start()
    else:
        log.info("Single-bot mode: waiting for Hermes to forward replies via /webhook/telegram")

    server = HTTPServer(("0.0.0.0", PORT), WebhookHandler)
    log.info(f"Agent 1 webhook server listening on port {PORT}")
    server.serve_forever()
