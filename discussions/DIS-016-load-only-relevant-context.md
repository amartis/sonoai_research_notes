---
id: DIS-016
title: Load only the context a task needs - a root context map, and decisions tagged by area
status: concluded
created: 2026-11-04
outcomes: [DEC-040]
related: [DEC-011, DEC-021, DEC-031, DEC-032]
---
# DIS-016: Load only the context a task needs - a root context map, and decisions tagged by area

## Question

The user wants Claude to load only the context that bears on the task at hand. They
asked for the root files that Claude starts its context search from, and suggested
the decision records as one starting point. The question came out of a review of
Claude usage on 2026-11-04 (weekly plan limit at 54 % after about 2 of 7 days).

Measured on 2026-11-04 (one session, app context report):

- About 85 k tokens load before the first message. Of these, instruction files are
  about 9 k: `CLAUDE.md` (8 kB), `CLAUDE.local.md` (7 kB), the user's global
  `CLAUDE.md` (3 kB), and `docs/workflow.md` (9 kB). workflow.md loads every time
  because `CLAUDE.md` imports it with `@docs/workflow.md`. Tool, MCP-tool and skill
  definitions are most of the rest.
- `research_notes/INDEX.md` lists all 39 DEC and 15 DIS records with status, but has
  no area column, so it cannot route a task to the few decisions that apply.
- Large docs are read during tasks, for example `docs/label-guide.md` (37 kB).

The usual name for this pattern is progressive disclosure: a small root file is
always loaded and points to the rest, which is read only when a task needs it
(context engineering, more broadly). There is no standard name for the root file;
"context map" or "index" is common. Both terms are from general knowledge, not a
checked source.

## Options considered

- **Root file**:
  - **A**: a new `docs/README.md` context map, one row per area (current doc,
    accepted DECs, code folder), linked from `CLAUDE.md`. Small, hand-kept, in the
    main repo.
  - **B**: grow `research_notes/INDEX.md` into the map. One file, but it is generated
    and lives in a separate repo.
- **Decisions as the starting point**: a DEC records why something changed at one
  time. The current rule is often spread over several DECs, or a later one replaced an
  earlier one ([DEC-028](../decisions/DEC-028-worktrees-for-parallel-sessions.md) replaced [DEC-007](../decisions/DEC-007-session-branches-no-worktrees.md)). Starting from DECs means reading history to
  find the present. So DECs are the second hop, after the current doc
  ([DEC-011](../decisions/DEC-011-docs-vs-research-notes.md): docs/ say how things
  work now, research_notes/ say why).
- **Routing decisions by area**: an `area:` front-matter field on each DEC, and a
  generated "accepted decisions by area" table in INDEX.md that leaves out
  superseded ones. Alternative: hand-list DECs in the map (goes stale).
- **workflow.md**: keep the `@` import (always loaded), or replace it with a plain
  link and a line saying when to read it, moving the few rules that must always apply
  into `CLAUDE.md`.

## Conclusion

The user accepted all three defaults (2026-11-04):
[DEC-040](../decisions/DEC-040-context-map-and-decision-areas.md). Option A for the
root file; an `area:` field on DECs with a generated per-area table; workflow.md
linked, not imported. Board tasks: [TASK-073](../../backlog/tasks/task-073%20-%20Decision-areas-area-field-on-every-DEC-and-an-accepted-decisions-by-area-table-in-INDEX.md-DEC-040.md) (decision areas and the per-area index
table) and [TASK-074](../../backlog/tasks/task-074%20-%20Context-map-in-docs-README.md-CLAUDE.md-links-workflow.md-instead-of-importing-it-agents-read-their-map-rows-DEC-040.md) (context map, CLAUDE.md and agents' read-first lists).

## Open questions

- Whether Claude Code supports rule files scoped to paths, beyond a `CLAUDE.md` in a
  subfolder (loaded when Claude works in that folder). Not checked; TASK-074 checks it
  in the Claude Code docs before relying on it.
