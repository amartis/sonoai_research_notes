# 2026-11-24

What the six epic 1 seed-0 runs (R1 to R6) tell us, and what to improve. Written by Claude
(Opus 5.5) at the user's request. An exploratory analysis of finished runs, not an EXP record
and not a decision; the EXP record of [TASK-197](../../../backlog/tasks/task-197%20-%20Epic-1-runs-on-RunPod-R1-to-R6-at-seed-0-then-seeds-1-and-2-of-the-best-recipe-shift-test-EXP-record-with-the-DEC-076-verdict-per-recipe-DEC-080.md) still has to be written. Aggregates only: no
images were opened and no file names or identifiers are given.

The user's steer for this note: the stomach is not vivid on ultrasound images, so stomach
DSC (W1 stomach) and stomach per-sample accuracy (W2 stomach) matter less. The summary below
therefore reads the results "with the stomach set aside"; the bar itself is unchanged.

Abbreviations and terms: **W1**, mean Dice similarity coefficient (DSC) over samples where
the organ is labelled present; **W2**, the share of samples labelled absent (closed negative,
presence policy `strict_v1`) on which the model predicts 0 pixels of the organ; **W3**,
W1(val) − W1(test) ([DEC-076](../../decisions/DEC-076-epic1-metrics-label-set-score-selection-ci-and-pass-rule.md)).
Bar: W1 liver ≥ 0.85, the other organs ≥ 0.70; W2 every organ ≥ 0.90; W3 every organ ≤ 0.10.
**R1 to R6**: the recipes of [DEC-077](../../decisions/DEC-077-epic1-model-choice-six-recipes.md)
Table 1 (R1 `transunet` ImageNet-21k; R2 `transunet` from scratch; R3 `resenc_unet` from
scratch; R4, R5, R6 DINOv3 ConvNeXt-B with an MLP, U-Net-style and UPerNet decoder). A
**failure** is one closed-negative sample with 1 or more predicted pixels of that organ.
**Datasource group**: datasources joined because they share an image, the unit of the test
split ([DEC-071](../../decisions/DEC-071-epic1-splitting-parameterised-split-method.md)); the
11 test groups are named A to K by test sample count, A largest. These letters differ from
those of the note [2026-11-24-liver-negative-label-check-claude.md](2026-11-24-liver-negative-label-check-claude.md)
(its A, B, C, D, E, F are B, C, F, J, A, K here). CI, 95% confidence interval.

## Summary

1. **No recipe meets the bar.** The three DINOv3 recipes are the best and close to each other
   (Tables 2 to 5). With the stomach set aside, R4 and R5 fail only W2 liver (R4 0.584, R5
   0.670; bar 0.90). Their W2 kidney meets the bar by point estimate only: the CI lower bound
   is 0.609 (R4) and 0.526 (R5), because 620 of the 718 test kidney negatives come from one
   group.
2. **Segmentation generalises well to unseen datasources for liver, kidney and gallbladder.**
   R4 on test: W1 liver 0.907, kidney 0.910, gallbladder 0.838; W3 at most 0.030 for these
   three organs in R4 to R6. The stomach is the exception (W1 0.565-0.618, W3 0.155-0.201).
3. **The W2 liver failures are shared by the models, and sit in three groups.** Of 543 test
   liver negatives, 131 failed in all four strong models (R1, R4, R5, R6), where 15.2 were
   expected if their errors were independent; 204 failed in none (Table 7). Groups B, C and F
   hold 509 of the 543. In B and C, liver is drawn on 165 of 466 and 120 of 304 samples, almost
   all kidney views, and closed absent on the rest (Table 6). The false livers there are
   smaller (median 0.023-0.025 of the input, R4) than the livers drawn in the same groups
   (median 0.086 and 0.105). This pattern fits "a small piece of liver was not drawn", but it
   does not prove it.
4. **The false liver is mostly not kidney taken for liver** (DINOv3 models). At most a median
   0.21-0.34 of the false-liver pixels can lie inside the kidney polygon (an upper bound from
   the pixel counts). For R1 this bound is 0.83, so R1's false liver may partly be kidney.
5. **Group F fails on both liver and kidney negatives in every model** (W2 liver 0.160-0.360,
   n = 25; W2 kidney 0.105-0.474, n = 19), while the same models segment F's positives well
   (R4 W1 liver 0.901, kidney 0.896). F is the first candidate for a group-level problem with
   "absent" labels.
6. **DINOv3 overfits the training groups after about 10 to 15 epochs** (Table 8). From epoch 10
   to 30, train W2 liver rose to 0.995 and val to 0.95, while test W2 liver fell from 0.687-0.724
   to 0.529-0.641; test mean W1 peaked at epoch 8 to 14 and was 0.035-0.051 lower at epoch 30;
   val loss was lowest at epoch 11 in all three. The selected epochs (15, 17, 19) come after
   these peaks.
7. **R6 (UPerNet) breaks down on some test images.** On 40 test samples with kidney labelled
   absent (33 in group A), R6 at its selected epoch predicted kidney over a median 0.541 of the
   input while its liver was right (DSC 0.917). R4 never did this, R5 only at epochs 25 and 30
   (8 samples), and R6's count jumps between epochs (0 to 40). It costs R6 0.095 of W2 kidney
   against R4 (paired CI −0.183 to −0.030). Val showed none. The cause is not known.
8. **R2 and R3 are undertrained, so they do not judge their architectures.** Both were selected
   at the last epoch (as was R1; [DEC-080](../../decisions/DEC-080-epic1-optimisation-strategy.md) rule 4 flag). R3 never predicted a gallbladder (W1 0.000;
   its W2 gallbladder of 1.000 is trivial). R1 and R2 began to predict gallbladder only at epoch
   11 and 18 (val W1 gallbladder 0.007 → 0.672 and 0.002 → 0.513 in one epoch). With SGD at
   lr 1e-3 for 13,890 steps, the rare small class starts late or not at all.
9. **Pretraining matters; the DINOv3 decoder matters little.** Paired on test, R1 − R2 mean W1
   (liver, kidney, gallbladder) +0.108 (CI 0.072 to 0.128); R4 − R1 +0.050 (0.031 to 0.062), but
   R4 and R1 also differ in optimiser (DEC-080). R5 − R4 −0.004 (−0.007 to +0.003); R5 − R4 W2
   liver +0.087 (−0.024 to +0.127). One seed each.
10. **Seeds 1 and 2 go to R4** under DEC-080 rule 5.2 (highest val mean W1: R4 0.86890, R6
    0.86865, R5 0.86546; the gap to R6 is above the 1e-4 tolerance but far within noise).
    R6's breakdown (point 7) is a second reason not to pick it.

## What to improve, in order

1. **Settle what "liver absent" means in groups B, C and F before any model change.** It is the
   only blocking criterion once the stomach is set aside, and no model change found here moves
   it near 0.90 (points 3, 5; items 5, 6 below). A cheap step before the image re-read: count, by
   group, which labeling rule or closure produced each liver negative (and F's kidney
   negatives), compared with the train groups where the models fitted them. This needs a new
   table ask (the `strict_v1` presence table with its reason columns). Then the blinded re-read
   of [TASK-233](../../../backlog/tasks/task-233%20-%20Blinded-re-read-of-test-liver-negatives-in-Label-Studio-40-both-fail-and-40-both-pass-samples-of-R1-and-R4-no-model-output-liver-visible-spleen-visible-kidney-side-dataset-record-DIS-049.md), stratified by group (B, C, F) and with F's kidney
   negatives added. If "absent" there turns out to mean "not drawn because small" or "not the
   organ of this task", the fix is a new presence policy version that makes those closures
   unknown, applied alike to train, val and test, and decided from the re-read, never from
   where the models failed.
2. **Stomach: make it report-only by a new DEC, but keep it as a training class.** Dropping it
   from the outputs would leave stomach pixels unlabelled and free for liver or kidney. [DEC-065](../../decisions/DEC-065-mission-upper-abdomen-anatomy-segmentation.md)
   says the bar is not changed after test results are seen, so that DEC must say it was made
   after seeing test, and an epic verdict under the changed bar is exploratory until checked on
   new data (for example the next dataset version, or the public images of epic 2).
3. **Continue with the DINOv3 encoder (R4, or R5), stop spending GPU time on R2 and R3,** and
   drop R6 unless point 7 is understood. A fair from-scratch comparison would need a much larger
   learning rate and many more steps (the analyst's reading, not checked here); it does not look
   worth the cost when the pretrained recipes already lead by +0.05 to +0.11 mean W1.
4. **Train DINOv3 shorter, or average weights.** 15 to 20 epochs instead of 30 would lose nothing
   that val can see (Table 8) and cut a run from about 1.6-1.9 h to about 0.8-1.3 h at 3.2-3.9
   minutes per epoch (wall time with evaluation). A shorter cosine schedule also changes the
   learning rate at every step, so it is a new recipe, not a cut of the old run. Weight averaging (EMA, SWA) may steady the late-epoch
   swings; DEC-080 rule 6 puts it in a new consult session.
5. **A per-organ area gate helps a little and is cheap.** Dropping an organ's whole prediction
   when it covers less than 0.5% of the input raised test W2 liver from 0.584 to 0.676 (R4) and
   from 0.670 to 0.713 (R5) at no cost in W1 liver, and gallbladder W2 to 0.975-0.978 for a W1
   loss of 0.012-0.013 (Table 9). It cannot reach 0.90 for liver: the false livers on test are
   too large. The threshold must be chosen on val, by a rule fixed before the next test read
   (DEC-076 rule 2 says a floor in the bar needs a new DEC).
6. **Ensembling R4 and R5 is unlikely to fix W2 liver.** Even counting a sample as failed only
   when all four strong models predict liver gives W2 liver 0.759 (Table 7). It is new
   evaluation code for a small gain.
7. **Look at group E for W1.** It has the lowest W1 liver and kidney of all test groups (R4
   0.836 and 0.819; gallbladder 0.767), and its stomach W1 is 0.39 on 79 positives. What sets it apart (device, view, image size) is not in the
   run records.
8. **Expect wide W2 CIs whatever the model.** Test liver negatives come from five groups (B and
   C hold 484 of 543) and kidney negatives mostly from A. A W2 verdict rests on two or three
   groups; the EXP record should show the per-group table beside the CI (DEC-076 rule 4 already
   asks for it).

Still open in TASK-197: the brightness shift test (no shift records
in any of the six run folders), seeds 1 and 2 of R4, and the EXP record.

## Done

- Read the six seed-0 run folders of TASK-197 on machine01: run metadata, recipes, the per-epoch
  evaluation summaries of val and test (every epoch) and train (every 5 epochs), and the
  per-sample records at the selected epochs and at the epochs named in the tables.
- Ran the epic 1 report (`sonoai.evaluation.epic1_report`, DEC-076 rules 4 to 6.3; cluster
  bootstrap, 2,000 replicates, seed 0; test clusters are the 11 datasource groups, val clusters
  the 2,920 images) on each run's selected epoch, with the presence states from the sample file.
- Table read, with the user's approval for this analysis
  ([DEC-052](../../decisions/DEC-052-privacy-covers-images-tables-readable-after-asking.md)), plain
  style on machine01: the epic 1 sample file, version 3, of dataset 261023 (sample number, split,
  datasource group, image hash, presence states), under `derived/`. Nothing was written to the
  data root.
- Own computations from the per-sample records: per-group values, cross-model failure counts,
  paired cluster-bootstrap differences between recipes (2,000 replicates, seed 0, the same drawn
  groups for both recipes), the area gate of Table 9, and size comparisons.

## Observations

### Table 1. Setup and checkpoint selection per recipe

Selected epoch by DEC-076 rule 3 (val mean W1, then val mean W2, then val loss). Minutes per
epoch: wall time of the run divided by 30, evaluation included. All runs: one A100 80 GB on
RunPod, batch 32, 30 epochs, fp32, `us_bright_v1` with `percentile_v1`, `leaf_dice_ce` 0.5/0.5.

| Recipe | Model and starting weights | Optimiser (DEC-080 Table 1) | Selected epoch | Val mean W1 at that epoch | Minutes per epoch |
|---|---|---|---|---|---|
| R1 | `transunet`, ImageNet-21k | SGD, poly | 30 (flag: 27 or later) | 0.829 | 3.4 |
| R2 | `transunet`, from scratch | SGD, poly | 30 (flag) | 0.769 | 3.5 |
| R3 | `resenc_unet`, from scratch | SGD, poly | 30 (flag) | 0.460 | 2.1 |
| R4 | DINOv3 ConvNeXt-B, MLP head | AdamW, frozen-encoder start, cosine | 15 | 0.869 | 3.3 |
| R5 | DINOv3 ConvNeXt-B, U-Net-style decoder | as R4 | 17 | 0.865 | 3.2 |
| R6 | DINOv3 ConvNeXt-B, UPerNet | as R4 | 19 | 0.869 | 3.9 |

### Table 2. Test W1 per organ, with 95% CIs

Cluster bootstrap over the 11 test datasource groups. Labelled-present samples: liver 1,617,
kidney 1,063, gallbladder 268, stomach 367.

| Recipe | Liver | Kidney | Gallbladder | Stomach |
|---|---|---|---|---|
| R1 | 0.891 (0.861 to 0.914) | 0.879 (0.839 to 0.896) | 0.734 (0.675 to 0.835) | 0.605 (0.460 to 0.728) |
| R2 | 0.836 (0.795 to 0.862) | 0.754 (0.706 to 0.795) | 0.589 (0.514 to 0.740) | 0.479 (0.415 to 0.524) |
| R3 | 0.776 (0.694 to 0.815) | 0.671 (0.612 to 0.721) | 0.000 (0.000 to 0.000) | 0.049 (0.010 to 0.100) |
| R4 | 0.907 (0.877 to 0.928) | 0.910 (0.873 to 0.923) | 0.838 (0.803 to 0.883) | 0.618 (0.391 to 0.750) |
| R5 | 0.898 (0.851 to 0.927) | 0.912 (0.881 to 0.924) | 0.835 (0.810 to 0.884) | 0.565 (0.383 to 0.754) |
| R6 | 0.897 (0.851 to 0.926) | 0.904 (0.866 to 0.918) | 0.824 (0.789 to 0.892) | 0.571 (0.407 to 0.757) |

### Table 3. Test W2 per organ, with 95% CIs

As Table 2. Closed-negative samples: liver 543, kidney 718, gallbladder 1,495, stomach 1,512.

| Recipe | Liver | Kidney | Gallbladder | Stomach |
|---|---|---|---|---|
| R1 | 0.527 (0.306 to 0.573) | 0.900 (0.556 to 0.956) | 0.950 (0.929 to 0.971) | 0.657 (0.453 to 0.857) |
| R2 | 0.053 (0.018 to 0.076) | 0.642 (0.333 to 0.851) | 0.830 (0.707 to 0.927) | 0.466 (0.291 to 0.752) |
| R3 | 0.000 (0.000 to 0.000) | 0.058 (0.000 to 0.170) | 1.000 (1.000 to 1.000) | 0.440 (0.252 to 0.734) |
| R4 | 0.584 (0.435 to 0.677) | 0.951 (0.609 to 1.000) | 0.941 (0.926 to 0.971) | 0.714 (0.486 to 0.921) |
| R5 | 0.670 (0.415 to 0.803) | 0.942 (0.526 to 0.973) | 0.944 (0.933 to 0.966) | 0.767 (0.599 to 0.923) |
| R6 | 0.569 (0.324 to 0.733) | 0.857 (0.455 to 0.949) | 0.958 (0.946 to 0.974) | 0.778 (0.619 to 0.933) |

R1 W2 kidney is 0.8997, below the bar. At the 1% area floor (information only, DEC-076 rule 2)
test W2 liver was 0.722 (R1), 0.703 (R4), 0.740 (R5), 0.659 (R6).

### Table 4. W3 per organ, with 95% CIs

Val and test drawn independently (DEC-076 rule 4).

| Recipe | Liver | Kidney | Gallbladder | Stomach |
|---|---|---|---|---|
| R1 | 0.023 (−0.003 to 0.051) | 0.041 (0.023 to 0.080) | 0.003 (−0.097 to 0.069) | 0.141 (0.020 to 0.279) |
| R2 | 0.046 (0.020 to 0.086) | 0.130 (0.088 to 0.180) | 0.025 (−0.129 to 0.109) | 0.216 (0.163 to 0.285) |
| R3 | 0.061 (0.022 to 0.139) | 0.126 (0.075 to 0.186) | 0.000 (0.000 to 0.000) | 0.156 (0.098 to 0.201) |
| R4 | 0.019 (−0.004 to 0.049) | 0.022 (0.008 to 0.061) | 0.007 (−0.040 to 0.047) | 0.155 (0.026 to 0.374) |
| R5 | 0.025 (−0.006 to 0.072) | 0.021 (0.008 to 0.053) | 0.008 (−0.045 to 0.042) | 0.199 (0.017 to 0.386) |
| R6 | 0.030 (−0.001 to 0.076) | 0.026 (0.011 to 0.065) | 0.022 (−0.049 to 0.066) | 0.201 (0.016 to 0.377) |

### Table 5. Criteria not met, per recipe (DEC-076 rule 5)

| Recipe | Not met | Not met, stomach aside | Met, but the CI bound is on the wrong side of the bar |
|---|---|---|---|
| R1 | W1 stomach; W2 liver, kidney, stomach; W3 stomach | W2 liver, W2 kidney | W1 gallbladder |
| R2 | W1 liver, stomach, gallbladder; W2 all four; W3 kidney, stomach | 7 criteria | W3 gallbladder |
| R3 | W1 all four; W2 liver, kidney, stomach; W3 kidney, stomach | 7 criteria | W3 liver |
| R4 | W1 stomach; W2 liver, stomach; W3 stomach | **W2 liver** | W2 kidney |
| R5 | W1 stomach; W2 liver, stomach; W3 stomach | **W2 liver** | W2 kidney |
| R6 | W1 stomach; W2 liver, kidney, stomach; W3 stomach | W2 liver, W2 kidney | none |

### Table 6. Test values per datasource group

Groups by test sample count (A largest). W1 and W2 shown where the group has 5 or more scored
samples ("-" otherwise); point values, no CI.

| Datasource group | Samples, n | Liver positive, n | Liver negative, n | Kidney negative, n | R4 W1 liver | R4 W1 kidney | R4 W1 gallbladder | W2 liver, R1 / R4 / R5 / R6 | W2 kidney, R1 / R4 / R5 / R6 |
|---|---|---|---|---|---|---|---|---|---|
| A | 663 | 649 | 12 | 620 | 0.914 | 0.851 | 0.830 | 0.500 / 0.583 / 0.750 / 0.833 | 0.910 / 0.968 / 0.965 / 0.873 |
| B | 466 | 165 | 301 | 3 | 0.907 | 0.927 | 0.874 | 0.571 / 0.681 / 0.807 / 0.731 | - |
| C | 304 | 120 | 183 | 0 | 0.851 | 0.913 | - | 0.497 / 0.459 / 0.503 / 0.328 | - |
| D | 201 | 201 | 0 | 0 | 0.947 | 0.917 | 0.889 | - | - |
| E | 186 | 181 | 0 | 0 | 0.836 | 0.819 | 0.767 | - | - |
| F | 126 | 101 | 25 | 19 | 0.901 | 0.896 | - | 0.160 / 0.360 / 0.240 / 0.240 | 0.474 / 0.263 / 0.158 / 0.105 |
| G | 112 | 112 | 0 | 0 | 0.941 | 0.912 | 0.890 | - | - |
| H | 41 | 41 | 0 | 41 | 0.965 | - | - | - | 1.000 / 1.000 / 1.000 / 1.000 |
| I | 31 | 31 | 0 | 26 | 0.952 | 0.949 | 0.766 | - | 1.000 / 1.000 / 0.885 / 0.846 |
| J | 30 | 9 | 21 | 1 | 0.874 | 0.926 | - | 0.619 / 0.524 / 0.619 / 0.571 | - |
| K | 8 | 7 | 1 | 8 | 0.889 | - | 0.913 | - | 0.500 / 1.000 / 1.000 / 1.000 |

Size of labelled and false liver, as a share of the 224 × 224 input (R4): labelled liver median
0.086 in B and 0.105 in C (P25 0.063 and 0.083); false liver on B's and C's failures median
0.025 and 0.023 (P75 0.059 and 0.062); in F, false liver median 0.050 against labelled liver
0.110. The 131 liver negatives that failed in all four models were in C (55), B (51), F (16),
J (7) and A (2).

### Table 7. Test liver negatives by the number of strong models that failed on them

Strong models: R1, R4, R5, R6. Expected counts if the four failed independently, each at its
own failure rate (Poisson-binomial). n = 543.

| Models that failed, of 4 | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Samples, observed | 204 | 93 | 66 | 49 | 131 |
| Samples, expected if independent | 63.7 | 182.2 | 192.7 | 89.2 | 15.2 |

W2 liver if a sample counts as failed only when at least 2, 3 or all 4 models fail on it: 0.547,
0.669, 0.759. On val (n = 630) the counts were 535, 47, 14, 15, 19.

### Table 8. DINOv3 recipes over training

Train evaluated every 5 epochs (unaugmented). Mean W1 over the four organs.

| Recipe | Epoch | Train W2 liver | Val W2 liver | Test W2 liver | Val mean W1 | Test mean W1 | Val loss |
|---|---|---|---|---|---|---|---|
| R4 | 5 | 0.889 | 0.871 | 0.637 | 0.846 | 0.808 | 0.327 |
| R4 | 10 | 0.979 | 0.937 | 0.724 | 0.860 | 0.812 | 0.323 |
| R4 | 15 | 0.977 | 0.929 | 0.584 | 0.869 | 0.818 | 0.322 |
| R4 | 20 | 0.995 | 0.951 | 0.591 | 0.864 | 0.791 | 0.325 |
| R4 | 30 | 0.995 | 0.951 | 0.551 | 0.867 | 0.787 | 0.326 |
| R5 | 5 | 0.894 | 0.871 | 0.678 | 0.825 | 0.789 | 0.330 |
| R5 | 10 | 0.982 | 0.946 | 0.702 | 0.852 | 0.801 | 0.323 |
| R5 | 15 | 0.982 | 0.941 | 0.665 | 0.863 | 0.800 | 0.323 |
| R5 | 20 | 0.996 | 0.952 | 0.604 | 0.863 | 0.793 | 0.325 |
| R5 | 30 | 0.995 | 0.956 | 0.641 | 0.864 | 0.787 | 0.329 |
| R6 | 5 | 0.886 | 0.840 | 0.444 | 0.843 | 0.808 | 0.328 |
| R6 | 10 | 0.971 | 0.946 | 0.687 | 0.858 | 0.805 | 0.322 |
| R6 | 15 | 0.978 | 0.938 | 0.519 | 0.868 | 0.811 | 0.323 |
| R6 | 20 | 0.996 | 0.959 | 0.567 | 0.865 | 0.785 | 0.326 |
| R6 | 30 | 0.995 | 0.954 | 0.529 | 0.865 | 0.786 | 0.329 |

Test samples with kidney labelled absent and more than 0.2 of the input predicted as kidney, by
epoch (10, 15, 17, 19, 20, 25, 30): R4 0 at every epoch; R5 0, 0, 0, 0, 0, 8, 8; R6 0, 4, 17,
40, 15, 34, 24. Val: none for R6 at its selected epoch (n = 836).

### Table 9. Area gate: an organ's whole prediction dropped when it covers less than a share of the input

Applied to the per-sample counts of the selected epoch; a positive sample whose prediction is
dropped scores DSC 0. Not a connected-component filter (the records hold no components).

| Recipe | Gate, share of input | Val W1 liver | Val W2 liver | Test W1 liver | Test W2 liver | Test W1 kidney | Test W2 kidney | Test W1 gallbladder | Test W2 gallbladder |
|---|---|---|---|---|---|---|---|---|---|
| R4 | 0 (none) | 0.926 | 0.929 | 0.907 | 0.584 | 0.910 | 0.951 | 0.838 | 0.941 |
| R4 | 0.0025 | 0.925 | 0.933 | 0.907 | 0.648 | 0.910 | 0.964 | 0.835 | 0.963 |
| R4 | 0.005 | 0.925 | 0.938 | 0.907 | 0.676 | 0.910 | 0.969 | 0.825 | 0.978 |
| R4 | 0.01 | 0.925 | 0.946 | 0.907 | 0.703 | 0.910 | 0.974 | 0.742 | 0.994 |
| R5 | 0 (none) | 0.923 | 0.957 | 0.898 | 0.670 | 0.912 | 0.942 | 0.835 | 0.944 |
| R5 | 0.0025 | 0.923 | 0.965 | 0.898 | 0.702 | 0.912 | 0.947 | 0.833 | 0.966 |
| R5 | 0.005 | 0.922 | 0.965 | 0.897 | 0.713 | 0.911 | 0.948 | 0.823 | 0.975 |
| R5 | 0.01 | 0.922 | 0.973 | 0.897 | 0.740 | 0.911 | 0.958 | 0.759 | 0.989 |

### Other observations

- Gallbladder misses (labelled present, 0 pixels predicted) on test: 0.019-0.045 in R4 to R6,
  0.060 in R1. Small gallbladders score lowest: R4 W1 0.780 in the smallest third (0.005-0.017 of
  the input) against 0.876 in the largest.
- Over- or under-segmentation is not an issue for the DINOv3 models: on test the median
  predicted-to-labelled area ratio is 0.93-1.04 for liver, kidney and gallbladder.
- Stomach W1 per group (R4): A 0.65, D 0.76, E 0.39, G 0.76, I 0.39 (2 decimals here because
  the group sizes are small: 22 to 129 positives).

## Limits

- Exploratory, one seed per recipe; recipe differences of a few thousandths are noise.
- The test CIs rest on 11 datasource groups, and W2 liver and W2 kidney on five groups each; the
  paired differences use the same cluster bootstrap and are as coarse.
- No images were looked at. Whether the liver-negative failures are label errors, hard images or
  a domain gap cannot be decided from counts (as the earlier note says).
- The kidney-confusion bound of point 4 and the area gate work on per-organ pixel counts; where
  in the image the false pixels lie is not recorded.
- R1 against R4 to R6 differs in model and optimiser (DEC-080 rule 1).

## Next

For the user to decide (nothing here is decided):

1. The closure-rule count for liver negatives of groups B, C and F (a new table ask), then the
   blinded re-read (TASK-233), stratified by group; possibly folded into [TASK-232](../../../backlog/tasks/task-232%20-%20Liver-negative-audit-of-the-TASK-197-runs-R1-and-R4-failure-rate-per-datasource-group-and-spleen-state-on-val-and-test-and-a-training-dynamics-count-of-train-liver-negatives-fit-late-or-never-aggregate-dataset-record-DIS-049.md) (liver-negative
   audit).
2. A consult on the stomach as report-only (point 2 of the list above, with the DEC-065 caveat).
3. A consult on shorter DINOv3 runs and weight averaging, after the re-read, since a policy
   change would mean retraining anyway.
4. TASK-197 continues: shift test, seeds 1 and 2 of R4, EXP record with this note's caveats.
