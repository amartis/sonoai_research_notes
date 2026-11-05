---
id: DEC-043
title: Cirrhosis task lseg_cirrhosis_v4 - GT organ and cirrhosis layers, the model predicts cirrhosis only, VOID for unknown organ status, strict eligibility
status: accepted
area: [training, datasets]
created: 2026-11-05
from: [DIS-019]
related: [DEC-004, DEC-006, DEC-033, DEC-034, DEC-041, DEC-044, DEC-045]
superseded_by:
---
# DEC-043: Cirrhosis task `lseg_cirrhosis_v4`

## Context

[DIS-019](../discussions/DIS-019-cirrhosis-training-task.md). The user wants a cirrhosis
task whose ground truth (GT) has an organ layer and a cirrhosis layer while the model
predicts only the cirrhosis layer. The organ layer measures where predicted cirrhosis
falls (inside the liver or not). `lseg_cirrhosis_v3` ([DEC-006](DEC-006-losses-optim-tracking.md),
[DEC-034](DEC-034-organ-layer-from-organ-polygons-only.md)) predicts both layers and its organ
layer is the liver only, so this is a new task kind ([DEC-004](DEC-004-training-tasks.md), [DEC-041](DEC-041-label-groups-per-recipe.md)).

## Decision

1. **Name and kind.** `lseg_cirrhosis_v4`. GT has two layers; the model outputs one
   (`background`, `cirrhosis`). The organ layer is not in the loss; it is used only for
   measuring. The task spec says which GT layers are predicted (for example
   `predicted_layers=(1,)`), and the loss and model output size follow it.
   [DEC-033](DEC-033-precirrhosis-as-middle-grade-of-cirrhosis-task.md) (precirrhosis, proposed) takes the next free version after `_v4`.
2. **Organ layer classes** (default class map in code; a recipe may change it, DEC-041):
   `background`, `liver` (with `portal_vein`, `hepatic_vascular_branch`,
   `hepatic_blood_duct`, `hepatic_duct` merged into it, so structures inside the liver count
   as liver), `gallbladder`, `kidney`, `spleen`, `stomach`, `intestine`, `pancreas`
   (label `pancreatin`), `diaphragm`, `lung`, `heart`. Containers are drawn before what lies
   inside them.
3. **VOID in the organ layer** = pixels whose organ status is unknown:
   - pixels of an organ label that is not one of the classes (for example
     `common_biliary_duct`, `spine`);
   - pixels inside a liver disease or liver sign polygon (the liver evidence list of
     `disease.py`, minus the organ labels) but outside every liver polygon;
   - all remaining (not outlined) pixels, unless at least one of the sample's labeling
     projects offered every organ class of the class map as a polygon label
     (`configs/data/label_projects.yaml`); then they are `background`.
4. **Cirrhosis layer**: `hepatic_cirrhosis` polygons are `cirrhosis`, everything else
   `background`; no VOID.
5. **Eligibility (strict).** A sample (one crop, all its projects; [DEC-044](DEC-044-cirrhosis-sample-set-quality-filter-and-split.md)) takes part when:
   - it has at least one `liver` polygon;
   - at least one of its projects offered the `hepatic_cirrhosis` polygon;
   - none of these holds: a `hepatic_precirrhosis` polygon or choice; the choice
     `cannotdiag`; a `hepatic_cirrhosis` choice without a cirrhosis polygon; the absence
     choice `notfound` together with a cirrhosis polygon.
   Positive = has a cirrhosis polygon; negative = has none.
6. **Measures**, per evaluation and per split, all derived from stored matrices:
   - the **joint pixel matrix**: rows = GT (organ class incl. VOID, cirrhosis class),
     columns = predicted cirrhosis class. Its cirrhosis marginal is the DEC-006 pixel
     matrix of the cirrhosis layer;
   - cirrhosis pixel **DSC** and **IoU**; the DEC-006 image matrix;
   - **pred-in-liver**: predicted cirrhosis pixels inside GT liver / predicted cirrhosis
     pixels outside VOID. The same share for the GT cirrhosis polygons is reported beside
     it as the reference (some polygons extend past the liver outline, DEC-006);
   - **accuracy**: a positive sample is correct when its cirrhosis DSC >= 0.5; a negative
     is correct when it has fewer predicted cirrhosis pixels than `image_min_pixels`
     (DEC-006 default). Reported overall and for positives and negatives apart, with n and
     95% CI ([writing.md](../../docs/writing.md)). The threshold is a task setting; per-sample
     matrices ([DEC-045](DEC-045-per-sample-confusion-matrices-in-runs.md)) let it be recomputed for any run.
7. **Checkpoint selection** uses the validation split only: cirrhosis pixel DSC, then
   accuracy, then loss (DEC-006 tie-breaker rule). Test results are recorded but never
   used for a choice.

## Consequences

- The model is a plain two-class segmentation model; the organ layer costs nothing at
  training time beyond building the target.
- Needs the per-project offered-label lists at target-building time (a `prepare` context,
  as in DEC-006) and the choice table (`flags_df`) for eligibility.
- Liver share is defined on every sample because a liver polygon is required.
- Work: a `method` task for the task kind and measures; an `exp` task for the runs.
