---
id: DEC-042
title: Qwen3-VL prompt tuning and its comparison use the user's v1 review, split by datasource as in DEC-037
status: accepted
area: [labeling]
created: 2026-11-04
from: [DIS-018]
related: [DEC-035, DEC-037]
superseded_by:
---
# DEC-042: Qwen3-VL prompt tuning and its comparison use the user's v1 review, split by datasource as in [DEC-037](DEC-037-cropper-v2-and-second-review-project.md)

## Context

[DIS-018](../discussions/DIS-018-qwen-prompt-tuning-and-comparison-set.md): the
"fixed 72-frame subset" of [DEC-035](DEC-035-qwen3-vl-second-annotator-on-gpu-box.md)
was never defined, and DEC-035 named no human label set for the comparison. On
2026-11-04 the user chose to tune and compare against their own local review.

## Decision

This replaces the last two "Blind" bullets of DEC-035 (human annotations not read
before the freeze; tuning on a 72-frame subset scored against the cropper and
polygons). The rest of DEC-035 stands, including: the model never sees the cropper's
boxes.

- **Human labels.** The user's submitted reviews in the local v1 project
  ("[TASK-032](../../backlog/tasks/task-032%20-%20Run-the-B-mode-cropper-on-a-dataset-version-polygon-check-reviewed-set-box-table-DEC-017.md) B-mode boxes v1", local target); skipped frames left out. Not the v2
  project and not the aws-labelstud set.
- **Split.** `split_by_datasource` from `sonoai.data.bmode_tune` on those frames,
  `search_share=0.7`, seed 0: the same split as cropper v2 tuning (DEC-037). The
  held-out datasource ids are written to the run's record before tuning starts.
- **Tuning.** Only on the search part. At most 5 prompt variants. Rank by the
  `bmode_tune` frame score (sum of matched-box IoU over the larger box count; IoU =
  box overlap, 0 to 1) against the user's boxes. A variant qualifies only if the
  polygon area outside its boxes is at most 0.02 and at most 5% of frames fail
  (no parsable answer). These two thresholds are a proposal, not checked against data.
- **Freeze.** The chosen prompt fixes `model_version` before any held-out frame is
  scored.
- **Comparison.** On the held-out part only: Qwen against the user's boxes, next to
  cropper v1 and cropper v2 on the same frames. Mean matched IoU, box-count accuracy,
  agreement on "No B-mode image", failed share; per datasource and overall; n and 95%
  CI (datasource bootstrap, as in `bmode_tune.summarise`); aggregates only.
- **Full run.** Unchanged: all 1,371 frames go through the frozen model and into the
  local mirror project `task-032-bmode-boxes-ai`.

## Consequences

- Qwen is no longer blind to the user's labels. Its test numbers stay fair only
  because tuning never reads held-out frames.
- The remote assistant's aws-labelstud set is not compared with Qwen. That can be a
  later task.
- Cropper v2 tuning ([TASK-032.08](../../backlog/tasks/task-032.08%20-%20Tune-cropper-v2-on-the-users-v1-review-build-its-box-table-and-polygon-check-DEC-037.md))
  and Qwen tuning use the same search frames; both are judged on the same held-out
  frames.
