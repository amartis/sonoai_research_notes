---
id: DEC-087
title: Glossary gaps go to one proposals file (docs/glossary/proposals.md), filed by /consult, instead of one board task per gap
status: accepted
area: [workflow]
created: 2026-11-23
from: [DIS-045]
related: [DEC-057, DEC-072, DEC-073, DEC-084, DEC-038]
superseded_by:
---
# DEC-087: Glossary proposals file

## Context

Terms reviews turned every missing or changed glossary row into a follow-up board task (13 so
far). Each one needed a full task cycle, and global terms also waited for the user's choice
([DEC-073](DEC-073-how-new-terms-are-coined.md) point 4). The user wants one queue file instead
([DIS-045](../discussions/DIS-045-glossary-proposals-file-instead-of-glossary-tasks.md)).
DEC-073 point 4 is unchanged: the user still chooses global terms in `/consult`, and writers
still add epic rows themselves.

## Decision

1. **File.** `docs/glossary/proposals.md` holds one table, and its rows are never deleted:
   `ID | Term | Scope | Change | Meaning | Where used | Suggested by | Status`.
   - ID: `T<task>-<n>`, e.g. `T192-1`. Parallel branches get unique IDs without coordinating.
   - Scope: `global` or `epic <N>`. Change: `new`, `change` (to an existing row) or `rename`.
   - Where used: repo paths, record IDs and code identifiers. Never data file or folder names.
   - Suggested by: the agent name and TASK, e.g. `reviewer-t192-terms, TASK-192`.
   - Status: `open`; `filed <date> DIS-NNN` (the row is in the glossary, under the chosen
     name); or `rejected <date> DIS-NNN: <descriptive words to use>`.
2. **Who adds rows.** The writer adds them in its own branch, both for its own gaps and for
   the "add to glossary" findings of its terms reviewer that it does not fix in the branch.
   Any task may add rows to this file, whatever its `touches` line says. No task lists the
   file in `touches`, so the ready rule ([DEC-038](DEC-038-ready-label-derived-by-script.md): no In Progress task shares its touches) does
   not block on it. Glossary gaps no longer become board tasks. Other findings still become
   Triage tasks.
3. **Merges.** `.gitattributes` sets `docs/glossary/proposals.md merge=union`, so rows
   appended on parallel branches merge without a conflict. A light check in
   `scripts/check.sh` ([DEC-084](DEC-084-light-check-sh-slow-marker-auto-full-run.md)) fails on a duplicate ID or an invalid Status. That catches a
   row the union merge doubled.
4. **Filing.** When `/consult` runs with no topic, its list of what waits on the user includes
   the count of open rows. When the user takes the rows up, `/consult` gives the DEC-073
   point 4 proposal for each global row (the name, how it passes 1a-c, the phrase it
   replaces, one other name considered) and the new wording for each change or epic row.
   It then edits the glossary files in its consult worktree, sets each Status, removes the
   markers (point 6) and commits together with its board edits.
5. **Decision trace.** A closed row's Status names the consult's DIS. That DIS lists every
   term decided, with its proposal and outcome, and it is the record of the user's choice
   that the terms reviewer looks for. No DEC is written per term. A DEC is written only when
   a term choice changes a rule, as [DEC-085](DEC-085-global-term-checkpoint-backup.md) did.
6. **Marker.** A new global term with an open row carries one marker,
   `(proposed term <ID>)`, right after the term where it is defined (in the doc or record
   that defines it). Other uses are not marked, because the "Where used" cell lists them for
   a later rename. Epic terms and changes to existing rows get no marker.
7. **Terms review.** A new global term with an open row and the marker where it is defined
   is not a finding. A new global term with no row is a should-fix: "add a row to
   docs/glossary/proposals.md". Findings name the row to add, never a task.

## Consequences

- The lead and consult skills, the reviewer and writer agents, `docs/workflow.md`,
  `docs/agents.md`, `docs/glossary/README.md` and `CLAUDE.md` are changed to follow this
  ([TASK-229](../../backlog/tasks/task-229%20-%20Glossary-proposals-file-DEC-087-docs-glossary-proposals.md-with-union-merge-and-an-ID-and-Status-check-lead-consult-reviewer-and-writer-agents-and-workflow-docs-send-glossary-gaps-there-instead-of-tasks-seed-rows-from-TASK-215-and-TASK-184.md)).
- The open glossary tasks [TASK-215](../../backlog/tasks/task-215%20-%20Global-glossary-row-for-input-normalisation-Data.normalize-term-choice-in-consult-DEC-073-point-4-found-in-TASK-192.md) and [TASK-184](../../backlog/tasks/task-184%20-%20Glossary-row-for-W3-generalisation-gap-val-W1-minus-test-W1-per-organ-in-the-epic-1-glossary.md) become rows and are archived. [TASK-222](../../backlog/tasks/task-222%20-%20Glossary-the-S3-bucket-row-also-covers-encrypted-checkpoint-backups-under-runs-DEC-083.md) stays
  a task, because its wording was already decided (DEC-085).
- A global term may appear in merged docs before the user chooses it. If the user picks
  another name, the rename follows the row's "Where used" cell.
