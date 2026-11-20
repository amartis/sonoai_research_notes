---
id: DEC-077
title: Epic 1 point 5 - model choice - six recipes (transunet pretrained and from scratch, resenc_unet from scratch, DINOv3 ConvNeXt-B with three decoders); the epic succeeds if any recipe meets the bar
status: accepted
area: [training]
created: 2026-11-19
from: [DIS-038]
related: [DEC-065, DEC-066, DEC-069, DEC-076, DEC-050, DEC-006, DEC-003]
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
datasources, so the choice can only be settled by our own runs. A **recipe** is what to train
([DEC-003](DEC-003-trainrecipe-files-structure.md)). Discussion:
[DIS-038](../discussions/DIS-038-epic1-model-choice.md).

## Decision

### 1. Six recipes

| Recipe | Registered model | Encoder weights at start | Decoder | Code to add |
|---|---|---|---|---|
| R1 | `transunet`, input normalised | ImageNet-21k (timm `vit_base_r50_s16_224.orig_in21k`, the model's default weights) | TransUNet cascaded upsampler | input normalisation (rule 3) |
| R2 | `transunet`, input normalised | none (from scratch) | same as R1 | same as R1 |
| R3 | `resenc_unet` | none (from scratch); 6 stages at 224 px | nnU-Net residual-encoder U-Net decoder | none |
| R4 | `dinov3_convnext_seg`, `decoder: mlp` | DINOv3 ConvNeXt-B (timm `convnext_base.dinov3_lvd1689m`) | SegFormer-style MLP head | new model |
| R5 | `dinov3_convnext_seg`, `decoder: unet` | same as R4 | U-Net-style: x2 upsampling blocks with skip concatenation over the four stages, then up to full size; channels as the `transunet` decoder (256, 128, 64, 16) | same new model |
| R6 | `dinov3_convnext_seg`, `decoder: upernet` | same as R4 | UPerNet (pyramid pooling on the last stage plus a feature pyramid; own code, no new package) | same new model |

Table 1. The six recipes of point 5, with their model, starting weights, decoder and the code
each needs. R1 and R2 separate the effect of pretraining on one model; R3 is a from-scratch
U-Net control; R4 to R6 compare decoders on one encoder (all the user's choices).

### 2. Which DINOv3: ConvNeXt-B

The DINOv3 encoder is **ConvNeXt-B** (`convnext_base.dinov3_lvd1689m`): 87.6 M parameters,
feature maps of 128, 256, 512 and 1,024 channels at strides 4, 8, 16 and 32 (checked in timm
1.0.30 on machine01, 2026-11-19); weights public, not gated, 350 MB (Hugging Face metadata,
same day). Why: in UltraBench 2 (the note's [1], Table 2) DINOv3 ConvNeXt variants ranked
above its ViT variants; ConvNeXt-L scored 0.822 against 0.820 for B (SE 0.007), with 196.2 M
encoder parameters against 87.6 M (timm, same check), on a 12 GB RTX 3060. Small and tiny
exist in timm but are not in the note's table.

### 3. Input normalisation

The reader gives every model 3-channel images in [0, 1] and stays the same. Each pretrained
encoder's model normalises its input inside `forward` with its weights' mean and std:

- `dinov3_convnext_seg`: ImageNet mean 0.485, 0.456, 0.406 and std 0.229, 0.224, 0.225.
- `transunet`: mean = std = 0.5 (its weights' timm config), for R1 and also for R2, so that
  R1 and R2 differ only in the starting weights (the user's choice: the best option for
  `transunet` in epic 1). This is a model argument; recipes that do not set it behave as
  before. Comparison with the cirrhosis runs of [EXP-003](../experiments/EXP-003-transunet-r50-b16-from-scratch-512-and-224-lseg-cirrhosis-v4.md)
  is not needed (the user).
- `resenc_unet` (from scratch, instance norm): no change.

### 4. Same recipe settings for all

All six recipes use the training settings of point 6 (optimisation). If point 6 gives
pretrained encoders their own settings (for example a frozen start and a lower encoder learning
rate, as the note suggests), they apply alike to R1 and R4 to R6. Seeds: point 6.

### 5. Success of the epic (the user's choice)

1. Every recipe of Table 1 is trained and tested; each gets its own DEC-076 rule 5 verdict on
   test, on its checkpoint selected on val (DEC-076 rule 3).
2. The epic succeeds (DEC-065 section 1) when at least one recipe meets W1, W2 and W3.

### 6. Not in this point

- Ultrasound-specific encoders (URFM, OpenUS, SAMUS; the note's Table 3) come only if no
  recipe meets the bar, through a new consult session.
- Prompt-based segmenters (SAM, MedSAM, UltraSam) and `transunet_r50_b16`: not used (the
  note's Section 4; EXP-003). `swin_unet`: no recipe here.

## Consequences

- DEC-065 Table 3 row 5 lean ("a pretrained model already in the registry") is extended to
  the six recipes of Table 1.
- Board: [TASK-185](../../backlog/tasks/task-185%20-%20Epic-1-models-dinov3_convnext_seg-DINOv3-ConvNeXt-B-encoder-with-an-MLP-U-Net-style-or-UPerNet-decoder-input-normalised-inside-the-model-and-an-input-normalisation-option-for-transunet-synthetic-tests-DEC-077.md) (models: `dinov3_convnext_seg` with three decoders
  and `transunet` input normalisation, method) and [TASK-186](../../backlog/tasks/task-186%20-%20DINOv3-ConvNeXt-B-weights-on-the-GPU-box-download-timm-convnext_base.dinov3_lvd1689m-on-machine01-with-aria2c-copy-to-the-boxs-Hugging-Face-cache-check-offline-loading-there-with-the-transunet-weights-DEC-077.md) (DINOv3
  ConvNeXt-B weights to the GPU box, infra). The training task for the six recipes is created
  in the point 6 session, after its DEC.
- GPU time: six runs or more (seeds: point 6). EXP-003 took about 5 h per 30-epoch run at
  224 px on the cirrhosis set; the anatomy set's time per run is not known yet.
- Reversal: all rules apply before the first run; adding or dropping a recipe is cheap.
- [DEC-079](DEC-079-epic1-brightness-robustness-augmentation-percentile-norm-shift-test.md) (brightness robustness, 2026-11-20): all six recipes train with
  `us_bright_v1`, and rule 3 is preceded by the per-image percentile normalisation of DEC-079
  rule 2.
