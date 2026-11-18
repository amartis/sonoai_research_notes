---
id: DIS-032
title: Epic 1 point 1 - model task definition - per-class sigmoid with masked unknowns, or one softmax with a per-pixel allowed-class set
status: concluded
created: 2026-11-17
outcomes: [DEC-066]
related: [DEC-065, DEC-059, DEC-060, DEC-006]
---
# DIS-032: Epic 1 point 1 - model task definition

## Question

Point 1 of [DEC-065](../decisions/DEC-065-mission-upper-abdomen-anatomy-segmentation.md)
(mission: upper-abdomen anatomy segmentation): which classes, which target form, and how the
three `strict_v1` states of a sample-label pair (positive, closed negative, unknown) become
loss and score. The labels are partly known per sample: a sample can have liver positive,
kidney negative and stomach unknown.

## Options considered

**1. Output and loss.**
- **A (DEC-065 starting lean): one sigmoid output per class.** Polygon mask as target for
  positives, empty mask for closed negatives, no loss for that class's output on samples
  where it is unknown. Used by MultiTalent (Ulrich et al., MICCAI 2023,
  [arXiv:2303.14444](https://arxiv.org/abs/2303.14444), code
  [MIC-DKFZ/MultiTalent](https://github.com/MIC-DKFZ/MultiTalent)) for datasets with
  conflicting class definitions. Handles truly overlapping classes. Weak point: inside a
  liver polygon, an unknown class gets no signal at all, although the pixel is liver.
- **B (chosen; the user's proposal, "multi-state training"): one softmax over background and
  the organs, and per pixel a set S of allowed classes**; the loss rises only when the
  prediction falls outside S (cross-entropy form: -log of the summed probability of the
  classes in S). Known in the literature as label-set or marginal losses:
  Fidon et al., MICCAI 2021, [arXiv:2107.03846](https://arxiv.org/abs/2107.03846), code
  [LucasFidon/label-set-loss-functions](https://github.com/LucasFidon/label-set-loss-functions)
  (marginalized cross-entropy, marginalized Dice, leaf-Dice); Shi et al. 2020, marginal and
  exclusion loss for partially labelled multi-organ CT,
  [arXiv:2007.03868](https://arxiv.org/abs/2007.03868); Fang and Yan, IEEE TMI 2020,
  [doi:10.1109/TMI.2020.3001036](https://doi.org/10.1109/TMI.2020.3001036); Bevandić et al.
  2021, [arXiv:2108.11224](https://arxiv.org/abs/2108.11224). (Links checked 2026-11-17;
  results of the papers not re-read in full.) Strong points: uses the knowledge that a pixel
  inside one organ is no other organ; takes positives without a polygon naturally (the class
  joins the set outside the polygons). Weak points: assumes one class per pixel; uncertain
  pixels can drift into a class that is often unknown. That drift is held back by closed
  negatives (partial-label learning needs the "ambiguity degree" below 1: Cour, Sapp and
  Taskar, JMLR 2011, [jmlr.org/papers/v12/cour11a](https://jmlr.org/papers/v12/cour11a.html);
  definition taken from secondary sources) and is measured by criterion W2 of DEC-065.
- Best case for A: when thin vessels and ducts inside the liver join the class list. Then A
  is the comparison run, not the main line.

**2. Check how often first-set polygons overlap before deciding.**
- Analyst's proposal: count overlaps on `strict_v1` positives first (aggregate only).
- **Chosen: skip.** The user is sure that the large-organ outlines rarely overlap; the
  allowed-set rule takes an overlap without failing (the pixel may be either organ).

**3. Loss code.**
- **Chosen: own implementation** in `src/sonoai/training/losses.py`, with values checked
  against the reference package on synthetic data; the package is not added to the
  requirements (one fewer pin on the GPU box; our losses already handle layers and
  ignored pixels).
- Alternative: depend on the package. Would win if we wanted its full family of losses
  without porting.

**4. Spleen.** The user removed spleen from the first set (strict_v1: 961 positives with
polygon, the fewest of the five). It moves to the pool.

## Conclusion

[DEC-066](../decisions/DEC-066-epic1-model-task-label-set-softmax.md): first set liver, kidney,
stomach, gallbladder; one softmax output over background and these four; a per-pixel
allowed-class set as target; label-set losses (own code); the per-class sigmoid as one
comparison run, planned in point 6. Build work: board task [TASK-157](../../backlog/tasks/task-157%20-%20Label-set-losses-for-the-anatomy-task-per-pixel-allowed-class-bitmask-target-builder-marginalized-cross-entropy-marginalized-Dice-and-leaf-Dice-synthetic-tests-DEC-066.md) (label-set losses,
method).

## Open questions

- Which Dice form (marginalized Dice or leaf-Dice) and weights: point 6 (optimisation).
- Whether all-unknown samples and positives without a polygon enter the sample file: point 2
  (data preparation).
- Exact scoring and checkpoint rule: point 4 (metrics).
