# MCM Vendor AI Affiliate System

Multi-agent affiliate marketing automation for XAUUSD signals via X (Twitter).

## Quick Start

```bash
# Check system status
./scripts/status.sh

# View logs
tail -f /var/log/mcm-agent*.log

# Manual trigger
cd /root/hermes-vendor-agent
source /root/.hermes/.env
python3 scripts/agent2.py  # Test onboarding
python3 scripts/agent3.py checklist  # Test checklist
```

## Architecture

5 autonomous agents working together:

- **Agent 1 (Port 3000):** Capture leads via webhook → Q1/Q2 → Score → Sheet
- **Agent 2 (Cron 8AM):** Onboarding D1-D7 sequences
- **Agent 3 (Cron 7AM/2PM/9PM):** Daily checklist, coaching, reports
- **Agent 4 (Port 3001):** EspoCRM webhook sync
- **Agent 5 (Cron 8PM/9PM/hourly):** System monitoring + Sheet→CRM sync

## Strategy (Updated 2026-06-22)

**Platform:** X (Twitter) threads ONLY  
**Source:** Telegram channels (azaam, edric, alex)  
**Hashtags:** #xauusd #gold #forex  
**Workflow:** Copy signal → Rewrite 280 chars → Post  
**Target Geo:** Canada, Italy, Germany, UAE, France, Saudi Arabia, UK, Poland

## Files

```
/root/hermes-vendor-agent/
├── scripts/
│   ├── agent1.py          # Webhook capture + Q1/Q2
│   ├── agent2.py          # Onboarding D1-D7
│   ├── agent3.py          # Daily loop (3 modes)
│   ├── agent4.py          # CRM sync webhooks
│   ├── agent5.py          # System monitor
│   ├── run-agent*.sh      # Cron wrappers
│   ├── deploy.sh          # Deployment script
│   └── status.sh          # Quick status check
├── prompts/
│   ├── onboard-d1.txt → d7.txt
│   ├── checklist.txt
│   ├── coaching.txt
│   └── report-*.txt
├── CLAUDE.md              # Project spec
├── AGENTS.md              # Agent workflows
├── DEPLOYMENT.md          # Deployment status
└── README.md              # This file
```

## Services

```bash
# Check services
systemctl status mcm-agent1 mcm-agent4

# Restart services
systemctl restart mcm-agent1
systemctl restart mcm-agent4

# View service logs
journalctl -u mcm-agent1 -f
journalctl -u mcm-agent4 -f
```

## Cron Schedule (Vietnam UTC+7)

| Time | Agent | Purpose |
|---|---|---|
| 7:00 AM | Agent 3 | Checklist |
| 8:00 AM | Agent 2 | Onboarding |
| 2:00 PM | Agent 3 | Coaching |
| 8:00 PM | Agent 5 | Daily report |
| 9:00 PM | Agent 3 | Performance report |
| 9:00 PM Fri | Agent 5 | Weekly summary |
| Every hour | Agent 5 | Sheet→CRM sync |

## Environment Variables

Required in `/root/.hermes/.env`:

```bash
TELEGRAM_BOT_TOKEN=...
GOOGLE_SHEET_ID=...
GOOGLE_SERVICE_ACCOUNT_FILE=/root/.hermes/mcm-vendor-sa.json
OPENAI_API_KEY=...  # For 9Router
OPENAI_BASE_URL=http://127.0.0.1:20128/v1
ADMIN_CHAT_ID=672890533
```

## Development

```bash
# Test Agent 2 locally
cd /root/hermes-vendor-agent
source /root/.hermes/.env
python3 scripts/agent2.py

# Test Agent 3 modes
python3 scripts/agent3.py checklist
python3 scripts/agent3.py coaching
python3 scripts/agent3.py report

# Test Agent 5
python3 scripts/agent5.py report
python3 scripts/agent5.py sync
```

## Monitoring

```bash
# Quick status
./scripts/status.sh

# Live logs (all agents)
tail -f /var/log/mcm-agent*.log

# Check state files
cat /root/.hermes/agent1_state.json | jq
cat /root/.hermes/agent2_state.json | jq

# Test webhooks
curl http://localhost:3000/health
curl http://localhost:3001/health
```

## Troubleshooting

**Agent 1 not responding:**
```bash
systemctl restart mcm-agent1
journalctl -u mcm-agent1 -n 50
```

**Cron not running:**
```bash
crontab -l  # Verify schedule
grep CRON /var/log/syslog  # Check cron execution
```

**LLM errors:**
```bash
curl http://127.0.0.1:20128/v1/models  # Check 9Router
```

**Sheet errors:**
```bash
# Verify SA credentials
cat /root/.hermes/mcm-vendor-sa.json
# Check GOOGLE_SHEET_ID in .env
```

## Support

- **Admin:** Hiep Hoang (@hiephoang47)
- **VPS:** 103.97.126.28:2018
- **Docs:** See CLAUDE.md, AGENTS.md, DEPLOYMENT.md
