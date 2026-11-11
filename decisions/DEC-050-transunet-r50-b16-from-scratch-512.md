---
id: DEC-050
title: Official TransUNet R50-ViT-B/16 model (get_r50_b16_config) as a new registered model, trained from scratch on lseg_cirrhosis_v4 at 512 px with a 224 px from-scratch control
status: accepted
area: [training]
created: 2026-11-11
from: [DIS-023]
related: [DEC-006, DEC-043, DEC-045, DEC-047]
superseded_by:
---
# DEC-050: TransUNet R50-ViT-B/16 from scratch at 512 px

## Context

[DIS-023](../discussions/DIS-023-transunet-r50-b16-from-scratch-at-512.md). The baseline is the
[TASK-088](../../backlog/tasks/task-088%20-%20Train-lseg_cirrhosis_v4-on-the-fixed-sample-file-and-write-the-EXP-record-DEC-043-DEC-045.md) run cirr-v4-tu-e30-r5 (recipe `261109_transunet_dec047`: timm-based `transunet`,
input 224, pretrained, SGD with Nesterov, global batch 24, 30 epochs, seed 0, no augmentation).
Our `transunet` differs from the official R50-ViT-B/16 in class token, dropout, norm eps,
shortcut norm and stem padding (DIS-023 Table 1).

## Decision

1. A new registered model, `transunet_r50_b16`, follows the official TransUNet code
   (https://github.com/Beckschen/TransUNet, `networks/vit_seg_modeling.py`,
   `vit_seg_modeling_resnet_skip.py`) with a config equal to `get_r50_b16_config()`:
   hidden 768, 12 layers, 12 heads, MLP 3072, dropout 0.1, attention dropout 0.0,
   ResNet stages (3, 4, 9) with width factor 1, decoder channels (256, 128, 64, 16),
   skip channels (512, 256, 64, 16) with n_skip 3, no class token, and
   `grid = img_size / 16` as the official `train.py` sets for R50. Initialisation as in the
   official code. Written in the repo (no vendored copy); the official repo's licence is
   checked and cited in the module docstring.
2. The new model loads no weights: `pretrained=True` is refused. Loading weights is a later
   task if wanted.
3. The existing `transunet` model is not changed.
4. Two new recipes, each equal to `261109_transunet_dec047` except the model (and input
   size): model `transunet_r50_b16`, no pretrained weights, input 512 px in one and 224 px
   in the other (the control). Optimiser, loss, schedule, global batch 24, 30 epochs,
   seed 0, sample file and per-sample matrices unchanged; no augmentation.
5. Both run on the GPU box. The exp task first checks memory at 512 px and sets
   `micro_batch` in the plan (not the recipe), so global batch 24 is kept by accumulation.
6. One EXP record compares cirr-v4-tu-e30-r5 (224, pretrained), the 224 from-scratch run and
   the 512 from-scratch run on val (selection) and test.

## Consequences

- A method task builds the model with synthetic tests; an exp task (blocked by it) adds the
  two recipes and plans, runs them in approve mode and writes the EXP record.
- The 512 run is long (estimate 25–40 h, unverified); the exp task reports the measured
  time per epoch after the first epoch.
