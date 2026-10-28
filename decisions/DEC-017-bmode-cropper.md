---
id: DEC-017
title: Classical B-mode box cropper, checked against label polygons and a reviewed set
status: accepted
created: 2026-10-28
from: [DIS-004]
related: [DEC-012]
superseded_by:
---
# DEC-017: Classical B-mode box cropper, checked against label polygons and a reviewed set

## Context

Frames hold one or two B-mode images among burned-in meta information,
sometimes with colour Doppler. Training and inference both need the B-mode
area. The `taskcrops_df` boxes are unreliable (many cover the whole file), and
no ready-made tool handles mixed-vendor screenshots with two-image layouts
(DIS-004).

## Decision

- **What**: a deterministic function in `src/sonoai/` (e.g.
  `sonoai.data.bmode_crop`) that takes one decoded frame (in memory) and
  returns 0-2 boxes: `left, top, right, bottom` in image pixels, `roi_cnt`,
  `roi_i`, a confidence, and a `has_color_doppler` flag. Boxes are tight
  around the B-mode image, including colour Doppler overlays inside it.
  The same function serves training preprocessing and inference.
- **How**: classical, NumPy/OpenCV, CPU only, BUSClean-like:
  1. grayscale mask (channels nearly equal, tolerant of JPEG noise);
  2. speckle texture mask (local standard deviation or entropy);
  3. removal of thin bright strokes (text, calipers, ticks), closing and hole
     filling (dark structures and colour Doppler inside the image stay in);
  4. connected components, keeping at most two that pass area, aspect and
     position checks; a profile-valley test splits two-image layouts;
  5. rejection of spectral Doppler and M-mode strips (streaks along the time
     axis, a straight baseline, strip shape) and of colour bars.

  Parameters live in a versioned config; every output records the cropper
  version. Low confidence falls back to the whole frame with a flag, so
  inference never drops a frame silently.
- **Not now**: fan/sector masks, detecting non-B-mode panels as their own
  type, a learned model (only if the classical cropper fails on whole
  datasources).
- **Output store**: a table of boxes per dataset version, next to (not
  replacing) `taskcrops_df`. Label polygons are placed through image pixels
  (`add_pos_in_img`) into the new boxes. No crops are written to disk.
  Amended 2026-10-28 (DEC-018): built locally from the plain dataset, in
  `<version>_plain/derived/`.
- **Checks**:
  - synthetic tests (generated speckle fans, text headers, colour Doppler
    patches, colour bars, one- and two-image layouts, spectral strips);
  - polygon containment on labelled frames: share of polygon area outside
    the boxes, and frames whose polygons fall in two regions with one box;
  - a review set of about 20 frames per datasource, including two-image and
    Doppler frames: the cropper proposes boxes and the user reviews and
    corrects them. Reviewed boxes become the regression set for later
    cropper versions.
- **DICOM**: where a source keeps DICOM, its ultrasound region tags
  (0018,6011) are used instead, or as ground truth.

All reported results are aggregates per datasource; no frames, names or
identifiers in notes or tasks.

## Consequences

- One code path crops for training and inference; changing it means a new
  cropper version and a re-run of the checks.
- Training data gains a box table per dataset version, specified in the
  style docs (`docs/datasets/styles/`, DEC-012).
- The review needs the user's time (about 20 frames per datasource), viewed
  only in the user's own session, as the data rules require.
- Board tasks: TASK-031, a `method` task (cropper and synthetic tests, touches
  `src/sonoai/data/`, `tests/`, `configs/`) and a `data` task depending on it
  (TASK-032: run, polygon check, review set, box table).
