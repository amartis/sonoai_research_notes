---
id: DEC-055
title: Every board task gets a numbered plan, one step per line, and one result note per step
status: accepted
area: [workflow]
created: 2026-11-11
from: [DIS-025]
related: [DEC-016, DEC-031, DEC-032]
superseded_by:
---
# DEC-055: Every board task gets a numbered plan, one step per line, and one result note per step

## Context

A task's results are recorded in the task file itself: Implementation Notes while the
work runs and a Final Summary at Review; experiment numbers in EXP records. On
2026-11-11 only 20 of the 101 task files had a plan, plans were one long line, and notes
did not say which step they belonged to ([DIS-025](../discussions/DIS-025-task-plan-and-step-results.md)).

## Decision

- When an agent starts a task, it writes the Implementation Plan with `--plan` (and
  `--append-plan` for later steps): numbered steps, one per line.
- After each step, it appends one note with `--append-notes`, starting with its
  `[<name>]` tag, then `Step N:` and the outcome: done (with the result, counts and
  checks), skipped (why) or changed (what and why). A step added during the work is
  appended to the plan with the next number and gets its note the same way.
- Other notes (problems found, questions) stay allowed; they need no step number.
- The Final Summary stays the short outcome of the whole task. EXP records stay the
  place for experiment numbers and conclusions; a step note links the EXP instead of
  repeating them.
- The patient-data rules for task text are unchanged: aggregates only, no file names.
- Rejected: steps as Definition of Done checkboxes (mixes steps with completion rules,
  and a checkbox holds no result).

## Consequences

- Rule text: `docs/workflow.md` ("When you are assigned a task") and the agent
  definitions in `.claude/agents/` (`data`, `exp`, `method`, `infra`, `aws`); board task
  [TASK-115](../../backlog/tasks/task-115%20-%20Agents-write-a-numbered-plan-one-step-per-line-and-one-result-note-per-step-DEC-055.md). The agent files are guard files, so the merge waits for the user ([DEC-032](DEC-032-agent-roster-consult-and-lead-skills.md)).
- Tasks already in Review or Done are not rewritten.
- Undo: revert the rule text; existing step notes stay as plain notes.
