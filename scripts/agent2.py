"""
Agent 2 - Onboard Agent
Cron: 8AM daily - check Google Sheet for affiliates needing D-X message today
Flow: read sheet -> find pending onboard_day -> Claude generate content by channel -> send Telegram -> update sheet
"""

import os, json, time, logging, urllib.request, urllib.parse, base64
from datetime import datetime, timezone
from pathlib import Path
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
SHEET_ID = os.environ["GOOGLE_SHEET_ID"]
SA_FILE = os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE", "/root/.hermes/mcm-vendor-sa.json")
ROUTER_KEY = os.environ["OPENAI_API_KEY"]
ROUTER_URL = os.environ.get("OPENAI_BASE_URL", "http://127.0.0.1:20128/v1")
MODEL = "kr/claude-sonnet-4.5"
STATE_FILE = "/root/.hermes/agent2_state.json"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("agent2")

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"

# Sheet column indexes (0-based) matching Affiliate Master schema
COL = {
    "lead_id": 0, "name": 1, "telegram_username": 2, "source": 3,
    "channel": 4, "score": 5, "path": 6, "status": 7,
    "onboard_day": 8, "last_contact": 9, "notes": 10,
}


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
    payload = base64.urlsafe_b64encode(claim.encode()).rstrip(b"=")
    key = serialization.load_pem_private_key(sa["private_key"].encode(), password=None)
    sig_input = header + b"." + payload
    sig = base64.urlsafe_b64encode(key.sign(sig_input, padding.PKCS1v15(), hashes.SHA256())).rstrip(b"=")
    jwt = (sig_input + b"." + sig).decode()
    data = urllib.parse.urlencode({"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": jwt}).encode()
    resp = urllib.request.urlopen("https://oauth2.googleapis.com/token", data=data, timeout=10)
    return json.loads(resp.read())["access_token"]

def sheets_read(tab):
    token = get_token()
    range_enc = urllib.parse.quote(f"{tab}!A2:P")
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{range_enc}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    resp = urllib.request.urlopen(req, timeout=15)
    data = json.loads(resp.read())
    return data.get("values", [])

def sheets_update_cell(row_num, col_letter, value):
    """row_num is 1-based (row 2 = first data row)."""
    token = get_token()
    range_enc = urllib.parse.quote(f"Affiliate Master!{col_letter}{row_num}")
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{range_enc}?valueInputOption=RAW"
    body = json.dumps({"values": [[value]]}).encode()
    req = urllib.request.Request(url, data=body, method="PUT")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    try:
        urllib.request.urlopen(req, timeout=15)
        return True
    except Exception as e:
        log.error(f"sheets_update error: {e}")
        return False

def sheets_append_log(affiliate_id, agent, action, detail, success=True):
    token = get_token()
    range_enc = urllib.parse.quote("Activity Log!A1")
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{range_enc}:append?valueInputOption=RAW&insertDataOption=INSERT_ROWS"
    now = datetime.now(timezone.utc).isoformat()
    body = json.dumps({"values": [[
        f"LOG-{int(time.time())}", affiliate_id, agent, action,
        detail, now, str(success).upper(), ""
    ]]}).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    try:
        urllib.request.urlopen(req, timeout=15)
    except Exception as e:
        log.error(f"sheets_append_log error: {e}")


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
        log.error(f"tg_send error: {e}")
        return None


# --- State ---
def load_state():
    if Path(STATE_FILE).exists():
        return json.loads(Path(STATE_FILE).read_text())
    return {}

def save_state(state):
    Path(STATE_FILE).write_text(json.dumps(state, indent=2, ensure_ascii=False))


# --- LLM content generation ---
def generate_content(day, name, channel, score="Warm"):
    target_leads = "10" if score == "Hot" else "5"
    prompt_file = PROMPTS_DIR / f"onboard-d{day}.txt"
    if prompt_file.exists():
        template = prompt_file.read_text(encoding="utf-8")
        prompt = (template
                  .replace("{{name}}", name)
                  .replace("{{channel}}", channel)
                  .replace("{{day}}", str(day))
                  .replace("{{target_leads}}", target_leads))
    else:
        prompt = f"""Affiliate: {name}
Kenh: {channel}
Stage: D{day} onboarding

Tao noi dung onboarding ngay {day} cho {name} ve chuong trinh affiliate XAUUSD MCM Vendor.
Cu the cho kenh {channel}.
Ngan gon, thiet thuc, co vi du thuc te.
Ket thuc bang 1 cau khuyen khich hanh dong cu the."""

    data = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 600,
        "stream": False,
    }).encode()
    req = urllib.request.Request(f"{ROUTER_URL}/chat/completions", data=data)
    req.add_header("Authorization", f"Bearer {ROUTER_KEY}")
    req.add_header("Content-Type", "application/json")
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        raw = resp.read().decode()
        if raw.startswith("data:"):
            content = ""
            for line in raw.split("\n"):
                line = line.strip()
                if line.startswith("data:") and line != "data: [DONE]":
                    try:
                        chunk = json.loads(line[5:].strip())
                        content += chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
                    except Exception:
                        pass
            return content.strip()
        else:
            r = json.loads(raw)
            return r["choices"][0]["message"]["content"].strip()
    except Exception as e:
        log.error(f"generate_content error: {e}")
        return None


# --- Main loop ---
def run():
    log.info("Agent 2 starting — checking onboard queue")
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    state = load_state()

    rows = sheets_read("Affiliate Master")
    sent_count = 0

    for i, row in enumerate(rows):
        def get(col):
            idx = COL.get(col, 99)
            return row[idx].strip() if idx < len(row) else ""

        lead_id = get("lead_id")
        name = get("name")
        username = get("telegram_username").lstrip("@")
        channel = get("channel") or "telegram"
        status = get("status")
        onboard_day_str = get("onboard_day")
        last_contact = get("last_contact")

        if status not in ("New", "Onboarding"):
            continue
        if not lead_id or not username:
            continue

        try:
            onboard_day = int(onboard_day_str) if onboard_day_str else 0
        except ValueError:
            onboard_day = 0

        if onboard_day >= 7:
            continue

        # Check if already sent today for this user
        state_key = f"{username}_{onboard_day + 1}"
        if state.get(state_key) == today:
            log.info(f"Skip {username} D{onboard_day + 1} — already sent today")
            continue

        next_day = onboard_day + 1
        log.info(f"Sending D{next_day} to {username} ({channel})")

        # Get chat_id from agent1 state if available
        agent1_state_file = Path(STATE_FILE).parent / "agent1_state.json"
        chat_id = f"@{username}"
        if agent1_state_file.exists():
            a1_state = json.loads(agent1_state_file.read_text())
            if username in a1_state:
                chat_id = a1_state[username].get("chat_id", f"@{username}")

        score = get("score") or "Warm"
        content = generate_content(next_day, name, channel, score)
        if not content:
            log.error(f"Failed to generate D{next_day} content for {username}")
            sheets_append_log(lead_id, "Agent2", "content_generate_failed", f"D{next_day}", False)
            continue

        result = tg_send(chat_id, content)
        if result and result.get("ok"):
            # Update onboard_day (col I = index 8, letter I)
            row_num = i + 2  # sheet row (1-based header + 1-based offset)
            sheets_update_cell(row_num, "I", next_day)
            # Update last_contact (col J)
            now_str = datetime.now(timezone.utc).isoformat()
            sheets_update_cell(row_num, "J", now_str)
            # Update status after D3
            if next_day >= 3 and status == "Onboarding":
                sheets_update_cell(row_num, "H", "Active")
                log.info(f"{username} promoted to Active after D3")
            elif next_day == 1:
                sheets_update_cell(row_num, "H", "Onboarding")

            state[state_key] = today
            save_state(state)
            sheets_append_log(lead_id, "Agent2", "onboard_message_sent", f"D{next_day} channel={channel}", True)
            sent_count += 1
            log.info(f"D{next_day} sent to {username}")
        else:
            log.error(f"Telegram send failed for {username}")
            sheets_append_log(lead_id, "Agent2", "telegram_send_failed", f"D{next_day}", False)

        time.sleep(1)  # rate limit

    log.info(f"Agent 2 done — sent {sent_count} messages")


if __name__ == "__main__":
    run()
