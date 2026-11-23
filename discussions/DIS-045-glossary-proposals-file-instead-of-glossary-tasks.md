---
id: DIS-045
title: Glossary proposals file instead of one board task per missing or changed glossary row
status: concluded
created: 2026-11-23
outcomes: [DEC-087]
related: [DEC-057, DEC-072, DEC-073, DEC-084, DEC-085]
---
# DIS-045: Glossary proposals file instead of glossary tasks

## Question

Each terms review that finds a missing or changed glossary row turns into a follow-up board
task. There have been 13 so far ([TASK-126](../../backlog/archive/tasks/task-126%20-%20Glossary-rows-for-the-fact-relations-config-Visit-unit-Exclusive-set-Implied-tag-Second-pass-pair-Selector-Ignored-tag-DEC-057-DEC-059.md), 129, 138, 140, 160, 161, 162, 165, 172, 174, 184,
215, 222). Each one needs triage, a worktree, a branch and a merge, often for one or two table
rows. A global term also has to wait for the user's choice in `/consult` ([DEC-073](../decisions/DEC-073-how-new-terms-are-coined.md) point 4). The
user finds this cumbersome. They proposed a single file of glossary update proposals, where
each task adds a row (the suggested term, its meaning, who suggested it, where it is used)
instead of creating a task.

## Options considered

- **A: one task per gap (today).** Every gap shows on the board. Each gap costs a full task
  cycle, and global-term tasks sit in Triage until the user takes them to `/consult`.
- **B: one proposals file, appended by writers (chosen).** One queue, no task per term. Parallel
  branches append to the same file, so the file needs a union merge and a check for doubled
  rows.
- **C: one file per proposal.** No merge conflicts, but the queue is scattered over many files
  and the user asked for one file with rows.

## Conclusion

Option B, recorded in [DEC-087](../decisions/DEC-087-glossary-proposals-file.md). The user chose:

1. `/consult` writes the accepted glossary rows itself, in its consult worktree, and closes the
   proposal rows. No task is made for them. The user asked for a decision trace that stays slim.
   Each closed row's Status names the consult's DIS, and that DIS lists each term decided with
   its DEC-073 point 4 proposal. There is no DEC per term.
2. The file holds every glossary gap an agent cannot close itself: new global terms, changes to
   existing rows (global or epic), and epic rows a writer left out. Writers still add epic rows
   directly (DEC-073 point 4).
3. A branch that uses a global term the user has not chosen yet may merge once the term has an
   open proposal row. The user asked for a status marker in the docs only if it is really
   necessary. We agreed on one marker, `(proposed term <ID>)`, placed only where the term is
   defined. A reader of that doc has no other way to see that the name is not chosen yet, and
   the "Where used" cell already lists the other uses for a later rename.

Board: [TASK-229](../../backlog/tasks/task-229%20-%20Glossary-proposals-file-DEC-087-docs-glossary-proposals.md-with-union-merge-and-an-ID-and-Status-check-lead-consult-reviewer-and-writer-agents-and-workflow-docs-send-glossary-gaps-there-instead-of-tasks-seed-rows-from-TASK-215-and-TASK-184.md) (infra) implements DEC-087 and moves the open glossary tasks [TASK-215](../../backlog/tasks/task-215%20-%20Global-glossary-row-for-input-normalisation-Data.normalize-term-choice-in-consult-DEC-073-point-4-found-in-TASK-192.md) and
[TASK-184](../../backlog/tasks/task-184%20-%20Glossary-row-for-W3-generalisation-gap-val-W1-minus-test-W1-per-organ-in-the-epic-1-glossary.md) into the file. [TASK-222](../../backlog/tasks/task-222%20-%20Glossary-the-S3-bucket-row-also-covers-encrypted-checkpoint-backups-under-runs-DEC-083.md) stays a task, because its wording was already decided in [DIS-044](DIS-044-checkpoint-backup-term-and-presign-lifetime.md).

No new term is coined here: "glossary proposals file" and "proposal row" are descriptive words.

## Open questions

None.
