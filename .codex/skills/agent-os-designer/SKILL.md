---
name: agent-os-designer
description: Design reusable AI agent operating systems for projects. Use when Codex needs to convert prompts, workflows, scripts, business processes, or messy AI project docs into goal-driven agent loops with tools, permissions, checks, stop conditions, human approval gates, and an AI-friendly project folder structure. Also use when auditing a repo to make it agent-ready or creating reusable agent contracts across projects.
---

# Agent OS Designer

Use this skill to turn a project, workflow, or business process into an agent-ready operating model. The output should help another agent work safely without relying on one-off prompts.

## Core Rule

Do not start by writing prompts. Start by designing the operating system around the work:

```text
Goal -> Loop -> Tool -> Check -> Stop -> Human Approval
```

Prompts are short-term instructions. Agent contracts, skills, commands, rules, references, actions, and folder structure are the long-term operating memory.

## Workflow

1. **Ground in the project**: inspect existing docs, scripts, workflows, folders, deployment notes, and current automation before proposing structure.
2. **Identify repeated work**: find workflows that happen daily, weekly, per lead/customer/ticket/content item, or per deployment.
3. **Convert work into agent loops**: for each workflow define goal, scope, inputs, tools, loop, checks, outputs, logs, stop conditions, and human approvals.
4. **Define permissions**: separate safe autonomous actions from actions requiring human approval.
5. **Map folder structure**: map the repo's current files into an AI project structure; include agents, skills, commands, rules, references, actions, build/deploy, ops, audit, and sales layers where relevant; prefer adding documentation layers before moving production files.
6. **Produce implementation artifacts**: write a plan or docs for agent contracts, permission matrix, stop conditions, approval gates, and folder structure.
7. **Keep it portable**: avoid project-specific assumptions unless the user asks for a project-specific skill or template.

## Default Deliverables

For an audit or design task, produce these sections:

- Current state summary
- Candidate agent loops
- Agent contracts
- Permission matrix
- Stop conditions and escalation gates
- Recommended AI project folder structure
- Files/docs to add
- Test and acceptance criteria

If asked to create files, default to:

```text
docs/agent-loop-operating-model.md
docs/ai-project-folder-structure.md
docs/permission-matrix.md
docs/human-approval-gates.md
```

For a reusable template layer, recommend:

```text
.ai/
  agents/
  skills/
  commands/
  rules/
  references/
  actions/
  audit/
```

## Reference Files

Read only the references needed for the task:

- `references/agent-contract-template.md`: use when defining one or more agent/workflow contracts.
- `references/folder-structure-template.md`: use when auditing or proposing project folders, including AI-Agent-Master style agents/skills/commands/rules/references.
- `references/permission-matrix-template.md`: use when deciding what agents may do autonomously.
- `references/stop-condition-template.md`: use when defining escalation, retry, failure, and stop rules.
- `references/project-audit-checklist.md`: use when auditing an existing repo or process.

## Design Standards

- Prefer simple workflows over complex multi-agent systems unless complexity clearly improves outcomes.
- Prefer explicit logs, checkpoints, and human approval gates for risky actions.
- Never allow agents to delete production data, spend money, send mass messages, publish externally, or change payouts without an approval gate unless the user explicitly defines that authority.
- Treat folder structure as an interface for agents: every important fact should have a discoverable home.
- Keep production refactors separate from documentation/operating model work unless explicitly requested.

