---
id: DEC-113
title: Checkpoint selection from epic 3 on - keep several checkpoints and remove the beaten ones by weighted criteria, a removal threshold and a veto; one primary checkpoint named on validation for the bar
status: accepted
area: [training]
created: 2026-11-26
from: [DIS-065]
related: [DEC-006, DEC-045, DEC-076, DEC-100, DEC-112]
superseded_by:
---
# DEC-113: Keep several checkpoints, remove the beaten ones

## Context

The user's proposal (2026-11-26) and its review are in
[DIS-065](../discussions/DIS-065-epic3-metrics-and-keeping-several-checkpoints.md) (epic 3 metrics
and keeping several checkpoints), Tables 1 and 2. Until now one checkpoint is chosen by ordered
tie-breakers ([DEC-006](DEC-006-losses-optim-tracking.md), `Selection` in `sonoai.training.loop`;
Epic 1: [DEC-076](DEC-076-epic1-metrics-label-set-score-selection-ci-and-pass-rule.md) rule 3). The
aim: every checkpoint that is good at something survives. Thresholds are the analyst's numbers.

## Decision

Accepted by the user on 2026-11-26, with the five changes of DIS-065 Table 2.

1. **Scope.** Epic 3 and the following epics. Epic 1 keeps DEC-076 rule 3.
2. **Selection criteria and weights**, set by the recipe; validation values only; the weights sum
   to 1. For epic 3 ([DEC-112](DEC-112-epic3-metrics-image-score-stone-scoring-cirrhosis-bar.md),
   epic 3 metrics): image-level AUC and Dice on positives, each with hepatoma 0.15, hemangioma,
   cyst and stone 0.10 each, ascites 0.05.
3. **Value of A against B on one criterion** (higher is better; a = A's value, b = B's):
   0 when a is below the floor; else 1 when a − b is at least the step; 0.5 when |a − b| is below the
   step; 0 when b − a is at least the step. Dice: floor 0.6, step 0.05. AUC: floor 0.70, step 0.02.
4. **A removes B** when the sum of weight x value reaches the removal threshold (0.666; it must be
   above 0.5, so two checkpoints never remove each other), unless B is better than A by at least the
   veto step on any criterion (Dice 0.10, AUC 0.05).
5. **Thin criteria are left out**: a criterion with fewer than 15 validation positives is dropped for
   the run and the other weights are scaled to sum 1 (epic 3: ascites).
6. **Near-copies**: when A and B are within the step on every criterion, the one with the lower
   weighted sum (sum of weight x criterion value) is removed. At most 5 survivors; above that, the
   lowest weighted sum is removed. If no checkpoint survives, the highest weighted sum is kept.
7. **Online during training**: a new checkpoint enters unless a survivor removes it, then removes the
   survivors it beats. A removed checkpoint does not come back. Measures of every epoch stay in the
   run ([DEC-045](DEC-045-per-sample-confusion-matrices-in-runs.md) rule 3); only the weights of
   removed checkpoints are deleted.
8. **One primary for the bar.** Before any test result is read, the survivor with the highest
   weighted sum is named the primary; the bar verdict uses it. The other survivors are tested and
   reported as secondary results, never for the bar or a choice (DEC-045 rule 3: test is never used
   for a choice).
9. **Steps, floors, veto and threshold** may be changed once after the first run's validation values
   are seen, before any test result, by a note in the EXP record; later changes need a new DEC.

## Consequences

- A new selection mode beside the DEC-006 tie-breakers, set in the recipe; DEC-006 stays the default.
- The order of epochs can change the survivors (rule 7).
- Reversal: survivors are chosen from stored per-epoch measures, so a changed rule can be re-run on
  past measures; deleted weights cannot be recovered.
