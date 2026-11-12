---
id: EXP-003
title: TransUNet R50-ViT-B/16 from scratch at 512 px and 224 px on lseg_cirrhosis_v4, against the pretrained 224 px baseline
status: done
created: 2026-11-12
from: [DEC-050]
related: [DIS-023, DEC-006, DEC-043, DEC-044, DEC-045, DEC-047]
---
# EXP-003: TransUNet R50-ViT-B/16 from scratch at 512 px and 224 px on lseg_cirrhosis_v4

Board task: [TASK-112](../../backlog/tasks/task-112%20-%20Train-lseg_cirrhosis_v4-with-transunet_r50_b16-from-scratch-at-512-px-and-a-224-px-control-compare-with-cirr-v4-tu-e30-r5-in-an-EXP-record-DEC-050.md) (runs and this record); the model came from [TASK-111](../../backlog/tasks/task-111%20-%20Model-transunet_r50_b16-official-TransUNet-R50-ViT-B-16-get_r50_b16_config-no-class-token-dropout-0.1-no-weight-loading-DEC-050.md).

- Date: runs 2026-11-11 to 2026-11-12; analysis 2026-11-12
- Code commit: branch `claude/exp-t112-r50b16-scratch` at `e5105e9` (master `19c8539` plus the
  recipes and plans) for both new runs; the baseline as in [TASK-088](../../backlog/tasks/task-088%20-%20Train-lseg_cirrhosis_v4-on-the-fixed-sample-file-and-write-the-EXP-record-DEC-043-DEC-045.md) (run cirr-v4-tu-e30-r5).
  The box copy has no `.git`, so `meta.json` holds no commit; the commit is from
  `logs/exp-runs.md`.
- Config: `configs/train/recipes/lseg_cirrhosis_v4/261111_transunet_r50_b16_scratch_224.py` and
  `..._512.py`, with plans `configs/train/plans/lseg_cirrhosis_v4/<recipe>/261111_gpubox.py`;
  baseline `261109_transunet_dec047.py`
- Runs: `cirr-v4-tu-e30-r5` (baseline), `cirr-v4-r50b16-s224-r1`, `cirr-v4-r50b16-s512-r1`
- Data: dataset version 261023 (enc1 on the GPU box), the fixed sample file of
  [DEC-047](../decisions/DEC-047-cirrhosis-v4-cases-per-project-group-and-liver-fallback.md) (sha256 `59e174bf...c55a`, the same in all three runs), split by datasource group
  ([DEC-044](../decisions/DEC-044-cirrhosis-sample-set-quality-filter-and-split.md)): train 10,331 samples (477 positive), val 2,068 (97 positive; 41 datasource
  groups, 12 with a positive), test 1,378 (64 positive; 11 groups, 4 with a positive)

Writing standard: [docs/writing.md](../../docs/writing.md) ([DEC-021](../decisions/DEC-021-communication-and-research-writing-standards.md)).

## Question / hypothesis

Exploratory. [DEC-050](../decisions/DEC-050-transunet-r50-b16-from-scratch-512.md) asked two things ([DIS-023](../discussions/DIS-023-transunet-r50-b16-from-scratch-at-512.md)):

1. How does the official TransUNet R50-ViT-B/16 (`transunet_r50_b16`), trained from scratch,
   compare with the pretrained timm-based `transunet` baseline at the same input size, 224 px?
2. Does a larger input, 512 px, help this model from scratch (512 against 224)?

Hypothesis (DIS-023): finer texture at 512 px helps cirrhosis segmentation; the 224 px
from-scratch control separates the size effect from the pretraining effect.

## Setup

All three runs share the baseline recipe except the model and input size: the [DEC-006](../decisions/DEC-006-losses-optim-tracking.md)
optimiser (SGD, momentum 0.9, weight decay 1e-4, lr 1e-3, poly schedule, fp32) plus Nesterov
momentum, 0.5 CE + 0.5 Dice on the predicted cirrhosis layer, global batch 24, 30 epochs
(12,900 optimiser steps), seed 0, no augmentation, evaluation of train, val and test every
epoch with per-sample matrices ([DEC-045](../decisions/DEC-045-per-sample-confusion-matrices-in-runs.md)). The checkpoint was selected on val only
([DEC-043](../decisions/DEC-043-cirrhosis-task-gt-organ-layer-predicted-cirrhosis-only.md) rule 7: highest val joint cirrhosis DSC, then the tie-breakers). The resolved
new recipes differ from the baseline only in `model.name`, `model.args.pretrained`,
`model.args.img_size` and `data.input_size` (checked on machine01 without data). All runs on the GPU box (RTX 3060 12 GB).

Table 1. Runs compared in this record: model, weights, input size, how the global batch of
24 was made, the epoch selected on val, and wall-clock time.

| Run | Board task | Model | Weights at start | Input, px | Micro-batch × accumulation | Selected epoch (of 30) | Mean time per epoch incl. evaluation, min | Total, h |
|---|---|---|---|---|---|---|---|---|
| cirr-v4-tu-e30-r5 (baseline) | TASK-088 | `transunet` (timm-based) | ImageNet-21k pretrained | 224 | 8 × 3 | 17 | 9.9 | 4.95 |
| cirr-v4-r50b16-s224-r1 | TASK-112 | `transunet_r50_b16` (official) | none (from scratch) | 224 | 8 × 3 | 14 | 10.6 | 5.28 |
| cirr-v4-r50b16-s512-r1 | TASK-112 | `transunet_r50_b16` (official) | none (from scratch) | 512 | 4 × 6 | 30 | 53.3 | 26.66 |

Time: from the first training line to the "finished" line of each run's log, divided by 30.
The 512 px micro-batch came from a memory check on the GPU box with synthetic tensors (fp32,
one SGD step): peak reserved memory 5.65 / 7.91 / 9.99 GiB at micro-batch 2 / 3 / 4, and 6 or 8 did not fit in
12 GiB (TASK-112 notes). The 224 run was started by the exp agent after the user's approval;
the 512 run was started by the user (confirmed by the user on 2026-11-12; the original line in
`logs/exp-runs.md`, "approved by the user via the lead", was corrected by an appended line).

**Measures.** DSC (Dice similarity coefficient) and IoU (intersection over union) of the
cirrhosis layer, pooled over all pixels of the split (the run's `joint_dsc` / `joint_iou`).
Accuracy per sample (DEC-043 rule 6): a positive sample (any ground-truth cirrhosis pixel) is
correct when its own cirrhosis DSC is at least 0.5, a negative one when no cirrhosis pixel is
predicted. "Positives found" = correct positives; "positives with any cirrhosis predicted" =
positives with at least one predicted cirrhosis pixel. The thresholds (0.5, 1 pixel) are the task's fixed values, not tuned on any split.

**CI method.** 95% percentile intervals from a cluster bootstrap over datasource groups
(the split unit of DEC-044; patient ids are not in the sample file, so a patient bootstrap
was not possible): 2,000 replicates, seed 0, groups drawn with replacement within the split,
measures recomputed on the drawn samples. Differences between runs are paired: the same
draws for every run. Method as `sonoai.data.bmode_tune.bootstrap_ci` (Field and Welsh 2007,
doi:10.1111/j.1467-9868.2007.00593.x, cited there); computed by a one-off script on
machine01 from the fetched per-sample matrices and the sample file's group column. The
pooled DSC and accuracy recomputed this way equal the runs' own values.

## Results

Table 2. Cirrhosis measures of the checkpoint selected on val, per run and split, with 95%
CIs (cluster bootstrap over datasource groups). Val n = 2,068 samples (97 positive, 1,971
negative); test n = 1,378 (64 positive, 1,314 negative).

| Run | Split | Cirrhosis DSC (95% CI) | Cirrhosis IoU (95% CI) | Accuracy (95% CI) | Positives found, n (proportion, 95% CI) | Positives with any cirrhosis predicted, n | Negatives correct, n (proportion) |
|---|---|---|---|---|---|---|---|
| cirr-v4-tu-e30-r5 | val | 0.696 (0.529–0.741) | 0.534 (0.359–0.588) | 0.954 (0.907–0.979) | 82/97 (0.845, 0.558–0.924) | 92/97 | 1,891/1,971 (0.959) |
| cirr-v4-r50b16-s224-r1 | val | 0.611 (0.411–0.672) | 0.440 (0.259–0.507) | 0.924 (0.855–0.962) | 80/97 (0.825, 0.464–0.936) | 90/97 | 1,830/1,971 (0.928) |
| cirr-v4-r50b16-s512-r1 | val | 0.586 (0.424–0.631) | 0.414 (0.269–0.460) | 0.894 (0.793–0.951) | 77/97 (0.794, 0.433–0.896) | 91/97 | 1,771/1,971 (0.899) |
| cirr-v4-tu-e30-r5 | test | 0.047 (0.005–0.143) | 0.024 (0.002–0.077) | 0.890 (0.829–0.942) | 2/64 (0.031, 0.000–0.150) | 10/64 | 1,224/1,314 (0.932) |
| cirr-v4-r50b16-s224-r1 | test | 0.026 (0.000–0.041) | 0.013 (0.000–0.021) | 0.759 (0.671–0.839) | 1/64 (0.016, 0.000–0.036) | 16/64 | 1,045/1,314 (0.795) |
| cirr-v4-r50b16-s512-r1 | test | 0.025 (0.001–0.056) | 0.012 (0.000–0.029) | 0.734 (0.637–0.799) | 1/64 (0.016, 0.000–0.034) | 25/64 | 1,011/1,314 (0.769) |

Table 3. Paired differences in the cirrhosis measures (first run minus second), with 95% CIs
from the same cluster bootstrap over datasource groups. Same samples in both runs.

| Comparison | What it changes | Split | Δ DSC (95% CI) | Δ IoU (95% CI) | Δ Accuracy (95% CI) | Δ Positives found (95% CI) |
|---|---|---|---|---|---|---|
| s224 − r5 | model and pretraining, 224 px | val | −0.085 (−0.147 to −0.057) | −0.094 (−0.138 to −0.062) | −0.030 (−0.061 to −0.013) | −0.021 (−0.158 to +0.050) |
| s512 − s224 | input size, from scratch | val | −0.025 (−0.044 to +0.014) | −0.026 (−0.048 to +0.012) | −0.030 (−0.067 to −0.009) | −0.031 (−0.111 to +0.060) |
| s512 − r5 | all three | val | −0.111 (−0.144 to −0.081) | −0.120 (−0.146 to −0.076) | −0.060 (−0.126 to −0.023) | −0.052 (−0.128 to −0.018) |
| s224 − r5 | model and pretraining, 224 px | test | −0.021 (−0.143 to +0.000) | −0.011 (−0.077 to +0.000) | −0.131 (−0.181 to −0.093) | −0.016 (−0.150 to +0.000) |
| s512 − s224 | input size, from scratch | test | −0.001 (−0.032 to +0.049) | −0.001 (−0.016 to +0.025) | −0.025 (−0.138 to +0.062) | +0.000 (−0.036 to +0.034) |
| s512 − r5 | all three | test | −0.022 (−0.141 to +0.046) | −0.012 (−0.076 to +0.024) | −0.155 (−0.246 to −0.088) | −0.016 (−0.150 to +0.034) |

Table 4. Learning progress: val cirrhosis DSC at epochs 5, 10, 15, 20, 25 and 30, and train
cirrhosis DSC (train split evaluated without augmentation) at epochs 10, 20 and 30. One seed per run; no CIs.

| Run | Val DSC at epoch 5 / 10 / 15 / 20 / 25 / 30 | Best val DSC (epoch) | Train DSC at epoch 10 / 20 / 30 |
|---|---|---|---|
| cirr-v4-tu-e30-r5 | 0.629 / 0.650 / 0.682 / 0.662 / 0.660 / 0.646 | 0.696 (17) | 0.758 / 0.902 / 0.939 |
| cirr-v4-r50b16-s224-r1 | 0.537 / 0.526 / 0.592 / 0.608 / 0.595 / 0.560 | 0.611 (14) | 0.528 / 0.787 / 0.931 |
| cirr-v4-r50b16-s512-r1 | 0.000 / 0.490 / 0.563 / 0.522 / 0.546 / 0.586 | 0.586 (30) | 0.476 / 0.543 / 0.738 |

No figures in this record; the per-epoch values in Table 4 stand in for a learning-curve plot.

## Analysis

**Pretraining and model (s224 against r5, 224 px).** On val, the from-scratch official
model scored lower than the pretrained baseline: DSC −0.085 (95% CI −0.147 to −0.057) and
accuracy −0.030 (−0.061 to −0.013). Both CIs exclude 0. The positives found barely changed
(80 against 82 of 97); most of the accuracy loss is in negatives (141 against 80 of 1,971
negatives with a false cirrhosis prediction). This comparison changes two things at once,
the weights at start and the model code (DIS-023 Table 1), so it cannot say how much of the
gap is pretraining. Pretraining is the larger change of the two (unverified: no run here
has the official model with pretrained weights).

**Input size (s512 against s224, from scratch).** On val, 512 px did not do better than
224 px: DSC −0.025 (−0.044 to +0.014), CI includes 0; accuracy −0.030 (−0.067 to −0.009),
again from more false positives on negatives. This is not a fair test of input size yet:

- The 512 run was probably undertrained. Its selected epoch was the last one (30), its val
  DSC was still rising over the last five epochs (0.538 to 0.586), and its train DSC at epoch
  30 was 0.738 against 0.931 for the 224 run. Val DSC was 0.000 at epoch 5. With the same
  12,900 optimiser steps, the 512 model sees 5.2 times more pixels per sample and learns
  more slowly per step.
- The decoder BatchNorm saw micro-batches of 4 samples at 512 px against 8 at 224 px
  (the encoder uses GroupNorm, which does not depend on batch size). Accumulation kept the
  global batch at 24 for the optimiser, but BatchNorm statistics come from each micro-batch.
  This is a second difference besides input size.

So the gaps point to pretraining (with the model change) as the clear effect at 224 px,
and say nothing firm about input size: the 512 result is limited by training length and
possibly by the BatchNorm micro-batch.

**Val-to-test gap (observation only, not investigated).** On test, all three runs scored a
cirrhosis DSC between 0.025 and 0.047 and found 1 or 2 of 64 positives at DSC ≥ 0.5, against
0.586–0.696 and 77–82 of 97 on val. This gap is much larger than any difference between the
runs. The test positives come from 4 datasource groups, so the test CIs are wide and rest
on few clusters. The from-scratch runs predicted cirrhosis in more test samples
(any-pixel positives 16 and 25 of 64 against 10; negatives correct 0.795 and 0.769 against
0.932). The cause is not studied here; it may become a separate task.

**Failure cases, in aggregate.** On val, the from-scratch runs mostly failed on negatives
(false cirrhosis on 141 and 200 of 1,971 negatives, against 80 for the baseline), not on
positives. On test, nearly all positives were missed by every run.

## Limitations

- One seed per run. The CIs cover sampling over datasource groups, not seed variation,
  which was not measured.
- Val has 12 datasource groups with a positive and test has 4: the CIs are wide, and the
  test CIs rest on very few clusters, so percentile intervals may be too narrow there.
- s224 against r5 changes the model code and the pretraining together.
- s512 against s224 changes input size, the BatchNorm micro-batch, and the effective training
  progress (undertrained at 30 epochs).
- No patient ids in the sample file, so the bootstrap is over datasource groups, not patients.
- Exploratory: the comparisons were set before the runs (DEC-050), but no test or threshold
  was fixed in advance, and Table 3 holds 24 differences with no correction for multiple
  comparisons.

## Conclusion and next steps

- At 224 px, the from-scratch official R50-ViT-B/16 was worse on val than the pretrained
  timm-based TransUNet (DSC −0.085, 95% CI −0.147 to −0.057), mostly through false positives
  on negatives. Pretraining (with the model change) is the effect the gap points to.
- From scratch, 512 px did not beat 224 px within 30 epochs (DSC −0.025, CI −0.044 to
  +0.014). The 512 run was likely undertrained, so this is not evidence against 512 px.
- All three runs failed on test (DSC ≤ 0.047); the val-to-test gap dominates and is left for
  a separate task.

**Seeds.** More seeds are not recommended now:
- The s224 − r5 gap on val (−0.085, CI excludes 0) is large next to its CI. Whether it is
  also larger than seed spread is unknown, because seed spread was never measured on this
  task. Seeds would not separate pretraining from the model code, which is the open question.
- For the size question, more seeds of the same 30-epoch, from-scratch 512 run would only
  repeat an undertrained comparison.
- More useful next runs, each needing a decision (not started): (a) the official
  R50-ViT-B/16 with pretrained weights at 224 px and 512 px, which separates pretraining
  from the model code and tests size with a model that learns fast enough; or (b) a longer
  512 schedule. If a choice later rests on a gap under about 0.03 DSC, run 2 more seeds of
  each run being compared first.

## Reporting checklist

- [x] Data: datasources, inclusion and exclusion, counts per class per split (Data line;
      inclusion and exclusion in DEC-044 and DEC-047)
- [x] Split by datasource or patient; no overlap between splits; test set untouched until
      the final evaluation (split by datasource group, DEC-044). Test was evaluated every epoch
      by the trainer (DEC-045) but never used for selection or thresholds.
- [ ] Reference standard: what the labels mean, who labelled, how disagreements were
      resolved. N/A here; see DEC-043 and DEC-047.
- [x] Model and training: config, preprocessing, augmentation, seeds (Setup, Table 1)
- [x] Metrics with 95% CI (method named) next to the baseline (Tables 2 and 3)
- [x] Operating point: fixed task values (DSC ≥ 0.5 for positives, any pixel for
      negatives), not tuned; checkpoint selected on val only
- [ ] Subgroups (datasource, device) where n allows: not done (12 and 4 groups with a positive)
- [x] Limitations, and whether the result is exploratory or confirmatory (exploratory)
