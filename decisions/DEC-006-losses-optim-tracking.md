---
id: DEC-006
title: Losses, optimisation, confusion-based metrics and result tracking
status: accepted
created: 2026-10-23
from: []
related: [DEC-003, DEC-004]
superseded_by:
---
# DEC-006: Losses, optimisation, confusion-based metrics and result tracking

## Context

[DEC-003](DEC-003-trainrecipe-files-structure.md) fixes what a recipe, plan and run are; [DEC-004](DEC-004-training-tasks.md) fixes what a task is.
Neither says how a loss or optimiser is chosen and built, how training is
made machine-independent, how results are measured beyond plain DSC / IoU,
or where non-scalar results go.

The layered disease tasks (`lseg_*`, organ layer + disease layer) need more:

- Their **primary measure is the confusion matrix**, at pixel level and at
  image level. DSC, IoU and everything else are derived from it.
- Treating every pixel as a case, DSC and IoU are "satisfactory cases over
  cases of attention". For graded diseases a near miss is partly
  satisfactory: ground truth steatosis 1 predicted as steatosis 2 is better
  than predicted as steatosis 3. Plain DSC scores both as 0.
- Diagnosis is made on images of the organ: a liver disease is judged on
  samples that show the liver, a kidney disease on samples that show the
  kidney. Rare findings (renal stones < 1% of pixels) are handled by being a
  task of their own on organ samples, not by loss weighting.

Today only `sonoai.tracking.Run` (config, metrics.jsonl, meta), the smoke
trainer, machine profiles (`sonoai.training.plan.Machine`) and
`sonoai.evaluation.confusion` (pixel matrices, plain DSC / IoU) exist.

## Decision

### Code layout

```
src/sonoai/
├── training/
│   ├── recipe.py        TrainRecipe, Data, Model, Optim, Eval (frozen, to_dict())
│   ├── presets.py       shared recipe defaults, e.g. transunet_official()
│   ├── plan.py          Machine (exists), TrainPlan
│   ├── losses.py        register_loss, build_loss
│   ├── optim.py         build_optimizer, build_scheduler, accumulation
│   ├── loop.py          shared loop: accumulation, autocast, eval, selection, logging
│   └── <trainer>.py     segmentation, segmentation_layered, detection: thin wrappers on loop.py
├── evaluation/
│   ├── confusion.py     (exists) pixel matrices; + image-level matrices
│   ├── scores.py        satisfaction matrices, flexible DSC / IoU, all derived from a matrix
│   └── evaluate.py      evaluate(task, model, loader) -> results, dispatched on task.type
└── tracking/
    ├── run.py           Run, extended to the DEC-003 run layout
    └── display.py       terminal and TensorBoard views of what Run records
```

Components are **registered by name** and selected in the recipe by name plus
JSON-serialisable args, so `TrainRecipe.to_dict()` records them completely.
No objects or callables in config files.

### Confusion matrices are the primary record

Every evaluation produces, per layer of the task:

1. **Pixel matrix**: rows ground truth, columns prediction, over all
   non-ignored pixels of the split (`ConfusionMatrix`, exists).
2. **Image matrix** (disease layer of `lseg` tasks; the only layer of `seg`
   tasks): one case per sample.
   - Ground-truth class of a sample: the disease-layer class with the
     largest ground-truth region (most pixels); `background` if it has none
     (a negative).
   - Predicted class: the disease-layer class with the most predicted pixels
     in the whole crop; `background` if fewer than `image_min_pixels` (task
     setting, default 1). Ground truth and prediction use the same area (the
     whole crop): restricting the prediction to the organ outline made a
     perfect prediction score below 1, because some disease polygons extend
     past the organ outline (amended 2026-10-23, before any run).
   - Samples whose disease layer is entirely ignored are not counted.

Both matrices are **saved at every evaluation**, as integers, in the run
(below). DSC, IoU, flexible DSC / IoU and any later measure are pure
functions of a matrix, so new measures can be computed on old runs without
re-running inference. Stored as JSON (readable, diffable, safe to load); a
pickle would execute code on load and is not used for results.

### Flexible DSC and IoU

Each task defines, per layer, a **satisfaction matrix** `S` over its
attention classes `A` (the layer's classes except `background`):
`S[g, p]` in `[0, 1]` is how satisfactory predicting `p` is when the truth is
`g`. With `C` the confusion matrix (pixel or image), `T` the weighted
satisfactory count, and row / column sums taken over all classes including
background:

```
T     = sum over g in A, p in A of  S[g, p] * C[g, p]
FDSC  = 2 T / ( sum_{g in A} C[g, :].sum()  +  sum_{p in A} C[:, p].sum() )
FIoU  =   T / ( sum_{g in A} C[g, :].sum()  +  sum_{p in A} C[:, p].sum()  -  T )
```

- With `S` the identity and one attention class this is exactly ordinary
  DSC / IoU, so single-disease tasks use the ordinary measure.
- With `S` the identity and several classes it is the pooled (micro) DSC;
  per-class ordinary DSC / IoU are still reported beside it.
- Example: 100 ground-truth steatosis-1 pixels all predicted as steatosis 2
  give `T = 50`, FDSC = 2·50 / (100 + 100) = **0.5** (ordinary DSC: 0).
- The same formula on the image matrix gives the image-level FDSC (cases are
  images instead of pixels).

`S` is part of the task (DEC-004: metrics belong to the task); changing it is
a new task version. Built with helpers in `scores.py`:

| Task | Disease layer `S` |
|---|---|
| `lseg_steatosis_v2` | ordinal over grades 0-3: \|g-p\| = 0 -> 1.0, = 1 -> 0.5, >= 2 -> 0 |
| `lseg_cirrhosis_v2` | single class (cirrhosis): ordinary DSC / IoU |
| `lseg_hepatoma_v2` | single class: ordinary DSC / IoU |
| every organ layer | single class: ordinary DSC / IoU |

The image-level matrix of a segmentation task is a classification readout
of the segmentation output (largest graded region -> image class). It is a
derived measure, not a separate model: a dedicated classification task
(e.g. `cls_steatosis_v1` trained on image-level labels) can later be
compared on the same image matrix and image FDSC.

```python
disease_task("steatosis", "liver", {...}, satisfaction=ordinal({0: 1.0, 1: 0.5}))
```

### Samples: diagnose on images of the organ

The disease tasks get a v2 eligibility rule:

- A sample takes part only if it **shows the task's organ**: it has at least
  one polygon whose label belongs to that organ, i.e. the organ itself, one
  of its diseases or one of its signs (a stone or a nephritis outline implies
  a kidney). The label-to-organ table is frozen in the task code, copied from
  `configs/data/label_taxonomy.yaml`.
- Negatives (organ present, disease absent) come **only from the projects in
  which the task's disease is annotated**, so a negative was looked at for
  that disease. This needs dataset-level context: a task may define
  `prepare(label_tables) -> context` (computed in memory once per dataset)
  and its eligibility takes `(spec, rows, context)`.
- Every single disease stays an independent task; no class weighting in the
  loss.
- **Graded diseases (steatosis)**: only organ area carrying a grade is a
  target. In the disease layer, liver pixels not covered by a
  `hepatic_steatosis__{0..3}` polygon, or covered by
  `hepatic_steatosis__ignore`, are `ignore_index`; pixels outside the liver
  stay background. Only crops with a grade take part, so the negatives are
  grade 0, never unlabelled livers (ungraded does not mean normal). In 261023
  this ignores ~2% of liver pixels and leaves out 2,474 ungraded liver crops
  (amended 2026-10-23, before any run).
- `lseg_cirrhosis_v2` drops precirrhosis for now: samples with a
  precirrhosis polygon are not eligible (205 in 261023), so they are neither
  positives nor negatives.

Tasks of the next run, counts on 261023 (crops with polygons):

| Task | Positives | Negatives, same projects | (all projects) | Organ layer annotated |
|---|---:|---:|---:|---:|
| `lseg_steatosis_v2` | 14,071 graded crops | none: grade 0 (6,401 crops) is the negative | - | 100% |
| `lseg_cirrhosis_v2` | 1,815 (cirrhosis only) | 14,708 | 27,145 | 100% |
| `lseg_hepatoma_v2` | 1,679 | 15,049 | 27,486 | 97% |

Positives of `lseg_cirrhosis_v2` are approximate (2,020 crops with either
label minus the precirrhosis ones); exact counts go in the task notes.

**Parked** (not in the next run, to be discussed): `renal_calculus` and
`hydronephrosis`. Kidney outlines are almost absent in their crops (3 of
1,963 stone crops), so the organ layer would barely train, and same-project
negatives are few (468 and 524). The flags may solve this: every
renal-calculus crop has a flag containing "renal", i.e. kidney organ
evidence exists at image level (see open questions).

The `_v1` disease tasks were never run; they are replaced by `_v2` and
removed (DEC-004 keeps old versions only while runs cite them). The parked
kidney tasks get no `_v2` until they are discussed.

### Losses

- `loss` (name) and `loss_args` are recipe fields; `loss` defaults to the
  task type's loss.
- `build_loss(name, task, **args)`: built **from the task, never from the
  data**; the task supplies `n_classes`, `ignore_index`, `layer_sizes`.
- `dice_ce`: `ce_weight * CE + dice_weight * Dice`, default 0.5 / 0.5 as in
  the official TransUNet code. Layered tasks: `dice_ce_per_layer`, a
  weighted sum over layers (`layer_weights`, default all 1).
- A loss term with no valid pixels (a fully ignored layer) is skipped, never
  NaN. Tested on synthetic targets.

### Optimisation: follow the official TransUNet training

The default preset `transunet_official()` follows the official TransUNet
trainer, with your initial learning rate:

| Setting | Value |
|---|---|
| optimiser | SGD, momentum 0.9, weight decay 1e-4 on all parameters |
| initial LR | **1e-3** (official default is 1e-2) |
| schedule | poly, per iteration: `lr = lr0 * (1 - it / max_it) ** 0.9`, no warmup |
| loss | 0.5 CE + 0.5 Dice |
| EMA | none (the official code uses none); no EMA field until a recipe needs it |
| precision | fp32 (official); `bf16` is a recipe variant |

- `Optim` fields are recipe fields; the plan / machine sets only
  `micro_batch` and `devices`.
- Accumulation: `accum = global_batch / (micro_batch * devices)`, must be a
  positive integer; each micro-batch loss is divided by `accum`. Schedules
  count optimiser steps, so they are the same on every machine.

### Checkpoint selection with tie-breakers

```python
Eval(every_epochs=1,
     select=("val/layer1/pixel_fdsc:max", "val/layer1/image_fdsc:max", "val/loss:min"),
     select_tol=1e-4)
```

A new evaluation becomes `best` if its first value beats the best by more
than `select_tol`; within the tolerance the next value decides, and so on.

### Result tracking

```
$SONOAI_RUNS_ROOT/<recipe name>/<plan name>/<run id>/
├── recipe.json  plan.json  task.json  meta.json      (DEC-003)
├── metrics.jsonl        scalars: per batch (loss, lr) and per evaluation (all derived measures)
├── eval/
│   ├── val_e012.json    per layer: pixel and image confusion matrices (counts), S, derived measures
│   └── best.json        copy of the evaluation that selected best.pt
├── tb/                  TensorBoard event files (a view of the above)
├── train.log
└── checkpoints/         last.pt, best.pt
```

- `metrics.jsonl` and `eval/` are the source of truth; `tb/` and the terminal
  are views. Only aggregates are recorded (counts, matrices, measures): never
  images, per-sample predictions or sample identifiers.
- `gpu fetch` (without `--all`) and the RunPod rsync bring back everything
  except `checkpoints/`.
- **Runs index**: a finished run appends one line to
  `$SONOAI_RUNS_ROOT/index.jsonl` (run ref, task + fingerprint, dataset
  version, split, machine, status, selection values of `best`, commit, dirty).
  `scripts/compare_runs.py` groups by task + fingerprint + dataset + split
  (DEC-004) and shows `best.json` matrices side by side. The index is a cache,
  rebuildable from the run directories.

### Live display

- **Terminal, every batch**: one updating progress line per epoch (tqdm) with
  batch loss, running mean loss, LR, it/s.
- **Terminal, every epoch**: a short table: train / val loss, per-layer pixel
  FDSC / FIoU, image FDSC, per-class ordinary DSC, then the disease layer's
  pixel matrix (row-normalised %) and image matrix (counts); a marker when
  `best` changes.
- **TensorBoard**: scalars per batch and per evaluation, and the confusion
  matrices as figures per evaluation (matplotlib). Event files are written
  into the run, so they work offline: view live on the GPU box through an SSH
  tunnel, or after `gpu fetch` on the workstation
  (`tensorboard --logdir $SONOAI_RUNS_ROOT`). Needs the `tensorboard`
  package on each machine (offline install on the GPU box).
- Not chosen: wandb (online service, the box is offline), MLflow (a server
  and store for what JSON + TensorBoard already cover).

## Consequences

- One recipe fully determines loss, optimiser and schedule; plans change only
  speed. Runs on the 3060 and the A100 are comparable up to hardware noise.
- Confusion matrices are kept for every evaluation, so flexible DSC, plain
  DSC / IoU and future measures (sensitivity per grade, kappa, ...) can be
  recomputed for any past run.
- Graded tasks are scored by how far a prediction is from the truth, not only
  whether it is exact, and the weighting is versioned with the task.
- Disease tasks train and evaluate only on images of their organ, with
  negatives from the same projects: fewer samples but trustworthy negatives.
  The next run covers the three liver tasks only; kidney tasks wait.
- Needs: `TaskSpec` fields `satisfaction` and `image_min_pixels`, optional
  `prepare` / context for eligibility, the `_v2` disease tasks (v1 removed),
  `scores.py` and image-level matrices with synthetic tests, `recipe.py`,
  `presets.py`, `losses.py`, `optim.py`, `Run` changes (run path, copies,
  `save_eval`, index line), `display.py`, `evaluate.py`, `loop.py`, the
  `segmentation_layered` trainer, the `scripts/train.py` rewrite, and torch +
  tensorboard on the workstation (offline install).

## Open questions

- **Precirrhosis** (deferred): bring it back into the cirrhosis task, and if
  so, is precirrhosis -> cirrhosis an adjacent (0.5) miss?
- **Kidney tasks** (deferred): organ evidence and negatives for
  `renal_calculus` / `hydronephrosis` before they get a `_v2`.
- **Flags as image-level labels**: every renal-calculus crop has flags
  containing "renal" and "calcul", every gallbladder-stone crop flags
  containing "gallbladder" and "stone". `flags_df` looks like image-level
  organ / diagnosis labels (181 values). If so they could (a) give organ
  evidence where no organ polygon exists and (b) be the ground truth of a
  classification task to compare with the image-level readout. Their names
  and meaning have not been reviewed.
- Negatives from all projects (5-30x more, but possibly never looked at for
  that disease) as a later variant, once a same-project baseline exists?
