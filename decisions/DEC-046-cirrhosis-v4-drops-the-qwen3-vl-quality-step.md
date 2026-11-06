---
id: DEC-046
title: Cirrhosis v4 sample set drops the Qwen3-VL quality step; bad samples are left out by choice labels and user skips only
status: accepted
area: [datasets, labeling]
created: 2026-11-05
from: [DIS-019]
related: [DEC-044, DEC-042, DEC-035]
superseded_by:
---
# DEC-046: Cirrhosis v4 drops the Qwen3-VL quality step

## Context

[DEC-044](DEC-044-cirrhosis-sample-set-quality-filter-and-split.md) rule 6 filters the cirrhosis
candidates with Qwen3-VL-8B-Instruct and accepts a prompt only if it flags at most 2% of
known-good frames. The two tuning runs of [TASK-086](../../backlog/tasks/task-086%20-%20Qwen3-VL-quality-filter-for-the-cirrhosis-candidates-tune-on-the-search-part-accept-on-held-out-datasources-at-most-2-of-known-good-flagged-run-on-all-candidates-EXP-record-DEC-044.md)
(search part, 297 known-good and 300 known-bad crops) did not give a usable filter: the
default prompt flagged 67/297 known-good (22.6%), the lenient prompt flagged 0/297 known-good
and 1/300 known-bad, so it filters nothing. On 2026-11-05 the user chose to drop the step.

## Decision

1. **DEC-044 rule 6 does not apply to `lseg_cirrhosis_v4`.** Bad samples are left out only by
   DEC-044 rule 4: a per-image choice label with role `quality` or `exclusion`, or a frame the
   user skipped in the local Label Studio review "[TASK-032](../../backlog/tasks/task-032%20-%20Run-the-B-mode-cropper-on-a-dataset-version-polygon-check-reviewed-set-box-table-DEC-017.md) B-mode boxes v1". Rules 1-5 and
   7-11 of DEC-044 stay as they are.
2. `sonoai-data sample-set freeze` gets an explicit `--no-verdicts` flag. The freeze output
   and the dataset record say that no Qwen3-VL check ran; no placeholder verdict table.
3. TASK-086 stops its GPU runs, records the two tuning runs in an EXP record and goes to
   Review without running on all candidates.

## Consequences

- Most candidates were never looked at by the user (on the 128 px table, 453 known-good and
  1,413 known-bad of 18,946 crops), so poor-quality crops without a choice label or skip stay
  in the set; the 128 px minimum is the only other guard. The dataset record reports the
  known-good and unreviewed counts per split (known-bad crops are dropped by rule 4).
- The Qwen3-VL quality filter can come back for a later version as a new DEC.
- Work: a `method` task for `--no-verdicts`; [TASK-087](../../backlog/tasks/task-087%20-%20Fix-the-cirrhosis-sample-file-and-its-train-val-test-split-dataset-record-with-counts-per-split-DEC-044.md) depends on it instead of TASK-086.
