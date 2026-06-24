"""
Agent 3 - Daily Loop Agent
Usage: agent3.py [checklist|coaching|report]
Cron (VPS timezone UTC+7):
  0 7  * * *  → checklist (7AM)
  0 14 * * *  → coaching  (2PM)
  0 21 * * *  → report    (9PM)
"""

import os, json, sys, time, logging, threading, urllib.request, urllib.parse, base64
from datetime import datetime, timezone, date, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

BOT_TOKEN = os.environ.get("AFFILIATE_BOT_TOKEN") or os.environ["TELEGRAM_BOT_TOKEN"]
SHEET_ID = os.environ["GOOGLE_SHEET_ID"]
SA_FILE = os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE", "/root/.hermes/mcm-vendor-sa.json")
ROUTER_KEY = os.environ["OPENAI_API_KEY"]
ROUTER_URL = os.environ.get("OPENAI_BASE_URL", "http://127.0.0.1:20128/v1")
HIEP_CHAT_ID = int(os.environ.get("ADMIN_CHAT_ID", "672890533"))
MODEL = "kr/claude-sonnet-4.5"
AGENT1_STATE = "/root/.hermes/agent1_state.json"
AGENT3_PORT = int(os.environ.get("AGENT3_PORT", "3002"))
INTERNAL_TOKEN = os.environ.get("AGENT_INTERNAL_TOKEN", "mcm-internal-2026")  # set AGENT_INTERNAL_TOKEN in .env
COOLDOWN_FILE = Path("/root/.hermes/agent3_cooldown.json")
PENDING_FILE = Path("/root/.hermes/agent3_pending.json")
DEBOUNCE_SECONDS = 300  # 5 minutes

COOLDOWN_HOURS = {
    "vip_upgrade": 24,
    "first_refer": 876000,  # once only (~100 years)
    "rank_up": 6,
    "debounced": 1,
}

# Persona inject: (status, situation) → (name, style)
# situation = "inactive" khi last_post > 3 ngày, "normal" còn lại
PERSONA_MAP = {
    ("VIP",        "normal"):   ("Justin Welsh",    "positioning, protect brand, scale có chọn lọc"),
    ("Active",     "inactive"): ("Chris Voss",      "tactical empathy, re-engage không áp lực"),
    ("Active",     "normal"):   ("Gary Vee",        "volume, action-first, không ngại thô"),
    ("Onboarding", "normal"):   ("Ali Abdaal",      "systems, habit nhỏ, bước từng ngày"),
    ("New",        "normal"):   ("Alex Hormozi",    "value, fast results, show the math"),
    ("Cold",       "inactive"): ("Steven Bartlett", "story, gợi lại lý do ban đầu, reconnect"),
}

FALLBACK = {
    "vip_upgrade": "🎉 {name} vừa lên VIP với {total_refer} refer! Thành quả xứng đáng. Tiếp tục phát huy nhé!",
    "first_refer": "🔥 Lead đầu tiên rồi {name}! Khởi đầu tuyệt vời. Checklist sáng mai có gợi ý scale tiếp.",
    "rank_up": "📈 {name} lên hạng #{rank}/{total_affiliates}! Đang đi đúng hướng.",
    "debounced": "🚀 {name} bùng nổ hôm nay! Top performer tuần này rồi!",
}

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


# --- Cooldown management ---
_cooldown_lock = threading.Lock()
_pending_lock = threading.Lock()

def _load_json(path):
    try:
        return json.loads(path.read_text()) if path.exists() else {}
    except Exception:
        return {}

def _save_json(path, data):
    path.write_text(json.dumps(data, indent=2))

def is_on_cooldown(affiliate_id, event):
    with _cooldown_lock:
        data = _load_json(COOLDOWN_FILE)
        last = data.get(affiliate_id, {}).get(event)
        if not last:
            return False
        hours = COOLDOWN_HOURS.get(event, 24)
        elapsed = (datetime.now(timezone.utc) - datetime.fromisoformat(last)).total_seconds() / 3600
        return elapsed < hours

def mark_cooldown(affiliate_id, event):
    with _cooldown_lock:
        data = _load_json(COOLDOWN_FILE)
        data.setdefault(affiliate_id, {})[event] = datetime.now(timezone.utc).isoformat()
        _save_json(COOLDOWN_FILE, data)

def add_to_pending(affiliate_id, event, context):
    with _pending_lock:
        data = _load_json(PENDING_FILE)
        fire_at = (datetime.now(timezone.utc) + timedelta(seconds=DEBOUNCE_SECONDS)).isoformat()
        if affiliate_id in data:
            events = data[affiliate_id]["events"]
            if event not in events:
                events.append(event)
            data[affiliate_id]["fire_at"] = fire_at
            data[affiliate_id]["context"].update(context)
        else:
            data[affiliate_id] = {"events": [event], "fire_at": fire_at, "context": context}
        _save_json(PENDING_FILE, data)


# --- Trigger processing ---
def build_trigger_prompt(name, channel, events, context):
    join_days = context.get("join_days", 30)
    total_refer = context.get("total_refer", 0)
    total_earn = context.get("total_earn", 0)
    rank = context.get("rank", "?")
    total_affiliates = context.get("total_affiliates", "?")
    status = context.get("status", "Active")
    last_post_str = context.get("last_post", "")

    tone = "Mentor (tận tình hướng dẫn)" if join_days < 30 else "Partner (đồng hành ngang vai)"

    situation = "inactive" if days_since(last_post_str) > 3 else "normal"
    persona_name, persona_style = PERSONA_MAP.get(
        (status, situation),
        ("Gary Vee", "action-first, volume, không ngại thô")
    )

    if len(events) > 1:
        event_desc = "Nhiều cột mốc cùng lúc: " + ", ".join(events)
    else:
        event_desc = {
            "vip_upgrade": "vừa lên VIP",
            "first_refer": "có lead đầu tiên",
            "rank_up": f"lên hạng #{rank}",
        }.get(events[0], events[0])

    return (
        f"Tư duy như {persona_name} ({persona_style}).\n\n"
        f"Affiliate: {name}\nKênh: {channel}\nSự kiện: {event_desc}\n"
        f"Thông tin: gia nhập {join_days} ngày trước, {total_refer} refer, "
        f"earn ${total_earn}, rank #{rank}/{total_affiliates}\n"
        f"Giọng điệu: {tone}\n\n"
        f"Viết 1 tin nhắn Telegram chúc mừng/khích lệ. Tối đa 4 câu. "
        f"Thân thiện, cụ thể, có chiều sâu dựa trên thông tin trên. "
        f"KHÔNG giải thích. Chỉ viết tin nhắn."
    )

def is_valid_message(text):
    return bool(text) and 10 <= len(text) <= 600

def get_fallback(event_type, context):
    template = FALLBACK.get(event_type, FALLBACK["debounced"])
    return template.format(
        name=context.get("name", "Bạn"),
        total_refer=context.get("total_refer", 0),
        rank=context.get("rank", "?"),
        total_affiliates=context.get("total_affiliates", "?"),
    )

def fire_trigger_message(affiliate_id, event_type, events, context):
    name = context.get("name", "Bạn")
    username = context.get("username", "").lstrip("@")
    if not username:
        log.warning(f"fire_trigger: no username for {affiliate_id}")
        return

    if is_on_cooldown(affiliate_id, event_type):
        log.info(f"fire_trigger: {affiliate_id}/{event_type} on cooldown, skip")
        return

    # Enrich context from Sheet
    try:
        rows = sheets_read()
        for row in rows:
            if get(row, "lead_id") == affiliate_id:
                context["channel"] = get(row, "channel") or context.get("channel", "x")
                context["total_refer"] = safe_int(get(row, "refer_this_week")) + safe_int(get(row, "refer_last_week"))
                context["total_earn"] = safe_int(get(row, "total_earn"))
                context["rank"] = safe_int(get(row, "rank")) or "?"
                context["status"] = get(row, "status") or "Active"
                context["last_post"] = get(row, "last_post") or ""
                context["total_affiliates"] = len([r for r in rows if len(r) > COL["status"] and r[COL["status"]] in ("Active", "VIP")])
                try:
                    ds = affiliate_id.split("-")[1]
                    join_date = date(int(ds[:4]), int(ds[4:6]), int(ds[6:8]))
                    context["join_days"] = (date.today() - join_date).days
                except Exception:
                    context["join_days"] = 30
                break
    except Exception as e:
        log.error(f"fire_trigger: sheet read error: {e}")

    prompt = build_trigger_prompt(name, context.get("channel", "x"), events, context)
    content = llm(prompt, max_tokens=200)

    if not is_valid_message(content):
        log.warning(f"fire_trigger: invalid LLM response for {affiliate_id}/{event_type}, using fallback")
        content = get_fallback(event_type, {**context, "name": name})

    chat_id = get_chat_id(username)
    result = tg_send(chat_id, content)
    events_str = "+".join(events)

    if result and result.get("ok"):
        mark_cooldown(affiliate_id, event_type)
        sheets_append_log(affiliate_id, f"trigger_{event_type}", f"events={events_str},sent=OK")
        log.info(f"fire_trigger: {affiliate_id} {event_type} sent OK")
    else:
        sheets_append_log(affiliate_id, f"trigger_{event_type}", f"events={events_str},sent=FAIL", success=False)
        log.error(f"fire_trigger: tg_send failed for {affiliate_id}")

def process_due_pending():
    with _pending_lock:
        data = _load_json(PENDING_FILE)
        now = datetime.now(timezone.utc)
        due = {k: v for k, v in data.items()
               if datetime.fromisoformat(v["fire_at"]) <= now}
        if not due:
            return
        for k in due:
            del data[k]
        _save_json(PENDING_FILE, data)

    for affiliate_id, item in due.items():
        events = item["events"]
        context = item["context"]
        event_type = "debounced" if len(events) > 1 else events[0]
        threading.Thread(
            target=fire_trigger_message,
            args=(affiliate_id, event_type, events, context),
            daemon=True
        ).start()

def debounce_processor():
    while True:
        time.sleep(30)
        try:
            process_due_pending()
        except Exception as e:
            log.error(f"debounce processor error: {e}")


# --- Trigger HTTP server ---
def enqueue_trigger(payload):
    affiliate_id = payload.get("affiliate_id", "")
    event = payload.get("event", "")
    if not affiliate_id or not event:
        log.warning("enqueue_trigger: missing affiliate_id or event")
        return
    if is_on_cooldown(affiliate_id, event):
        log.info(f"enqueue_trigger: {affiliate_id}/{event} on cooldown, ignoring")
        return
    context = {
        "name": payload.get("name", ""),
        "username": payload.get("username", "").lstrip("@"),
        "channel": payload.get("channel", "x"),
        "total_refer": payload.get("total_refer", 0),
        "total_earn": payload.get("total_earn", 0),
        "rank": payload.get("rank", "?"),
        "total_affiliates": payload.get("total_affiliates", "?"),
    }
    log.info(f"enqueue_trigger: queuing {event} for {affiliate_id}")
    add_to_pending(affiliate_id, event, context)

class TriggerHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        log.info(f"{self.client_address[0]} {fmt % args}")

    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status":"ok","agent":"agent3-trigger"}')
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path != "/webhook/trigger":
            self.send_response(404)
            self.end_headers()
            return
        if self.headers.get("X-Internal-Token", "") != INTERNAL_TOKEN:
            self.send_response(401)
            self.end_headers()
            log.warning(f"trigger: invalid token from {self.client_address[0]}")
            return
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status":"queued"}')
        threading.Thread(target=enqueue_trigger, args=(payload,), daemon=True).start()

def run_server():
    threading.Thread(target=debounce_processor, daemon=True).start()
    server = HTTPServer(("0.0.0.0", AGENT3_PORT), TriggerHandler)
    log.info(f"Agent 3 trigger server listening on :{AGENT3_PORT}")
    server.serve_forever()


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
    if mode == "server":
        run_server()
    else:
        rows = sheets_read()
        if mode == "checklist":
            run_checklist(rows)
        elif mode == "coaching":
            run_coaching(rows)
        elif mode == "report":
            run_report(rows)
        else:
            log.error(f"Unknown mode: {mode}. Use checklist|coaching|report|server")
            sys.exit(1)
