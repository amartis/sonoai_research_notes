# Self-supervised, generative and anatomy-aware learning for the epic 1 model: a literature study

- Date: 2026-11-24. Written by Claude (Opus 5.5) at the user's request.
- For: research epic 1 ([DEC-065](../decisions/DEC-065-mission-upper-abdomen-anatomy-segmentation.md),
  upper-abdomen anatomy segmentation) and the diagnosis epic after it. It follows
  [DIS-052](../discussions/DIS-052-epic1-next-recipes-after-six-seed0-runs.md) (next recipes after
  the six seed-0 runs) and the 2026-11-18 note
  [epic1-anatomy-segmentation-models-and-papers.md](epic1-anatomy-segmentation-models-and-papers.md)
  ("the 2026-11-18 note"), and does not repeat them.
- How: web search on 2026-11-24, then 59 papers and 4 free books downloaded on machine01 into
  [ssl-generative-anatomy-priors-papers/](ssl-generative-anatomy-priors-papers/README.md) (PDFs
  not in git). Each was read as text (pdftotext): the abstract of every paper, plus the method,
  result tables or conclusion of the core ones. No paper was read in full; Section 9 says what was
  read of each. Numbers are as the sources state them, with the PDF page (p.), and none were
  reproduced. No table, per-sample record or image of the project was read.
- **Nothing is decided here.** The candidate changes C7 to C13 (Table 4 in Section 6: seven
  changes to the recipe R4 defined below) come after the six candidate changes C1 to C6 of
  DIS-052 (Table 3 there: weight averaging, a shorter run, a larger input, stronger augmentation,
  parameter-efficient tuning, and a presence head that gates the masks). Like those, C7 to C13
  are labels in this note only.

Terms and abbreviations: **SSL**, self-supervised learning (learning from unlabelled images
through a pretext task); **MIM**, masked image modelling (hide parts of the image, predict them);
**MAE**, masked autoencoder; **JEPA**, joint-embedding predictive architecture; **DSC**, Dice
similarity coefficient; **FPR**, false-positive rate; **FiLM**, feature-wise linear modulation
(a learned per-channel scale and shift); **VAE**, variational autoencoder; **DAE**, denoising
autoencoder; **DG**, domain generalisation. **R4**: the DINOv3 ConvNeXt-B recipe with the MLP
head of [DEC-077](../decisions/DEC-077-epic1-model-choice-six-recipes.md). **W1, W2, W3**: the
epic 1 scores of [DEC-076](../decisions/DEC-076-epic1-metrics-label-set-score-selection-ci-and-pass-rule.md)
(W2 is the "no phantom organs" score). **Phantom organ**: an organ predicted on a sample where it
is a closed negative (known absent). **Datasource group**: as in DIS-052. Labels from other records and from Section 1:

- **P1 to P7**: the seven proposals of DIS-052 (P1 relabel liver in kidney views, P2 grouped
  5-fold selection, P3 stomach report-only, P4 base recipe, P5 first changes, P6 inference
  steps, P7 seeds and comparisons).
- **O1 to O3**: the user's three observations in Section 1.
- **Fact 1 to fact 7**: the numbered facts of DIS-052.

## 0. Summary

1. **Next changes to R4, cheapest first** (Section 6): a decoder that is conditioned on
   per-organ presence (C7), and a model of plausible organ layouts learnt from label masks
   (C8), both after the liver labels in kidney views are settled (P1 of DIS-052, the relabel
   proposal). The strongest
   evidence on phantom organs is HALOS [32]: a presence classifier that only shares the encoder
   did not lower the FPR (0.285 against 0.259 for nnU-Net), but feeding the predicted presence
   into the segmentation features did (0.031) [32, p.9].
2. **The "DINO-Med" pattern** is continued DINO-style pretraining on one's own medical images,
   with the recipe almost unchanged: MedDINOv3 on CT [05], UltraDINO on fetal ultrasound [57],
   RAD-DINO on chest X-ray [04]. The gain is real but modest when labels are plentiful
   (MedDINOv3: 85.51 to 87.38 DSC on AMOS22 [05, p.8]; UltraDINO: 79.51 against 79.26 DSC for
   DINOv2 on the full FASS set, 74.24 against 69.11 with 20 training images [57, p.5]). For us
   it is the bigger bet C10 (continued SSL of R4's encoder), mainly because the same encoder will serve diagnosis.
3. **The generative principle enters in three places**, in the order I would try them: as a
   prior on masks (C8, the mask-plausibility model: plausibility check, label audit, post-processing [24]–[26], [42]); as a
   pretext task (MIM in C10, continued SSL [11], [14], [15]); and as a data source (mask-conditioned synthetic
   images [46]–[48], later). A generative segmentation head that samples several masks [37],
   [39], [54] is for uncertainty and label audit, not for the bar.
4. **Geometric and size relations.** No paper found here learns general anatomical relations
   for abdominal ultrasound. The evidence covers single-structure shape priors [24]–[28],
   hand-coded pairwise rules (containment and exclusion [29], size bounds [30]) and image-level
   organ existence [32]. My recommendation: learn the joint layout from masks (C8, the mask-plausibility model) and
   image-level presence (C7, the presence-conditioned decoder); hand-code a rule only where a clinician confirms it.
5. **Meta-learning.** DINO is SSL, not meta-learning. The meta-learning that fits our main
   problem (the datasource gap, W3, the val-to-test drop of W1) is episodic domain generalisation over datasource groups:
   MLDG [59], and SAML [60], which beat pooled training by 2.15 DSC points on six prostate MRI
   sites [60, p.8] (C9, episodic training over datasource groups). Few-shot and in-context segmenters [50]–[54] fit new structures in
   later epics.
6. **Spleen read as liver.** By [DEC-066](../decisions/DEC-066-epic1-model-task-label-set-softmax.md)
   (Epic 1 model task definition) rule 3 (the allowed-class set per pixel as target), a drawn spleen lies outside every first-set polygon, so its pixels are trained as
   background, or as "background or liver" with no liver loss when liver is unknown (my reading
   of the rule; the share of such samples is not counted). Little in training separates spleen
   from liver. C11 (spleen as a training class) puts spleen back or adds an "unknown region" score [55].
7. **The 224 × 224 stretch distorts geometry.** [DEC-069](../decisions/DEC-069-epic1-data-preparation.md)
   (Epic 1 data preparation) rule 4 (the 224 × 224 stretch) stretches each crop to 224 × 224 without keeping its aspect, so shape and size
   relations change from crop to crop. An aspect-preserving resize (C13, a change to R4's input) is a cheap
   precondition for any shape or size prior (my reasoning; no paper tested it on our data).

## 1. Question and scope

The user's aim: find the best inference model and optimisation strategies, with recent trends,
for a model that forms knowledge of anatomical structure (relations between organs, their
sizes), with interest in generative models, DINO and its medical variants, transformers, MAE,
and meta-learning.

The user's observations from the liver-negative gallery of [TASK-197](../../backlog/tasks/task-197%20-%20Epic-1-runs-on-RunPod-R1-to-R6-at-seed-0-then-seeds-1-and-2-of-the-best-recipe-shift-test-EXP-record-with-the-DEC-076-verdict-per-recipe-DEC-080.md)
(R4 and R6 reviewed; counts not given; R6 is the DINOv3 recipe with a UPerNet decoder, one of the
six Epic 1 recipes R1 to R6 of DEC-077, the Epic 1 model choice):

- O1. Most of the "F-both-large" samples (both models predict a large liver on a sample labelled
  liver-absent; my reading of the gallery group's name) show a liver. This supports section 1 of
  DIS-052 (the user's liver view): those are label errors, not model errors.
- O2. On a few samples one or both models read the spleen as liver. Spleen has few samples and
  is not a first-set class (DEC-066, Epic 1 model task definition, rule 1: spleen leaves the first set).
- O3. On a few samples a phantom organ appears.

Questions for this study:

- Q1. Which pretraining gives the best encoder for our ultrasound: DINO-family, MIM, JEPA or
  anatomy-aware SSL?
- Q2. How can a model learn relations between organs (position, adjacency, size)?
- Q3. Where do generative models help: pretraining, priors on masks, uncertainty, data?
- Q4. Which meta-learning or few-shot methods fit, and for which problem?
- Q5. Which methods address O2 and O3 directly?

Out of scope: architectures and decoders already compared (the 2026-11-18 note, fact 1 of DIS-052: decoders differ little),
promptable segmenters (SAM family, section 3 of DIS-052: bigger bets), and label-noise methods (the
2026-11-24 label-noise journal note).

## 2. Keyword map

Table 1. Keyword groups, what each means in one line, and where this note covers it.

| Group | Keywords | What it is | Section |
|---|---|---|---|
| SSL by self-distillation | DINO, iBOT, DINOv2, DINOv3, Gram anchoring, RAD-DINO, MedDINOv3, UltraDINO | a student network matches a teacher (a moving average of itself) across views of one image | 4.1 |
| MIM (generative SSL) | MAE, SimMIM, SparK, ConvNeXt V2 FCMAE, deblurring MAE, USF-MAE | hide most of the image, reconstruct the pixels | 4.2 |
| Latent prediction | I-JEPA, V-JEPA 2, V-JEPA 2.1, LeJEPA | hide regions, predict their embeddings (not pixels) from the visible context | 4.3 |
| Anatomy-aware SSL | Adam, Adam-v2 / Eden, PEAC, Alice | pretext tasks built on the consistency and part-whole hierarchy of anatomy | 4.4 |
| Shape and relation priors | ACNN, Post-DAE, constrained VAE, HybridGNet, topological interaction, size constraints | a learnt or hand-coded model of plausible masks that corrects or constrains the segmenter | 4.5 |
| Organ hallucination | HALOS, RAOS hallucination ratio, presence gating | false-positive organs and how image-level existence suppresses them | 4.6 |
| Generative segmentation | probabilistic U-Net, diffusion segmentation, ambiguous segmentation, normative QA | a model that samples several plausible masks per image | 4.7 |
| Generative data | ControlNet, mask-conditioned diffusion, synthetic ultrasound | images generated from a mask, to add rare classes | 4.8 |
| Meta-learning and in-context | MAML, MLDG, SAML, prototypical networks, PANet, SSL-ALPNet, UniverSeg, Tyche | learning to learn: from tasks or domains to a new task or domain | 4.9 |
| Open set | RbA ("rejected by all"), one-vs-all heads | marking regions that belong to no known class | 4.10 |
| Generative and representation learning merging | REPA, RAE, diffusion as SSL (l-DAE) | DINO-type encoders inside generative models and the reverse | 4.11 |

Further keywords worth following, not studied here: equivariant networks (B1 chapter 5),
test-time adaptation, continual learning (B4 section 19.7), video SSL on cine loops (V-JEPA 2
[17], if the data hold loops), and conformal prediction for segmentation uncertainty.

## 3. How the families relate

DINO is not meta-learning. It is SSL by self-distillation: a student network is trained to
output the same distribution as a teacher network on another view of the same image, and the
teacher is a moving average of the student [01]. Meta-learning means "learning the learning
algorithm" from many tasks or datasets, each split into its own train and test part [B4,
section 19.6.4, p.755]. Murphy notes that this is close to domain generalisation, except that
every training distribution gets its own train and test split, so the model can "practise"
generalising [B4, p.755]. That is exactly the shape of our datasource groups.

I-JEPA [16, pp.2-3] places SSL in three families, by what the loss compares:

Table 2. The three SSL families, with the methods of this note in each and the property that
matters for us.

| Family | Loss compares | Methods here | Property that matters for us |
|---|---|---|---|
| Joint embedding (invariance) | embeddings of two augmented views | DINO [01], DINOv2 [03], DINOv3 [56], RAD-DINO [04], MedDINOv3 [05], UltraDINO [57], PEAC [22], Alice [23] | strong global features; the views and augmentations encode what should not matter |
| Generative (reconstruction) | predicted and true pixels of hidden regions | MAE [11], SimMIM [12], SparK [14], FCMAE [13], deblurring MAE [15], USF-MAE [58], diffusion as SSL [40], [41] | learns local detail and what fills a hidden region from its context |
| Joint-embedding predictive | predicted and true embeddings of hidden regions | I-JEPA [16], V-JEPA 2 [17], V-JEPA 2.1 [18], LeJEPA [19] | predicts the content of a region from its context without modelling speckle-level pixels |

Two links matter. iBOT [02] and DINOv2/v3 already combine the first two: a DINO loss on the
whole image plus a masked-token loss on patches. And the reconstruction and predictive
families are the "generative principle" inside SSL: a model that can fill a hidden region of an
ultrasound image from the rest must encode where organs usually lie and how large they are.
That is the closest the SSL literature comes to the relational knowledge the user asks for,
and it is implicit, not tested as such in any paper read here.

## 4. Evidence

### 4.1 DINO family and its medical variants ("DINO-Med")

- **DINOv3** [56] adds Gram anchoring: a loss that keeps the matrix of pairwise patch
  similarities of the student close to that of an earlier teacher, so dense features do not
  degrade in long training [56, p.12]. The ConvNeXt models of DINOv3, including R4's ConvNeXt-B,
  are distilled from the 7-billion-parameter ViT teacher [56, p.31].
- **MedDINOv3** [05] continued DINOv3 pretraining on 3.87 million CT slices, in three stages.
  On AMOS22 (abdominal CT), DSC went from 85.51 (DINOv3 weights) to 86.58 (stage 1,
  DINOv2-style self-distillation), 86.54 (adding Gram anchoring) and 87.38 (adding
  high-resolution adaptation) [05, p.8, Table 3]. Its authors call Gram anchoring optional
  in their setting [05, p.2]. It beat nnU-Net by 2.57 DSC points on AMOS22 and 5.49 on BTCV
  [05, p.2].
- **UltraDINO** [57] trained DINOv2 from scratch on 2 million fetal ultrasound images (ViT-S and
  ViT-B, 40 epochs, two H100 GPUs [57, p.4]). Against DINOv2 weights from natural images, with
  UPerNet decoders at 224 × 224: JNU-IFM with 4 training patients 86.01 against 83.55 DSC; FASS
  with 20 training images 74.24 against 69.11; full FASS (942 images) 79.51 against 79.26
  [57, p.5, Table 1]. Its conclusion: domain pretraining pays, and well-tuned general methods
  need no new method [57, p.9]. It compared against DINOv2, not DINOv3.
- **RAD-DINO** [04]: DINOv2 trained only on biomedical images (chest X-ray), with no text, matched
  or beat language-supervised medical encoders [04, p.1].
- **"Does DINOv3 set a new medical vision standard?"** [06]: frozen DINOv3 is a strong baseline
  across medical tasks but degrades where domain specialisation is deep (whole-slide images,
  electron microscopy, PET), and larger models or finer features did not reliably help [06,
  p.1]. Its only ultrasound task was cardiac registration (CAMUS) [06, p.3].
- **Segmenters on DINOv3:** SegDINO [07] (frozen encoder, MLP head, like R4's head) reached DSC
  0.8318 on TN3K thyroid ultrasound against 0.8027 for TransUNet [07, p.4]; Dino U-Net [08]
  (frozen encoder, adapter, U-Net decoder); DINO-AugSeg [09] (few-shot, wavelet-domain feature
  augmentation, includes ultrasound); DINO-Med3D [10] (3D, MICCAI 2026). None tests unseen
  ultrasound datasources.

Reading for us: the pattern is "keep the DINO recipe, change the data". The gains are largest
with few labels, which describes the diagnosis epic better than epic 1. UltraBench 2 (2026-11-18
note, Section 3.1) already found ultrasound encoders level with DINOv3 ConvNeXt-B on anatomy.

### 4.2 Masked image modelling

- **MAE** [11]: hide 75% of the patches and reconstruct pixels; the encoder sees only visible
  patches, which makes pretraining 3 times or more faster [11, p.1].
- **ConvNeXt and MIM.** Naively combining ConvNeXt with MAE "leads to subpar performance"; ConvNeXt
  V2 needed fully convolutional masking (FCMAE) and a new normalisation layer (GRN) in the
  architecture [13, p.1]. **SparK** [14] instead uses sparse convolution and a hierarchical
  decoder and "can be used directly on any convolutional model without backbone
  modifications", tested on ResNet and ConvNeXt [14, p.1]. So for R4's ConvNeXt-B (V1 design,
  DINOv3 weights), SparK is the MIM option that keeps the weights; FCMAE would change the
  backbone.
- **Ultrasound.** On thyroid ultrasound classification, MAE pretrained on ultrasound beat MAE
  pretrained on ImageNet (accuracy 89.45% against 87.25%), while MoCo v3, a contrastive method,
  gained little from ultrasound pretraining (87.08% against 86.96%); adding deblurring to the MAE
  task gave 90.19% [15, p.6, Table 1]. USF-MAE [58] pretrained an MAE on about 370,000 ultrasound
  images from 46 public datasets [58, p.1]; its tests are classification only.

### 4.3 Latent prediction (JEPA)

- **I-JEPA** [16] predicts the embeddings of large hidden blocks from a spread-out context block,
  without hand-made view augmentations, and beat MAE on linear probing with less compute
  [16, p.2].
- **V-JEPA 2.1** [18] targets dense features: a loss on all tokens, visible and hidden, applied
  at several encoder depths, for "spatially structured" features in images and video [18, p.1].
- **LeJEPA** [19] (November 2025) replaces the teacher-student and stop-gradient tricks with one
  regulariser that pushes embeddings towards an isotropic Gaussian: one trade-off
  hyperparameter, about 50 lines of code, stable across ResNets, ViTs and ConvNets [19, p.1].

Reading for us: JEPA is the cleanest form of "predict the hidden anatomy from its context",
which is the relational knowledge the user wants. No medical segmentation result was found for
it here, so it is a research option for C10 (continued SSL of R4's encoder), not a recipe.

### 4.4 Anatomy-aware SSL

Adam [20] and Adam-v2 [21] build pretext tasks on the hierarchy of anatomy (each structure
distinct, each part of a larger whole), with branches for localisability, composability and
decomposability [21, p.1]; Adam reports 9% to 30% better few-shot segmentation than SSL
baselines [20, p.1]. PEAC [22] matches patches across images of the same protocol. Alice [23]
mines views with the same anatomy in 3D CT. All four rely on anatomy appearing in a consistent
place across images (chest X-ray, CT). Free-hand ultrasound views do not have a fixed frame, so
the premise holds less well (my reading). Low priority.

### 4.5 Shape, relation and size priors

- **Learnt shape priors.** ACNN [24] trains an autoencoder on label masks and adds a loss that
  makes the segmenter's output codes match those of the mask autoencoder, used at training time
  only [24, p.5]. Post-DAE [25] uses a
  denoising autoencoder trained only on masks (no images) to project any segmentation onto
  plausible shapes after the fact. Painchaud et al. [26] warp implausible cardiac masks to the
  nearest valid shape in a constrained VAE: anatomically implausible results fell to 0.12% on
  CAMUS ultrasound [26, p.7]. Chen et al. [35] use an adversarially learnt shape prior in
  semi-supervised ultrasound segmentation.
- **Plausibility by construction.** HybridGNet [27] decodes organs as graphs of contour points,
  so anatomical constraints hold by construction [27, p.1]; Mask-HybridGNet [28] (2026) trains this
  from ordinary masks, without hand-placed landmarks [28, p.1].
- **Hand-coded relations.** The topological interaction loss [29] enforces containment and
  exclusion between classes; on BTCV it treated spleen, left kidney, liver and stomach as
  mutually exclusive (no two touching) [29, p.9]. Kervadec et al. [30] add differentiable
  penalties for inequality constraints such as the size of a region. Gu et al. [34] turn
  GPT-4o descriptions of inter-organ position and shape into priors in the segmentation head.
  The survey [31] groups these approaches.

Reading for us: in a 2D ultrasound crop, liver and right kidney touch at the hepatorenal
interface, so an exclusion rule like [29]'s would be wrong for that pair. Hand-coded rules need
a clinician's check for every pair and view. A mask prior learnt from our label masks (as in
[24]–[26]) learns adjacency, relative position and relative size together, without rules.

### 4.6 Organ hallucination (phantom organs)

- **HALOS** [32] (MRI, organs removed by surgery). On the UK Biobank test set, FPR for removed
  gallbladders was 0.259 for nnU-Net, 0.189 with oversampling, 0.285 for a multi-task model with
  a presence classifier sharing the encoder, and 0.031 for HALOS, which feeds the classifier's
  predicted presence into the segmentation features at several scales [32, p.9, Table 2]. The
  authors conclude that "multi-task training alone is not sufficient to reduce organ
  hallucinations" [32, p.9]. Post-processing with the true presence also reached FPR 0 but can
  leave holes in the neighbouring organ [32, p.8].
- **RAOS** [33] (CT, 413 scans) defines an organ hallucination ratio. Its authors found
  hallucinations after organ removal "widespread and not specific to any particular organ"
  [33, p.4], and that most of the seven state-of-the-art methods tested could not tell a
  removed organ was missing [33, p.7].

Reading for us: this is direct evidence for O3 (phantom organs) and for C6 of DIS-052 (the presence head), with one
correction. A presence head that only shares the encoder is not enough; its output must
condition the segmentation features (C7, the presence-conditioned decoder).

### 4.7 Generative segmentation and uncertainty

The probabilistic U-Net [37] (a U-Net plus a conditional VAE), diffusion segmenters [38], [39] and
Tyche [54] (in-context, several outputs) sample several plausible masks per image and reproduce
how often each variant appears among annotators [37, p.1], [39, p.1]. Dronne et al. [42]
(2026) model plausible masks given the image and flag where a mask departs from them; the
diffusion model localised subtle boundary errors more consistently than a VAE [42, p.1].
Akshat et al. [43] pretrained a diffusion model on 21 unlabelled CT scans and report liver DSC
rising from 0.75 to 0.93 with that pretraining [43, p.1]; one small benchmark (BTCV), so weak
evidence. Its claim that the pretrained encoder attends to the anatomy around an organ rests on
Grad-CAM maps only [43, p.11].

Reading for us: for O1 ("liver absent" labels that show a liver) a model of "masks that fit
this image" is a label-audit tool. For diagnosis it gives an uncertainty per organ.

### 4.8 Generative data

ControlNet [46] adds mask conditioning to a pretrained image diffusion model. Stojanovski et al.
[47] generated echocardiograms from label maps; a segmenter trained only on synthetic images
reached DSC 88.6% (left-ventricle endocardium) on real images [47, p.1]. SegGuidedDiff [48]
follows a multi-class mask at each sampling step (CT, MRI). For spleen (O2, spleen read as liver) this could add rare
examples, but generated images come from patient images and carry their rules, and their
realism for abdominal ultrasound is untested here. Later.

### 4.9 Meta-learning, few-shot and in-context

- **Episodic domain generalisation.** MLDG [59] splits the training domains in every batch into
  virtual train and test domains, and requires that a step that helps the first also helps the
  second [59, p.1]. SAML [60] adds shape compactness and smoothness losses under the simulated
  shift; over six prostate MRI sites, mean DSC 87.67 against 85.52 for pooled training
  ("DeepAll") [60, p.8, Table 2]. Caution: in DomainBed no DG method beat plain pooled training
  by more than 1 point on average, over 7 classification datasets (2026-11-18 note, Section 3.5).
- **Few-shot and in-context.** MAML [49] trains weights that adapt in a few gradient steps;
  prototypical networks [50] and PANet [51] classify pixels by distance to class prototypes;
  SSL-ALPNet [52] trains such a model on superpixel pseudo-labels without annotations.
  UniverSeg [53] segments a new task from example image-mask pairs with no training, after
  training on 53 medical datasets [53, p.1]; Tyche [54] adds several outputs per image.

Reading for us: episodic DG targets W3 (the val-to-test drop of W1; fact 4 of DIS-052: val does not see the
datasource gap) and fits P2 of DIS-052 (grouped 5-fold selection),
which already defines the groups. Few-shot methods fit new structures in later epics (vessels,
lesions), not the epic 1 bar.

### 4.10 Open set

RbA [55] observes that mask-classification heads behave like one-vs-all classifiers and scores a
region as unknown when every known class rejects it [55, p.1]. With one softmax (DEC-066 rule 2: one softmax output over the classes)
every pixel must take a known class, so a spleen pixel goes to background or to the most similar
organ. Per-organ sigmoids (the sigmoid comparison run, [TASK-199](../../backlog/tasks/task-199%20-%20Decide-sigmoid-comparison-run-of-the-best-epic-1-recipe-one-sigmoid-per-organ-with-unknown-outputs-masked-DEC-066-rule-7-DEC-080-rule-6.md))
allow "none of these".

### 4.11 Trend: generative models and representation learners merge

REPA [44] aligns the hidden states of a diffusion transformer with DINOv2 features and trains
SiT models more than 17.5 times faster [44, p.1]. RAE [45] replaces the VAE of latent diffusion
with a frozen DINO, SigLIP or MAE encoder plus a trained decoder [45, p.1]. Chen et al. [41] show
that a denoising diffusion model, simplified step by step, becomes a classical DAE that still
learns good representations. The direction: one encoder for recognition and generation. For us
that points to a later research option, a generative model in the latent space of our own
ultrasound encoder (synthetic data, mask QA and features in one), not to a recipe now.

## 5. What addresses the three observations

Table 3. The user's observations, the likely mechanism, the methods that act on it, and the
strength of the evidence. "My reading" marks reasoning not tested in a source.

| Observation | Likely mechanism | Methods that act on it | Evidence |
|---|---|---|---|
| O1: large false livers are mostly real livers | "liver absent" closures on kidney views with a visible liver ([DIS-049](../discussions/DIS-049-epic1-low-test-w2-liver-label-check.md), DIS-052 fact 5: the W2 liver failures look like undrawn small liver) | relabel (P1 of DIS-052, the relabel proposal; [TASK-233](../../backlog/tasks/task-233%20-%20Blinded-re-read-of-test-liver-negatives-in-Label-Studio-40-both-fail-and-40-both-pass-samples-of-R1-and-R4-no-model-output-liver-visible-spleen-visible-kidney-side-dataset-record-DIS-049.md)); a mask-given-image model as a label audit [42], [37] | strong for the mechanism (the user's gallery review; the blinded re-read is still to come); weak to medium for the audit tool (CT, not ultrasound) |
| O2: spleen read as liver | spleen not a class; its pixels are trained as background, or as "background or liver" with no liver loss when liver is unknown (my reading of DEC-066, Epic 1 model task definition, rule 3: the allowed-class set per pixel); few spleen samples | spleen as a training class (C11); one-vs-all heads and an unknown score [55]; more spleen data, public or synthetic [47], [48]; context from SSL (C10) | medium for one-vs-all [55] (natural images); none tested on spleen versus liver in ultrasound |
| O3: phantom organs | image-level error: the model segments an organ the image does not show | presence-conditioned decoder (C7) [32]; mask prior (C8) [25], [26]; plausibility by construction [27], [28] | strong for C7 in MRI [32]; medium for mask priors (cardiac, chest) |

## 6. Candidate changes to R4

Table 4. Candidates C7 to C13, each a change against R4, in the suggested order within each tier.
Costs are my estimates from fact 7 of DIS-052 (1.6 to 1.9 A100 hours per 30-epoch R4 run) unless a
source is named. Every candidate is chosen on out-of-group predictions (P2 of DIS-052, grouped
5-fold selection), never on test. O1 to O3 are the observations of Section 1 (false livers that
show a liver, spleen read as liver, phantom organs); W1 to W3 are the scores defined at the top.

| Tier | Candidate | Change | Aims at | Evidence | Cost and needs |
|---|---|---|---|---|---|
| 1 | C7 | Presence-conditioned decoder: a per-organ presence head (sigmoid, unknown masked), whose output scales and shifts decoder features (FiLM, as in [32]); replaces C6 of DIS-052 (the presence head that gates masks) | O3, W2 | [32]: FPR 0.259 to 0.031; encoder sharing alone 0.285 | method task; R4's training cost; after P1 of DIS-052 (settling liver labels in kidney views), or it learns the wrong closures harder |
| 1 | C8 | Mask-plausibility model: a DAE or VAE trained on epic 1 label masks only; used (a) to flag labels and predictions far from plausible layouts, (b) as post-processing [25], (c) later as a training loss [24] | O1 audit, O3, organ relations and sizes | [24]–[26]: cardiac MRI and ultrasound, chest X-ray; single structures, not multi-organ abdomen | method task; small model, a few GPU hours (my estimate); masks are derived from label tables, so a table ask; where it may run needs a check of the data rules |
| 1 | C13 | Aspect-preserving resize (pad to square) instead of the stretch | geometry for C8 and any size prior | none (my reasoning) | a DEC replacing rule 4 of DEC-069 (Epic 1 data preparation: the 224 × 224 stretch); one R4 run; can go with C3 of DIS-052 (input 384) |
| 2 | C9 | Episodic training over datasource groups (MLDG [59]; SAML's shape losses [60]) | W3 | [60]: +2.15 DSC on six MRI sites; DomainBed caution | method task; about twice the cost per step (my estimate); needs the groups of P2 of DIS-052 (grouped 5-fold selection) |
| 2 | C11 | Spleen back as a training class where drawn (scored as report only), or per-organ sigmoids with an unknown score | O2 | [55] natural images; TASK-199 (sigmoid comparison run) | a DEC changing rule 1 of DEC-066 (spleen leaves the first set); a count of drawn spleens by group (needs a table ask) |
| 2 | C10 | Continued SSL of R4's encoder on all the project's unlabelled ultrasound: DINO-style self-distillation with a masked-token term (as in DINOv2/v3), Gram anchoring optional; SparK [14] as the MIM alternative that keeps the ConvNeXt weights; LeJEPA [19] as a simpler research alternative | W1, W3, and the diagnosis backbone | [05], [57], [04], [15] | tens of A100 hours (DIS-052 estimate, unverified); enc1 data on RunPod only ([DEC-024](../decisions/DEC-024-plain-never-leaves-machine01-ec2-label-studio-decrypts-in-ram.md)); a count of usable unlabelled images |
| 3 | C12 | Generative segmentation head (probabilistic U-Net [37] or diffusion [39]) for several masks per image | uncertainty for diagnosis, label audit | [37], [39], [54] | method task; after C7 and C8 |
| 3 | later | Mask-conditioned synthetic ultrasound for rare organs [46]–[48]; a generative model in our encoder's latent space [44], [45]; anatomy-aware SSL [20]–[23]; contour-graph decoders [27], [28] | O2, data, geometry | weak for our case | research tasks |

Figure 1. Proposed order of the candidates against R4. Each arrow starts only after the step
above it is done; C1 and C2 are DIS-052's weight-averaging and shorter-run candidates, and P1, P2, P6 and P7 are its proposals (relabel, grouped selection, inference steps, seeds).

```
DIS-052 P1 (relabel: settle liver in kidney views; TASK-232, the liver-negative audit of the TASK-197 runs; TASK-233, the blinded re-read of test liver negatives)
   │
   ├──▶ C8 mask-plausibility model ── first use: audit the relabelled masks
   │
   ├──▶ C13 aspect-preserving resize (one DEC, one run)
   │
   ▼
DIS-052 P2 (grouped folds, out-of-group selection)
   │
   ├──▶ C7 presence-conditioned decoder      ┐
   ├──▶ C1/C2 of DIS-052                     ├─ each against R4, 2 seeds (DIS-052 P7, seeds)
   ├──▶ C9 episodic DG over groups           ┘
   ├──▶ C11 spleen as a class (after its count)
   ▼
C10 continued SSL of the encoder ──▶ shared backbone for the diagnosis epic
```

For the inference model (what runs at test time), my suggestion from the literature read here:
R4, or its C7 version (presence-conditioned decoder), as a 5-fold ensemble from P2 of DIS-052
(grouped 5-fold selection), with flip test-time augmentation (P6 of DIS-052, inference steps),
a presence gate from C7 and, if C8 (mask-plausibility model) works, a plausibility projection or flag. All thresholds are set on out-of-group
predictions.

## 7. What to read first

Table 5. A reading order for the user, books first. Chapters checked in the PDFs' contents pages.

| Order | Source | Part | Why |
|---|---|---|---|
| 1 | Prince, *Understanding Deep Learning* [B3] | ch. 12 (transformers), 14 (unsupervised learning), 17 (VAEs), 18 (diffusion) | the clearest short path to the generative models used here |
| 2 | Murphy, *Probabilistic ML: Advanced Topics* [B4] | sections 19.6.2 and 19.6.4 (domain generalisation, meta-learning, book pages 752-758); 32.3.2 and 32.3.3 (generative and self-supervised representation learning, book pages 1059-1064); ch. 20 (generative models overview) | how meta-learning, DG and SSL relate |
| 3 | DINOv3 [56] | sections on Gram anchoring and the ConvNeXt distillation (pp.12, 31) | R4's encoder |
| 4 | HALOS [32] | whole paper (13 pages) | the most direct evidence for C7 (presence-conditioned decoder) |
| 5 | MedDINOv3 [05] and UltraDINO [57] | whole papers (10 and 11 pages) | the "DINO-Med" pattern for C10 (continued SSL) |
| 6 | Post-DAE [25] and Painchaud et al. [26] | whole papers | mask priors for C8 (mask-plausibility model) |
| 7 | SAML [60] | whole paper | episodic DG for C9 (episodic training over groups) |
| 8 | I-JEPA [16] and LeJEPA [19] | sections 1-3 | the predictive family |
| 9 | Bronstein et al., *Geometric Deep Learning* [B1] | ch. 3 (geometric priors) | symmetry and invariance as design tools |
| 10 | Lai et al., *The Principles of Diffusion Models* [B2] | Parts A and B | diffusion in depth, if C12 (generative segmentation head) or synthetic data go ahead |

## 8. Open questions for a consult session

- How many unlabelled ultrasound images, by datasource, could C10 (continued SSL of R4's encoder) use (enc1 on RunPod)? A count
  without images; needs a table ask.
- How many samples have a drawn spleen, and in how many of those is liver unknown? (O2, spleen read as liver, and C11, spleen as a training class.)
- May a model trained on label masks only (C8, the mask-plausibility model) run on RunPod, or only on machine01? A data-rule
  question (the masks are derived from label tables).
- Which organ pairs are known to touch or never touch in each standard view? A clinician's input
  before any hand-coded relation rule.
- Do the data hold cine loops? Video SSL (V-JEPA 2 [17]) would then apply.

## 9. Limits of this study

- Not systematic: web search plus known lines of work, English only, arXiv versions only.
- No paper was read in full. Read for every paper: abstract and first page. Also read: DINOv3
  sections 4.2, 7.2 and conclusion; MedDINOv3 contributions, Tables 1 and 3 and conclusion;
  UltraDINO setup, Table 1 and conclusion; HALOS Tables 1 and 2 and conclusion; RAOS sentences on
  hallucination; SAML Table 2; deblurring MAE Table 1; ACNN method (p.5); Painchaud et al.
  results (p.7); topological interaction datasets and metrics; SegDINO Table 1; I-JEPA sections
  1-2; Murphy section 19.6.4.
- No result was reproduced. Medical results come mostly from CT, MRI, chest X-ray and cardiac
  ultrasound, not abdominal ultrasound; none tests unseen ultrasound datasources.
- Preprints not peer reviewed by the version saved: among others [05], [06], [07], [08], [18],
  [19], [28], [34], [35], [42], [43], [45], [57], [58].
- Search leads not downloaded: MaskHybrid (abdominal ultrasound, Frontiers 2025), SegDINO
  multi-scale (arXiv:2606.17972), ShapeKit (CT post-processing), D2MAE (MICCAI 2025), V-JEPA 2.1's
  medical uses. Bishop and Bishop's *Deep Learning* was not downloaded (whether a free PDF exists
  was not checked).

## References

PDFs: [ssl-generative-anatomy-priors-papers/](ssl-generative-anatomy-priors-papers/README.md),
file names start with the reference number. All papers are arXiv versions (version as saved);
a venue is given only where the PDF's first pages print it. Title and version of every file
were checked against its first page on 2026-11-24.

Self-distillation and DINO for medical images

1. Caron M, et al. Emerging properties in self-supervised vision transformers (DINO).
   [arXiv:2104.14294](https://arxiv.org/abs/2104.14294) v2. [PDF](files/ssl-generative-anatomy-priors-papers/01-caron-2021-dino.pdf)
2. Zhou J, et al. iBOT: image BERT pre-training with online tokenizer. ICLR 2022.
   [arXiv:2111.07832](https://arxiv.org/abs/2111.07832) v3. [PDF](files/ssl-generative-anatomy-priors-papers/02-zhou-2022-ibot.pdf)
3. Oquab M, et al. DINOv2: learning robust visual features without supervision. TMLR 2024.
   [arXiv:2304.07193](https://arxiv.org/abs/2304.07193) v2. [PDF](files/ssl-generative-anatomy-priors-papers/03-oquab-2024-dinov2.pdf)
4. Pérez-García F, et al. Exploring scalable medical image encoders beyond text supervision
   (RAD-DINO). [arXiv:2401.10815](https://arxiv.org/abs/2401.10815) v3. [PDF](files/ssl-generative-anatomy-priors-papers/04-perez-garcia-2025-rad-dino.pdf)
5. Li Y, et al. MedDINOv3: how to adapt vision foundation models for medical image segmentation?
   [arXiv:2509.02379](https://arxiv.org/abs/2509.02379) v3. [PDF](files/ssl-generative-anatomy-priors-papers/05-li-2025-meddinov3.pdf)
6. Liu C, et al. Does DINOv3 set a new medical vision standard? Benchmarking 2D and 3D
   classification, segmentation, and registration. [arXiv:2509.06467](https://arxiv.org/abs/2509.06467) v3. [PDF](files/ssl-generative-anatomy-priors-papers/06-liu-2025-dinov3-medical-benchmark.pdf)
7. Yang S, et al. SegDINO: an efficient design for medical and natural image segmentation with
   DINO-V3. [arXiv:2509.00833](https://arxiv.org/abs/2509.00833) v1. [PDF](files/ssl-generative-anatomy-priors-papers/07-yang-2025-segdino.pdf)
8. Li H, Gao Y, et al. Dino U-Net: exploiting high-fidelity dense features from foundation
   models for medical image segmentation. [arXiv:2508.20909](https://arxiv.org/abs/2508.20909) v2. [PDF](files/ssl-generative-anatomy-priors-papers/08-li-2025-dino-unet.pdf)
9. Xu G, et al. Exploiting DINOv3-based self-supervised features for robust few-shot medical
   image segmentation (DINO-AugSeg). [arXiv:2601.08078](https://arxiv.org/abs/2601.08078). [PDF](files/ssl-generative-anatomy-priors-papers/09-xu-2026-dino-augseg.pdf)
10. Hu H, et al. DINO-Med3D: bridging dimension and domain gaps in volumetric segmentation via
    progressive adaptation. MICCAI 2026. [arXiv:2606.18886](https://arxiv.org/abs/2606.18886) v1. [PDF](files/ssl-generative-anatomy-priors-papers/10-hu-2026-dino-med3d.pdf)
56. Siméoni O, et al. DINOv3. [arXiv:2508.10104](https://arxiv.org/abs/2508.10104) v1. [PDF](files/ssl-generative-anatomy-priors-papers/56-simeoni-2025-dinov3.pdf)
57. Ambsdorf J, et al. General methods make great domain-specific foundation models: a
    case-study on fetal ultrasound (UltraDINO). [arXiv:2506.19552](https://arxiv.org/abs/2506.19552) v1. [PDF](files/ssl-generative-anatomy-priors-papers/57-ambsdorf-2025-ultradino.pdf)

Masked image modelling

11. He K, et al. Masked autoencoders are scalable vision learners. [arXiv:2111.06377](https://arxiv.org/abs/2111.06377) v3. [PDF](files/ssl-generative-anatomy-priors-papers/11-he-2022-mae.pdf)
12. Xie Z, et al. SimMIM: a simple framework for masked image modeling. [arXiv:2111.09886](https://arxiv.org/abs/2111.09886). [PDF](files/ssl-generative-anatomy-priors-papers/12-xie-2022-simmim.pdf)
13. Woo S, et al. ConvNeXt V2: co-designing and scaling ConvNets with masked autoencoders.
    [arXiv:2301.00808](https://arxiv.org/abs/2301.00808) v1. [PDF](files/ssl-generative-anatomy-priors-papers/13-woo-2023-convnext-v2.pdf)
14. Tian K, et al. Designing BERT for convolutional networks: sparse and hierarchical masked
    modeling (SparK). ICLR 2023 submission version. [arXiv:2301.03580](https://arxiv.org/abs/2301.03580) v2. [PDF](files/ssl-generative-anatomy-priors-papers/14-tian-2023-spark.pdf)
15. Kang Q, et al. Deblurring masked autoencoder is better recipe for ultrasound image
    recognition. [arXiv:2306.08249](https://arxiv.org/abs/2306.08249) v3. [PDF](files/ssl-generative-anatomy-priors-papers/15-kang-2023-deblurring-mae-ultrasound.pdf)
58. Megahed Y, et al. USF-MAE: ultrasound self-supervised foundation model with masked
    autoencoding. [arXiv:2510.22990](https://arxiv.org/abs/2510.22990) v2. [PDF](files/ssl-generative-anatomy-priors-papers/58-megahed-2025-usf-mae.pdf)

Latent prediction

16. Assran M, et al. Self-supervised learning from images with a joint-embedding predictive
    architecture (I-JEPA). [arXiv:2301.08243](https://arxiv.org/abs/2301.08243) v3. [PDF](files/ssl-generative-anatomy-priors-papers/16-assran-2023-i-jepa.pdf)
17. Assran M, et al. V-JEPA 2: self-supervised video models enable understanding, prediction and
    planning. [arXiv:2506.09985](https://arxiv.org/abs/2506.09985) v1. [PDF](files/ssl-generative-anatomy-priors-papers/17-assran-2025-v-jepa-2.pdf)
18. Mur-Labadia L, et al. V-JEPA 2.1: unlocking dense features in video self-supervised learning.
    [arXiv:2603.14482](https://arxiv.org/abs/2603.14482) v3. [PDF](files/ssl-generative-anatomy-priors-papers/18-mur-labadia-2026-v-jepa-2-1.pdf)
19. Balestriero R, LeCun Y. LeJEPA: provable and scalable self-supervised learning without the
    heuristics. [arXiv:2511.08544](https://arxiv.org/abs/2511.08544) v3. [PDF](files/ssl-generative-anatomy-priors-papers/19-balestriero-2025-lejepa.pdf)

Anatomy-aware SSL

20. Hosseinzadeh Taher MR, et al. Towards foundation models learned from anatomy in medical
    imaging via self-supervision (Adam). [arXiv:2309.15358](https://arxiv.org/abs/2309.15358) v1. [PDF](files/ssl-generative-anatomy-priors-papers/20-hosseinzadeh-2023-adam.pdf)
21. Hosseinzadeh Taher MR, Gotway MB, Liang J. Representing part-whole hierarchies in foundation
    models by learning localizability, composability, and decomposability from anatomy via
    self-supervision (Adam-v2). CVPR 2024. [arXiv:2404.15672](https://arxiv.org/abs/2404.15672) v1. [PDF](files/ssl-generative-anatomy-priors-papers/21-hosseinzadeh-2024-adam-v2.pdf)
22. Zhou Z, et al. Learning anatomically consistent embedding for chest radiography (PEAC).
    [arXiv:2312.00335](https://arxiv.org/abs/2312.00335) v2. [PDF](files/ssl-generative-anatomy-priors-papers/22-zhou-2023-peac.pdf)
23. Jiang Y, et al. Anatomical invariance modeling and semantic alignment for self-supervised
    learning in 3D medical image analysis (Alice). [arXiv:2302.05615](https://arxiv.org/abs/2302.05615) v3. [PDF](files/ssl-generative-anatomy-priors-papers/23-jiang-2023-alice.pdf)

Shape, relation and size priors; hallucination

24. Oktay O, et al. Anatomically constrained neural networks (ACNN): application to cardiac image
    enhancement and segmentation. IEEE Trans Med Imaging. [arXiv:1705.08302](https://arxiv.org/abs/1705.08302) v4. [PDF](files/ssl-generative-anatomy-priors-papers/24-oktay-2018-acnn.pdf)
25. Larrazabal AJ, Martínez C, Glocker B, Ferrante E. Post-DAE: anatomically plausible
    segmentation via post-processing with denoising autoencoders. IEEE Trans Med Imaging.
    [arXiv:2006.13791](https://arxiv.org/abs/2006.13791) v1. [PDF](files/ssl-generative-anatomy-priors-papers/25-larrazabal-2020-post-dae.pdf)
26. Painchaud N, et al. Cardiac segmentation with strong anatomical guarantees. IEEE Trans Med
    Imaging 2020. [arXiv:2006.08825](https://arxiv.org/abs/2006.08825) v1. [PDF](files/ssl-generative-anatomy-priors-papers/26-painchaud-2020-cardiac-anatomical-guarantees.pdf)
27. Gaggion N, Mansilla L, Mosquera C, Milone DH, Ferrante E. Improving anatomical plausibility
    in medical image segmentation via hybrid graph neural networks: applications to chest x-ray
    analysis (HybridGNet). IEEE Trans Med Imaging. [arXiv:2203.10977](https://arxiv.org/abs/2203.10977) v3. [PDF](files/ssl-generative-anatomy-priors-papers/27-gaggion-2023-hybridgnet.pdf)
28. Gaggion N, et al. Mask-HybridGNet: graph-based segmentation with emergent anatomical
    correspondence from pixel-level supervision. [arXiv:2602.21179](https://arxiv.org/abs/2602.21179) v1. [PDF](files/ssl-generative-anatomy-priors-papers/28-gaggion-2026-mask-hybridgnet.pdf)
29. Gupta S, et al. Learning topological interactions for multi-class medical image
    segmentation. [arXiv:2207.09654](https://arxiv.org/abs/2207.09654) v1. [PDF](files/ssl-generative-anatomy-priors-papers/29-gupta-2022-topological-interaction.pdf)
30. Kervadec H, Dolz J, Tang M, Granger E, Boykov Y, Ben Ayed I. Constrained-CNN losses for
    weakly supervised segmentation. [arXiv:1805.04628](https://arxiv.org/abs/1805.04628) v2. [PDF](files/ssl-generative-anatomy-priors-papers/30-kervadec-2019-constrained-cnn-losses.pdf)
31. Bohlender S, Oksuz I, Mukhopadhyay A. A survey on shape-constraint deep learning for medical
    image segmentation. [arXiv:2101.07721](https://arxiv.org/abs/2101.07721) v1. [PDF](files/ssl-generative-anatomy-priors-papers/31-bohlender-2021-shape-constraint-survey.pdf)
32. Rickmann AM, et al. HALOS: hallucination-free organ segmentation after organ resection
    surgery. [arXiv:2303.07717](https://arxiv.org/abs/2303.07717) v1. [PDF](files/ssl-generative-anatomy-priors-papers/32-rickmann-2023-halos.pdf)
33. Luo X, Li Z, Zhang S, Liao W, Wang G. Rethinking abdominal organ segmentation (RAOS) in the
    clinical scenario: a robustness evaluation benchmark with challenging cases.
    [arXiv:2406.13674](https://arxiv.org/abs/2406.13674) v1. [PDF](files/ssl-generative-anatomy-priors-papers/33-luo-2024-raos.pdf)
34. Gu Y, Tsao W, et al. Leveraging textual anatomical knowledge for class-imbalanced
    semi-supervised multi-organ segmentation. [arXiv:2501.13470](https://arxiv.org/abs/2501.13470) v2. [PDF](files/ssl-generative-anatomy-priors-papers/34-gu-2025-textual-anatomical-knowledge.pdf)
35. Chen Y, Wang Y, et al. Striving for simplicity: simple yet effective prior-aware
    pseudo-labeling for semi-supervised ultrasound image segmentation.
    [arXiv:2503.13987](https://arxiv.org/abs/2503.13987) v1. [PDF](files/ssl-generative-anatomy-priors-papers/35-chen-2025-prior-aware-pseudo-labelling-ultrasound.pdf)

Generative segmentation, generative data, and the merging trend

37. Kohl SAA, et al. A probabilistic U-Net for segmentation of ambiguous images. NeurIPS 2018.
    [arXiv:1806.05034](https://arxiv.org/abs/1806.05034) v4. [PDF](files/ssl-generative-anatomy-priors-papers/37-kohl-2018-probabilistic-unet.pdf)
38. Wu J, et al. MedSegDiff: medical image segmentation with diffusion probabilistic model.
    [arXiv:2211.00611](https://arxiv.org/abs/2211.00611) v5. [PDF](files/ssl-generative-anatomy-priors-papers/38-wu-2022-medsegdiff.pdf)
39. Rahman A, Valanarasu JMJ, Hacihaliloglu I, Patel VM. Ambiguous medical image segmentation
    using diffusion models. [arXiv:2304.04745](https://arxiv.org/abs/2304.04745) v1. [PDF](files/ssl-generative-anatomy-priors-papers/39-rahman-2023-ambiguous-diffusion.pdf)
40. Baranchuk D, et al. Label-efficient semantic segmentation with diffusion models. ICLR 2022.
    [arXiv:2112.03126](https://arxiv.org/abs/2112.03126) v3. [PDF](files/ssl-generative-anatomy-priors-papers/40-baranchuk-2022-ddpm-segmentation.pdf)
41. Chen X, Liu Z, Xie S, He K. Deconstructing denoising diffusion models for self-supervised
    learning. [arXiv:2401.14404](https://arxiv.org/abs/2401.14404) v1. [PDF](files/ssl-generative-anatomy-priors-papers/41-chen-2024-deconstructing-diffusion-ssl.pdf)
42. Dronne C, et al. Image-conditioned diffusion models for quality assurance of organ-at-risk
    segmentations in radiotherapy. [arXiv:2608.23432](https://arxiv.org/abs/2608.23432) v1. [PDF](files/ssl-generative-anatomy-priors-papers/42-dronne-2026-diffusion-qa-organ-at-risk.pdf)
43. Akshat G, et al. Unsupervised anatomical feature learning via diffusion models.
    [arXiv:2608.25693](https://arxiv.org/abs/2608.25693) v1. [PDF](files/ssl-generative-anatomy-priors-papers/43-akshat-2026-diffusion-anatomical-feature-learning.pdf)
44. Yu S, et al. Representation alignment for generation: training diffusion transformers is
    easier than you think (REPA). ICLR 2025. [arXiv:2410.06940](https://arxiv.org/abs/2410.06940) v4. [PDF](files/ssl-generative-anatomy-priors-papers/44-yu-2025-repa.pdf)
45. Zheng B, Ma N, Tong S, Xie S. Diffusion transformers with representation autoencoders (RAE).
    [arXiv:2510.11690](https://arxiv.org/abs/2510.11690) v1. [PDF](files/ssl-generative-anatomy-priors-papers/45-zheng-2026-rae.pdf)
46. Zhang L, Rao A, Agrawala M. Adding conditional control to text-to-image diffusion models
    (ControlNet). [arXiv:2302.05543](https://arxiv.org/abs/2302.05543) v3. [PDF](files/ssl-generative-anatomy-priors-papers/46-zhang-2023-controlnet.pdf)
47. Stojanovski D, et al. Echo from noise: synthetic ultrasound image generation using diffusion
    models for real image segmentation. [arXiv:2305.05424](https://arxiv.org/abs/2305.05424) v2. [PDF](files/ssl-generative-anatomy-priors-papers/47-stojanovski-2023-echo-from-noise.pdf)
48. Konz N, Chen Y, Dong H, Mazurowski MA. Anatomically-controllable medical image generation
    with segmentation-guided diffusion models. [arXiv:2402.05210](https://arxiv.org/abs/2402.05210) v4. [PDF](files/ssl-generative-anatomy-priors-papers/48-konz-2024-segmentation-guided-diffusion.pdf)

Meta-learning, few-shot, in-context and open set

49. Finn C, Abbeel P, Levine S. Model-agnostic meta-learning for fast adaptation of deep networks
    (MAML). ICML 2017. [arXiv:1703.03400](https://arxiv.org/abs/1703.03400) v3. [PDF](files/ssl-generative-anatomy-priors-papers/49-finn-2017-maml.pdf)
50. Snell J, Swersky K, Zemel R. Prototypical networks for few-shot learning.
    [arXiv:1703.05175](https://arxiv.org/abs/1703.05175) v2. [PDF](files/ssl-generative-anatomy-priors-papers/50-snell-2017-prototypical-networks.pdf)
51. Wang K, et al. PANet: few-shot image semantic segmentation with prototype alignment.
    [arXiv:1908.06391](https://arxiv.org/abs/1908.06391) v2. [PDF](files/ssl-generative-anatomy-priors-papers/51-wang-2019-panet.pdf)
52. Ouyang C, et al. Self-supervision with superpixels: training few-shot medical image
    segmentation without annotation (SSL-ALPNet). [arXiv:2007.09886](https://arxiv.org/abs/2007.09886) v2. [PDF](files/ssl-generative-anatomy-priors-papers/52-ouyang-2020-ssl-alpnet.pdf)
53. Butoi VI, et al. UniverSeg: universal medical image segmentation.
    [arXiv:2304.06131](https://arxiv.org/abs/2304.06131) v1. [PDF](files/ssl-generative-anatomy-priors-papers/53-butoi-2023-universeg.pdf)
54. Rakic M, et al. Tyche: stochastic in-context learning for medical image segmentation.
    [arXiv:2401.13650](https://arxiv.org/abs/2401.13650) v2. [PDF](files/ssl-generative-anatomy-priors-papers/54-rakic-2024-tyche.pdf)
55. Nayal N, et al. RbA: segmenting unknown regions rejected by all.
    [arXiv:2211.14293](https://arxiv.org/abs/2211.14293) v2. [PDF](files/ssl-generative-anatomy-priors-papers/55-nayal-2023-rba.pdf)
59. Li D, Yang Y, Song YZ, Hospedales TM. Learning to generalize: meta-learning for domain
    generalization (MLDG). [arXiv:1710.03463](https://arxiv.org/abs/1710.03463) v1. [PDF](files/ssl-generative-anatomy-priors-papers/59-li-2018-mldg.pdf)
60. Liu Q, Dou Q, Heng PA. Shape-aware meta-learning for generalizing prostate MRI segmentation
    to unseen domains (SAML). [arXiv:2007.02035](https://arxiv.org/abs/2007.02035) v1. [PDF](files/ssl-generative-anatomy-priors-papers/60-liu-2020-saml-shape-aware-meta-learning.pdf)

Books (free PDFs from their authors)

- B1. Bronstein MM, Bruna J, Cohen T, Veličković P. *Geometric Deep Learning: Grids, Groups,
  Graphs, Geodesics, and Gauges*. [arXiv:2104.13478](https://arxiv.org/abs/2104.13478) v2, 160 pages. [PDF](files/ssl-generative-anatomy-priors-papers/books/B1-bronstein-2021-geometric-deep-learning.pdf)
- B2. Lai CH, Song Y, Kim D, Mitsufuji Y, Ermon S. *The Principles of Diffusion Models*
  (forthcoming, MIT Press). [arXiv:2510.21890](https://arxiv.org/abs/2510.21890) v3, 522 pages. [PDF](files/ssl-generative-anatomy-priors-papers/books/B2-lai-2025-principles-of-diffusion-models.pdf)
- B3. Prince SJD. *Understanding Deep Learning*. MIT Press 2023; PDF version of 2026-02-08
  (release v5.0.3, [udlbook](https://github.com/udlbook/udlbook/releases/tag/v5.0.3)), 541 pages. [PDF](files/ssl-generative-anatomy-priors-papers/books/B3-prince-2026-understanding-deep-learning-v5.0.3.pdf)
- B4. Murphy KP. *Probabilistic Machine Learning: Advanced Topics*. MIT Press; PDF release
  2025-dec-10 ([probml/pml2-book](https://github.com/probml/pml2-book/releases/tag/2025-dec-10)),
  1,370 pages, CC BY-NC-ND. [PDF](files/ssl-generative-anatomy-priors-papers/books/B4-murphy-2025-pml2-advanced-topics.pdf)
