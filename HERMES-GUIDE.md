# Hermes Setup & Deploy Guide - MCM Vendor

## Prerequisites

- VPS: AlmaLinux 9.x
- SSH: `ssh -p 2018 root@103.97.126.28`
- Workdir: `/root/hermes-vendor-agent`
- Services: `mcm-agent1`, `9router`, `hermes-gateway`
- Python 3.11+, pip, systemd
- Secrets live in `/root/.hermes/.env`, never in git.

## Directory Structure

```text
/root/hermes-vendor-agent/
  CLAUDE.md
  SOUL.md
  AGENTS.md
  HERMES-GUIDE.md
  scripts/
    agent1.py
    deploy.sh
  skills/
    agent1-capture.yaml
  prompts/
    qualify.txt
/root/.hermes/
  .env
  mcm-vendor-sa.json
  agent1_state.json
  agent2_state.json
  agent3_state.json
/root/logs/
```

## Step 1 - Clone Repo

```bash
ssh -p 2018 root@103.97.126.28
cd /root
git clone <repo-url> hermes-vendor-agent
cd /root/hermes-vendor-agent
mkdir -p /root/.hermes /root/logs
cp .env.example /root/.hermes/.env
nano /root/.hermes/.env
```

## Step 2 - Configure Env

```env
TELEGRAM_BOT_TOKEN=<telegram-bot-token>
TELEGRAM_HOME_CHANNEL=672890533
GOOGLE_SHEET_ID=<google-sheet-id>
GOOGLE_SERVICE_ACCOUNT_FILE=/root/.hermes/mcm-vendor-sa.json
OPENAI_API_KEY=<9router-or-openai-key>
OPENAI_BASE_URL=http://127.0.0.1:20128/v1
OPENAI_MODEL=kr/claude-sonnet-4.5
APP_PORT=3000
APP_HOST=0.0.0.0
WEBHOOK_SECRET=<random-secret>
LOG_LEVEL=INFO
LOG_DIR=/root/logs
```

## Step 3 - Google Service Account

1. Create Google service account.
2. Generate JSON key and upload to `/root/.hermes/mcm-vendor-sa.json`.
3. Share the Google Sheet with the service account email.
4. Enable Google Sheets API.

Test:

```bash
python3 - <<'PY'
import json
with open('/root/.hermes/mcm-vendor-sa.json') as f:
    sa = json.load(f)
print(sa['client_email'])
PY
```

## Step 4 - Python Environment

```bash
cd /root/hermes-vendor-agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

If `requirements.txt` is not present yet, install minimum runtime deps used by `scripts/agent1.py`:

```bash
pip install cryptography
```

## Step 5 - Agent 1 Systemd Service

Create `/etc/systemd/system/mcm-agent1.service`:

```ini
[Unit]
Description=MCM Vendor Agent 1 - Webhook Capture
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/hermes-vendor-agent
Environment="PATH=/root/hermes-vendor-agent/venv/bin"
EnvironmentFile=/root/.hermes/.env
ExecStart=/root/hermes-vendor-agent/venv/bin/python /root/hermes-vendor-agent/scripts/agent1.py
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=mcm-agent1

[Install]
WantedBy=multi-user.target
```

Enable/start:

```bash
systemctl daemon-reload
systemctl enable mcm-agent1
systemctl restart mcm-agent1
systemctl status mcm-agent1 --no-pager
```

Health:

```bash
curl http://localhost:3000/health
```

Expected:

```json
{"status":"ok","agent":"agent1-capture","version":"1.0.0"}
```

## Step 6 - Test Webhook

```bash
curl -X POST http://localhost:3000/webhook/capture \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "telegram_username": "@testuser123",
    "source": "x_post",
    "chat_id": 123456789,
    "timestamp": "2026-06-22T10:00:00Z"
  }'
```

Expected response:

```json
{"status":"accepted","message":"Lead received"}
```

## Step 7 - Cron Jobs

```bash
# Agent 2
0 8 * * * /root/hermes-vendor-agent/scripts/agent2-onboard.sh >> /root/logs/agent2.log 2>&1

# Agent 3
0 7 * * * /root/hermes-vendor-agent/scripts/agent3-checklist.sh >> /root/logs/agent3-checklist.log 2>&1
0 14 * * * /root/hermes-vendor-agent/scripts/agent3-coaching.sh >> /root/logs/agent3-coaching.log 2>&1
0 21 * * * /root/hermes-vendor-agent/scripts/agent3-report.sh >> /root/logs/agent3-report.log 2>&1

# Agent 5
0 20 * * * /root/hermes-vendor-agent/scripts/agent5-monitor.sh >> /root/logs/agent5.log 2>&1
0 21 * * 5 /root/hermes-vendor-agent/scripts/agent5-weekly.sh >> /root/logs/agent5-weekly.log 2>&1
```

Check timezone:

```bash
timedatectl
```

Target timezone: `Asia/Saigon`.

## Step 8 - Hermes Gateway

Hermes gateway handles admin DM/home channel behavior such as `/sethome`. If it is provided by Hermes CLI/service instead of this repo, do not invent `scripts/hermes-gateway.py`.

Check:

```bash
systemctl status hermes-gateway --no-pager
journalctl -u hermes-gateway -n 50 --no-pager
```

If gateway config/auth fails, inspect gateway logs and provider credentials in `/root/.hermes/.env`. Do not commit those values.

## Debug Commands

```bash
systemctl status mcm-agent1 hermes-gateway --no-pager
journalctl -u mcm-agent1 -n 80 --no-pager
journalctl -u hermes-gateway -n 80 --no-pager
curl http://localhost:3000/health
cat /root/.hermes/agent1_state.json | python3 -m json.tool
curl http://127.0.0.1:20128/health
curl http://127.0.0.1:20128/quota
```

## Common Errors

| Error | Cause | Fix |
|---|---|---|
| `Connection refused :3000` | Agent 1 down | `systemctl restart mcm-agent1` |
| Sheet auth fail | SA JSON missing/not shared | Upload JSON and share Sheet with SA email |
| Telegram API error | Bot token/chat ID issue | Check env and BotFather token |
| Provider authentication failed | Hermes gateway provider creds invalid | Check gateway logs and provider env |
| 9Router quota exceeded | LLM quota done | Use fallback or wait/reset quota |
| Cron not running | Timezone/syntax/service issue | Check `crontab -l`, `timedatectl`, logs |

## Deploy Script

`scripts/deploy.sh` should pull latest code, restart `mcm-agent1`, and health check. Keep it simple until Agents 2-5 exist.

```bash
cd /root/hermes-vendor-agent
git pull origin main
systemctl restart mcm-agent1
sleep 2
curl -s http://localhost:3000/health
```

## Security

1. Never commit `/root/.hermes/.env`.
2. Never commit Telegram bot token, OpenAI/9Router key, or Google SA JSON.
3. Rotate exposed secrets immediately.
4. Keep `.env.example` placeholder-only.
5. Validate webhook secret before production traffic if endpoint is public.

## Next Steps

1. Stabilize Agent 1 capture + Telegram replies.
2. Build Agent 2 onboarding scripts and prompts.
3. Build Agent 3 checklist/coaching/report.
4. Add EspoCRM webhook sync for Agent 4.
5. Add Agent 5 monitor/audit.