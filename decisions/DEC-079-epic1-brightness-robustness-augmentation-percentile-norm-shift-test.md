---
id: DEC-079
title: Epic 1 brightness robustness - augmentation us_bright_v1, per-image percentile normalisation inside every epic 1 model, and a brightness shift test reported in every EXP record (not in the bar)
status: accepted
area: [training]
created: 2026-11-20
from: [DIS-039]
related: [DEC-065, DEC-049, DEC-068, DEC-076, DEC-077]
superseded_by:
---
# DEC-079: Epic 1 brightness robustness

## Context

The user (2026-11-20): the epic 1 model's performance must not change when its input is
deliberately brightened or darkened, because (1) a countable share of the samples of 261023 were
brightened before we scraped them, and (2) at serving time users may send brightened or darkened
images (deliberate colour control, device settings). Today the only brightness changes in training
are the mild ones of `us_mild_v2` ([DEC-068](DEC-068-us-mild-v2-zero-image-and-background-outside-the-crop.md),
values of [DEC-049](DEC-049-mild-ultrasound-augmentation-us-mild-v1.md) item 2); the models take
[0, 1] input with a fixed mean and std ([DEC-077](DEC-077-epic1-model-choice-six-recipes.md)
rule 3); nothing measures the effect of brightness on W1 and W2
([DEC-076](DEC-076-epic1-metrics-label-set-score-selection-ci-and-pass-rule.md)). Point 6
(optimisation strategy, including the augmentation) of
[DEC-065](DEC-065-mission-upper-abdomen-anatomy-segmentation.md) is not settled and no epic 1
training run exists. Discussion: [DIS-039](../discussions/DIS-039-epic1-brightness-robustness.md).

## Decision

### 1. Augmentation `us_bright_v1`

A new registered augmentation (DEC-049: a changed set is a new name; `us_mild_v1` and `us_mild_v2`
stay as they are). Steps in the order they run:

| # | Step | p | Values | Against `us_mild_v2` |
|---|---|---|---|---|
| 1 | crop-box jitter (before the crop) | 0.5 | each edge up to ±3% of the box side | same |
| 2 | gain, `x * g` | 0.5 | g log-uniform in [0.5, 2.0] | new step |
| 3 | offset, `x + b` | 0.5 | b uniform in [−0.2, 0.2] | was ±0.1 |
| 4 | contrast, `c * x + (1 − c) * mean(grey(x))` (torchvision `adjust_contrast`) | 0.5 | c uniform in [0.6, 1.5] | was 0.85 to 1.15 |
| 5 | gamma, `x ** γ` | 0.5 | γ log-uniform in [0.5, 2.0] | was 0.8 to 1.25 |
| 6 | depth gain curve | 0.3 | 3 gains in 0.8 to 1.2 | same |
| 7 | horizontal flip | 0.5 | | same |
| 8 | affine | 0.5 | rotation ±10°, scale 0.9 to 1.1, shift ±5% | same |

Table 1. Steps of `us_bright_v1`. Values are our choice, not tuned, set to cover the shift grid of
rule 3.

- Steps 2 to 6 act on the image only, the same way on its 3 channels, each followed by a clip to
  [0, 1] (the clip stands for the saturation of a brightened image).
- Every random value is drawn for every item in a fixed order, as in `us_mild_v1`.
- Outside the original crop box the image is 0 and the target is the task's target fill, as in
  `us_mild_v2` (DEC-068), applied last.

### 2. Per-image percentile normalisation inside the model

1. For each image of a batch, p1 and p99 are the 1st and 99th percentiles of all its pixel
   values, over all 3 channels together (linear interpolation, as `torch.quantile`). The image
   becomes `clamp((x − p1) / (p99 − p1), 0, 1)`. It is left unchanged when `p99 − p1 < 1/255`.
2. What it undoes: a gain, an offset or a contrast change about the mean, applied to the whole
   crop, is an affine change of every grey value, the black pixels outside the scan area included;
   p1 and p99 move with it, so it is undone exactly as long as no pixel clips. All pixels count
   for that reason: with only the pixels above 0, an offset would turn the black corners grey and
   bring them into the percentiles, and the result would differ.
3. What it does not undo: gamma, clipping (saturated pixels are lost), and a change that leaves
   the black corners black while the tissue brightens (as a scanner's gain may); rule 1 covers
   these. In training, the DEC-068 fill stays 0 after an augmented offset, so for those samples
   the offset is only partly undone; there is no fill at evaluation or serving.
4. Where: first in `forward`, before the mean and std of DEC-077 rule 3 (`dinov3_convnext_seg`,
   `transunet` with input normalisation); for `resenc_unet` it is the only input step. A model
   argument, default off, so recipes that do not set it, and their checkpoints, behave as before.
   No parameters and no state_dict keys. Being inside the model, it goes with the checkpoint to
   serving.

### 3. Brightness shift test (reported, not in the bar)

1. Grid `bright_grid_v1` (a changed grid is a new name), 10 levels, each applied to every pixel of
   the [0, 1] crop as read for evaluation (unaugmented), then clipped to [0, 1]:

   | Change | Formula | Levels |
   |---|---|---|
   | gain | `x * g` | g = 0.5, 0.7, 1.4, 2.0 |
   | offset | `x + b` | b = −0.2, +0.2 |
   | gamma | `x ** γ` | γ = 0.5 (brighter), 2.0 (darker) |
   | contrast | `c * x + (1 − c) * mean(grey(x))` | c = 0.6, 1.5 |

   Table 2. The levels of `bright_grid_v1`. Our choice, not from literature or from a measurement
   of 261023.
2. On the checkpoint selected on val (DEC-076 rule 3), on val and test, unchanged and at each
   level: per-sample records as DEC-076 rule 6.1; per split, organ c and level k: W1<sub>c</sub>,
   W2<sub>c</sub>, and the drops W1<sub>c</sub>(unchanged) − W1<sub>c</sub>(k) and
   W2<sub>c</sub>(unchanged) − W2<sub>c</sub>(k), with paired cluster-bootstrap 95% CIs (clusters,
   replicates and seed of DEC-076 rule 4; each replicate uses the same drawn clusters for both
   arms).
3. **Report only** (the user's choice): every epic 1 EXP record shows the table; the verdict stays
   W1, W2 and W3 (DEC-076 rule 5). A criterion on the shift test enters the bar only by a new DEC,
   set before the run it judges.

### 4. Use in epic 1

All six recipes of DEC-077 train with `us_bright_v1` and with the percentile normalisation on
(the user's choice, 2026-11-20). There is no arm without the normalisation, so the shift test
does not separate the two parts. Point 6 settles the rest (loss, optimiser, schedule, epochs,
seeds), and its training task runs the shift test on every run.

### 5. Not in this decision

- No measurement of the brightened share of 261023 and no check for brightened copies of one image
  across train, val and test (the user: skip; DIS-039 says when to reopen).
- Consistency loss, test-time averaging over brightness, histogram equalisation: not used.

## Consequences

- DEC-077 rule 3 is preceded, for the six recipes, by rule 2 here; DEC-077 is otherwise unchanged.
- DEC-065 Table 3 row 6 lean (`us_mild_v1`) is replaced, for the augmentation, by `us_bright_v1`.
- Board (method, milestone m-1): [TASK-191](../../backlog/tasks/task-191%20-%20Augmentation-us_bright_v1-us_mild_v2-with-a-gain-step-and-wide-offset-contrast-and-gamma-ranges-for-brightness-robustness-synthetic-tests-DEC-079.md) (augmentation `us_bright_v1`, rule 1), [TASK-192](../../backlog/tasks/task-192%20-%20Per-image-percentile-normalisation-inside-transunet-dinov3_convnext_seg-and-resenc_unet-1st-to-99th-percentile-of-the-pixels-above-0-mapped-to-0-1-before-the-encoder-mean-and-std-default-off-synthetic-tests-DEC-079.md)
  (per-image percentile normalisation in the three models, rule 2), [TASK-193](../../backlog/tasks/task-193%20-%20Brightness-shift-test-grid-bright_grid_v1-on-the-checkpoint-selected-on-val-per-sample-records-per-level-W1-and-W2-drops-per-organ-with-paired-cluster-bootstrap-CIs-synthetic-tests-DEC-079.md) (brightness shift
  test and its report, rule 3; depends on TASK-191). The GPU runs belong to the point 6 training
  task.
- GPU: the shift test adds 11 evaluations of val and test per run (no training).
- Reversal: all rules apply before the first epic 1 run and are cheap to change now; after runs,
  a change of rule 1 or 2 means retraining, a change of rule 3 only re-evaluation.
- [DEC-080](DEC-080-epic1-optimisation-strategy.md) (point 6, optimisation, 2026-11-20): rule 2.4
  is replaced by DEC-080 rule 3. The percentile normalisation is a reader step (`percentile_v1`
  in the recipe's `Data`), not a model argument, with its percentiles over the pixels of the
  original crop box; in training it runs after the brightness steps and before the flip, the
  affine and the fill; the shift test applies its level first. Rules 2.1 to 2.3 are unchanged.
