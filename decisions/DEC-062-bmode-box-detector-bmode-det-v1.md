---
id: DEC-062
title: B-mode box detector bmode_det v1 - FCOS ResNet-50 with one class and a wholeness value per box, own and public negatives, datasource-held-out test
status: accepted
area: [training, datasets]
created: 2026-11-17
from: [DIS-029]
related: [DEC-017, DEC-035, DEC-037, DEC-044, DEC-045, DEC-063, DEC-064]
superseded_by:
---
# DEC-062: B-mode box detector bmode_det v1 - FCOS ResNet-50 with one class and a wholeness value per box, own and public negatives, datasource-held-out test

## Context

An engine is needed that finds B-mode ultrasound in an image, both in a screenshot with
other screen content and in an image that is only part of a B-mode area. It will filter
scraped public images (milestone m-4) and later guard model inputs
([DIS-029](../discussions/DIS-029-bmode-box-detector.md)). Dataset 261023 has a B-mode box
per frame from the classical cropper v1
([DEC-017](DEC-017-bmode-cropper.md): 29,832 boxes on 29,468 frames, 6,717 fallback) and
a set of boxes reviewed by the user. The repo has no detection trainer yet.

## Decision

The user accepted this on 2026-11-17 (consult session, plan approved).

1. **Model.** torchvision FCOS with a ResNet-50-FPN backbone (COCO-pretrained), one class
   `B-mode`, plus one extra output per location, `whole` in [0, 1]: the share of the full
   B-mode image that is visible in the input (1 = complete; 0.4 = 40 % visible, cut by the
   image edge). If the extra output turns out costly, the fallback is plain two-class FCOS
   (`B-mode`, `B-mode partial`; partial = `whole` below a threshold), recorded in the task.
2. **Image-level answers.** "Contains B-mode" = the top box score is at least a threshold;
   "B-mode fills the image" = box area over image area. No extra outputs for these.
3. **Sample kinds.** Crops are made in memory at read time and never written to disk.

   | Kind | Input | Target boxes |
   | --- | --- | --- |
   | frame | whole 261023 frame with a cropper box | its 1-2 B-mode boxes, `whole` = 1 |
   | box | B-mode box crop | one box = whole input, `whole` = 1 |
   | box_sub | random sub-crop of a box, at least 30 % of its area | one box = whole input, `whole` = visible share |
   | frame_part | random frame crop that cuts through a box | the clipped box, `whole` = visible share |
   | own_neg | frame region that overlaps no box | none |
   | mednist | MedNIST image (other modalities) | none |
   | natural | Imagenette-320 image | none |

   *Table 1. Sample kinds of bmode_det v1. Fallback frames (cropper found no box) are left
   out. The black corners of a sector scan inside the box count as part of the B-mode image.*

4. **Boxes.** The user's reviewed boxes where they exist, else cropper v1 non-fallback
   boxes. Test boxes and test `own_neg` regions come only from reviewed frames.
5. **Same input form for every kind.** All inputs become 3-channel RGB; random rescale,
   JPEG compression and grey conversion apply to every kind, so size, compression and
   colour are not cues (MedNIST is 64 x 64 grey).
6. **Split.** Own samples: test held out by datasource group, reusing
   `sonoai.data.sample_sets` (`datasource_groups`, `choose_test_groups`, `make_split`) as
   in [DEC-044](DEC-044-cirrhosis-sample-set-quality-filter-and-split.md); public sets:
   random, stratified by class, same shares. Validation and test crops are fixed in the
   sample file, which gives the sample numbers runs key on
   ([DEC-045](DEC-045-per-sample-confusion-matrices-in-runs.md)); train crops are random.
7. **Evaluation**, each with a 95 % CI (bootstrap over datasources for own data), overall
   and per kind: image-level AUROC and sensitivity at 99 % specificity; box AP at IoU 0.5
   and 0.75; mean absolute error of `whole`. Baselines on the same test: the
   `modality.py` heuristic (image level), the classical cropper v1 (boxes and confidence)
   and Qwen3-VL prompted with the existing box prompt
   ([DEC-035](DEC-035-qwen3-vl-second-annotator-on-gpu-box.md)). Shortcut check: positives
   downscaled to 64 px and MedNIST upscaled, scored again.
8. **Public negatives** (MedNIST, Imagenette-320) are stored as in
   [DEC-063](DEC-063-public-non-patient-datasets-root.md).

## Consequences

- New code: a sample builder (`sonoai.data.bmode_det`, a `sonoai-data` command) and the
  repo's first detection trainer with task `bmode_det`. Both are tested on synthetic data.
- The sample file is a new derived table of 261023_plain
  (`bmode_det_samples_v1_261023_plain_df.pkl`); the exp task builds it with the builder's
  command and lists it on its `tables:` line.
- The detector is trained on cropper v1 boxes outside the reviewed set, so it can learn the
  cropper's errors; the test uses reviewed boxes only.
- Not decided now: an external ultrasound test set, wiring the detector into scraping,
  using it as a learned cropper.
- Board tasks (milestone m-4):
  - [TASK-133](../../backlog/tasks/task-133%20-%20Public-negatives-for-the-B-mode-box-detector-MedNIST-and-Imagenette-320-under-PUBLIC_DATA_ROOT-licence-records-copy-to-the-GPU-box-DEC-062-DEC-063.md) (public negatives MedNIST and Imagenette-320, infra);
  - [TASK-134](../../backlog/tasks/task-134%20-%20B-mode-detector-sample-builder-sonoai.data.bmode_det-and-sonoai-data-bmode-det-samples-the-sample-kinds-of-DEC-062-whole-share-split-synthetic-tests-DEC-062.md) (sample builder and crop geometry, method);
  - [TASK-135](../../backlog/tasks/task-135%20-%20Detection-trainer-and-task-bmode_det-FCOS-ResNet-50-FPN-with-a-whole-output-per-box-in-memory-crop-reader-with-the-same-input-form-for-every-kind-metrics-and-baseline-scorers-synthetic-tests-DEC-062.md) (detection trainer and task bmode_det, method; blocked by TASK-134);
  - [TASK-136](../../backlog/tasks/task-136%20-%20bmode_det-v1-on-261023-build-the-sample-file-train-on-the-GPU-box-metrics-with-95-CI-against-modality.py-cropper-v1-and-Qwen3-VL-shortcut-check-EXP-record-DEC-062.md) (sample file, training run and EXP record, exp; blocked by TASK-133 to TASK-135).
