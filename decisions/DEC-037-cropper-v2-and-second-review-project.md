---
id: DEC-037
title: Cropper v2 is tuned on the user's v1 review with a datasource hold-out, and prelabels a second project with the unfinished v1 frames
status: accepted
created: 2026-11-03
from: [DIS-013]
related: [DEC-017, DEC-019, DEC-018]
superseded_by:
---
# DEC-037: Cropper v2 is tuned on the user's v1 review with a datasource hold-out, and prelabels a second project with the unfinished v1 frames

## Context

[DIS-013](../discussions/DIS-013-cropper-v2-from-the-users-review.md): the user's review in the local project
"[TASK-032](../../backlog/tasks/task-032%20-%20Run-the-B-mode-cropper-on-a-dataset-version-polygon-check-reviewed-set-box-table-DEC-017.md) B-mode boxes v1" had 599 submitted and 54 skipped frames out of 1,371
on 2026-11-03. The user wants better prelabels for the rest of the labeling.

## Decision

- **Cropper v2**: parameters only (no code change). `version: 2` in
  `configs/data/bmode_crop.yaml`. The v1 values are kept as a frozen copy,
  `configs/data/bmode_crop_v1.yaml`, so that v1 can be rebuilt.
- **Tuning**: on the user's submitted v1 reviews (local target; skipped frames left out).
  Split by datasource: search on the frames of about 70% of datasources (fixed seed).
  Report v1 against v2 on the other 30%: mean IoU of matched boxes, box-count accuracy,
  and the share of fallback boxes, each with n and a 95% CI. v2 is adopted only if it is
  better on the held-out frames and the full-dataset polygon check is not worse (v1:
  polygon area outside boxes 0.006).
- **Box table**: `derived/bmode_boxes_v2_df.pkl` in `261023_plain`.
  `derived/bmode_boxes_df.pkl` stays v1, because the v1 project reads it.
- **Second project**: "TASK-032 B-mode boxes v2", slug `task-032-bmode-boxes-v2`, on the
  local Label Studio. Source: the v2 box table. Result table: `derived/bmode_review_v2_df.pkl`.
  Frames: the v1 project's frame list, minus the frames submitted or skipped in the v1
  local project when v2 is created. The frame list is copied from v1, not resampled.
- The v1 project stays open, but no new labeling goes there after v2 is created.

## Consequences

- Each review row already records the `cropper_version` it was proposed with. The
  regression set therefore mixes v1 and v2 rows. Boxes from the v2 project are
  anchored to v2 proposals, so version comparisons use v1-project frames only.
- Pulling the v1 review needs [TASK-064](../../backlog/tasks/task-064%20-%20sonoai-label-pull-one-result-table-per-target-so-local-and-aws-labelstud-reviews-of-the-same-frames-do-not-overwrite-each-other.md) first (one result table per target); before
  the first pull, check the 25 rows of unrecorded origin in the existing table (TASK-032 note).
- Tasks: [TASK-032.06](../../backlog/tasks/task-032.06%20-%20Cropper-tuning-code-score-boxes-against-reviewed-boxes-datasource-hold-out-search-versioned-box-tables-DEC-037.md), [TASK-032.07](../../backlog/tasks/task-032.07%20-%20Labeling-project-from-another-projects-frame-list-minus-its-finished-frames-status-counts-skipped-as-finished-DEC-037.md) (method), [TASK-032.08](../../backlog/tasks/task-032.08%20-%20Tune-cropper-v2-on-the-users-v1-review-build-its-box-table-and-polygon-check-DEC-037.md), [TASK-032.09](../../backlog/tasks/task-032.09%20-%20Create-the-local-project-TASK-032-B-mode-boxes-v2-with-cropper-v2-prelabels-DEC-037.md) (data).
