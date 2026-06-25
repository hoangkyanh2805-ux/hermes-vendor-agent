---
name: project-kickstart-os
description: Start new software, AI, automation, content, or business operating-system projects from an idea. Use when Codex needs to turn a vague concept, source materials, case studies, or a new repo into a build-ready project brief, first-principles requirements, folder structure, agent roles, skills/commands/rules/references, MVP build map, first sprint, and SOP/Ops runbook. This skill should orchestrate knowledge-asset-factory for source distillation and agent-os-designer for agent loops and AI project structure when those skills are available.
---

# Project Kickstart OS

Use this skill as the entrypoint when starting a new project from scratch or turning a rough idea into a build-ready repository.

## Core Rule

Do not start by coding. Start by creating the operating context that prevents the project from drifting:

```text
Idea -> Sources -> Brief -> Requirements -> Architecture -> Folder Structure -> Agent/Rules -> MVP Map -> Sprint -> SOP Ops
```

## How To Use Related Skills

If raw source material exists, first use `knowledge-asset-factory` to distill ideas, frameworks, and reusable assets.

If the project needs agent loops, permissions, commands, rules, or AI-friendly folder structure, use `agent-os-designer` patterns after the brief is stable.

This skill coordinates the kickoff and produces the initial project operating package.

## Workflow

1. **Collect inputs**: idea, user/client, outcome, constraints, source docs, target platform, deadline, budget, team, risk tolerance.
2. **Distill sources**: summarize source materials into mechanisms, frameworks, and project implications.
3. **Define the project brief**: objective, audience, success metrics, non-goals, constraints, assumptions.
4. **Write first-principles requirements**: business outcome, user workflows, data model, integrations, guardrails.
5. **Choose project shape**: app, automation, agent system, content engine, sales ops, internal tool, API/service, or hybrid.
6. **Design folder structure**: docs, knowledge, playbook, scripts/src, services, prompts, skills, rules, references, ops, audit, sales where relevant.
7. **Define agent/AI operating layer**: agent roles, skills, commands, rules, references, stop conditions, approval gates.
8. **Create MVP build map**: phases, critical path, deletion/defer list, acceptance criteria.
9. **Create first sprint**: tasks for the first 1-2 weeks with owner, output, verification, and dependencies.
10. **Create SOP/Ops runbook**: daily/weekly/monthly cadence, monitoring, escalation, backup, deploy, audit.

## Default Deliverables

When asked to plan only, return:

- Project brief
- Source distillation summary
- First-principles requirements
- Recommended folder structure
- Agent/AI operating layer
- MVP build map
- First sprint plan
- SOP/Ops runbook outline
- Acceptance criteria

When asked to create files, default to:

```text
docs/project-brief.md
docs/requirements.md
docs/mvp-build-map.md
docs/architecture.md
docs/sop-ops-runbook.md
docs/first-sprint.md
```

For AI-heavy projects, also recommend:

```text
.ai/agents/
.ai/rules/
.ai/references/
.ai/actions/
.ai/audit/
```

## Reference Files

Read only the references needed:

- `references/project-brief-template.md`: use for project definition and constraints.
- `references/requirements-template.md`: use for first-principles product/technical requirements.
- `references/folder-blueprint-template.md`: use for repo structure and AI operating layer.
- `references/mvp-build-map-template.md`: use for phases, critical path, and defer/delete decisions.
- `references/first-sprint-template.md`: use for first 1-2 week execution plan.
- `references/sop-ops-runbook-template.md`: use for daily/weekly/monthly ops, monitoring, escalation, deployment, and audit.

## Quality Bar

- Prefer a small, buildable first version over a large abstract system.
- Always identify what to delete/defer.
- Every phase must have observable acceptance criteria.
- Every recurring operation must have cadence, owner, input, output, and escalation path.
- Every risky action must have a human approval gate.
- Do not create folders/files unless the user asks to write artifacts.
