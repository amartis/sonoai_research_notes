---
id: DIS-066
title: "Parked ideas after DIS-065: survival groups, classifier head, box detector"
status: parked
created: 2026-11-26
outcomes: []
related: [DIS-065, DEC-113, DEC-112, DEC-110, DEC-100, DEC-004, DEC-045, DEC-062]
---
# DIS-066: Parked ideas after DIS-065 - survival groups, classifier head, box detector

## Question

After [DIS-065](DIS-065-epic3-metrics-and-keeping-several-checkpoints.md) (epic 3 metrics and
keeping several checkpoints) concluded, the user (2026-11-26) asked about three further ideas for
epic 3 ([DEC-100](../decisions/DEC-100-epic3-mission-spot-liver-diseases.md), epic 3 mission: spot
liver diseases). Each idea separates two jobs: saying whether a class is present in an image
(image-level, judged by AUC) and drawing its outline (judged by Dice, and maybe HD95, the 95th
percentile Hausdorff distance). The user then chose to keep the original plan,
[DEC-113](../decisions/DEC-113-checkpoint-selection-by-removing-beaten-checkpoints.md) (keep several
checkpoints, remove the beaten ones) as accepted, and to park the ideas here with one board task each.

## Options considered

### Idea 1: two survival groups and a pair of checkpoints in the product

The user's proposal. Run the DEC-113 rules in two separate groups instead of one mixed group:

- **Assessor group**: judged only on image-level AUC per class (weights inside the group: hepatoma
  0.30; hemangioma, cyst and stone 0.20 each; ascites 0.10, left out while it has fewer than 15
  validation positives, DEC-113 rule 5).
- **Drawer group**: judged only on Dice on positives per class, same weights; HD95 stored as
  information.

The product combines one checkpoint of each group:

| Step | Checkpoint | What it does |
|---|---|---|
| 1 | Assessor | Says whether the class is present: top-50 image score ([DEC-112](../decisions/DEC-112-epic3-metrics-image-score-stone-scoring-cirrhosis-bar.md) rule 1) against the threshold fixed on validation |
| 2 | Drawer | Draws the outline only where the assessor said yes, class by class |
| 3 | Fallback | The assessor says yes and the drawer draws nothing: the assessor's own outline, marked as a fallback |

Table 1. The proposed two-checkpoint product (analyst's proposal on the user's idea).

- For: each role keeps its best checkpoint (in the single DEC-113 group, the best-AUC checkpoint can
  be removed by one that wins enough Dice without reaching a veto step); criteria in a group are of
  one kind; it matches the product's two jobs.
- Against or open: the bar (DEC-112 rule 4) must be read on the pair, as one primary pair named on
  validation before any test result, with a "gated Dice" (the drawer's outline kept only where the
  assessor said yes; a miss by the assessor counts as Dice 0); two forward passes in serving; two
  checkpoints to version. Dice measures overlap, not how smooth an outline looks; HD95 is closer to
  outline quality.
- Best alternative: keep the DEC-113 single group and name two primaries among its survivors
  (cheaper, but the best assessor may already be removed).

### Idea 2: one model with two heads (segmentation plus image-level classification)

The user's question. Add a small image-level head to the epic 3 segmentation model (pooling on the
deepest encoder features, one sigmoid per spot class and ascites); training loss = segmentation loss
+ lambda x binary cross-entropy on the image labels.

- For: the image decision gets its own trained output and loss, with direct pressure against false
  positives on negative images. Storing both the head score and the top-50 score per sample lets one
  run compare them on the same checkpoints. The two heads may peak at different epochs, which idea 1
  handles (assessor group on the head's AUC, drawer group on Dice).
- Main risk, shortcut learning: an image-level head can learn the look of a site or device instead
  of the lesion. Epic 3 validation hepatoma positives (193) sit in fewer than 5 datasource groups, the
  largest holding 68% ([DIS-065](DIS-065-epic3-metrics-and-keeping-several-checkpoints.md), Facts
  used); DEC-100 records a cirrhosis model that fell from 0.696 Dice on validation to 0.047 on test.
  The top-50 score is tied to where the model draws; the head is not. Checks if tried: AUC per
  datasource group, and how often the head says yes where the segmentation draws nothing.
- The head adds information only from samples that have an image label and no outline; whether
  such samples exist was not checked (the user was not asked to read a table).
- Records: departs from [DEC-110](../decisions/DEC-110-epic3-task-form-allowed-class-sets-stone-takes-the-overlap.md)
  rule 5 (image score from the pixel probabilities) and DEC-112 rule 1 (top-50 score); a yes needs a
  new DEC and maybe a new task version ([DEC-004](../decisions/DEC-004-training-tasks.md), training
  tasks; not checked).
- Proposed form if tried: a comparison run after the first one-head run, on the same recipe, like
  the sigmoid comparison run of DEC-110 rule 7.

### Idea 3: box detection plus segmentation

The other reading of "detection": a detector with a box head and a mask head, one score and one
outline per lesion (as Mask R-CNN).

- For: handles several lesions per image; false positives can be counted per lesion.
- Against: a much larger change (boxes made from outlines, lesion-level measures beside the DEC-112
  measures, a new task form). The repo already has a box detector, FCOS for bmode_det v1
  ([DEC-062](../decisions/DEC-062-bmode-box-detector-bmode-det-v1.md) item 1), which could be a starting point.

### HD95

Suggested with ideas 1 and 2: store HD95 per class on positives as information. Rules needed first:
a fixed cap when the prediction is empty (HD95 is undefined then); pixels at the 512 input, not mm,
because pixel spacing differs between devices. HD95 also punishes small far-away blobs inside
positive images, which an image-level gate does not remove.

## Related work

Checked by web search on 2026-11-26 (titles and abstracts or search summaries, not full papers):

| Work | What it does | Link |
|---|---|---|
| Classify, then segment | SIIM-ACR pneumothorax challenge (2019): a review says the second-place team separated classification from segmentation | [scitepress 2021](https://www.scitepress.org/Papers/2021/101854/101854.pdf) |
| Localise, then segment, breast ultrasound | a two-stage pipeline said to reduce false positives | [CEUR Vol-4164 paper 27](https://ceur-ws.org/Vol-4164/paper27.pdf) |
| Y-Net (Mehta et al., MICCAI 2018) | U-Net with an added classification branch, breast biopsy slides | [arXiv 1806.01313](https://arxiv.org/abs/1806.01313) |
| Zhou et al., Medical Image Analysis 70:101918 (2021) | joint segmentation and classification of tumours in 3D breast ultrasound; abstract reports both improved over single-task models | [record](https://pure.korea.ac.kr/en/publications/multi-task-learning-for-segmentation-and-classification-of-tumors/) |
| Mask R-CNN (He et al. 2017) | box head and mask head on one network | [arXiv 1703.06870](https://arxiv.org/abs/1703.06870) |
| Per-task checkpoints in multi-task learning | each branch keeps the checkpoint best on its own validation measure | [arXiv 2610.41134](https://arxiv.org/pdf/2610.41134), [MSFT, arXiv 2603.21606](https://arxiv.org/html/2603.21606) |
| ELECTRE outranking | weighted agreement index against a cut level (0.5 to 1), indifference and veto thresholds; the DEC-113 rule is close to it | [R MCDA ELECTRE3](https://search.r-project.org/CRAN/refmans/MCDA/html/ELECTRE3.html), [arXiv 2511.09120](https://arxiv.org/pdf/2511.09120) |
| Shortcut learning (Geirhos et al. 2020) | models solving a task through an unintended cue | [doi:10.1038/s42256-020-00257-z](https://doi.org/10.1038/s42256-020-00257-z) |

Table 2. Work related to the three ideas. No paper was found that picks two checkpoints of the same
run for the two jobs (idea 1); its parts are established.

## Conclusion

Parked by the user on 2026-11-26: the original plan stands (DEC-113 as accepted; its code task
[TASK-288](../../backlog/tasks/task-288%20-%20Checkpoint-selection-mode-that-keeps-several-checkpoints-and-removes-the-beaten-ones-weighted-criteria-floors-steps-removal-threshold-veto-near-copy-rule-cap-primary-by-weighted-sum-set-by-the-recipe-synthetic-tests-DEC-113.md), selection mode that removes beaten checkpoints, unchanged). One Parked board task per idea,
label `needs-decision`:

- [TASK-289](../../backlog/tasks/task-289%20-%20Decide-whether-checkpoint-selection-keeps-two-survival-groups-image-level-AUC-group-Dice-group-and-the-product-serves-a-pair-of-checkpoints-DIS-066.md)
  (idea 1, two survival groups and a pair of checkpoints). Reopen when the first epic 3 run with
  DEC-113 selection shows that the best image-level checkpoint and the best drawing checkpoint differ
  or are removed.
- [TASK-290](../../backlog/tasks/task-290%20-%20Decide-whether-to-try-a-two-head-model-for-epic-3-segmentation-plus-an-image-level-classification-head-as-a-comparison-run-after-the-first-one-head-run-DIS-066.md)
  (idea 2, two-head model). Reopen when the first epic 3 one-head run is done and its false positives
  on negative images are known.
- [TASK-291](../../backlog/tasks/task-291%20-%20Decide-whether-to-try-box-detection-plus-segmentation-one-score-and-one-mask-per-lesion-for-the-epic-3-spot-classes-DIS-066.md)
  (idea 3, box detection plus segmentation). Reopen when idea 2 is tried, or images with several
  lesions turn out to matter for the product.

## Open questions

- Do samples exist with an image-level label and no outline (decides how much idea 2 can gain)?
  Answering needs a table read, with the user's ok.
- HD95 rules (empty-prediction cap, units) if HD95 is added.
