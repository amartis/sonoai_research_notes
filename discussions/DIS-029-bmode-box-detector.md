---
id: DIS-029
title: B-mode box detector - one class with a wholeness value, negatives, sample kinds, ResNet vs Qwen3-VL
status: concluded
created: 2026-11-17
outcomes: [DEC-062, DEC-063]
related: [DEC-017, DEC-024, DEC-035, DEC-037, DEC-042, DEC-044, DEC-045, DEC-051, EXP-001]
---
# DIS-029: B-mode box detector - one class with a wholeness value, negatives, sample kinds, ResNet vs Qwen3-VL

## Question

The user wants an engine that tells whether an image contains B-mode ultrasound. It
must answer yes both for a screenshot that holds a B-mode image among other screen
content and for an image that is only (part of) the B-mode area. Two uses: filter
scraped public images (milestone m-4, scrape-public-datasources; today only a colour and
speckle heuristic, `src/sonoai/scraping/roboflow/modality.py`) and, later, guard model
inputs. The user proposed MedNIST and a small natural-image dataset as negatives, and
the project's own frames, with their B-mode crops, as positives.

## Options considered

**Output form.**

- **A, image classifier** (first draft): two image-level outputs, `contains` and `whole`.
  Simple, but it does not say where the B-mode is.
- **B, box detector, one class `B-mode` plus a float `whole` per box** (user's choice):
  says where, and how much of the B-mode image is visible. "Contains B-mode" is the top
  box score; "B-mode fills the image" is box area over image area. Needs one custom
  output on the detector head.
- **C, box detector with two classes `B-mode` and `B-mode partial`**: no custom head code;
  keeps as the fallback if the float output turns out costly.

**Meaning of `whole`.** The user chose "share of the full B-mode image that is visible in
the input" (1 = complete, 0.4 = 40 % visible, cut by the image edge). The other reading,
"share of the input covered by B-mode", needs no extra output because the box gives it.

**Negatives.**

- MedNIST alone is an easy negative: 64 x 64 grey images, so a model can separate them by
  size and colour, and the test would look near perfect while saying little.
- The user chose MedNIST + Imagenette-320 + regions of our own screenshots that overlap no
  B-mode box (text panels, strips), with every input brought to the same form (RGB,
  random rescale, JPEG and grey conversion on every kind) so size, compression and colour
  are not cues.
- Alternative not taken: COCO val2017 instead of Imagenette (more varied scenes, licences
  vary per image).

**Positives.** Whole frame, the B-mode box crop, random sub-crops of the box, and frame
crops cutting through a box. Frames where the cropper found no box (fallback) are left
out.

**Backbone.**

| | ResNet-50 detector, trained | Qwen3-VL-8B prompted, no training | Qwen3-VL fine-tuned or as backbone |
| --- | --- | --- | --- |
| Training needed | yes, on our cropper and reviewed boxes | none; the box prompt exists in `src/sonoai/labeling/ai_annotator.py` | heavy, on the GPU box |
| Speed | fast; CPU use on machine01 for scraping is plausible (estimate, unverified) | about 6 s per image on the GPU box ([EXP-001](../experiments/EXP-001-qwen3-vl-quality-filter-tuning-cirrhosis-v4.md)) | seconds per image (estimate) |
| `whole` output | trained, can be calibrated | as text, not calibrated | trainable |
| Box accuracy on our frames | expected high (trained on our layouts) | not measured; [TASK-032.11](../../backlog/tasks/task-032.11%20-%20Compare-Qwen3-VL-cropper-v1-and-cropper-v2-with-the-users-v1-review-on-the-held-out-datasources-EXP-record-DEC-042.md) compares it with the croppers | not measured |
| Unseen screen layouts | risk: trained on our devices only | stronger prior from web-scale pretraining | stronger prior |
| Evidence here | none yet | EXP-001: as a quality filter, no usable filter (other question) | none |

*Table 1. Backbone options for the B-mode box detector. Speeds other than EXP-001's are
estimates.*

## Conclusion

- [DEC-062](../decisions/DEC-062-bmode-box-detector-bmode-det-v1.md): detector `bmode_det`
  v1, torchvision FCOS ResNet-50-FPN, one class `B-mode` with a `whole` output per box;
  the sample kinds, split, anti-shortcut input and evaluation. Qwen3-VL prompted is a
  baseline only (user's choice).
- [DEC-063](../decisions/DEC-063-public-non-patient-datasets-root.md) (proposed): public
  non-patient datasets get their own root and may go to the GPU box.
- Board tasks (milestone m-4): [TASK-133](../../backlog/tasks/task-133%20-%20Public-negatives-for-the-B-mode-box-detector-MedNIST-and-Imagenette-320-under-PUBLIC_DATA_ROOT-licence-records-copy-to-the-GPU-box-DEC-062-DEC-063.md) (public negatives download, infra), [TASK-134](../../backlog/tasks/task-134%20-%20B-mode-detector-sample-builder-sonoai.data.bmode_det-and-sonoai-data-bmode-det-samples-the-sample-kinds-of-DEC-062-whole-share-split-synthetic-tests-DEC-062.md)
  (sample builder, method), [TASK-135](../../backlog/tasks/task-135%20-%20Detection-trainer-and-task-bmode_det-FCOS-ResNet-50-FPN-with-a-whole-output-per-box-in-memory-crop-reader-with-the-same-input-form-for-every-kind-metrics-and-baseline-scorers-synthetic-tests-DEC-062.md) (detection trainer and task, method), [TASK-136](../../backlog/tasks/task-136%20-%20bmode_det-v1-on-261023-build-the-sample-file-train-on-the-GPU-box-metrics-with-95-CI-against-modality.py-cropper-v1-and-Qwen3-VL-shortcut-check-EXP-record-DEC-062.md)
  (sample file build, training run and EXP record, exp).
- Left out by the user: a separate data task for the sample file (folded into the exp
  task) and choosing an external ultrasound test set.

Sources checked in this discussion:

- MedNIST licence CC BY-SA 4.0, images from TCIA, RSNA Bone Age and NIH Chest X-ray:
  <https://huggingface.co/monai-test/mednist_reg/blob/main/docs/data_license.txt>
- MedNIST size, 58,954 images in 6 classes at 64 x 64 (Mendeley "Medical MNIST", the
  closest match found): <https://data.mendeley.com/datasets/8hdt269s7r>
- Imagenette: 10 ImageNet classes, 9,469 train and 3,925 validation images, 320 px variant,
  Apache 2.0 per the Hugging Face card (fastai repo LICENSE not read yet):
  <https://huggingface.co/datasets/frgfm/imagenette/blob/main/README.md>,
  <https://www.tensorflow.org/datasets/catalog/imagenette>

## Open questions

- External ultrasound test set (devices and layouts not in 261023): not taken up now.
- Wiring the detector into the scraping pipeline, and using it as a learned cropper: after
  the EXP record of the first run.
