---
id: DEC-105
title: When the number the board CLI picked is held by another member, task-create deletes the task file it just created (untracked and unchanged) and retries, instead of archiving it (amends DEC-093 point 4)
status: accepted
area: [workflow]
created: 2026-11-25
from: [DIS-060]
related: [DEC-093]
superseded_by:
---
# DEC-105: task-create deletes its own new file on a held number

## Context

[DEC-093](DEC-093-id-ledger-number-reservations-task-claims-offline-modes.md) point 4: if another
member holds the number the board CLI chose, the new task is archived and created again. The
archived file keeps the held number, so two files share one ID once the other member's task reaches
master ([DIS-060](../discussions/DIS-060-task-create-stray-archived-files-when-the-ledger-is-ahead.md)).

## Decision

1. On a held number, `task-create` deletes the task file the board CLI just created and retries
   (up to 10 tries, as before).
2. It deletes only a file that git does not track and that is unchanged since the CLI wrote it. If
   the CLI also changed another file (for example a parent task), that change is undone too.
3. When any of that cannot be done safely, it stops and tells the member which task file is left
   and what to do; it never archives the file.

## Consequences

- No task file with another member's number is left on the board; DEC-093 point 4 now reads
  "deleted" instead of "archived".
- Code and docs: [TASK-273](../../backlog/tasks/task-273%20-%20task-create-deletes-its-own-new-task-file-instead-of-archiving-it-when-another-member-holds-the-number-DEC-105.md) (`scripts/reserve_id.py`, its tests, `docs/workflow.md`).
