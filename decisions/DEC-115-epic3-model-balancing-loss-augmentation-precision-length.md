---
id: DEC-115
title: Epic 3 model and optimisation - DINOv3 ConvNeXt-B with the U-Net-style decoder, repeat-factor sampling with t 0.2 over the four spot classes and the cirrhosis negatives, the Epic 1 loss, optimiser and augmentation, bf16 for 20 epochs after a one-epoch timing run
status: accepted
area: [training]
created: 2026-11-26
from: [DIS-067]
related: [DEC-045, DEC-077, DEC-079, DEC-080, DEC-100, DEC-108, DEC-109, DEC-110, DEC-112, DEC-114]
superseded_by:
---
# DEC-115: Epic 3 model and optimisation

## Context

The model and optimisation point of the epic 3 mission
([DEC-100](DEC-100-epic3-mission-spot-liver-diseases.md), mission of epic 3, rule 7); options, counts and
estimates in [DIS-067](../discussions/DIS-067-epic3-model-and-optimisation.md) (epic 3 model and
optimisation). Fixed before: input 512 x 512 and two resize modes
([DEC-109](DEC-109-epic3-input-512-no-minimum-side-two-resize-modes.md), epic 3 data preparation); one
softmax over background, the four spot classes and ascites with allowed-class sets, task `seg_spot_v1`
([DEC-110](DEC-110-epic3-task-form-allowed-class-sets-stone-takes-the-overlap.md), epic 3 task form);
the image score and pixel scores ([DEC-112](DEC-112-epic3-metrics-image-score-stone-scoring-cirrhosis-bar.md),
epic 3 metrics); checkpoints kept in two groups, assessors by image-level AUC and drawers by Dice
([DEC-114](DEC-114-checkpoint-selection-in-two-groups-assessors-and-drawers.md)). Train holds 11,329
samples of the epic 3 sample file ([DEC-108](DEC-108-epic3-split-test-and-validation-by-whole-groups.md),
epic 3 split).

Terms: the **four spot classes** are `hepatoma`, `hemangioma`, `hepatic_cyst`, `hepatic_stone`;
**cirrhosis negatives** are samples with hepatoma negative and cirrhosis positive (DEC-108 rule 3,
column `cirrhosis_negative` of the sample file). **Head** and **encoder** as in
[DEC-080](DEC-080-epic1-optimisation-strategy.md) (Epic 1 optimisation strategy). **Repeat factor**: how
much more often than once per epoch, in expectation, a training sample is drawn.

## Decision

Accepted by the user on 2026-11-26 (the three recommendations of DIS-067 and the settings kept from Epic 1).

1. **Model.** `dinov3_convnext_seg` with `decoder: unet` (the U-Net-style decoder of Epic 1 recipe R5,
   [DEC-077](DEC-077-epic1-model-choice-six-recipes.md), Epic 1 model choice, Table 1), encoder weights
   DINOv3 ConvNeXt-B (timm `convnext_base.dinov3_lvd1689m`), input mean and std inside the model
   (DEC-077 rule 3), six output channels in the DEC-110 rule 1 order. One architecture for the first
   runs. No start from an Epic 1 checkpoint: Epic 1 trained on groups that may be in the epic 3 test
   groups (not checked).
2. **Balancing: repeat-factor sampling** of the train split (DEC-100 rule 6).
   1. Per class c of the sampler: f_c = share of train samples positive for c (for the cirrhosis
      negatives: `cirrhosis_negative` true); r_c = max(1, √(t / f_c)), t = 0.2.
   2. A sample's weight is the highest r_c of its classes, 1 when it has none of them. Unknown and
      negative states count as "not of the class".
   3. Classes of the sampler: the four spot classes and the cirrhosis negatives. `ascites` is not in it
      (DEC-100 rule 2).
   4. Each epoch draws as many samples as train has (11,329; 354 steps of 32, last part dropped), with
      replacement, with probability proportional to the weight, from a generator seeded by the recipe
      seed. Validation, test and the train evaluation are not resampled.
   5. t and the class list are recipe values; the run records f_c, r_c and the expected share of each
      class per batch.
   Expected effect (arithmetic from the split counts, overlaps ignored): samples with a spot class from
   11.6% to 22% of a batch; per batch of 32 about 3.5 hepatoma, 1.1 hemangioma, 0.9 cyst, 1.5 stone and
   2.0 cirrhosis negatives; a cyst drawn about 5 times per epoch.
3. **Loss.** `leaf_dice_ce` with `ce_weight` 0.5 and `dice_weight` 0.5 over the six classes, no class
   weights (DEC-080 rule 2; DEC-110 rule 6 filled). The low importance of `ascites` (DEC-100 rule 2) is:
   left out of the sampler (rule 2.3) and its weight 0.10 in checkpoint selection (DEC-114 rule 2); no
   loss weight.
4. **Optimiser and schedule**: the DINOv3 column of DEC-080 Table 1, unchanged: AdamW, head lr 1e-3,
   encoder peak 0.01 x head lr with the layer-wise factor 0.9 per stage, weight decay 1e-2, cosine per
   step to 0, encoder frozen for 1,000 steps then warmed up over 1,000 steps, gradient clipping at 1.0.
   T = 20 x 354 = 7,080 steps.
5. **Augmentation and normalisation**: `us_bright_v1` on the train split and the reader step
   `percentile_v1`, where DEC-080 rule 3 puts them; in fit-scale mode the padding counts as outside the
   crop box (DEC-109 rule 3).
6. **Precision, batch, length, evaluation.**
   1. bf16 autocast; global batch 32, micro-batch 32, no accumulation; 20 epochs.
   2. Val and test every epoch, train (unaugmented) every 5 epochs, per-sample records on, as
      [DEC-045](DEC-045-per-sample-confusion-matrices-in-runs.md) rule 3 (per-epoch evaluation) and
      DEC-080 rule 4. Test is read only for the DEC-114 pair and survivors (DEC-100 rule 5).
   3. Checkpoint selection: the DEC-114 mode.
   4. If an epoch of the DEC-114 pair is 18 or later, the EXP record flags the run as possibly
      undertrained (as DEC-080 rule 4 at 27 of 30).
7. **Timing run first.** One epoch of the rule 1 to 6 recipe on RunPod (one A100 80 GB, as DEC-080
   rule 5.1), started by the user: peak memory (`torch.cuda.max_memory_reserved`), median step time,
   minutes per epoch with evaluation, cost. If micro-batch 32 does not fit, nothing else is changed:
   the question goes back to the user (the decoder's BatchNorm would see fewer samples with
   accumulation).
8. **Left to the organisation point** (DEC-100 rule 7): the run plan (stretch against fit-scale,
   DEC-109 rule 3; strict_v1 then loose_v1, DEC-100 rule 3), seeds, and the EXP record layout.

## Consequences

- Estimated cost per 20-epoch run: about 12.5 min per epoch and about 4.2 h, about $9 at $2.19/h on one
  A100 80 GB (scaled from Epic 1 step times by pixel count; not measured; bf16 gain not counted). The
  timing run replaces the estimate.
- Not now (each needs a new consult session): the MLP decoder comparison; class weights, focal loss or a
  batch-wide Dice (the first choice if specificity fails); a presence head; weight averaging (EMA, SWA);
  larger or ultrasound-specific encoders; the sigmoid comparison
  ([TASK-283](../../backlog/tasks/task-283%20-%20Epic-3-sigmoid-comparison-run-after-the-first-softmax-results-one-sigmoid-per-class-with-an-unknown-class-masked-on-the-sample-on-the-chosen-recipe-DEC-110-rule-7.md),
  Parked).
- Board (milestone m-1): TASK-292 (repeat-factor sampler, method; rule 2); TASK-293 (epic 3 recipes,
  stretch and fit-scale, RunPod plans and the timing plan, method; rules 1 to 7; after TASK-292,
  [TASK-286](../../backlog/tasks/task-286%20-%20Epic-3-evaluation-for-seg_spot_v1-top-50-image-score-pixel-scores-with-the-stone-counted-for-its-mass-per-sample-record-validation-AUC-and-Dice-measures-synthetic-tests-DEC-112.md) epic 3 evaluation and [TASK-288](../../backlog/tasks/task-288%20-%20Checkpoint-selection-mode-that-keeps-several-checkpoints-and-removes-the-beaten-ones-weighted-criteria-floors-steps-removal-threshold-veto-near-copy-rule-cap-primary-by-weighted-sum-set-by-the-recipe-synthetic-tests-DEC-113.md) two-group selection mode); TASK-294 (one-epoch timing run,
  exp; rule 7; after TASK-293).
- Reversal: before the first run, recipe values; afterwards, new runs.
