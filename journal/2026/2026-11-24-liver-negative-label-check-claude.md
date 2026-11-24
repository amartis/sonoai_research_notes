# 2026-11-24

Low W2 liver on test for R1 and R4: are the liver-negative labels wrong, or is the model
mistaking the spleen for liver? Written by Claude (Opus 5.5) in a consult session at the
user's request. An exploratory check of two finished runs, not an EXP record and not a
decision. Aggregates only: no images were opened and no file names or identifiers are given.

Abbreviations and terms: **W2**, the "no phantom organs" score of epic 1: for one organ, the
share of samples labelled absent (a *closed negative*, presence policy `strict_v1`) on which
the model predicts 0 pixels of that organ ([DEC-076](../../decisions/DEC-076-epic1-metrics-label-set-score-selection-ci-and-pass-rule.md) Table 1). A **failure** here is one such sample
with 1 or more predicted liver pixels, so failure rate = 1 − W2. **W2, 1% floor**: the same,
but predictions below 1% of the input area count as none (information only, DEC-076 rule 2).
**R1**: recipe `transunet` with ImageNet-21k weights; **R4**: DINOv3 ConvNeXt-B encoder with
an MLP head ([DEC-077](../../decisions/DEC-077-epic1-model-choice-six-recipes.md)). **Datasource group**: datasources joined because they share an image;
the unit of the test split ([DEC-071](../../decisions/DEC-071-epic1-splitting-parameterised-split-method.md)). **Kidney view**: a sample with kidney positive and stomach
and gallbladder negative (a description used in this note only). CI, confidence interval;
κ, Cohen's kappa.

## Summary

1. **The low score is real and specific to test.** W2 liver fell from 0.860 (val) to 0.527 on
   test for R1, and from 0.929 to 0.584 for R4 (n = 630 val and 543 test liver negatives;
   Table 1). The 1% floor raised test only to 0.722 and 0.703.
2. **Both models failed on the same samples, far beyond chance.** On test, 184 samples failed
   in both models where 107.0 were expected if their errors were independent; κ = 0.573
   (95% CI 0.446-0.655). The cause sits in the samples, not in one model. This does not tell
   a wrong label from a hard image.
3. **Almost all liver negatives are kidney views,** 540 of 543 on test (val 580 of 630). The
   false liver is small: median 0.016 (R1) and 0.030 (R4) of the input area, about the size
   of the smallest labelled livers (test positives, 10th percentile 0.068).
4. **The failure depends on the datasource group.** Val shares groups with train and failed
   on 0.071-0.140 of liver negatives. Test holds out groups and failed on 0.416-0.473.
   Every test group with 12 or more liver negatives failed often (0.319 to 0.840; Table 3),
   so no single group explains it.
5. **Confusing the spleen with liver does not explain the test failures, as labelled.** 538 of
   543 test liver negatives also have the spleen labelled absent. Where a spleen is drawn
   (val 143, train 723), both models failed *less* often than where it is absent (Table 2).
   Only 5 test liver negatives have a spleen drawn; all 5 failed in both models (too few to
   judge).
6. **What remains, by the analyst's reading: the meaning of "absent" in these labels.** Test
   sources almost never label a spleen (5 of 2,168 test samples, against 877 of 17,843 in
   train + val). In general ultrasound anatomy, a kidney view is usually seen through the
   liver (right) or the spleen (left); that is the analyst's understanding, not verified
   here. Yet 537 of 542 test kidney views have both liver and spleen labelled absent. Either
   these views truly show neither organ, or "absent" there means "not labelled". The second
   would make liver label errors likely. Only a look at the images can decide this.
7. **Proposed next step (not yet agreed):** a blinded re-read by the user in Label Studio of
   about 40 samples both models failed on and 40 that both got right, mixed and without the
   model output, marking per image: liver visible? spleen visible? which kidney? This gives
   a label-error rate with a 95% CI. Test labels must not be changed only where the models
   failed; that would raise the test score by construction.

## Done

- Read the two runs' per-sample eval records on machine01 (val, test and train records;
  selected epochs: R1 epoch 30, R4 epoch 15; train records at the same epochs): the seed-0
  run folders of R1 and R4 from
  [TASK-197](../../../backlog/tasks/task-197%20-%20Epic-1-runs-on-RunPod-R1-to-R6-at-seed-0-then-seeds-1-and-2-of-the-best-recipe-shift-test-EXP-record-with-the-DEC-076-verdict-per-recipe-DEC-080.md) (epic 1 runs on RunPod).
- Tables read, with the user's approval for this check ([DEC-052](../../decisions/DEC-052-privacy-covers-images-tables-readable-after-asking.md)), plain style on machine01:
  the epic 1 sample file, version 3, of dataset 261023 (split, datasource group and image per
  sample) and the spleen rows of the `strict_v1` presence table of dataset 261023 (spleen
  state), both under `derived/`. Nothing was
  written. The join was checked: the liver state in the run records equals the sample file's
  in 1.000 of test and val samples and 0.9998 of train samples.
- Looked up four methods for the analysis (section "Methods that apply").

## Observations

### Table 1. W2 liver per split and model

W2 liver and W2 liver with the 1% floor, with 95% CIs, at the checkpoint selected on val
mean W1 (R1 epoch 30, R4 epoch 15). CIs: test by cluster bootstrap over datasource groups
(5,000 replicates, seed 0; the liver negatives come from only 6 groups, so this CI is
coarse); val and train by bootstrap over images (one sample per image here).

| Split | Liver negatives, n | R1 W2 (95% CI) | R4 W2 (95% CI) | R1 W2, 1% floor (95% CI) | R4 W2, 1% floor (95% CI) |
|---|---|---|---|---|---|
| train | 3,111 | 0.887 (0.876-0.898) | 0.977 (0.971-0.982) | 0.954 (0.946-0.961) | 0.987 (0.984-0.991) |
| val | 630 | 0.860 (0.833-0.887) | 0.929 (0.908-0.948) | 0.930 (0.910-0.949) | 0.946 (0.927-0.963) |
| test | 543 | 0.527 (0.341-0.572) | 0.584 (0.439-0.675) | 0.722 (0.402-0.757) | 0.703 (0.524-0.775) |

R1 failed on 0.113 of its own train liver negatives, so it never fully fitted them; R4 failed
on 0.023.

### Shared failures of R1 and R4

Samples where both models failed, the count expected if the two failed independently (rate R1
× rate R4 × n), and Cohen's κ between the two failure indicators (CI as in Table 1).

| Split | n | Both failed | Expected if independent | κ (95% CI) |
|---|---|---|---|---|
| train | 3,111 | 58 | 8.3 | 0.244 (0.191-0.296) |
| val | 630 | 39 | 6.3 | 0.543 (0.434-0.644) |
| test | 543 | 184 | 107.0 | 0.573 (0.446-0.655) |

Size of the false liver, as a share of the input area (224 × 224 px), among failures only:

| Split | Model | Failures, n | P10 | P25 | Median | P75 | P90 |
|---|---|---|---|---|---|---|---|
| test | R1 | 257 | 0.001 | 0.005 | 0.016 | 0.047 | 0.074 |
| test | R4 | 226 | 0.002 | 0.008 | 0.030 | 0.061 | 0.082 |
| val | R1 | 88 | 0.001 | 0.003 | 0.010 | 0.026 | 0.054 |
| val | R4 | 45 | 0.003 | 0.011 | 0.029 | 0.041 | 0.054 |

Only 3 test samples (val 2) had a false liver of 0.10 of the area or more in both models.
For comparison, labelled liver polygons cover 0.068 (10th percentile) and 0.150 (median) of
the input on test (n = 1,617 positives), and 0.042 and 0.113 on val (n = 2,288).

### Table 2. Failure rate by the spleen label

Failure rate (1 − W2) on liver-negative samples, by the spleen's state under `strict_v1`, with
95% Wilson CIs. Wilson CIs treat samples as independent; samples of one datasource group are
not, so the test CIs are too narrow. Every spleen positive here has a spleen polygon.

| Split | Spleen state | n | R1 failure rate (95% CI) | R4 failure rate (95% CI) |
|---|---|---|---|---|
| train | absent | 2,385 | 0.132 (0.119-0.146) | 0.025 (0.020-0.032) |
| train | drawn | 723 | 0.048 (0.035-0.067) | 0.018 (0.011-0.031) |
| val | absent | 487 | 0.158 (0.128-0.193) | 0.074 (0.054-0.101) |
| val | drawn | 143 | 0.077 (0.043-0.132) | 0.063 (0.033-0.115) |
| test | absent | 538 | 0.468 (0.427-0.511) | 0.411 (0.370-0.453) |
| test | drawn | 5 | 1.000 (0.566-1.000) | 1.000 (0.566-1.000) |

Train also had 3 liver negatives with the spleen state unknown (R1 failed on all 3, R4 on
none).

How often a spleen is drawn at all: 732 of 14,836 train samples, 145 of 3,007 val samples and
5 of 2,168 test samples. In train + val, 10 of the 13 datasource groups that have 10 or more
kidney views with liver absent have no spleen drawn in those views. So the "liver absent,
spleen absent" pattern also exists in training groups, and R4 fitted most of them there
(train failure rate 0.025).

### Table 3. Test failure rate per datasource group

Failure rate on test liver negatives per datasource group, groups named by size (A largest),
with 95% Wilson CIs (samples treated as independent within a group).

| Group | n | R1 failure rate (95% CI) | R4 failure rate (95% CI) |
|---|---|---|---|
| A | 301 | 0.429 (0.374-0.485) | 0.319 (0.269-0.374) |
| B | 183 | 0.503 (0.431-0.574) | 0.541 (0.469-0.612) |
| C | 25 | 0.840 (0.653-0.936) | 0.640 (0.445-0.798) |
| D | 21 | 0.381 (0.208-0.591) | 0.476 (0.283-0.676) |
| E | 12 | 0.500 (0.254-0.746) | 0.417 (0.193-0.680) |
| F | 1 | 1.000 (0.207-1.000) | 0.000 (0.000-0.793) |

### Three explanations, and what the data say about each

| Explanation | What it predicts | What was seen |
|---|---|---|
| Label wrong: liver visible, labelled absent | Small false livers; shared failures; group-dependent, if the labelling habit differs by source | Small false livers (median 0.016-0.030); κ 0.573; failures high in every test group. Consistent, not proven. |
| Label right, spleen taken for liver | Higher failure where a spleen is drawn | The opposite in train and val; test has almost no spleen drawn. Not supported as labelled. Not ruled out if "spleen absent" is itself wrong. |
| Label right, test images differ (devices, views) | Failures only in held-out groups, labels fine | Failure rate val 0.071-0.140 against test 0.416-0.473. Consistent, not separable from a group-specific labelling habit without the images. |

### Methods that apply

| Method | Idea | Use here |
|---|---|---|
| Error consistency, Geirhos, Meding and Wichmann 2020 ([arXiv:2006.16736](https://arxiv.org/abs/2006.16736)) | κ between two decision-makers' errors shows whether they err on the same inputs beyond chance | Done above (κ 0.573 on test) |
| Kinds of label noise, Frénay and Verleysen 2014 ([doi:10.1109/TNNLS.2013.2292894](https://doi.org/10.1109/TNNLS.2013.2292894)) | Label noise can be completely random, depend on the class, or depend on the input ("not at random") | If these are label errors, they depend on the input (small liver at the edge of a kidney view), so more data does not average them out. The definitions were checked only through papers that cite the survey. |
| Confident learning, Northcutt, Jiang and Chuang 2021 ([arXiv:1911.00068](https://arxiv.org/abs/1911.00068), JAIR) | Rank samples by how strongly out-of-sample predictions disagree with the given label; estimate the label-error rate (`cleanlab`) | Test predictions are out of sample; needs a per-sample liver probability, which the records do not store (pixel counts only) |
| Area under the margin, Pleiss et al. 2020 ([arXiv:2001.10528](https://arxiv.org/abs/2001.10528)) | Wrongly labelled training samples are learned late or never | The per-sample train records every 5 epochs already exist; R1 never fitted 0.113 of its train liver negatives |

A related note of the same day, on a per-sample, per-epoch view of suspected label errors:
`2026-11-24-label-noise-heatmap-claude.md` (another session).

### Limits

- Exploratory: one seed per recipe, two recipes, and R1 against R4 differs in model and
  optimiser ([DEC-080](../../decisions/DEC-080-epic1-optimisation-strategy.md)).
- The test CIs rest on 6 datasource groups; the bootstrap CI is coarse and the Wilson CIs are
  too narrow.
- No images were looked at; no kidney side is labelled in the dataset; the runs saved no
  predicted masks, so where the false liver lies in the image (edge, near the kidney, near a
  spleen) is not known.
- The spleen state comes from the same labellers' closures as the liver state, so Table 2
  rests on the same labels that are in doubt.

## Next

Waiting on the user (consult session, nothing decided yet):

1. A liver-negative audit task (scope `data`): failures per group and spleen state (done here
   in part), area-under-the-margin ranking of the train liver negatives from the existing
   records.
2. The blinded re-read in Label Studio (Summary point 7), with liver, spleen and kidney side
   per image.
3. [TASK-197](../../../backlog/tasks/task-197%20-%20Epic-1-runs-on-RunPod-R1-to-R6-at-seed-0-then-seeds-1-and-2-of-the-best-recipe-shift-test-EXP-record-with-the-DEC-076-verdict-per-recipe-DEC-080.md) (epic 1 runs R1 to R6) keeps running; its EXP record should carry this note's
   caveat on W2 liver.
