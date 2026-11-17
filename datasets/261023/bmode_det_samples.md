# bmode_det v1 sample file and train/val/test split on 261023_plain

[TASK-136](../../../backlog/tasks/task-136%20-%20bmode_det-v1-on-261023-build-the-sample-file-train-on-the-GPU-box-metrics-with-95-CI-against-modality.py-cropper-v1-and-Qwen3-VL-shortcut-check-EXP-record-DEC-062.md), [DEC-062](../../decisions/DEC-062-bmode-box-detector-bmode-det-v1.md), [DEC-044](../../decisions/DEC-044-cirrhosis-sample-set-quality-filter-and-split.md), [DEC-063](../../decisions/DEC-063-public-non-patient-datasets-root.md). Aggregates only; no images, file names or identifiers. Counts and a fixed split, no model. Reporting checklists (CLAIM, STARD): not applicable.

Made on 2026-11-17 on `261023_plain` ([DEC-018](../../decisions/DEC-018-plain-style-for-local-research.md)) with `sonoai-data bmode-det-samples 261023_plain` (default config `configs/data/bmode_det.yaml`, `version: 1`, seed 0; code at master 98b02e6, builder of [TASK-134](../../../backlog/tasks/task-134%20-%20B-mode-detector-sample-builder-sonoai.data.bmode_det-and-sonoai-data-bmode-det-samples-the-sample-kinds-of-DEC-062-whole-share-split-synthetic-tests-DEC-062.md)). Column meanings and the split rule: [derived.md](../../../docs/datasets/styles/derived.md) (section `bmode_det_samples`). Task `det_bmode_v1`.

## Result

- Sample file: `derived/bmode_det_samples_v1_261023_plain_df.pkl` in `261023_plain` (plain, machine01 only). **No enc1 copy yet**: the command writes the plain file only and `make-enc` skips `derived/`, so the GPU box cannot read it yet ([TASK-137](../../../backlog/tasks/task-137%20-%20bmode_det-sample-file-on-the-GPU-box-enc1-copy-of-derived-bmode_det_samples_v1_-version-_plain_df.pkl-for-the-TASK-135-reader-DEC-062.md), open).
- Table sha256: `bae1dc33333170007124364f263a3366678159f4d50c27b3898578233352b633` (checked again on the written file). A changed table is a new file name ([DEC-053](../../decisions/DEC-053-table-naming-and-preservation.md)).
- Box source: cropper v1 (`cropper_version` 1) with the user's reviewed boxes where they exist.
- Reader check: the detector's sample reader (`BmodeDetReader`, [TASK-135](../../../backlog/tasks/task-135%20-%20Detection-trainer-and-task-bmode_det-FCOS-ResNet-50-FPN-with-a-whole-output-per-box-in-memory-crop-reader-with-the-same-input-form-for-every-kind-metrics-and-baseline-scorers-synthetic-tests-DEC-062.md)) accepted the table (train 75,651, val 15,139, test 10,087 rows).
- Build time about 60 s on machine01.

## Images

Table 1. Own images from the box table to the sample file. Counts are images (one image = one file of the labeling crop table, after merging second paths of the same image).

| Step | Images |
|---|---|
| In the box table | 29,468 |
| Left out: cropper fallback, not reviewed | 6,308 |
| Left out: second path of the same image | 121 |
| Left out: unreadable, box outside the image, no labeling row | 0 |
| Kept | 23,039 |
| of those reviewed by the user | 805 (0 reviewed as "no B-mode") |
| Dropped from test groups (not reviewed) | 16,818 |
| In the sample file | 6,221 |

## Split

- Test: 51 datasource groups (51 datasources), chosen by the DEC-044 rule 9 counts on the rows that stay in test. Only reviewed images of a test group are test rows.
- Train: 19 datasource groups (21 datasources); val: 18 groups (20 datasources). No image is in more than one split.
- Shares of the 28,529 own rows kept: train 75.0% (21,394), val 15.0% (4,282), test 10.0% (2,853); share of rows with a target box in test minus that of the rows kept: +1.8 points (limit 2).
- Box source of the images in the file: test 598 reviewed; val 32 reviewed, 903 cropper; train 175 reviewed, 4,513 cropper.
- Images with 2 boxes: test 56 of 598, val 3 of 935, train 12 of 4,688.
- Public rows (MedNIST 6 classes, Imagenette-320 10 classes): seeded random split per dataset and class, 75/15/10%.

Table 2. Rows per kind and split. Own kinds (`frame` to `own_neg`) come from 261023 images; `mednist` and `natural` are public images (DEC-063). `frame` rows = images, `box`, `box_sub` and `frame_part` rows = boxes. Train rows of `box_sub`, `frame_part` and `own_neg` (12,006) get a new random input window each time they are read; val and test windows are fixed.

| kind | train | val | test | all |
|---|---|---|---|---|
| frame | 4,688 | 935 | 598 | 6,221 |
| box | 4,700 | 938 | 654 | 6,292 |
| box_sub | 4,700 | 938 | 654 | 6,292 |
| frame_part | 4,700 | 938 | 654 | 6,292 |
| own_neg | 2,606 | 533 | 293 | 3,432 |
| mednist | 44,216 | 8,843 | 5,895 | 58,954 |
| natural | 10,041 | 2,014 | 1,339 | 13,394 |
| all | 75,651 | 15,139 | 10,087 | 100,877 |

## Open points (counts only)

1. **The test choice drops most own data.** 80,680 of 109,209 own rows (73.9%; 16,818 of 23,039 kept images) are dropped, because the chosen test groups hold many images that were not reviewed. The rule (DEC-062 items 4 and 6, as built in TASK-134) counts the test share on the rows kept, so a dropped row costs nothing in the choice. Train keeps 4,688 images from 21 datasources; test spans 51 datasources.
2. **Public rows outnumber own rows:** 72,348 public against 28,529 own rows (71.7% of all rows); MedNIST alone is 58,954. The config's `max_per_class` (unset, so every image) can limit this in a new config version.
3. Test boxes are reviewed boxes only (DEC-062 item 4); train and val are mostly cropper boxes (96.3% and 96.6% of images), so the detector can learn the cropper's errors.
