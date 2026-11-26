---
id: DIS-065
title: Epic 3 metrics - image score, stone scoring, cirrhosis bar, and keeping several checkpoints by removing beaten ones
status: concluded
created: 2026-11-26
outcomes: [DEC-112, DEC-113, DEC-114]
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

## Second thought: two groups, assessors and drawers (the user, 2026-11-26)

The user's change to DEC-113: two parallel groups of survivors instead of one. One group keeps the
checkpoints that draw well (best Dice: "drawers"); the other keeps the checkpoints that tell well,
sample by sample, whether a class is present (best image-level AUC: "assessors"). As a product the
two are combined: the assessor says whether there is a hepatoma, the drawer draws it.

Review (the analyst's):

- Sound for epic 3: the bar (DEC-112 rules 4 and 5) uses only the image-level score, never the
  outline, so the assessor alone decides the bar and the drawer only adds outline quality. Cost:
  nothing in training; two forward passes at serving when the pair differs.
- Test must not choose: the pair is named on validation before any test result (as DEC-113 rule 8).
- The two can disagree (assessor says "present", drawer draws no pixel of that class, or another
  class there): the product needs a fixed rule, and the report counts the cases.
- Both come from the same run, so the best-AUC and best-Dice epochs may be the same or within noise
  (validation: hepatoma positives from fewer than 5 groups, 19 cyst and 22 hemangioma positives);
  then the pair is one checkpoint.
- Dice measures overlap, not a smooth edge; the user's "more beautiful outline" is likely but not
  what Dice measures.
- One checkpoint per class (e.g. a stone drawer) is left for later: it multiplies the choices made
  on 19 to 31 positives per class.

Related published ideas (checked 2026-11-26; none does exactly this):

| Idea | Closeness | Source |
|---|---|---|
| Classification-guided module of UNet 3+: an image-level "organ present" head gates the segmentation output, tested on liver | gate plus drawer, but one network | Huang et al. 2020, [arXiv 2004.08790](https://arxiv.org/abs/2004.08790) |
| Best epoch per task in multitask learning | closest to two groups | Harutyunyan et al., [arXiv 1703.07771](https://arxiv.org/abs/1703.07771); [arXiv 2610.41134](https://arxiv.org/abs/2610.41134) |
| Checkpoint ensembles: keep the best few checkpoints of one run, average them | keeping several, no roles | Chen et al. 2017, [arXiv 1710.03282](https://arxiv.org/abs/1710.03282) |
| Classifier blanks empty masks, segmenter draws (Kaggle pneumothorax challenge) | gate plus drawer, two models | unverified: no write-up confirming the gating was found |

Table 4. Published ideas close to two checkpoints with split roles. Removing beaten checkpoints keeps
those that no other checkpoint beats (a Pareto set, in the sense of multi-objective optimisation).

The user accepted (2026-11-26) the three recommendations:

1. Two groups replace the DEC-113 mixed group: assessors on image-level AUC per class, drawers on
   Dice per class; the class weights doubled so each group sums to 1 (hepatoma 0.30; hemangioma,
   cyst, stone 0.20 each; ascites 0.10, dropped as thin); floors, steps, veto and threshold as
   DEC-113; at most 3 survivors per group.
2. The bar uses the pair named on validation: the assessor's verdict is the bar; the drawer's Dice
   and the Dice of the combined output are reported as information.
3. When the assessor says a class is present and the drawer predicts no pixel of it, the product
   shows the assessor's own outline, and the report counts these cases.

Record: [DEC-114](../decisions/DEC-114-checkpoint-selection-in-two-groups-assessors-and-drawers.md)
(checkpoint selection in two groups), which supersedes DEC-113. Board: [TASK-288](../../backlog/tasks/task-288%20-%20Checkpoint-selection-mode-that-keeps-several-checkpoints-and-removes-the-beaten-ones-weighted-criteria-floors-steps-removal-threshold-veto-near-copy-rule-cap-primary-by-weighted-sum-set-by-the-recipe-synthetic-tests-DEC-113.md) (selection mode) and
[TASK-287](../../backlog/tasks/task-287%20-%20Epic-3-metrics-report-thresholds-fixed-on-validation-bar-and-cirrhosis-bar-verdicts-group-bootstrap-intervals-per-group-values-negatives-in-four-parts-contested-table-from-per-sample-records-synthetic-tests-DEC-112.md) (epic 3 metrics report) updated.

## Open questions

- The steps, floors, veto, threshold and cap may be set again once, after the first run's
  validation values (DEC-114 rule 10, carried over from DEC-113 rule 9).
- A boundary measure for the drawers (e.g. the 95th-percentile Hausdorff distance) if outline
  quality beyond overlap matters; not a criterion now.
- One checkpoint per class (per-class drawers or assessors), once validation has more positives.

## Further ideas, parked (the user, 2026-11-26)

Asked by the user after the second thought above, reviewed by the analyst (a separate session), and
parked by the user: the plan stays DEC-114 (checkpoint selection in two groups). One Parked board
task per idea, label `needs-decision`. Each idea separates the same two jobs as the two groups: saying
whether a class is present (image-level, judged by AUC) and drawing it (judged by Dice).

### Idea A: one model with two heads, segmentation plus an image-level classification head

Add a small image-level head to the epic 3 segmentation model (pooling on the deepest encoder
features, one sigmoid per spot class and ascites); training loss = segmentation loss + lambda x binary
cross-entropy on the image labels. Store both the head's score and the top-50 score (DEC-112 rule 1)
per sample, so one run compares their AUC on the same checkpoints. With DEC-114, the assessor group
would be judged on the head's AUC and the drawer group on Dice.

- For: the image decision gets its own trained output and loss, with direct pressure against false
  positives on negative images (the top-50 score is derived from the pixels, not trained for).
- Main risk, shortcut learning: an image-level head can learn the look of a site or device instead
  of the lesion. Validation hepatoma positives (193) come from fewer than 5 datasource groups, the
  largest holding 68% (Facts used, above); DEC-100 (epic 3 mission) records a cirrhosis model that
  fell from 0.696 Dice on validation to 0.047 on test. The top-50 score is tied to where the model
  draws; the head is not. Checks if tried: AUC per datasource group, and how often the head says
  "present" where the segmentation draws nothing.
- The head adds information only from samples with an image label and no outline; whether such
  samples exist was not checked (it needs a table read, with the user's ok).
- Records: departs from DEC-110 rule 5 (image score from the pixel probabilities) and DEC-112 rule 1
  (top-50 score); a yes needs a new DEC and maybe a new task version (DEC-004, training tasks; not
  checked). Proposed form: a comparison run after the first one-head run, on the same recipe, like
  the sigmoid comparison run of DEC-110 rule 7.
- Board: [TASK-290](../../backlog/tasks/task-290%20-%20Decide-whether-to-try-a-two-head-model-for-epic-3-segmentation-plus-an-image-level-classification-head-as-a-comparison-run-after-the-first-one-head-run-DIS-065-idea-A.md) (decide whether to try the two-head model). Reopen when the first epic 3 one-head
  run is done and its false positives on negative images are known.

### Idea B: box detection plus segmentation

A detector with a box head and a mask head (as Mask R-CNN): one score and one outline per lesion.

- For: handles several lesions per image; false positives can be counted per lesion.
- Against: a much larger change (boxes made from outlines, lesion-level measures beside the DEC-112
  measures, a new task form). The repo already has a box detector, FCOS for bmode_det v1
  ([DEC-062](../decisions/DEC-062-bmode-box-detector-bmode-det-v1.md) item 1), as a possible start.
- Board: [TASK-291](../../backlog/tasks/task-291%20-%20Decide-whether-to-try-box-detection-plus-segmentation-one-score-and-one-mask-per-lesion-for-the-epic-3-spot-classes-DIS-065-idea-B.md) (decide whether to try box detection plus segmentation). Reopen when idea A is
  tried, or images with several lesions turn out to matter for the product.

### HD95, if added for the drawers (open question above)

Rules needed first: a fixed cap when the prediction is empty (HD95, the 95th-percentile Hausdorff
distance, is undefined then); pixels at the 512 input, not mm, because pixel spacing differs between
devices. HD95 also punishes small far-away blobs inside positive images, which the assessor's gate
does not remove.

### More related work

| Work | What it does | Source |
|---|---|---|
| Classify, then segment (SIIM-ACR pneumothorax challenge, 2019) | a review says the second-place team separated classification from segmentation; partly answers the unverified row of Table 4 | [scitepress 2021](https://www.scitepress.org/Papers/2021/101854/101854.pdf) |
| Localise, then segment, breast ultrasound | a two-stage pipeline said to reduce false positives | [CEUR Vol-4164 paper 27](https://ceur-ws.org/Vol-4164/paper27.pdf) |
| Y-Net (Mehta et al., MICCAI 2018) | U-Net with an added classification branch (idea A), breast biopsy slides | [arXiv 1806.01313](https://arxiv.org/abs/1806.01313) |
| Zhou et al., Medical Image Analysis 70:101918 (2021) | joint segmentation and classification of tumours in 3D breast ultrasound; the abstract reports both improved over single-task models (idea A) | [record](https://pure.korea.ac.kr/en/publications/multi-task-learning-for-segmentation-and-classification-of-tumors/) |
| Mask R-CNN (He et al. 2017) | box head and mask head on one network (idea B) | [arXiv 1703.06870](https://arxiv.org/abs/1703.06870) |
| ELECTRE outranking | weighted agreement index against a cut level (0.5 to 1), indifference and veto thresholds; confirms the analogy of the review above, given there from memory | [R MCDA ELECTRE3](https://search.r-project.org/CRAN/refmans/MCDA/html/ELECTRE3.html), [arXiv 2511.09120](https://arxiv.org/pdf/2511.09120) |
| Shortcut learning (Geirhos et al. 2020) | models solving a task through an unintended cue (the main risk of idea A) | [doi:10.1038/s42256-020-00257-z](https://doi.org/10.1038/s42256-020-00257-z) |

Table 5. Work related to ideas A and B, checked by web search on 2026-11-26 (titles and abstracts or
search summaries, not full papers).
