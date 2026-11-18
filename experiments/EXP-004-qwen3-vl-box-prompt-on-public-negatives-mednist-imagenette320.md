---
id: EXP-004
title: Qwen3-VL box prompt (DEC-035, unchanged) on public negatives, MedNIST and Imagenette-320
status: done
created: 2026-11-18
from: [DIS-031]
related: [DEC-035, DEC-062, DEC-063]
---
# EXP-004: Qwen3-VL box prompt on public negatives (MedNIST, Imagenette-320)

Board task: [TASK-154](../../backlog/tasks/task-154%20-%20Run-the-Qwen3-VL-box-prompt-on-100-MedNIST-and-Imagenette-320-images-per-class-on-the-GPU-box-EXP-record-with-the-share-of-wrong-boxes-per-class-DIS-031.md) (this run and record); command from [TASK-153](../../backlog/tasks/task-153%20-%20Qwen3-VL-box-prompt-on-public-negatives-sonoai-label-command-that-prompts-a-seeded-sample-of-MedNIST-and-Imagenette-320-and-writes-per-class-aggregates-with-Wilson-95-intervals-synthetic-tests-DIS-031.md). Discussion: [DIS-031](../discussions/DIS-031-qwen-box-prompt-on-public-negatives.md).
Writing standard: [docs/writing.md](../../docs/writing.md).

- Date: 2026-11-18 (run 09:40 to 10:03 local time of the GPU box)
- Run name: `exp-t154-qwen-negatives-r2` on the GPU box (an earlier start, `exp-t154-qwen-negatives`, failed at once: the `sonoai-label` entry point is not installed on the box; no image was read; r2 calls the same code through `python -c`). Common-box run folder `20261118-014225`.
- Code: master `78e68c8` plus the TASK-153 command; the box copy has no `.git`, so the table holds `code-unknown`.
- Model: Qwen3-VL-8B-Instruct, revision `0c351dd01ed8`, 4-bit nf4, greedy, max 256 new tokens.
- Prompt hash (sha256): `7ead0c7ac18686cb97e5b85be26d8c736c27f6b0b473cde76c01612de0f78970` (the [DEC-035](../decisions/DEC-035-qwen3-vl-second-annotator-on-gpu-box.md) box prompt, unchanged; the digest of the drawn files is `625175fe...`).
- Data: public only ([DEC-063](../decisions/DEC-063-public-non-patient-datasets-root.md)). MedNIST (6 classes) and Imagenette-320 val (10 classes), 100 images per class drawn with seed 0, RGB as stored: n = 1,600. No shortfall.

## Question

Exploratory check, no tuning. [DEC-062](../decisions/DEC-062-bmode-detector-training-box-source-and-negatives.md) expects negatives (images with no B-mode image) to get no box, so the model should answer "No B-mode image". Does the unchanged prompt do that? No threshold was set by the agent.

## Results

Table 1. Replies of the unchanged box prompt on public negatives. n = images; boxes = reply with at least one box; no_bmode = reply "No B-mode image"; unparsed = reply not understood; wrong = boxes + unparsed; share wrong with 95% Wilson interval; time = model seconds per image (one run, so no interval on time).

| Dataset | Class | n | boxes | no_bmode | unparsed | Share wrong [95% CI] | s/image |
|---|---|---|---|---|---|---|---|
| MedNIST | AbdomenCT | 100 | 7 | 93 | 0 | 0.070 [0.034, 0.137] | 0.59 |
| MedNIST | BreastMRI | 100 | 55 | 45 | 0 | 0.550 [0.452, 0.644] | 1.29 |
| MedNIST | CXR | 100 | 0 | 100 | 0 | 0.000 [0.000, 0.037] | 0.50 |
| MedNIST | ChestCT | 100 | 60 | 40 | 0 | 0.600 [0.502, 0.691] | 1.39 |
| MedNIST | Hand | 100 | 1 | 99 | 0 | 0.010 [0.002, 0.054] | 0.52 |
| MedNIST | HeadCT | 100 | 20 | 80 | 0 | 0.200 [0.133, 0.289] | 0.81 |
| MedNIST | all | 600 | 143 | 457 | 0 | 0.238 [0.206, 0.274] | 0.85 |
| Imagenette-320 | 9 classes (WordNet ids n01440764, n02102040, n02979186, n03000684, n03028079, n03394916, n03417042, n03425413, n03888257) | 100 each | 0 | 100 each | 0 | 0.000 [0.000, 0.037] each | 0.60 to 0.65 |
| Imagenette-320 | n03445777 | 100 | 1 | 99 | 0 | 0.010 [0.002, 0.054] | 0.62 |
| Imagenette-320 | all | 1,000 | 1 | 999 | 0 | 0.001 [0.000, 0.006] | 0.61 |
| Both | all | 1,600 | 144 | 1,456 | 0 | 0.090 [0.077, 0.105] | not computed |

The intervals treat images as independent. Images of one class share a source, so the intervals are likely too narrow for the dataset-level rows. The both-datasets row is my computation from the table's counts (Wilson formula); the rest is the run's own output.

## Analysis

- Imagenette-320 (photographs): 1 box in 1,000 images; no unparsed replies. This meets the DEC-062 expectation.
- MedNIST: 143 boxes in 600 images (0.238). The expectation does not hold for medical images of other modalities. Boxes by class, in counts: ChestCT 60, BreastMRI 55, HeadCT 20, AbdomenCT 7, Hand 1, CXR 0 (each of 100). Of the 144 boxes in total, 142 are in four MedNIST classes: ChestCT, BreastMRI, HeadCT, AbdomenCT.
- Unparsed replies: 0 of 1,600.
- Time: 0.5 to 0.65 s per image for "no box" classes; 0.8 to 1.4 s per image where boxes are frequent (longer replies). Whole run about 23 minutes.
- Exploratory, one seed, one draw. Whether a box on a CT or MRI slice is wrong for the detector's purpose is the user's decision; I looked at no image. Any prompt change is a new decision.

## Limits

One draw (seed 0); public datasets only, not the real negatives of the B-mode project; time per image is from one run on one GPU (RTX 3060 shared box).
