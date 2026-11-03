---
id: DIS-013
title: Tune the B-mode cropper on the user's TASK-032 review and prelabel the remaining frames with it
status: concluded
created: 2026-11-03
outcomes: [DEC-037]
related: [DEC-017, DEC-019, DEC-035]
---
# DIS-013: Tune the B-mode cropper on the user's [TASK-032](../../backlog/tasks/task-032%20-%20Run-the-B-mode-cropper-on-a-dataset-version-polygon-check-reviewed-set-box-table-DEC-017.md) review and prelabel the remaining frames with it

## Question

The user is reviewing the cropper's boxes (cropper v1, [DEC-017](../decisions/DEC-017-bmode-cropper.md))
in the local Label Studio project "TASK-032 B-mode boxes v1" (1,371 frames, 72 datasources).
On 2026-11-03 the project had 599 frames submitted and 54 skipped. The user asked
whether to use these reviews now to tune the cropper's parameters, and then to put
the remaining frames in a second project whose prelabels come from the tuned cropper.
Better prelabels mean fewer corrections for the rest of the labeling.

Known weak points of v1 (TASK-032 polygon check, 261023_plain): fallback (whole-frame
box) on 0.218 of labelled frames; of the two-image frames, 0.750 got one box or the
fallback (n = 900, 2 datasources).

## Options considered

- **Names**: a new cropper version `2` with its own box table file, versus rebuilding
  the v1 table in place. Rebuilding in place breaks the v1 project, whose pull reads
  the v1 table as its proposals.
- **Frames of the second project**: only the v1 frames not yet submitted or skipped,
  versus all 1,371 frames again. Doing all again repeats about 650 frames of work.
  The frame list must be copied from the v1 project. The sampler picks frames
  from the box table, so a v2 table would pick a different sample.
- **Tuning**: on all reviewed frames, versus holding out about 30% of datasources to
  report v1 against v2 honestly. About 600 frames over 72 datasources overfit easily.
  Parameters only, versus code changes as well.

## Conclusion

The user agreed to all the recommendations ([DEC-037](../decisions/DEC-037-cropper-v2-and-second-review-project.md)):
cropper v2 is a parameter-only change, tuned with a datasource hold-out.
It gets its own box table. A second local project, "TASK-032 B-mode boxes v2", holds the
v1 frames that are not finished when it is created.
Board tasks: [TASK-032.06](../../backlog/tasks/task-032.06%20-%20Cropper-tuning-code-score-boxes-against-reviewed-boxes-datasource-hold-out-search-versioned-box-tables-DEC-037.md) (tuning code), [TASK-032.07](../../backlog/tasks/task-032.07%20-%20Labeling-project-from-another-projects-frame-list-minus-its-finished-frames-status-counts-skipped-as-finished-DEC-037.md) (project from another project's frame
list), [TASK-032.08](../../backlog/tasks/task-032.08%20-%20Tune-cropper-v2-on-the-users-v1-review-build-its-box-table-and-polygon-check-DEC-037.md) (tune and build v2, real data), [TASK-032.09](../../backlog/tasks/task-032.09%20-%20Create-the-local-project-TASK-032-B-mode-boxes-v2-with-cropper-v2-prelabels-DEC-037.md) (create the v2 project).
They depend on [TASK-064](../../backlog/tasks/task-064%20-%20sonoai-label-pull-one-result-table-per-target-so-local-and-aws-labelstud-reviews-of-the-same-frames-do-not-overwrite-each-other.md) (one result table per target).

Found in passing: `sonoai-label status` reports "to go" as total minus submitted, so
skipped frames are counted as still to go (772 shown, 718 actually left on
2026-11-03). Fixed in TASK-032.07.

## Open questions

- Boxes the user draws in the v2 project start from v2 proposals. So those boxes
  are anchored to v2, and the accuracy measured on them flatters v2. Version
  comparisons should use the v1-project frames (TASK-032 AC#3). Which frames form
  the regression set is still open in TASK-032.
- If parameter tuning cannot fix the two-image split, a code change (cropper v3)
  goes to Triage.
