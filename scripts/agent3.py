"""
Agent 3 - Daily Loop Agent
Usage: agent3.py [checklist|coaching|report]
Cron:
  0 0 * * *  → checklist (7AM UTC+7)
  0 7 * * *  → coaching  (2PM UTC+7)
  0 14 * * * → report    (9PM UTC+7)
"""

import os, json, sys, time, logging, urllib.request, urllib.parse, base64
from datetime import datetime, timezone, date
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
AGENT1_STATE = "/root/.hermes/agent1_state.json"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("agent3")

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"

COL = {
    "lead_id": 0, "name": 1, "telegram_username": 2, "source": 3,
    "channel": 4, "score": 5, "path": 6, "status": 7,
    "onboard_day": 8, "last_contact": 9, "last_post": 10,
    "refer_this_week": 11, "refer_last_week": 12,
    "total_earn": 13, "rank": 14, "notes": 15,
}


# --- Google Sheets (same JWT pattern as agent2) ---
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

def sheets_update_cell(row_num, col_letter, value, token=None):
    if token is None:
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

def sheets_append_log(affiliate_id, action, detail, success=True):
    token = get_token()
    range_enc = urllib.parse.quote("Activity Log!A1")
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{range_enc}:append?valueInputOption=RAW&insertDataOption=INSERT_ROWS"
    now = datetime.now(timezone.utc).isoformat()
    body = json.dumps({"values": [[
        f"LOG-{int(time.time())}", affiliate_id, "Agent3", action,
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


# --- LLM ---
def llm(prompt, max_tokens=400):
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


# --- Helpers ---
def get_chat_id(username):
    p = Path(AGENT1_STATE)
    if p.exists():
        state = json.loads(p.read_text())
        if username in state:
            return state[username].get("chat_id", f"@{username}")
    return f"@{username}"

def days_since(date_str):
    """Return days since date_str (YYYY-MM-DD or ISO datetime). -1 if unparseable."""
    if not date_str:
        return 999
    try:
        d = date.fromisoformat(date_str[:10])
        return (date.today() - d).days
    except Exception:
        return 999

def safe_int(val, default=0):
    try:
        return int(val) if val else default
    except ValueError:
        return default

def get(row, col_name):
    idx = COL.get(col_name, 99)
    return row[idx].strip() if idx < len(row) else ""


# --- Mode: CHECKLIST ---
def run_checklist(rows):
    log.info("Mode: checklist (7AM)")
    sent = 0
    for row in rows:
        status = get(row, "status")
        if status not in ("Onboarding", "Active", "VIP"):
            continue
        username = get(row, "telegram_username").lstrip("@")
        if not username:
            continue

        name = get(row, "name")
        channel = get(row, "channel") or "telegram"
        onboard_day = safe_int(get(row, "onboard_day"))
        refer_this_week = safe_int(get(row, "refer_this_week"))
        refer_last_week = safe_int(get(row, "refer_last_week"))
        last_post = get(row, "last_post")
        days_post = days_since(last_post)

        template = (PROMPTS_DIR / "checklist.txt").read_text(encoding="utf-8")
        prompt = (template
                  .replace("{{name}}", name)
                  .replace("{{channel}}", channel)
                  .replace("{{status}}", status)
                  .replace("{{onboard_day}}", str(onboard_day))
                  .replace("{{days_since_post}}", str(days_post) if days_post < 999 else "chua ro")
                  .replace("{{refer_this_week}}", str(refer_this_week))
                  .replace("{{refer_last_week}}", str(refer_last_week)))

        content = llm(prompt, max_tokens=200)
        if not content:
            continue

        chat_id = get_chat_id(username)
        result = tg_send(chat_id, content)
        if result and result.get("ok"):
            sent += 1
            sheets_append_log(get(row, "lead_id"), "checklist_sent", f"channel={channel}")
        time.sleep(0.5)

    log.info(f"Checklist done — sent to {sent} affiliates")


# --- Mode: COACHING ---
def run_coaching(rows):
    log.info("Mode: coaching (2PM)")
    sent = 0
    for row in rows:
        status = get(row, "status")
        if status not in ("Onboarding", "Active", "VIP"):
            continue
        username = get(row, "telegram_username").lstrip("@")
        if not username:
            continue

        refer_this_week = safe_int(get(row, "refer_this_week"))
        refer_last_week = safe_int(get(row, "refer_last_week"))
        last_post = get(row, "last_post")
        days_post = days_since(last_post)

        drop_trigger = refer_last_week > 0 and refer_this_week < refer_last_week * 0.7
        inactive_trigger = days_post > 3

        if not drop_trigger and not inactive_trigger:
            continue

        name = get(row, "name")
        channel = get(row, "channel") or "telegram"

        template = (PROMPTS_DIR / "coaching.txt").read_text(encoding="utf-8")
        prompt = (template
                  .replace("{{name}}", name)
                  .replace("{{channel}}", channel)
                  .replace("{{refer_this_week}}", str(refer_this_week))
                  .replace("{{refer_last_week}}", str(refer_last_week))
                  .replace("{{days_since_post}}", str(days_post) if days_post < 999 else "chua ro"))

        content = llm(prompt, max_tokens=150)
        if not content:
            continue

        chat_id = get_chat_id(username)
        result = tg_send(chat_id, content)
        if result and result.get("ok"):
            sent += 1
            reason = "drop" if drop_trigger else "inactive"
            sheets_append_log(get(row, "lead_id"), "coaching_sent", f"reason={reason}")
        time.sleep(0.5)

    log.info(f"Coaching done — sent to {sent} affiliates")


# --- Mode: REPORT ---
def run_report(rows):
    log.info("Mode: report (9PM)")
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    token = get_token()

    # Filter active affiliates and compute ranks
    active = []
    for i, row in enumerate(rows):
        status = get(row, "status")
        if status not in ("Active", "VIP"):
            continue
        username = get(row, "telegram_username").lstrip("@")
        if not username:
            continue
        active.append({
            "i": i,
            "lead_id": get(row, "lead_id"),
            "name": get(row, "name"),
            "username": username,
            "channel": get(row, "channel") or "telegram",
            "refer_this_week": safe_int(get(row, "refer_this_week")),
            "refer_last_week": safe_int(get(row, "refer_last_week")),
            "total_earn": safe_int(get(row, "total_earn")),
            "last_post": get(row, "last_post"),
        })

    # Sort by refer_this_week DESC for ranking
    active.sort(key=lambda x: x["refer_this_week"], reverse=True)
    total = len(active)

    flagged = [a for a in active if days_since(a["last_post"]) >= 3]
    top = active[0] if active else None
    total_leads_today = sum(a["refer_this_week"] for a in active)

    # Send each affiliate their personal report + update rank in sheet
    aff_template = (PROMPTS_DIR / "report-affiliate.txt").read_text(encoding="utf-8")
    for rank_idx, aff in enumerate(active, start=1):
        # Update rank column (O = index 14)
        row_num = aff["i"] + 2
        sheets_update_cell(row_num, "O", rank_idx, token)

        earn_today = round(aff["refer_this_week"] / 7 * 8, 1)
        refer_today = round(aff["refer_this_week"] / 7, 1)

        if rank_idx > 1:
            gap = active[rank_idx - 2]["refer_this_week"] - aff["refer_this_week"]
            gap_msg = f"Con {gap} lead → len #{rank_idx - 1}"
        else:
            gap_msg = "Ban dang #1! Giu vung nhe"

        # 1-line insight from LLM
        insight_prompt = (
            f"Affiliate {aff['name']} kenh {aff['channel']} "
            f"refer {aff['refer_this_week']} tuan nay. "
            f"Viet 1 nhan xet ngan (max 15 tu), khich le hoac goi y cu the."
        )
        insight = llm(insight_prompt, max_tokens=60) or "Tiep tuc co gang!"

        msg = (aff_template
               .replace("{{refer_today}}", str(refer_today))
               .replace("{{earn_today}}", str(earn_today))
               .replace("{{rank}}", str(rank_idx))
               .replace("{{total_affiliates}}", str(total))
               .replace("{{gap_msg}}", gap_msg)
               .replace("{{insight}}", insight))

        chat_id = get_chat_id(aff["username"])
        tg_send(chat_id, msg)
        sheets_append_log(aff["lead_id"], "report_sent", f"rank={rank_idx}/{total}")
        time.sleep(0.5)

    # Send PM summary to Hiep
    pm_template = (PROMPTS_DIR / "report-pm.txt").read_text(encoding="utf-8")
    pm_msg = (pm_template
              .replace("{{date}}", today_str)
              .replace("{{total_leads}}", str(total_leads_today))
              .replace("{{active_count}}", str(total))
              .replace("{{top_username}}", top["username"] if top else "none")
              .replace("{{top_count}}", str(top["refer_this_week"]) if top else "0")
              .replace("{{flagged_count}}", str(len(flagged))))

    tg_send(HIEP_CHAT_ID, pm_msg)
    log.info(f"Report done — {total} affiliates, {len(flagged)} flagged, PM notified")


# --- Entry point ---
if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("AGENT3_MODE", "checklist")
    rows = sheets_read()
    if mode == "checklist":
        run_checklist(rows)
    elif mode == "coaching":
        run_coaching(rows)
    elif mode == "report":
        run_report(rows)
    else:
        log.error(f"Unknown mode: {mode}. Use checklist|coaching|report")
        sys.exit(1)
