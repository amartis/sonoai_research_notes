---
id: DIS-067
title: Epic 3 model and optimisation at 512 px - architecture, balancing, loss and the low importance of ascites, augmentation, precision and length
status: concluded
created: 2026-11-26
outcomes: [DEC-115]
related: [DEC-045, DEC-077, DEC-079, DEC-080, DEC-100, DEC-108, DEC-109, DEC-110, DEC-112, DEC-114, DIS-052]
---
# DIS-067: Epic 3 model and optimisation

## Question

The model and optimisation point of the epic 3 mission
([DEC-100](../decisions/DEC-100-epic3-mission-spot-liver-diseases.md), mission of epic 3, rule 7):
architecture and pretraining, loss and the low importance of `ascites`, the balancing method (DEC-100
rule 6), augmentation, precision and length at 512 px. It could start once checkpoint selection was
decided ([DEC-114](../decisions/DEC-114-checkpoint-selection-in-two-groups-assessors-and-drawers.md),
two groups, assessors by image-level AUC and drawers by Dice).

Terms: the **four spot classes** are `hepatoma`, `hemangioma`, `hepatic_cyst`, `hepatic_stone`;
**cirrhosis negatives** are samples with hepatoma negative and cirrhosis positive. **Repeat-factor
sampling**: each training sample is drawn more often the rarer its rarest class.

## Facts checked

- Train split of the epic 3 sample file ([split record](../datasets/261023/spot_e3_split.md), Table 1):
  11,329 samples; positives hepatoma 967 (8.54%), hemangioma 103 (0.91%), cyst 64 (0.56%), stone 184
  (1.62%), ascites 89; cirrhosis negatives 305 (2.69%). A random batch of 32 holds on average 2.7
  hepatoma, 0.29 hemangioma, 0.18 cyst, 0.52 stone.
- Epic 1 at 224 px ([DIS-052](DIS-052-epic1-next-recipes-after-six-seed0-runs.md), Epic 1 results):
  the three DINOv3 ConvNeXt-B recipes led and their decoders differed by at most 0.004 in validation
  mean Dice; R5 (U-Net-style decoder) had a higher test W2 liver than R4 (MLP head), not significant.
  Validation there was by image; in epic 3 it is by whole datasource groups
  ([DEC-108](../decisions/DEC-108-epic3-split-test-and-validation-by-whole-groups.md), epic 3 split).
- Epic 1 step times on one A100 80 GB, fp32, batch 32, 224 px: R4 0.317 s, R5 0.305 s
  ([RunPod cost note](../journal/2026/2026-11-24-runpod-gpu-cost-claude.md), Table 1). Peak memory was
  never logged.
- Code on master: `leaf_dice_ce` computes the Dice per sample; no sampler and no class weights exist
  for the segmentation trainer (`sonoai.training.loop` shuffles uniformly); bf16 autocast exists
  (`Optim.precision`). The DINOv3 decoders contain BatchNorm.
- Repeat-factor sampling, r(c) = max(1, √(t / f(c))) with a sample taking the highest factor of its
  classes: read in Detectron2's `RepeatFactorTrainingSampler`
  ([code](https://ide-kyxt.pcl.ac.cn/GiRay/detectron/src/branch/master/detectron2/data/samplers/distributed_sampler.py)),
  which cites LVIS ([arXiv:1908.03195](https://arxiv.org/pdf/1908.03195v2.pdf), Appendix B.2; the
  appendix not read). nnU-Net's "more than a third of the samples of a batch hold foreground"
  ([arXiv:1809.10486](https://arxiv.org/pdf/1809.10486)): from a search summary, not read.

## Options considered

| # | Question | Recommendation (accepted) | Why | Best alternative, and when it would win |
|---|---|---|---|---|
| 1 | Architecture | DINOv3 ConvNeXt-B with the U-Net-style decoder (Epic 1 R5), one architecture | Epic 1 lead of DINOv3; learned upsampling to full size for small outlines (median stone 19 px at 512; reasoning, not measured); same speed as the MLP head | Both decoders at seed 0, keep the better: if the decoder should be settled by data; one more run |
| 2 | Balancing; low importance of ascites | Repeat-factor sampling, t = 0.2, over the four spot classes and the cirrhosis negatives; ascites out of the sampler, no loss weight | Doubles the spot share and keeps about 78% of a batch negative for the specificity bar; the square root avoids 17-fold repeats of a cyst; no change to the label-set loss | A fixed share (at least a third of each batch with a spot class, nnU-Net style), or t = 0.3: if hemangioma or cyst Dice stays near 0 |
| 3 | Precision and length | bf16, 20 epochs, after a one-epoch timing run | fp32 at batch 32 and 512 px may not fit in 80 GB, and accumulation changes BatchNorm; DINOv3 recipes were selected at epochs 15 to 19 in Epic 1; about 4.2 h instead of about 6.3 h per run (estimates) | fp32 and 30 epochs as Epic 1 ([DEC-080](../decisions/DEC-080-epic1-optimisation-strategy.md)): for an exact match with Epic 1 settings |

Table 1. The three questions put to the user, with the analyst's recommendation, all accepted on
2026-11-26.

Table 2. Repeat-factor sampling at three thresholds t (arithmetic from the train counts above, overlaps
of classes ignored; draws in proportion to the weight, as many per epoch as train holds). Per class:
repeat factor r, and expected samples per batch of 32. Spot share = share of drawn samples holding a
spot class.

| t | hepatoma | hemangioma | cyst | stone | cirrhosis negatives | Spot share |
|---|---|---|---|---|---|---|
| none (natural) | 1, 2.7 | 1, 0.29 | 1, 0.18 | 1, 0.52 | 1, 0.86 | 11.6% |
| 0.1 | 1.08, 2.7 | 3.32, 0.88 | 4.21, 0.69 | 2.48, 1.18 | 1.93, 1.52 | 17.0% |
| **0.2 (chosen)** | 1.53, 3.5 | 4.69, 1.14 | 5.95, 0.90 | 3.51, 1.53 | 2.73, 1.97 | 22.1% |
| 0.3 | 1.87, 4.0 | 5.74, 1.32 | 7.29, 1.04 | 4.30, 1.76 | 3.34, 2.26 | 25.5% |

At t = 0.2 a cyst is drawn about 5 times per epoch (5.95 × 11,329 / 13,529, the sum of the weights).

Kept from Epic 1 without a question (the user did not object): loss `leaf_dice_ce` 0.5/0.5 (DEC-080
rule 2); the DINOv3 AdamW path (DEC-080 rule 1); `us_bright_v1` and `percentile_v1` ([DEC-079](../decisions/DEC-079-epic1-brightness-robustness-augmentation-percentile-norm-shift-test.md), DEC-080
rule 3). A batch-wide Dice, which also penalises outlines drawn on negative images, is the first
alternative to the loss if specificity fails.

Said once by the analyst: no start from an Epic 1 checkpoint, because Epic 1 trained on groups that
may be in the epic 3 test groups (not checked).

**Correction after the questions.** The question on precision said test would be evaluated only on the
surviving checkpoints after training. The trainer evaluates test every epoch, as
[DEC-045](../decisions/DEC-045-per-sample-confusion-matrices-in-runs.md) rule 3 (train, val and test
every epoch, test never used for a choice) asks; DEC-115 keeps that, and test is read only for the
DEC-114 pair and survivors (DEC-100 rule 5). This needs no new code and costs about 1.5 min per epoch
(estimate), counted in the DEC-115 cost.

## Estimates

Scaled from the Epic 1 R5 step time by pixel count (5.2 times), not measured, bf16 gain not counted:
about 1.6 s per step, 354 steps per epoch, about 9.4 min of training plus about 3 min of val and test
evaluation per epoch; about 4.2 h and $9 per 20-epoch run at $2.19/h. The timing run of TASK-294
replaces these.

## Conclusion

Accepted by the user on 2026-11-26:
[DEC-115](../decisions/DEC-115-epic3-model-balancing-loss-augmentation-precision-length.md) (epic 3
model and optimisation). Board, milestone m-1: TASK-292 (repeat-factor sampler, method), TASK-293
(epic 3 recipes, stretch and fit-scale, RunPod plans and the one-epoch timing plan, method; after
TASK-292, [TASK-286](../../backlog/tasks/task-286%20-%20Epic-3-evaluation-for-seg_spot_v1-top-50-image-score-pixel-scores-with-the-stone-counted-for-its-mass-per-sample-record-validation-AUC-and-Dice-measures-synthetic-tests-DEC-112.md) epic 3 evaluation and [TASK-288](../../backlog/tasks/task-288%20-%20Checkpoint-selection-mode-that-keeps-several-checkpoints-and-removes-the-beaten-ones-weighted-criteria-floors-steps-removal-threshold-veto-near-copy-rule-cap-primary-by-weighted-sum-set-by-the-recipe-synthetic-tests-DEC-113.md) two-group selection mode), TASK-294 (one-epoch timing
run on RunPod, exp; after TASK-293).

## Open questions

- The organisation point (DEC-100 rule 7): run plan (stretch against fit-scale, strict_v1 then
  loose_v1), seeds, EXP record layout.
- Whether micro-batch 32 fits at 512 px in bf16 (TASK-294).
- MLP decoder comparison, class weights, focal or batch-wide Dice, presence head, weight averaging:
  only through a new consult session, after the first results.
