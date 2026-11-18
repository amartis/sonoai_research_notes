---
id: DEC-068
title: us_mild_v2 - outside the crop the image is 0 and the target is background, for class-id and label-set tasks
status: accepted
area: [training]
created: 2026-11-18
from: []
related: [DEC-049, DEC-066, DEC-067]
superseded_by:
---
# DEC-068: us_mild_v2 - outside the crop the image is 0 and the target is background

## Context

`us_mild_v1` ([DEC-049](DEC-049-mild-ultrasound-augmentation-us-mild-v1.md)) fills two regions:

| Region | Image in us_mild_v1 | Target in us_mild_v1 |
|---|---|---|
| Affine fill (source pixel outside the image, DEC-049 item 3) | 0 | background (class id 0) |
| Jitter band (pixels of the enlarged crop box outside the original box, DEC-049 item 2) | real image pixels | background (class id 0) |

Table 1. Fill of `us_mild_v1` per region.

Two problems:

1. For a label-set target ([DEC-066](DEC-066-epic1-model-task-label-set-softmax.md) rule 3,
   bitmask) the value 0 is the empty set, which the label-set losses refuse.
   [DEC-067](DEC-067-us-mild-v1-fill-for-label-set-targets.md) answered this alone, with fill
   {background}, and is replaced by this record.
2. In the jitter band, real tissue gets the target background: label noise.

`us_mild_v1` was run in [EXP-002](../experiments/EXP-002-augmentation-ablation-lseg-cirrhosis-v4.md) (augmentation ablation, cirrhosis v4), so DEC-049's rule
applies: a changed step is a new name, and v1 stays as it is.

## Decision

1. **New augmentation `us_mild_v2`**: the same steps, probabilities and values as
   `us_mild_v1` (DEC-049 item 2), and the same random draws in the same order. The only change:
   outside the original crop box, the image is 0 and the target is background. So in the jitter
   band the image is 0 (not the real pixels), and in the affine fill the image stays 0.
2. **Background** is the task's target fill value: class id 0 for class-id tasks, the label set
   {background} (bitmask value 1) for label-set tasks. The value comes from the task.
3. `us_mild_v1` is unchanged, so EXP-002 stays reproducible. It works with class-id tasks only;
   with a label-set task it is refused.

Reasons (the user's rule, agreed in a consult session; no DIS record): every pixel outside the
crop is treated the same way, as black and background; no real tissue gets the background
label; one rule covers class-id and label-set tasks.

## Consequences

- DEC-067 is superseded.
- Board: [TASK-158](../../backlog/tasks/task-158%20-%20us_mild_v1-fill-for-label-set-targets-augmentation-writes-target-0-outside-the-image-and-outside-the-original-crop-box-the-empty-set-of-a-DEC-066-bitmask-target-which-the-label-set-losses-refuse.md) (us_mild_v2: zero image and background target outside the crop, method)
  implements it.
- Runs that want the new rule name `augment: us_mild_v2`; nothing changes in existing configs.
