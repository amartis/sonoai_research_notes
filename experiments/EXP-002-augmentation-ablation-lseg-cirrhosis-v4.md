---
id: EXP-002
title: Augmentation ablation - different augmentation styles on lseg_cirrhosis_v4 (draft)
status: planned
created: 2026-11-10
from: [DEC-049]
related: [DIS-022, DEC-043, DEC-045, DEC-006]
---
# EXP-002: Augmentation ablation - different augmentation styles on lseg_cirrhosis_v4

**Draft.** Rows and columns are set up; every result cell is empty until its run is
fetched. Board tasks: [TASK-088](../../backlog/tasks/task-088%20-%20Train-lseg_cirrhosis_v4-on-the-fixed-sample-file-and-write-the-EXP-record-DEC-043-DEC-045.md) (baseline run, no augmentation) and [TASK-109](../../backlog/tasks/task-109%20-%20Train-lseg_cirrhosis_v4-with-augment-us_mild_v1-same-recipe-and-seed-as-cirr-v4-tu-e30-r5-and-compare-in-an-EXP-record-DEC-049.md) (run with
`us_mild_v1`), which fill this record.

- Date: started 2026-11-10
- Code commit: per run, in Table 1
- Config: `configs/train/recipes/lseg_cirrhosis_v4/261109_transunet_dec047.py` (baseline);
  one recipe per further row, identical except `Data.augment`
- Runs: Table 1
- Data: dataset version 261023, fixed sample file of [DEC-047](../decisions/DEC-047-cirrhosis-v4-cases-per-project-group-and-liver-fallback.md) (sha256 `59e174bf...c55a`);
  train 10,331 / val 2,068 / test 1,378 samples; test held out by datasource
  ([DEC-044](../decisions/DEC-044-cirrhosis-sample-set-quality-filter-and-split.md))

Writing standard: [docs/writing.md](../../docs/writing.md) ([DEC-021](../decisions/DEC-021-communication-and-research-writing-standards.md)).

## Question / hypothesis

Exploratory. Does training-time augmentation change cirrhosis segmentation quality on
lseg_cirrhosis_v4 ([DEC-043](../decisions/DEC-043-cirrhosis-task-gt-organ-layer-predicted-cirrhosis-only.md)), and which augmentation styles help or hurt?
Hypothesis ([DIS-022](../discussions/DIS-022-data-augmentation-for-ultrasound-segmentation.md)): mild geometry and gain changes help, because positives are
rare (477 of 10,331 train samples, 4.6%) and devices differ; styles that alter
echotexture may hurt.

## Setup

Each row is one run. All runs share the baseline recipe: TransUNet pretrained, input
224 × 224, global batch 24, 30 epochs, SGD as in [DEC-006](../decisions/DEC-006-losses-optim-tracking.md), seed 0. Only `Data.augment`
differs. Checkpoint selection on val only ([DEC-006](../decisions/DEC-006-losses-optim-tracking.md), joint-task rule in
`sonoai.training.segmentation`). The train split is evaluated without augmentation
([DEC-045](../decisions/DEC-045-per-sample-confusion-matrices-in-runs.md) rule 3).

Augmentation styles (columns of Table 1), parameters as in [DEC-049](../decisions/DEC-049-mild-ultrasound-augmentation-us-mild-v1.md) item 2:

| Style | What it changes | Status under DEC-049 |
|---|---|---|
| Horizontal flip | mirrors left-right, p=0.5 | in `us_mild_v1` |
| Rotation, scale, shift | rotation ±10°, scale 0.9–1.1, shift ±5%, p=0.5 | in `us_mild_v1` |
| Crop-box jitter | each B-mode box edge ±3% before the crop, p=0.5 | in `us_mild_v1` |
| Brightness, contrast, gamma | ±0.1, 0.85–1.15, 0.8–1.25, each p=0.5 | in `us_mild_v1` |
| Depth gain curve | row-wise gain 0.8–1.2 through 3 points, p=0.3 | in `us_mild_v1` |
| Blur, sharpen, speckle noise, JPEG | texture and compression | not built; only after `us_mild_v1` is measured |
| Vertical flip, 90° rotation | flips the depth axis | excluded |
| Elastic warp | local deformation | excluded |
| Cutout, MixUp, CutMix | hides or mixes image regions | excluded |

Table 2. Augmentation styles compared in this record, with their settings and their status
under DEC-049. p is the probability that a style is applied to a training sample.

## Results

Table 1. Runs of the augmentation ablation on lseg_cirrhosis_v4: augmentation styles used
(✓ used, – not used) and cirrhosis-layer measures of the checkpoint selected on val.
Val n = 2,068 samples (97 positive); test n = 1,378 (64 positive). Empty cells are pending.

| Run | Board task | Augment name | Horizontal flip | Rotation, scale, shift | Crop-box jitter | Brightness, contrast, gamma | Depth gain curve | Blur, sharpen, speckle, JPEG | Vertical flip, 90° rotation | Elastic warp | Cutout, MixUp, CutMix | Selected epoch | Val cirrhosis DSC (95% CI) | Val cirrhosis IoU (95% CI) | Val positives detected, n/97 | Val negatives correct, n/1,971 | Test cirrhosis DSC (95% CI) | Test cirrhosis IoU (95% CI) | Test positives detected, n/64 | Difference in val DSC vs baseline (95% CI) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cirr-v4-tu-e30-r5 (baseline) | TASK-088 | none | – | – | – | – | – | – | – | – | – | | | | | | | | | 0 (reference) |
| (pending) | TASK-109 | `us_mild_v1` | ✓ | ✓ | ✓ | ✓ | ✓ | – | – | – | – | | | | | | | | | |

DSC: Dice similarity coefficient. IoU: intersection over union. CI: confidence interval,
by bootstrap over datasources (method to be confirmed when filled). "Positives detected"
and "negatives correct" use the joint matrix of DEC-043 at the task's operating point.
Rows for further styles (for example geometry only, or texture added) are added only when
a run is planned for them; no such run is planned now (DEC-049).

### Figures (planned)

Figure 1 (planned). Difference in cirrhosis DSC between each augmented run and the
baseline, on val and on test, as points with 95% CI bars (paired bootstrap over
datasources, same samples in both runs); one seed per run; a vertical line at 0 marks no
change. Makes the effect of each augmentation set visible at a glance.

Figure 2 (planned). Val cirrhosis DSC per epoch for every run in Table 1, one line per run,
epochs 1–30, the selected epoch marked; train (evaluated without augmentation) as a dashed
line of the same colour. Shows whether augmentation slows learning or reduces the gap
between train and val (overfitting).

Figure 3 (planned). Augmentation styles per run as a grid (rows: runs, columns: the styles
of Table 2), each cell coloured by use, beside each row's val DSC difference from
Figure 1. Links each set of styles to its effect.

Figures as SVG beside this record, colour-blind-safe palette (docs/writing.md); metrics
only, no images.

## Analysis

Pending.

## Limitations

- One seed per run: a small difference may be seed noise. With about 97 val positives the
  CIs will be wide; more seeds only if the gap is small (DEC-049 item 6).
- `us_mild_v1` changes five styles at once, so the effect of each one is not separated.
- Augmentation parameters are starting values, not tuned.

## Conclusion and next steps

Pending.

## Reporting checklist

- [ ] Data: datasources, inclusion and exclusion, counts per class per split
- [ ] Split by datasource or patient; no overlap between splits; test set
      untouched until the final evaluation
- [ ] Reference standard: what the labels mean, who labelled, how
      disagreements were resolved
- [ ] Model and training: config, preprocessing, augmentation, seeds
- [ ] Metrics with 95% CI (method named) next to the baseline
- [ ] Operating point: how the threshold was chosen, on which split
- [ ] Subgroups (datasource, device) where n allows
- [ ] Limitations, and whether the result is exploratory or confirmatory
