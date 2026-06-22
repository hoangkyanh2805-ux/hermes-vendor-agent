# MCM Vendor — AI Affiliate System

Hệ thống affiliate XAUUSD tự động dùng 1 Hermes Agent + 5 skills.  
Tự động capture lead, qualify, onboard 7 ngày, daily coaching, CRM sync, và monitor tiến độ.

---

## Architecture

```
Landing Page Form
    │
    ▼ POST /webhook/capture
┌─────────────────┐
│  Agent 1        │  Capture & Qualify
│  port :3000     │  → Telegram Q1/Q2 → Score Hot/Warm/Cold
│  systemd        │  → Google Sheet append
└────────┬────────┘
         │ triggers
    ┌────▼─────┐      ┌────────────┐      ┌──────────────┐
    │ Agent 2  │      │  Agent 3   │      │  Agent 4     │
    │ Onboard  │      │ Daily Loop │      │  CRM Sync    │
    │ 7-day D1-D7│    │ 7AM/2PM/9PM│      │  port :3001  │
    │ cron 8AM │      │ cron       │      │  EspoCRM whk │
    └──────────┘      └────────────┘      └──────────────┘
                                                │
                                    ┌───────────▼──────────┐
                                    │  Agent 5 — Monitor   │
                                    │  8PM daily + Fri 9PM │
                                    │  GitHub + SOP audit  │
                                    └──────────────────────┘
```

**Stack:** Hermes v0.17 · Claude Sonnet 4.5 via 9Router · Telegram Bot · Google Sheets · EspoCRM Docker

---

## Quick Deploy (VPS AlmaLinux)

```bash
# 1. Clone
ssh -p 2018 root@YOUR_VPS_IP
git clone https://github.com/YOUR_ORG/hermes-vendor-agent /root/hermes-vendor-agent
cd /root/hermes-vendor-agent

# 2. Config
mkdir -p /root/.hermes
cp .env.example /root/.hermes/.env
nano /root/.hermes/.env          # điền keys
# Upload Google SA JSON:
# scp -P 2018 mcm-vendor-sa.json root@VPS:/root/.hermes/

# 3. EspoCRM
docker compose up -d
# Mở http://VPS_IP:8080 → đăng nhập admin / mật khẩu từ .env

# 4. Services
cp services/mcm-agent1.service /etc/systemd/system/
cp services/mcm-agent4.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now mcm-agent1 mcm-agent4

# 5. Cron (crontab -e)
0 1 * * * /root/hermes-vendor-agent/scripts/run-agent2.sh >> /var/log/mcm-agent2.log 2>&1
0 0 * * * /root/hermes-vendor-agent/scripts/run-agent3.sh checklist >> /var/log/mcm-agent3.log 2>&1
0 7 * * * /root/hermes-vendor-agent/scripts/run-agent3.sh coaching  >> /var/log/mcm-agent3.log 2>&1
0 14 * * * /root/hermes-vendor-agent/scripts/run-agent3.sh report   >> /var/log/mcm-agent3.log 2>&1
0 13 * * * /root/hermes-vendor-agent/scripts/run-agent5.sh report   >> /var/log/mcm-agent5.log 2>&1
0 14 * * 5 /root/hermes-vendor-agent/scripts/run-agent5.sh weekly   >> /var/log/mcm-agent5.log 2>&1
* * * * * docker exec mcm-espocrm /usr/local/bin/php /var/www/html/cron.php > /dev/null 2>&1

# 6. Hermes SOUL.md
cp SOUL.md /root/.hermes/SOUL.md
# Cập nhật VPS IP, admin chat_id, và service URLs
```

---

## Required ENV Variables

| Var | Mô tả |
|-----|-------|
| `OPENAI_API_KEY` | 9Router API key (prefix `9r-`) |
| `OPENAI_BASE_URL` | `http://127.0.0.1:20128/v1` |
| `TELEGRAM_BOT_TOKEN` | Token từ @BotFather |
| `ADMIN_CHAT_ID` | Telegram user_id của PM |
| `GOOGLE_SHEET_ID` | ID từ URL của spreadsheet |
| `GOOGLE_SERVICE_ACCOUNT_FILE` | Path đến file JSON (trên VPS) |
| `ESPOCRM_URL` | `http://VPS_IP:8080` (dùng IP, không localhost) |
| `ESPOCRM_API_KEY` | Từ EspoCRM Admin > API Keys |
| `AFFILIATE_BASE_URL` | Base URL của tracking link |

---

## Google Sheet Schema

**Tab: Affiliate Master** (16 cột)

| Col | Name | Written by |
|-----|------|------------|
| A | lead_id | Agent 1 |
| B | name | Agent 1 |
| C | telegram_username | Agent 1 |
| D | source | Agent 1 |
| E | channel | Agent 1 (via LLM) |
| F | score | Agent 1 |
| G | path | Agent 1 |
| H | status | Agent 4 |
| I | onboard_day | Agent 2 |
| J | last_contact | Agent 2/3 |
| K | last_post | Agent 3 |
| L | refer_this_week | Agent 3/4 |
| M | refer_last_week | Agent 3 |
| N | total_earn | Agent 4 |
| O | rank | Agent 3 |
| P | notes | Manual |

**Tab: Activity Log** (8 cột): log_id, affiliate_id, agent, action, detail, timestamp, success, error_msg

---

## 5 Agents

| Agent | File | Trigger | Port |
|-------|------|---------|------|
| Capture | `scripts/agent1.py` | Webhook POST /webhook/capture | 3000 |
| Onboard | `scripts/agent2.py` | Cron 8AM daily | — |
| Daily Loop | `scripts/agent3.py` | Cron 7AM / 2PM / 9PM | — |
| CRM Sync | `scripts/agent4.py` | EspoCRM webhook (live) | 3001 |
| Monitor | `scripts/agent5.py` | Cron 8PM + Fri 9PM | — |

---

## Health Check

```bash
curl http://localhost:3000/health   # Agent 1
curl http://localhost:3001/health   # Agent 4
systemctl status mcm-agent1 mcm-agent4
systemctl --user status hermes-gateway
docker ps | grep espocrm
```

---

## Debug

```bash
journalctl -u mcm-agent1 -f                          # Agent 1 live logs
journalctl -u mcm-agent4 -f                          # Agent 4 live logs
cat /root/.hermes/agent1_state.json | python3 -m json.tool  # Lead states
bash scripts/run-agent2.sh                           # Manual agent2 run
bash scripts/run-agent3.sh checklist                 # Manual 7AM checklist
bash scripts/run-agent5.sh report                    # Manual monitor report
```

---

## EspoCRM Webhooks (4 events)

Registered via Admin > Webhooks trong EspoCRM UI hoặc API:

| Event | URL | Handler |
|-------|-----|---------|
| `Lead.create` | `http://VPS_IP:3001/webhook/espo/lead-create` | Append Sheet |
| `Opportunity.create` | `.../opportunity` | Update commission |
| `Contact.fieldUpdate.cStatus` | `.../status-change` | Grant tracking link |
| `Contact.fieldUpdate.cTotalEarn` | `.../commission` | Sync earnings |

EspoCRM cần cron job trên host để process webhook queue:
```bash
* * * * * docker exec mcm-espocrm /usr/local/bin/php /var/www/html/cron.php
```

---

## Adapt cho ngành khác

Chỉ thay:
- `prompts/qualify.txt` — 2 câu qualify phù hợp ngành
- `prompts/onboard-d1.txt` đến `d7.txt` — nội dung onboarding
- `prompts/checklist.txt` — daily task theo ngành
- SOUL.md — context ngành cho Hermes

Giữ nguyên: 5 agent skeleton, 3 cron, EspoCRM stack, Agent 5.

---

## Bundle Pricing

| Tier | Giá | Bao gồm |
|------|-----|---------|
| Starter (self-setup) | $497 | Toàn bộ code + docs |
| Done-for-you | $1,997 | Setup + customize ngành |
| Enterprise | $4,997+ | Custom + training + support 3 tháng |
| Monthly SaaS | $197/tháng | Managed hosting + updates |

---

*MCM Vendor SOP Bundle v1.0 · 2026 · Powered by Hermes + Claude Code*
