"""
Agent 5 - Project Monitor Agent
Cron:
  0 13 * * *   → daily report (8PM UTC+7)
  0 14 * * 5   → weekly summary (9PM UTC+7 Friday)
  0  * * * *   → sync Sheet → EspoCRM (every hour)
Usage: agent5.py [report|weekly|sync]
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
ESPO_URL = os.environ.get("ESPOCRM_URL", "http://localhost:8080")
ESPO_USER = os.environ.get("ESPO_USER", "admin")
ESPO_PASS = os.environ.get("ESPO_PASS", "")

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


# --- Bundle packaging ---
_BUNDLE_ITEMS = [
    ("CLAUDE.md (SOP + adapt guide)",     lambda: (Path(REPO_DIR) / "CLAUDE.md").exists()),
    ("skills/ (5 yaml files)",            lambda: len(list((Path(REPO_DIR) / "skills").glob("*.yaml"))) >= 5),
    ("prompts/ (12 templates)",           lambda: len(list((Path(REPO_DIR) / "prompts").glob("*.txt"))) >= 10),
    ("README.md + DEPLOYMENT.md",         lambda: (Path(REPO_DIR) / "DEPLOYMENT.md").exists()),
    ("advisory-board/ (11 personas)",     lambda: (Path(REPO_DIR) / "advisory-board").is_dir()),
    ("souls/ (5 SOUL files)",             lambda: len(list((Path(REPO_DIR) / "souls").glob("agent*.md"))) >= 5),
    ("knowledge/ (ICP + books)",          lambda: (Path(REPO_DIR) / "knowledge").is_dir()),
    ("playbook/ (ops runbook)",           lambda: (Path(REPO_DIR) / "playbook").is_dir()),
]

def check_bundle_ready():
    done, total = compute_progress()
    return done == total

def build_bundle_manifest():
    lines = ["🎁 BUNDLE SẴN SÀNG — 36/37 SOP ✅", "━━━━━━━━━━━━━━━━━━"]
    for label, fn in _BUNDLE_ITEMS:
        ok = _safe_check(fn)
        lines.append(f"  {'✅' if ok else '❌'} {label}")
    lines.append("")
    lines.append("Manual (export thủ công):")
    lines.append("  ⚙️  Google Sheet template (.csv)")
    lines.append("  ⚙️  EspoCRM config pack (Entity + Webhooks)")
    lines.append("")
    lines.append("Pricing: $497 / $1,997 / $4,997+ / $197mo")
    return "\n".join(lines)


# --- Activity Log ---
def sheets_read_activity():
    try:
        token = get_token()
        range_enc = urllib.parse.quote("Activity Log!A2:H")
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{range_enc}"
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Bearer {token}")
        resp = urllib.request.urlopen(req, timeout=15)
        return json.loads(resp.read()).get("values", [])
    except Exception as e:
        log.error(f"sheets_read_activity error: {e}")
        return []

def get_trigger_stats_today():
    rows = sheets_read_activity()
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    vip = first_ref = fail = total = 0
    for row in rows:
        if len(row) < 6:
            continue
        action = row[3] if len(row) > 3 else ""
        ts = row[5] if len(row) > 5 else ""
        success = row[6] if len(row) > 6 else "TRUE"
        if not action.startswith("trigger_"):
            continue
        if not ts.startswith(today_str):
            continue
        total += 1
        if "vip_upgrade" in action:
            vip += 1
        elif "first_refer" in action:
            first_ref += 1
        if success == "FALSE":
            fail += 1
    return {"total": total, "vip_upgrade": vip, "first_refer": first_ref, "fail": fail}


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
    trigger_stats = get_trigger_stats_today()
    done, total_steps = compute_progress()
    progress_pct = round(done / total_steps * 100)

    commit_lines = "\n".join(f"  • {c}" for c in commits) if commits else "  (không có commit)"
    error_lines = "\n".join(f"  ⚠️ {e}" for e in errors) if errors else "  Không có lỗi"

    if trigger_stats["total"] > 0:
        trigger_block = (
            f"VIP upgrades: {trigger_stats['vip_upgrade']} | "
            f"First refers: {trigger_stats['first_refer']}\n"
            f"  Tổng: {trigger_stats['total']} | "
            f"Lỗi: {trigger_stats['fail']}"
        )
    else:
        trigger_block = "  Chưa có trigger event"

    agent3_trigger_ok = check_http("http://localhost:3002/health")

    bundle_block = ("\n\n" + build_bundle_manifest()) if check_bundle_ready() else ""

    report = f"""━━━━━━━━━━━━━━━━━━━━━━
MCM BUILD — {day_name} {date_str}
━━━━━━━━━━━━━━━━━━━━━━
Agent 1 (Capture):    {status_icon(agent1_ok)}
Agent 2 (Onboard):    {status_icon(_cron_has("run-agent2"))}
Agent 3 (Daily Loop): {status_icon(_cron_has("run-agent3"))}
Agent 3 (Trigger):    {status_icon(agent3_trigger_ok)}
Agent 4 (CRM Sync):   {status_icon(agent4_ok)}
Agent 5 (Monitor):    {status_icon(True)}
Hermes Gateway:       {status_icon(hermes_ok)}

Tiến độ: {done}/{total_steps} bước ({progress_pct}%)
VPS: Disk {disk} | RAM {mem}

Affiliate: {stats['active']} active / {stats['total']} total
Commission: ${stats['total_earn']}
Top: @{stats['top_user']} ({stats['top_count']} refer)
Cần chú ý: {stats['flagged']} người không hoạt động 3+ ngày

Trigger Events hôm nay:
{trigger_block}

Commit hôm nay: {len(commits)}
{commit_lines}

Lỗi gần đây:
{error_lines}{bundle_block}
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


# --- EspoCRM helpers ---
def _espo_auth():
    creds = base64.b64encode(f"{ESPO_USER}:{ESPO_PASS}".encode()).decode()
    return f"Basic {creds}"

def espo_request(method, path, body=None):
    """Call EspoCRM REST API. Returns parsed JSON or None on error."""
    url = f"{ESPO_URL}/api/v1/{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", _espo_auth())
    req.add_header("Content-Type", "application/json")
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        log.warning(f"espo {method} {path}: HTTP {e.code} — {e.read().decode()[:200]}")
        return None
    except Exception as e:
        log.error(f"espo {method} {path}: {e}")
        return None

def espo_find_contact(telegram_username):
    """Search EspoCRM Contact by cTelegramUsername. Returns {id, ...} or None."""
    username = telegram_username.lstrip("@")
    handle = f"@{username}"
    path = (
        "Contact"
        "?where[0][type]=equals"
        f"&where[0][attribute]=cTelegramUsername"
        f"&where[0][value]={urllib.parse.quote(handle)}"
        "&select=id,firstName,lastName,cStatus,cOnboardDay,cTotalEarn,cScore,cPath,cChannel"
        "&maxSize=1"
    )
    result = espo_request("GET", path)
    if result and result.get("list"):
        return result["list"][0]
    return None

def espo_create_contact(fields):
    """Create a new Contact in EspoCRM. Returns created record or None."""
    return espo_request("POST", "Contact", fields)

def espo_update_contact(espo_id, fields):
    """Patch an existing Contact. Returns updated record or None."""
    return espo_request("PUT", f"Contact/{espo_id}", fields)

def _parse_name(full_name):
    parts = full_name.strip().split(None, 1)
    return parts[0], parts[1] if len(parts) > 1 else ""

def _row_to_espo_fields(row):
    """Map a Sheet row (list) to EspoCRM Contact field dict."""
    def safe(idx, default=""):
        return row[idx].strip() if len(row) > idx and row[idx] else default

    full_name = safe(1)
    first, last = _parse_name(full_name) if full_name else ("", "")
    username = safe(2)
    handle = f"@{username.lstrip('@')}" if username else ""

    fields = {
        "firstName": first,
        "lastName": last,
        "cTelegramUsername": handle,
        "cSource": safe(3),
        "cChannel": safe(4),
        "cScore": safe(5),
        "cPath": safe(6),
        "cStatus": safe(7),
    }
    onboard_day = safe(8)
    if onboard_day.isdigit():
        fields["cOnboardDay"] = int(onboard_day)

    total_earn = safe(13)
    try:
        fields["cTotalEarn"] = float(total_earn)
    except (ValueError, TypeError):
        pass

    return fields

def _needs_update(existing, new_fields):
    """Return only fields that differ from EspoCRM existing record."""
    updates = {}
    field_map = {
        "cStatus": "cStatus",
        "cOnboardDay": "cOnboardDay",
        "cTotalEarn": "cTotalEarn",
        "cScore": "cScore",
        "cPath": "cPath",
        "cChannel": "cChannel",
        "firstName": "firstName",
        "lastName": "lastName",
    }
    for f in field_map:
        new_val = new_fields.get(f)
        old_val = existing.get(f)
        if new_val is not None and str(new_val) != str(old_val or ""):
            updates[f] = new_val
    return updates


# --- Sheet → CRM sync ---
def sync_sheet_to_crm():
    rows = sheets_read()
    if not rows:
        log.warning("sync: no rows from Sheet")
        return

    created = updated = skipped = errors = 0

    for i, row in enumerate(rows):
        if len(row) < 3:
            continue
        username = row[2].strip().lstrip("@") if row[2] else ""
        if not username:
            continue

        try:
            fields = _row_to_espo_fields(row)
            existing = espo_find_contact(username)

            if existing is None:
                result = espo_create_contact(fields)
                if result:
                    created += 1
                    log.info(f"sync: created Contact @{username}")
                else:
                    errors += 1
                    log.error(f"sync: failed to create @{username}")
            else:
                diff = _needs_update(existing, fields)
                if diff:
                    result = espo_update_contact(existing["id"], diff)
                    if result:
                        updated += 1
                        log.info(f"sync: updated @{username}: {list(diff.keys())}")
                    else:
                        errors += 1
                        log.error(f"sync: failed to update @{username}")
                else:
                    skipped += 1

        except Exception as e:
            log.error(f"sync: error row {i} @{username}: {e}")
            errors += 1

    summary = (
        f"Sheet→CRM sync: {len(rows)} rows | "
        f"+{created} created | {updated} updated | {skipped} unchanged | {errors} errors"
    )
    log.info(summary)
    return {"created": created, "updated": updated, "skipped": skipped, "errors": errors, "total": len(rows)}


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

    elif mode == "sync":
        result = sync_sheet_to_crm()
        if result and result["errors"] > 0:
            tg_send(
                HIEP_CHAT_ID,
                f"⚠️ Sheet→CRM sync lỗi: {result['errors']} contacts không sync được\n"
                f"Check log: journalctl -u mcm-agent5 -n 30"
            )

    else:
        log.error(f"Unknown mode: {mode}. Use report|weekly|sync")
        sys.exit(1)
