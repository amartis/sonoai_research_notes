---
id: DIS-023
title: TransUNet R50-ViT-B/16 (official get_r50_b16_config) from scratch at 512 px on lseg_cirrhosis_v4
status: concluded
created: 2026-11-11
outcomes: [DEC-050]
related: [DEC-006, DEC-043, DEC-045, DEC-047]
---
# DIS-023: TransUNet R50-ViT-B/16 from scratch at 512 px

## Question

The user asked for a recipe equal to `261109_transunet_dec047` (the [TASK-088](../../backlog/tasks/task-088%20-%20Train-lseg_cirrhosis_v4-on-the-fixed-sample-file-and-write-the-EXP-record-DEC-043-DEC-045.md) run
cirr-v4-tu-e30-r5: TransUNet, input 224, ImageNet-21k pretrained) but with input 512 px,
no pretrained weights, and the model built from the official TransUNet
`get_r50_b16_config()`.

## What we found

Our registered `transunet` model wraps timm's `vit_base_r50_s16_*`. Built at 512 px with no
weights it has the R50-ViT-B/16 sizes (ResNet stages 3-4-9, 12 layers, width 768,
32×32 tokens, 105.9 M parameters, checked by building it on machine01). It still differs
from the official model (checked against https://github.com/Beckschen/TransUNet,
`networks/vit_seg_configs.py`, `vit_seg_modeling.py`, `vit_seg_modeling_resnet_skip.py`,
`train.py`, read 2026-11-11):

| Item | Ours (`transunet`) | Official R50-ViT-B/16 |
|---|---|---|
| Class token | yes | none |
| Transformer dropout | 0.0 | 0.1 (MLP, after the position embedding); attention dropout 0.0 |
| GroupNorm eps / weight-standardisation eps | 1e-5 / 1e-8 | 1e-6 / 1e-5 |
| Shortcut GroupNorm groups | 32 | one group per channel |
| Stem padding | timm "same" | explicit padding 3, max pool padding 0, zero-pad features to size |
| Token grid at 512 px | 32×32 | 32×32 when `grid = img_size / 16` (as `train.py` sets for R50) |

Table 1. Our timm-based TransUNet against the official R50-ViT-B/16 at 512 px.

Two expectations, not measured: at 512 px the GPU box (RTX 3060 12 GB) probably cannot
hold micro-batch 8, and the run may take about 25–40 h (the 224 run took about 5.2 h).
A 106 M-parameter hybrid ViT from scratch on about 10k training images may do worse than
the pretrained one (unverified).

## Options considered

- **Model, A (chosen)**: a new registered model that follows the official code and config;
  `transunet` unchanged so cirr-v4-tu-e30-r5 stays reproducible.
- **Model, B**: options on the timm model (no class token, dropout 0.1); less code, still
  not exact (padding, eps, shortcut norm).
- **Model, C**: the current model with `pretrained=False`; no new code, not the official config.
- **Machine**: GPU box with a memory check and a lower plan micro-batch (chosen), or RunPod
  A100 (faster, costs money, approval per run).
- **Control run**: a 224 px from-scratch run with the same new model (chosen), so the EXP
  record can separate input size from pretraining; or only the 512 run.

## Conclusion

The user chose A, the GPU box, and the 224 control (2026-11-11). Recorded in
[DEC-050](../decisions/DEC-050-transunet-r50-b16-from-scratch-512.md); work on the board as one method
task (the model) and one exp task (two recipes, two runs, one EXP record).

## Open questions

- Loading pretrained weights into the new model is out of scope; a later task if wanted.
