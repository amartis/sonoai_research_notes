---
id: DEC-091
title: Mission of the third research epic - outlining and flagging spot liver diseases on 261023 (hepatoma, hemangioma, cyst, stone; ascites as a side class)
status: accepted
area: [training, datasets]
created: 2026-11-25
from: [DIS-050]
related: [DEC-045, DEC-059, DEC-065, DEC-075, DEC-076, DEC-092]
superseded_by:
---
# DEC-091: Mission of Epic 3 - spot liver diseases

## Context

Counts and the reasons are in [DIS-050](../discussions/DIS-050-epic3-spot-liver-disease-mission.md).
Labels record no pathology or CT/MRI confirmation, so a model can only be shown to agree with
readers of B-mode images. The cirrhosis model fell from 0.696 DSC on val to 0.047 on test
([EXP-003](../experiments/EXP-003-transunet-r50-b16-from-scratch-512-and-224-lseg-cirrhosis-v4.md)).

## Decision

1. **Mission.** A 2D B-mode model on dataset version 261023 that outlines spot liver diseases and
   gives an image-level score for each, for use as a reader's aid with an adjustable sensitivity.
   Claim: agrees with readers on datasource groups not seen in training. Not "diagnoses cancer".
2. **Classes.** `hepatoma`, `hemangioma`, `hepatic_cyst`, `hepatic_stone` are the four spot
   classes. `ascites` is trained with low importance and left out of class balancing. Out: abscess
   and the generic `tumor`, `cyst`, `parasite`.
3. **Labels.** Sample-label index v2 of [DEC-092](DEC-092-group-skip-and-sample-label-index-v2.md),
   read by the existing presence policies. Policies are compared by training, in this order (the
   user's, 2026-11-25): strict_v1 (top priority), loose_v1 (second), posrich_v1 (low priority, its
   extra positives are contested labels). Epic 3 focuses on the first two. Only the train labels
   differ between them. One split, made once, and one truth for val and test, strict_v1 on index v2,
   for every policy; a pair unknown there is not scored. An unknown pair is never background. A
   positive without a polygon has an image-level target only.
4. **Provisional bar**, image level, on test groups, at a threshold fixed on val: sensitivity
   at least 0.80, specificity at least 0.90, val minus test at most 0.10, for (a) any of the four
   spot classes and (b) hepatoma. A sample is negative for (a) when all four are negative.
   Numbers are the analyst's, not from literature; the metrics session may change them before the
   first test result. Hemangioma, cyst, stone and ascites are reported without a bar. Specificity
   on hepatoma negatives with positive cirrhosis is always reported.
5. **What is tracked.** Per class: DSC on positives and no-prediction score on negatives (as
   W1, W2 in Epic 1), a GT-class by predicted-class confusion matrix, sensitivity and
   specificity over thresholds, and AUC with CI per class and for any spot class. The
   per-sample record must hold a continuous image-level score per class and the joint pixel counts
   from the first run: Epic 1 records cannot be completed afterwards
   ([DIS-048](../discussions/DIS-048-epic1-confusion-matrix-for-label-set-targets.md)). Test only at
   the selected epoch ([DEC-045](DEC-045-per-sample-confusion-matrices-in-runs.md) rule 3). Details at the metrics stage.
6. **Balancing** is needed (positives are 0.6% to 9% of the known samples, by class); the method is
   chosen at the optimisation stage.
7. **Order of later points:** negatives and conflicts, split, more data, task form, metrics,
   model and optimisation, organisation. Milestone m-1 fits; no new milestone.

## Consequences

- Epic 3 does not depend on the Epic 1 verdict.
- The policy order may change after the first results, not the val and test truth.
- Any point DEC that departs from rules 2 to 4 needs its own DEC.
