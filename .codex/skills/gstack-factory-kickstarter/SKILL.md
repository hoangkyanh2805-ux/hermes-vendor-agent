---
name: gstack-factory-kickstarter
description: Create a new GStack-style factory repository from briefs, case studies, video guides, social posts, GitHub repos, or brainstorms. Use when Codex needs to design a central production-workshop repo that turns raw sources into reusable LEGO modules, command workflows, skills, SOP runbooks, QA checklists, host adapters for Codex/Claude/Hermes, and safe install packages for runtime projects without modifying production repos first.
---

# GStack Factory Kickstarter

Use this skill to create or plan a new factory repo inspired by GStack. The factory repo is not the runtime product. It is the workshop that turns raw ideas into tested modules, skills, commands, and runbooks before anything is installed into a production/runtime repo.

## Core Rule

Do not patch the runtime project first. Manufacture the module in the factory first:

```text
Raw Source -> Extract Mechanism -> Module Contract -> Command OS -> QA -> Ship Package -> Install Gate -> Runtime Repo
```

The runtime repo stays stable. The factory repo absorbs ambiguity, experiments, source distillation, module design, QA checklists, and reusable asset production.

## Source Patterns

Use the factory for inputs like:

- case studies such as Landhold/ZeremAI
- video guides such as Hermes setup/deploy walkthroughs
- X/Facebook/LinkedIn posts
- GitHub repos such as GStack, agency-agents, LangGraph, Hermes Agent
- industry briefs such as forex, real estate, education, spa/clinic, SaaS
- brainstorm transcripts

## GStack-Inspired Layers

Design the new repo around these layers:

```text
Command skills       -> /extract /spec /autoplan /review /qa /ship /canary /retro /learn
Skill templates      -> SKILL.md.tmpl as source, generated SKILL.md as output
Host adapters        -> Codex, Claude, Hermes path/tool/capability rewrites
Browser QA           -> Playwright-style real flow testing when UI/web exists
JSONL learnings      -> decisions, module history, reusable patterns
Module packages      -> LEGO-style modules with install guides and rollback plans
Hermes orchestrator  -> intake, router, approval gate, cron/status, not deep reasoning
Runtime repo install -> only after QA and human approval
```

## Recommended Tech

Default to the lightweight GStack-style stack:

```text
Bun + TypeScript
Markdown SKILL.md.tmpl
Playwright for browser QA when needed
JSONL for learnings and module history
Git/GitHub for versioning
Markdown/HTML raw sources
```

Do not add Postgres, Redis, Docker, Next.js, FastAPI, LangGraph runtime, n8n, or dashboard UI until the factory has real need for them.

## Workflow

1. Clarify the factory objective: define what raw sources it will process and what modules it should manufacture.
2. Separate repo types:
   - factory repo: central workshop.
   - module: LEGO output inside factory.
   - runtime repo: stable production system that receives approved modules.
   - standalone repo: created only when a module is mature enough to deploy or sell separately.
3. Create source intake model: raw source paths, job files, source status, confidence, and owner.
4. Define command OS: extract, spec, autoplan, review, qa, ship, canary, retro, learn.
5. Define module contract: input, output, touched surfaces, forbidden surfaces, install path, rollback, test fixtures.
6. Define Hermes role: Hermes may receive briefs, create jobs, route commands, ask approvals, run cron/status reports. Hermes must not do deep strategic work, production edits, deployments, payouts, or pushes without approval.
7. Define VSCode/strong-model role: Claude/Codex in VSCode performs deep analysis, module design, skill writing, code review, and final artifact production.
8. Define host adapters: generate skills for .codex, .claude, and .hermes by rewriting paths, tool names, and suppressed features.
9. Define QA gates: static validation, module contract review, browser flow QA when applicable, install dry run, canary plan.
10. Define output package: module folder, skills, prompts, schemas, playbooks, sales assets, install guide, rollback plan.

## Default Repo Blueprint

Use this blueprint unless the target project requires a smaller variant:

```text
<factory-repo>/
  AGENTS.md
  README.md
  package.json
  bun.lock

  _refs/
    gstack/

  briefs/
  jobs/

  knowledge/
    raw/
      case-studies/
      video-guides/
      social-posts/
      github-repos/
    distilled/
    project-maps/

  skills-src/
    mcm-extract/SKILL.md.tmpl
    mcm-spec/SKILL.md.tmpl
    mcm-autoplan/SKILL.md.tmpl
    mcm-review/SKILL.md.tmpl
    mcm-qa/SKILL.md.tmpl
    mcm-ship/SKILL.md.tmpl
    mcm-canary/SKILL.md.tmpl
    mcm-retro/SKILL.md.tmpl
    mcm-learn/SKILL.md.tmpl

  hosts/
    codex.ts
    claude.ts
    hermes.ts

  scripts/
    gen-skill-docs.ts
    extract-source.ts
    validate-module.ts
    validate-skill.ts

  browser/
    qa-runner.ts

  modules/
    <module-name>/
      module-brief.md
      module-contract.md
      command-map.md
      agent-map.md
      qa-checklist.md
      install-guide.md
      rollback-plan.md
      prompts/
      schemas/
      skills/
      sales-onepager.md

  playbook/
  learnings/
    patterns.jsonl
    modules.jsonl
    decisions.jsonl

  tests/
    fixtures/
```

## Command Map

Use these commands as the first factory vocabulary:

| Command | Job |
|---|---|
| /mcm-extract | Extract mechanism from case study, post, video, or repo |
| /mcm-spec | Turn idea into spec and module contract |
| /mcm-autoplan | Create module plan with business, technical, and ops review |
| /mcm-review | Audit overbuild, missing guardrails, wrong tool copying, blast radius |
| /mcm-qa | Create and run QA checklist or browser flow test |
| /mcm-ship | Package docs, skills, playbook, install package |
| /mcm-canary | Monitor after install or deploy |
| /mcm-retro | Weekly learning, module quality, KPI review |
| /mcm-learn | Save winning and losing patterns into JSONL learnings |

## Module Contract Rule

Every module must answer:

```text
MODULE NAME:
SOURCE INPUTS:
TARGET RUNTIME:
BUSINESS GOAL:
INPUT CONTRACT:
OUTPUT CONTRACT:
TOUCHES:
DOES NOT TOUCH:
REQUIRED APPROVALS:
QA CHECKS:
INSTALL PATHS:
ROLLBACK PLAN:
SUCCESS METRICS:
```

## Hermes Role Rule

Use Hermes as the factory manager, not the deep brain:

```text
Hermes cheap model routes.
Claude/Codex strong model reasons.
Scripts validate.
Human approves.
```

Hermes can:

- receive briefs from Telegram or chat
- save raw source and job files
- classify task type
- suggest VSCode commands
- ask approval questions
- run reminders, cron digests, and status reports

Hermes must not autonomously:

- edit production runtime code
- deploy to VPS
- change payouts or commission
- send mass messages
- push GitHub commits
- create standalone repos

## Default Output

When planning a new factory repo, output:

- factory objective
- repo vs module vs runtime boundaries
- recommended tech stack
- folder blueprint
- command OS
- Hermes dispatcher role
- strong-model VSCode role
- first module pipeline
- QA/ship/install gates
- first sprint
- acceptance criteria

When writing files, create the repo operating package first, not production code.

## Reference Files

Read only what the task needs:

- references/module-contract-template.md: use when designing LEGO modules.
- references/factory-repo-blueprint.md: use when creating or reviewing repo structure.
- references/hermes-dispatcher-template.md: use when defining Hermes intake/router/approval behavior.
- references/source-to-module-pipeline.md: use when processing case studies, video guides, social posts, or GitHub repos.

## Quality Bar

- Keep the factory separate from runtime repos.
- Prefer module packages before standalone repos.
- Do not install a module into runtime without QA and human approval.
- Treat raw sources as immutable; write distilled/project-map outputs separately.
- Every module must have install and rollback instructions.
- Every risky action must have a human gate.
- The first version should manufacture one module end-to-end before adding UI or database.
