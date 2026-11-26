---
id: DEC-112
title: Epic 3 metrics - image score as the mean of the 50 highest pixel probabilities, stone counted for its mass in the mass Dice, final bar with a cirrhosis specificity bar of 0.80, intervals over groups, metrics in seg_spot_v1
status: accepted
area: [training]
created: 2026-11-26
from: [DIS-065]
related: [DEC-004, DEC-045, DEC-076, DEC-100, DEC-103, DEC-108, DEC-110, DEC-113]
superseded_by:
---
# DEC-112: Epic 3 metrics

## Context

The metrics point of the epic 3 mission ([DEC-100](DEC-100-epic3-mission-spot-liver-diseases.md)
rule 7); discussion and counts in [DIS-065](../discussions/DIS-065-epic3-metrics-and-keeping-several-checkpoints.md)
(epic 3 metrics and keeping several checkpoints). Test holds 105 cirrhosis negatives (hepatoma
negative, cirrhosis positive) in 8 datasource groups (split record of [TASK-279](../../backlog/tasks/task-279%20-%20Epic-3-split-on-261023-build-the-table-of-samples-to-split-run-the-feasibility-report-freeze-the-sample-file-with-the-DEC-108-limits-and-its-enc1-copy-dataset-record-per-split-and-class-DEC-108.md),
`datasets/261023/spot_e3_split.md`). The task form is [DEC-110](DEC-110-epic3-task-form-allowed-class-sets-stone-takes-the-overlap.md)
(epic 3 task form: one softmax over background, the four spot classes and ascites).

Terms: the **four spot classes** are `hepatoma`, `hemangioma`, `hepatic_cyst`, `hepatic_stone`;
a pixel is **predicted as class c** when the argmax of the six output channels is c; **p_c** is the
softmax probability of c at a pixel.

## Decision

Accepted by the user on 2026-11-26.

1. **Image-level score** of class c on a sample: the mean of the 50 highest p_c over the input
   pixels (the top-50 mean). For "any of the four spot classes" (DEC-100 rule 4 item a): the top-50
   mean of the per-pixel sum of the four spot-class probabilities. The maximum p_c and the predicted
   area of c (pixels predicted as c) are stored too, as information only. This fills DEC-110 rule 5.
2. **Pixel scores** per class as Epic 1 ([DEC-076](DEC-076-epic1-metrics-label-set-score-selection-ci-and-pass-rule.md)
   rules 1 and 2): Dice on positives with an outline, the no-prediction score (0 pixels predicted)
   on negatives, unknown and contested pairs not scored ([DEC-103](DEC-103-epic3-negatives-and-contested-labels.md)
   rule 4); the 0.1% and 1% area floors as information.
3. **Stone inside a mass** (DEC-110 rule 3, the stone takes its overlap with a mass): in the Dice of
   a positive `hepatoma`, `hemangioma` or `hepatic_cyst`, the outline is the mass's full outline, and
   pixels predicted as `hepatic_stone` inside the overlap of a positive stone outline and that mass
   outline count as predicted mass. The stone's own scores are unchanged. Not applied to the
   image-level score.
4. **Bar** (the provisional bar of DEC-100 rule 4 becomes final): on test groups, at a threshold fixed
   on validation, for (a) any spot class and (b) hepatoma: sensitivity at least 0.80, specificity at
   least 0.90, validation minus test at most 0.10 (for each of the two). The threshold of each item
   is the highest one at which validation sensitivity is at least 0.80.
5. **Cirrhosis bar** (DEC-103 rule 3, an own bar for cirrhosis): specificity on cirrhosis negatives
   at least 0.80, for both items (a) and (b), at the same threshold.
6. **Pass rule** as DEC-076 rule 5: a criterion is met on its point estimate; the record says when the
   95% interval lies across the bar. The bar is not changed after a test result has been seen.
7. **Intervals**: 95% percentile intervals from a bootstrap over datasource groups, 2,000
   replicates, seed 0, on validation ([DEC-108](DEC-108-epic3-split-test-and-validation-by-whole-groups.md)
   rule 6) and test; validation minus test with independent draws. Where the cases of a measure
   (positives for sensitivity and Dice, negatives for specificity) come from fewer than 5 groups, the
   per-group values are given and the interval is marked unreliable. Every record also gives the
   per-group values beside the interval, and the four parts of the negatives (DEC-103 rule 2).
8. **Reported without a bar**: hemangioma, cyst, stone and ascites; AUC with interval per class and
   for any spot class; sensitivity and specificity over thresholds; the class-by-class confusion
   matrix; the contested samples' table (DEC-103 rule 5).
9. **Per-sample record**, from the first run (DEC-100 rule 5), for each sample and class: the state
   read from the target, the three image-level values of rule 1, predicted, outline and overlap pixel
   counts, the extra overlap of rule 3, and the joint pixel counts of target class by predicted
   class. Split, group, the parts of the negatives and contested pairs are joined from the sample
   file at report time. Keyed by sample number only ([DEC-045](DEC-045-per-sample-confusion-matrices-in-runs.md) rule 2).
10. **Task version**: the metrics go into `seg_spot_v1` itself, not a new `seg_spot_v2`, as DEC-076
    rule 6.2; [DEC-004](DEC-004-training-tasks.md) (a changed fingerprint is a new version) is waived
    for this one change because no run uses the task yet. If a run already used it, the code task
    stops and returns the question.
11. **Checkpoint selection** is [DEC-113](DEC-113-checkpoint-selection-by-removing-beaten-checkpoints.md)
    (keep several checkpoints, remove the beaten ones); the bar of rules 4 and 5 is read on its
    primary checkpoint.

## Consequences

- With 105 cirrhosis negatives, a measured 0.80 has a 95% interval of about 0.71 to 0.87 before
  grouping (DIS-065), so the cirrhosis bar is read with its interval.
- The image-level score needs the probabilities at evaluation, not only the argmax.
- Rule 3 needs the stone-mass overlap at evaluation; the target alone does not hold it (it gives
  {`hepatic_stone`} there).
- Reversal: before the first run, low; after, re-score the stored per-sample records (cheap), except
  rule 1's values, which need inference again if changed.
