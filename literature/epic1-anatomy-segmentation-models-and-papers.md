# Epic 1: models and papers for the upper-abdomen anatomy segmentation model

- Date: 2026-11-18. Written by Claude (Opus 5.5) at the user's request.
- For: research epic 1, [DEC-065](../decisions/DEC-065-mission-upper-abdomen-anatomy-segmentation.md) (mission: upper-abdomen anatomy segmentation). Mainly point 5
  (model choice); also point 6 (optimisation) and point 4 (metrics).
- How: web search, then each source opened at arXiv, Europe PMC, the publisher, GitHub or
  Hugging Face on 2026-11-18. Numbers are as the sources state them; none were reproduced.
  Most full texts were not read; Section 7 says what was not checked.

## 1. Question

Which architectures, pretrained weights and papers best serve the first working 2D model that
outlines liver, kidney, stomach and gallbladder on B-mode crops of dataset 261023, and still
works on datasource groups it never saw (DEC-065 criterion W3: val DSC minus test DSC ≤ 0.10)?

Fixed by earlier decisions and not reopened here:

- Background plus four organs, one softmax, a per-pixel allowed-class set as target,
  label-set losses ([DEC-066](../decisions/DEC-066-epic1-model-task-label-set-softmax.md)).
- Input 224 × 224 px, the crop stretched to it; crops with a shorter side below 224 px are
  out ([DEC-069](../decisions/DEC-069-epic1-data-preparation.md)).
- Test is whole datasource groups; val is drawn at random, by image, from the other groups
  ([DEC-071](../decisions/DEC-071-epic1-splitting-parameterised-split-method.md), proposed).
- Stack: GPU box with an RTX 3060 (12 GB) and no internet; torch 2.11.0, timm 1.0.30,
  dynamic-network-architectures 0.4.2 (`requirements.txt`). Registered models:
  `resenc_unet`, `transunet` (ImageNet-21k weights through timm), `swin_unet`,
  `transunet_r50_b16`. In [EXP-003](../experiments/EXP-003-transunet-r50-b16-from-scratch-512-and-224-lseg-cirrhosis-v4.md) (cirrhosis), the pretrained `transunet` at 224 px beat
  `transunet_r50_b16` from scratch on val; all three runs failed on test (DSC ≤ 0.047).

DSC: Dice similarity coefficient. FM: foundation model, a network pretrained on a very large
image set for reuse. DG: domain generalisation, here working on unseen datasource groups.
OOD: out of distribution. SE: standard error.

## 2. Recommendation

1. **Keep the DEC-065 lean for the first run: `transunet`** (ImageNet-21k weights). It is
   registered, its weights are already on the GPU box, and it trained at 224 px (EXP-003). No
   paper compares it with the newer encoders on ultrasound, so that comparison is ours to run.
2. **Add one model: a DINOv3 ConvNeXt-B encoder with a light decoder.** This is the main
   candidate. In the largest head-to-head benchmark of pretrained encoders on ultrasound that
   this search found (UltraBench 2 [1], 16 encoders), DINOv3 ConvNeXt-B and -L were in the top tier for anatomical
   segmentation (mean DSC 0.820 and 0.822 against 0.826 for the best), level with the
   ultrasound-specific models. Its weights are already in the pinned timm 1.0.30
   (`convnext_base.dinov3_lvd1689m`: 87.6 M parameters, 224 px, four feature maps at strides
   4 to 32), so it needs no new package. The decoder can be the SegFormer-style MLP head [7]
   that [1] used for such encoders. Licence: DINOv3 License (custom; use and change allowed;
   publications must acknowledge it) [2].
3. **Optional control: `resenc_unet` from scratch** (the nnU-Net residual-encoder U-Net [4],
   [5]). Well-configured CNN U-Nets remain hard to beat in 3D CT and MRI [5]. But in the one
   abdominal ultrasound study that trained both kinds, nnU-Net scored lower on spleen, the organ
   with the fewest labelled images (172): DSC 0.60 against 0.81 for UltraSam (a pretrained
   foundation model) and 0.82 for EVIT U-Net; on kidney 0.85 against 0.91 to 0.93 [8]. Its
   role is to show what pretraining adds, not to be the main line.
4. **Ultrasound-specific encoders only later**, and only if W3 fails with the above. The best
   of them (SAMUS, OpenUS, URFM-L) did not beat DINOv3 ConvNeXt by more than the noise in [1],
   and each has a cost: a non-commercial licence (USFM, OpenUS), custom CUDA kernels (OpenUS),
   no weights link found (URFM), or a prompt-based design (SAMUS, UltraSam). See Table 3.
5. **For unseen datasources, the training recipe matters at least as much as the
   architecture** (point 6; my reading of the papers, not a result of any one of them): train
   the decoder with the encoder frozen first, then the encoder
   at a lower learning rate (LP-FT [12]; recipe of [1]); average weights over the last part of
   training (SWAD [14]); add stronger generic intensity and image-quality augmentation
   (BigAug [16]; TrivialAugment on ultrasound [17]); and use leaf-Dice, not marginal Dice, as
   the Dice part of the label-set loss [20].

Table 1. Models recommended for point 5, in the order to run them.

| Order | Model | Pretrained weights | Evidence | Licence of weights | Work to add | Role |
|---|---|---|---|---|---|---|
| 1 | `transunet` (ResNet-50 + ViT-B/16 hybrid encoder, TransUNet [6]) | ImageNet-21k, through timm | EXP-003: trained at 224 px on 261023 (cirrhosis); no external benchmark | not checked | none | first run (DEC-065 lean) |
| 2 | DINOv3 ConvNeXt-B encoder + MLP decoder | `convnext_base.dinov3_lvd1689m` in timm 1.0.30 | [1]: anatomical mean DSC 0.820 (ConvNeXt-L 0.822), top tier of 16 | DINOv3 License | a registered model (timm `features_only` encoder, decoder, the weights' own input normalisation); weights downloaded on machine01 and copied to the GPU box | main candidate |
| 3 | `resenc_unet` | none (from scratch) | [4], [5]; [8] | none needed | none | optional control |
| 4 | an ultrasound-specific encoder (SAMUS, USF-MAE or URFM) | see Table 3 | [1]: 0.826, 0.813, 0.822 | see Table 3 | own loader and decoder | later, only if W3 fails |

## 3. Evidence

### 3.1 Pretrained encoders compared on ultrasound

Radhachandran et al. [1] (ML4H 2026) fine-tuned 16 encoders from 11 model families on 10
public ultrasound segmentation tasks with one protocol: AdamW, batch 32, cosine schedule, at
most 10,000 steps; encoder frozen for the first 1,000 steps, then trained at 0.01 times the
head learning rate with layer-wise learning-rate decay; TrivialAugment-style augmentation;
Dice plus cross-entropy loss. Decoder: a progressive upsampler for ViT and SAM encoders, a
SegFormer-style MLP for hierarchical encoders; the paper reports the difference between the
two as within the noise. Test images were letterboxed to 256 × 256 px. There was no
cross-site or cross-device test.

Table 2. Anatomical segmentation in UltraBench 2 [1] (six tasks, full fine-tuning): mean DSC
with SE, and the two abdominal tasks. Selected rows of 16, as read from Tables 15 and 7 of
arXiv version 2.

| Rank of 16 | Encoder | Pretraining data | Anatomical mean DSC (SE) | Liver DSC (AUL) | Kidney capsule DSC (Open Kidney) |
|---|---|---|---|---|---|
| 1 | SAMUS (SAM ViT-B + CNN branch) | US30K, about 30,000 images: thyroid, breast, heart | 0.826 (0.007) | 0.908 | 0.853 |
| 2 | OpenUS (VMamba-S) | about 309,000 images, 38 to 42 public datasets (sources differ) | 0.822 (0.007) | 0.913 | 0.840 |
| 3 | URFM-L (ViT-L) | about 1 M ultrasound images, about half private | 0.822 (0.007) | 0.913 | 0.827 |
| 4 | DINOv3 ConvNeXt-L | 1.689 billion web images | 0.822 (0.007) | 0.914 | 0.825 |
| 6 | DINOv3 ConvNeXt-B | 1.689 billion web images | 0.820 (0.007) | 0.908 | 0.829 |
| 7 | DINOv3 ViT-L | 1.689 billion web images | 0.815 (0.007) | 0.912 | 0.822 |
| 8 | USF-MAE (ViT) | about 370,000 images, 46 public datasets | 0.813 (0.007) | 0.901 | 0.813 |
| 9 | USFM (ViT-B) | about 2 M ultrasound images | 0.813 (0.007) | 0.899 | 0.804 |
| 10 | DINOv3 ViT-B | 1.689 billion web images | 0.811 (0.007) | 0.906 | 0.829 |
| 13 | UltraSam (SAM ViT-B) | US-43d, over 280,000 image-mask pairs | 0.809 (0.007) | 0.890 | 0.804 |
| 16 | EchoCare (Swin) | 4.5 M ultrasound images | 0.801 (0.008) | 0.894 | 0.795 |

AUL: Annotated Ultrasound Liver images (public). SE: standard error, as reported in [1].
Per-task values have their own SE in [1], not shown.

What this shows:

- The 16 encoders span 0.025 DSC; neighbouring ranks often differ by less than one SE. The
  authors' summary: ultrasound-specific pretraining still leads on classification; the best
  general-purpose models have drawn level on segmentation.
- Full fine-tuning was consistently as good as, and usually much better than, training the
  head only. Parameter count alone did not help (their Appendix D).
- ConvNeXt variants of DINOv3 ranked above its ViT variants.
- Limits: in-distribution test splits of public datasets; SAMUS's pretraining overlaps one of
  the tasks. Nothing here measures robustness to an unseen datasource.

Related: Ambsdorf et al. [29] (MICCAI 2025) trained unmodified DINOv2 on about 2 M fetal
ultrasound images from one region and beat models pretrained on natural or other ultrasound
images on three fetal datasets from different countries; they wrote that "scaling in natural
image pretraining does not translate to ultrasound performance". If a later version needs
more, self-supervised pretraining on our own unlabelled crops (train groups only) is the
route that worked in [29]; not for this epic.

### 3.2 Ultrasound-specific encoders: weights, licence and fit

Table 3. Ultrasound-specific pretrained encoders, as found on their repositories and papers
on 2026-11-18.

| Encoder, reference | Architecture | Pretraining data | Weights | Licence | Fit with our stack |
|---|---|---|---|---|---|
| SAMUS [23] (MICCAI 2024) | SAM ViT-B + CNN branch | US30K: thyroid, breast, heart; no abdominal organ | Google Drive | MIT (code) | own code; image encoder usable with our decoder, as in [1] |
| USF-MAE [26] | ViT, masked autoencoder | about 370,000 images, 46 public datasets, 224 px | Google Drive | MIT (code); weights not stated | simplest to load; authors show no segmentation |
| URFM [22] (iScience 2025) | ViT-B, ViT-L | 1,003,465 images, 15 organs incl. liver, kidney, gallbladder; about half private (54% by our sum of its Table 1) | the paper says GitHub, without a link; none found | not stated | cannot fetch yet |
| USFM [21] (Med Image Anal 2024) | ViT | about 2 M images, many devices | Google Drive | CC BY-NC 4.0 | non-commercial only |
| OpenUS [25] | VMamba-S | about 309,000 images, 38 to 42 public datasets | Google Drive | CC BY-NC 4.0 (badge) | needs a `mamba_ssm` 2.2.4 wheel built for torch 2.2 and Python 3.10; clashes with our pins |
| UltraSam [24] (IJCARS 2025) | SAM ViT-B | US-43d, 43 public datasets | public S3 | not stated | OpenMMLab stack; its install example pins torch 2.0 and mmcv 2.1; point or box prompts |
| EchoCare [27] | Swin | 4.5 M images, over 23 countries | said to be released; link not checked | not checked | lowest tier in [1] |
| UltraFedFM [28] (npj Digit Med 2025) | ViT-B | 1,015,754 images, federated | not found | – | – |

CC BY-NC: Creative Commons Attribution-NonCommercial. A medical alternative pretrained on CT,
MRI and ultrasound (RadImageNet [38], 1.35 M images, ResNet and other CNNs) beat ImageNet
weights on small ultrasound classification tasks in its own paper; its weights and access
were not checked.

### 3.3 Strong from-scratch baselines

- nnU-Net [4] configures a U-Net for each dataset by fixed rules. nnU-Net Revisited [5]
  (MICCAI 2024) found that many claims of transformer or Mamba models beating U-Nets failed
  under rigorous validation; CNN U-Nets with residual or
  ConvNeXt-style encoders in the nnU-Net framework, scaled to the hardware, gave the best
  results. Its residual-encoder presets: M fits 9 to 11 GB of GPU memory, L needs 24 GB, XL
  40 GB [5]. Our `resenc_unet` is from the same network library.
- Limit: [5] covers 3D CT and MRI datasets; it does not test pretrained 2D encoders or
  ultrasound.

### 3.4 What DSC to expect on abdominal ultrasound

For the DEC-065 bar (liver ≥ 0.85; kidney, stomach and gallbladder ≥ 0.70). Every study found
tested within its own sources (one centre or one public dataset); none tested unseen
datasources.

Table 4. Reported DSC for abdominal organs on B-mode ultrasound.

| Study | Data | Test | Liver | Kidney | Other organs |
|---|---|---|---|---|---|
| UltraBench 2 [1] | AUL; Open Kidney (public) | public split | 0.878 to 0.914 over 16 encoders | capsule 0.795 to 0.853 | – |
| Addo et al. 2026 [8], medRxiv | children, trauma scans (FAST), 200 clips, 1,807 image-mask pairs, one centre | 20% of clips held out (361 pairs) | 0.84 to 0.90 by model | 0.85 to 0.93 by model; pooled 0.91 (95% CI 0.87 to 0.95) | spleen 0.60 to 0.82 by model; diaphragm pooled 0.63 |
| Singla et al. [9] (Open Kidney dataset) | over 500 patients | not checked | – | capsule 0.85 | – |
| Wang et al. 2026 [10], Ultrasound Med Biol | 465 videos, 5,535 frames, one centre | split by case | "strong", no number in abstract | right kidney "strong" | pancreas IoU 0.538 |

FAST: focused assessment with sonography for trauma. IoU: intersection over union. Per-model
values of [8] are from its code repository (two decimals, as stated there); pooled values from
its abstract.

Reading: the liver bar (0.85) sits inside the in-distribution range reported (0.84 to 0.91);
the kidney bar (0.70) is below every reported value. No verified gallbladder or stomach
segmentation benchmark was found, and no study reports the val-to-test drop on new
datasources, so W3 has no anchor in the literature.

### 3.5 Generalisation to unseen datasources

Table 5. Methods for unseen-domain performance: evidence, its setting, and possible use in
epic 1.

| Method | Evidence | Setting of the evidence | Possible use (point) |
|---|---|---|---|
| Plain training on all source data, carefully tuned (ERM) | DomainBed [13]: with any model-selection rule, no DG method beat ERM on average by more than 1 point; selection on a validation set drawn from the training domains did better than leave-one-domain-out | 7 image classification datasets | default; agrees with DEC-071 (val drawn from the training groups) |
| Head first, then the whole network (LP-FT) | Kumar et al. [12]: full fine-tuning +2% in distribution but −7% OOD against a linear probe; LP-FT +1% in distribution and +10% OOD against full fine-tuning | 10 classification shift datasets | freeze the encoder at the start, then a low encoder learning rate, as [1] did (6) |
| Weight averaging | SWAD [14]: +1.6 points OOD on average over 5 DG benchmarks; WiSE-FT [15]: +4 to 6 points under shift | classification (WiSE-FT: zero-shot CLIP models) | average the weights of the last epochs (6) |
| Stacked image-quality, appearance and spatial augmentation (BigAug) | Zhang et al. [16]: DSC drop on unseen domains about 11%, against 39% with standard augmentation | 3D MRI and 3D echocardiography, small source sets | a stronger intensity set than `us_mild_v2` as one comparison (6) |
| Generic augmentation on ultrasound | Tupper and Gagné [17]: augmentations made for natural images, including TrivialAugment, were effective on ultrasound and sometimes beat ultrasound-specific ones | a benchmark of public ultrasound classification and segmentation tasks | supports generic intensity changes (6) |
| Foundation encoders, with or without parameter-efficient tuning | Cekmeceli et al. [18]: DINOv2, SAM, MedSAM and MAE encoders improved DG in medical segmentation; Rein [19] in street scenes | medical (modalities not named in the abstract); natural images | supports a pretrained encoder; parameter-efficient tuning not needed at first |
| Ultrasound-specific DG methods | MI-SegNet [30]; Nora [31], which states that style-transfer DG methods work less well than expected on ultrasound | train on one source, test on other ultrasound sources | later, only if W3 fails |

The BigAug figures are from the arXiv version of [16]; the journal version was not re-read.

### 3.6 Which Dice in the label-set loss (point 6)

Fidon et al. [20] (MICCAI 2021) trained on 18 fully and 146 partly labelled fetal brain MRI
volumes. Leaf-Dice beat marginal Dice on all 8 structures, by the most on corpus callosum
(DSC 62.0% against 11.1%) and deep grey matter (71.4% against 37.8%); marginalized
cross-entropy was not tested there. [TASK-157](../../backlog/tasks/task-157%20-%20Label-set-losses-for-the-anatomy-task-per-pixel-allowed-class-bitmask-target-builder-marginalized-cross-entropy-marginalized-Dice-and-leaf-Dice-synthetic-tests-DEC-066.md) implements both Dice forms, so point 6 can take
leaf-Dice as the default. [DIS-032](../discussions/DIS-032-epic1-model-task-definition-label-set-loss.md) lists the other label-set papers.

### 3.7 Metrics (point 4)

Metrics Reloaded [32] gives a way to choose validation metrics from the properties of the
problem, with an online tool; Reinke et al. [33] list metric pitfalls. Both are for the
point-4 session; their content beyond the abstracts was not re-read.

## 4. Not recommended now

- Prompt-based segmenters (SAM [34], SAM 2 [35], MedSAM [36], UltraSam [24], UltraSAM3 [37]):
  built for clicks, boxes or text prompts; our task is a fixed five-class output at 224 px.
  UltraSAM3 lists no weights.
- `transunet_r50_b16` from scratch lost to the pretrained `transunet` on val in EXP-003.
  `swin_unet` has no run here and no new evidence for it.
- OpenUS and USFM as the main line: licence and stack (Table 3).
- 3D and video models: out of scope (DEC-065 section 5).

## 5. Open questions for the consult sessions

1. Point 5: are non-commercial weights acceptable for this project (USFM, OpenUS: CC BY-NC)?
   Until decided, Table 1 uses none.
2. Point 6: [1] and [12] fine-tune pretrained encoders with AdamW, a frozen start and a lower
   encoder learning rate; the [DEC-006](../decisions/DEC-006-losses-optim-tracking.md) defaults are SGD with momentum and one learning rate
   (EXP-003). Which applies to a pretrained encoder is a point-6 choice.
3. Point 4: public liver and kidney masks (AUL, Open Kidney; listed in the journal note
   [2026-11-18-public-datasets-claude.md](../journal/2026/2026-11-18-public-datasets-claude.md))
   could serve as one extra unseen datasource for W3, through the public data root of [DEC-063](../decisions/DEC-063-public-non-patient-datasets-root.md).
   Their outline rules differ from ours; worth it only as a side check.

## 6. How the evidence was weighed

The ranking in Table 1 rests on three things: evidence on ultrasound segmentation (Table 2),
cost in our stack (Table 3: pinned packages, licence, weights reachable on machine01), and
DEC-065 rule 4.6 (simplest working choice first; prefer what is in the repo). No paper tests
any of these encoders on unseen ultrasound datasources, so the choice between rows 1 and 2 of
Table 1 can only be settled by our own runs.

## 7. Limits of this study

- Most numbers come from abstracts, repository pages and paper tables read through a web
  fetch tool on 2026-11-18; full texts were not read except for parts of [1], [20], [22] and
  [31].
- The search was not systematic (no PRISMA protocol); English sources only; paywalled papers
  were read only through their abstracts.
- Not checked: licence of the `transunet` ImageNet-21k weights; the weights licences of
  SAMUS, USF-MAE and UltraSam; the EchoCare weights link; the RadImageNet weights.
- Preprints not yet peer reviewed: [8], [18], [25], [26], [27], [37].

## References

Checked on 2026-11-18 at the source named. arXiv: e-print server; Europe PMC: literature
database with publisher metadata.

1. Radhachandran A, Tupper A, Gagné C, Speier W. UltraBench 2: towards robust evaluation of
   vision foundation models on ultrasound. ML4H 2026 (PMLR 346). arXiv:2609.28610 (v2).
   [doi:10.48550/arXiv.2609.28610](https://doi.org/10.48550/arXiv.2609.28610) (arXiv HTML v2)
2. Siméoni O, et al. DINOv3. arXiv:2508.10104, 2025.
   [arxiv.org/abs/2508.10104](https://arxiv.org/abs/2508.10104). Weights:
   [timm/convnext_base.dinov3_lvd1689m](https://huggingface.co/timm/convnext_base.dinov3_lvd1689m);
   licence: [DINOv3 License](https://github.com/facebookresearch/dinov3/blob/main/LICENSE.md)
   (arXiv; Hugging Face; GitHub)
3. Liu Z, et al. A ConvNet for the 2020s. CVPR 2022.
   [arxiv.org/abs/2201.03545](https://arxiv.org/abs/2201.03545) (arXiv)
4. Isensee F, et al. nnU-Net: a self-configuring method for deep learning-based biomedical
   image segmentation. Nat Methods 2021;18:203–211.
   [doi:10.1038/s41592-020-01008-z](https://doi.org/10.1038/s41592-020-01008-z) (Europe PMC)
5. Isensee F, et al. nnU-Net Revisited: a call for rigorous validation in 3D medical image
   segmentation. MICCAI 2024. [arxiv.org/abs/2404.09556](https://arxiv.org/abs/2404.09556);
   presets: [resenc_presets.md](https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/resenc_presets.md)
   (arXiv; GitHub)
6. Chen J, et al. TransUNet: transformers make strong encoders for medical image segmentation.
   [arxiv.org/abs/2102.04306](https://arxiv.org/abs/2102.04306), 2021; journal version: Med
   Image Anal 2024;97:103280.
   [doi:10.1016/j.media.2024.103280](https://doi.org/10.1016/j.media.2024.103280) (arXiv; Europe PMC)
7. Xie E, et al. SegFormer: simple and efficient design for semantic segmentation with
   transformers. NeurIPS 2021. [arxiv.org/abs/2105.15203](https://arxiv.org/abs/2105.15203) (arXiv)
8. Addo N, Narang K, Sinha R, et al. (10 authors). Development and evaluation of automated
   organ segmentation models for abdominal ultrasound in injured children. medRxiv, posted
   2026-10-29. [doi:10.64898/2026.10.27.26366648](https://doi.org/10.64898/2026.10.27.26366648);
   per-model results: [Kornblith-Lab/US-AbdomenSeg](https://github.com/Kornblith-Lab/US-AbdomenSeg)
   (Sciety record; GitHub)
9. Singla R, et al. The Open Kidney Ultrasound Data Set.
   [arxiv.org/abs/2206.06657](https://arxiv.org/abs/2206.06657), 2022 (arXiv)
10. Wang X, et al. Deep learning-based standard section recognition and multi-organ
    segmentation in upper abdominal ultrasound. Ultrasound Med Biol 2026;52(9):2088–2096.
    [doi:10.1016/j.ultrasmedbio.2026.06.003](https://doi.org/10.1016/j.ultrasmedbio.2026.06.003) (Europe PMC)
11. Xiao T, et al. Unified perceptual parsing for scene understanding (UPerNet). ECCV 2018.
    [arxiv.org/abs/1807.10221](https://arxiv.org/abs/1807.10221) (arXiv). A decoder
    alternative to [7].
12. Kumar A, Raghunathan A, Jones R, Ma T, Liang P. Fine-tuning can distort pretrained features
    and underperform out-of-distribution. ICLR 2022.
    [arxiv.org/abs/2202.10054](https://arxiv.org/abs/2202.10054) (arXiv)
13. Gulrajani I, Lopez-Paz D. In search of lost domain generalization. ICLR 2021.
    [arxiv.org/abs/2007.01434](https://arxiv.org/abs/2007.01434) (arXiv; venue from the ICLR
    2021 site in search results)
14. Cha J, et al. SWAD: domain generalization by seeking flat minima. NeurIPS 2021.
    [arxiv.org/abs/2102.08604](https://arxiv.org/abs/2102.08604) (arXiv)
15. Wortsman M, et al. Robust fine-tuning of zero-shot models. CVPR 2022.
    [arxiv.org/abs/2109.01903](https://arxiv.org/abs/2109.01903) (arXiv)
16. Zhang L, et al. Generalizing deep learning for medical image segmentation to unseen
    domains via deep stacked transformation. IEEE Trans Med Imaging 2020;39:2531–2540.
    [doi:10.1109/TMI.2020.2973595](https://doi.org/10.1109/TMI.2020.2973595); figures from
    [arxiv.org/abs/1906.03347](https://arxiv.org/abs/1906.03347) (Europe PMC; arXiv)
17. Tupper A, Gagné C. Revisiting data augmentation for ultrasound images. TMLR 2025.
    [arxiv.org/abs/2501.13193](https://arxiv.org/abs/2501.13193); code:
    [adamtupper/ultrasound-augmentation](https://github.com/adamtupper/ultrasound-augmentation) (arXiv)
18. Cekmeceli K, et al. Do vision foundation models enhance domain generalization in medical
    image segmentation? [arxiv.org/abs/2409.07960](https://arxiv.org/abs/2409.07960), 2024 (arXiv)
19. Wei Z, et al. Stronger, fewer, & superior: harnessing vision foundation models for domain
    generalized semantic segmentation (Rein). CVPR 2024.
    [arxiv.org/abs/2312.04265](https://arxiv.org/abs/2312.04265) (arXiv; CVF open access in
    search results)
20. Fidon L, et al. Label-set loss functions for partial supervision: application to fetal
    brain 3D MRI parcellation. MICCAI 2021.
    [doi:10.1007/978-3-030-87196-3_60](https://doi.org/10.1007/978-3-030-87196-3_60) (arXiv
    record and ar5iv full text)
21. Jiao J, et al. USFM: a universal ultrasound foundation model generalized to tasks and
    organs towards label efficient image analysis. Med Image Anal 2024;96:103202.
    [doi:10.1016/j.media.2024.103202](https://doi.org/10.1016/j.media.2024.103202); code:
    [openmedlab/USFM](https://github.com/openmedlab/USFM) (Europe PMC; GitHub)
22. Kang Q, et al. URFM: a general ultrasound representation foundation model for advancing
    ultrasound image diagnosis. iScience 2025;28:112917.
    [doi:10.1016/j.isci.2025.112917](https://doi.org/10.1016/j.isci.2025.112917) (Europe PMC full text)
23. Lin X, et al. Beyond adapting SAM: towards end-to-end ultrasound image segmentation via
    auto prompting (SAMUS). MICCAI 2024.
    [arxiv.org/abs/2309.06824](https://arxiv.org/abs/2309.06824); code:
    [xianlin7/SAMUS](https://github.com/xianlin7/SAMUS) (arXiv; GitHub)
24. Meyer A, et al. UltraSam: a foundation model for ultrasound using large open-access
    segmentation datasets. Int J Comput Assist Radiol Surg 2025.
    [doi:10.1007/s11548-025-03517-8](https://doi.org/10.1007/s11548-025-03517-8); code:
    [CAMMA-public/UltraSam](https://github.com/CAMMA-public/UltraSam) (arXiv; GitHub)
25. Zheng X, et al. OpenUS: a fully open-source foundation model for ultrasound image analysis
    via self-adaptive masked contrastive learning.
    [arxiv.org/abs/2511.11510](https://arxiv.org/abs/2511.11510), 2025; code:
    [XZheng0427/OpenUS](https://github.com/XZheng0427/OpenUS) (arXiv; GitHub)
26. Megahed Y, et al. USF-MAE: ultrasound self-supervised foundation model with masked
    autoencoding. [arxiv.org/abs/2510.22990](https://arxiv.org/abs/2510.22990), 2025; code:
    [Yusufii9/USF-MAE](https://github.com/Yusufii9/USF-MAE) (search results; GitHub)
27. Zhang H, et al. A fully open and generalizable foundation model for ultrasound clinical
    applications (EchoCare). [arxiv.org/abs/2509.11752](https://arxiv.org/abs/2509.11752),
    2025 (arXiv)
28. Jiang Y, et al. From pretraining to privacy: federated ultrasound foundation model with
    self-supervised learning (UltraFedFM). npj Digit Med 2025.
    [doi:10.1038/s41746-025-02085-0](https://doi.org/10.1038/s41746-025-02085-0) (arXiv record)
29. Ambsdorf J, et al. General methods make great domain-specific foundation models: a
    case-study on fetal ultrasound. MICCAI 2025.
    [arxiv.org/abs/2506.19552](https://arxiv.org/abs/2506.19552) (arXiv)
30. Bi Y, et al. MI-SegNet: mutual information-based US segmentation for unseen domain
    generalization. MICCAI 2023. [arxiv.org/abs/2303.12649](https://arxiv.org/abs/2303.12649) (arXiv)
31. Wei Z, Wu C, Du H, Yu R, Du B, Xu Y. Noise-robust tuning of SAM for domain generalized
    ultrasound image segmentation (Nora). MICCAI 2025.
    [papers.miccai.org 1075](https://papers.miccai.org/miccai-2025/paper/1075_paper.pdf); code:
    [wkklavis/Nora](https://github.com/wkklavis/Nora) (MICCAI open-access PDF)
32. Maier-Hein L, et al. Metrics reloaded: recommendations for image analysis validation. Nat
    Methods 2024;21:195–212.
    [doi:10.1038/s41592-023-02151-z](https://doi.org/10.1038/s41592-023-02151-z) (Europe PMC)
33. Reinke A, et al. Understanding metric-related pitfalls in image analysis validation. Nat
    Methods 2024;21:182–194.
    [doi:10.1038/s41592-023-02150-0](https://doi.org/10.1038/s41592-023-02150-0) (Europe PMC)
34. Kirillov A, et al. Segment anything. 2023.
    [arxiv.org/abs/2304.02643](https://arxiv.org/abs/2304.02643) (arXiv)
35. Ravi N, et al. SAM 2: segment anything in images and videos. 2024.
    [arxiv.org/abs/2408.00714](https://arxiv.org/abs/2408.00714) (arXiv)
36. Ma J, et al. Segment anything in medical images (MedSAM). Nat Commun 2024;15:654.
    [doi:10.1038/s41467-024-44824-z](https://doi.org/10.1038/s41467-024-44824-z) (Europe PMC)
37. Xu B, et al. UltraSAM3: a concept-driven foundation model for universal ultrasound image
    segmentation. [arxiv.org/abs/2607.29200](https://arxiv.org/abs/2607.29200), 2026 (arXiv)
38. Mei X, et al. RadImageNet: an open radiologic deep learning research dataset for effective
    transfer learning. Radiol Artif Intell 2022;4:e210315.
    [doi:10.1148/ryai.210315](https://doi.org/10.1148/ryai.210315) (Europe PMC)
