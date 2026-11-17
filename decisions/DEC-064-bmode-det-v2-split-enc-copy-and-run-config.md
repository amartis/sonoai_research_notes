---
id: DEC-064
title: bmode_det v2 - test from chosen datasource groups without the test-share rule, enc1 copy of the sample file, run config as a recipe and plan
status: accepted
area: [training, datasets]
created: 2026-11-17
from: [DIS-029]
related: [DEC-062, DEC-044, DEC-053, DEC-003, DEC-024]
superseded_by:
---
# DEC-064: bmode_det v2 - test from chosen datasource groups without the test-share rule, enc1 copy of the sample file, run config as a recipe and plan

## Context

The first bmode_det sample file (v1 on 261023_plain, built in
[TASK-136](../../backlog/tasks/task-136%20-%20bmode_det-v1-on-261023-build-the-sample-file-train-on-the-GPU-box-metrics-with-95-CI-against-modality.py-cropper-v1-and-Qwen3-VL-shortcut-check-EXP-record-DEC-062.md);
counts in [its dataset record](../datasets/261023/bmode_det_samples.md)) showed three problems:

1. **Most own data is dropped.** Test may hold only reviewed images
   ([DEC-062](DEC-062-bmode-box-detector-bmode-det-v1.md) item 4) and must be 8-13 % of the
   rows kept ([DEC-044](DEC-044-cirrhosis-sample-set-quality-filter-and-split.md) rule 8, through DEC-062 item 6). Only 805 images are reviewed, so the
   chosen test groups were large and their unreviewed images were dropped: 16,818 of 23,039
   usable images (73.9 % of own rows). Train kept 4,688 images from 21 datasources.
2. **The file cannot reach the GPU box.** The builder writes the plain file only, `make-enc`
   skips `derived/`, and the GPU box holds enc1 data only
   ([DEC-024](DEC-024-plain-never-leaves-machine01-ec2-label-studio-decrypts-in-ram.md)).
3. **The run config path is out of date.** `scripts/train.py` refuses
   `configs/experiments/*.yaml`; runs are recipe and plan files
   ([DEC-003](DEC-003-trainrecipe-files-structure.md)).

The user agreed to the lead's proposals on 2026-11-17 (lead session on TASK-136). For the
split, the user chose option A below, which keeps the datasource hold-out. Option B (all
reviewed images as test, all unreviewed images as train, datasources shared between them)
was rejected because the same datasources in train and test give test results that look
better than they are.

## Decision

This amends DEC-062 item 6 for own rows from sample file version 2 on. Version 1 stays as it
was built.

1. **Own split, option A.** Test is still whole datasource groups, and only the reviewed
   images of a test group are test rows. The unreviewed images of a test group are dropped:
   they are never in train or val. The DEC-044 rule 8 test share (8-13 % of rows kept, with
   its 2-point tolerance on the share of rows with a box) no longer applies to bmode_det.
   Instead, test groups are chosen so that as few images as possible are dropped while test
   holds at least `min_test_reviewed` reviewed images (a config value). The method agent picks
   and documents the choice rule. Train and val take every image of the other groups, split at random by
   image as before (DEC-044 rule 10, no datasource rule; corrected 2026-11-17). Public sets keep the random per-class split.
2. **The minimum is set after seeing values.** Before v2 is built, the exp agent reports, on
   261023, a table of possible `min_test_reviewed` values against test groups, test images and
   dropped images (counts only). The user sets the value from it. The test will be smaller than
   v1's 598 images, so its 95 % CIs will be wider.
3. **MedNIST cap.** The v2 config sets `public.mednist.max_per_class`. MedNIST is 58,954 of
   100,877 rows in v1, and each 64 px image is scaled up to the input size. The user sets the
   value after seeing the per-class counts.
4. **Enc1 copy.** `sonoai-data bmode-det-samples` gets an `--enc` option. It writes the same
   bytes into the dataset's enc1 store at the same path, as `sample-set freeze` does for the
   cirrhosis sample file (`sonoai.data.sample_sets.write_sample_file`). `gpu put` then copies
   the enc1 dataset to the GPU box. Plain data stays on machine01.
5. **Run config.** The bmode_det run is a recipe under `configs/train/recipes/det_bmode_v1/`
   and a plan under `configs/train/plans/det_bmode_v1/`. Starting values are the trainer's
   examples: COCO-pretrained, min_size 800 / max_size 1333, SGD lr 0.01 with a poly schedule,
   global batch 16, 12 epochs, augment `bmode_det_v1`, 1,000 bootstrap replicates for the CIs.
   The exp agent gives a run-time estimate and asks before the run.
6. **Sample-file names in records.** Dataset and EXP records may name the derived sample file
   by its versioned table name (`bmode_det_samples_v<version>_<codename>_df.pkl`). It is a name
   we chose for our own table, not a patient file name.

## Consequences

- [TASK-137](../../backlog/tasks/task-137%20-%20bmode_det-sample-file-on-the-GPU-box-enc1-copy-of-derived-bmode_det_samples_v1_-version-_plain_df.pkl-for-the-TASK-135-reader-DEC-062.md) (method) adds the `--enc` option and the option-A test
  choice, with synthetic tests. [TASK-136](../../backlog/tasks/task-136%20-%20bmode_det-v1-on-261023-build-the-sample-file-train-on-the-GPU-box-metrics-with-95-CI-against-modality.py-cropper-v1-and-Qwen3-VL-shortcut-check-EXP-record-DEC-062.md)
  (exp) depends on it. It then reports the `min_test_reviewed` and MedNIST tables, builds v2
  with its enc1 copy, trains and writes the EXP record.
- v1 stays in `derived/` as built ([DEC-053](DEC-053-table-naming-and-preservation.md)); its dataset record notes that v2 replaces it for
  training.
- A smaller test set means wider CIs. If they are too wide to compare with the baselines,
  reviewing more boxes in the test groups is the way to grow the test set.
