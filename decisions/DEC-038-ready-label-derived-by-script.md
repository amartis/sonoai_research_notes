---
id: DEC-038
title: A derived ready label on board tasks, kept in sync by ready_tasks.py from three hooks
status: accepted
area: [workflow]
created: 2026-11-03
from: [DIS-014]
related: [DEC-016, DEC-032, DEC-031]
superseded_by:
---
# DEC-038: A derived ready label on board tasks, kept in sync by ready_tasks.py from three hooks

## Context

[DIS-014](../discussions/DIS-014-ready-label-on-the-board.md): the user wants ready tasks
to stand out on the board. Readiness is computed by `scripts/ready_tasks.py` (rule in
docs/workflow.md) and changes whenever other tasks change.

## Decision

- A label `ready` marks the tasks `ready_tasks.py` lists as ready. Only
  `python scripts/ready_tasks.py --sync-labels` adds or removes it, editing only the
  `labels:` line. No person or agent sets it by hand. Statuses ([DEC-016](DEC-016-notes-hook-backlog-features.md)) do not change.
- The sync acts only in the main checkout; in a worktree it does nothing, so branches
  never carry label changes.
- It runs from:
  - Backlog.md `onStatusChange` in `backlog/config.yml`;
  - a Claude Code PostToolUse hook in `.claude/settings.json`, after Bash calls that run
    `backlog task create` or `backlog task edit`;
  - git post-merge and board start, through `scripts/board_mirror.py`;
  - once per `/lead` pass.
- Changed label lines are committed with the next board commit.

## Consequences

- The label line in committed task files changes as other tasks move.
- Web UI edits of deps or labels show up at the next hook run, not at once.
- Board task: [TASK-067](../../backlog/tasks/task-067%20-%20Derived-ready-label-on-board-tasks-synced-by-ready_tasks.py-DEC-038.md) (infra). It changes guards (`.claude/settings.json`, the `/lead`
  skill), so its merge waits for the user ([DEC-032](DEC-032-agent-roster-consult-and-lead-skills.md)).
