---
id: DIS-052
title: Epic 1 next recipes after the six seed-0 runs - settle "liver absent" first, select on held-out datasource groups, candidate changes to R4, inference steps, bigger bets, and the path to diagnosis
status: open
created: 2026-11-24
outcomes: []
related: [DIS-049, DEC-065, DEC-066, DEC-069, DEC-071, DEC-076, DEC-077, DEC-079, DEC-080, DEC-043, EXP-003]
---
# DIS-052: Epic 1 next recipes after the six seed-0 runs

## Question

After the six seed-0 runs of [TASK-197](../../backlog/tasks/task-197%20-%20Epic-1-runs-on-RunPod-R1-to-R6-at-seed-0-then-seeds-1-and-2-of-the-best-recipe-shift-test-EXP-record-with-the-DEC-076-verdict-per-recipe-DEC-080.md)
(epic 1 runs on RunPod), the user asked which new recipes would work better (models,
optimisation, generalisation tactics), to get the best model from the dataset we have, with
diagnosis as the next intention. The user's view, given in the same session: "I think low test
score is not that bad at all, because small piece of liver can be skipped labeling by the
labeler". The user asked for this record of the analyst's suggestions. Recent computer vision
(CV) trends are for the user's next session (Open questions). **Nothing is decided here.**

Terms and abbreviations: **W1**, **W2**, **W3** are the epic 1 scores of
[DEC-076](../decisions/DEC-076-epic1-metrics-label-set-score-selection-ci-and-pass-rule.md)
(W1: mean Dice similarity coefficient, DSC, over samples where the organ is labelled present;
W2: share of samples labelled absent, a closed negative under `strict_v1`, with 0 predicted
pixels of the organ; W3: W1 on val minus W1 on test). Bar: W1 liver ≥ 0.85, the other organs
≥ 0.70; W2 ≥ 0.90; W3 ≤ 0.10. **R1 to R6**: the recipes of
[DEC-077](../decisions/DEC-077-epic1-model-choice-six-recipes.md) Table 1. **Datasource group**:
datasources joined because they share an image, the unit of the test split
([DEC-071](../decisions/DEC-071-epic1-splitting-parameterised-split-method.md)). **Kidney view**:
a sample with kidney present and stomach and gallbladder absent (as in [DIS-049](DIS-049-epic1-low-test-w2-liver-label-check.md)). **C1 to C6**:
labels of candidate recipe changes in this note only; a DEC would give them recipe names.
CI, 95% confidence interval; EMA, exponential moving average of weights; SWA, stochastic weight
averaging; LP-FT, training the head first with the encoder frozen, then the whole network;
LoRA, low-rank adapters; SSL, self-supervised learning; TTA, test-time augmentation; HRI,
hepatorenal index.

## Facts checked

Read for this note: the summary eval records (per split and epoch; no per-sample records),
recipes, run metadata and train logs of the six run folders on machine01; DIS-049 and its
journal note [2026-11-24-liver-negative-label-check-claude.md](../journal/2026/2026-11-24-liver-negative-label-check-claude.md);
[2026-11-24-label-noise-heatmap-claude.md](../journal/2026/2026-11-24-label-noise-heatmap-claude.md);
[2026-11-19-optimiser-choice-claude.md](../journal/2026/2026-11-19-optimiser-choice-claude.md);
DEC-065, [DEC-066](../decisions/DEC-066-epic1-model-task-label-set-softmax.md), DEC-069, DEC-071, DEC-076, DEC-077, DEC-079, [DEC-080](../decisions/DEC-080-epic1-optimisation-strategy.md); the literature note
[epic1-anatomy-segmentation-models-and-papers.md](../literature/epic1-anatomy-segmentation-models-and-papers.md).
No table, per-sample record or image was read. The CIs, per-group values, cross-model counts and
area-gate values below come from another session's note of the same day,
[2026-11-24-epic1-six-runs-analysis-claude.md](../journal/2026/2026-11-24-epic1-six-runs-analysis-claude.md)
("the six-runs note"), which read the per-sample records and the sample file with the user's ok.
Exploratory: one seed per recipe.

Table 1. Test values at the checkpoint selected on val (DEC-076 rule 3), seed 0, point
estimates. n test: liver 1,617 present and 543 absent, kidney 1,063 and 718, stomach 367 and
1,512, gallbladder 268 and 1,495. CIs: the six-runs note, Tables 2 to 4.

| Recipe | Selected epoch | Val mean W1 | Test W1 liver / kidney / stomach / gallbladder | Test W2 liver / kidney / stomach / gallbladder | W3 stomach |
|---|---|---|---|---|---|
| R1 `transunet`, ImageNet-21k, SGD | 30 (flag: 27 or later) | 0.829 | 0.891 / 0.879 / 0.605 / 0.734 | 0.527 / 0.900 / 0.657 / 0.950 | 0.141 |
| R2 `transunet`, from scratch, SGD | 30 (flag) | 0.769 | 0.836 / 0.754 / 0.479 / 0.589 | 0.053 / 0.642 / 0.466 / 0.830 | 0.216 |
| R3 `resenc_unet`, from scratch, SGD | 30 (flag) | 0.460 | 0.776 / 0.671 / 0.049 / 0.000 | 0.000 / 0.058 / 0.440 / 1.000 | 0.156 |
| R4 DINOv3 ConvNeXt-B, MLP head, AdamW | 15 | 0.869 | 0.907 / 0.910 / 0.618 / 0.838 | 0.584 / 0.951 / 0.714 / 0.941 | 0.155 |
| R5 DINOv3, U-Net-style decoder | 17 | 0.865 | 0.898 / 0.912 / 0.565 / 0.835 | 0.670 / 0.942 / 0.767 / 0.944 | 0.199 |
| R6 DINOv3, UPerNet | 19 | 0.869 | 0.897 / 0.904 / 0.571 / 0.824 | 0.569 / 0.857 / 0.778 / 0.958 | 0.201 |

1. **No recipe meets the bar.** The DINOv3 recipes lead, and their decoders differ little
   (val mean W1 within 0.004). Seeds 1 and 2 go to R4 under DEC-080 rule 5.2 (R4 0.86890,
   R6 0.86865). W3 of liver, kidney and gallbladder is at most 0.030 for R4 to R6.
2. **Criteria not met by R4 and R5:** W1, W2 and W3 stomach, and W2 liver. With the stomach set
   aside (the user's steer in the six-runs note: the stomach is not vivid on ultrasound), they
   fail only W2 liver; their W2 kidney meets the bar by point estimate only (CI lower bound 0.609
   and 0.526). R6 also fails W2 kidney: it predicts kidney over about half the input on some test
   images with kidney absent, which R4 never does (six-runs note, point 7).
3. **The SGD recipes are undertrained, so they do not judge their architectures.** All three
   were selected at epoch 30. R1 and R2 first predicted a gallbladder at epochs 11 and 18;
   R3 never did, and its val W2 kidney is 0.110. Their lr of 1e-3 is a tenth of the official
   TransUNet and nnU-Net values (0.01; checked in the 2026-11-19 note).
4. **Val does not see the datasource gap, and the gap grows with training.** Val is drawn from
   the training groups (DEC-071). For R4 to R6, test mean W1 peaked at epochs 8 to 14 and was
   0.035 to 0.051 lower at epoch 30, and test W2 liver fell from 0.687-0.724 at epoch 10 to
   0.529-0.641 at epoch 30, while val stayed flat (six-runs note, Table 8). Test stomach W1 fell
   from 0.684 (epoch 8) to 0.522 (epoch 30) in R6 and from 0.642 (epoch 5) to 0.541 in R4. The
   selected epochs (15, 17, 19) come after these peaks. These test curves are for diagnosis only;
   no epoch may be chosen from them (DEC-076 rule 3).
5. **The W2 liver failures are shared and look like undrawn small liver.** 540 of 543 test liver
   negatives are kidney views (DIS-049). 131 failed in all four strong models (R1, R4, R5, R6)
   where 15.2 were expected if independent. In the two largest groups of liver negatives the false
   livers (R4 median 0.023-0.025 of the input) are smaller than the livers drawn in the same
   groups (median 0.086-0.105). Test sources draw a spleen on 5 of 2,168 samples.
6. **Inference steps alone cannot bring W2 liver to 0.90.** At the 1% area floor (information
   only, DEC-076 rule 2) test W2 liver is 0.659-0.740. Dropping an organ's prediction below 0.5%
   of the input gives 0.676 (R4) and 0.713 (R5). Counting a sample as failed only when all four
   strong models fail gives 0.759 (six-runs note, Tables 7 and 9).
7. **Time:** 3.2 to 3.9 minutes per epoch for R4 to R6 on one A100 80 GB, about 1.6 to 1.9 h per
   30-epoch run, evaluation included.

## Options considered

### 1. The user's liver view, and the stomach

The analyst's reading, given once:

- **The user's view holds in large part.** Points 5 and 6 fit "a small piece of liver was not
  drawn" in kidney views, in projects whose labellers drew only the organ of the task. In general
  ultrasound anatomy a right-kidney view is seen through the liver (the analyst's understanding,
  not verified here). It is not proven until the blinded re-read
  ([TASK-233](../../backlog/tasks/task-233%20-%20Blinded-re-read-of-test-liver-negatives-in-Label-Studio-40-both-fail-and-40-both-pass-samples-of-R1-and-R4-no-model-output-liver-visible-spleen-visible-kidney-side-dataset-record-DIS-049.md)).
- **Two limits.** About a quarter of the false livers cover more than about 5% of the input, the
  size of small drawn livers (DIS-049 journal note). And the same "liver absent" pattern exists in
  most training groups (DIS-049), so the models were trained to suppress liver in kidney views:
  if these labels are wrong, they cost the model, not only the score.
- **For diagnosis, liver in kidney views matters.** The liver next to the right kidney is where
  the HRI, an ultrasound sign of fatty liver, is read (the analyst's understanding; one automated
  HRI paper was found by search, not read: [PMC8446496](https://pmc.ncbi.nlm.nih.gov/articles/PMC8446496)).
  So drawing the liver there is worth more to the next epic than making it unknown.
- **Stomach.** The analyst first called the stomach the larger problem, because it fails W1, W2
  and W3. With the user's steer (stomach not vivid) and liver diagnosis next, the analyst agrees
  that the stomach can leave the bar, as the six-runs note proposes: keep it as a training class
  (dropping it would free stomach pixels for liver or kidney), report it only, by a new DEC that
  states it was made after test was seen ([DEC-065](../decisions/DEC-065-mission-upper-abdomen-anatomy-segmentation.md)
  section 2), so an epic verdict under it is exploratory until checked on new data. The stomach
  W3 stays the clearest sign of a datasource gap and is worth watching in every new recipe.

### 2. Proposals

Table 2. The analyst's proposals, in the suggested order. Status of every row: open.

| # | Question | Recommendation (default) | Why | Best alternative, and when it would win | Cost to reverse |
|---|---|---|---|---|---|
| P1 | What "liver absent" in kidney views becomes | After TASK-233: if liver is often visible, **draw the liver** in those views (relabel), by a new DEC that applies to all splits | Fact 5; it is the only blocking criterion with the stomach set aside; the HRI needs that liver (section 1) | A new presence-policy version that makes those closures unknown: wins when relabelling costs too many labeller hours; needs no labelling, and saved records can be re-scored | Policy: low (re-score, retrain). Relabel: labelling time, not reversible in effort |
| P2 | Where selection happens | **Grouped 5-fold cross-validation over the train and val datasource groups** (nnU-Net style): epochs, thresholds and recipe choices on out-of-group predictions; the 5 fold models become an ensemble; test stays as it is | Fact 4: val misses the gap; every training group gets an out-of-group score, also usable for label audits (confident learning needs out-of-sample predictions, DIS-049 journal note) | One held-out "val by group" split: cheaper (one run per recipe), but fewer groups for selection. Or keep DEC-071 val: DomainBed found training-domain val as good as leave-domain-out on average in classification (literature note, Section 3.5), which fact 4 does not support here | Medium: amends DEC-071; 5 runs per recipe and seed (about 8 to 10 A100 h for R4) |
| P3 | The stomach in the bar | Report-only by a new DEC, kept as a training class (section 1) | The user's steer; liver diagnosis next | Keep it in the bar: wins if a later epic needs stomach masks | Low (a DEC) |
| P4 | Base recipe for changes | **R4** (DINOv3 ConvNeXt-B with the MLP head); no more GPU time on R2, R3 or R6 | Facts 1 to 3; R4 is the simplest DINOv3 recipe and never broke down on kidney | R5: wins if seeds show its W2 liver lead is real (+0.087, CI −0.024 to +0.127, six-runs note) | Low |
| P5 | First recipe changes | **C1 and C2** (Table 3), each against R4, chosen by P2 | Cheapest; they target fact 4 directly; no data rule changes | C3 first, if W1 of small organs matters more than W3 for the next epic | Low (new recipes) |
| P6 | Inference steps | A per-organ area gate, connected-component cleanup and flip TTA, set on out-of-group predictions (P2), never on test | Cheap W2 gains (fact 6); a stray-pixel speckle fails W2 | Skip them: they cannot reach 0.90 for liver (fact 6); connected components need saved masks, which the eval does not keep | Low |
| P7 | Seeds and comparisons | 2 seeds per candidate, paired against R4's 3 seeds on the same test groups, as differences with CIs | Recipe differences of a few thousandths are noise; test rests on 11 groups, W2 liver on five | One seed per candidate as a screen, seeds only for the winner | Low |

Table 3. Candidate changes to R4, one change each. C1 and C2 first (P5).

| Candidate | Change against R4 | Criterion it aims at | Evidence | Needs |
|---|---|---|---|---|
| C1 | EMA or SWA of the weights over the later epochs | W3, late-epoch swings | SWAD: +1.6 points on average on unseen domains over five benchmarks (checked in the 2026-11-19 note); DEC-080 rule 6 deferred averaging "for example if W3 fails" | a method task; a consult session (DEC-080 rule 6) |
| C2 | Shorter run (15 to 20 epochs, its own cosine schedule) or a longer frozen-encoder start | W3, W2 liver | Fact 4; LP-FT: +10% out of distribution against full fine-tuning (literature note, Section 3.5) | recipe only; selection by P2 |
| C3 | Input 384 (or 448) instead of 224 | W1 of small organs | At 224 the deepest ConvNeXt map is 7 × 7; the smallest third of gallbladders scored W1 0.780 against 0.876 for the largest (six-runs note) | a new DEC replacing [DEC-069](../decisions/DEC-069-epic1-data-preparation.md) rule 4 and its 224 px minimum side; about 3 times the compute (analyst's estimate) |
| C4 | Stronger ultrasound appearance augmentation (speckle, blur and resolution, depth gain curves, zoom), as a new augmentation name | W3 | BigAug: DSC drop on unseen domains about 11% against 39% with standard augmentation (literature note, Section 3.5) | a method task; checked against the brightness shift test of [DEC-079](../decisions/DEC-079-epic1-brightness-robustness-augmentation-percentile-norm-shift-test.md) |
| C5 | Parameter-efficient tuning of a frozen DINOv3 (Rein-style tokens or LoRA) | W3 | Rein and Rein++ report beating full fine-tuning for segmentation on unseen domains with about 1% trainable parameters (web-search summaries, not read: [Rein](https://arxiv.org/abs/2312.04265), [Rein++](https://arxiv.org/html/2508.01667v1)) | a method task |
| C6 | A presence head (one sigmoid per organ per image, unknown masked) that gates the masks | W2 | A phantom organ is an image-level error; the head is also a view classifier for diagnosis; related to [TASK-199](../../backlog/tasks/task-199%20-%20Decide-sigmoid-comparison-run-of-the-best-epic-1-recipe-one-sigmoid-per-organ-with-unknown-outputs-masked-DEC-066-rule-7-DEC-080-rule-6.md) | a method task; only after P1, since it would learn wrong closed negatives even harder |

### 3. Bigger bets (after P1 to P7)

- **Continued SSL of the DINOv3 encoder on all the project's unlabelled ultrasound** (enc1 data on
  RunPod only, [DEC-024](../decisions/DEC-024-plain-never-leaves-machine01-ec2-label-studio-decrypts-in-ram.md)),
  then R4's fine-tuning. Reason: the encoder becomes the shared backbone for segmentation and
  diagnosis. Reported, from web-search summaries only (not read): MedDINOv3, domain-adaptive
  DINOv3 pretraining on CT, +2.57 and +5.49 DSC over nnU-Net on two abdominal CT benchmarks
  ([arXiv:2509.02379](https://arxiv.org/abs/2509.02379)); UltraDINO, DINOv2-style pretraining on
  about 2 million fetal ultrasound images, found that scaling natural-image pretraining did not
  carry over to ultrasound ([arXiv:2506.19552](https://arxiv.org/abs/2506.19552)). Cost: tens of
  A100 hours (analyst's estimate, unverified).
- **Ultrasound-specific encoders.** Low priority: in UltraBench 2 the best one led DINOv3
  ConvNeXt-B by 0.826 against 0.820 anatomical mean DSC, SE 0.007 (literature note, Section
  3.1). Newer ones (Open questions) are unverified.
- **Promptable segmenters as a labelling aid for P1**, not as the epic model: a model pre-draws
  the liver in kidney views and the labeller accepts or corrects it in Label Studio. Inference on
  images runs only where the patient-data rules allow it (machine01, the GPU box or RunPod).
- **A properly configured nnU-Net v2 2D** (its own planning, lr 0.01, momentum 0.99, a long
  schedule) in place of R3, only if a from-scratch CNN baseline is wanted. "nnU-Net Revisited"
  (MICCAI 2024, [arXiv:2404.09556](https://arxiv.org/abs/2404.09556); seen in a search summary,
  not re-read) argues that a well-configured U-Net is hard to beat.
- **Not worth it now:** more decoder comparisons (fact 1); ConvNeXt-L (0.822 against 0.820 in
  UltraBench 2); picking epochs from test curves (fact 4).

### 4. Toward diagnosis

- The liver mask already looks usable as an organ layer ([DEC-043](../decisions/DEC-043-cirrhosis-task-gt-organ-layer-predicted-cirrhosis-only.md)):
  R4 test W1 liver 0.907 (CI 0.877 to 0.928), W3 liver 0.019.
- Fix liver in kidney views (P1) before a fatty-liver task, because of the HRI.
- One backbone for segmentation and diagnosis; diagnosis features pooled inside the liver mask;
  images of one study combined, since the diagnosis is per patient.
- Split diagnosis data by datasource group from the start: [EXP-003](../experiments/EXP-003-transunet-r50-b16-from-scratch-512-and-224-lseg-cirrhosis-v4.md)
  had cirrhosis DSC 0.696 on val and 0.047 on test.
- C6's presence head doubles as a view classifier (liver, kidney, hepatorenal view) to choose the
  images a diagnosis model reads.
- Report diagnosis with STARD-AI or TRIPOD+AI ([writing.md](../../docs/writing.md)).

## Conclusion

Open. No DEC and no board task came from this session. Suggested next steps for a consult
session: P1 once TASK-233 is done (with [TASK-232](../../backlog/tasks/task-232%20-%20Liver-negative-audit-of-the-TASK-197-runs-R1-and-R4-failure-rate-per-datasource-group-and-spleen-state-on-val-and-test-and-a-training-dynamics-count-of-train-liver-negatives-fit-late-or-never-aggregate-dataset-record-DIS-049.md),
the liver-negative audit), then P2 and P3 as DECs, then tasks for C1 and C2. TASK-197 goes on
unchanged: shift test, seeds 1 and 2 of R4, and the EXP record.

## Open questions

- **Recent CV trends: for the user's next session.** Leads found by web search on 2026-11-24.
  None was read: the page fetch failed (DNS), so everything below is from search summaries and
  unverified.
  - DINOv3 for medical images: an off-the-shelf benchmark ([arXiv:2509.06467](https://arxiv.org/abs/2509.06467)),
    MedDINOv3 ([arXiv:2509.02379](https://arxiv.org/abs/2509.02379)), DINO-Med3D for 3D
    ([arXiv:2606.18886](https://arxiv.org/html/2606.18886)).
  - SAM 3 family: SAM 2 against SAM 3 on 16 medical datasets, SAM 3 stronger on ultrasound
    ([PMLR v315](https://proceedings.mlr.press/v315/chakrabarty26a.html)); Medical SAM3, vanilla
    SAM 3 degrades on medical data ([arXiv:2601.10880](https://arxiv.org/abs/2601.10880));
    MedSAM-3 ([arXiv:2511.19046](https://arxiv.org/abs/2511.19046)); UltraSAM3, SAM 3 adapted on
    about 112,000 ultrasound images ([arXiv:2607.29200](https://arxiv.org/abs/2607.29200));
    few-shot concept prompts for SAM 3 on ultrasound ([arXiv:2608.01663](https://arxiv.org/abs/2608.01663)).
  - Ultrasound foundation models and benchmarks: SonoBase / SonoCorpus, about 457,000 images from
    53 public datasets ([arXiv:2609.19230](https://arxiv.org/abs/2609.19230)); the FM_UIA 2026
    challenge baseline ([arXiv:2602.01055](https://arxiv.org/abs/2602.01055)); a fully open
    ultrasound model ([arXiv:2509.11752](https://arxiv.org/abs/2509.11752)); UltraDINO
    ([arXiv:2506.19552](https://arxiv.org/abs/2506.19552)).
  - Foundation model adaptation against task-specific training, including breast ultrasound
    ([arXiv:2611.14519](https://arxiv.org/abs/2611.14519)).
  - Domain-generalised segmentation by parameter-efficient tuning: Rein, Rein++, Causal-Tune
    ([arXiv:2512.16567](https://arxiv.org/abs/2512.16567)).
  - Partial labels: marginal loss best when more than one label is missing across domains, in
    echocardiography ([arXiv:2607.05008](https://arxiv.org/abs/2607.05008)); per-class loss
    masking for partly labelled liver CT ([PMLR v307](https://proceedings.mlr.press/v307/ostmo26a.html)).
- P1: how many training samples a relabel would touch, by group (a count for TASK-232 or a new
  data task; needs a table ask).
- P2: whether the train and val groups split into 5 folds that each hold every first-set organ,
  present and absent (a feasibility count, like [TASK-167](../../backlog/tasks/task-167%20-%20Epic-1-split-feasibility-report-on-261023-run-the-TASK-166-report-on-the-anatomy-candidate-table-at-tolerances-1-2-3-and-5-points-dataset-record-for-the-user-to-set-tolerances-and-minimum-counts-DEC-071.md) for DEC-071).
- Whether R6's kidney breakdown (fact 2) points at something in the data or only at UPerNet.
