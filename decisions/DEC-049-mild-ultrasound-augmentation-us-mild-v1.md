---
id: DEC-049
title: Mild ultrasound augmentation us_mild_v1 (torchvision v2), an unaugmented train reader for evaluation, and one comparison run against the no-augmentation baseline
status: accepted
area: [training]
created: 2026-11-10
from: [DIS-022]
related: [DEC-006, DEC-017, DEC-043, DEC-045]
superseded_by:
---
# DEC-049: Mild ultrasound augmentation us_mild_v1

## Context

[DIS-022](../discussions/DIS-022-data-augmentation-for-ultrasound-segmentation.md). No augmentation exists; `Data.augment` is a name that the reader
refuses. [DEC-045](DEC-045-per-sample-confusion-matrices-in-runs.md) rule 3 requires the train split to be evaluated without
augmentation. Baseline: [TASK-088](../../backlog/tasks/task-088%20-%20Train-lseg_cirrhosis_v4-on-the-fixed-sample-file-and-write-the-EXP-record-DEC-043-DEC-045.md) run cirr-v4-tu-e30-r5 (no augmentation).

## Decision

1. `Data.augment` names a registered augmentation; the first is `us_mild_v1`, applied to
   the train split during training only. Val, test and the train evaluation read without
   augmentation (an unaugmented train reader, DEC-045 rule 3).
2. `us_mild_v1`, starting values (chosen, not tuned):
   - crop-box jitter: each box edge moves by up to ±3% of the box side, p=0.5, clamped to
     the image, before the crop;
   - horizontal flip, p=0.5;
   - affine, p=0.5: rotation ±10°, scale 0.9–1.1, shift up to ±5% per axis;
   - brightness ±0.1 (additive), contrast 0.85–1.15, gamma 0.8–1.25, each p=0.5, the same
     on all 3 channels, result clipped to [0, 1];
   - depth gain curve, p=0.3: the image is multiplied row by row by a smooth curve through
     3 random gains in 0.8–1.2 at top, middle and bottom, then clipped to [0, 1].
   - Never: vertical flip, 90° rotation, elastic warp, cutout, MixUp, CutMix, hue or
     saturation changes.
3. Geometry moves image and target together; the target uses nearest-neighbour sampling.
   Pixels with no source pixel get image value 0 and target value background (0) on every
   layer, as black pixels outside the scan area are labelled today.
4. Library: torchvision 0.26 `transforms.v2` (already pinned); the crop-box jitter and the
   depth gain curve are written in the repo. No new dependency.
5. Randomness comes from the recipe seed, the epoch and the worker, so a run can be
   repeated.
6. Comparison: one run of the TASK-088 recipe with `augment="us_mild_v1"` and nothing else
   changed (same seed), against cirr-v4-tu-e30-r5, reported in an EXP record. More seeds
   only if the gap is small against seed noise.

## Consequences

- A method task builds it (reader, registry, train-evaluation reader, tests on synthetic
  data); an exp task runs the comparison after TASK-088 has its baseline.
- Texture augmentation (blur, speckle noise, JPEG) stays out until `us_mild_v1` is measured.
- A changed set is a new name (`us_mild_v2`, ...), never an edit of `us_mild_v1`, so old
  runs stay reproducible.
