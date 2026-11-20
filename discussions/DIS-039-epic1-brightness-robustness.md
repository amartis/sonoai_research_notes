---
id: DIS-039
title: Epic 1 brightness robustness - how the anatomy model is made and shown not to depend on deliberate brightening or darkening of its input
status: concluded
created: 2026-11-20
outcomes: [DEC-079]
related: [DEC-065, DEC-049, DEC-068, DEC-076, DEC-077, DIS-022, DIS-007]
---
# DIS-039: Epic 1 brightness robustness

## Question

The user (2026-11-20): the epic 1 model's performance must not be affected by deliberately
brightened (or darkened) input. Two reasons, in the user's words:

1. a countable share of the samples of dataset 261023 were brightened on purpose before we
   scraped them;
2. at serving time a user may send a brightened or darkened image, by deliberate colour
   control or because of the ultrasound device's settings.

Where things stand ([DEC-065](../decisions/DEC-065-mission-upper-abdomen-anatomy-segmentation.md),
mission of epic 1):

- `us_mild_v2` ([DEC-068](../decisions/DEC-068-us-mild-v2-zero-image-and-background-outside-the-crop.md),
  steps of [DEC-049](../decisions/DEC-049-mild-ultrasound-augmentation-us-mild-v1.md)) changes
  brightness only mildly: additive offset within ±0.1, contrast 0.85 to 1.15, gamma 0.8 to 1.25,
  depth gain curve 0.8 to 1.2.
- [DEC-077](../decisions/DEC-077-epic1-model-choice-six-recipes.md) rule 3: every model takes
  [0, 1] input; the pretrained ones subtract a fixed mean and divide by a fixed std inside
  `forward`. Nothing adapts to the brightness of one image.
- Nothing measures how scores change with input brightness; the bar (DEC-065 section 2,
  [DEC-076](../decisions/DEC-076-epic1-metrics-label-set-score-selection-ci-and-pass-rule.md))
  is W1, W2 and W3 on the images as they are.
- Point 6 (optimisation strategy, which includes the augmentation) is not settled, and no epic 1
  training run exists yet, so all of this can still change at low cost.

## Options considered

| Question | Analyst's recommendation | Chosen (the user) | When the recommendation would have won |
|---|---|---|---|
| Does brightness robustness enter the bar? | yes, as a criterion W4: on test, for every first-set organ and every level of a fixed brightness grid, W1 and W2 drop by at most 0.03 from the unchanged input | **report only**: the same shift test on val and test, shown with paired CIs in every EXP record; the verdict stays W1, W2, W3 | when a model that meets W1 to W3 but fails on brightened input must not count as working |
| How do the models learn it? | a wider photometric augmentation (`us_bright_v1`) only | **augmentation plus per-image percentile normalisation inside the model** | when the simplest working choice comes first (DEC-065 rule 4.6), or when the share of each part in the result must be measured |
| Measure the brightened samples first? | yes: per-sample brightness statistics inside the crop, and a dHash check for brightened copies of one image across train, val and test | **skip** | when the brightened share is large, or when the brightened samples are copies of other images in the set (val is split by image md5, DEC-076 rule 4, so a brightened copy of a train image could land in val and make val and checkpoint selection optimistic; the Roboflow scraper README says Universe projects are "often re-augmented") |

Table 1. The three questions put to the user, the analyst's recommendation, the user's choice
and when the recommendation would have won.

Also offered and not chosen: a **consistency loss** (two photometric views of each crop and a
loss on the difference of their predictions): new loss code and about twice the compute.
Not offered: test-time averaging over brightness levels (slower serving) and histogram
equalisation (changes the grey-level texture and lifts speckle; the analyst's judgement, not
checked against a source).

The analyst said once, in the option text, that "report only" lets a model pass the epic and
still fail on brightened input, which the user had called necessary to avoid. The user kept
"report only".

Decided by the analyst and told to the user:

- **The shift grid** (10 levels on the [0, 1] crop, clipped to [0, 1]): gain ×0.5, ×0.7, ×1.4,
  ×2.0; offset −0.2 and +0.2; gamma 0.5 (brighter) and 2.0 (darker); contrast 0.6 and 1.5. Our
  choice, not taken from literature or from the data (no measurement, see above).
- **Augmentation ranges** chosen to cover the grid: gain log-uniform 0.5 to 2.0 (a new step),
  offset ±0.2, contrast 0.6 to 1.5, gamma log-uniform 0.5 to 2.0, each p = 0.5 and clipped.
  Geometry, crop-box jitter, depth gain curve and the DEC-068 fill stay as in `us_mild_v2`.
- **The percentiles are taken over all pixels of the crop**, as in the option shown to the user.
  The analyst first considered only the pixels above 0 (so the black corners outside the scan
  area would not pin the 1st percentile at 0), and dropped it: an offset on the whole image turns
  those corners grey and brings them into the percentiles, so the result would no longer equal
  that of the unchanged image. With all pixels, every pixel moves by the same affine change and
  so do the percentiles.
- **All six recipes of DEC-077 use both parts.** There is no arm without the normalisation, so
  the shift test cannot say how much each part contributes.

What normalisation can and cannot do (the analyst's reasoning, given to the user): a gain, an
offset or a contrast change about the mean, applied to the whole crop, is an affine change of
the grey values, and the percentiles move with it, so it is undone exactly as long as no pixel
clips; gamma is not affine, clipping loses information, and a scanner gain that leaves the
black area black is not a whole-image change, so those stay with the augmentation.

## Conclusion

[DEC-079](../decisions/DEC-079-epic1-brightness-robustness-augmentation-percentile-norm-shift-test.md):
augmentation `us_bright_v1`, per-image percentile normalisation inside every epic 1 model
(argument, default off), and a brightness shift test reported in every epic 1 EXP record, not in
the bar. Board: [TASK-191](../../backlog/tasks/task-191%20-%20Augmentation-us_bright_v1-us_mild_v2-with-a-gain-step-and-wide-offset-contrast-and-gamma-ranges-for-brightness-robustness-synthetic-tests-DEC-079.md), [TASK-192](../../backlog/tasks/task-192%20-%20Per-image-percentile-normalisation-inside-transunet-dinov3_convnext_seg-and-resenc_unet-1st-to-99th-percentile-of-the-pixels-above-0-mapped-to-0-1-before-the-encoder-mean-and-std-default-off-synthetic-tests-DEC-079.md), [TASK-193](../../backlog/tasks/task-193%20-%20Brightness-shift-test-grid-bright_grid_v1-on-the-checkpoint-selected-on-val-per-sample-records-per-level-W1-and-W2-drops-per-organ-with-paired-cluster-bootstrap-CIs-synthetic-tests-DEC-079.md) (method), listed in DEC-079 Consequences.

## Open questions

- How many samples of 261023 were brightened before scraping, and whether some are copies of
  other images across train and val (the check was skipped). Reopen if the shift test shows
  large drops, or W3 (val minus test) is large.
- Whether a criterion on the shift test enters the bar of a later round.
- The share of each part (augmentation, normalisation) in the result: needs an arm without the
  normalisation.
