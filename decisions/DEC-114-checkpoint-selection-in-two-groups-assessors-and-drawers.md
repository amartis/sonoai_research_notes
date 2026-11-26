---
id: DEC-114
title: Checkpoint selection from epic 3 on in two groups - assessors kept by image-level AUC, drawers kept by Dice; one pair named on validation, the assessor for the bar; the assessor's outline when the drawer draws none
status: accepted
area: [training]
created: 2026-11-26
from: [DIS-065]
related: [DEC-006, DEC-045, DEC-076, DEC-100, DEC-112, DEC-113]
superseded_by:
---
# DEC-114: Checkpoint selection in two groups, assessors and drawers

## Context

[DEC-113](DEC-113-checkpoint-selection-by-removing-beaten-checkpoints.md) (keep several checkpoints,
remove the beaten ones) kept checkpoints by one mixed set of criteria: image-level AUC and Dice on
positives together. The user's second thought (2026-11-26, in
[DIS-065](../discussions/DIS-065-epic3-metrics-and-keeping-several-checkpoints.md), epic 3 metrics and
keeping several checkpoints, section "Second thought"): two groups of survivors, one of checkpoints
that tell well whether a class is in the image (assessors), one of checkpoints that draw its outline
well (drawers); the product combines one of each. The bar of
[DEC-112](DEC-112-epic3-metrics-image-score-stone-scoring-cirrhosis-bar.md) (epic 3 metrics) rules 4
and 5 uses only the image-level score, so the assessor alone decides the bar. This DEC replaces
DEC-113 whole; rules 3, 4, 5, 7 and 9 of DEC-113 carry over within each group. Thresholds are the
analyst's numbers, not from literature.

## Decision

Accepted by the user on 2026-11-26 (the three recommendations in DIS-065, "Second thought").

1. **Scope.** Epic 3 and the following epics. Epic 1 keeps
   [DEC-076](DEC-076-epic1-metrics-label-set-score-selection-ci-and-pass-rule.md) rule 3 (Epic 1
   checkpoint selection).
2. **Two groups, kept apart**, each with its own criteria, set by the recipe; validation values only;
   the weights of each group sum to 1. For epic 3:
   - **Assessors**: image-level AUC per class (DEC-112 rule 1 score).
   - **Drawers**: Dice on positives per class (DEC-112 rules 2 and 3).

   Weights in each group: hepatoma 0.30; hemangioma, cyst and stone 0.20 each; ascites 0.10 (the
   DEC-113 class weights doubled). The DEC-113 mixed group is not kept.
3. **Value of A against B on one criterion** (DEC-113 rule 3): 0 when a is below the floor; else 1
   when a − b is at least the step; 0.5 when |a − b| is below the step; 0 when b − a is at least the
   step. Dice: floor 0.6, step 0.05. AUC: floor 0.70, step 0.02.
4. **A removes B within a group** when the sum of weight x value over that group's criteria reaches
   the removal threshold (0.666; above 0.5), unless B is better than A by at least the veto step on
   any criterion of that group (Dice 0.10, AUC 0.05).
5. **Thin criteria are left out** per group: a criterion with fewer than 15 validation positives is
   dropped for the run and the group's other weights are scaled to sum 1 (epic 3: ascites; hepatoma
   then 0.333, the other three 0.222 each).
6. **Near-copies, cap, fallback** per group: when A and B are within the step on every criterion of
   the group, the one with the lower weighted sum is removed. At most 3 survivors per group; above
   that, the lowest weighted sum is removed. If no checkpoint survives in a group, its highest
   weighted sum is kept. A checkpoint may survive in both groups.
7. **Online during training**: each group updates per epoch as DEC-113 rule 7 (a new checkpoint
   enters unless a survivor removes it, then removes the survivors it beats; a removed checkpoint
   does not come back). The weights of a checkpoint are deleted only when it is in neither group.
   Measures of every epoch stay in the run
   ([DEC-045](DEC-045-per-sample-confusion-matrices-in-runs.md) rule 3).
8. **One pair for the bar.** Before any test result is read, the assessor with the highest weighted
   sum in its group and the drawer with the highest weighted sum in its group are named the pair
   (one checkpoint when the same wins both). The bar verdict of DEC-112 rules 4 and 5 uses the
   assessor alone (this is how DEC-112 rule 11, "the primary checkpoint", reads from now on). The
   report also gives, as information: the drawer's Dice on positives, and the Dice of the combined
   output (rule 9). Other survivors are tested and reported as secondary results, never for the bar
   or a choice (DEC-045 rule 3).
9. **Combined output** (what the product shows), per class c: the assessor decides whether c is
   present, at a threshold fixed on validation (for the two bar items, DEC-112 rule 4; for each
   other class, by the same rule, the highest threshold with validation sensitivity at least 0.80,
   as information). When present, the outline is the drawer's pixels predicted as c; when the drawer
   predicts no pixel of c, the outline is the assessor's own pixels predicted as c, and the report
   counts how often this happens (n and share of the samples called present). When absent, nothing
   is drawn. The combined Dice on a positive of c called absent is 0.
10. **Steps, floors, veto, threshold and cap** may be changed once after the first run's validation
    values are seen, before any test result, by a note in the EXP record; later changes need a new DEC.

## Consequences

- DEC-113 is superseded by this DEC. A new selection mode beside the
  [DEC-006](DEC-006-losses-optim-tracking.md) tie-breakers (`Selection` in `sonoai.training.loop`),
  set in the recipe; DEC-006 stays the default.
- Serving runs two checkpoints when the pair differs: two forward passes per image.
- If the same checkpoint wins both groups in the first runs, the pair is one checkpoint and nothing
  else changes; the EXP record says so.
- Dice measures overlap, not a smooth edge; a boundary measure (e.g. the 95th-percentile Hausdorff
  distance) is not a criterion now (DIS-065, "Second thought", open questions).
- Reversal: survivors are chosen from stored per-epoch measures, so a changed rule can be re-run on
  past measures; deleted weights cannot be recovered.
- Code: [TASK-288](../../backlog/tasks/task-288%20-%20Checkpoint-selection-mode-that-keeps-several-checkpoints-and-removes-the-beaten-ones-weighted-criteria-floors-steps-removal-threshold-veto-near-copy-rule-cap-primary-by-weighted-sum-set-by-the-recipe-synthetic-tests-DEC-113.md)
  (selection mode, now in two groups, method) and
  [TASK-287](../../backlog/tasks/task-287%20-%20Epic-3-metrics-report-thresholds-fixed-on-validation-bar-and-cirrhosis-bar-verdicts-group-bootstrap-intervals-per-group-values-negatives-in-four-parts-contested-table-from-per-sample-records-synthetic-tests-DEC-112.md)
  (epic 3 metrics report: the pair, the combined output, the fallback count, method).
