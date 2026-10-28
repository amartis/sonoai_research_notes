---
id: DEC-016
title: Pre-commit hook for research_notes; Backlog decision, doc and draft features unused
status: accepted
created: 2026-10-28
from: [DIS-003]
related: [DEC-009, DEC-011, DEC-012]
superseded_by:
---
# DEC-016: Pre-commit hook for research_notes; Backlog decision, doc and draft features unused

## Context

The code repo refuses data files and stale notebooks in a pre-commit hook
(DEC-009); `research_notes/` has no hook, only its `.gitignore`, which
`git add -f` bypasses. The code hook cannot be reused as is: it blocks every
`.xlsx`, while DEC-012 allows the labeling-project tag table in dataset
version folders, and notes need an `INDEX.md` check instead of lint.
Separately, `backlog init` created `backlog/decisions/`, `docs/` and `drafts/`.
They are empty and untracked (git keeps no empty folders), and the CLI
recreates them, but using those features would start a second set of
decisions and docs next to DEC records and `docs/`.

## Decision

- **Notes hook**: `research_notes/.githooks/pre-commit`, committed in the
  notes repo and enabled once per clone with
  `git config core.hooksPath .githooks`. On the staged files it:
  - refuses images, tables, archives, checkpoints, arrays and encrypted
    blobs, except `datasets/*/label_projects.xlsx` (DEC-012); `.svg` plots are
    allowed;
  - refuses any staged file over 1 MB, with the same exception;
  - runs `python3 tools/build_index.py --check`, so `INDEX.md` stays current.

  It must take about a second. The notes README names the setup step.
- **Backlog features**: Backlog's decisions, docs and drafts are not used.
  Decisions are DEC records in `research_notes/`, docs go in `docs/`
  (DEC-011), and new tasks start in Triage (or To Do for small obvious ones,
  DEC-009), not as drafts. The empty folders are left alone.

## Consequences

- A forced add of a data file into the notes is refused, as in the code repo.
- A notes commit with a stale `INDEX.md` fails; run `build_index.py` first.
- One place each for decisions, docs and tasks.
