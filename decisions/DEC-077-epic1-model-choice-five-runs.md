---
id: DEC-077
title: Epic 1 point 5 - model choice - five runs (transunet, resenc_unet from scratch, DINOv3 ConvNeXt-B with three decoders), a test verdict for each
status: proposed
area: [training]
created: 2026-11-19
from: [DIS-038]
related: [DEC-065, DEC-066, DEC-069, DEC-076, DEC-050, DEC-006]
superseded_by:
---
# DEC-077: Epic 1 point 5 - model choice

## Context

[DEC-065](DEC-065-mission-upper-abdomen-anatomy-segmentation.md) (mission: upper-abdomen
anatomy segmentation) point 5 asks for the architecture and pretraining of the first anatomy
model. Fixed before: background plus four organs, one softmax, label-set losses
([DEC-066](DEC-066-epic1-model-task-label-set-softmax.md)); input 224 x 224
([DEC-069](DEC-069-epic1-data-preparation.md)); the W1, W2, W3 score, checkpoint selection on
val and the pass rule ([DEC-076](DEC-076-epic1-metrics-label-set-score-selection-ci-and-pass-rule.md)).
Evidence: the literature note
[epic1-anatomy-segmentation-models-and-papers.md](../literature/epic1-anatomy-segmentation-models-and-papers.md)
(2026-11-18; "the note" below). No paper found there tests any candidate on unseen ultrasound
datasources, so the choice can only be settled by our own runs. Discussion:
[DIS-038](../discussions/DIS-038-epic1-model-choice.md).

## Decision

### 1. Five runs

| Run | Registered model | Encoder weights at start | Decoder | Code to add |
|---|---|---|---|---|
| M1 | `transunet` | ImageNet-21k (timm `vit_base_r50_s16_224.orig_in21k`) | TransUNet cascaded upsampler | none |
| M2 | `resenc_unet` | none (from scratch); 6 stages at 224 px | nnU-Net residual-encoder U-Net decoder | none |
| M3 | `dinov3_convnext_seg`, `decoder: mlp` | DINOv3 ConvNeXt-B (timm `convnext_base.dinov3_lvd1689m`) | SegFormer-style MLP head | new model |
| M4 | `dinov3_convnext_seg`, `decoder: unet` | same as M3 | U-Net-style: x2 upsampling blocks with skip concatenation over the four stages, then up to full size; channels as the `transunet` decoder (256, 128, 64, 16) | same new model |
| M5 | `dinov3_convnext_seg`, `decoder: upernet` | same as M3 | UPerNet (pyramid pooling on the last stage plus a feature pyramid; own code, no new package) | same new model |

Table 1. The five runs of point 5, with their model, starting weights, decoder and the code
each needs. M2 is the from-scratch control: it shows what pretraining adds (the user's
choice). M3 to M5 compare decoders on one encoder (the user's choice).

### 2. Which DINOv3: ConvNeXt-B

The DINOv3 encoder is **ConvNeXt-B** (`convnext_base.dinov3_lvd1689m`): 87.6 M parameters,
feature maps of 128, 256, 512 and 1,024 channels at strides 4, 8, 16 and 32 (checked in timm
1.0.30 on machine01, 2026-11-19); weights public, not gated, 350 MB (Hugging Face metadata,
same day). Why: in UltraBench 2 (the note's [1], Table 2) DINOv3 ConvNeXt variants ranked
above its ViT variants; ConvNeXt-L scored 0.822 against 0.820 for B (SE 0.007), with 196.2 M
encoder parameters against 87.6 M (timm, same check), on a 12 GB RTX 3060. Small and tiny exist in timm but are
not in the note's table.

### 3. Input normalisation

The reader gives every model 3-channel images in [0, 1]. `dinov3_convnext_seg` applies its
weights' own mean and std (ImageNet: 0.485, 0.456, 0.406 / 0.229, 0.224, 0.225) inside
`forward`, so the reader stays the same. `transunet` stays as trained in
[EXP-003](../experiments/EXP-003-transunet-r50-b16-from-scratch-512-and-224-lseg-cirrhosis-v4.md):
it gets [0, 1] although its weights' config says mean = std = 0.5. That is not changed here;
a Triage task records it.

### 4. Same recipe for all runs

All five runs use the recipe of point 6 (optimisation). If point 6 gives pretrained encoders
their own settings (for example a frozen start and a lower encoder learning rate, as the note
suggests), they apply alike to M1, M3, M4 and M5. Seeds: point 6.

### 5. A verdict for each run (the user's choice)

1. Each run's checkpoint selected on val (DEC-076 rule 3) gets its own DEC-076 rule 5 verdict
   on test.
2. The mission (DEC-065 section 1) is met when at least one run meets W1, W2 and W3.
3. All five runs are trained and tested, whatever an earlier run scored, so no run is added
   or dropped because of a test result.
4. The EXP record also says which run the DEC-076 selection keys (val mean W1, then val mean
   W2, then val loss) would pick, and that five runs gave five chances at the bar, with no
   correction for that.

### 6. Not in this point

- Ultrasound-specific encoders (URFM, OpenUS, SAMUS; the note's Table 3) come only if no
  run meets the bar, through a new consult session.
- Prompt-based segmenters (SAM, MedSAM, UltraSam) and `transunet_r50_b16` from scratch: not
  used (the note's Section 4; EXP-003). `swin_unet`: no run here.

## Consequences

- DEC-065 Table 3 row 5 lean ("a pretrained model already in the registry") is extended: one
  registry model (M1), one from-scratch control (M2) and one new pretrained encoder (M3 to M5).
- Board: a method task for `dinov3_convnext_seg` (three decoders, normalisation inside,
  synthetic tests), and an infra task to bring its weights to the GPU box. The training task
  for the five runs is created in the point 6 session, after its DEC.
- GPU time: five runs instead of one. EXP-003 took about 5 h per 30-epoch run at 224 px on
  the cirrhosis set; the anatomy set's time per run is not known yet.
- Reversal: all rules apply before the first run; dropping or adding a run is cheap until
  test results are seen. After that, rule 5.3 holds for this round.
