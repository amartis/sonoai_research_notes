---
id: DIS-040
title: Epic 1 point 6 - optimisation strategy - optimiser per model lineage, leaf-Dice label-set loss, percentile normalisation in the reader, batch 32 for 30 epochs in fp32 on RunPod
status: concluded
created: 2026-11-20
outcomes: [DEC-080]
related: [DEC-065, DEC-066, DEC-077, DEC-079, DEC-006, DEC-049, DEC-068, DEC-076, DEC-048]
---
# DIS-040: Epic 1 point 6 - optimisation strategy

## Question

[DEC-065](../decisions/DEC-065-mission-upper-abdomen-anatomy-segmentation.md) (mission:
upper-abdomen anatomy segmentation) point 6 asks for the loss, optimiser, schedule,
augmentation, epochs and sanity steps of the six recipes of
[DEC-077](../decisions/DEC-077-epic1-model-choice-six-recipes.md). It is the last point before
the training task. Left open by earlier points:

- [DEC-066](../decisions/DEC-066-epic1-model-task-label-set-softmax.md) rule 4: which Dice form
  (marginalized Dice or leaf-Dice) and which weights; rule 7: when the sigmoid comparison run
  happens.
- DEC-077 rule 4: one set of settings for all recipes, unless point 6 gives pretrained encoders
  their own; seeds.
- [DEC-079](../decisions/DEC-079-epic1-brightness-robustness-augmentation-percentile-norm-shift-test.md)
  (brightness robustness, accepted the same day): `us_bright_v1` and per-image percentile
  normalisation for all six recipes; the rest is point 6.

Where the code stands (2026-11-20, master `f1f33d0`): `sonoai.training.optim` registers only
`sgd` and the schedules `constant` and `poly`; no AdamW, warm-up, parameter groups, encoder
freeze or EMA. The label-set losses `marginalized_dice_ce` and `leaf_dice_ce` exist
([TASK-157](../../backlog/tasks/task-157%20-%20Label-set-losses-for-the-anatomy-task-per-pixel-allowed-class-bitmask-target-builder-marginalized-cross-entropy-marginalized-Dice-and-leaf-Dice-synthetic-tests-DEC-066.md)) with default weights 1.0 and 1.0, and a recipe cannot set loss
weights (`TrainRecipe` has no `loss_args`). The loop supports fp32, bf16 and fp16 and
gradient clipping. The epic 1 sample file v3 has train 14,836, val 3,007 and test 2,168 samples
([anatomy_e1_split.md](../datasets/261023/anatomy_e1_split.md)). RunPod has a machine profile
(`runpod_a100`: A100 80 GB, micro-batch 32, enc1 only), but no run has used it, and
`deploy/runpod/run.sh` still calls the old `configs/experiments` interface.

Sources: the literature note
[epic1-anatomy-segmentation-models-and-papers.md](../literature/epic1-anatomy-segmentation-models-and-papers.md)
and the journal note
[2026-11-19-optimiser-choice-claude.md](../journal/2026/2026-11-19-optimiser-choice-claude.md)
(AdamW against SGD by architecture, the user's input for this session). The UltraBench 2
fine-tuning protocol ([arXiv:2609.28610](https://arxiv.org/abs/2609.28610) v2, HTML) was read
again on 2026-11-20 through a web-fetch tool: Section 4.1 verbatim; Appendix C and Table 4 only
through a tool summary (marked below).

## Options considered

Table 1. The questions of this session, the analyst's recommendation, the user's choice and when
the recommendation would have won.

| # | Question | Analyst's recommendation | Chosen (the user) | When the recommendation would have won |
|---|---|---|---|---|
| 1 | Optimiser | the [EXP-003](../experiments/EXP-003-transunet-r50-b16-from-scratch-512-and-224-lseg-cirrhosis-v4.md) SGD for all six (in the repo, shown to train, no code; DEC-065 rule 4.6) | **by lineage**: EXP-003 SGD for `transunet` (R1, R2); AdamW with a frozen-encoder start (UltraBench 2 style) for DINOv3 ConvNeXt-B (R4 to R6), from Section 2 of the journal note | if a single optimiser must hold across all recipes so that R1 against R4 to R6 differs only in the model |
| 2 | Label-set loss | leaf-Dice + marginalized cross-entropy, 0.5 / 0.5 | first marginalized Dice, then (change of thought) **leaf-Dice 0.5 / 0.5 with marginalized cross-entropy** | (taken) |
| 3 | Augmentation | `us_mild_v2`; then, once DEC-079 was found, keep DEC-079 (`us_bright_v1`) | **`us_bright_v1`**, and the percentile normalisation is **preprocessing in the reader**, not a step inside the model | (normalisation) if checkpoints are served outside this repository's reader, where a step inside the model cannot be forgotten |
| 4 | Optimiser of R3 (`resenc_unet`, from scratch) | EXP-003 SGD, as R1 and R2 | **accepted** | - |
| 5 | AdamW values of R4 to R6 | the UltraBench 2 values (below) | **accepted** | - |
| 6 | Length, batch, seeds, machine (the user: RunPod first, the priority) | global batch 32, 30 epochs, train evaluation every 5 epochs; seed 0 for all six, then seeds 1 and 2 for the best recipe; all on RunPod, after a readiness and timing check | **accepted** | - |
| 7 | Precision on the A100 | bf16 autocast | **fp32, no autocast** | if the run cost matters more than staying at the [DEC-006](../decisions/DEC-006-losses-optim-tracking.md) default |
| 8 | Sanity step before the full runs (DEC-065 lean: overfit a small subset) | an overfit check per recipe on 64 train samples | **later**: a Parked task; the user starts and watches each run, and wants TensorBoard over the network as on the GPU box | if a broken path would otherwise be found only after a full run |
| 9 | Sigmoid comparison run (DEC-066 rule 7) | after the six seed-0 verdicts, on the best recipe; its task Parked now | **accepted** | - |

Alternatives shown and not chosen: AdamW with LP-FT for all six recipes, and SGD with LP-FT for
the pretrained ones (question 1); `marginalized_dice_ce` and `leaf_dice_ce` at the default 1 / 1
(question 2); nnU-Net SGD (momentum 0.99, lr 1e-2) for R3 (question 4); the journal note's AdamW
values (head lr 1e-4, encoder 0.1 times the head, weight decay 0.05) and UltraBench 2 without
layer-wise decay (question 5); global batch 24 as in EXP-003, and 3 seeds per recipe
(question 6).

Said once by the analyst and kept by the user:

- With an optimiser by lineage, R1 against R4 to R6 differs in model **and** optimiser, so
  that comparison cannot say which of the two made the difference. R1 against R2 (pretraining)
  and R4 against R5 and R6 (decoder) stay clean.
- Fidon et al. 2021 ([arXiv:2107.03846](https://arxiv.org/abs/2107.03846)) found leaf-Dice
  better than marginalized Dice on all 8 structures (said when the user first chose
  marginalized Dice; the user then changed to leaf-Dice).

Decided by the analyst and told to the user:

- **Where the normalisation runs in the reader.** After the brightness steps of `us_bright_v1`
  (steps 2 to 6 of DEC-079 Table 1) and before the flip, the affine and the [DEC-068](../decisions/DEC-068-us-mild-v2-zero-image-and-background-outside-the-crop.md) fill, with
  its percentiles taken over the pixels of the original crop box. Then an augmented offset is
  undone in full (DEC-079 rule 2.3 noted that inside the model it is undone only in part, because
  the fill stays 0), and pixels of the jitter band, which are set to 0 at the end, do not move the
  percentiles. For every unaugmented read (val, test, the train evaluation) the original crop box
  is the whole image, so the step equals DEC-079 rule 2.1 as written. The shift test applies its
  level first and the normalisation after it, as at serving.
- **Monitoring.** TensorBoard on the pod, bound to 127.0.0.1 and seen through an SSH tunnel from
  machine01, as on the GPU box ([DEC-048](../decisions/DEC-048-tensorboard-on-the-gpu-box-through-an-ssh-tunnel.md)). RunPod's public HTTP proxy was not chosen: anyone with its URL
  would see the board (only aggregates are logged, DEC-006). That the proxy has no login is the
  analyst's understanding, not checked.
- **UltraBench 2 values.** Read verbatim (Section 4.1): AdamW; head lr 1e-3; encoder lr ceiling
  0.01 times the head lr; layer-wise lr decay for full fine-tuning; cosine schedule; encoder
  frozen for the first 1,000 steps, then its lr warmed up linearly from 0 over 1,000 steps;
  batch 32; at most 10,000 steps; evaluation every 100 steps and early stopping on val loss;
  Dice + cross-entropy with equal weights; "the hyperparameters, augmentations, and task heads
  were not optimized per model" (Section 6.2). From a tool summary of Appendix C and Table 4
  only, not read verbatim: weight decay 1e-2, decay factor 0.9 over 4 groups, gradient-norm clip
  1.0, minimum lr 0. Betas, eps and precision were not found. DEC-080 takes the unverified values
  as our choice.

Time and cost: not known. EXP-003 took 9.9 min per epoch for 10,331 train samples on the RTX 3060
(train evaluated every epoch). No RunPod run exists, so the minutes per epoch on the A100 in fp32
and the hourly price come from the readiness task's timing run, before any full run.

## Conclusion

[DEC-080](../decisions/DEC-080-epic1-optimisation-strategy.md) (accepted by the user, 2026-11-20): the settings of the
six recipes, the move of the percentile normalisation into the reader (it replaces DEC-079
rule 2.4), the run plan on RunPod and what is left for later. Board tasks: listed in DEC-080
Consequences.

## Open questions

- An overfit check before full runs (Parked task).
- The sigmoid comparison run, after the six seed-0 verdicts (Parked task).
- Weight averaging (SWAD or EMA) and stronger domain-generalisation methods: only if W3 fails.
- [TASK-182](../../backlog/tasks/task-182%20-%20Label-set-evaluation-reads-each-organs-state-from-the-sample-file-instead-of-from-the-bitmask-target-two-edge-cases-differ-via-a-TaskSamples-accessor-DEC-076.md) (in-run W1 and W2 read the organ state from the target, two edge cases differ
  from the sample file): still in Triage, for the user.
