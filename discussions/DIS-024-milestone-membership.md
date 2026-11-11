---
id: DIS-024
title: Milestone membership - why new training tasks were missing from m-1
status: concluded
created: 2026-11-11
outcomes: [DEC-051]
related: [DEC-016, DEC-039]
---
# DIS-024: Milestone membership - why new training tasks were missing from m-1

## Question

The user expected milestone m-1 ("Train on dataset 261023") to hold every task about
training on dataset 261023, but recently added training tasks (for example [TASK-112](../../backlog/tasks/task-112%20-%20Train-lseg_cirrhosis_v4-with-transunet_r50_b16-from-scratch-at-512-px-and-a-224-px-control-compare-with-cirr-v4-tu-e30-r5-in-an-EXP-record-DEC-050.md),
TransUNet runs at 512 px) were not in it. Why, and how do we keep milestones complete?

## Findings

- Backlog.md 1.55.3 has no rule-based milestones. A milestone file holds only an id,
  a title and a free-text description. A task belongs to a milestone only when its own
  `milestone:` field is set (`backlog task create -m` / `task edit -m`).
- No skill or doc told sessions or agents to set `-m`. Of the tasks created from
  [TASK-089](../../backlog/tasks/task-089%20-%20Loss-and-evaluate-pass-only-the-predicted-GT-layers-to-the-loss-for-tasks-with-predicted_layers-DEC-043.md) onward, about half had no milestone; agents' Triage tasks almost never had one.
- The m-1 description was out of date: it named only the training stack (losses,
  optimisation, loop, evaluation, tracking), not tasks, sample sets, GPU-box runs or
  EXP records, so it could not guide a choice either.

## Options considered

- **A, rule in docs and skills only**: each milestone description states what belongs
  in it; whoever creates a task picks the milestone by those descriptions. Cheap, but
  relies on memory.
- **B, A plus a check**: `scripts/check.sh` warns about open tasks with no milestone.
  Catches misses; possible noise from tasks with no fitting milestone (board, docs
  tooling).

## Conclusion

The user chose B (2026-11-11): [DEC-051](../decisions/DEC-051-milestone-membership-rule.md).
The check is a new Triage task. The user also agreed to set m-1 on 22 tasks that
match the new rule (open and Done, including 4 Done tasks from 2026-11-03 that prepared
the 261023 training tasks), and m-2 on [TASK-032.14](../../backlog/tasks/task-032.14%20-%20ai-label-run-on-the-GPU-box-records-code-unknown-in-model_version-pass-the-code-version-to-the-box.md) (ai-label code version), like its
parent [TASK-032](../../backlog/tasks/task-032%20-%20Run-the-B-mode-cropper-on-a-dataset-version-polygon-check-reviewed-set-box-table-DEC-017.md).

## Open questions

- None.
