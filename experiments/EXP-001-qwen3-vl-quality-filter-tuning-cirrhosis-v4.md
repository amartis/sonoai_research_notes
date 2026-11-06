---
id: EXP-001
title: Qwen3-VL quality filter for the cirrhosis v4 candidates, prompt tuning on the search part (no usable filter)
status: done
created: 2026-11-05
from: [DEC-044]
related: [DEC-046, DEC-035, DEC-042, DEC-037]
---
# EXP-001: Qwen3-VL quality filter for the cirrhosis v4 candidates, prompt tuning on the search part

- Date: 2026-11-05
- Board task: [TASK-086](../../backlog/tasks/task-086%20-%20Qwen3-VL-quality-filter-for-the-cirrhosis-candidates-tune-on-the-search-part-accept-on-held-out-datasources-at-most-2-of-known-good-flagged-run-on-all-candidates-EXP-record-DEC-044.md) (Qwen3-VL quality filter for the cirrhosis candidates)
- Code commit: `dcf3d89` (branch `claude/exp-t086-qwen-quality`, synced to the GPU box before the runs;
  the run tables record the code version as `unknown`)
- Config: none in `configs/experiments/`; `sonoai-label` AI annotator, question `quality` (`sonoai.labeling.ai_annotator`)
- Runs (common box, project `task-032-bmode-boxes`, crop list `cirr-v4-q1`):
  `q-tune-b1` (run folder `20261105-111339`), `q-tune-b2` (run folder `20261105-121759`)
- Data: dataset version 261023 (enc1 store read in memory on the GPU box; aggregate tables on
  machine01), 128 px minimum crop side table of [TASK-085](../../backlog/tasks/task-085%20-%20Cirrhosis-candidate-samples-on-261023_plain-counts-per-filter-step-and-the-size-report-the-user-picks-the-minimum-crop-side-DEC-044.md); search part of the
  datasource split ([DEC-037](../decisions/DEC-037-cropper-v2-and-second-review-project.md), as used in [DEC-042](../decisions/DEC-042-qwen-tuning-and-comparison-on-the-users-v1-review.md)): 49 search and 21 held-out datasources

Writing standard: [docs/writing.md](../../docs/writing.md) ([DEC-021](../decisions/DEC-021-communication-and-research-writing-standards.md)).

## Question / hypothesis

Exploratory. Can a few-shot prompt make Qwen3-VL-8B-Instruct flag poor-quality crops among
the cirrhosis candidates while it flags at most 2% of known-good crops
([DEC-044](../decisions/DEC-044-cirrhosis-sample-set-quality-filter-and-split.md) rule 6)?
Only the tuning step on the search part ran; the acceptance check on the held-out part did not
run (see Conclusion).

## Setup

- **Model:** Qwen/Qwen3-VL-8B-Instruct, revision `0c351dd01ed8`, 4-bit NF4 (bitsandbytes, double
  quantisation, bfloat16 compute), on the GPU box ([DEC-035](../decisions/DEC-035-qwen3-vl-second-annotator-on-gpu-box.md)). Greedy decoding
  (`do_sample` false), at most 64 new tokens. Reply: JSON with a verdict (good or bad) and one
  reason (none, dark, blurred, low_resolution, paper_scan, unusual_device, marks, other).
- **Prompts:**
  - *default* (B1, `QUALITY_PROMPT` in the code, prompt hash `e9d106256d8b` with the examples):
    answer bad if the crop is too dark, blurred, low-resolution, a photo or scan of paper, from an
    unusual device, or covered in marks.
  - *lenient b2* (B2, prompt hash `1eacca066cd7` with the examples): most crops are normal; answer
    bad only for a clear defect; small or slightly soft pictures and ordinary on-screen text or
    calipers are normal; when unsure, answer good.
- **Few-shot examples q1:** 8 crops (4 known-good, 4 known-bad: 3 with reason other,
  1 low_resolution), one per datasource, all from the search part, drawn with seed 0 without
  viewing images. Same examples in both runs.
- **Reference standard:** from the user's review "[TASK-032](../../backlog/tasks/task-032%20-%20Run-the-B-mode-cropper-on-a-dataset-version-polygon-check-reviewed-set-box-table-DEC-017.md) B-mode boxes v1" in the local Label
  Studio. Known-good: frames the user finished without skipping. Known-bad: crops with a
  `quality` choice label and frames the user skipped. One reviewer (the user); no second reader.
- **Crops judged (both runs, same 597 crops):** all 297 known-good crops of the search part
  (38 datasources) and 300 of the 1,303 known-bad crops of the search part, drawn with seed 0
  (20 datasources). The 8 example crops were left out.
- **Metric:** share of crops flagged (verdict bad) per known class. Unparsed replies count as
  flagged (the user's choice, 2026-11-05); there were none in either run. 95% CI: percentile
  cluster bootstrap over datasources, 2,000 resamples, seed 0 (`ai_annotator.quality_score`,
  the DEC-042 method).
- **Time:** about 58 min (B1) and 59 min (B2) on the GPU box, about 6 s per crop.

## Results

Table 1. Share of search-part crops flagged by each prompt. n is the number of crops; ds is the
number of datasources; CI is the 95% percentile bootstrap over datasources. Target: at most
0.020 of known-good flagged.

| Run | Prompt | Known class | Flagged / n | Share flagged (95% CI) | Datasources |
|---|---|---|---|---|---|
| q-tune-b1 | default | known-good | 67 / 297 | 0.226 (0.131-0.329) | 38 |
| q-tune-b1 | default | known-bad | 175 / 300 | 0.583 (0.174-0.858) | 20 |
| q-tune-b2 | lenient b2 | known-good | 0 / 297 | 0.000 (0.000-0.000) | 38 |
| q-tune-b2 | lenient b2 | known-bad | 1 / 300 | 0.003 (0.000-0.023) | 20 |

Table 2. Reasons given for flagged crops (verdict bad), counts per run and known class.

| Run | Known class | low_resolution | dark | marks | blurred | other |
|---|---|---|---|---|---|---|
| q-tune-b1 | known-good (67 flagged) | 49 | 3 | 9 | 1 | 5 |
| q-tune-b1 | known-bad (175 flagged) | 142 | 24 | 2 | 0 | 7 |
| q-tune-b2 | known-bad (1 flagged) | 0 | 0 | 0 | 0 | 1 |

No crop was flagged as paper_scan or unusual_device in either run.

Table 3. q-tune-b1 (default prompt): share flagged by shorter crop side. Same CI method as
Table 1; a CI with one or two datasources is close to a point and is not reliable. Median
shorter side: 490 px (known-good), 520 px (known-bad).

| Shorter crop side, px | Known-good: flagged / n | Known-good: share (95% CI) | ds | Known-bad: flagged / n | Known-bad: share (95% CI) | ds |
|---|---|---|---|---|---|---|
| 128-199 | 5 / 8 | 0.625 (0.000-0.714) | 2 | 0 / 1 | 0.000 (0.000-0.000) | 1 |
| 200-299 | 8 / 19 | 0.421 (0.000-0.533) | 4 | 5 / 10 | 0.500 (0.500-0.500) | 1 |
| 300-399 | 5 / 21 | 0.238 (0.000-0.500) | 10 | 6 / 6 | 1.000 (1.000-1.000) | 3 |
| 400 or more | 49 / 249 | 0.197 (0.103-0.304) | 35 | 164 / 283 | 0.580 (0.112-0.870) | 17 |

The lenient prompt flagged no known-good crop in any size band and 1 known-bad crop (400 px or more).

## Analysis

- **Default prompt (B1):** it separated the classes in part (0.583 of known-bad against 0.226 of
  known-good flagged), but its known-good share is about 11 times the 0.020 target, and the lower
  CI bound (0.131) is far above it. Most known-good flags gave reason low_resolution (49 of 67),
  and the known-good share fell as crops got larger (0.625 at 128-199 px to 0.197 at 400 px or
  more; few crops and datasources below 400 px). The model reads small crops as low resolution.
  Even at 400 px or more the known-good share (0.197) stays far above 0.020.
- **Lenient prompt (B2):** it met the known-good target (0/297) but flagged 1 of 300 known-bad,
  so it removes almost nothing: the shift from B1 moved the model to answer good on nearly every crop.
- **Between the two:** with greedy decoding the model gives a verdict, not a score, so there was
  no threshold to tune between "flags a fifth of good crops" and "flags nothing". A further prompt
  variant would be another full GPU run (about one hour) without a clear way to aim it.
- The known-bad CI is wide (0.174-0.858) because the flag share differs much between the
  20 datasources.

## Limitations

- Exploratory, tuning only: the search part was used to write the prompts, so these shares are
  optimistic; no held-out check ran.
- Two prompts, one example set, one model at one quantisation; no repeat runs (greedy decoding is
  deterministic for a fixed input).
- The reference standard is one reviewer's choices in a box review, not a quality grading; some
  known-bad crops were skipped for reasons other than image quality, so the known-bad share is
  not a sensitivity for "poor quality".
- Known-bad crops were a seeded sample (300 of 1,303) from 20 of 25 search datasources.
- Raw model replies were not stored (only verdict and reason); importing B2 replaced the B1 rows
  of the same crops in `derived/` on machine01; the B1 run table stays in the common box.
- Size bands below 400 px have few crops and datasources.

## Conclusion and next steps

No prompt gave a usable filter: the default prompt flagged 0.226 of known-good crops (target at
most 0.020), and the lenient prompt flagged almost nothing (0/297 known-good, 1/300 known-bad).
On 2026-11-05 the user dropped the Qwen3-VL quality step for `lseg_cirrhosis_v4`
([DEC-046](../decisions/DEC-046-cirrhosis-v4-drops-the-qwen3-vl-quality-step.md)); bad crops are left out only by choice labels and user skips (DEC-044 rule 4).
The held-out acceptance check and the run on all candidates were not done and are void under
DEC-046. If the filter comes back for a later version (new DEC), these results suggest giving the
model the crop size or excluding low_resolution as a reason, and storing raw replies.

## Reporting checklist

Drawn from CLAIM 2024, STARD-AI and TRIPOD+AI (details in `docs/writing.md`).

- [x] Data: datasources, inclusion and exclusion, counts per class per split (search part only; Setup)
- [x] Split by datasource; no overlap between splits; held-out part not used (no test step ran)
- [x] Reference standard: what the labels mean, who labelled (one reviewer, the user); disagreements N/A
- [x] Model and settings: model, revision, quantisation, prompts, examples, decoding, seeds
- [x] Metrics with 95% CI (method named); baseline N/A (first prompts), compared with the 0.020 target
- [x] Operating point: N/A (verdict, no threshold); prompts were chosen on the search part only
- [x] Subgroups: by crop size (Table 3); per-datasource rates not reported (few crops per datasource)
- [x] Limitations, and the result is exploratory
