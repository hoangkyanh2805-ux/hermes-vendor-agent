# Project Audit Checklist

Use this checklist before designing agent loops or folder structure.

## Repo/Project Facts

- What is the project objective?
- What are the main workflows?
- What folders already exist?
- What scripts/services run in production?
- What docs describe deployment and operations?
- What data stores are sources of truth?
- What external APIs/tools are used?

## Agent Readiness

- Are agent goals explicit?
- Are permissions explicit?
- Are stop conditions explicit?
- Are human approval gates explicit?
- Are logs/audits available?
- Are tests/checks available?
- Are fallbacks defined for quota/API failures?

## Folder Readiness

- Is there a place for agent contracts?
- Is there a place for reusable skills/actions?
- Is there a place for rules/guardrails?
- Is there a place for references/source material?
- Is there a place for build/deploy docs?
- Is there a place for ops cadence?
- Is there a place for audit/evidence?
- Is there a place for sales/offer assets if commercial?

## Output Recommendation

Classify each gap as:

- `document-now`: add docs/templates only
- `build-later`: useful but not blocking
- `production-risk`: needs approval and tests
- `delete/defer`: not needed or adds complexity
