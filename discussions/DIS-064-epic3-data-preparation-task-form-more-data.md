---
id: DIS-064
title: Epic 3 data preparation (input size, minimum crop side, resize), task form for overlapping outlines, and more data
status: open
created: 2026-11-26
outcomes: [DEC-109, DEC-110, DEC-111]
related: [DEC-066, DEC-068, DEC-069, DEC-100, DEC-103, DEC-108, DIS-056]
---
# DIS-064: Epic 3 data preparation, task form and more data

## Question

Three points of the epic 3 handoff in [DIS-056](DIS-056-epic3-spot-liver-disease-mission.md) (the
epic 3 mission discussion), taken in the order of
[DEC-100](../decisions/DEC-100-epic3-mission-spot-liver-diseases.md) (the epic 3 mission) rule 7:

1. **Data preparation**, not a point of DEC-100 rule 7 but needed before training: input size,
   minimum crop side, and how a crop is brought to the input size.
2. **More data** (point 8): public sets, the book images of the labeling projects P49 and P52, and
   the request to the authors of Tiyarattanachai 2021.
3. **Task form** (point 9 in the user's order): the output form when outlines of two classes overlap.

The split is already fixed ([DEC-108](../decisions/DEC-108-epic3-split-test-and-validation-by-whole-groups.md),
the epic 3 split by whole datasource groups); its sample file is being built in
[TASK-279](../../backlog/tasks/task-279%20-%20Epic-3-split-on-261023-build-the-table-of-samples-to-split-run-the-feasibility-report-freeze-the-sample-file-with-the-DEC-108-limits-and-its-enc1-copy-dataset-record-per-split-and-class-DEC-108.md)
(the epic 3 split run).

## Facts checked

Five tables of 261023_plain read with the user's ok of 2026-11-26 (strict_v1 presence table on index
v2, sample-label index v2, taskcrops table, polygon table, flag table; read only, in memory,
aggregates; no table written). Spot classes: `hepatoma`, `hemangioma`, `hepatic_cyst`,
`hepatic_stone` (DEC-100 rule 2). Universe: the 16,176 samples with a known strict_v1 state for at
least one spot class, in 55 datasource groups (DEC-108 rule 1 counted 57 groups; not reconciled).
Polygons were drawn on a 256 x 256 grid of the crop (polygon points are in percent of the crop).

| Class | Positives | Lesion share of the crop, median (P10) | Median width at input 224 / 384 / 512 px | Median width in source pixels |
|---|---:|---|---|---:|
| `hepatoma` | 1,417 | 2.98% (0.65%) | 38 / 66 / 85 | 115 |
| `hemangioma` | 204 | 0.66% (0.23%) | 18 / 31 / 39 | 49 |
| `hepatic_cyst` | 116 | 0.68% (0.18%) | 18 / 31 / 40 | 49 |
| `hepatic_stone` | 298 | 0.14% (0.07%) | 8.5 / 15 / 19 | 23 |

Table 1. Lesion size. Width = square root of the lesion's pixel area after the crop is stretched to
the input, capped at its source pixels (a stretched input holds no more detail than the source).
At 224 px a tenth of the stones are 6 px wide or less. Ascites: 122 positives under the label
`ascites` in this count; [DEC-102](../decisions/DEC-102-quality-skips-other-organ-projects-index-v2.md) (quality skips of other organs' projects) gives 136; not reconciled.

| Minimum crop side | Samples dropped | Positives dropped: hepatoma / hemangioma / cyst / stone | Datasource groups emptied |
|---|---:|---|---:|
| 224 px | 148 (0.9%) | 4 / 0 / 1 / 1 | 1 |
| 384 px | 1,734 | 84 / 49 / 14 / 38 | 3 |
| 512 px | 5,891 (36%) | 391 / 99 / 56 / 175 | 16 |

Table 2. Samples lost per minimum crop side (shorter side of the crop box in source pixels; median
720, 5th percentile 224). Crop width over height: quartiles 0.74 and 1.33.

| Pair of classes on one sample | Overlap below 10% of the smaller outline | 10% to 50% | 50% to 90% | 90% or more (nested) |
|---|---:|---:|---:|---:|
| `hepatic_stone` inside `hepatoma` | 0 | 3 | 3 | 5 |
| `hepatic_stone` inside `hemangioma` | 0 | 0 | 2 | 0 |
| `hepatic_stone` and `hepatic_cyst` | 0 | 1 | 0 | 0 |
| `hepatoma`, `hemangioma`, `hepatic_cyst` with each other | 5 | 0 | 0 | 0 |
| `ascites` and `hepatoma` | 1 | 0 | 0 | 0 |

Table 3. Every sample-class pair whose outlines overlap at all (20; 18 with both classes positive,
2 with one unknown). Serious overlap is always a stone inside a mass (13, 4% of the stone
positives); the masses only touch at their edges. 88 samples have two or more spot classes positive.

- Positives without a polygon: 3 pairs in all (hemangioma 1, cyst 2).
- Book images (labeling projects with no crop rows): P49 gives image-level choices on 894 tasks
  with a spot class (hepatoma 666, hemangioma 102, cyst 113, stone 32); P52 outlines few (1,271
  tasks visited; hepatoma 14). P1 (steatosis scoring) has hepatoma 316, hemangioma 69 and cyst 37
  choices but its tasks cannot be placed on samples (no crop rows, no task-order link).
- Public liver sets: AUL (735 images, licence unclear) and TCIA B-mode-and-CEUS-Liver (120
  patients, CC BY 4.0), as listed in the journal note
  [2026-11-18-public-datasets-claude.md](../journal/2026/2026-11-18-public-datasets-claude.md);
  whether their labels map to the four classes was not checked.

## Options considered

| # | Question | Analyst's recommendation | Chosen by the user (2026-11-26) |
|---|---|---|---|
| 1 | Input size, minimum crop side, resize | 512 x 512, no minimum, stretch as in Epic 1 | 512 x 512 and no minimum; **two resize modes compared by training**: stretch, and fit-scale (aspect kept, the longer side fills the input, the rest padded); padding as [DEC-068](../decisions/DEC-068-us-mild-v2-zero-image-and-background-outside-the-crop.md) (image 0, target background) |
| 2 | Task form | One sigmoid per class with unknown masked, plus an image-level head | **The user's plan**: one softmax over background, the four spot classes and ascites with the Epic 1 allowed-class sets; the stone takes the overlap with a mass; **a sigmoid comparison run later** |
| 3 | More data | First runs on 261023 only; book images and public sets checked beside them; the analyst drafts the author request | No book images; public sets postponed (maybe epic 4); the author request is already sent |

Table 4. The three questions as put and answered.

**Comparison asked by the user for question 2** (example: one 512 x 512 crop, hepatoma positive,
a stone fully inside it, hemangioma unknown, cyst and ascites negative):

| Criterion | Allowed-class sets, one softmax (the user's plan) | One sigmoid per class, unknown masked (the analyst's first recommendation) |
|---|---|---|
| Masses exclusive for one lesion | Built in: the classes compete per pixel | Not built in: one lesion can score high as hepatoma and hemangioma |
| Unknown class | Allowed only outside the positive outlines, so the unknown hemangioma is still ruled out inside the hepatoma | The whole channel is masked on the sample |
| Stone inside a mass | Weak as in Epic 1: the overlap holds {hepatoma, stone}, the loss is met by hepatoma alone, and the argmax can drop the stone | Exact: both channels are 1 there |
| Image-level score | From the pixel probabilities per class | Its own head |
| Code | Label-set losses and evaluation exist from Epic 1 | New masked loss and evaluation |

Table 5. The two task forms. The weak row of the user's plan is fixed by giving the overlap to the
stone (DEC-110 rule 3): hepatoma then loses about 5% of its outline as a target on 13 samples, and a
stone predicted inside a mass outline is counted for that mass at scoring. The image-level head
was argued for the book images; without them, and with 3 positives without a polygon, it is not needed.

## Conclusion

[DEC-109](../decisions/DEC-109-epic3-input-512-no-minimum-side-two-resize-modes.md) (data
preparation), [DEC-110](../decisions/DEC-110-epic3-task-form-allowed-class-sets-stone-takes-the-overlap.md)
(task form) and [DEC-111](../decisions/DEC-111-epic3-more-data-261023-only.md) (more data), all
`proposed` until the user confirms the text. Board tasks: see the DECs.

No new term: "stretch" and "fit-scale" are said in words; the recipe field values are code names.

## Open questions

- How the image-level score per class is taken from the pixel probabilities (maximum, mean of the
  top pixels, or predicted area), and the scoring of a stone inside a mass outline: the metrics
  point, with the cirrhosis bar of [DEC-103](../decisions/DEC-103-epic3-negatives-and-contested-labels.md)
  (epic 3 negatives and contested labels) rule 3.
- Which resize mode wins, and which recipe the sigmoid comparison run uses: after the first runs.
