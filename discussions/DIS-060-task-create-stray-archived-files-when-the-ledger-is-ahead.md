---
id: DIS-060
title: task-create leaves archived task files with another member's number when the ID ledger is ahead of the board
status: concluded
created: 2026-11-25
outcomes: [DEC-105]
related: [DIS-051, DIS-059, DEC-093]
---
# DIS-060: task-create leaves stray archived task files

## Question

`scripts/reserve_id.py task-create` runs the board CLI, which picks the next task number from the
board it can see. When another member has reserved that number in the ID ledger but their task is
not on master yet, the number is held, and [DEC-093](../decisions/DEC-093-id-ledger-number-reservations-task-claims-offline-modes.md) point 4 says the new task is archived and
created again. On 2026-11-25 this left four archived files with numbers another member holds.
Once that member's real tasks reach master, two files share one task ID and `scripts/check.sh`
fails. Merging master first does not help, because the other member's tasks are not on master yet.

## Options considered

- **Delete the new file** the CLI made seconds earlier, only when git does not track it and it is
  unchanged, then retry. No stray files, no ID clash; the retry loop stays.
- **Renumber the new file** to the next free ledger number (file name and id line). One CLI call
  instead of several, but the script edits task files by hand and breaks if the CLI's format changes.
- **Keep archiving**, and the member deletes the stray files by hand before committing.

## Conclusion

The user chose to delete the file: [DEC-105](../decisions/DEC-105-task-create-deletes-its-own-new-file-on-a-held-number.md),
carried by [TASK-273](../../backlog/tasks/task-273%20-%20task-create-deletes-its-own-new-task-file-instead-of-archiving-it-when-another-member-holds-the-number-DEC-105.md).

## Open questions

None.
