---
id: DEC-011
title: docs/ describes how things work now; research_notes/ records why
status: accepted
created: 2026-10-28
from: [DIS-003]
related: [DEC-007, DEC-009]
superseded_by:
---
# DEC-011: docs/ describes how things work now; research_notes/ records why

## Context

DIS-003 asked whether `docs/` should move into `research_notes/`. Both hold
prose about the project, and without a rule it is unclear where a new text
goes. `CLAUDE.md` imports `@docs/workflow.md`; `research_notes/` is a separate
repo, gitignored in the code repo and absent on clones, the GPU box and RunPod
(DEC-007).

## Decision

- **`docs/` (code repo)**: how things work now: process (`workflow.md`),
  architecture and data flow (`diagrams/`), formats the code reads or writes.
  Edited in place to stay current, in the same commit as the code it describes.
- **`research_notes/` (own repo)**: why and what was found: DIS, DEC, EXP,
  journal, literature, dataset version records. Dated records; a change of
  mind is a new record that supersedes the old one.
- `docs/` stays in the code repo. Code, docstrings and `CLAUDE.md` cite
  `docs/` for formats and process; they may cite DEC/EXP ids for the why, but
  must not need `research_notes/` to be present.
- Where a notes README repeats the workflow, it links to `docs/workflow.md`
  instead.

## Consequences

- A text's home follows from what it is: current description → `docs/`,
  decision or finding → `research_notes/`.
- Format specs now in `research_notes/datasets/` move to `docs/` (DEC-012).
