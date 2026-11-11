---
id: DEC-051
title: Milestone membership - each milestone description is an inclusion rule, and every new task gets a milestone by it
status: accepted
area: [workflow]
created: 2026-11-11
from: [DIS-024]
related: [DEC-016, DEC-039]
superseded_by:
---
# DEC-051: Milestone membership - each milestone description is an inclusion rule, and every new task gets a milestone by it

## Context

[DIS-024](../discussions/DIS-024-milestone-membership.md): Backlog.md 1.55.3 has no
rule-based milestones; a task is in a milestone only when its own `milestone:` field is
set. Nothing told sessions to set it, so new training tasks were missing from m-1
("Train on dataset 261023").

## Decision

- Each milestone description (`backlog/milestones/`) states what belongs in it
  ("Belongs here" / "Not here"). The m-1 description is rewritten this way.
- Whoever creates a task (consult, lead, any agent's Triage task) sets `-m <id>` by
  those descriptions; when none fits, the task has no milestone, and a consult session
  says so in its reply. A subtask takes its parent's milestone.
- A new milestone is added with its inclusion rule in the description, never with a
  bare title.
- `scripts/check.sh` warns (does not fail) about open tasks with no milestone: a new
  Triage task.

## Consequences

- Rule text: [docs/workflow.md](../../docs/workflow.md) (Board section and the agents'
  "new task" step) and the consult skill, step 4.
- Board changes: m-1 set on 22 tasks, m-2 on [TASK-032.14](../../backlog/tasks/task-032.14%20-%20ai-label-run-on-the-GPU-box-records-code-unknown-in-model_version-pass-the-code-version-to-the-box.md), in the
  `consult-milestones` branch.
