---
id: DEC-066
title: Epic 1 point 1 - model task definition - four organs, one softmax output, a per-pixel allowed-class set as target, label-set losses
status: accepted
area: [training]
created: 2026-11-17
from: [DIS-032]
related: [DEC-065, DEC-059, DEC-060, DEC-061, DEC-006]
superseded_by:
---
# DEC-066: Epic 1 point 1 - model task definition (label-set softmax)

## Context

[DEC-065](DEC-065-mission-upper-abdomen-anatomy-segmentation.md) (mission: upper-abdomen
anatomy segmentation) leaves the final class list, the target form and the use of the three
`strict_v1` states (positive, closed negative, unknown) to this point. Its rule 4.2 holds:
an unknown pair is never background. Options and sources:
[DIS-032](../discussions/DIS-032-epic1-model-task-definition-label-set-loss.md).

## Decision

1. **Classes.** Background plus four organs: `liver`, `kidney`, `stomach`, `gallbladder`
   (K = 5 outputs). `spleen` leaves the first set and joins the pool (the user's choice).
   The bar of DEC-065 section 2 now reads: liver DSC ≥ 0.85, kidney, stomach and gallbladder
   ≥ 0.70.
2. **Output.** One softmax over the K = 5 channels per pixel; the predicted label is the
   argmax.
3. **Target: an allowed-class set per pixel**, S ⊆ {background, liver, kidney, stomach,
   gallbladder}, stored as a bitmask (bit 0 background, bit k organ k). For one sample, with
   each organ's `strict_v1` state:
   - a. pixel inside the polygon of one or more positive organs: S = those organs;
   - b. pixel outside every positive polygon: S = {background} ∪ {organs unknown for this
     sample} ∪ {organs positive but without a polygon};
   - c. an organ that is a closed negative for the sample is never in S;
   - d. S is never empty (b always holds background).
   - Assumption: a positive organ's polygons cover all of it in the crop, so the organ is not
     in S outside them. Point 2 may revise this if labels show partial outlines.
4. **Loss: label-set losses.** Cross-entropy part: -log Σ_{c∈S} p_c (marginalized
   cross-entropy). Dice part: marginalized Dice or leaf-Dice (Fidon et al., MICCAI 2021,
   [arXiv:2107.03846](https://arxiv.org/abs/2107.03846)); the choice and weights are point 6.
   A pixel whose S holds all five classes adds no loss.
5. **Code.** Own implementation in `src/sonoai/training/losses.py`, registered by name;
   synthetic tests check it against values from the reference implementation
   ([LucasFidon/label-set-loss-functions](https://github.com/LucasFidon/label-set-loss-functions)),
   which is not added to the requirements.
6. **Score.** Per sample and organ: DSC (Dice similarity coefficient) of the argmax mask
   against the polygon mask where the organ is positive with a polygon (W1); no predicted
   pixel of the organ where it is a closed negative (W2); nothing where it is unknown.
   Details and the checkpoint rule: point 4.
7. **Comparison.** One sigmoid output per class with unknown outputs masked out (the
   DEC-065 starting lean) is one comparison run, planned in point 6; its code is a task then.
8. **No overlap check.** First-set polygons are taken to overlap rarely (the user's
   judgement, not measured); rule 3a takes an overlap without failing.

## Consequences

- DEC-065 Table 2: `spleen` moves from first set to pool. Sections 1, 4 and 5 of DEC-065 are
  unchanged.
- Board: [TASK-157](../../backlog/tasks/task-157%20-%20Label-set-losses-for-the-anatomy-task-per-pixel-allowed-class-bitmask-target-builder-marginalized-cross-entropy-marginalized-Dice-and-leaf-Dice-synthetic-tests-DEC-066.md) (label-set losses and the bitmask target builder, method) can start now; it
  needs no real data.
- Points 2 (data preparation), 4 (metrics) and 6 (optimisation) start from rules 3, 6 and 4.
