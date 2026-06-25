# AI Project Folder Structure Template

Use this as a decision framework, not a forced repo migration.

## Standard Folders

| Folder | Purpose |
|---|---|
| `agents/` or `.ai/agents/` | Agent contracts: goal, scope, loop, permissions, stop conditions |
| `skills/` | Reusable capabilities, modules, or procedural skills |
| `rules/` or `.ai/rules/` | Permission matrix, approval gates, data write policy, safety rules |
| `references/` or `knowledge/` | Source material, specs, case studies, schemas, business context |
| `actions/` or `playbook/` | Step-by-step workflows and operating playbooks |
| `build/`, `services/`, deployment docs | Build, deploy, rollback, service definitions, CI/CD |
| `ops/` | Daily/weekly/monthly operating rhythm |
| `audit/` | QA, evidence, SOP audits, incident reviews |
| `sales/` | Offers, scripts, decks, pricing, ROI calculators when project is commercial |
| `design/` or `web/` | UI specs, screen maps, dashboard definitions, screenshots |

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
  rules/
  references/
  actions/
  audit/
```

## Mapping Rule

Do not move working production files just to satisfy this structure. First document where things belong; migrate later only with tests and deploy awareness.
