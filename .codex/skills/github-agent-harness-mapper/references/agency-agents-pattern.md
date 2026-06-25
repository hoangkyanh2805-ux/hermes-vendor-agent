# agency-agents Pattern

Use this reference when mapping msitarzewski/agency-agents or similar agent roster repos.

## What To Extract

Extract the role framework, not the full catalog:

```text
division -> agent file -> identity -> mission -> workflow -> deliverables -> metrics -> style
```

Useful fields:

- Agent name
- Specialty
- When to use
- Identity and mission
- Responsibilities
- Not responsible for
- Workflow process
- Deliverables
- Success metrics
- Communication style
- Critical rules

## Contract Template

```text
AGENT ROLE:
SOURCE PATTERN:
POSITION IN WORKFLOW:
RECEIVES:
RESPONSIBILITY:
NOT RESPONSIBLE FOR:
TOOLS PERMITTED:
PRODUCES:
SUCCESS METRICS:
FAILURE BEHAVIOR:
HANDOFF TO:
HUMAN APPROVAL:
```

## Mapping Rules

- Keep only agents that match real repeated work in the target project.
- Prefer 3-7 agents for an operating workflow.
- Do not create a role for work that is already a simple function, script, or checklist.
- If one role owns too many cognitive jobs, split it.
- If two roles always need the same context and output, merge them.

## Good MCM Role Candidates

- Partner Growth Architect
- Lead Qualification Agent
- Onboarding Agent
- Daily Coaching Agent
- CRM/Payout Sync Agent
- SOP Auditor
- Reality Checker / QA Gate
