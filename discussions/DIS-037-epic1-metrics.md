---
id: DIS-037
title: Epic 1 point 4 - metrics - score definition, checkpoint selection, CI method, pass rule, metrics in seg_anatomy_v2
status: concluded
created: 2026-11-19
outcomes: [DEC-076]
related: [DEC-065, DEC-066, DEC-070, DEC-071, DEC-075, DEC-006, DEC-004]
---
# DIS-037: Epic 1 point 4 - metrics

## Question

[DEC-065](../decisions/DEC-065-mission-upper-abdomen-anatomy-segmentation.md) point 4 asks
for the final bar, the checkpoint selection rule and the CI method for the first anatomy model.
[TASK-171](../../backlog/tasks/task-171%20-%20Decide-whether-adding-metrics-to-seg_anatomy_v2-in-epic-1-point-4-makes-a-new-task-version-v3-since-metrics-are-in-the-task-fingerprint.md)
(new task version?) waits on the same session.

## Options considered

| Question | Chosen | Alternative | When the alternative would win |
|---|---|---|---|
| Metrics in `seg_anatomy_v2` or a new v3 | v2 (the user: leaving metrics out was deliberate); no recipe or script uses it | v3, as [DEC-004](../decisions/DEC-004-training-tasks.md) reads | A run folder already used v2 (not checked) |
| W2 "predicts none" | 0 pixels; looser floors reported only | A floor (e.g. 0.5% of the input) in the bar | Stray argmax pixels turn out to dominate W2 failures |
| Pass rule | Point estimate meets the bar; CI reported with the verdict | CI lower bound meets the bar | A strict claim is needed; with about 11 test groups it would likely fail |
| Checkpoint selection | Mean W1 over the four organs, then mean W2, then val loss (proposed by the analyst, in DEC-065's lean; not asked) | Pooled pixel DSC ([DEC-006](../decisions/DEC-006-losses-optim-tracking.md) default) | Per-sample means are too noisy on a small val |
| CI method | Cluster bootstrap as [EXP-003](../experiments/EXP-003-transunet-r50-b16-from-scratch-512-and-224-lseg-cirrhosis-v4.md) (test by group, val by image); per-group table beside it (decided by the analyst, told to the user) | Patient bootstrap | Patient ids become available |

Table 1. The questions of point 4, the choice and the best alternative.

## Conclusion

[DEC-076](../decisions/DEC-076-epic1-metrics-label-set-score-selection-ci-and-pass-rule.md)
(proposed). Board tasks after the user accepts it.

## Open questions

- Whether any run folder used `seg_anatomy_v2` (the method task checks first).
- The checkpoint rule and the CI details were not put to the user as questions; the user can
  change them before accepting DEC-076.
