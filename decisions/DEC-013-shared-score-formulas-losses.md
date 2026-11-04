---
id: DEC-013
title: Losses reuse the matrix score formulas (soft confusion matrix, fdsc_ce)
status: accepted
area: [training]
created: 2026-10-28
from: [DIS-003]
related: [DEC-004, DEC-006]
superseded_by:
---
# DEC-013: Losses reuse the matrix score formulas (soft confusion matrix, fdsc_ce)

## Context

[DEC-006](DEC-006-losses-optim-tracking.md) makes every score (DSC, IoU, flexible DSC / IoU with the task's
satisfaction matrix `S`) a pure function of a confusion matrix, and defines
the losses separately (`dice_ce`, following the official TransUNet code).
A Dice-type loss is the same kind of measure as the metric, so writing the
formula twice lets the two drift, and `S` would exist in a metric form only.
Discussed with the user in [DIS-003](../discussions/DIS-003-project-setup-structure.md) (2026-10-28).

## Decision

Amends the Losses section of DEC-006; the rest of DEC-006 stands.

- **One formula, any matrix.** The matrix formulas in
  `src/sonoai/evaluation/scores.py` (per-class DSC / IoU, flexible DSC / IoU
  with `S`) are written with plain array operations so they accept a NumPy
  integer matrix (metrics, saved runs) and a torch float matrix (losses,
  differentiable). An optional `eps` smooths numerator and denominator; it is
  0 for metrics.
- **Soft confusion matrix.** `training/losses.py` builds
  `C_soft[g, p] = sum over non-ignored pixels of onehot(gt)[g] * softmax(logits)[p]`
  per batch (per layer for layered tasks) and passes it to the shared
  formulas. Losses import from `evaluation`; `evaluation` does not import
  from `training`.
- **New loss `fdsc_ce`**: `ce_weight * CE + fdsc_weight * (1 - soft FDSC)`,
  with the task's `S` ([DEC-004](DEC-004-training-tasks.md): `S` belongs to the task). With `S` the
  identity it is a linear soft Dice + CE. Selected per recipe by name.
- **`dice_ce` stays as DEC-006 has it**, matching the official TransUNet
  loss (including its squared denominator), so the baseline is a faithful
  reproduction. It remains the default loss of segmentation tasks.
- Cross-entropy is not a function of the confusion matrix and stays its own
  term.
- In a loss, a class absent from the batch (zero row and column sums) is left
  out of the formula, never NaN (as DEC-006 requires); the metric reports
  `None` for it, as now.

## Consequences

- The satisfaction matrix of a task scores the model in training and in
  evaluation the same way; graded tasks (steatosis) can train on the ordinal
  credit they are measured with.
- `dice_ce` and `fdsc_ce` with `S` the identity can be compared directly
  (squared vs linear soft Dice).
- A loss is still per batch while metrics pool over a split; the formula is
  shared, the aggregation is not.
- Synthetic tests check that the shared formulas give the same value on a
  NumPy and a torch matrix, that hard one-hot "probabilities" reproduce the
  metric exactly, and that the loss has gradients and no NaN with absent
  classes.
