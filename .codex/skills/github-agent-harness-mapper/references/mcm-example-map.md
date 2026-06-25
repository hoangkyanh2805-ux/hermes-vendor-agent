# MCM Example Map

Use this reference when applying agency-agents + LangGraph thinking to Hermes/MCM.

## Agent Contracts

| MCM Agent | agency-agents-style Role | LangGraph Node |
|---|---|---|
| Agent 1 | Lead Qualification Agent | capture_and_qualify |
| Agent 2 | Partner Onboarding Agent | onboard_partner |
| Agent 3 | Daily Growth Coach | coach_and_report |
| Agent 4 | CRM/Payout Sync Agent | sync_crm_payout_rank |
| Agent 5 | SOP Auditor / Incident Monitor | audit_and_escalate |

## Harness Loop

```text
lead_submit
  -> capture_and_qualify
  -> if Hot: fast_track_onboarding
  -> if Warm/Cold: nurture_onboarding
  -> daily_growth_loop
  -> crm_payout_sync
  -> audit_and_escalate
  -> active_vip_or_churned
```

## Shared State

```json
{
  "lead_id": "",
  "telegram_username": "",
  "score": "Hot|Warm|Cold",
  "path": "fast_track|nurture",
  "onboard_day": 0,
  "status": "new|onboarding|active|vip|churned|needs_attention",
  "activity_log": [],
  "crm_event": {},
  "refer_this_week": 0,
  "commission_total": 0,
  "rank": null,
  "retry_count": 0,
  "needs_human": false,
  "errors": []
}
```

## Human Gates

- Sheet auth fails.
- Telegram send fails repeatedly.
- CRM payout/rank update conflicts.
- Commission or payout amount changes.
- GitHub action or deployment action affects production.
- Agent cannot recover after 3 retries.

## Reusable Assets For MCM

- docs/mcm-agent-harness-map.md
- docs/mcm-state-and-guardrails.md
- docs/mcm-sop-ops-runbook.md
- .codex/skills/mcm-partner-growth-os/SKILL.md
