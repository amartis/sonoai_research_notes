---
id: DEC-061
title: strict_v1 A9 also checks the target side of a value-absent implied tag (R50), and three readings of DEC-060 taken in TASK-123
status: accepted
area: [labeling]
created: 2026-11-17
from: [DIS-028]
related: [DEC-059, DEC-060]
superseded_by:
---
# DEC-061: strict_v1 A9 also checks the target side of a value-absent implied tag (R50), and three readings of DEC-060 taken in TASK-123

## Context

[TASK-123](../../backlog/tasks/task-123%20-%20Presence-policies-registry-the-policies-chosen-in-TASK-122-sonoai-data-sample-label-presence-tests-on-synthetic-rows-DEC-059.md)
implemented the presence policies of [DEC-060](DEC-060-first-presence-policies-of-261023.md)
on synthetic rows. Its review raised one gap and three readings for the user.

**The gap.** DEC-060 section 4 (`strict_v1`, step 1) states A9 from the subject side: the
row's label tag is the subject of an `implied_tags` entry. The only entry with
`value: absent` in the 261023 fact relations config is R50 (P7 `skip_notliver` implies no P2
`liver`). Its subject is a skip tag, never a content label, so no row has it as its label and
the check never acts. Pn = labeling project n.

## Decision

The user accepted all four points on 2026-11-17 (consult session).

1. **A9, target side (amends DEC-060 section 4, `strict_v1`).** A positive of a label is
   unknown (reason `conformance`) when the label's tag is the target of a kept
   `implied_tags` entry with `value: absent` and the entry's subject is given on the same
   sample by a task of the entry's projects. A subject that is a task-skip tag counts,
   although that task gives no answer. The `via_task_order` part is not read (as before;
   its P9 item is dropped, DEC-060 Table 1). The subject-side A9 of DEC-060 is unchanged.
   `loose_v1` and `posrich_v1` are unchanged (no A8, A9 checks).
2. **Dropped closure.** A dropped closure QA tag still makes its labeling group visited: the
   task answer is `open`, not `none`.
3. **A9 target in another project.** When the entry names another labeling project and that
   project has no task on the sample, the target counts as not given.
4. **Grade gap.** Grading tasks with a task skip, and grading tasks with inconsistent grading
   (R22, R27), are not counted in `grade_gap`.

The presence summary sheet stays as built in TASK-123 (rows per label, state and reason).
Totals per reason across labels, if wanted, go in the [TASK-124](../../backlog/tasks/task-124%20-%20Build-the-261023-sample-label-presence-tables-of-the-chosen-policies-dataset-record-comparing-counts-per-label-and-state-across-policies-DEC-059.md) dataset record.

## Consequences

- `strict_v1` keeps its name and version: no presence table has been built yet (TASK-124), so
  no table carries the old reading.
- TASK-123 gets one more acceptance criterion (point 1, with synthetic tests) and goes back to
  To Do for the `method` agent; the docstring of `strict_v1` and fact-driven-model.md section 5
  state the target-side check.
- Points 2-4 match the code on the TASK-123 branch; no change.
