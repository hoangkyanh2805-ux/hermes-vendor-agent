---
name: knowledge-asset-factory
description: Convert raw ideas, case studies, Facebook posts, video notes, GitHub repos, docs, and brainstorm transcripts into reusable knowledge assets. Use when Codex needs to ingest messy sources and produce distilled insights, frameworks, playbooks, project-specific maps, skill candidates, reusable templates, or assets that can be reused across multiple projects.
---

# Knowledge Asset Factory

Use this skill to turn scattered inputs into reusable project knowledge. Inputs may be local files, pasted notes, social posts, case studies, video summaries, GitHub repositories, or prior brainstorms.

## Core Rule

Do not merely summarize. Convert raw material into reusable assets:

```text
Raw Source -> Insight -> Principle -> Framework -> Project Map -> Reusable Asset -> Skill Candidate
```

A good output should help future projects move faster without rereading the original source.

## Workflow

1. **Inventory sources**: list source type, path/URL, author/context if known, and confidence level.
2. **Extract signal**: identify mechanisms, patterns, constraints, metrics, workflows, and claims worth reusing.
3. **Classify knowledge**: tag each insight as principle, framework, playbook, checklist, template, sales asset, agent loop, folder structure, tech pattern, or skill candidate.
4. **Map to current project**: explain what already exists, what is missing, what to delete/defer, and what can become an asset.
5. **Distill reusable assets**: produce concise frameworks, templates, checklists, prompts, folder maps, or skill outlines.
6. **Recommend storage**: place each asset in the right repo layer such as docs, knowledge, playbook, .codex/skills, .ai, or sales.
7. **Create next actions**: define what to save now, what to turn into a skill, what to test, and what to ignore.

## Default Output Shape

For each batch of sources, produce:

- Source inventory
- Key extracted insights
- Reusable frameworks
- Project-specific map
- Asset recommendations
- Skill candidates
- Suggested file paths
- Acceptance criteria

## Storage Model

Recommend this knowledge pipeline when the project lacks one:

```text
knowledge/
  raw/
    case-studies/
    facebook-posts/
    github-repos/
    video-notes/
  distilled/
    principles/
    frameworks/
    patterns/
    playbooks/
  reusable-assets/
    skills/
    templates/
    checklists/
    sales-assets/
  project-maps/
    <project-name>/
```

Do not force this structure into production projects. Prefer adding docs first, then folders when the user wants a reusable knowledge base.

## Reference Files

Read only what the task needs:

- `references/extraction-template.md`: use for extracting signal from messy sources.
- `references/classification-taxonomy.md`: use for classifying insights into reusable knowledge types.
- `references/reusable-asset-template.md`: use when producing templates, checklists, playbooks, or sales assets.
- `references/project-map-template.md`: use when mapping source material into the current repo/project.
- `references/skill-candidate-template.md`: use when deciding whether an insight should become a Codex skill.

## Quality Bar

- Separate source facts from your inferences.
- Preserve the mechanism, not just the headline.
- Prefer reusable frameworks over one-off notes.
- Mark low-confidence claims when a source is incomplete or not directly verified.
- Do not recommend building tools before identifying the reusable pattern and current project gap.
- Do not store long raw pasted content in final docs unless explicitly requested; distill it.
