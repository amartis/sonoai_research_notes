# 2026-11-19

Optimiser choice by architecture: reasoning log and a short study. Written by Claude
(Opus 5.5) at the user's request. Input for [DEC-065](../../decisions/DEC-065-mission-upper-abdomen-anatomy-segmentation.md) point 6 (optimisation); not a decision.

## Done

- Answered two questions from the user: (1) AdamW or SGD with Nesterov momentum (weight
  decay 1e-4, lr 1e-3, poly 0.9) for DINOv3 ConvNeXt-B (`convnext_base.dinov3_lvd1689m`,
  recipes R4 to R6 of [DEC-077](../../decisions/DEC-077-epic1-model-choice-six-recipes.md)); (2) which optimisers suit the `transunet` recipes (R1
  pretrained, R2 from scratch) for point 6.
- Checked the claims of both answers against the papers on the web, and studied the user's
  summary: "AdamW works better for transformer models; SGD + Nesterov is a strong candidate
  for traditional CNNs".

Abbreviations: SGD, stochastic gradient descent; AdamW, Adam with decoupled weight decay;
lr, learning rate; LLRD, layer-wise lr decay; BN, IN, LN: batch, instance and layer
normalisation; ViT, vision transformer; ID and OOD, in and out of distribution; EMA,
exponential moving average of weights; SWAD, dense stochastic weight averaging; LP-FT,
linear probing then fine-tuning; DSC, Dice similarity coefficient.

## Observations

### 1. Reasoning log

**Question 1: DINOv3 ConvNeXt-B.**

1. Read DEC-077 (six recipes; rule 4: one set of point-6 settings, applied alike to R1 and
   R4 to R6), `src/sonoai/training/optim.py` (only `sgd` is registered: no AdamW, no
   parameter groups, no LLRD, no warm-up), and the epic 1 literature note
   (`literature/epic1-anatomy-segmentation-models-and-papers.md`). The note records that
   UltraBench 2 fine-tuned all 16 encoders with AdamW, a frozen encoder for the first 1,000
   steps, then the encoder at 0.01 times the head lr with LLRD.
2. Arguments, in order: ConvNeXt has LN, a patchify stem and layer scale, and was trained
   with AdamW; Kumar et al. 2024 found AdamW ahead of SGD OOD for ConvNeXt; our W3 bar is
   OOD (unseen datasources); the SGD setting has one lr for a random decoder and a
   pretrained encoder and no warm-up; AdamW's extra state is about 0.35 GB for 87.6 M
   parameters (87.6 M × 4 bytes; arithmetic, not a source).
3. Answer: AdamW, decoder lr about 1e-4, encoder 0.1 times that or stage-wise LLRD, weight
   decay 0.05 without decay on 1-D parameters, warm-up or frozen start, then poly 0.9. If SGD
   is kept: freeze the stem, add warm-up, sweep the lr.

**Question 2: `transunet` (R1, R2).**

1. Read DEC-065 row 6 (lean: [DEC-006](../../decisions/DEC-006-losses-optim-tracking.md) defaults), DEC-006 (`SGD_DEFAULTS` from the official
   TransUNet trainer, marked unverified there), [EXP-003](../../experiments/EXP-003-transunet-r50-b16-from-scratch-512-and-224-lseg-cirrhosis-v4.md) Tables 1 and 4, and
   `src/sonoai/models/transunet.py` (timm `vit_base_r50_s16_224`: a ResNet-50 front end,
   then ViT-B; BN in the decoder).
2. EXP-003 (cirrhosis task, SGD + Nesterov, lr 1e-3, poly) showed that SGD trains this
   family in distribution: the pretrained `transunet` reached train DSC 0.939 at epoch 30
   and its best val DSC 0.696 at epoch 17; the from-scratch `transunet_r50_b16` reached
   0.611 at epoch 14. All three runs failed on test (DSC 0.025 to 0.047). The limit there
   was generalisation to unseen datasource groups, not convergence.
3. What changed from answer 1: the hybrid's convolutional front end weakens the case for
   AdamW (Xiao et al. 2021), so for R1 and R2 the reason for AdamW is uniformity across
   recipes (DEC-077 rule 4; R1 against R2 must differ only in starting weights), not that
   SGD fails.
4. Answer: AdamW for R1, R2 and R4 to R6; R3 (`resenc_unet`) may keep nnU-Net's SGD; add
   SWAD or EMA weight averaging, with the BN statistics recomputed after averaging; flag
   the R1 against R2 recipe conflict for point 6.

**What was checked and what was from memory.** Table 1 lists each specific claim of the two
answers and its status after the check of this note.

Table 1. Claims made in the two answers, and their status after checking the sources
(Section 2 and References).

| Claim in the answers | Status after checking |
|---|---|
| ConvNeXt's ADE20K fine-tune used AdamW, lr 1e-4, weight decay 0.05, LLRD 0.9 | Partly wrong. ConvNeXt's paper swept lr {8e-5, 1e-4} and LLRD {0.8, 0.9} and follows the BEiT and Swin settings; its own text states neither optimiser nor weight decay [8]. AdamW, 1e-4, 0.05 came from a later paper that reused the setup |
| Kumar et al.: AdamW "clearly" better OOD for ConvNeXt and ViTs | Overstated. ConvNeXt-B OOD 79.5 against 77.3 (+2.2); CLIP ViT-B/16 +8.1; supervised ViT-B/16 about −0.2, DINO ViT-B/16 about +2.5 (the last two read through a tool summary of the tables, not verbatim) [7] |
| Freezing the first layer lets SGD match AdamW (OOD 76.7 against 76.0) | Confirmed [7]. For ConvNeXt the frozen part is the 4 × 4 stride-4 stem; whether the first stage is frozen too is stated inconsistently in the paper |
| Conv front end cuts ViT's SGD gap from up to 10% to under 0.2% | Confirmed (ImageNet, in distribution) [6] |
| Official TransUNet SGD lr 1e-2 | Confirmed: lr 0.01, momentum 0.9, weight decay 1e-4, batch 24 [9]. Nesterov and the lr schedule are not stated in the paper |
| nnU-Net: SGD, lr 1e-2, momentum 0.99 | Confirmed, Nesterov, poly power 0.9, 1,000 epochs of 250 mini-batches [13]. Weight decay (said 3e-5) was not found in the text read: unverified |
| UNETR: AdamW, lr 1e-4 | Confirmed [11] |
| ViT-B LLRD 0.75 to 0.9 (MAE, BEiT) | MAE: 0.75, read through a tool summary only [14]; BEiT not checked |
| SWAD: +1.6% on average over five benchmarks | Confirmed [16] |
| SAM costs about twice as much per step | Not checked this session (two forward-backward passes per step is how SAM works, but no source was read) |

### 2. Study: AdamW against SGD with momentum, by architecture

**Short answer.** The user's summary holds as a default, with three limits. What decides it
is the stem, the normalisation and fine-tuning against training from scratch, more than
attention against convolution:

- **Holds.** Transformers are hard for SGD (Section 2.1). For classic CNNs with BN or IN,
  SGD with (Nesterov) momentum is the long-standing default and stays competitive
  (Section 2.2).
- **Limit 1: a modern CNN behaves like a transformer here.** ConvNeXt (LN, patchify stem)
  was trained with AdamW and fine-tunes better with it OOD [7, 8].
- **Limit 2: a convolutional front end makes a ViT easy for SGD** [6], and in fine-tuning
  the gap sits in the first layer: freeze it and SGD matches AdamW [7].
- **Limit 3: AdamW is not worse on classic CNNs once weight decay is decoupled** [5], and
  the best ResNet-50 recipe in timm uses LAMB, an adaptive optimiser [15]. The difference
  between the two families is often small for classic CNNs.

#### 2.1 Why Adam(W) helps transformers

- Zhang J. et al. [1]: stochastic gradient noise is heavy-tailed for BERT and well
  concentrated for ResNet-50; heavy-tailed noise is one cause of SGD's weaker results, and
  clipping or adaptive steps address it.
- Kunstner et al. [2]: noise is not the main factor. The gap grows with batch size, and in
  full batch sign descent with momentum closes most of it; Adam with large batches behaves
  like sign descent.
- Zhang Y. et al. [3]: the Hessian spectrum differs strongly between parameter blocks in
  every transformer examined, but not in CNNs. One lr for all blocks (SGD) is the bottleneck;
  per-block step sizes (Adam) remove it.

The three papers disagree on the mechanism but agree that the gap is a property of
transformer blocks, not of vision or language data.

#### 2.2 Classic CNNs and SGD

- Wilson et al. [4]: on several deep models, solutions found by adaptive methods
  generalised worse than SGD's, often much worse, even with better training loss. This is
  Adam with coupled (L2) weight decay.
- Loshchilov and Hutter [5]: decoupling weight decay from the gradient step lets Adam
  compete with SGD with momentum on image classification, where it was outperformed before.
- Wightman et al. [15]: the timm ResNet-50 procedures A1 to A3 use LAMB (A1: lr 5e-3,
  weight decay 0.01, 600 epochs, ImageNet top-1 80.4%). They report convergence trouble with
  SGD under their binary cross-entropy loss, and cite similar AdamW and SGD results for
  ResNet-50 from earlier work. No controlled SGD against LAMB comparison is given.
- Kumar et al. [7], fine-tuning: AdamW and SGD perform comparably on BiT ResNet-50 (OOD
  73.6 against 73.1) and BiT ResNet-101 (74.5 against 74.6).

#### 2.3 The stem and normalisation decide it

- Xiao et al. [6]: ViT with a patchify stem is sensitive to optimiser (AdamW against SGD),
  hyperparameters and schedule length; with SGD it lost up to 10% top-1. A stem of about 5
  stacked stride-2 3 × 3 convolutions cut the SGD gap to under 0.2% and made training stable.
- Kumar et al. [7]: large AdamW over SGD gaps occur when fine-tuning gradients in the first
  ("embedding") layer are much larger than in the rest. Freezing it (under 1% of the
  parameters) gives SGD an average OOD accuracy of 76.7%, against 72.0% for plain SGD and
  76.0% for AdamW, over 7 models and 5 datasets. ConvNeXt's embedding layer is its 4 × 4
  stride-4 convolution.
- ConvNeXt [8]: trained on ImageNet-1K with AdamW (lr 4e-3, weight decay 0.05, betas 0.9 and
  0.999, 20-epoch warm-up, cosine), not SGD.

#### 2.4 Fine-tuning pretrained encoders and unseen data

- Kumar et al. [7]: the AdamW advantage is mainly OOD (OOD +4.0 against ID +1.2 on
  average), which is our W3 setting.
- LP-FT [12] and UltraBench 2 [17]: train the head with the encoder frozen first, then the
  encoder at a lower lr; UltraBench 2 did this with AdamW on 10 ultrasound tasks.
- SWAD [16]: weight averaging over a window chosen on val loss improved unseen-domain
  accuracy by 1.6% on average over five benchmarks, without changing the optimiser.

#### 2.5 What segmentation recipes used

Table 2. Optimiser settings as stated in each paper, for the segmentation models closest to
our recipes. "Not stated" means not found in the text read.

| Model (architecture) | Optimiser | Initial lr | Weight decay | Schedule | Batch, steps | Data | Ref |
|---|---|---|---|---|---|---|---|
| TransUNet (ResNet-50 + ViT-B hybrid) | SGD, momentum 0.9 (Nesterov not stated) | 0.01 | 1e-4 | Not stated | 24; 14k (Synapse), 20k (ACDC) iterations | CT, MRI | [9] |
| Swin-Unet (pure transformer) | SGD, momentum 0.9 | Not stated | 1e-4 | Not stated | 24; not stated | CT, MRI | [10] |
| UNETR (ViT encoder, CNN decoder) | AdamW | 1e-4 | Not stated | Not stated | 6; 20k iterations | CT, MRI | [11] |
| SegFormer (hierarchical transformer) | AdamW | 6e-5 | Not stated | Poly, factor 1.0 | 16; 160k iterations (ADE20K) | Natural images | [18] |
| ConvNeXt + UperNet (modern CNN) | Follows BEiT and Swin settings (optimiser not stated in its text) | Swept {8e-5, 1e-4}; LLRD {0.8, 0.9} | Not stated | Not stated | 16; 160k iterations | ADE20K | [8] |
| nnU-Net (U-Net, IN) | SGD, Nesterov, momentum 0.99 | 0.01 | Not found | Poly, power 0.9 | Per dataset (often 2 in 3D); 1,000 × 250 iterations | CT, MRI and others | [13] |
| UltraBench 2 (16 encoders, fine-tuned) | AdamW | Encoder 0.01 × head, with LLRD | Not in our note | Cosine | 32; at most 10,000 steps | Ultrasound | [17] |

ACDC: Automated Cardiac Diagnosis Challenge (MRI). Synapse: multi-organ abdominal CT. ADE20K:
natural-scene segmentation benchmark.

Practice follows each model's lineage more than the transformer against CNN line: Swin-Unet,
a pure transformer, was trained with SGD, and nnU-Net, a CNN, with SGD and very high
Nesterov momentum.

#### 2.6 What this suggests for the six recipes (the analyst's reading, not a decision)

Table 3. Recipes of DEC-077, the architecture facts that matter for the optimiser, and the
optimiser the evidence above leans to.

| Recipe | Encoder start; normalisation; stem | Lean | Main evidence |
|---|---|---|---|
| R1 `transunet` pretrained | ImageNet-21k; GN in ResNet, LN in ViT, BN in decoder; conv front end | AdamW with lower encoder lr (uniform with R4 to R6); SGD also workable | [6], [7], [17]; DEC-077 rule 4 |
| R2 `transunet` from scratch | None; as R1 | Same optimiser as R1, so R1 against R2 measures pretraining | [3], [6]; DEC-077 Table 1 caption |
| R3 `resenc_unet` from scratch | None; IN; conv stem | SGD, Nesterov, momentum 0.99, lr 0.01, poly 0.9 (nnU-Net) | [13], [4] |
| R4 to R6 DINOv3 ConvNeXt-B | LVD-1689M; LN; patchify stem | AdamW, lower encoder lr or LLRD, warm-up or frozen start; SGD only with the stem frozen | [7], [8], [17] |

GN: group normalisation. EXP-003's from-scratch run used the official `transunet_r50_b16`,
not R2's timm model, so its result says little about R2 directly.

#### 2.7 Limits of this study

- Most evidence is ImageNet classification or natural-image segmentation; only UltraBench 2
  [17] is ultrasound, and it did not compare optimisers.
- No runs of our own; EXP-003 is a different task (cirrhosis) and used one optimiser.
- Full texts were not read end to end. Values marked "tool summary" in Table 1 were not seen
  verbatim. Venues not shown on the pages read are given as arXiv only.

### 3. Open points for point 6

- R1 and R2: identical recipe (cleanest pretraining comparison), or R1 with the pretrained
  recipe (frozen start, lower encoder lr), so that R1 against R2 measures pretraining with
  its fine-tuning recipe?
- R3: its own nnU-Net SGD recipe, or the uniform one?
- Weight averaging (SWAD or EMA): if used, recompute the BN running statistics of the
  `transunet` decoder after averaging (`torch.optim.swa_utils.update_bn`).
- Code gap: `src/sonoai/training/optim.py` has only `sgd`. AdamW, parameter groups
  (encoder against decoder lr, no decay on 1-D parameters), LLRD, warm-up and EMA would
  need a method task.
- DEC-006's `SGD_DEFAULTS` note says the official TransUNet values are unverified: the paper
  [9] confirms lr 0.01, momentum 0.9, weight decay 1e-4 (our default lr 1e-3 is the user's
  change); Nesterov is our addition. The poly schedule comes from the official code, which
  was not checked here.

## Next

- Point 6 decision (the user, in another discussion).
- Then a method task for the optimiser code above, if the decision needs it.

## References

All checked on the web on 2026-11-19 (arXiv, proceedings or ar5iv pages).

1. Zhang J, Karimireddy SP, Veit A, et al. Why are adaptive methods good for attention
   models? NeurIPS 2020. [arXiv:1912.03194](https://arxiv.org/abs/1912.03194)
2. Kunstner F, Chen J, Lavington JW, Schmidt M. Noise is not the main factor behind the gap
   between SGD and Adam on transformers, but sign descent might be. ICLR 2023.
   [arXiv:2304.13960](https://arxiv.org/abs/2304.13960)
3. Zhang Y, Chen C, Ding T, Li Z, Sun R, Luo ZQ. Why transformers need Adam: a Hessian
   perspective. NeurIPS 2024. [arXiv:2402.16788](https://arxiv.org/abs/2402.16788)
4. Wilson AC, Roelofs R, Stern M, Srebro N, Recht B. The marginal value of adaptive gradient
   methods in machine learning. NeurIPS 2017. [arXiv:1705.08292](https://arxiv.org/abs/1705.08292)
5. Loshchilov I, Hutter F. Decoupled weight decay regularization. ICLR 2019.
   [arXiv:1711.05101](https://arxiv.org/abs/1711.05101)
6. Xiao T, et al. Early convolutions help
   transformers see better. NeurIPS 2021. [arXiv:2106.14881](https://arxiv.org/abs/2106.14881)
7. Kumar A, Shen R, Bubeck S, Gunasekar S. How to fine-tune vision models with SGD. ICLR
   2024. [arXiv:2211.09359](https://arxiv.org/abs/2211.09359)
8. Liu Z, et al. A ConvNet for the 2020s (ConvNeXt). CVPR 2022.
   [arXiv:2201.03545](https://arxiv.org/abs/2201.03545)
9. Chen J, et al. TransUNet: transformers make strong encoders for medical image
   segmentation. 2021. [arXiv:2102.04306](https://arxiv.org/abs/2102.04306)
10. Cao H, et al. Swin-Unet: Unet-like pure transformer for medical image
    segmentation. 2021. [arXiv:2105.05537](https://arxiv.org/abs/2105.05537)
11. Hatamizadeh A, et al. UNETR: transformers for 3D medical image
    segmentation. 2021. [arXiv:2103.10504](https://arxiv.org/abs/2103.10504)
12. Kumar A, Raghunathan A, Jones R, Ma T, Liang P. Fine-tuning can distort pretrained
    features and underperform out-of-distribution. ICLR 2022.
    [arXiv:2202.10054](https://arxiv.org/abs/2202.10054)
13. Isensee F, et al. nnU-Net: a self-configuring method for deep learning-based biomedical
    image segmentation. Nat Methods 2021;18:203–211
    ([doi:10.1038/s41592-020-01008-z](https://doi.org/10.1038/s41592-020-01008-z)); preprint read: [arXiv:1904.08128](https://arxiv.org/abs/1904.08128)
14. He K, et al. Masked autoencoders are scalable vision
    learners. [arXiv:2111.06377](https://arxiv.org/abs/2111.06377)
15. Wightman R, Touvron H, Jégou H. ResNet strikes back: an improved training procedure in
    timm. 2021. [arXiv:2110.00476](https://arxiv.org/abs/2110.00476)
16. Cha J, et al. SWAD: domain generalization by seeking flat minima. NeurIPS
    2021. [arXiv:2102.08604](https://arxiv.org/abs/2102.08604)
17. Radhachandran A, Tupper A, Gagné C, Speier W. UltraBench 2: towards robust evaluation of
    vision foundation models on ultrasound. ML4H 2026. [arXiv:2609.28610](https://arxiv.org/abs/2609.28610);
    as summarised in `literature/epic1-anatomy-segmentation-models-and-papers.md` (its [1]),
    not re-read today.
18. Xie E, et al. SegFormer: simple and efficient design for semantic
    segmentation with transformers. NeurIPS 2021. [arXiv:2105.15203](https://arxiv.org/abs/2105.15203)
