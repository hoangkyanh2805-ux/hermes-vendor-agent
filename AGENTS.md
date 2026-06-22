# MCM Vendor - 5 Agents Workflow

## Tom tat 5 agents

| Agent | Trigger | Role | Output |
|---|---|---|---|
| Agent 1 | Webhook POST `/webhook/capture` | Capture + qualify lead | Sheet append + Telegram Q1/Q2 + score Hot/Warm/Cold |
| Agent 2 | Cron 8AM daily | Onboard D1-D7 | Daily sequence -> Sheet `onboard_day++` |
| Agent 3 | Cron 7AM, 2PM, 9PM | Daily loop | Checklist + coaching + report |
| Agent 4 | EspoCRM webhook events | CRM sync | Event log + commission/rank sync |
| Agent 5 | Cron 8PM + GitHub webhook | Monitor + SOP audit | Report Hiep + GitHub action trigger |

## Lifecycle Lead - Capture den VIP

```
Lead submit form
  -> Agent 1 webhook capture
  -> Telegram Q1: channel?
  -> Telegram Q2: income goal?
  -> 9Router score: Hot/Warm/Cold
  -> Sheet append + Activity Log
  -> Telegram welcome: fast_track hoac nurture
  -> Agent 2 onboarding
  -> Agent 3 daily loop
  -> Agent 4 CRM sync
  -> Active / VIP / Churned
```

## Branch logic

FAST_TRACK (Hot):
- Agent 2 onboarding accelerated, 3-4 days.
- Sheet status: `Onboarding` -> `Active` on D4.
- Agent 3 sends immediate daily checklist.
- Target: first refer by D7.

NURTURE (Warm/Cold):
- Agent 2 onboarding standard, 7 days.
- Sheet status: `Onboarding`.
- Agent 3 soft checklist every 2 days.
- Target: first refer by D14.

## Flow 1 - Lead to Active

1. Landing page submits form.
2. Agent 1 receives `POST /webhook/capture`.
3. Agent 1 sends Telegram Q1.
4. State saved in `/root/.hermes/agent1_state.json`.
5. Agent 1 sends Q2 after Q1 answer.
6. Q1 + Q2 sent to 9Router scoring.
7. Affiliate Master receives new row.
8. Activity Log receives `lead_qualified` row.
9. Welcome template sent by Telegram.
10. Agent 2 picks up onboarding on next cron.

## Flow 2 - Refer Success

1. Affiliate posts link on TikTok/Telegram/Facebook/X.
2. Follower signs up.
3. EspoCRM emits `Opportunity.create`.
4. Agent 4 increments `refer_this_week` and `commission_total`.
5. Rank recalculated.
6. Agent 3 report says today's earn, rank, and gap to next rank.
7. If refer count > 10/week, tier becomes `VIP`.

## Flow 3 - No Activity to Re-engage

1. Agent 3 checks activity at 2PM.
2. If no post/reply for 3+ days, send coaching message.
3. If no reply for 7 days, Sheet flag becomes `needs_attention`.
4. Agent 2 requeues suitable onboarding content.

## Flow 4 - CRM Event to Sheet Sync

EspoCRM events:

- `Lead.create`: Agent 4 creates/updates Affiliate Master row and notifies Hiep.
- `Contact.status_change`: generate tracking link, send to affiliate, update Sheet.
- `Opportunity.create`: update commission and rank, next Agent 3 report reflects it.
- `Contact.total_earn_update`: sync earnings, recalc VIP tier, alert Agent 2 if promotable.

## State Management

Agent 1 state: `/root/.hermes/agent1_state.json`

```json
{
  "username1": {
    "lead_id": "AFF-20260622-001",
    "q1_answer": "TikTok",
    "q2_answer": "$5000/month",
    "score": "Hot",
    "path": "fast_track",
    "sheet_row_id": 42,
    "timestamp": "2026-06-22T10:00:00Z",
    "stage": "welcome_sent"
  }
}
```

Agent 2 state: `/root/.hermes/agent2_state.json`

```json
{
  "username1": {
    "onboard_day": 3,
    "path": "fast_track",
    "d1_sent": true,
    "d2_sent": true,
    "d3_sent": false,
    "next_send": "2026-06-24T08:00:00Z"
  }
}
```

Agent 3 state: `/root/.hermes/agent3_state.json`

```json
{
  "username1": {
    "last_checklist_7am": "2026-06-22T07:00:00Z",
    "last_coaching_2pm": "2026-06-21T14:00:00Z",
    "last_report_9pm": "2026-06-22T21:00:00Z",
    "refer_this_week": 3,
    "refer_last_week": 2,
    "rank": 12
  }
}
```

## Cron Schedule

```bash
# Agent 1: webhook service, no cron

# Agent 2
0 8 * * * /root/hermes-vendor-agent/scripts/agent2-onboard.sh

# Agent 3
0 7 * * * /root/hermes-vendor-agent/scripts/agent3-checklist.sh
0 14 * * * /root/hermes-vendor-agent/scripts/agent3-coaching.sh
0 21 * * * /root/hermes-vendor-agent/scripts/agent3-report.sh

# Agent 5
0 20 * * * /root/hermes-vendor-agent/scripts/agent5-monitor.sh
0 21 * * 5 /root/hermes-vendor-agent/scripts/agent5-weekly.sh
```

Timezone: Asia/Saigon.

## Error Handling

| Agent | Error | Action |
|---|---|---|
| Agent 1 | Webhook timeout >30s | Ack fast, background work, log fail if needed |
| Agent 1 | Sheet auth fail | Notify Hiep, log error, keep state |
| Agent 2 | Telegram API error | Retry 5 minutes later, log |
| Agent 3 | LLM quota exceeded | Use fallback template, log |
| Agent 4 | CRM webhook miss | Agent 5 audit/manual sync |
| Agent 5 | GitHub API fail | Log only, continue monitor |

## Communication Channels

- Agent 1 <-> Lead: Telegram DM.
- Agent 2 -> Affiliate: Telegram DM onboarding.
- Agent 3 -> Affiliate: Telegram checklist/coaching/report.
- Agent 4 <-> CRM: EspoCRM API/webhooks.
- Agent 5 -> Hiep: Telegram channel/DM.
- All agents -> Sheet: Google Sheets API.
- All LLM calls -> 9Router at `127.0.0.1:20128`.