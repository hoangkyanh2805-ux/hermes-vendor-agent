# Stop Condition Template

Agents should be designed to stop at the right time, not run forever.

## Common Stop Conditions

- Required input is missing or ambiguous.
- A tool/API fails repeatedly, default threshold: 3 attempts.
- A quota, budget, or rate-limit threshold is reached.
- Two sources of truth disagree and the conflict changes business outcome.
- The next action would delete data, spend money, publish externally, or alter payouts.
- The agent cannot verify that its last action succeeded.
- The result drifts from the stated goal.
- User approval is required by the permission matrix.

## Escalation Format

When stopping, report:

```text
Stopped because: <condition>
Goal affected: <goal>
Evidence: <logs/tool outputs/data>
Safe next options: <2-3 options>
Recommended option: <one option>
What approval/input is needed: <specific request>
```

## Retry Policy

Default:

- Retry transient tool failures up to 3 times.
- Do not retry validation failures without changing input/plan.
- After repeated failure, stop and escalate with evidence.
