# Folder Blueprint Template

Use this as a starting point, then adapt to the project.

```text
docs/
  project-brief.md
  requirements.md
  architecture.md
  mvp-build-map.md
  sop-ops-runbook.md
  first-sprint.md

knowledge/
  raw/
  distilled/
  reusable-assets/
  project-maps/

playbook/
  ops/
  sales/
  support/

.ai/
  agents/
  rules/
  references/
  actions/
  audit/

.codex/
  skills/

src/ or scripts/
services/
tests/
web/ or app/
config/
```

Rules:

- Do not move production files just to match this blueprint.
- Add docs first, refactor folders later.
- Keep raw source material separate from distilled knowledge.
- Keep reusable skills/assets separate from project-specific implementation.
