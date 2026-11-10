---
id: DIS-022
title: Data augmentation for ultrasound segmentation training
status: concluded
created: 2026-11-10
outcomes: [DEC-049]
related: [DEC-006, DEC-017, DEC-043, DEC-045, DIS-007]
---
# DIS-022: Data augmentation for ultrasound segmentation training

## Question

Which data augmentation makes sense for training ultrasound segmentation, starting with
lseg_cirrhosis_v4 ([DEC-043](../decisions/DEC-043-cirrhosis-task-gt-organ-layer-predicted-cirrhosis-only.md))? No augmentation exists yet: `Data.augment` is
a name only and the sample reader refuses it. Why now: the first cirrhosis run
([TASK-088](../../backlog/tasks/task-088%20-%20Train-lseg_cirrhosis_v4-on-the-fixed-sample-file-and-write-the-EXP-record-DEC-043-DEC-045.md), cirr-v4-tu-e30-r5) trains without augmentation, and positives are rare
(477 of 10,331 train samples, 4.6%), so more variety for them may help.

## Options considered

Each candidate was judged from ultrasound physics and the task's cues (my judgement, not
checked against papers):

| Augmentation | Verdict | Reason |
|---|---|---|
| Horizontal flip | use | screen orientation varies by view; texture has no left/right |
| Small rotation, scale, shift | use, mild | probe tilt and position |
| Crop-box jitter | use | cropper error ([DEC-017](../decisions/DEC-017-bmode-cropper.md)); project-specific |
| Brightness, contrast, gamma | use, mild | gain and dynamic range differ by device ([DIS-007](DIS-007-device-type-tagging-and-sensitivity.md)) |
| Depth gain curve (TGC) | use, mild | per-depth gain knobs on the scanner |
| Blur, sharpen, speckle noise, JPEG | later, own test | cirrhosis is read from echotexture; may erase or fake it |
| Vertical flip, 90° rotation | no | depth runs downward (skin on top, attenuation and shadows below) |
| Strong elastic warp | no | may change surface nodularity, a cirrhosis sign |
| Cutout, MixUp, CutMix | no | mixes or hides diseased and healthy texture; labels become wrong |

Table 1. Candidate augmentations for ultrasound segmentation, with verdict and reason.

The official TransUNet code reportedly uses 90° rotation, flips and ±20° rotation, made for
CT (unverified: repository not checked); not taken over, because ultrasound has a depth
direction.

Further choices put to the user (2026-11-10):

- **First set**: mild ultrasound set (chosen) · geometry only · mild set plus texture.
- **Comparison**: one extra run, same seed as the baseline (chosen) · 2 seeds per arm ·
  three arms (none, geometry, geometry + intensity).
- **Library**: torchvision 0.26 `transforms.v2`, already pinned (chosen) · albumentations
  (new pin on the GPU box).

## Conclusion

[DEC-049](../decisions/DEC-049-mild-ultrasound-augmentation-us-mild-v1.md): a named augmentation `us_mild_v1` built with torchvision v2,
an unaugmented train reader for the train evaluation ([DEC-045](../decisions/DEC-045-per-sample-confusion-matrices-in-runs.md) rule 3), and one run
of the TASK-088 recipe with `augment="us_mild_v1"` and the same seed, compared with
cirr-v4-tu-e30-r5. Board: a `method` task for the code, an `exp` task for the run.

## Open questions

- Texture augmentation (blur, speckle, JPEG): only after `us_mild_v1` is measured, and
  better with device information from [DIS-007](DIS-007-device-type-tagging-and-sensitivity.md).
- More seeds, if the gap between the two runs is small against seed noise (about 97 val
  positives).
