---
id: DIS-004
title: B-mode cropper for ultrasound frames
status: concluded
created: 2026-10-28
outcomes: [DEC-017]
related: [DEC-012]
---
# DIS-004: B-mode cropper for ultrasound frames

## Question

Ultrasound frames usually hold one or two B-mode images, sometimes with a
colour Doppler overlay, surrounded by burned-in meta information (patient
details, device, settings, scales, colour bars). We want a simple cropper
that finds the B-mode image(s) in a frame, for training preprocessing and
for inference on new frames.

The existing crop boxes in `taskcrops_df` (`left/right/top/bottom`,
`roi_cnt`, `roi_i`) cannot be used as ground truth: many cover the whole file
regardless of where the B-mode area is (user, 2026-10-28).

## Options considered

- **Output**: (A) boxes; (B) fan/sector masks. A for now: a box is enough
  for training; masks can come later.
- **Non-B-mode panels** (spectral Doppler, M-mode, elastography): ignore
  them or detect them as their own region type. Ignored for now, but the
  cropper must still reject them: a spectral trace or M-mode strip is
  grayscale and textured and would otherwise pass as B-mode.
- **Ready-made tools** (surveyed 2026-10-28):
  - DICOM *Sequence of Ultrasound Regions* (0018,6011) gives region boxes
    and types (tissue, colour flow, spectral, M-mode) exactly, but only for
    sources kept as DICOM; exported images lose it.
  - BUSClean (hawaii-ai/bus-cleaning, arXiv 2407.11316): open-source breast
    ultrasound preprocessing; crops the scan area by thresholding against
    the background mode, morphology and the largest connected component.
    Single-image breast DICOM only; no two-image layouts or UI handling.
  - SlicerUltrasound Anonymize module (3D Slicer): interactive fan masking
    from 3-4 clicked corners, an AI fan detector in development. A GUI tool,
    not a library.
  - Research methods (fan delineation, beam template matching) and generic
    zero-shot detectors/segmenters (Grounding DINO, SAM): no maintained
    ultrasound tool; the generic models are heavy and GPU-bound.

  None covers mixed-vendor screenshots with two-image layouts and colour
  Doppler, so we write our own, BUSClean-like, classical cropper.
- **Method**: (A) classical heuristic (grayscale + speckle texture masks,
  text/stroke removal, hole filling, connected components, layout split);
  (B) a small learned segmenter or detector. A first; B only for the cases A
  fails on, measured per datasource.
- **Ground truth**: (A) only a consistency check against label polygons
  (a labelled structure must lie inside a B-mode box); (B) plus a hand-checked
  review set. B chosen: about 20 frames per datasource, the algorithm proposes
  boxes and the user reviews them.

## Conclusion

Agreed with the user on 2026-10-28; carried by [DEC-017](../decisions/DEC-017-bmode-cropper.md) (accepted
2026-10-28). Board tasks: [TASK-031](../../backlog/tasks/task-031%20-%20B-mode-box-cropper-and-batch-command-DEC-017.md) (`method`: the cropper, batch command and
synthetic tests) and [TASK-032](../../backlog/tasks/task-032%20-%20Run-the-B-mode-cropper-on-a-dataset-version-polygon-check-reviewed-set-box-table-DEC-017.md) (`data`, depends on TASK-031: run it, polygon
check, reviewed set, box table).

## Open questions

- Do any datasources still have the original DICOM files? If so, their
  region tags can be used directly or as extra ground truth.
- Where the box table lives in a dataset version (a new table in the style
  docs, `docs/datasets/styles/`), settled in the `data` task.
