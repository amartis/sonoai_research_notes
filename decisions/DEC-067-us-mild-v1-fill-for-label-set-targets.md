---
id: DEC-067
title: us_mild_v1 fill for label-set targets - filled target pixels are {background}
status: superseded
area: [training]
created: 2026-11-18
from: []
related: [DEC-049, DEC-066]
superseded_by: DEC-068
---
# DEC-067: us_mild_v1 fill for label-set targets - filled target pixels are {background}

## Context

`us_mild_v1` ([DEC-049](DEC-049-mild-ultrasound-augmentation-us-mild-v1.md)) writes target
value 0 (background as a class id) in two places:

1. **Affine fill** (DEC-049 item 3): pixels whose source lies outside the image; the image is
   0 (black) there.
2. **Crop-box jitter** (DEC-049 item 2): real image pixels of the enlarged box that lie outside
   the original crop box, where label polygons were clipped.

For a label-set target ([DEC-066](DEC-066-epic1-model-task-label-set-softmax.md) rule 3,
bitmask) the value 0 is the empty set, which the label-set losses refuse, so an anatomy run
with `us_mild_v1` would stop at the first filled pixel. Found in [TASK-157](../../backlog/tasks/task-157%20-%20Label-set-losses-for-the-anatomy-task-per-pixel-allowed-class-bitmask-target-builder-marginalized-cross-entropy-marginalized-Dice-and-leaf-Dice-synthetic-tests-DEC-066.md) (label-set losses).

Options discussed in a consult session (no DIS record; the choice was small):

| Option | Affine fill | Jitter band | When it would win |
|---|---|---|---|
| A (chosen) | {background} = 1 | {background} = 1 | Box edges sit at the scan-area edge, so the band is mostly outside the scan area |
| B | {background} = 1 | full set = 31 (no loss) | B-mode boxes are often tight, so the band holds organ tissue whose polygons were clipped |
| C | full set = 31 | full set = 31 | Augmentation should never add a label |

Table 1. Fill options for a label-set target (K = 5 classes; full set = 2^5 - 1 = 31, which adds
no loss under DEC-066 rule 4).

## Decision

1. For a label-set task, `us_mild_v1` fills target pixels with **{background}** (bitmask value
   1) in both places: the affine fill and the jitter band outside the original crop box.
2. The fill value comes from the task; class-id tasks keep 0, so their targets and past runs
   are unchanged.
3. This defines `us_mild_v1` for label-set targets (none existed before), so it is not a
   change of `us_mild_v1` under DEC-049; a later change of the fill is a new augmentation name.

Reasons: it keeps the meaning of DEC-049 item 3 (filled pixels are background, as black outside
the scan area is labelled today); samples are B-mode crops ([DEC-065](DEC-065-mission-upper-abdomen-anatomy-segmentation.md)), so the up-to-3% band outside
the box is mostly outside the scan area (an assumption, not measured); class-id runs and the
DEC-066 rule 7 sigmoid comparison then see the same targets.

## Consequences

- Board: [TASK-158](../../backlog/tasks/task-158%20-%20us_mild_v1-fill-for-label-set-targets-augmentation-writes-target-0-outside-the-image-and-outside-the-original-crop-box-the-empty-set-of-a-DEC-066-bitmask-target-which-the-label-set-losses-refuse.md) (us_mild_v1 fill for label-set targets, method) implements it.
- If DEC-066 point 2 (data preparation) finds tight B-mode boxes, option B is the alternative,
  as a new augmentation name.
