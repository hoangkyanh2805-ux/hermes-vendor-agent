# AI Project Folder Structure Template

Use this as a decision framework, not a forced repo migration.

## Standard Folders

| Folder | Purpose |
|---|---|
| `agents/` or `.ai/agents/` | Agent contracts: goal, scope, loop, permissions, stop conditions |
| `skills/` | Reusable capabilities, modules, or procedural skills |
| `commands/` | Slash-command style daily workflows such as build, spec, review, deploy, harden, monitoring |
| `rules/` or `.ai/rules/` | Permission matrix, approval gates, data write policy, naming conventions, project structure rules |
| `references/` or `knowledge/` | Source material, specs, case studies, schemas, business context |
| `actions/` or `playbook/` | Step-by-step workflows and operating playbooks |
| `build/`, `services/`, deployment docs | Build, deploy, rollback, service definitions, CI/CD |
| `ops/` | Daily/weekly/monthly operating rhythm |
| `audit/` | QA, evidence, SOP audits, incident reviews |
| `sales/` | Offers, scripts, decks, pricing, ROI calculators when project is commercial |
| `design/` or `web/` | UI specs, screen maps, dashboard definitions, screenshots |

## AI-Agent-Master Layer

For Claude/Codex-style projects, model the reusable operating layer as:

```text
.claude/ or .codex/
  agents/      role definitions and specialist personas
  skills/      packaged reusable know-how and procedures
  commands/    slash-command workflows for daily tasks
  rules/       project-wide laws and guardrails
  references/  deep reference docs and playbooks
```

Use this layer to stop repeating instructions in prompts. Agents define who acts, skills define how they act, commands define common entrypoints, rules define what must never be broken, and references provide deep context on demand.

## Recommended Minimal Layer

For an existing production repo, prefer adding docs first:

```text
docs/agent-loop-operating-model.md
docs/ai-project-folder-structure.md
docs/permission-matrix.md
docs/human-approval-gates.md
```

Only add `.ai/` when the user wants a reusable template layer:

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

## Mapping Rule

Do not move working production files just to satisfy this structure. First document where things belong; migrate later only with tests and deploy awareness.
