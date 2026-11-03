---
id: DIS-014
title: Show on the board which tasks are ready to start
status: concluded
created: 2026-11-03
outcomes: [DEC-038]
related: [DEC-016, DEC-032]
---
# DIS-014: Show on the board which tasks are ready to start

## Question

The user wants tasks that are ready to start to stand out on the Backlog.md board.
Readiness today exists only in the output of `scripts/ready_tasks.py`. A task is ready
when it is To Do, all its dependencies are Done, it has no `needs-decision` label, and
its `touches` overlap no In Progress task. Readiness is therefore derived: it changes
whenever another task's status, dependencies, labels or touches change, or a task is created.

## Options considered

- **How it shows**:
  - A label `ready` set by a script: it shows on each card, and statuses stay as
    they are ([DEC-016](../decisions/DEC-016-notes-hook-backlog-features.md)).
  - A new status Ready: it would flip back to To Do whenever an overlapping task starts.
  - A read-only "Ready now" page: nothing shows on the cards.
- **When it refreshes**:
  - Backlog.md's `onStatusChange` config key (found in the 1.55.3 binary, passes
    `$OLD_STATUS` and `$NEW_STATUS`): catches status moves.
  - A Claude Code PostToolUse hook after `backlog task create/edit`: catches agent
    edits of deps, labels and descriptions.
  - git post-merge and board start (already run `board_mirror.py`).
  - A file watcher: catches everything, but adds a long-running process.

## Conclusion

The user chose the label, refreshed by three hooks: Backlog.md `onStatusChange`, a
Claude PostToolUse hook, and git post-merge (plus board start)
([DEC-038](../decisions/DEC-038-ready-label-derived-by-script.md)). No file watcher.
Board task: [TASK-067](../../backlog/tasks/task-067%20-%20Derived-ready-label-on-board-tasks-synced-by-ready_tasks.py-DEC-038.md).

## Open questions

- Whether `onStatusChange` also fires for status changes made in the web UI
  (checked in TASK-067). Web UI edits of deps or labels are caught only at the next hook.
