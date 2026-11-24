# 2026-11-24

Per-sample, per-epoch heatmap to check suspected label errors behind a low W2 liver score on
test: is there an existing concept for it? Written by Claude (Opus 5.5) at the user's
request. A literature pointer, not a decision and not an analysis: no run file or table was
read.

Abbreviations and terms: W2, the "no phantom organs" score of epic 1 (per organ, the share of
samples where the organ is a closed negative, labelled absent, in which the model predicts
0 pixels of it; [DEC-076](../../decisions/DEC-076-epic1-metrics-label-set-score-selection-ci-and-pass-rule.md) Table 1, `docs/glossary/epic1-upper-abdomen-anatomy.md`); R1 and R4,
recipes of [DEC-077](../../decisions/DEC-077-epic1-model-choice-six-recipes.md) (R1: `transunet`, ImageNet-21k weights; R4: DINOv3 ConvNeXt-B encoder with
an MLP head); AUM, area under the margin; DSC, Dice similarity coefficient.

## Done

- The user observed that the test-split W2 liver scores of R1 and R4 were not satisfactory,
  and that both models failed on the same case, "Liver-negative" (the user's name: liver
  labelled as a closed negative). The user suspected a labeling problem and proposed a
  heatmap with samples on the x axis, epochs on the y axis and a per-sample score as colour.
- Searched the literature for this diagram and analysis style. Four papers matched (Table 1).
  Each was checked on 2026-11-24 at arXiv and the venue page; PDFs saved in
  [label-noise-training-dynamics-papers/](../../literature/label-noise-training-dynamics-papers/README.md).
- Checked what the runs may already hold: [DEC-045](../../decisions/DEC-045-per-sample-confusion-matrices-in-runs.md) rule 3 evaluates train, val and test every
  epoch and stores per-sample records keyed by sample number, when the task asks for them;
  DEC-076 rule 6.1 puts per-sample records (organ, state, predicted pixel count) into
  `seg_anatomy_v2`. Not checked: whether the R1 and R4 runs actually wrote these files for
  every epoch.

## Observations

### 1. The concept exists: training dynamics

The heatmap is a picture of **training dynamics**: how the model's fit to each sample's
label changes over epochs. Three of the papers below build label-error detectors from it;
the fourth uses agreement between out-of-sample predictions instead of epochs.

Table 1. Published methods that flag suspect labels from model behaviour per sample.

| Method | Signal recorded per sample | How a suspect label shows | Reference |
|---|---|---|---|
| Dataset Cartography ("data maps") | Mean and variability, over epochs, of the model's confidence in the given label | "Hard-to-learn" region (low mean, low variability), which the authors report often holds labeling errors | [1] |
| Forgetting events | Count of transitions from correct to wrong between epochs | Samples never learned or forgotten often; mostly atypical or noisy | [2] |
| AUM | Labelled-class logit minus the largest other logit, averaged over epochs | Low or negative AUM; a deliberately mislabelled extra class sets the cut-off | [3] |
| Confident Learning (cleanlab, open-source library) | Out-of-sample predicted probabilities (no epoch axis) | The model confidently prefers another class over the given label | [4] |

The first three are defined on **training** samples; the fourth on cross-validated
(out-of-sample) predictions. Claims in this table were checked against the abstracts in the
saved PDFs; see section 4 for what was not read.

### 2. What the heatmap can and cannot show on the test split

- On test the model never sees the label, so the plot is not training dynamics in the sense
  of [1] to [3]. It shows whether a held-out sample is predicted against its label from early
  epochs on and stays so.
- That pattern fits a label error, but also a genuinely hard sample or one from a
  distribution the model did not see (test is whole datasource groups, [DEC-071](../../decisions/DEC-071-epic1-splitting-parameterised-split-method.md)). The plot
  alone cannot separate these. Confidence: moderate, by reasoning, not tested.
- Two different models (R1, R4: different encoder, weights and decoder) failing on the same
  samples is the stronger signal; it is the reasoning of [4]. Confirming a label error needs
  someone to look at the images, which only the user does.
- A W2 label is a presence state from the presence policy ([DEC-059](../../decisions/DEC-059-fact-driven-model-sample-label-index-presence-policies.md), [DEC-060](../../decisions/DEC-060-first-presence-policies-of-261023.md)), not a drawn
  outline. If the labels are wrong, the cause may lie in the facts or in the policy that
  turned them into a closed negative, not only in an annotator's work. Unverified; a
  question for the follow-up.

### 3. Suggested design (not built)

- The per-sample no-phantom score of W2 is 0 or 1, so a heatmap of it is coarse. A
  continuous colour shows more: the predicted liver area as a share of the input area
  (the quantity behind the W2 area floors, DEC-076 rule 2), on a log scale.
- One panel per model (R1, R4), same x order for both: samples sorted by their mean over
  epochs, or grouped by presence state and datasource group.
- A strip with each sample's mean over epochs; optionally a Cartography-style scatter
  (x: variability over epochs, y: mean).
- Run the same on the **train** split: if the closed-negative liver labels are wrong there
  too, [1] or [3] find them, and fixing them also changes training.
- Use the test curves for diagnosis only, never to choose an epoch or a model (DEC-045
  rule 3: test is recorded and never used for a choice).

### 4. Limits

- Only the abstracts and venue pages were read on 2026-11-24, not the full texts. The PDFs
  are saved for a full reading.
- The fit of [1] to [3] to segmentation is not checked: they were shown on classification
  (and [1] on NLP tasks). Here the natural unit is one sample and one organ class.

## Next

- If the user wants the plot: list the tables and run files to read (per-sample records of
  the R1 and R4 runs, the epic 1 sample file's split and state columns), get the user's ok
  (patient-data rules), then build it as a notebook in `notebooks/` that calls code in
  `src/sonoai/`.
- The user looks at the flagged closed-negative liver samples in Label Studio to tell a
  label error from a hard case.
- If label errors are confirmed: a new task (Triage) on the presence facts or policy for
  liver.

## References

Checked on 2026-11-24 at arXiv and the venue page named. PDF copies (arXiv versions) in
[label-noise-training-dynamics-papers/](../../literature/label-noise-training-dynamics-papers/README.md);
file names start with the reference number.

1. Swayamdipta S, Schwartz R, Lourie N, Wang Y, Hajishirzi H, Smith NA, Choi Y. Dataset
   cartography: mapping and diagnosing datasets with training dynamics. EMNLP 2020,
   pp. 9275–9293. [doi:10.48550/arXiv.2009.10795](https://doi.org/10.48550/arXiv.2009.10795);
   [ACL Anthology 2020.emnlp-main.746](https://aclanthology.org/2020.emnlp-main.746);
   code: [github.com/allenai/cartography](https://github.com/allenai/cartography)
2. Toneva M, Sordoni A, Tachet des Combes R, Trischler A, Bengio Y, Gordon GJ. An empirical
   study of example forgetting during deep neural network learning. ICLR 2019.
   [doi:10.48550/arXiv.1812.05159](https://doi.org/10.48550/arXiv.1812.05159)
3. Pleiss G, Zhang T, Elenberg E, Weinberger KQ. Identifying mislabeled data using the area
   under the margin ranking. NeurIPS 2020.
   [doi:10.48550/arXiv.2001.10528](https://doi.org/10.48550/arXiv.2001.10528);
   [NeurIPS proceedings](https://papers.nips.cc/paper/2020/hash/c6102b3727b2a7d8b1bb6981147081ef-Abstract.html)
4. Northcutt CG, Jiang L, Chuang IL. Confident learning: estimating uncertainty in dataset
   labels. J Artif Intell Res 2021;70. [doi:10.48550/arXiv.1911.00068](https://doi.org/10.48550/arXiv.1911.00068);
   [JAIR article 12125](https://jair.org/index.php/jair/article/view/12125);
   code: [github.com/cleanlab/cleanlab](https://github.com/cleanlab/cleanlab)
