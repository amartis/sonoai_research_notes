---
id: DIS-018
title: Qwen3-VL prompt tuning and comparison use the user's v1 review with the DEC-037 datasource hold-out
status: concluded
created: 2026-11-04
outcomes: [DEC-042]
related: [DEC-035, DEC-037, DIS-009]
---
# DIS-018: Qwen3-VL prompt tuning and comparison use the user's v1 review with the [DEC-037](../decisions/DEC-037-cropper-v2-and-second-review-project.md) datasource hold-out

## Question

[TASK-032.05](../../backlog/tasks/task-032.05%20-%20Run-the-Qwen3-VL-second-annotator-on-the-TASK-032-frames-and-compare-with-the-human-labels-DEC-035.md)
(run the Qwen3-VL second annotator and compare it with the human labels) stopped on
2026-11-03 before any GPU run. [DEC-035](../decisions/DEC-035-qwen3-vl-second-annotator-on-gpu-box.md)
says prompt tuning uses "a fixed 72-frame subset", scored only against the cropper and
the label polygons. No record defines those 72 frames or the score. The number 72 is
most likely the count of datasources in the sample (1,371 frames from 72 datasources,
[DIS-009](DIS-009-claude-as-second-annotator.md)), not a frame list. DEC-035 also names
no human label set for the comparison.

## Options considered

**Tuning frames**
- **One random frame per datasource (72 frames), scored against cropper v1 and the
  polygons** (the reading of DEC-035). Keeps Qwen blind to every human label until the
  freeze. Con: cropper boxes are not ground truth, so tuning pulls Qwen toward copying
  the cropper.
- **The user's labelled frames in the local Label Studio project** (the user's choice).
  Tunes against human boxes. Con: Qwen is no longer blind to the user's labels; tuning
  and testing on the same frames would inflate the result, so a hold-out is needed.

**Score**
- **Mean matched-box IoU against cropper v1**, with guards. Rejected with the frame
  choice above.
- **IoU against the user's boxes**, with guards: polygon area outside the boxes at most
  0.02 and failed frames at most 5%; at most 5 prompt variants (the user's choice). The
  two thresholds are a proposal, not checked against data.

**Hold-out**
- **The DEC-037 datasource split** (seed 0, about 70% of datasources to search, the rest
  held out; `sonoai.data.bmode_tune.split_by_datasource`). Cropper v1, cropper v2 and
  Qwen then share one held-out set. Chosen.
- **A small fixed tuning subset, test on the rest.** Faster per prompt variant on the
  GPU box. Not chosen; GPU time per variant is unmeasured.

**Which human labels**
- **The remote assistant's set on aws-labelstud** (DIS-009's "human annotator"), with
  the user's reviews secondary. Not chosen.
- **The user's local reviews only.** Chosen, and only the v1 project
  ("[TASK-032](../../backlog/tasks/task-032%20-%20Run-the-B-mode-cropper-on-a-dataset-version-polygon-check-reviewed-set-box-table-DEC-017.md) B-mode boxes v1"), submitted frames, skipped frames left out: the same set
  DEC-037 tunes cropper v2 on. The v1 project takes no new labels once the v2 project is
  created, so the set stays fixed.

## Conclusion

[DEC-042](../decisions/DEC-042-qwen-tuning-and-comparison-on-the-users-v1-review.md):
tune and compare against the user's v1 review, split by datasource as in DEC-037. A
small method task adds the scoring code; TASK-032.05 is rewritten to match.

## Open questions

- GPU-box time per prompt variant over the search frames (about 70% of 599 submitted
  frames on 2026-11-03): unmeasured. If it is too slow, a fixed subsample of the search
  frames is the fallback; that would be a new decision.
