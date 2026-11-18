---
id: DIS-031
title: Does the Qwen3-VL B-mode box prompt answer "No B-mode image" on the public negatives (MedNIST, Imagenette-320)?
status: concluded
created: 2026-11-17
outcomes: []
related: [DEC-035, DEC-042, DEC-062, DEC-063, DIS-029]
---
# DIS-031: Does the Qwen3-VL B-mode box prompt answer "No B-mode image" on the public negatives (MedNIST, Imagenette-320)?

## Question

The Qwen3-VL-8B box prompt ([DEC-035](../decisions/DEC-035-qwen3-vl-second-annotator-on-gpu-box.md))
is a baseline for the B-mode box detector ([DEC-062](../decisions/DEC-062-bmode-box-detector-bmode-det-v1.md)).
It was tuned on ultrasound screen frames only. Does it wrongly return a box on the
public negatives (MedNIST: other modalities, 64 x 64 grey; Imagenette-320: natural photos)?
[TASK-136](../../backlog/tasks/task-136%20-%20bmode_det-v1-on-261023-build-the-sample-file-train-on-the-GPU-box-metrics-with-95-CI-against-modality.py-cropper-v1-and-Qwen3-VL-shortcut-check-EXP-record-DEC-062.md) scores Qwen3-VL on the detector's test samples, but only after training.

## Options considered

- **Own small exp task now**: the answer comes before the detector run and can change the
  baseline plan. Needs a small command, because `ai-label run` only reads the enc1 store
  of an allowed project.
- **Leave it to TASK-136 step 14**: no new work, answer late, pooled with other kinds.

## Conclusion

The user chose (2026-11-17): own small task; 100 images per class (MedNIST 6 classes,
Imagenette 10 classes, 1,600 images, fixed seed); check only, the prompt stays unchanged
(a changed prompt would change its hash and break the [DEC-042](../decisions/DEC-042-qwen-tuning-and-comparison-on-the-users-v1-review.md)
comparisons). Measure: share of images with a box or an unparsed reply, per class and
per dataset, with 95% Wilson interval. Any prompt change after seeing the values is a
new decision. No DEC needed: no existing decision changes. Work: a method task (command) and
an exp task (run on the GPU box); public images are not patient data ([DEC-063](../decisions/DEC-063-public-non-patient-datasets-root.md)).

## Open questions

- No ultrasound positive control in this check; the miss rate on real frames comes from
  [TASK-032.11](../../backlog/tasks/task-032.11%20-%20Compare-Qwen3-VL-cropper-v1-and-cropper-v2-with-the-users-v1-review-on-the-held-out-datasources-EXP-record-DEC-042.md) and TASK-136.
