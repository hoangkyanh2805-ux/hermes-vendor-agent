# Factory Repo Blueprint

Use this when creating a new GStack-style factory repo.

```text
<factory-repo>/
  AGENTS.md
  README.md
  package.json

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
  hosts/
  scripts/
  browser/
  modules/
  playbook/
  learnings/
  tests/
```

## Boundary Rules

- `knowledge/raw` is immutable source intake.
- `knowledge/distilled` contains extracted mechanisms.
- `knowledge/project-maps` maps mechanisms to a target project or industry.
- `modules` contains LEGO outputs.
- `skills-src` contains source templates.
- generated host-specific skills should be separated from source templates.
- runtime repos receive only approved module packages.

