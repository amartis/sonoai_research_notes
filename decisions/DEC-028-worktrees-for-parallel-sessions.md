---
id: DEC-028
title: Each session works in its own git worktree, made by scripts/worktree.sh
status: accepted
created: 2026-10-30
from: []
related: [DEC-007]
superseded_by:
---
# DEC-028: Each session works in its own git worktree, made by scripts/worktree.sh

## Context

[DEC-007](DEC-007-session-branches-no-worktrees.md) kept every session in the main
checkout, one branch at a time, because worktrees lack the gitignored pieces the work
needs (`.env`, `CLAUDE.local.md`, the nested `research_notes/` repo) and left stray
checkouts. By 2026-10-30 two sessions often ran at once. In one checkout they switched
branches under each other: commits landed on the wrong branch (one went straight to
`master`), and a branch name was reused. The user asked to use worktrees instead.

## Decision

- **One worktree per session** (one branch each), at `../ml_research-wt/<topic>` (a sibling
  of the repo, outside the data roots), on branch `claude/<topic>` from `master`.
- **Made and removed only by `scripts/worktree.sh`** (`new`, `list`, `remove`). `new` links
  the main checkout's `.env`, `CLAUDE.local.md`, `research_notes/` and `logs/` into the
  worktree, so data roots, the patient-data hook, notes and the cloud log are the same
  everywhere.
- **Code runs from the worktree's own `src/`**: the default venv's editable install points
  at the main checkout, so pytest sets `pythonpath = ["src"]`, `scripts/check.sh` exports
  `PYTHONPATH` to its own `src/`, and `new` writes `.worktree-env` (source it in a shell).
- **The main checkout stays on `master`**: merges happen there, with the user's go-ahead
  (`git merge --no-ff claude/<topic>`), and the board web UI shows it. Board edits made in a
  worktree reach the board when merged.
- A short read-only question or a one-line fix may still be done in the main checkout,
  only while no other session is editing there.
- The app's own `.claude/worktrees/` is not used.

## Consequences

- Sessions no longer collide; several can edit at once. The board's `touches:` line still
  tells which tasks would conflict at merge time.
- Every worktree must be removed after its merge (`scripts/worktree.sh remove <topic>`).
- A CLI started in a worktree without `.worktree-env` runs the main checkout's code.
- Supersedes DEC-007. To undo: remove the worktrees and restore DEC-007 with a new DEC.
