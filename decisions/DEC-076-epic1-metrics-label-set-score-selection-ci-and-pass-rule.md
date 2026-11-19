---
id: DEC-076
title: Epic 1 point 4 - metrics - the label-set score (W1, W2, W3), checkpoint selection on val, cluster bootstrap CIs, pass rule, metrics added to seg_anatomy_v2
status: accepted
area: [training]
created: 2026-11-19
from: [DIS-037]
related: [DEC-065, DEC-066, DEC-070, DEC-071, DEC-075, DEC-006, DEC-004, DEC-045]
superseded_by:
---
# DEC-076: Epic 1 point 4 - metrics

## Context

[DEC-065](DEC-065-mission-upper-abdomen-anatomy-segmentation.md) (mission: upper-abdomen
anatomy segmentation) point 4 asks for the final bar, the checkpoint selection rule and the CI
method. [DEC-066](DEC-066-epic1-model-task-label-set-softmax.md) rule 6 fixes the score in
words; [DEC-070](DEC-070-anatomy-label-set-task-states-in-sample-file.md) rule 4 makes the
evaluation refuse a label-set task until this point. The test set has about 11 datasource
groups ([DEC-075](DEC-075-epic1-split-values-tolerance-and-minimum-counts.md)), so its CIs are
wide. Val shares datasources with train ([DEC-071](DEC-071-epic1-splitting-parameterised-split-method.md)),
so val scores are optimistic. Discussion: [DIS-037](../discussions/DIS-037-epic1-metrics.md).

Terms: a **sample** is one crop of one image; the **first set** is liver, kidney, stomach,
gallbladder ([DEC-066](DEC-066-epic1-model-task-label-set-softmax.md) rule 1). A pixel is
**predicted as organ c** when the argmax of the 5 output channels is c.

## Decision

### 1. Per-sample score (DEC-066 rule 6, made exact)

For each sample and each first-set organ c, by the organ's `strict_v1` state in the sample file:

| State of c | Score | Definition |
|---|---|---|
| positive (with polygon) | DSC<sub>ic</sub> | 2·\|P∩G\| / (\|P\|+\|G\|); P = pixels predicted as c, G = the organ's polygon mask in the crop; 0 when P is empty |
| closed negative | clean<sub>ic</sub> | 1 when P is empty (0 pixels), else 0 |
| unknown | none | not scored, adds to no count |

Table 1. The score of one sample and one organ. Pixels with the ignore value are left out of P
and G; pixels outside the original crop count as background (target fill, [DEC-068](DEC-068-us-mild-v2-zero-image-and-background-outside-the-crop.md)).

Measures per split and organ c (all unweighted means over samples):

- **W1<sub>c</sub>** = mean DSC<sub>ic</sub> over samples where c is positive.
- **W2<sub>c</sub>** = mean clean<sub>ic</sub> over samples where c is a closed negative.
- **W3<sub>c</sub>** = W1<sub>c</sub>(val) − W1<sub>c</sub>(test).

The bar of DEC-065 Table 1 applies as written, with the classes of DEC-066 rule 1: W1: liver
≥ 0.85, kidney, stomach, gallbladder ≥ 0.70; W2: every organ ≥ 0.90; W3: every organ ≤ 0.10.

### 2. "Predicts none" is 0 pixels

W2 uses 0 predicted pixels. The record of each run also shows W2<sub>c</sub> at floors of 0.1%
and 1% of the input area, as information. A floor enters the bar only by a new DEC, set after
the values are seen.

### 3. Checkpoint selection (val only)

Criteria, in order, tolerance 1e-4 ([DEC-006](DEC-006-losses-optim-tracking.md) rule, `Selection` in `sonoai.training.loop`):
1. val **mean of W1<sub>c</sub> over the four organs**, max (matches the bar; each organ counts
   the same);
2. val **mean of W2<sub>c</sub> over the four organs**, max;
3. val loss, min.

Pixel-pooled DSC is not used for selection (it weights large organs and large crops more).
The test split is never read for selection ([DEC-043](DEC-043-cirrhosis-task-gt-organ-layer-predicted-cirrhosis-only.md) rule 7, [DEC-045](DEC-045-per-sample-confusion-matrices-in-runs.md) rule 3).

### 4. Confidence intervals

95% percentile intervals from a cluster bootstrap, 2,000 replicates, seed 0, as in
[EXP-003](../experiments/EXP-003-transunet-r50-b16-from-scratch-512-and-224-lseg-cirrhosis-v4.md)
(`sonoai.data.bmode_tune.bootstrap_ci`; Field and Welsh 2007, doi:10.1111/j.1467-9868.2007.00593.x):
- **test**: clusters are datasource groups;
- **val**: clusters are images (val is split by image hash);
- **W3**: val and test are drawn independently, and the CI is that of the difference.
Because test has few groups, each EXP record also gives the per-group W1 and W2 (samples and
value per group) beside the CI.

### 5. Pass rule

A criterion is **met** when its point estimate meets the bar. The EXP record says, for each
criterion, "met" or "met, but the 95% CI lower bound (upper bound for W3) is on the wrong side
of the bar". The bar is not changed after test results of a run have been seen (DEC-065
Table 1).

### 6. Task and code

1. The DEC-066 rule 6 score and the per-sample record (organ, state, predicted, polygon and
   overlap pixel counts) go into `seg_anatomy_v2`'s evaluation; the label-set refusal of
   DEC-070 rule 4 is removed.
2. **Metrics are added to `seg_anatomy_v2` itself, not to a new v3** (the user's choice: leaving
   them out was deliberate). [DEC-004](DEC-004-training-tasks.md)'s rule (a changed fingerprint is a new version) is
   waived for this one change because no recipe, script or run of this repository uses the
   task yet (grep of `configs/` and `scripts/`; run folders not checked). If a run already
   used v2, the task of rule 6.1 stops and returns the question.
3. A report function turns the per-sample records and the sample file's split and group
   columns into the W1, W2, W3 table with CIs and the per-group table.

## Consequences

- DEC-070 rule 4 is replaced by rule 6.1; [TASK-171](../../backlog/archive/tasks/task-171%20-%20Decide-whether-adding-metrics-to-seg_anatomy_v2-in-epic-1-point-4-makes-a-new-task-version-v3-since-metrics-are-in-the-task-fingerprint.md) (new task version?) is closed by rule 6.2.
- Board tasks: [TASK-180](../../backlog/tasks/task-180%20-%20Label-set-evaluation-for-seg_anatomy_v2-per-sample-W1-Dice-and-W2-clean-score-per-organ-by-state-per-sample-records-selection-keys-metrics-registered-on-the-task-evaluation-refusal-removed-synthetic-tests-DEC-076.md) (label-set evaluation for seg_anatomy_v2) and [TASK-181](../../backlog/tasks/task-181%20-%20Epic-1-metrics-report-W1-W2-W3-table-with-cluster-bootstrap-95-CIs-test-by-datasource-group-val-by-image-per-group-table-and-the-DEC-076-verdict-wording-from-per-sample-records-and-the-sample-file-synthetic-tests-DEC-076.md) (metrics report with CIs), both method; TASK-169 and TASK-171 archived. Plan: a method task for rules 1 to 3 and 6.1 to
  6.2; a method task for the report (rule 4, 5, 6.3). The method task touches the segmentation
  trainer, as [TASK-169](../../backlog/archive/tasks/task-169%20-%20Segmentation-trainer-refuses-a-label-set-task-at-setup-before-training-starts-today-evaluate-refuses-only-at-the-first-evaluation.md) (trainer refuses a label-set task at setup) does; TASK-169 is
  superseded by it and is closed there.
- Reversal: all rules apply before the first run; a later change means a new DEC and
  re-scoring saved per-sample records (cheap), not retraining.
