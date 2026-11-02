---
id: DEC-031
title: DEC / DIS records and docs/ shown on the task board as read-only copies
status: accepted
created: 2026-11-02
from: []
related: [DEC-016, DEC-011, DEC-021]
superseded_by:
---
# DEC-031: DEC / DIS records and docs/ shown on the task board as read-only copies

## Context

The user asked (2026-11-02) to see documents and decisions on the Backlog.md
board, next to the tasks. [DEC-016](DEC-016-notes-hook-backlog-features.md) had ruled out Backlog's decisions and docs
features, so that records live in one place: DEC and DIS in `research_notes/`,
process docs in `docs/` ([DEC-011](DEC-011-docs-vs-research-notes.md)). Moving the records into Backlog would break
the DIS → DEC → TASK links, the index tool and about 100 links.

## Decision

Amends the "Backlog features" part of DEC-016; its notes-hook part stands.

- **Read-only copies**: `scripts/board_mirror.py` writes the DEC records to the
  board's Decisions page (`backlog/decisions/`, id `decision-NNN`, title
  `DEC-NNN: ...`, same status) and the DIS records and `docs/**/*.md` to its
  Documents page (`backlog/docs/discussions/`, `backlog/docs/project/`).
  Each copy starts with a line naming its source; relative links are
  rewritten so they still reach the same files.
- **Sources do not move**: edits go to the source; copies are overwritten on
  the next run. `backlog decision` and `backlog doc` are not used. Drafts stay
  unused.
- **Not in git**: the copies are gitignored, so there is no duplicate text in
  history and nothing to merge. They are refreshed when `scripts/servers.sh`
  starts the board, by the `post-merge` git hook, and by hand.
- Chosen by the user over moving the records into Backlog; scope DEC + DIS +
  `docs/` chosen by the user.

## Consequences

- One board shows tasks, decisions and docs; links still point at the
  sources.
- After editing a note without a merge, the board shows the old copy until
  `python scripts/board_mirror.py` runs.
- Anyone who edits a copy on the board loses the edit; the first line of
  every copy says so.
