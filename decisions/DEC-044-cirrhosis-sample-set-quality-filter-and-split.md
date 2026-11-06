---
id: DEC-044
title: Cirrhosis sample set - one sample per image and crop box, rule and Qwen3-VL quality filter, a fixed sample file, test held out by datasource
status: accepted
area: [datasets, labeling]
created: 2026-11-05
from: [DIS-019]
related: [DEC-035, DEC-036, DEC-037, DEC-042, DEC-043, DEC-046, DIS-012]
superseded_by:
---
# DEC-044: Cirrhosis sample set, quality filter and split

## Context

[DIS-019](../discussions/DIS-019-cirrhosis-training-task.md). The task of
[DEC-043](DEC-043-cirrhosis-task-gt-organ-layer-predicted-cirrhosis-only.md) needs a fixed set of samples
of normal image quality, split into train, val and test. `taskcrops_df` has one row per
labeling task, so one crop can appear in several projects. The general rule for quality and
exclusion crops is still open ([TASK-062](../../backlog/tasks/task-062%20-%20Decide-the-rule-for-leaving-out-quality-and-case-exclusion-crops-from-train-val-test-DIS-012.md)); this DEC sets it for this task only.

## Decision

### Sample identity

1. **One sample = one image + one crop box**: key = image hash (`np_md5_c3_current`) and
   the box (`left`, `top`, `right`, `bottom`). The labels (polygons and choices) of every
   `taskcrops_df` row with that key are combined.
2. If one image hash appears under two datasources, those datasources form one **group**
   for the test split, so the image cannot sit on both sides.

### Filter, in this order (counts reported after each step)

3. **Eligible** under DEC-043 (liver polygon, cirrhosis looked at, clear status).
4. **Rule filter**: drop a sample when any of its projects gave a choice label with role
   `quality` or `exclusion` (`configs/data/choice_labels.yaml`, [DEC-036](DEC-036-choice-polygon-relation-table.md)), or when its frame was
   skipped by the user in the local project "[TASK-032](../../backlog/tasks/task-032%20-%20Run-the-B-mode-cropper-on-a-dataset-version-polygon-check-reviewed-set-box-table-DEC-017.md) B-mode boxes v1".
5. **Size**: drop crops whose shorter side is below a minimum. The data task reports the
   counts at a few candidate minimums; the user picks one before the sample file is fixed.
6. *(Not used for `lseg_cirrhosis_v4`: dropped by [DEC-046](DEC-046-cirrhosis-v4-drops-the-qwen3-vl-quality-step.md), 2026-11-05.)*
   **Qwen3-VL-8B-Instruct filter** (4-bit, on the GPU box, enc1 in memory, [DEC-035](DEC-035-qwen3-vl-second-annotator-on-gpu-box.md)): the
   prompt asks whether the crop is a normal-quality liver B-mode scan (not dark, blurred,
   low-resolution, a paper scan, from an unusual device, or covered in marks).
   - Bad examples for the prompt: crops with a `quality` choice and frames the user skipped in
     "TASK-032 B-mode boxes v1". Known-good: frames the user finished there without skipping.
   - Prompt tuning sees only the search part of the [DEC-037](DEC-037-cropper-v2-and-second-review-project.md) datasource split; prompt examples
     come from that part only ([DEC-042](DEC-042-qwen-tuning-and-comparison-on-the-users-v1-review.md) pattern).
   - **Acceptance, on the held-out datasources:** the filter flags at most 2% of known-good
     frames (point estimate, 95% CI reported), and its share of known-bad frames flagged is
     reported. If no prompt meets 2%, the Qwen step is not used and the user is asked.
   - Then it runs on every sample left after step 5; flagged samples are dropped.

### Fixed sample file

7. The result is one table inside the dataset, `derived/cirrhosis_v4_samples_df.pkl` in
   `261023_plain`: sample number, the `taskcrops_df` ids it combines, datasource group,
   positive or negative, split. A copy goes into the enc1 store (encrypted) so the GPU box
   reads it in memory; it never leaves machine01 in plain form ([DEC-024](DEC-024-plain-never-leaves-machine01-ec2-label-studio-decrypts-in-ram.md)). Runs record the
   table's hash. A changed table is a new file name, never an overwrite.

### Split

8. Seeded and reproducible. Targets: train 75%, val 15%, test 10% of samples; allowed
   ranges train 70-85%, val 15-23%, test 8-13%.
9. **Test first, by datasource group**: a set of groups whose samples are 8-13% of the
   total and whose cirrhosis share is within 2 percentage points of the whole set, closest
   to 10%. No group is in both test and train+val.
10. **Train / val at random** on the rest, without the datasource rule (the user's choice),
    stratified by positive / negative; crops of one image stay in one split.
11. If no test choice meets rule 9, the task stops and reports the closest options; the
    user decides.

## Consequences

- Validation shares datasources (and maybe patients) with train, so validation scores are
  optimistic; the test split is the unbiased one (said to the user in DIS-019).
- The quality and exclusion rule here applies to this task; TASK-062 stays open for others.
- Work: `method` code for sample merging, filters and split search; a `method` extension
  of the ai-label command for the quality question; a `data` task for the candidate list;
  an `exp` task for the Qwen tuning and run; a `data` task that fixes the file and the split
  and writes the dataset record (aggregates only).
