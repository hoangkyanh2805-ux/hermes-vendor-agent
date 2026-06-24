# Spec-Driven Development

A 4-phase workflow: write the spec first, get alignment, then build. No surprise pivots, no wasted code.

## When to use

- Before building any new agent skill or feature (>30 min of work)
- When requirements are ambiguous or could be interpreted multiple ways
- When touching multiple files or systems (agent1 + agent2 + sheet schema)

## Phases

### Phase 1 — SPECIFY
Write a spec doc covering:
- **What** this does (one sentence)
- **Why** it's needed (user problem or business goal)
- **Inputs** (webhook payload, sheet row, env vars)
- **Outputs** (Telegram message, sheet update, log entry)
- **Edge cases** (LLM failure, missing chat_id, empty field)
- **Out of scope** (what this intentionally does NOT do)

Present the spec to the user. Wait for explicit approval before proceeding.

### Phase 2 — PLAN
Given the approved spec, list:
- Files to create or modify (exact paths)
- Functions to add or change
- New env vars or config needed
- Test scenarios (at least 2: happy path + 1 failure case)

Present the plan. Wait for approval.

### Phase 3 — TASKS
Break the plan into discrete, checkable tasks. Each task must be:
- One atomic change (one function, one file section, one config entry)
- Independently verifiable
- Marked with the agent it belongs to (agent1/agent2/agent3/agent4/agent5)

### Phase 4 — IMPLEMENT
Execute tasks in order. After each task:
- Mark it done in the task list
- If a task fails, stop and surface the blocker — don't skip ahead

## MCM Vendor context
- Agents: agent1 (capture), agent2 (onboard), agent3 (daily-loop), agent4 (crm-sync), agent5 (monitor)
- State files: `/root/.hermes/agent1_state.json`, `agent2_state.json`
- Sheet: Google Sheets "Affiliate Master" + "Activity Log"
- Fallback chain: kr/claude-sonnet-4.5 → gemini/gemini-2.0-flash → rule-based/hardcoded
- Commit convention: `feat:` / `fix:` / `done:` / `test:` / `blocked:` + `[agent-name]`
