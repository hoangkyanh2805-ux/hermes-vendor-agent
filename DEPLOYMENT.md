# MCM Vendor AI Affiliate - Deployment Status

**Last Updated:** 2026-06-22 22:18 Vietnam Time  
**Status:** ✅ PRODUCTION READY

---

## Services Running

| Service | Port | Status | Command |
|---|---|---|---|
| Agent 1 (Capture + Telegram polling) | 3000 | ✅ Running | `systemctl status mcm-agent1` |
| Agent 4 (CRM Sync) | 3001 | ✅ Running | `systemctl status mcm-agent4` |
| Agent 3 (Trigger server) | 3002 | ✅ Running | embedded trong mcm-agent1 cron |
| Dashboard (mcm-web) | 3003 | ✅ Running | `systemctl status mcm-web` |
| EspoCRM Docker | 8080 | ✅ Running | `docker ps \| grep espocrm` |
| 9Router (LLM proxy) | 20128 | ✅ Running | `ps aux \| grep 9router` |

> **Note:** `hermes-gateway.service` không tồn tại. Agent 1 tự poll Telegram qua `AFFILIATE_BOT_TOKEN` trực tiếp trong systemd service — không cần Hermes Gateway.

---

## Cron Schedule (All times Vietnam UTC+7)

| Agent | Time | Cron | Purpose |
|---|---|---|---|
| Agent 2 | 8:00 AM daily | `0 8 * * *` | Onboarding D1-D7 |
| Agent 3 | 7:00 AM daily | `0 7 * * *` | Daily checklist |
| Agent 3 | 2:00 PM daily | `0 14 * * *` | Coaching |
| Agent 3 | 9:00 PM daily | `0 21 * * *` | Performance report |
| Agent 5 | 8:00 PM daily | `0 20 * * *` | System monitor |
| Agent 5 | 9:00 PM Friday | `0 21 * * 5` | Weekly summary |
| Agent 5 | Every hour | `0 * * * *` | Sheet→CRM sync |

---

## Strategy Configuration

### Platform
- **Primary:** X (Twitter) threads ONLY
- **Removed:** TikTok (no longer used)

### Content Source
- **Telegram channels:** azaam, edric, alex
- **Workflow:** Copy signal → Rewrite 280 chars → Post with hashtags

### Hashtags
- `#xauusd`
- `#gold`
- `#forex`

### Target Geo (8 countries)
- Canada
- Italy
- Germany
- United Arab Emirates
- France
- Saudi Arabia
- United Kingdom
- Poland

---

## Prompts Updated (12 files)

All prompts now reflect X-only strategy with Telegram signal rewrite workflow:

1. `onboard-d1.txt` - Welcome + workflow intro
2. `onboard-d2.txt` - X thread format guide + examples
3. `onboard-d3.txt` - Script mẫu copy-paste
4. `onboard-d4.txt` - Hook optimization
5. `onboard-d5.txt` - Scale 2-3 threads/day
6. `onboard-d6.txt` - Advanced tactics + A/B test
7. `onboard-d7.txt` - Graduation + 30-day roadmap
8. `checklist.txt` - Daily tasks for X threads
9. `coaching.txt` - Rewrite coaching
10. `qualify.txt` - Q1/Q2 scoring
11. `report-affiliate.txt` - Daily performance
12. `report-pm.txt` - PM summary for Hiep

---

## Agent Flow

```
Lead submits form
  ↓
Agent 1: Capture webhook (:3000)
  → Q1: Channel? (X selected)
  → Q2: Income goal?
  → 9Router scoring (Hot/Warm/Cold)
  → Sheet append (Affiliate Master + Activity Log)
  → Telegram welcome message
  ↓
Agent 2: Onboarding (cron 8AM)
  → D1-D7 sequence
  → Update onboard_day in Sheet
  → Status: Onboarding → Active (after D3)
  ↓
Agent 3: Daily Loop (cron 7AM/2PM/9PM)
  → 7AM: Checklist (rewrite Telegram signals to X threads)
  → 2PM: Coaching (if inactive/drop)
  → 9PM: Report (rank, earn, gap to next tier)
  ↓
Agent 4: CRM Sync (webhook :3001)
  → EspoCRM events → Sheet update
  → Commission, rank, tier calc
  ↓
Agent 5: Monitor (cron 8PM/9PM/hourly)
  → 8PM: Daily system report to Hiep
  → 9PM Fri: Weekly summary
  → Hourly: Sheet→CRM sync
```

---

## Test Data

**Lead:** hiephoang47 (@hiephoang47)
- Status: Onboarding
- onboard_day: 1
- Channel: x
- Score: Warm
- Path: nurture
- D1 sent: ✅ (tested successfully 2x today)
- Sheet row: 5

---

## Git Commits

```
0742d73 fix: X-only strategy - Telegram signals rewrite
979b943 fix: add geo targeting to checklist.txt
74f4180 update: focus X threads + 8 target countries
```

---

## Health Checks

```bash
# Check services
systemctl status mcm-agent1 mcm-agent4
curl http://localhost:3000/health
curl http://localhost:3001/health

# Check cron
crontab -l

# Check logs
tail -f /var/log/mcm-agent1.log
tail -f /var/log/mcm-agent2.log
tail -f /var/log/mcm-agent3.log
tail -f /var/log/mcm-agent5.log

# Check state
cat /root/.hermes/agent1_state.json
cat /root/.hermes/agent2_state.json

# Check Sheet
# https://docs.google.com/spreadsheets/d/GOOGLE_SHEET_ID
```

---

## Next Steps

1. ✅ All agents deployed
2. ✅ Cron schedules fixed
3. ✅ Strategy updated to X-only
4. ⏳ Monitor first real lead through full D1-D7 flow
5. ⏳ Verify Agent 3/5 cron executions tonight (8PM, 9PM)
6. ✅ EspoCRM webhooks configured — 4 events → http://103.97.126.28:3001/webhook/espo/*

---

---

## Recovery Procedures

### VPS reboot / service crash

```bash
# Restart webhook services
systemctl restart mcm-agent1 mcm-agent4

# Verify recovery
curl http://localhost:3000/health
curl http://localhost:3001/health

# Check cron still loaded (cron survives reboot)
crontab -l
```

### 9Router offline (LLM calls fail)

Symptoms: agents ghi log "llm error" liên tục, Telegram nhận FALLBACK messages.

```bash
# Check 9Router process
ps aux | grep 9router
# Restart (path depends on install)
/usr/local/bin/9router restart
# Verify
curl http://127.0.0.1:20128/v1/models
```

Fallback behavior: Agent 3 trigger dùng `FALLBACK` dict hardcoded — không crash, chỉ mất personalization. Agents 1/2 sẽ fail và ghi log error.

### Google Sheets API quota exceeded

Symptoms: `sheets_read error: HTTP 429` trong logs.

```bash
tail -f /var/log/mcm-agent3.log | grep -i quota
```

- Quota reset tự động sau 60 giây (read) hoặc 100 giây (write)
- Không cần làm gì — agents retry tự động ở cron tiếp theo
- Nếu liên tục: check số lượng affiliate × số cron/ngày — có thể cần tăng quota project

### EspoCRM Docker down

```bash
docker ps | grep espocrm
docker start mcm-espocrm
# hoặc
cd /root && docker-compose up -d
```

### Rollback deploy

```bash
# Xem recent commits
git -C /root/hermes-vendor-agent log --oneline -10

# Rollback 1 commit (agents cron — không cần restart)
git -C /root/hermes-vendor-agent revert HEAD --no-edit

# Rollback service agents (cần restart sau)
git -C /root/hermes-vendor-agent checkout <commit-hash> -- scripts/agent1.py scripts/agent4.py
systemctl restart mcm-agent1 mcm-agent4
```

### Agent state bị corrupt

```bash
# Backup trước
cp /root/.hermes/agent1_state.json /root/.hermes/agent1_state.json.bak

# Reset state sạch (agent sẽ re-process từ đầu)
echo '{}' > /root/.hermes/agent1_state.json
echo '{}' > /root/.hermes/agent2_state.json

# Cooldown/pending agent3
rm -f /root/.hermes/agent3_cooldown.json
rm -f /root/.hermes/agent3_pending.json
```

---

## Support

- **Admin:** Hiep Hoang (@hiephoang47, ID: 672890533)
- **VPS:** 103.97.126.28:2018
- **Workdir:** /root/hermes-vendor-agent
- **Logs:** /var/log/mcm-agent*.log
