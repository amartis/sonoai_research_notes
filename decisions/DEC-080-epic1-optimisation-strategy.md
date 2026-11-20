---
id: DEC-080
title: Epic 1 point 6 - optimisation strategy - EXP-003 SGD for transunet and resenc_unet, UltraBench 2 AdamW with a frozen-encoder start for DINOv3, leaf-Dice label-set loss, us_bright_v1 with percentile normalisation in the reader, batch 32 for 30 epochs in fp32 on RunPod
status: accepted
area: [training]
created: 2026-11-20
from: [DIS-040]
related: [DEC-065, DEC-066, DEC-077, DEC-079, DEC-006, DEC-068, DEC-076, DEC-045, DEC-048, DEC-024]
superseded_by:
---
# DEC-080: Epic 1 point 6 - optimisation strategy

## Context

[DEC-065](DEC-065-mission-upper-abdomen-anatomy-segmentation.md) (mission: upper-abdomen
anatomy segmentation) point 6 asks for the loss, optimiser, schedule, augmentation, epochs and
sanity steps of the six recipes R1 to R6 of
[DEC-077](DEC-077-epic1-model-choice-six-recipes.md). Fixed before: background plus four organs,
one softmax, label-set losses ([DEC-066](DEC-066-epic1-model-task-label-set-softmax.md));
selection on val by mean W1, mean W2, val loss
([DEC-076](DEC-076-epic1-metrics-label-set-score-selection-ci-and-pass-rule.md) rule 3);
`us_bright_v1`, per-image percentile normalisation and the brightness shift test
([DEC-079](DEC-079-epic1-brightness-robustness-augmentation-percentile-norm-shift-test.md)).
Train has 14,836 samples (epic 1 sample file v3). Options, sources and what was checked:
[DIS-040](../discussions/DIS-040-epic1-optimisation-strategy.md).

Terms: **head** is every parameter of a model that is not in its pretrained encoder (decoder
and output layer); **encoder** is the DINOv3 ConvNeXt-B backbone of `dinov3_convnext_seg`
(stem and stages 1 to 4). **Step** is one optimiser step of the global batch
([DEC-006](DEC-006-losses-optim-tracking.md)).

## Decision

### 1. Optimiser and schedule, by model lineage (the user's choice)

| Setting | R1, R2 (`transunet`), R3 (`resenc_unet`) | R4 to R6 (`dinov3_convnext_seg`) |
|---|---|---|
| Optimiser | SGD, momentum 0.9, Nesterov | AdamW, betas (0.9, 0.999), eps 1e-8 (torch defaults) |
| Initial lr | 1e-3 on all parameters | head 1e-3; encoder peak 0.01 × head lr, times the layer-wise factor below |
| Layer-wise lr factor (encoder) | - | stage 4 (deepest) 1.0, stage 3 0.9, stage 2 0.81, stage 1 and the stem 0.729 |
| Weight decay | 1e-4 on all parameters | 1e-2, decoupled, on all parameters |
| Schedule | poly per step, `lr0 * (1 - t / T) ** 0.9`, no warm-up | head: cosine per step from 1e-3 to 0 at step T, no warm-up |
| Encoder start | - | steps 0 to 999: encoder frozen (not updated; its optimiser state does not advance); steps 1,000 to 1,999: encoder lr factor rises linearly from 0 to 1; from step 2,000 on: factor 1 |
| Encoder lr at step t | - | 0.01 × head_lr(t) × warm-up factor(t) × layer-wise factor |
| Gradient clipping | none | global norm 1.0 |

Table 1. Optimiser and schedule of the six recipes. T is the number of steps of the run
(rule 4). The left column is the optimisation of
[EXP-003](../experiments/EXP-003-transunet-r50-b16-from-scratch-512-and-224-lseg-cirrhosis-v4.md)
(the DEC-006 preset with Nesterov momentum). The right column follows UltraBench 2 (Radhachandran
et al., ML4H 2026, [arXiv:2609.28610](https://arxiv.org/abs/2609.28610) v2, Section 4.1, read
verbatim on 2026-11-20: AdamW, head lr 1e-3, encoder ceiling 0.01 × head lr, layer-wise lr decay,
cosine schedule, encoder frozen for 1,000 steps then warmed up linearly over 1,000 steps). Our
choice, because the source was read only through a tool summary or does not state it: weight
decay 1e-2, decay factor 0.9 per ConvNeXt stage (the stem with stage 1), clipping at 1.0, cosine
to 0, betas and eps, decay on all parameters, and early stopping replaced by rule 4.

R1 against R2 (pretraining), R2 against R3 (architecture, both from scratch) and R4 against R5
and R6 (decoder) each differ in one thing. R1 against R4 to R6 differs in model and optimiser,
so that comparison does not say which of the two made a difference (DEC-077 rule 4 is replaced
here).

### 2. Loss

All six recipes: `leaf_dice_ce` with `ce_weight` 0.5 and `dice_weight` 0.5: 0.5 marginalized
cross-entropy + 0.5 leaf-Dice ([DEC-066](DEC-066-epic1-model-task-label-set-softmax.md) rule 4;
Fidon et al., MICCAI 2021, [arXiv:2107.03846](https://arxiv.org/abs/2107.03846)). The weights
need a `loss_args` recipe field (the registered default is 1.0 and 1.0).

### 3. Augmentation and percentile normalisation in the reader

1. **Augmentation** of the train split: `us_bright_v1`
   (DEC-079 rule 1), for all six recipes.
2. **The per-image percentile normalisation is a reader step, not a model step** (the user's
   choice; it replaces DEC-079 rule 2.4). Formula and the skip below 1/255: DEC-079 rule 2.1,
   with the percentiles taken over the pixels of the original crop box. It is named
   (`percentile_v1`) and recorded in the recipe's `Data`, default off.
3. **Where it runs:**
   - train: after the brightness steps of `us_bright_v1` (DEC-079 Table 1, steps 2 to 6) and
     before the flip, the affine and the [DEC-068](DEC-068-us-mild-v2-zero-image-and-background-outside-the-crop.md) fill, so an augmented offset is undone in full,
     and the jitter band (set to 0 at the end) does not move the percentiles;
   - every unaugmented read (val, test, the train evaluation): right after the crop is read;
     there the original crop box is the whole image, so the step is DEC-079 rule 2.1 as written;
   - the brightness shift test (DEC-079 rule 3): the level's change first, then this step;
   - serving: the same reader step; a checkpoint alone does not normalise.
4. The fixed mean and std of DEC-077 rule 3 stay inside the models and run after this step.

### 4. Length, batch, precision, evaluation

- Global batch **32** for all six; **30 epochs**, 463 steps per epoch (14,836 // 32), T = 13,890
  steps. The R4 to R6 encoder is frozen for the first 1,000 steps (about 2.2 epochs).
- **fp32, no autocast** (the user's choice; DEC-006 default).
- Evaluation of val and test every epoch; the train split (unaugmented, [DEC-045](DEC-045-per-sample-confusion-matrices-in-runs.md) rule 3) every
  5 epochs; per-sample records on (DEC-045, DEC-076 rule 6.1). Selection: DEC-076 rule 3.
- If the selected epoch is 27 or later, the EXP record flags the run as possibly undertrained. A
  longer run is a new consult session, not a change of this rule.

### 5. Seeds, machine, who runs

1. One run per recipe with **seed 0**, on **RunPod** (Secure Cloud, one A100 80 GB, machine
   profile `runpod_a100`, micro-batch 32, so no accumulation), enc1 data only
   ([DEC-024](DEC-024-plain-never-leaves-machine01-ec2-label-studio-decrypts-in-ram.md)). The
   DEC-076 rule 5 verdict of each recipe is that of its seed-0 run (DEC-077 rule 5).
2. Then **seeds 1 and 2** for the recipe with the highest val mean W1 at seed 0, on RunPod. The
   EXP record shows all three seeds; the verdict stays that of seed 0.
3. **The user starts and watches each run.** Before the first full run, a readiness check on
   RunPod: the image, a network volume with `261023_enc1`, the pretrained weights, and a timing
   run of one epoch of R1 and of R4 that gives minutes per epoch, peak memory and the hourly price.
4. **Monitoring:** TensorBoard on the pod, bound to 127.0.0.1, seen from machine01 through an SSH
   tunnel, as on the GPU box ([DEC-048](DEC-048-tensorboard-on-the-gpu-box-through-an-ssh-tunnel.md)).
5. A later run of a recipe on the GPU box uses the same recipe with micro-batch 8 × accumulation
   4. The `transunet` decoder's BatchNorm then sees 8 samples instead of 32, so such a run is not
   compared directly with the RunPod runs.
6. The brightness shift test (DEC-079 rule 3) runs on every run, after training.

### 6. Not now

- **Overfit check** before the full runs (the DEC-065 lean): later; a Parked task.
- **Sigmoid comparison run** (DEC-066 rule 7): after the six seed-0 verdicts, on the best recipe;
  its code and run are a Parked task.
- Weight averaging (SWAD, EMA), bf16, other augmentations: not in this round; only through a new
  consult session, for example if W3 fails.

## Consequences

- DEC-077 rule 4 (the same settings for all recipes) is replaced by rule 1. DEC-079 rule 2.4
  (normalisation inside the model) is replaced by rule 3; the model argument of DEC-079 rule 2.4
  is not built. DEC-065 Table 3 row 6 and DEC-066 rules 4 (Dice form, weights) and 7 (when) are
  settled here.
- Board (milestone m-1):
  - method: [TASK-071](../../backlog/tasks/task-071%20-%20Recipe-fields-for-DEC-006-selection-and-loss-args-Eval.select-as-several-criteria-Eval.select_tol-TrainRecipe.loss_args.md) cut down to the `loss_args` field; [TASK-192](../../backlog/tasks/task-192%20-%20Per-image-percentile-normalisation-inside-transunet-dinov3_convnext_seg-and-resenc_unet-1st-to-99th-percentile-of-the-pixels-above-0-mapped-to-0-1-before-the-encoder-mean-and-std-default-off-synthetic-tests-DEC-079.md) rewritten for the reader step
    (after [TASK-191](../../backlog/tasks/task-191%20-%20Augmentation-us_bright_v1-us_mild_v2-with-a-gain-step-and-wide-offset-contrast-and-gamma-ranges-for-brightness-robustness-synthetic-tests-DEC-079.md)); [TASK-193](../../backlog/tasks/task-193%20-%20Brightness-shift-test-grid-bright_grid_v1-on-the-checkpoint-selected-on-val-per-sample-records-per-level-W1-and-W2-drops-per-organ-with-paired-cluster-bootstrap-CIs-synthetic-tests-DEC-079.md) applies its level before the reader step (after TASK-192); a new
    [TASK-194](../../backlog/tasks/task-194%20-%20AdamW-path-for-the-DINOv3-recipes-AdamW-head-and-encoder-parameter-groups-layer-wise-lr-factor-per-ConvNeXt-stage-encoder-frozen-then-warmed-up-cosine-schedule-synthetic-tests-DEC-080-rule-1.md) for the AdamW path of rule 1; [TASK-195](../../backlog/tasks/task-195%20-%20Epic-1-recipes-R1-to-R6-for-seg_anatomy_v2-and-their-RunPod-plans-models-of-DEC-077-optimisation-of-DEC-080-us_bright_v1-with-percentile_v1-leaf_dice_ce-0.5-0.5-batch-32-30-epochs-fp32-load-test-without-training-DEC-080-DEC-077.md) for the six recipe files and the RunPod plans;
    [TASK-183](../../backlog/tasks/task-183%20-%20Epoch-table-and-TensorBoard-view-show-W1-and-W2-for-label-set-evaluation-records-today-they-show-only-the-loss-and-empty-FDSC-fields.md) (W1 and W2 in the epoch table) to To Do, for monitoring;
  - infra: [TASK-196](../../backlog/tasks/task-196%20-%20RunPod-for-epic-1-run.sh-for-plans-user-runbook-TensorBoard-SSH-tunnel-1-epoch-timing-run-of-R1-and-R4-DEC-080-rule-5.md), RunPod readiness, run script, TensorBoard tunnel and the timing run (rule 5.3, 5.4);
  - exp: [TASK-197](../../backlog/tasks/task-197%20-%20Epic-1-runs-on-RunPod-R1-to-R6-at-seed-0-then-seeds-1-and-2-of-the-best-recipe-shift-test-EXP-record-with-the-DEC-076-verdict-per-recipe-DEC-080.md), the six seed-0 runs, seeds 1 and 2 of the best recipe, the shift test and the EXP
    record;
  - Parked, `needs-decision`: [TASK-198](../../backlog/tasks/task-198%20-%20Decide-an-overfit-check-per-epic-1-recipe-before-its-full-run-DEC-080-rule-6.md) (the overfit check); [TASK-199](../../backlog/tasks/task-199%20-%20Decide-sigmoid-comparison-run-of-the-best-epic-1-recipe-one-sigmoid-per-organ-with-unknown-outputs-masked-DEC-066-rule-7-DEC-080-rule-6.md) (the sigmoid comparison).
- Cost: not known until the timing run. EXP-003 took 9.9 min per epoch for 10,331 train samples
  on the RTX 3060; no A100 figure exists here.
- Reversal: free before the first run. After it, a change of rule 1, 2, 3 or 4 means retraining
  the recipes it touches (three or six runs); rule 5.2 and 6 add runs without changing the
  others.
