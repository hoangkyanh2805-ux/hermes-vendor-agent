---
name: github-agent-harness-mapper
description: Map proven GitHub agent repositories, especially agency-agents and LangGraph-style frameworks, into reusable agent roles, contracts, harness loops, state models, guardrails, HITL gates, project assets, and Codex/Claude skills. Use when Codex must avoid designing from scratch and instead extract patterns from existing repos, case studies, docs, or AI workflow examples for reuse across projects.
---

# GitHub Agent Harness Mapper

Use this skill to turn proven GitHub repositories into reusable AI operating assets. The default pairing is:

```text
agency-agents -> role/persona/contract layer
LangGraph -> harness/loop/state/checkpoint layer
```

Do not start by inventing a new architecture. Start from source repos, extract the mechanism, then map it into the target project.

## Core Rule

Map first, design second:

```text
Repo Pattern -> Extract Mechanism -> Agent Contract -> Harness Loop -> Guardrail -> Reusable Skill/Asset
```

Treat GitHub repos as reference implementations, not things to copy blindly. Preserve the pattern and adapt the surface.

## Workflow

1. Inventory sources: list each GitHub repo, doc, case study, Facebook post, video note, or local file.
2. Classify repo role:
   - role-framework: agent roster, personas, responsibilities, deliverables.
   - harness-framework: loop engine, state machine, graph, checkpoints, retries.
   - tool-framework: tools, MCP, APIs, execution environment.
   - ops-framework: observability, evals, deployment, runbooks.
3. Extract mechanism: identify structure, lifecycle, inputs, outputs, state, stop conditions, and reusable naming.
4. Map to target project: connect repo patterns to existing project agents, scripts, docs, data stores, cron jobs, webhooks, and sales/ops flows.
5. Create role contracts: use agency-agents style for agent identity, mission, responsibilities, output contract, metrics, and communication style.
6. Create harness loops: use LangGraph style for state, nodes, edges, checkpoints, retries, human interrupts, and observability.
7. Define guardrails: permissions, no-go actions, approval gates, fallback chain, error handling, and rollback.
8. Package assets: recommend or create docs, skills, commands, rules, templates, or runbooks that can be reused by future projects.

## Default Output

Produce these sections unless the user asks for a narrower artifact:

- Source inventory
- Repo roles and why they matter
- Extracted mechanisms
- Target project map
- Agent contract table
- Harness loop map
- State schema
- Tool and permission matrix
- Stop conditions and HITL gates
- Reusable assets to create
- Skill candidates
- SOP/Ops runbook outline
- Acceptance criteria

## Default Mapping For agency-agents + LangGraph

Use this pairing when the user mentions agency-agents, LangGraph, harness, loop, AI-Agent-Master, agent structure, or reusable project skills:

```text
agency-agents
  -> agents/
  -> role descriptions
  -> mission/workflow/deliverables
  -> success metrics
  -> communication style

LangGraph
  -> graph nodes
  -> state object
  -> edges / routing
  -> checkpoint / resume
  -> interrupt / human-in-the-loop
  -> tracing / debugging
```

Combined asset:

```text
agents/<agent-name>.md
skills/<workflow-skill>/SKILL.md
docs/agent-harness-map.md
docs/state-and-guardrails.md
docs/sop-ops-runbook.md
```

## MCM Default Map

For Hermes/MCM, map the 5-agent workflow like this:

```text
Agent 1 capture/qualify -> LangGraph node: capture_lead
Agent 2 onboarding D1-D7 -> node: onboard_partner
Agent 3 checklist/coaching/report -> node: daily_growth_loop
Agent 4 CRM sync/commission/rank -> node: sync_crm_and_payout
Agent 5 monitor/SOP audit -> node: audit_and_escalate
```

Shared state:

```text
lead_id, telegram_username, score, path, onboard_day, status,
activity_log, crm_event, commission_total, rank, retry_count,
last_checkpoint, needs_human, errors
```

## Reference Files

Read only what the task needs:

- references/agency-agents-pattern.md: use when extracting role/persona/agent contract patterns.
- references/langgraph-harness-pattern.md: use when mapping loop/state/checkpoint/HITL patterns.
- references/mapping-output-template.md: use when producing a saved plan, project map, or reusable asset.
- references/mcm-example-map.md: use when applying this skill to Hermes/MCM.

## Quality Bar

- Separate verified repo facts from inference.
- Name exactly which source repo pattern is being reused.
- Do not recommend copying an entire repo unless the user explicitly asks.
- Prefer small reusable assets over one giant document.
- Every loop must have state, retry limit, fallback, stop condition, and human approval rule.
- Every agent contract must say what the agent is not responsible for.
