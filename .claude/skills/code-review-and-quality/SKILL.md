# Code Review and Quality

5-axis review for every agent script change before merging or deploying to VPS.

## When to use

- After writing a new feature or fix in any agent script
- Before committing a `done:` or `fix:` commit
- When a bug was found in production (post-mortem review)

## The 5 axes

### 1. Correctness
- Does it handle the failure cases? (LLM timeout, 402 quota, Telegram rate limit, sheet API error)
- Is the fallback chain complete? (kr/ → gemini/ → rule-based/hardcoded)
- Are edge cases covered? (empty chat_id, missing sheet row, stale state file)
- Will this break existing affiliates who are mid-flow?

### 2. Readability
- Can someone reading this in 3 months understand what and why?
- Are variable names specific? (`chat_id` not `cid`, `lead_id` not `lid`)
- Is the happy path easy to trace top-to-bottom without jumping around?

### 3. Architecture
- Does this change belong in the right agent? (capture in agent1, daily loop in agent3)
- Is shared logic duplicated? (JWT/token generation, `tg_send`, `sheets_append_log`)
- Does this create a new dependency that wasn't in the original design?

### 4. Security
- No secrets hardcoded (API keys, bot tokens, sheet IDs)
- `HERMES_WEBHOOK_SECRET` validated on every webhook POST
- No user input fed directly to shell commands or SQL
- `.env` never committed (check `.gitignore`)

### 5. Performance / Reliability
- Timeouts set on all external calls (Sheets API, Telegram, LLM)
- No blocking calls in the webhook handler that could miss the 30s SLA
- State file reads/writes are atomic enough (no partial write corruption)
- Cron jobs don't overlap if they run long

## Output format

For each issue found:
```
[AXIS] File:line — description of the problem
Severity: critical / warning / suggestion
Fix: one-line recommendation
```

Then: overall verdict — **ship** / **fix then ship** / **rework needed**

## MCM Vendor context
- VPS: AlmaLinux 103.97.126.28
- Scripts: `/root/hermes-vendor-agent/scripts/`
- State: `/root/.hermes/agent1_state.json`, `agent2_state.json`
- Crons: agent2 8AM, agent3 7AM/2PM/9PM, agent5 8PM
- SLA: webhook → Telegram reply in <30 seconds
