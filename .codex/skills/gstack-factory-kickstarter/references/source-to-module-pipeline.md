# Source To Module Pipeline

Use this pipeline when processing raw sources.

```text
Raw Source
  -> Source Inventory
  -> Mechanism Extraction
  -> Reusable Principle
  -> Target Project Map
  -> Module Candidate
  -> Module Contract
  -> Command Map
  -> QA Checklist
  -> Ship Package
  -> Install Gate
```

## Source Types

| Source | Extract |
|---|---|
| Case study | business mechanism, metric, tool stack, cadence |
| Video guide | setup steps, dependencies, secrets, deploy checks |
| Social post | insight, claim, framework, missing context |
| GitHub repo | architecture pattern, reusable workflow, host/runtime model |
| Brief | target market, ICP, action loop, KPI, module boundaries |

## Output Paths

```text
knowledge/distilled/<source>-mechanism.md
knowledge/project-maps/<source>-to-<target>.md
modules/<module>/module-contract.md
modules/<module>/qa-checklist.md
modules/<module>/install-guide.md
modules/<module>/rollback-plan.md
```

