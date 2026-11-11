---
id: DIS-025
title: Where a task's planned steps and their results are recorded
status: concluded
created: 2026-11-11
outcomes: [DEC-055]
related: [DEC-016, DEC-031, DEC-032]
---
# DIS-025: Where a task's planned steps and their results are recorded

## Question

The user asked where the result of a task's work is recorded, and proposed keeping the
planned steps in the task and a result for each step beside them.

Today (docs/workflow.md, "When you are assigned a task") an agent sets an Implementation
Plan with `--plan` at the start, logs Implementation Notes with `--append-notes`, and ends
with a Final Summary (`--final-summary`). Experiment numbers go in EXP records; code
changes in commits with `Refs: TASK-NNN`. The task file and "the backlog" are the same
thing: board tasks replaced the old TSK records.

Count over the 101 board task files on 2026-11-11: 20 have a plan, 75 have notes,
60 have a final summary. Plans are written as one long line ("1. ... 2. ..."), and notes
are free text that do not say which step they belong to.

## Options considered

- **A: numbered plan, one result note per step**: the plan has one numbered step per line;
  after each step the agent appends a note "Step N: ..." (done, skipped or changed, and
  the result). Uses existing CLI flags (`--plan`, `--append-plan`, `--append-notes`;
  backlog 1.55.3). Plan and results stay separate sections, linked by step number.
- **B: steps as Definition of Done items**: each step a `--dod` checkbox, ticked with
  `--check-dod`. Gives a checkbox view on the board, but mixes steps with the real
  completion rules, and a checkbox holds no result text.
- **C: leave as is**: no cost, but the plan is mostly missing and results are hard to
  match to steps.

## Conclusion

The user chose A on 2026-11-11: [DEC-055](../decisions/DEC-055-task-plan-steps-and-step-results.md). The rule text change is board
task [TASK-115](../../backlog/tasks/task-115%20-%20Agents-write-a-numbered-plan-one-step-per-line-and-one-result-note-per-step-DEC-055.md).

## Open questions

None.
