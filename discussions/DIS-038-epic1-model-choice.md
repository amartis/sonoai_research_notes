---
id: DIS-038
title: Epic 1 point 5 - model choice - which models, which run is judged, which decoder for DINOv3
status: concluded
created: 2026-11-19
outcomes: [DEC-077]
related: [DEC-065, DEC-066, DEC-069, DEC-076, DEC-050]
---
# DIS-038: Epic 1 point 5 - model choice

## Question

[DEC-065](../decisions/DEC-065-mission-upper-abdomen-anatomy-segmentation.md) point 5 asks
for the architecture and pretraining of the first anatomy model. Points 1 to 4 are settled
([DEC-066](../decisions/DEC-066-epic1-model-task-label-set-softmax.md), [DEC-069](../decisions/DEC-069-epic1-data-preparation.md), [DEC-071](../decisions/DEC-071-epic1-splitting-parameterised-split-method.md), [DEC-075](../decisions/DEC-075-epic1-split-values-tolerance-and-minimum-counts.md), [DEC-076](../decisions/DEC-076-epic1-metrics-label-set-score-selection-ci-and-pass-rule.md)). The evidence was gathered the day before in
[epic1-anatomy-segmentation-models-and-papers.md](../literature/epic1-anatomy-segmentation-models-and-papers.md)
("the note").

## Options considered

| Question | Analyst's recommendation | Chosen (the user) | When the recommendation would have won |
|---|---|---|---|
| Which models | `transunet` and DINOv3 ConvNeXt-B, chosen on val | both, plus `resenc_unet` from scratch as control | GPU time is short; the control is not needed for the mission |
| Which run is judged | the run picked by the DEC-076 selection keys on val; only its test verdict counts | a verdict for each run; the mission is met if any run passes | a single claim must not depend on test (several runs give several chances at the bar) |
| Decoder on DINOv3 | SegFormer-style MLP head, as UltraBench 2 used (the note's [1]) | all three: MLP, U-Net-style, UPerNet | the decoder difference in [1] is within the noise, so two runs could be saved |

Table 1. The three questions of point 5, the analyst's recommendation, the user's choice and
when the recommendation would have won.

Decided by the analyst and told to the user:

- DINOv3 encoder size ConvNeXt-B, not L: L scored 0.822 against 0.820 for B in [1] (SE 0.007)
  at a larger size, on a 12 GB GPU; ConvNeXt variants ranked above the ViT ones in [1].
- The new model normalises its input with its weights' mean and std inside `forward`.
- `transunet` keeps the input it had in [EXP-003](../experiments/EXP-003-transunet-r50-b16-from-scratch-512-and-224-lseg-cirrhosis-v4.md) ([0, 1], while its weights' config says
  mean = std = 0.5); this mismatch becomes a Triage task, not a change here, so M1 stays the
  model already shown to train.
- All five runs are trained whatever earlier runs score; the EXP record names the run val
  would pick and says that five runs gave five chances at the bar.

The analyst said once, plainly, that a verdict for each run makes a pass more likely by
chance than a single pre-picked run; the user kept that choice.

## Conclusion

[DEC-077](../decisions/DEC-077-epic1-model-choice-five-runs.md) (five runs, a verdict for each).
Board tasks: listed in DEC-077 Consequences; the training task comes with point 6.

## Open questions

- Should `transunet` normalise its input to its weights' mean and std (0.5, 0.5)? Changing it
  makes new runs not comparable with EXP-003. Triage task.
- Point 6: the recipe for pretrained encoders (frozen start, encoder learning rate) and seeds.
