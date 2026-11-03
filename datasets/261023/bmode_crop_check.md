# B-mode cropper check on 261023_plain (cropper version 1)

[TASK-032](../../../backlog/tasks/task-032%20-%20Run-the-B-mode-cropper-on-a-dataset-version-polygon-check-reviewed-set-box-table-DEC-017.md), [DEC-017](../../decisions/DEC-017-bmode-cropper.md), [DIS-004](../../discussions/DIS-004-bmode-cropper.md). Exploratory. Aggregates per datasource only; no
images, file names or identifiers. Computed on 2026-11-02 on `261023_plain`
([DEC-018](../../decisions/DEC-018-plain-style-for-local-research.md)), in memory, from `derived/bmode_boxes_df.pkl` (cropper version 1,
built 2026-10-28; spec: `docs/datasets/styles/derived.md` in the code repo,
commit 0888dd3). Per-datasource numbers are stored in the dataset as
`derived/bmode_polygon_check_df.pkl`.

Status: polygon check (AC#1) and DICOM question (AC#4) done. The reviewed set
(AC#2) and accuracy on it (AC#3) wait on the human box review on aws-labelstud
([DEC-025](../../decisions/DEC-025-aws-labelstud-public-https.md)).

## Question

Do the cropper's boxes keep the labelled anatomy inside them, and does the
cropper find both images on frames that hold two? Polygons are a proxy for
"the B-mode image": a box that cuts polygons is too small or misplaced; a box
that holds them may still be too large (only the review can tell).

## Method

- **Data.** `polygons_df` (129,815 polygons) joined to `taskcrops_df` to get
  pixel positions in the whole file (`add_pos_in_img`); 17,222 polygons
  (13.3%) belong to tasks without a crop row and cannot be placed (known gap,
  `plain.md`). Every image in the box table decoded (0 errors). Each placed
  polygon was assigned to the box that holds most of its points
  (`add_pos_in_box`). 7 polygons with zero area were dropped. n = 112,586
  polygons on 25,888 frames in 68 of 72 datasources.
- **Area outside.** Polygon area outside its box (Sutherland-Hodgman clip to
  the box, shoelace area), summed, divided by total polygon area: an
  area-weighted proportion. Fallback frames get a whole-frame box, so their
  area outside is 0 by construction; the share is also given without them.
- **Two-region frames.** Frames whose old crops in `taskcrops_df` split them
  into two images (`roi_cnt == 2`) and that have polygons in both old crops.
  The old crops are taken as the reference for "two images" (assumption: they
  were set per frame when the tasks were made; not re-checked here). Counted:
  frames given two boxes, one (non-fallback) box, or a fallback box.
- **95% CI.** Per datasource: percentile bootstrap over frames (2,000
  resamples, seed 0). Overall: percentile bootstrap over datasources
  (cluster bootstrap, 2,000 resamples), since frames of one datasource are not
  independent. Two-region shares: Wilson interval per datasource.

## Results

**Overall** (68 datasources, 25,888 frames, 112,586 polygons):

- Polygon area outside the boxes: **0.006** (95% CI 0.003-0.009, bootstrap
  by datasource). Without fallback frames (20,241 frames, 67 datasources):
  0.007 (95% CI 0.004-0.011).
- 249 of 112,586 polygons (0.002) have more than half their area outside.
- 5,647 of 25,888 labelled frames (0.218) are fallback frames.
- Area outside above 0.010 in 9 datasources, above 0.050 in 2 (128 and 47).

**Two-region frames**: 981 old two-image frames, all in datasources 201 and
204; 900 of them have polygons in both old crops.

Table 1. Old two-image frames with polygons in both old crops, by box count
from the cropper (version 1). "Not two boxes" = one box or fallback; 95% CI
by Wilson per datasource. Overall: no CI, since there are only 2
datasources (a pooled Wilson interval, 0.721-0.777, ignores clustering).

| Datasource | Frames (n) | Two boxes | One box | Fallback | Not two boxes | 95% CI |
|---:|---:|---:|---:|---:|---:|---|
| 201 | 719 | 171 | 546 | 2 | 0.762 | 0.730-0.792 |
| 204 | 181 | 54 | 114 | 13 | 0.702 | 0.631-0.764 |
| All | 900 | 225 | 660 | 15 | 0.750 | - |

On those one-box frames, the single box covers both images rather than one:
in datasource 201 the box spans a median 0.789 of the frame width while each
old crop spans 0.402-0.479; in datasource 204, in 66 of 119 one-box frames the
box covers at least 0.9 of both old crops. This is why the polygon area
outside stays small (0.011 and 0.018) in these datasources: the polygons are
inside a box that merges two images.

Table 2. Polygon area outside the cropper's boxes per datasource, sorted by
area outside. Proportions of polygon area; 95% CI by bootstrap over frames
(none when a datasource has one frame). Frames: labelled frames with at least
one placed polygon. Fallback frames have a whole-frame box.

| Datasource | Frames | Polygons | Fallback frames | Area outside | 95% CI | Area outside, non-fallback | Polygons > half outside |
|---:|---:|---:|---:|---:|---|---:|---:|
| 128 | 170 | 782 | 0 | 0.091 | 0.063-0.123 | 0.091 | 62 |
| 47 | 235 | 237 | 191 | 0.058 | 0.019-0.103 | 0.189 | 10 |
| 127 | 39 | 111 | 1 | 0.026 | 0.001-0.059 | 0.027 | 2 |
| 5 | 632 | 1,860 | 5 | 0.025 | 0.019-0.033 | 0.026 | 12 |
| 133 | 150 | 471 | 5 | 0.025 | 0.010-0.044 | 0.026 | 5 |
| 204 | 789 | 3,121 | 54 | 0.018 | 0.013-0.025 | 0.019 | 56 |
| 142 | 55 | 227 | 0 | 0.013 | 0.004-0.025 | 0.013 | 0 |
| 201 | 864 | 5,578 | 31 | 0.011 | 0.008-0.015 | 0.011 | 39 |
| 137 | 69 | 255 | 1 | 0.011 | 0.000-0.029 | 0.011 | 2 |
| 116 | 3,067 | 18,801 | 589 | 0.009 | 0.007-0.011 | 0.011 | 7 |
| 138 | 490 | 2,144 | 23 | 0.008 | 0.004-0.014 | 0.008 | 21 |
| 2 | 1,541 | 11,525 | 274 | 0.008 | 0.006-0.010 | 0.009 | 27 |
| 119 | 1,039 | 2,479 | 189 | 0.008 | 0.004-0.011 | 0.010 | 0 |
| 4 | 230 | 1,530 | 0 | 0.008 | 0.005-0.010 | 0.008 | 0 |
| 7 | 120 | 783 | 0 | 0.007 | 0.004-0.010 | 0.007 | 0 |
| 3 | 732 | 5,297 | 26 | 0.004 | 0.002-0.007 | 0.004 | 3 |
| 121 | 1,866 | 9,833 | 119 | 0.003 | 0.002-0.003 | 0.003 | 0 |
| 126 | 681 | 2,771 | 1 | 0.002 | 0.001-0.005 | 0.002 | 0 |
| 10 | 397 | 2,662 | 0 | 0.002 | 0.001-0.003 | 0.002 | 0 |
| 130 | 143 | 513 | 4 | 0.002 | 0.000-0.005 | 0.002 | 0 |
| 122 | 1,097 | 5,916 | 115 | 0.002 | 0.001-0.002 | 0.002 | 1 |
| 203 | 955 | 3,154 | 13 | 0.002 | 0.001-0.003 | 0.002 | 2 |
| 141 | 28 | 119 | 4 | 0.001 | 0.000-0.004 | 0.002 | 0 |
| 9 | 100 | 504 | 0 | 0.001 | 0.000-0.002 | 0.001 | 0 |
| 145 | 277 | 787 | 5 | 0.001 | 0.000-0.002 | 0.001 | 0 |
| 146 | 127 | 539 | 2 | 0.000 | 0.000-0.001 | 0.001 | 0 |
| 132 | 72 | 278 | 5 | 0.000 | 0.000-0.001 | 0.000 | 0 |
| 155 | 467 | 1,475 | 27 | 0.000 | 0.000-0.001 | 0.000 | 0 |
| 120 | 47 | 215 | 29 | 0.000 | 0.000-0.001 | 0.001 | 0 |
| 113 | 32 | 287 | 0 | 0.000 | 0.000-0.001 | 0.000 | 0 |
| 8 | 100 | 615 | 0 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 11 | 46 | 298 | 26 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 158 | 174 | 711 | 2 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 112 | 330 | 2,683 | 0 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 150 | 166 | 436 | 0 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 114 | 763 | 1,727 | 373 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 115 | 207 | 825 | 0 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 118 | 1,116 | 3,530 | 411 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 124 | 34 | 131 | 0 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 1 | 550 | 2,816 | 0 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 154 | 304 | 936 | 48 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 148 | 314 | 1,214 | 197 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 153 | 193 | 734 | 5 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 140 | 1 | 4 | 0 | 0.000 | - | 0.000 | 0 |
| 135 | 16 | 56 | 0 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 12 | 491 | 561 | 366 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 160 | 146 | 443 | 8 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 161 | 11 | 59 | 0 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 131 | 70 | 245 | 3 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 152 | 45 | 183 | 0 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 202 | 558 | 2,319 | 15 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 6 | 1,075 | 2,936 | 1,068 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 147 | 31 | 89 | 6 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 50 | 153 | 154 | 116 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 13 | 769 | 779 | 705 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 159 | 21 | 88 | 7 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 123 | 122 | 619 | 0 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 129 | 315 | 1,135 | 268 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 144 | 41 | 133 | 0 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 151 | 8 | 17 | 0 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 157 | 5 | 17 | 5 | 0.000 | 0.000-0.000 | - | 0 |
| 49 | 218 | 223 | 92 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 48 | 234 | 234 | 0 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 14 | 500 | 502 | 23 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 156 | 168 | 684 | 166 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 51 | 49 | 51 | 21 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 149 | 32 | 143 | 3 | 0.000 | 0.000-0.000 | 0.000 | 0 |
| 143 | 1 | 2 | 0 | 0.000 | - | 0.000 | 0 |

## Analysis

- **Boxes rarely cut labelled anatomy.** 0.6% of polygon area falls outside
  the boxes overall. Two datasources stand out: 128 (0.091, 62 polygons more
  than half outside, no fallback: boxes too tight or on the wrong region) and
  47 (0.058; 0.189 on its 44 non-fallback frames, while 191 of its 235
  labelled frames fall back). 5, 127 and 133 are near 0.025.
- **Two-image frames are mostly merged into one box.** On the only two
  datasources with two-image frames, 0.750 of the frames with polygons in both
  images got one box (or fallback), not two. The cropper's valley split
  (`valley`, `split_min_part`) does not separate these layouts. This is the
  main failure found here.
- **Fallback is common** (0.218 of labelled frames, 0.228 of all images).
  Fallback hides cropper errors from this check (area outside is 0 by
  construction), so these numbers are a lower bound on cut anatomy. Several
  datasources are almost all fallback (6: 1,068 of 1,075; 13: 705 of 769;
  156: 166 of 168; 129, 47, 50, 12 and 157 above 0.7).
- **Not measured here:** boxes that are too large (the check rewards them),
  and frames without polygons. Both need the reviewed set.

## Limitations

- Polygons cover only part of the B-mode image, so "inside" is a necessary,
  not a sufficient, condition for a correct box.
- 13.3% of polygons cannot be placed (no crop row); 4 of 72 datasources have
  no placed polygon.
- The two-image reference is the old crops, available only for datasources
  201 and 204; two-image layouts elsewhere are not detected by this check.
- Exploratory; thresholds and parameters were not tuned on these numbers.

## DICOM region tags (DIS-004 open question)

None of the 72 datasources keeps DICOM region tags in the data available on
machine01. Checked 2026-11-02 over every file under the data root (88,451
files): no `.dcm` / `.dicom` file, no `DICOMDIR`, no file with the DICOM
preamble (`DICM` at byte 128). The images of `261023_plain` (29,468: PNG, JPEG
and BMP) carry no embedded metadata or EXIF and no text mentioning DICOM or
the ultrasound region sequence. Whether original DICOM files still exist at
the sources (outside this machine) cannot be told from this data: a question
for the user.

## Conclusion and next steps

- Polygon containment is good overall (0.006, 95% CI 0.003-0.009), with
  follow-up needed for datasources 128 and 47.
- Splitting two-image frames fails on most of them (0.750 not split): a
  parameter fix or a learned model is needed before training uses two-image
  datasources 201 and 204. To be confirmed on the reviewed set (AC#3).
- Next (after the human review): reviewed set as the regression set (AC#2),
  IoU and `roi_cnt` accuracy per datasource (AC#3), list of failing
  datasources.
