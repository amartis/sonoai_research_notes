---
id: DEC-109
title: Epic 3 data preparation - input 512 x 512, no minimum crop side, two resize modes (stretch and fit-scale with padding) compared by training
status: accepted
area: [training, datasets]
created: 2026-11-26
from: [DIS-064]
related: [DEC-068, DEC-069, DEC-100, DEC-108]
superseded_by:
---
# DEC-109: Epic 3 input size, minimum crop side and resize modes

## Context

[DIS-064](../discussions/DIS-064-epic3-data-preparation-task-form-more-data.md) (epic 3 data
preparation, task form and more data) Tables 1 and 2: at 224 x 224, the Epic 1 input
([DEC-069](DEC-069-epic1-data-preparation.md),
Epic 1 data preparation), a median stone is 8.5 px wide; at 512 it is 19 px, near its 23 px in the
source. A 224 px minimum crop side would drop 148 of 16,176 samples. Which samples enter is already
fixed by [DEC-108](DEC-108-epic3-split-test-and-validation-by-whole-groups.md) (epic 3 split) rule 1;
quality-skipped samples have no known state there.

## Decision

Accepted by the user on 2026-11-26.


1. **Input 512 x 512** for every epic 3 recipe. A later recipe that departs from it needs a DEC.
2. **No minimum crop side.** Every sample of the epic 3 sample file (DEC-108 rule 5) enters
   training, validation and test; a crop smaller than the input is enlarged.
3. **Two resize modes, compared by training** on the same recipe:
   - **stretch**: the crop is resized to 512 x 512, aspect not kept (as in Epic 1);
   - **fit-scale**: aspect kept; the crop is scaled so that its longer side is 512 and centred; the
     rest of the input is padding, with image 0 and the target fill {background}, as outside the
     crop in [DEC-068](DEC-068-us-mild-v2-zero-image-and-background-outside-the-crop.md) (us_mild_v2).
     Augmentations treat the padding as outside the crop box.
4. **The choice** between the two modes is made on validation, with the group-bootstrap intervals
   of DEC-108 rule 6; the run plan is set at the organisation point of [DEC-100](DEC-100-epic3-mission-spot-liver-diseases.md) rule 7.
5. Validation and test of a run use the run's resize mode; the brightness and other shift tests do too.

## Consequences

- Per sample, 512 x 512 is 5.2 times the pixels of 224 x 224 (arithmetic, not a timing).
- In fit-scale, a crop of aspect 1.33 gets about 384 px on its shorter axis instead of 512.
- Code: [TASK-282](../../backlog/tasks/task-282%20-%20Fit-scale-resize-mode-in-the-sample-reader-aspect-kept-longer-side-fills-the-input-centred-padding-with-image-0-and-the-target-fill-stretch-stays-the-default-synthetic-tests-DEC-109.md) (method) adds the fit-scale mode to the sample reader (a recipe field whose default,
  stretch, leaves every existing recipe and its `recipe.json` unchanged).
- Reversal: before training, a recipe value; after training, new runs.
