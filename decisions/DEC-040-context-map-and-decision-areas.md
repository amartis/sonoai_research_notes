---
id: DEC-040
title: A root context map in docs/README.md, decisions tagged by area, and workflow.md linked instead of imported
status: accepted
area: [workflow]
created: 2026-11-04
from: [DIS-016]
related: [DEC-011, DEC-021, DEC-031, DEC-032]
superseded_by:
---
# DEC-040: A root context map in docs/README.md, decisions tagged by area, and workflow.md linked instead of imported

## Context

[DIS-016](../discussions/DIS-016-load-only-relevant-context.md): the user wants Claude
to load only the context a task needs (progressive disclosure). Today `CLAUDE.md`
imports `docs/workflow.md` into every session, and nothing routes a task to the docs
and decisions of its area: `research_notes/INDEX.md` has no area column.

## Decision

- **Root file.** `docs/README.md` is the context map: under 2 kB, one row per area,
  each row naming the current doc(s) in `docs/`, the area's row in the per-area
  decisions table, and the code folder. `CLAUDE.md` says "start here" and links it.
  Lookup order for a task: map row → current doc (how things work now,
  [DEC-011](DEC-011-docs-vs-research-notes.md)) → accepted DECs of the area (why) →
  code.
- **Areas.** A fixed list: `data-security`, `datasets`, `labeling`, `training`,
  `workflow`, `infra`, `aws`. A new area is added by editing this list (a new DEC).
- **Decisions by area.** Every DEC gets an `area:` front-matter field (one or more of
  the areas). `research_notes/tools/build_index.py` generates an "Accepted decisions by
  area" table in INDEX.md that lists accepted DECs only; superseded and proposed ones
  stay in the full table. `build_index.py --check` fails when a DEC has no area or an
  unknown one. The templates gain the field.
- **workflow.md.** `CLAUDE.md` links `docs/workflow.md` with a line saying when to read
  it (records, board, branches, checks), instead of the `@docs/workflow.md` import.
  Rules that must apply in every session stay in, or move to, `CLAUDE.md`: the task
  status flow and who moves tasks to Done, the commit trailer, worktree start and end.
- **Agents.** Each agent's "Read first" list names its map row(s) instead of whole
  docs, beyond the hard rules in `CLAUDE.md`.
- Path-scoped rule files are used only after the Claude Code docs confirm they exist
  and how they load (open question in DIS-016).

## Consequences

- Instruction files loaded in every session shrink by about 2.5 k tokens (workflow.md).
  The larger gain, which is expected but not measured, is fewer whole docs read per task.
- Two places must be kept current: the map (by hand, when a doc or area is added) and
  each new DEC's `area:` (checked by `build_index.py --check`, so `scripts/check.sh`
  catches a missing one).
- Changing `CLAUDE.md`, agent files and skills is a guard change: merges wait for the
  user ([DEC-032](DEC-032-agent-roster-consult-and-lead-skills.md)).
- Board tasks: [TASK-073](../../backlog/tasks/task-073%20-%20Decision-areas-area-field-on-every-DEC-and-an-accepted-decisions-by-area-table-in-INDEX.md-DEC-040.md) (areas on DECs, per-area table, `--check`, templates) and
  [TASK-074](../../backlog/tasks/task-074%20-%20Context-map-in-docs-README.md-CLAUDE.md-links-workflow.md-instead-of-importing-it-agents-read-their-map-rows-DEC-040.md) (docs/README.md, CLAUDE.md, agents' read-first lists; depends on TASK-073).
