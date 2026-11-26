---
id: DIS-065
title: Epic 3 metrics - image score, stone scoring, cirrhosis bar, and keeping several checkpoints by removing beaten ones
status: concluded
created: 2026-11-26
outcomes: [DEC-112, DEC-113]
related: [DIS-064, DEC-004, DEC-006, DEC-045, DEC-076, DEC-100, DEC-103, DEC-108, DEC-110]
---
# DIS-065: Epic 3 metrics and keeping several checkpoints

## Question

The metrics point of the epic 3 handoff ([DEC-100](../decisions/DEC-100-epic3-mission-spot-liver-diseases.md),
epic 3 mission, rule 7), asked by [TASK-284](../../backlog/tasks/task-284%20-%20Decide-epic-3-metrics-image-level-score-from-the-pixel-probabilities-scoring-of-a-stone-inside-a-mass-outline-the-cirrhosis-specificity-bar-from-the-test-counts-interval-method-DEC-100-rules-4-and-5-DEC-103-rule-3-DEC-110.md)
(decide the epic 3 metrics): how the image-level score per class comes from the pixel
probabilities ([DEC-110](../decisions/DEC-110-epic3-task-form-allowed-class-sets-stone-takes-the-overlap.md),
epic 3 task form, rule 5); how a stone predicted inside a mass outline is scored (DEC-110 rule 3,
the stone takes its overlap with a mass); the final bar and the cirrhosis bar
([DEC-103](../decisions/DEC-103-epic3-negatives-and-contested-labels.md), epic 3 negatives, rule 3);
the interval method; the per-sample record (DEC-100 rule 5); whether adding metrics to the task
makes a new task version ([DEC-004](../decisions/DEC-004-training-tasks.md), training tasks).
The user added a new question: keep several checkpoints instead of one.

## Facts used

From the split record of [TASK-279](../../backlog/tasks/task-279%20-%20Epic-3-split-on-261023-build-the-table-of-samples-to-split-run-the-feasibility-report-freeze-the-sample-file-with-the-DEC-108-limits-and-its-enc1-copy-dataset-record-per-split-and-class-DEC-108.md) (`datasets/261023/spot_e3_split.md`, epic 3 split on 261023):

- Test: 2,421 samples in 11 datasource groups. Cirrhosis negatives (hepatoma negative, cirrhosis
  positive) 105 in 8 groups, largest group 34.3%; the cirrhosis part of the samples negative for all
  four spot classes is also 105.
- Validation: 2,426 samples in 14 groups. Positives: hepatoma 193 (fewer than 5 groups, largest 68%),
  hemangioma 22, cyst 19 (largest group 89.5%), stone 31 (8 groups), ascites fewer than 5.
  Cirrhosis negatives 60.
- Lesion size ([DIS-064](DIS-064-epic3-data-preparation-task-form-more-data.md) Table 1, epic 3 data preparation): stones have a median share of the crop of
  0.14% and a 10th percentile of 0.07%, about 180 pixels at a 512 x 512 input.
- A specificity of 0.80 measured on 105 negatives has a Wilson 95% interval of 0.714 to 0.865
  (0.90: 0.828 to 0.944), computed here, treating samples as independent; the interval over groups is wider.

## Answers so far (the user, 2026-11-26)

1. **Image-level score** of class c: the mean of the 50 highest pixel probabilities of c (50 pixels
   is below the area of the smallest tenth of stones). For "any of the four spot classes" (DEC-100
   rule 4 item a) the same on the per-pixel sum of the four spot-class probabilities. The maximum
   pixel probability and the predicted area (pixels whose argmax is c) are stored as information.
2. **Stone rule at scoring**: only in the Dice of a mass (hepatoma, hemangioma, cyst): pixels
   predicted as stone inside the overlap of a positive stone outline and the mass outline count as
   predicted mass, and the mass outline is its full outline. Not applied to the image-level score.
3. **Bar**: the provisional values of DEC-100 rule 4 become final (sensitivity at least 0.80,
   specificity at least 0.90, validation minus test at most 0.10, for any spot class and for
   hepatoma). The threshold is the highest one with validation sensitivity at least 0.80.
   **Cirrhosis bar**: specificity on cirrhosis negatives at least 0.80, for both items. A criterion
   is met on its point estimate; the record says when the 95% interval crosses the bar (as
   [DEC-076](../decisions/DEC-076-epic1-metrics-label-set-score-selection-ci-and-pass-rule.md),
   Epic 1 metrics, rule 5).

Not asked, proposed as defaults: intervals as DEC-076 rule 4 (Epic 1 intervals) with validation
also over groups ([DEC-108](../decisions/DEC-108-epic3-split-test-and-validation-by-whole-groups.md),
epic 3 split, rule 6): percentile intervals from a bootstrap over datasource groups, 2,000
replicates, seed 0; where a measure's cases come from fewer than 5 groups, the per-group values are
given and the interval is marked as unreliable. "Predicts none" is 0 pixels, with the 0.1% and 1%
floors as information (DEC-076 rule 2).

## The user's proposal: keep several checkpoints

Instead of choosing one checkpoint, remove the beaten ones; every checkpoint that is good at
something survives. For this epic and the following epics.

1. Define the selection criteria (the user's "key indices"; name to be chosen).
2. Give each a weight; the weights sum to 1.
3. Set a removal threshold (the user's "overriding threshold"), e.g. 0.666: with three equal
   weights, two out of three.

Checkpoint A removes checkpoint B when the sum over criteria of weight x value reaches the
threshold, where the value is 1 (A beats B), 0.5 (half) or 0 (A does not beat B).

| Criterion | Classes | Weight each | Sum |
|---|---|---:|---:|
| Image-level AUC | hepatoma | 0.5 x 1.5/5 = 0.15 | 0.15 |
| Image-level AUC | hemangioma, cyst, stone | 0.5 x 1/5 = 0.10 | 0.30 |
| Image-level AUC | ascites | 0.5 x 0.5/5 = 0.05 | 0.05 |
| Dice on positives | hepatoma | 0.15 | 0.15 |
| Dice on positives | hemangioma, cyst, stone | 0.10 | 0.30 |
| Dice on positives | ascites | 0.05 | 0.05 |

Table 1. The user's criteria and weights (sum 1.00). Reading of "other disease than ascites": each
of hemangioma, cyst and stone has weight 0.10; this is the reading that makes the weights sum to 1.

Value for Dice (the user's): 0 when A's Dice is below 0.6; 0.5 when A and B differ by less than 0.05;
1 when A is better by 0.05 or more. No rule was given for AUC.

## Review of the proposal

The idea is sound and close to the outranking methods of multi-criteria decision analysis (the
ELECTRE family: a weighted agreement index against a threshold, with indifference and veto
thresholds; from memory, not verified). With a threshold above 0.5, two checkpoints can never
remove each other: a half value counts for both, so the two sums add up to at most 1. Problems found:

| # | Problem | Suggested change |
|---|---|---|
| 1 | Near-copies all survive: neighbouring epochs differ by less than 0.05 everywhere, so each pair scores 0.5 < 0.666 and nothing is removed; tens of checkpoints may survive. | When A and B are within the 0.5 band on every criterion, keep the one with the higher weighted sum. Cap the survivors (e.g. 5); above the cap drop the lowest weighted sum. |
| 2 | "Keep every checkpoint good at something" is not enforced: A can remove B although B is much better on one criterion (e.g. stone Dice), if A wins enough weight elsewhere. | Veto: B survives A when B is better by at least a veto step on any criterion (e.g. Dice 0.10, AUC 0.05). |
| 3 | Validation has fewer than 5 ascites positives in epic 3, and 19 cyst and 22 hemangioma positives: their AUC and Dice are mostly noise. | A criterion with fewer than 15 validation positives is left out and the other weights are scaled to sum 1. A 0.05 Dice step is within the noise for cyst; the steps may be set after the first run's validation values, before any test result. |
| 4 | AUC needs its own steps: AUC values crowd near 0.9, so 0.05 is a large gap. | AUC: 0.5 band below 0.02, beat at 0.02 or more, floor 0.70 (A's AUC below it counts 0). Analyst's numbers. |
| 5 | Several survivors tested on test, with the best one reported, is a choice made on test ([DEC-045](../decisions/DEC-045-per-sample-confusion-matrices-in-runs.md) rule 3, per-sample records: test is never used for a choice; DEC-100 rule 5). | Before test, one survivor is named the primary by validation only (highest weighted sum); the bar verdict uses it. The other survivors are tested and reported as secondary, never for the bar. |

Table 2. Problems of the proposal and the suggested change for each. Numbers in the changes are the
analyst's, not from literature.

Smaller points:

- During training the rule runs online: a new checkpoint enters unless a survivor removes it, and it
  removes the survivors it beats. A removed checkpoint does not come back, so the result can depend
  on the order of epochs. Per-epoch measures stay in the run for every epoch (DEC-045 rule 3); only
  the weights of removed checkpoints are deleted.
- Removal can run in a cycle (A removes B, B removes C, C removes A). If no checkpoint survives,
  the one with the highest weighted sum is kept.
- The bar's item (a), any spot class, is not a criterion; hepatoma dominates it. It can be added.
- Code: a new selection mode beside the [DEC-006](../decisions/DEC-006-losses-optim-tracking.md) tie-breaker rule (`Selection` in
  `sonoai.training.loop`), set by the recipe (criteria, weights, steps, floors, veto, threshold,
  cap); Epic 1 keeps DEC-076 rule 3 (Epic 1 checkpoint selection).
- Names: no new term needed; descriptive words work: "selection criteria", "weight", "removal
  threshold", "A removes B", "veto step".

## Worked example

Ascites left out (change 3), weights scaled by 1/0.9: hepatoma 0.167 per criterion, the other three
classes 0.111 each. A against B:

| Criterion | Hepatoma | Hemangioma | Cyst | Stone |
|---|---:|---:|---:|---:|
| AUC value | 1 | 0.5 | 0 | 1 |
| Dice value | 1 | 0.5 | 0 | 0.5 |

Table 3. Values of A against B in the example. Sum: 0.167 x 2 + 0.111 x (0.5 + 0 + 1 + 0.5 + 0 + 0.5)
= 0.333 + 0.278 = 0.611, below 0.666: A does not remove B. If A had also beaten B on cyst Dice by
0.05 or more, the sum would be 0.722 and A would remove B, unless B's cyst AUC is better by at least
0.05 (veto, change 2).

## Conclusion

The user accepted (2026-11-26) the selection rule with the five changes of Table 2, for epic 3 and
the following epics (Epic 1 unchanged), and the metrics in `seg_spot_v1` itself. Records:
[DEC-112](../decisions/DEC-112-epic3-metrics-image-score-stone-scoring-cirrhosis-bar.md) (epic 3
metrics) and [DEC-113](../decisions/DEC-113-checkpoint-selection-by-removing-beaten-checkpoints.md)
(keep several checkpoints, remove the beaten ones). Board: method tasks for the epic 3 evaluation,
the epic 3 metrics report, and the selection mode (see DEC-112 and DEC-113).

## Open questions

- The steps, floors, veto and threshold of DEC-113 may be set again after the first run's
  validation values (DEC-113 rule 9).
