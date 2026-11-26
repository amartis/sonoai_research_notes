# Large-scale ultrasound foundation-model, segmentation and benchmark papers, and public-dataset lists (research notes)

Notes for the epic 4 report writer (epic 4: public ultrasound datasets). Written 2026-11-26.
Scope: papers from 2023 to 2026 that train or benchmark ultrasound models on many images collected
mostly from public datasets, plus surveys and curated lists of public ultrasound datasets. Paper
level only: dataset access, licence and size are reported only as the papers and lists state them.

How the sources were read: arXiv PDFs were saved in the job's tmp folder and read as text with
pdftotext (2026-11-25/26). GitHub READMEs and GitHub API metadata (licence, last push) were read on
2026-11-26. Two pages (the PMC page of Alsharid et al. and the EchoCare homepage) were read through
the WebFetch tool, whose small model transcribed them: spot-check those numbers before relying on
them. The project's local PDFs are in
[../files/ssl-generative-anatomy-priors-papers/](../files/ssl-generative-anatomy-priors-papers/).
All sums marked "my sum" are my own arithmetic over a paper's table.

Abbreviations. FM: foundation model (a network pretrained on many images, then adapted). SSL:
self-supervised learning (pretraining without labels). MAE: masked autoencoder. SAM: Segment
Anything Model. VLM: vision-language model. EUS: endoscopic ultrasound. CEUS: contrast-enhanced
ultrasound. ABUS: automated breast ultrasound (3D). TCIA: The Cancer Imaging Archive. HF: Hugging
Face. CC BY / NC / SA / ND: Creative Commons attribution / non-commercial / share-alike /
no-derivatives. MD5: a file checksum. "High priority" marks abdomen and liver data (project epics 1
and 3: upper-abdomen anatomy segmentation and liver disease).

## 1. Which papers train ultrasound models on large image counts mostly from public sources, and which named papers are private or misnamed?

### Takeaway
Ten papers or resources reach 100k to 5M ultrasound images mostly or only from public data: UltraSam
(US-43d), USF-MAE (OpenUS-46), OpenUS, UltraFedFM (about 70 to 77% public), URFM (about 46% public),
EchoCare (EchoCareData, 138 public datasets, sources not listed), UltraSAM3, SonoCorpus/SonoBase
(53 datasets, 2026), US-JEPA (OPUS, 5.1M frames from 50 datasets, 2026) and SAMUS (US30K, smaller).
UltraDINO, USFM, FetalCLIP and the echo models (EchoCLIP, EchoPrime, EchoFM) are mainly or wholly
private; the general medical sets (MedSAM, SA-Med2D-20M, IMed-361M, BiomedParse, MedSAM2) contain
only a small ultrasound part.

### Cited Findings
Table 1.1. Each paper named in the brief, plus others found, and whether its training data are
public. "Checked at" is the primary source read.

| Paper (venue, year) | Data verdict | Checked at |
|---|---|---|
| UltraSam, US-43d (IJCARS 2025) | public only: 43 open-access datasets | [arXiv 2411.16222](https://arxiv.org/abs/2411.16222); [doi:10.1007/s11548-025-03517-8](https://doi.org/10.1007/s11548-025-03517-8) |
| USF-MAE, OpenUS-46 (Biomed Signal Process Control 2026, per README) | public only: 46 datasets | [arXiv 2510.22990](https://arxiv.org/abs/2510.22990); journal [doi:10.1016/j.bspc.2026.110313](https://doi.org/10.1016/j.bspc.2026.110313) (from the README, not opened) |
| OpenUS (preprint 2025) | public only: 42 datasets (38 pretraining, 4 downstream) | [arXiv 2511.11510](https://arxiv.org/abs/2511.11510) |
| SAMUS, US30K (MICCAI 2024) | public only: 7 datasets | [arXiv 2309.06824](https://arxiv.org/abs/2309.06824) |
| UltraFedFM (npj Digit Med 2025) | mixed: 782,513 of 1,015,754 images public by the text | [arXiv 2411.16380](https://arxiv.org/abs/2411.16380) |
| URFM (iScience 2025) | mixed: about 46% public (RadImageNet and others), 54% private (West China Hospital) | [Europe PMC full text PMC12312112](https://europepmc.org/article/PMC/PMC12312112); [doi:10.1016/j.isci.2025.112917](https://doi.org/10.1016/j.isci.2025.112917) |
| USFM (Med Image Anal 2024) | mostly private or undisclosed (3M-US) | [GitHub README](https://github.com/openmedlab/USFM); constituents "not disclosed" per [UltraBench 2, Table 11](https://arxiv.org/abs/2609.28610); OpenUS calls it "two million private US images" ([arXiv 2511.11510](https://arxiv.org/abs/2511.11510)); paper itself not open access, not re-read |
| EchoCare, EchoCareData / EchoAtlas (preprint 2025) | public by the paper: 138 datasets, 4.5M images; names not listed anywhere I could find | [arXiv 2509.11752](https://arxiv.org/abs/2509.11752); [README](https://github.com/CAIR-HKISI/EchoCare); [homepage](https://echocare.cares-copilot.com/) |
| UltraSAM3 (preprint 2026) | public only: 37 datasets | [arXiv 2607.29200](https://arxiv.org/abs/2607.29200) |
| SonoCorpus and SonoBase (preprint 2026, v2 15 Oct 2026) | public only: 53 datasets | [arXiv 2609.19230](https://arxiv.org/abs/2609.19230) |
| US-JEPA, OPUS corpus (preprint 2026) | public only: 50 datasets, 5,123,697 frames | [arXiv 2602.19322](https://arxiv.org/abs/2602.19322) |
| UltraDINO, FUS2M (MICCAI 2025) | private: 2M fetal images from the Danish national fetal database | [arXiv 2506.19552](https://arxiv.org/abs/2506.19552); local PDF 57 |
| MedSAM (Nat Commun 2024) | public, all modalities: 1,570,263 image-mask pairs, 10 modalities; ultrasound share not in the text | [arXiv 2304.12306](https://arxiv.org/abs/2304.12306) |
| SA-Med2D-20M / SAM-Med2D (2023) | "public and private datasets"; ultrasound 2,968 of 4.6M images | [arXiv 2311.11969](https://arxiv.org/abs/2311.11969); [arXiv 2308.16184](https://arxiv.org/abs/2308.16184) |
| IMIS-Bench, IMed-361M (2024; CVPR 2025, venue unverified) | 110 public datasets plus some clinical data; 5 ultrasound datasets | [arXiv 2411.12814](https://arxiv.org/abs/2411.12814) |
| BiomedParse (2024) | 45 public datasets, 9 modalities, about 1.1M images; ultrasound part not extracted | [arXiv 2405.12971](https://arxiv.org/abs/2405.12971) |
| MedSAM2 (2025) | public: ultrasound = 19,232 annotated frames | [arXiv 2504.03600](https://arxiv.org/abs/2504.03600) |
| EchoCLIP (2023/2024) | private: 1,032,975 echo videos, Cedars-Sinai | [arXiv 2308.15670](https://arxiv.org/abs/2308.15670) |
| EchoPrime (2024) | private: 12,124,168 echo videos, Cedars-Sinai | [arXiv 2410.09704](https://arxiv.org/abs/2410.09704) |
| EchoFM (2024) | mostly private: 286,080 internal videos (over 20M images) plus CAMUS and EchoNet-Dynamic | [arXiv 2410.23413](https://arxiv.org/abs/2410.23413) |
| FetalCLIP (2025) | private: 207,943 clinical images (Corniche Hospital, Abu Dhabi) plus 2,092 textbook image-caption pairs | [arXiv 2502.14807](https://arxiv.org/abs/2502.14807) |
| PanEcho | not checked | – |
| UniUSNet, BroadUS-9.7K (BIBM 2024) | public: 10 datasets, about 9.7k images | [README](https://github.com/Zehui-Lin/UniUSNet); [arXiv 2406.01154](https://arxiv.org/abs/2406.01154) |
| TinyUSFM, UniUS-Bench (IEEE JBHI 2026) | 200,000-image subset of USFM's data; benchmark from public data | only via [UltraBench 2, Appendix A.2](https://arxiv.org/abs/2609.28610); paper [doi:10.1109/JBHI.2026.3678309](https://doi.org/10.1109/JBHI.2026.3678309) not read |
| Ultrasound-CLIP, US-365K (preprint 2026) | public web: 364,365 image-text pairs from 5 public repositories | [arXiv 2604.01749](https://arxiv.org/abs/2604.01749) |
| Dolphin (technical report 2025) | mixed: over 2M samples from textbooks, public repositories, guidelines and synthetic data | [arXiv 2509.25748](https://arxiv.org/abs/2509.25748) |
| DeblurringMIM (Kang et al. 2023) | private thyroid images, West China Hospital | local PDF 15; [arXiv 2306.08249](https://arxiv.org/abs/2306.08249) |

- The "AUL dataset" of the earlier study is Annotated Ultrasound Liver images (Xu et al.), a public
  liver set of 735 images used by UltraBench 2 for liver-mass classification, liver-mass
  segmentation and liver segmentation — [UltraBench 2, Table 2](https://arxiv.org/abs/2609.28610).
- UltraDINO's FUS2M: "a random sample of 2 million ultrasound images" from three of five Danish
  regions, 2008 to 2018, under national approvals; evaluation on public FASS, JNU-IFM and Fetal
  Planes — [arXiv 2506.19552](https://arxiv.org/abs/2506.19552), local PDF 57, p. 3.
- The three other local PDFs are small: DeblurringMIM pretrained on 10,675 private thyroid images
  ([arXiv 2306.08249 v3](https://arxiv.org/abs/2306.08249), local PDF 15); Chen et al. 2025 used
  TN3K and BUSI ([arXiv 2503.13987](https://arxiv.org/abs/2503.13987), local PDF 35); Echo from
  noise trained on CAMUS and tested on EchoNet-Dynamic (local PDF 47). UniverSeg's MegaMedical
  (local PDF 53) has four ultrasound sets: BUS (163), CAMUS (500), HMC-QU (292), Thyroid
  cine-clip (167).
- No paper I read says it drew on Roboflow Universe. Two rows of Alsharid et al. ("Liver
  ultrasound computer vision project", "Ultrasound normal kidney image computer vision dataset")
  and UltraSAM3's "Ultrasound_Normal_Kidney" have Roboflow-style names (unverified; not chased, out
  of scope under [DEC-081](../../decisions/DEC-081-epic2-mission-roboflow-universe-ultrasound-scraper.md) and [DEC-096](../../decisions/DEC-096-epic2-retrieval-path-official-routes-terms-reading-fetch-budget.md), the epic 2 Roboflow scraper decisions).

### Inferences
- The brief's names are all real papers; the private ones (UltraDINO, USFM, FetalCLIP, EchoCLIP,
  EchoPrime, mostly EchoFM) are useful only as weights, not as data recipes.
- The 2026 papers (SonoCorpus, US-JEPA, UltraSAM3, UltraBench 2) are newer than the project's
  earlier studies and carry the best per-dataset tables.

### Gaps
- PanEcho, EchoApex and SonoSAM were not checked (budget). BiomedParse's and MedSAM's ultrasound
  datasets sit in supplementary tables and figures I did not read.
- USFM's dataset composition was not re-read at source (paper not open access).

## 2. For each paper: total images, number of datasets, public versus private share, and the public datasets with counts

### Takeaway
Per-dataset tables exist for US-43d, OpenUS-46, OpenUS, UltraFedFM, URFM, UltraSAM3, SonoCorpus,
OPUS and UltraBench 2; counts for the same dataset often differ by source (frames versus images,
versions, train-only splits). Abdominal and liver public data are small except RadImageNet's
ultrasound subset (about 390k images with organ labels) and CEUS liver video sets.

### Cited Findings
Table 2.1. Totals as stated, with my sums of each paper's own table where they differ.

| Paper | Images (as stated) | Datasets | Public share | My sum of the per-dataset table |
|---|---|---|---|---|
| UltraSam US-43d | 282,321 image-mask pairs ("annotated segmentation masks") | 43 | 100% | 42 rows ("MUP & MicroSeg" is one row): 186,894 images, 279,765 masks |
| USF-MAE OpenUS-46 | about 370,000; "374,192 images exactly" | 46 | 100% | 374,192 (matches) |
| OpenUS | 308,584 images in 42 datasets | 38 pretraining + 4 downstream | 100% | 38 pretraining rows: 290,036; plus 4 downstream: 309,364 |
| SAMUS US30K | about 30k images, 69k masks | 7 | 100% | per-dataset counts only in the supplement (not found) |
| UltraFedFM | 1,015,754; 782,513 public | 14 public + 2 private clients (16) | 77% (text) | Suppl. Table 1: public 719,087 + private 299,059 = 1,018,146 (71% public) |
| URFM | 1,003,465 | 6 public sources + private | 45.6% | public 457,340, private 546,125 (sums to the total) |
| EchoCare EchoCareData | over 4.5M "image-class tuples" | 138 | 100% (paper) | no table |
| UltraSAM3 | 112,634 train images, 171,693 masks; test 25,986 images | 37 | 100% | Table 3 total given |
| SonoCorpus | 456,963 images or frames; 1,626,085 masks | 53 (40 2D, 8 video, 5 3D) | 100% | Table S1 total given |
| US-JEPA OPUS | 5,123,697 frames | 50 | 100% | Table A.1 |
| UltraBench 2 | 21 tasks, training split capped at 1,000 examples per task | 12 | 100% | Table 2 |

Sources: [US-43d](https://arxiv.org/abs/2411.16222) (Section 2.1, Table 1); [OpenUS-46](https://arxiv.org/abs/2510.22990) (Section 2.1, Table 1); [OpenUS](https://arxiv.org/abs/2511.11510) (Section 4.1, Table 6); [SAMUS](https://arxiv.org/abs/2309.06824); [UltraFedFM](https://arxiv.org/abs/2411.16380) (Methods, Supplementary Table 1); [URFM](https://europepmc.org/article/PMC/PMC12312112) (Table 1); [EchoCare](https://arxiv.org/abs/2509.11752) (Sections 2.1, 4.3); [UltraSAM3](https://arxiv.org/abs/2607.29200) (Section 4.1, Table 3); [SonoCorpus](https://arxiv.org/abs/2609.19230) (Table S1); [US-JEPA](https://arxiv.org/abs/2602.19322) (Section 5.1, Table A.1); [UltraBench 2](https://arxiv.org/abs/2609.28610) (Table 2).

Per-dataset lists, as printed (count unit as in the paper):

- **US-43d** (images / masks) — [arXiv 2411.16222, Table 1](https://arxiv.org/abs/2411.16222):
  Brachial Plexus 40,788/36,736; EchoNet-Dynamic 20,048/20,048; CAMUS 19,232/58,570; Thyroid US
  CineClip 17,412/17,412; EchoNet-Pediatric 15,449/15,449; SegThy 12,737/22,928; ACOUSLIC
  6,620/6,620; US Nerve Segmentation 5,635/2,323; regPro 4,706/6,492; STMUS NDA 4,355/4,368;
  FH-PS-AOP 4,000/7,999; TNSCUI 3,644/3,659; TG3K 3,585/23,283; TN3K 3,493/3,821; MUP & MicroSeg
  2,910/2,650; ASUS 2,864/7,887; CardiacUDC 1,961/7,251; BUS-BRA 1,875/1,875; FASS 1,588/6,383;
  MMOTU 2d 1,489/1,489; Fast-U-Net 1,411/1,407; EchoCP 1,300/2,364; Common Carotid Artery
  1,100/1,100; HC18 999/999; UBPD 939/4,416; FALLMUD 810/1,626; BUS-UC 810/791; **AUL 735/2,102
  (high priority)**; "Breast" 690/690 (the README lists BUSI in its place; same dataset, unverified);
  DDTI 637/645; LUSS phantom 564/3,816; GIST514-DB 514/505; **KidneyUS 487/487 (high priority)**;
  BUS-UCLM 264/281; BrEaST 252/266; BUID 232/236; S1 201/204; MMOTU 3d 187/187; BUS 164/164;
  **105US 105/105 (liver, high priority)**; **AbdomenUS 60/89 (high priority)**; STU-Hospital 42/42.
- **OpenUS-46** (images used) — [arXiv 2510.22990, Table 1](https://arxiv.org/abs/2510.22990):
  105US 105; AbdomenUS 1,544; ACOUSLIC 300; AUL 735; BLUES 4,133; BP 11,143 (README links the
  Kaggle nerve set); brachial plexus 7,462; BrEaST 256; BUS (Dataset B) 163; BUS_UC 811; BUS_UCML
  683; BUS-BRA 1,875; Cactus 37,736; CAMUS_public 19,237; CardiacUDC 760; CCAUI 1,100; DFHI 3,832;
  EchoCP 11,519; EchoNet-Dynamic 112,740; EchoNet-Pediatric 46,573; FALLMUD 813; FASS 1,588;
  Fast-U-Net 1,414; FEFT 6,720; FETAL_PLANES_DB 12,400; FH-PS-AOP 4,000; GIST514-DB 514; HC 1,334;
  JNU-IFM 6,224; kidneyUS 534; LUSS_phantom 564; MicroSeg 2,910; MMOTU-2D 1,469; MMOTU-3D 170;
  Pocus 2,264; Porcine (spinal cord, animal) 12,468; PSFHS 1,358; regPro 6,424; S1 201; Segthy
  15,820; STMUS_NDA 8,169; STU-Hospital 42; Thyroid Dataset (TRFE-Net repository) 3,838; Thyroid US
  Cineclip 17,412; Ultrasound Fetus Dataset (Kaggle) 1,880; UPBD 955. 36 of US-43d's 43 sets were
  kept; 7 were dropped as inaccessible, redundant or duplicated.
- **OpenUS** pretraining (images) — [arXiv 2511.11510, Table 6](https://arxiv.org/abs/2511.11510):
  105US 105; AbdomenUS 617; ACOUSLIC 6,620; ASUS 2,865; AUL 735; brachial plexus 40,788; BrEaST
  252; BUID 232; BUS UC 810; BUS UCML 264; BUS 163; CAMUS 19,232; CCAUI 1,100; DDTI 637;
  EchoNet-Dynamic 20,048; EchoNet-Pediatric 15,450; FALLMUD 813; FASS 1,588; Fast-U-Net 1,411;
  GIST514-DB 43,656 (as printed, against 514 elsewhere); HC 1,334; kidneyUS 487; LUSS phantom 564;
  MicroSeg 1,931; MMOTU-2D 1,469; MMOTU-3D 170; regPro 4,706; S1 201; Segthy 12,737; STMUS NDA
  4,355; STU-Hospital 42; TG3K 3,585; Thyroid US Cineclip 17,412; UPBD 955; US nerve Segmentation
  11,134; USAnotAI 366; Cactus 37,736; IUGC25 33,466. Downstream: BUSI (1,560 as stated), Fetal
  Planes 12,400, BUS-BRA 1,875, TN3K 3,493.
- **SAMUS US30K**: TN3K, DDTI, TG3K, BUSI, UDIAT, CAMUS, HMC-QU — [README](https://github.com/xianlin7/SAMUS).
- **UltraFedFM** clients (images) — [arXiv 2411.16380, Supplementary Table 1](https://arxiv.org/abs/2411.16380):
  BUV 25,727; **CLUST (liver) 35,626**; EchoNet-Dynamic 150,243; FETAL-PLANES 12,400; TDSC-ABUS
  126,918; Leg-3D-US 115,263; Thyroid Ultrasound Cine-clip 17,412; **SYSU-FLL-CEUS (liver CEUS)
  118,485**; CAMUS 21,214; COVID-BLUES 42,226; NerveUS 11,143; **LEPset (pancreas EUS) 11,499**;
  FPUS 20,378; **GBUSV (gallbladder video) 10,553**; private: ERUS 63,426 and PrivateUS 235,633.
  Downstream public sets include LEPset, SYSU-FLL-CEUS, GBCU, BUSI, BUV, BUS-BRA, BUS-UCLM, POCUS,
  FETAL-PLANES, HFUS, NerveUS, DDTI, Thyroid cine-clip, TG3K, TN3K, LUMINOUS, CardiacUDA, JNU-IFM
  (Data availability). Countries: China 57.30%, United States 15.94%, Germany 10.14%.
- **URFM** (images) — [Table 1](https://europepmc.org/article/PMC/PMC12312112): RadImageNet thyroid
  92,566, **kidney 111,209, liver 74,852, gallbladder 39,743, pancreas 21,639, spleen 6,518, bile
  duct 3,646, aorta 18,097 (high priority)**, bladder 758, uterus 15,400, ovary 3,593, vein 1,725
  (RadImageNet total 389,746, my sum); BUV 26,052; ultrasoundcases.info 2,255; LEPset 8,000; CAMUS
  18,887; FETAL_PLANES_DB 12,400; private: thyroid 351,419, breast 56,356, mixed abdomen 123,037,
  bladder 15,313. Downstream public: BUS-BRA, AUL, LEPset, MMOTU-2D, Fetal Planes, BUID.
- **UltraSAM3** (train images) — [arXiv 2607.29200, Table 3](https://arxiv.org/abs/2607.29200):
  **AbdomenUS 788**; BUID 185; BUSI 624; BUS_BRA 1,500; BUS_DatasetB 130; BUS_UC 648; S1 192; CAMUS
  1,600; CardiacUDC 1,717; EchoCP 434; EchoNet_Dynamic 17,496; EchoNet_Pediatric 12,071; Unity
  13,136; CCA 2,307; ACOUSLIC 5,327; FASS 1,270; Fast_UNet 1,128; HC 799; fh_ps 3,200; focus 250;
  **KidneyUS 388; Ultrasound_Normal_Kidney 864; Annotated_Ultrasound_Liver 588**; LUSS 451; FALLMUD
  650; LUMINOUS 272; STMUS_NDA 6,535; UPBD 764; OTU_2d 1,175; OTU_3d 136; MicroSeg 2,079; RegPro
  3,518; DDTI 509; Segthy 10,675; TG3K 2,868; TN3K 2,794; Thyroid_US_Cineclip 13,566. External
  test sets: BrEaST, CCAUI, 105US_tumor, KFGNet.
- **SonoCorpus** (deduplicated images or frames; masks) — [arXiv 2609.19230, Table S1](https://arxiv.org/abs/2609.19230):
  AbdomenUS 59; ASUS 2,825; AUL 735 (1,367 masks); BrEaST 252; BUID 232; BUS 159; BUS-UC 811;
  BUS-UCLM 263; BUSI-WHU 927; CardiacNet 1,550; CardiacUDC 1,409; CDNet (cervix) 325;
  Common-Carotid-Artery 1,100; EchoCP 558; EchoNet-Dynamic 20,048; EchoNet-Pediatric 15,450;
  FALLMUD 813; FASS 1,563; Fast-U-Net 406; GIST514-DB 514; JNU-IFM 5,202; LUSS 561; MI-SegNet
  2,143; MMOTU-2d 1,469; MUP 2,621; PPL (lung) 2,756; RVENet 247,014 (1,235,070 masks); S1 192;
  SegThy 12,726; STMUS-NDA 8,153; STU-Hospital 42; TDSC-ABUS 3,166; ThyroidUSCineClip 17,412; TN3K
  3,493; TNSCUI 3,568; UBPD 946; US-Nerve 2,295; US105 105; benchmark tier: Brachial-Plexus 39,025;
  BUSI 646; C-TRUS 477; CAMUS 19,232; HC18 998; PFUS 13,906; RegPro 4,688; TG3K 3,585; external
  tier: ACOUSLIC 6,620; BUS-BRA 1,875; DDTI 629; FUGC 440; **KidneyUS 468**; LUMINOUS 341;
  MMOTU-3d 170. 17 countries.
- **OPUS** (frames) — [arXiv 2602.19322, Table A.1](https://arxiv.org/abs/2602.19322): EchoNet-LVH
  1,957,928; EchoNet-Dynamic 1,770,636; Prostate-MRI-US-Biopsy 219,484; SegThy 136,243;
  **B-mode-and-CEUS-Liver 126,543; SYSU-CEUS-FLL 110,654; RadImageNet kidney 111,252, liver 78,535,
  gallbladder 39,743, pancreas 21,645, spleen 6,520, portal vein 769 (high priority)**; RadImageNet
  thyroid 92,598, cardiac 19,062, uterus 13,312, ovarian 3,595, fibroid 2,095, bladder 758;
  EchoNet TEE View Classifier 55,261; ABUS-TDSC 44,474; cardiacUDC 38,071; COVID-Blues 31,696; BUV
  25,026; COVIDx-US 22,697; CAMUS 19,232; ReMIND 18,734; ultrasoundcases.info (all organs; e.g.
  muscle 17,459, breast 4,956, **kidney 3,924, abdominal 3,199, liver 2,714, pancreas 1,506,
  spleen 1,207, gallbladder 1,186**); Stanford Thyroid Cine 17,412; LEPset 11,493; NerveUS 11,143;
  **GB1 (gallbladder) 10,692**; Thyd2 8,489; MuscleUS 8,169; **TRUSTED (kidney, 3D) 7,280**;
  ProstateTRUS 5,037; PCOS_US 3,841; TG3K 3,585; TN3K 3,493; Mus-V 3,114; MUPSD 2,910; Yang
  (uterus) 1,973; cardiacCCAUS 1,100; BUSI_WHU 927; UBPD 955; BUSI 780; BUS_UC 811; BUS_UCLM 683;
  **abdominal_US 617**; DDTI 610; GIST_EUS 514; **OpenKidney 500**; Carotid US Boundary Study 500;
  ovarianUS 301; Breast-Lesions-USG 256; BUSC 250; DatasetA 250; BUID 205; Breast_S1 201; UDIAT
  163; 105US 105 (labelled pancreas here); **USAnotAI 61 each for liver, kidney, gallbladder,
  spleen, bowel, bladder**. Downstream: AUL, Butterfly, Fatty Liver, BUS-BRA, TN5000 and others
  from UltraBench.
- **UltraBench 2** datasets and licences — [arXiv 2609.28610, Tables 2 and 3](https://arxiv.org/abs/2609.28610):
  **AUL (CC BY 4.0; liver mass classification and segmentation, liver segmentation, 735 frames)**;
  BUS-BRA (CC BY 4.0); CAMUS (CC BY-NC-SA 4.0); COVID-BLUES (CC BY-NC-ND 4.0); Fetal Planes (CC BY
  4.0); **GBCU (research use, from the provider)**; **MASLD = Byra fatty liver (CC BY 4.0; 55
  patients)**; MMOTU-2D (CC BY-NC-ND 4.0); **Open Kidney (research use, from the provider; capsule
  and regions)**; PSFHS (CC BY 4.0); STMUS (CC BY 4.0); TN3K (MIT). Excluded by name: BUSI (data
  quality), LEPset (heavy on-image annotations), Butterfly, POCUS, US Nerve (licensing), Stanford
  Thyroid (size).
- **General medical sets**: SA-Med2D-20M has 2,968 ultrasound images and 2,968 masks of 4.6M images
  (TN-SCUI2020, not redistributed; Kaggle Nerve; BUSI) — [arXiv 2311.11969, Table 1 and
  appendix](https://arxiv.org/abs/2311.11969). IMed-361M (6.4M images, 110 datasets) lists five
  ultrasound sets: CETUS2014, CuRIOUS2022 tumour, TDSC-ABUS2023, µ-RegPro, DDTI —
  [arXiv 2411.12814, appendix](https://arxiv.org/abs/2411.12814). MedSAM2 used 19,232 ultrasound
  frames and annotated 251,550 RVENet echo frames with its human-in-the-loop pipeline —
  [arXiv 2504.03600](https://arxiv.org/abs/2504.03600). BroadUS-9.7K: BUSI, BUSIS, UDIAT, BUS-BRA,
  **Fatty-Liver (Byra)**, **kidneyUS**, DDTI, Fetal HC, CAMUS, **Appendix (Zenodo 7669442)** —
  [README](https://github.com/Zehui-Lin/UniUSNet).
- **Vision-language sets**: US-365K draws 364,365 image-text pairs from ultrasoundcases.info, LITFL
  100+ Ultrasound Quiz, MedPix, POCUS Atlas and RadImageNet — [arXiv 2604.01749, Section 3](https://arxiv.org/abs/2604.01749).
  U2-Bench samples 7,241 cases from 40 licensed datasets, 25 of them taken from Alsharid et al. —
  [arXiv 2505.17779, Section 3 and Table 7](https://arxiv.org/abs/2505.17779). FETAL-GAUGE: 42,036
  images and 93,451 question-answer pairs from 13 public fetal datasets — [arXiv 2512.22278, Table 5](https://arxiv.org/abs/2512.22278).

### Inferences
- Labelled public abdominal masks are small: AUL 735, Open Kidney about 500, AbdomenUS about 60 to
  800 (counts disagree), 105US 105, USAnotAI 366 — about 1.5k to 2.5k images in all, an order of
  magnitude below the project's about 20k labelled images. RadImageNet's ultrasound subset (about
  390k abdominal and pelvic images with organ-level labels, used by URFM, OPUS and Project
  Imaging-X) and the CEUS liver video sets are the only large public abdominal sources; neither
  carries organ masks as far as these papers say (Imaging-X lists RadImageNet-US as classification).
- For epic 3 (liver disease), the papers' public liver-disease sets are AUL (mass classes), Byra
  fatty liver (steatosis), B-mode-and-CEUS-Liver and SYSU-FLL-CEUS (focal lesions), plus smaller
  ones from Alsharid et al. (BEHSOF, Ultrasound Elastography).

### Gaps
- SAMUS's per-dataset counts (supplement), EchoCare's 138 dataset names, USFM's sources and
  MedSAM's ultrasound datasets were not found.
- Conflicts left open: GIST514-DB 43,656 in OpenUS against 514 elsewhere; USF-MAE "10,578 images
  reserved for evaluation" against the 3,858 its Table 1 gives for those three sets, and the README's
  "360K from 43 datasets"; UltraFedFM text against its supplement (above); DeblurringMIM 10,675
  pretraining images (arXiv v3) against "about 280,000" in [UltraBench 2, Appendix A.8](https://arxiv.org/abs/2609.28610)
  and "280K" in [OpenUS](https://arxiv.org/abs/2511.11510) (a later version may differ, unverified).

## 3. How did the papers count images, and what is a fair basis for comparing with about 20k labelled images?

### Takeaway
The headline counts mix video frames, 3D slices and (in places) masks; a few echocardiography,
nerve and thyroid-cine video sets supply most of each total. Comparing like with like means
counting distinct labelled still images (or patients), with frames from one video counted once.

### Cited Findings
- US-43d counts annotated frames and slices; 3D volumes are cut to sagittal slices — [arXiv 2411.16222, Section 2.1](https://arxiv.org/abs/2411.16222).
  By my sum of its Table 1, five video-derived sets (Brachial Plexus, EchoNet-Dynamic, CAMUS,
  Thyroid cine-clip, EchoNet-Pediatric) give 112,929 of 186,894 images (60%).
- OpenUS-46 sampled videos at 3 frames per second and treated frames as independent images,
  resized to 224 × 224 px — [arXiv 2510.22990, Section 2.1](https://arxiv.org/abs/2510.22990).
- EchoCare sampled videos at 10-frame intervals, removed images with under 1,000 non-zero pixels,
  deduplicated by URL and image hash, and counts "image-class tuples"; it screened about 13,000
  candidates, then 1,136 to 334 entries, ending at 138 datasets; GPT-4o extracted download links —
  [arXiv 2509.11752, Sections 2.1, 4.3, 4.4](https://arxiv.org/abs/2509.11752).
- UltraFedFM's public total is dominated by frames and slices: EchoNet-Dynamic 150,243, TDSC-ABUS
  (3D) 126,918, SYSU-FLL-CEUS 118,485 and Leg-3D-US (3D) 115,263 are 510,909 of the 719,087 public
  images in its supplement (71%, my sum) — [arXiv 2411.16380](https://arxiv.org/abs/2411.16380).
- SonoCorpus counts deduplicated images or frames and flattens 3D volumes to slices; RVENet alone
  is 247,014 of 456,963 (54%), and eight video or 3D sets give 384,813 (84%, my sum) —
  [arXiv 2609.19230, Table S1](https://arxiv.org/abs/2609.19230).
- OPUS: 79.7% of 5,123,697 frames come from video; EchoNet-LVH plus EchoNet-Dynamic are 3,728,564
  (73%, my sum) — [arXiv 2602.19322, Section 5.1 and Table A.1](https://arxiv.org/abs/2602.19322).
- UltraBench 2 caps each task's training split at 1,000 patients, sequences or images and splits by
  patient — [arXiv 2609.28610, Section 3](https://arxiv.org/abs/2609.28610).
- Augmentation is applied during training, not counted (OpenUS lists flips, colour jitter, blur —
  [arXiv 2511.11510, Section 7.1](https://arxiv.org/abs/2511.11510)). Phantoms and simulation are
  inside some totals: Cactus (heart phantom, 37,736), FPUS23 (fetal phantom), LUSS (lung phantom),
  and AbdomenUS, whose source is titled "US simulation and segmentation" (Vitale et al. 2020) —
  [OpenUS-46 Table 1](https://arxiv.org/abs/2510.22990); [U2-Bench Table 7](https://arxiv.org/abs/2505.17779).

### Inferences
- A fair comparison with the project's about 20k labelled images: count distinct labelled still
  images with masks, frames per video counted once, by anatomy. On that basis the public total with
  masks is likely low hundreds of thousands at most, mostly heart, nerve, thyroid, breast and fetal;
  the upper-abdomen share is about 1% to 2% (estimate from the tables above, not a count).
- Unlabelled scale for SSL pretraining is different: OPUS and EchoCareData reach millions of frames,
  but most frames are highly correlated echo video.

### Gaps
- No paper reports distinct patients across its whole corpus; SonoCorpus records patient-level
  splits where identifiers exist but gives no corpus-wide patient total.

## 4. Did any paper release combined data, a preprocessing pipeline or download scripts, and under what licence?

### Takeaway
The most reusable shortcuts are SonoCorpus's Zenodo manifest (53 datasets with source, access,
licence, split indices and MD5 checksums of every file; no images) and the UltraBench 2 Python
package (12 datasets, 10 hosted on Hugging Face, fixed splits). UltraSam ships per-dataset COCO
converters for US-43d. SAMUS is the only paper that redistributes a combined image set (US30K).

### Cited Findings
Table 4.1. Released data and tooling. Licence and last push are from the GitHub API (read 2026-11-26)
unless the cell says otherwise.

| Resource | What it releases | What it automates | Licence | Last push |
|---|---|---|---|---|
| SonoCorpus / SonoBase | versioned manifest on Zenodo ([doi:10.5281/zenodo.22770825](https://doi.org/10.5281/zenodo.22770825)): source, access conditions, licence, metadata, split indices, MD5 of every file; does not redistribute images | verifying a self-downloaded copy, reusing splits; "continuously updated" | code MIT, weights CC BY-NC 4.0 (paper); manifest licence not checked | repo not checked |
| UltraBench 2 ([GitHub](https://github.com/adamtupper/ultrabench), `pip install ultrabench`) | prepared versions of 10 of 12 datasets on Hugging Face; GBCU and Open Kidney processed locally from the provider's files | download, standardised preprocessing, fixed train/test splits, evaluation scripts, leaderboard | MIT (code); data under each source licence (Table 3) | 2026-11-11 |
| UltraSam US-43d ([GitHub](https://github.com/CAMMA-public/UltraSam)) | one link per dataset (43); converters to COCO per dataset; merge, split and class-agnostic scripts | conversion and merging after manual download; no download | CC BY-NC-SA 4.0 (LICENSE file) | 2026-04-13 |
| USF-MAE OpenUS-46 ([GitHub](https://github.com/Yusufii9/USF-MAE)) | link table for 46 datasets; Google Drive link for three more ("OpenUS-49", contents not opened) | nothing beyond links | MIT | 2026-04-25 |
| OpenUS ([GitHub](https://github.com/XZheng0427/OpenUS)) | link table for 42 datasets; downstream preparation scripts (BrainBenchmark, CAMUS, USenhance, FOCUS) | downstream manifests only | README badge CC BY-NC 4.0; no licence file detected | 2026-06-09 |
| SAMUS ([GitHub](https://github.com/xianlin7/SAMUS)) | preprocessed US30K (PNG) on Google Drive | a ready combined set of 7 datasets | MIT (code); data licence not stated | 2025-04-17 |
| UltraFedFM ([GitHub](https://github.com/yuncheng97/UltraFedFM)) | links in the paper's Data availability; preprocessing code | folder layout for 16 clients | Apache-2.0 | 2026-07-11 |
| UltraSAM3 ([GitHub](https://github.com/zhuqh19/UltraSAM3)) | name table of 37 datasets; weights on Hugging Face | none for data | no licence detected | 2026-10-11 |
| EchoCare ([GitHub](https://github.com/CAIR-HKISI/EchoCare)) | paper says EchoCareData is at the homepage with all download links; the README's dataset sections are empty links and the homepage lists no datasets (WebFetch, 2026-11-26) | none found | no licence detected | 2025-12-03 |
| MedSAM2 ([GitHub](https://github.com/bowang-lab/MedSAM2)) | annotated RVENet frames ([HF](https://huggingface.co/datasets/wanglab/RVENet-MedSAM2)); a dataset-list site, [medsam-datasetlist.github.io](https://medsam-datasetlist.github.io) (not opened) | – | Apache-2.0 | 2025-07-11 |
| IMIS-Bench ([GitHub](https://github.com/uni-medical/IMIS-Bench)) | IMed-361M on Hugging Face | – | no licence detected | 2025-02-27 |
| UniUSNet ([GitHub](https://github.com/Zehui-Lin/UniUSNet)) | links for 10 datasets, demo data layout | – | no licence detected | 2025-06-25 |
| U2-Bench ([HF](https://huggingface.co/datasets/DolphinAI/u2-bench)) | 7,241 benchmark cases | evaluation toolkit | not checked | – |
| US-365K ([HF](https://huggingface.co/datasets/JJY-0823/US-365K)) | 364,365 image-text pairs scraped from public web repositories | – | not checked | – |

Other licences: USFM CC BY-NC 4.0 (LICENSE file); FetalCLIP CC BY-NC 4.0; DeblurringMIM CC BY-NC
4.0; MedSAM, SAM-Med2D, BiomedParse, UltraDINO Apache-2.0 (GitHub API, 2026-11-26).

- UltraBench 2's own comparison: US-43d gives preprocessing code but no fixed splits and no download
  interface; UniUS-Bench and UltraFedFM give neither; "existing benchmarks also only link to the
  original datasets" — [arXiv 2609.28610, Table 1 and Section 2.1](https://arxiv.org/abs/2609.28610).
- SonoCorpus Table S1b records each source's licence as audited on 14 September 2026, e.g. AUL,
  BrEaST, FASS, HC18, BUS-BRA CC BY 4.0; CAMUS, RegPro, ACOUSLIC, KidneyUS CC BY-NC-SA 4.0;
  EchoNet-Dynamic, EchoNet-Pediatric, RVENet research-use agreements; TDSC-ABUS and TNSCUI
  challenge-only terms; 14 "Not stated" — [arXiv 2609.19230, Table S1b](https://arxiv.org/abs/2609.19230).

### Inferences
- For a download plan, start from the SonoCorpus manifest (widest licence audit and checksums),
  use UltraBench 2's loader for its 12 datasets, and US-43d's converters for COCO masks. None of
  them automates downloads behind registration (EchoNet, Stanford, Open Kidney, GBCU).
- SAMUS's US30K redistributes CAMUS (CC BY-NC-SA) and other sets without a stated licence; use the
  original sources instead (my judgement, not checked with the authors).

### Gaps
- SonoCorpus's GitHub repository and the Zenodo record's own licence were not opened.
- What USF-MAE's "OpenUS-49" Google Drive link holds (it may be an image archive, so it was not
  opened).

## 5. Which surveys and curated lists enumerate public ultrasound datasets?

### Takeaway
The largest dataset-focused catalogue is Alsharid et al. 2025 (72 public ultrasound datasets,
searches to September 2025); the largest per-dataset inventories with counts and licences are
SonoCorpus (53, 2026) and US-43d (43); Project Imaging-X (2026) covers all modalities and lists
about 19 2D and 27 3D ultrasound datasets.

### Cited Findings
Table 5.1. Surveys and lists, with the number of ultrasound datasets each enumerates.

| Source | Date | Ultrasound datasets listed | Notes | Link |
|---|---|---|---|---|
| Alsharid et al., npj Digit Med 8:777 | published 2025-11-24; searches April 2024 to September 2025 | 72 (plus 56 open models) | SonoDQS score of documentation completeness; a webpage was promised "upon paper acceptance", URL not given | [doi:10.1038/s41746-025-02162-4](https://doi.org/10.1038/s41746-025-02162-4); [PMC12722232](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/) |
| SonoCorpus manifest (Qin et al.) | arXiv v2 2026-10-15; licences audited 2026-09-14 | 53 | counts, countries, scanners, licences, checksums | [arXiv 2609.19230](https://arxiv.org/abs/2609.19230); [Zenodo](https://doi.org/10.5281/zenodo.22770825) |
| OPUS (US-JEPA) | 2026 | 50 | frame counts by anatomy | [arXiv 2602.19322](https://arxiv.org/abs/2602.19322) |
| OpenUS-46 (USF-MAE) | 2025 | 46 | link table | [README](https://github.com/Yusufii9/USF-MAE) |
| US-43d (UltraSam) | 2024, README updated 2026 | 43 | link table, converters | [README](https://github.com/CAMMA-public/UltraSam) |
| OpenUS | 2025 | 42 | link table with sizes | [README](https://github.com/XZheng0427/OpenUS) |
| U2-Bench, Table 7 | ICLR 2026 | 40 (25 from Alsharid) | with licences | [arXiv 2505.17779](https://arxiv.org/abs/2505.17779) |
| UltraSAM3 | 2026 | 37 + 4 external | names and paper titles | [README](https://github.com/zhuqh19/UltraSAM3) |
| Project Imaging-X | 2026 | 19 "major" 2D (Table 10 has 24 rows incl. multi-modal TCIA sets, about 457,663 images, 390k of them RadImageNet-US); 27 3D (56,609 volumes) | survey of 1000+ medical datasets | [arXiv 2603.27460](https://arxiv.org/abs/2603.27460); [GitHub](https://github.com/uni-medical/Project-Imaging-X) |
| FETAL-GAUGE | 2025 preprint | 13 fetal | with licences | [arXiv 2512.22278](https://arxiv.org/abs/2512.22278) |
| UltraBench 2 | 2026 | 12 | with licences | [arXiv 2609.28610](https://arxiv.org/abs/2609.28610) |
| BroadUS-9.7K (UniUSNet) | 2024 | 10 | links | [README](https://github.com/Zehui-Lin/UniUSNet) |
| Project journal note | 2026-11-18 | 21 B-mode + 3 raw-signal + 11 hubs | earlier in-project list | [2026-11-18-public-datasets-claude.md](../../journal/2026/2026-11-18-public-datasets-claude.md) |

- The papers searched Papers with Code, Google Dataset Search, GitHub, Google Scholar, Kaggle,
  ResearchGate, Mendeley Data, Zenodo and Data in Brief ([US-43d](https://arxiv.org/abs/2411.16222));
  Alsharid et al. also used WeChat, blogs and ChatGPT with Bing ([PMC12722232](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/)).
- Search-only finds, not opened: a Sensors 2025 review of ultrasound segmentation listing common
  datasets ([PMC12031589](https://pmc.ncbi.nlm.nih.gov/articles/PMC12031589/)); a fetal ultrasound
  deep-learning review covering 2015 to 2024 ([Discover Applied Sciences 2025](https://link.springer.com/article/10.1007/s42452-025-06644-8));
  a GitHub awesome list on ultrasound plane detection ([Yulv-git](https://www.Github.com/Yulv-git));
  a scoping review of radiology vision FMs ([arXiv 2607.07219](https://arxiv.org/abs/2607.07219), saved, not read).

### Inferences
- Cross-checking a per-anatomy census against Alsharid (72) plus SonoCorpus (53) plus OPUS (50)
  covers most names below; U2-Bench and FETAL-GAUGE add Kaggle and fetal sets.

### Gaps
- No dedicated "awesome ultrasound datasets" GitHub list was found in one search. Not counted:
  openmedlab/Awesome-Medical-Dataset (US-43d links to its TN3K and TN-SCUI pages), the MedSAM
  dataset-list site, Hugging Face collections (the 2026-11-18 note found 71 HF results for
  "ultrasound") and Papers with Code (its current status is unverified).
- The Alsharid table was transcribed by the fetch tool's model, not checked line by line.

## 6. Master list: public ultrasound dataset names, with anatomy and the sources that mention each

### Takeaway
About 190 names in total, of which about 35 are abdominal or liver ("high priority"); the
best-covered sets (BUSI, CAMUS, DDTI, TN3K, HC18, Open Kidney, AUL, BUS-BRA) appear in 10 or more
sources. Names vary a lot (aliases are given in each row).

### Cited Findings
Source codes (each links to the table it was read from): U43 = [US-43d Table 1 and README](https://arxiv.org/abs/2411.16222);
O46 = [OpenUS-46 Table 1](https://arxiv.org/abs/2510.22990); OUS = [OpenUS Table 6 and README](https://arxiv.org/abs/2511.11510);
S30 = [SAMUS US30K README](https://github.com/xianlin7/SAMUS); UFF = [UltraFedFM Suppl. Tables 1-2](https://arxiv.org/abs/2411.16380);
URF = [URFM Tables 1-2](https://europepmc.org/article/PMC/PMC12312112); US3 = [UltraSAM3 Table 3](https://arxiv.org/abs/2607.29200);
SC = [SonoCorpus Table S1](https://arxiv.org/abs/2609.19230); OP = [OPUS, US-JEPA Table A.1](https://arxiv.org/abs/2602.19322);
UB2 = [UltraBench 2 Tables 2-3](https://arxiv.org/abs/2609.28610) ("UB2 excl." = named as excluded);
U2B = [U2-Bench Table 7](https://arxiv.org/abs/2505.17779) (my partial parse, about 34 of 40 names);
FG = [FETAL-GAUGE Table 5](https://arxiv.org/abs/2512.22278); AL = [Alsharid et al. Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/);
IX = [Project Imaging-X Table 10 and Section 4.4](https://arxiv.org/abs/2603.27460);
B97 = [BroadUS-9.7K](https://github.com/Zehui-Lin/UniUSNet); IM = [IMed-361M appendix](https://arxiv.org/abs/2411.12814);
SA = [SA-Med2D-20M appendix](https://arxiv.org/abs/2311.11969); MS2 = [MedSAM2](https://arxiv.org/abs/2504.03600);
EF = [EchoFM](https://arxiv.org/abs/2410.23413); UVS = UniverSeg MegaMedical (local PDF 53);
J = [project journal note 2026-11-18](../../journal/2026/2026-11-18-public-datasets-claude.md).
"(ds)" = used only downstream. Counts are as stated by the source in brackets.

Table 6.1. Abdomen, liver, biliary, pancreas, kidney and gastrointestinal (all **high priority**).

| Dataset (aliases) | Anatomy | Mentioned by | Counts as stated |
|---|---|---|---|
| AUL, Annotated Ultrasound Liver | liver, liver masses | U43, O46, OUS, US3, SC, UB2, AL, URF (ds), OP (ds), J | 735 images (U43, SC, AL); masks 2,102 (U43), 1,367 (SC); licence CC BY 4.0 (UB2, SC), "available on request" (AL) |
| 105US (105US_tumor, US105) | liver tumour (OP labels it pancreas) | U43, O46, OUS, US3 (external), SC, OP | 105 |
| AbdomenUS (abdominal_US, "US simulation and segmentation", Vitale et al. 2020) | abdominal organs, bones, vessels; includes simulated images (title) | U43, O46, OUS, US3, SC, OP, U2B | 60 (U43), 59 (SC), 617 (OUS, OP), 986 (US3 train + test), 1,544 (O46) |
| Byra fatty liver (MASLD, Fatty-Liver) | liver steatosis | UB2, AL, U2B, B97, J, OP (ds) | 550 images, 55 patients |
| B-mode-and-CEUS-Liver (TCIA) | liver masses, B-mode and CEUS | AL, OP, J | 120 patients (AL); 126,543 frames (OP) |
| SYSU-FLL-CEUS (SYSU-CEUS-FLL) | liver focal lesions, CEUS video | UFF, OP | 118,485 (UFF); 110,654 (OP) frames |
| CLUST (CLUST15) | liver tracking | UFF, IX | 35,626 (UFF); 34 (IX) |
| BEHSOF | liver | AL | 113 |
| Ultrasound Elastography | liver cancer | AL | 2,000 |
| Liver ultrasound computer vision project | liver | AL | 400; Roboflow-style name (unverified, not chased) |
| Chinese ultrasound-report dataset | breast, thyroid, liver | AL | 7,390 |
| USenhance2023 ("Ultrasound image enhancement") | thyroid, liver, breast, kidney, carotid | AL, IX, OUS (ds) | 2,464 (AL); 1.5k (IX) |
| RadImageNet, ultrasound subset | 15 abdominal and pelvic structures plus thyroid | URF, OP, IX | 389,746 (URF, my sum); about 390k (IX; "commercial license may restrict accessibility") |
| ultrasoundcases.info (teaching website) | many organs | URF, OP | e.g. liver 2,714, kidney 3,924 (OP); a website, not a dataset release |
| USAnotAI | abdominal regions and organs | OUS, OP | 366 (OUS); 61 per organ (OP) |
| Open Kidney Ultrasound Data Set (kidneyUS, KidneyUS, OpenKidney) | kidney | U43, O46, OUS, US3, SC (external), UB2, AL, U2B, B97, OP, J | 514 images (UB2, AL); 487 (U43); 534 (O46); 468 (SC); licence CC BY-NC-SA (SC) |
| Ultrasound Normal Kidney (image dataset) | kidney | US3, AL | 1,080 (AL); Roboflow-style name (unverified) |
| TRUSTED | kidney, 3D | OP | 7,280 |
| AREN0532, AREN0533, AREN0534 (TCIA, multi-modal) | paediatric kidney tumours | IX | – |
| AHEP0731 (TCIA, multi-modal) | liver | IX | – |
| CPTAC-PDA (TCIA, multi-modal) | pancreas | IX | – |
| GBCU, Gallbladder Cancer Ultrasound | gallbladder | UFF (ds), UB2, AL, J | 1,255 images, 218 patients |
| GBUSV, gallbladder ultrasound video | gallbladder | UFF, AL, J | 10,553 frames (UFF); 64 (AL) |
| GB1 (Turki et al. 2025) | gallbladder | OP | 10,692 |
| LEPset | pancreas, EUS | UFF, URF, AL, OP, U2B, UB2 excl. | 11,500 (AL); 8,000 (URF) |
| GIST514-DB (GIST_EUS) | gastrointestinal stromal tumour, EUS | U43, O46, OUS, SC, OP | 514; 43,656 (OUS, as printed) |
| C-TRUS | colon wall, transabdominal | SC, AL, U2B | 477 (SC); 827 (AL) |
| Regensburg Pediatric Appendicitis | appendix, right lower abdomen | AL; B97 "Appendix" (Zenodo 7669442, likely the same, unverified) | 2,097 |
| ASUS | spine (OpenUS labels it abdomen) | U43, OUS, SC | about 2,825 to 2,865 |

Table 6.2. Breast.

| Dataset (aliases) | Mentioned by | Counts as stated |
|---|---|---|
| BUSI | U43 (README), OUS (ds), S30, US3, SC, OP, AL, U2B, IX, B97, SA, UFF (ds), J, UB2 excl. | 780 (AL, OP); 646 to 647 (SC, IX) |
| BUS-BRA | U43, O46, OUS (ds), US3, SC (external), UB2, AL, URF (ds), UFF (ds), B97, J | 1,875 |
| BrEaST (BREAST-LESIONS-USG, Breast-Lesions-USG) | U43, O46, OUS, US3 (external), SC, OP, U2B, IX, J | 252 to 256 |
| BUS Dataset B (UDIAT, UDIAT-B, BUS_DatasetB, "Breast ultrasound B dataset") | U43, O46, OUS, S30, US3, SC, OP, AL, IX, B97, UVS | 159 to 164 |
| BUS_UC (BUS-UC) | U43, O46, OUS, US3, SC, OP | 810 to 811 |
| BUS-UCLM (BUS_UCML) | U43, O46, OUS, SC, OP, UFF (ds) | 263 to 264, or 683 (O46, OP) |
| BUID | U43, OUS, US3, SC, OP, URF (ds) | 205 to 232 |
| S1 (Breast_S1) | U43, O46, OUS, US3, SC, OP | 192 to 201 |
| STU-Hospital | U43, O46, OUS, SC, AL | 42 |
| BUSI-WHU | SC, OP | 927 |
| BUSC (Iqbal 2023a) | OP | 250 |
| DatasetA (Jimenez et al. 2024) | OP | 250 |
| BUSIS | AL, B97 | 562 |
| BUV, breast lesion detection in ultrasound videos | UFF, URF, OP, AL, U2B | 188 videos (AL); about 25,000 to 26,000 frames |
| TDSC-ABUS (ABUS-TDSC, TDSC-ABUS2023), 3D | UFF, OP, SC, IM, IX | 126,918 (UFF); 44,474 (OP); 3,166 (SC); 200 volumes (IX) |
| GDPH & SYSUCC | AL, U2B | 2,405 |
| OASBUD (raw signals) | IX, J | 200 (IX) |
| BreastMNIST (MedMNIST, from BUSI) | IX | 156 (IX, as printed) |
| Ultrasound Breast Images for Breast Cancer (Kaggle, Sairam 2020) | U2B | – |

Table 6.3. Thyroid and neck.

| Dataset (aliases) | Mentioned by | Counts as stated |
|---|---|---|
| DDTI | U43, OUS, S30, US3, SC (external), OP, AL, U2B, IX, B97, IM, UFF (ds), J | 481 to 637 |
| TN3K | U43, OUS (ds), S30, US3, SC, OP, UB2, IX, UFF (ds), J; O46 "Thyroid Dataset" (TRFE-Net repository, 3,838; identity unverified) | 3,493 |
| TG3K | U43, OUS, S30, US3, SC, OP, UFF (ds) | 3,585 |
| TN-SCUI 2020 (TNSCUI) | U43, SC, IX, SA | 3,568 to 3,644 |
| Stanford Thyroid Ultrasound Cine-clip (TUCC) | U43, O46, OUS, US3, SC, OP, UFF, AL, UVS, J, UB2 excl. | 17,412 frames; 167 patients |
| SegThy | U43, O46, OUS, US3, SC, OP | 12,726 to 15,820 images; 136,243 slices (OP) |
| "Thyroid" (Krönke et al. 2022) | AL, U2B | 214 (AL); same author as SegThy (relation unverified) |
| KFGNet (thyroid video) | US3 (external), AL, U2B | 3,668 (AL) |
| TN5000 | AL, OP (ds) | 5,000 |
| Thyd2 (Hou et al. 2024) | OP | 8,489 |
| AUITD (Algerian thyroid, Kaggle) | U2B | – |

Table 6.4. Heart (echocardiography, adult and paediatric).

| Dataset (aliases) | Mentioned by | Counts as stated |
|---|---|---|
| CAMUS | U43, O46, OUS, S30, US3, SC, OP, UFF, URF, MS2, EF, UB2, AL, U2B, IX, B97, UVS, J | 500 patients; 19,232 frames (U43, SC, OP, MS2) |
| EchoNet-Dynamic | U43, O46, OUS, US3, SC, OP, UFF, EF, AL, J | 10,300 videos (AL); 20,048 labelled frames (U43, SC); 1,770,636 frames (OP) |
| EchoNet-Pediatric | U43, O46, OUS, US3, SC, J | 15,449 to 15,450 frames; 46,573 (O46) |
| EchoNet-LVH | OP, AL, J | 12,000 videos (AL); 1,957,928 frames (OP) |
| EchoNet TEE View Classifier | OP | 55,261 frames |
| RVENet | SC, MS2 | 3,583 videos, 831 patients (MS2); 247,014 frames (SC) |
| CardiacUDC (CardiacUDA) | U43, O46, US3, SC, OP, UFF (ds) | 760 to 38,071 |
| EchoCP | U43, O46, US3, SC | 558 to 11,519 |
| HMC-QU | S30, UVS | 292 (UVS) |
| CardiacNet | SC | 1,550 |
| Unity Imaging Collaborative | US3, AL, U2B | 75,000 (AL); 13,136 train (US3) |
| CACTUS (heart phantom) | O46, OUS, AL | 37,736 |
| TMED (Tufts) | AL | 6,567 |
| MIMIC-IV-ECHO | AL | 525,000 |
| TED project | AL | 98 |
| CETUS2014 (3D) | IM, IX | 45 volumes (IX) |
| STACOM 2011 (3D) | IX | 1,158 volumes |
| MVSeg-3DTEE2023 (3D) | IX | 175 volumes |

Table 6.5. Fetal, obstetric and gynaecological.

| Dataset (aliases) | Mentioned by | Counts as stated |
|---|---|---|
| FETAL_PLANES_DB (Fetal Planes, Fetus12K) | O46, OUS (ds), UFF, URF, UB2, AL, U2B, FG, J; UltraDINO (ds) | 12,400 |
| HC18 (HC, Fetal HC) | U43, O46, OUS, US3, SC, AL, U2B, IX, B97, J; FG "Large Fetal Head Biometry" (Radboud; likely the same, unverified) | 1,334 (999 train) |
| FASS | U43, O46, OUS, US3, SC, FG, AL; UltraDINO (ds) | 1,563 to 1,588 |
| Fast-U-Net | U43, O46, OUS, US3, SC | 406 to 1,414 |
| ACOUSLIC-AI | U43, O46, OUS, US3, SC (external), AL, U2B | 6,620 frames; 300 or 600 cases |
| FH-PS-AOP (fh_ps) | U43, O46, US3 | 4,000 |
| PSFHS | O46, UB2, U2B, IX | 1,358 (O46); 4.7k (IX) |
| JNU-IFM | O46, SC, UFF (ds), U2B; UltraDINO (ds) | 5,202 to 6,224 |
| DFHI | O46 | 3,832 |
| IUGC25 | OUS | 33,466 |
| FUGC | SC | 440 |
| FOCUS (four-chamber fetal heart) | US3, AL, FG, OUS (ds) | 300 |
| FEFT (first-trimester fetal echo) | O46; FG "Echo (1st trimester)" possibly the same (unverified) | 6,720 |
| FPUS23 (fetal phantom) | UFF, AL, U2B, FG | 15,728 (AL); 20,378 (UFF) |
| Ultrasound Fetus Dataset (Kaggle) | O46 | 1,880 |
| African Fetal Standard Plane | U2B; FG "MFUP" (Egypt, Algeria, Uganda, Ghana, Malawi; relation unverified) | – |
| Echogenic (Da Correggio et al. 2023) | U2B | – |
| 3-Vessel View; Echo (2nd trimester); Fetal Planes & Organs; Fetus Head Tumor; NatalIA; NT Scan | FG | NT Scan 1,519 patients |
| BrainBenchmark (fetal brain landmarks) | OUS (ds) | 104 (per EchoCare) |
| PFUS | SC (benchmark) | 13,906 frames; identity not checked |
| MMOTU-2D (OTU_2d) | U43, O46, OUS, US3, SC, UB2, URF (ds), J | 1,469 to 1,489 |
| MMOTU-3D (OTU_3d) | U43, O46, OUS, US3, SC (external) | 170 to 187 |
| Polycystic ovary ultrasound images | AL, U2B | 54 |
| PCOSGen | AL | 4,668 |
| PCOS_US; Auto-PCOS classification (Kaggle) | OP; U2B | 3,841 (OP) |
| ovarianUS (Borna et al. 2025) | OP | 301 |
| Uterus (Tiantian Yang 2023) | OP | 1,973 |
| CDNet (cervix) | SC | 325 |

Table 6.6. Lung, nerve, muscle and musculoskeletal, vascular, prostate, brain, skin and other.

| Dataset (aliases) | Anatomy | Mentioned by | Counts as stated |
|---|---|---|---|
| POCUS (covid19_ultrasound) | lung | O46, UFF (ds), AL, J, UB2 excl. | 211 (AL) |
| COVID-BLUES (BLUES) | lung | O46, UFF, OP, UB2, AL, U2B, J | 362 (AL); 63 patients (UB2) |
| COVIDx-US | lung | OP, AL | 242 (AL) |
| LUSS phantom | lung phantom | U43, O46, OUS, US3, SC | 561 to 564 |
| PPL | lung | SC | 2,756 |
| Lung ultrasound dataset for AI-based lung disease classification; POCUS LUS datasets | lung | AL | 1,062; 10 |
| US Nerve Segmentation (Kaggle 2016; NerveUS, US-Nerve, BP) | brachial plexus | U43, O46, OUS, SC, OP, UFF, AL, IX, SA, J, UB2 excl. | 5,635 train; 11,143 (UFF, OP) |
| Brachial Plexus (Regional-US) | brachial plexus | U43, O46, OUS, SC (benchmark) | 39,025 to 40,788; 7,462 (O46) |
| UBPD (UPBD) | brachial plexus | U43, O46, OUS, US3, SC, OP | 939 to 955 |
| Ultrasound Guided Regional Anesthesia | nerves | AL, U2B | 277 |
| STMUS_NDA (STMUS, MuscleUS) | muscle | U43, O46, OUS, US3, SC, OP, UB2 | 4,355 or 8,153 to 8,169 |
| FALLMUD | lower-leg muscle | U43, O46, OUS, US3, SC, AL, U2B | 810 to 813 |
| LUMINOUS | lumbar multifidus muscle | US3, SC (external), UFF (ds), AL | 341 |
| Mus-V | muscle | OP | 3,114 |
| Leg-3D-US | muscle, 3D | UFF | 115,263 |
| Knee ultrasound dataset (population cohort) | knee | AL, U2B | 7,571 |
| Muscle-tendon junction tracking; 2D-to-3D forearm reconstruction; TUS-REC | arm, forearm, tendon | AL | 1,344; 2,400; 1,200 |
| HFUS (Mendeley) | high-frequency ultrasound (identity unverified) | UFF (ds) | – |
| Porcine spinal cord | animal | O46 | 12,468 |
| CCAUI (Common Carotid Artery, cardiacCCAUS) | carotid | U43, O46, OUS, US3 (external), SC, OP | 1,100 |
| CCA (MI-SegNet carotid) | carotid | US3, SC, AL | 2,143 to 2,307 |
| CUBS (Carotid Ultrasound Boundary Study) | carotid | AL, OP, U2B | 2,176 (AL); 500 (OP) |
| UK Biobank carotid (fields 20222, 20223, 30005) | carotid | AL | 43,195; 83,193 |
| Carotid artery ultrasound and colour Doppler (Kaggle) | carotid | U2B | – |
| Geometric ultrasound localization microscopy | microvessels | AL | – |
| MicroSeg (Micro-US prostate segmentation, MUPSD) | prostate | U43, O46, OUS, US3, OP, AL, U2B | 75 patients (AL); 1,931 to 2,910 |
| MUP | prostate | U43, SC | 2,621 (SC) |
| µ-RegPro (regPro, RegPro, u-RegPro) | prostate | U43, O46, OUS, US3, SC, AL, IM, IX | 108 cases (AL, IX); 4,688 to 6,424 slices |
| mu-Reg | prostate | AL | – |
| Prostate-MRI-US-Biopsy (UCLA) | prostate | OP, AL, IX | 1,151 (AL, IX); 219,484 slices (OP) |
| ProstateTRUS (Baum et al. 2023) | prostate | OP | 5,037 |
| RESECT; BITE; ReMIND; ReMIND2Reg; 3D ultrasound neuroimages | brain | AL; ReMIND also OP | 23; 14; 114 (OP 18,734 frames); 104; 5 |
| CuRIOUS 2018/2019/2022; Learn2Reg LUMIR | brain | IM (CuRIOUS2022), IX | LUMIR 269 volumes |
| Mouse brain tumour (high-resolution) | non-human | AL | 1,856 |
| Dermatologic ultrasound images | skin | AL, U2B | 202 |
| Butterfly (MIT Grand Hack 2018) | 9 point-of-care views | OP (ds), UB2 excl. | 41,076 images, 31 patients |
| ImageCLEF 2015/2016; APOLLO-5; CMB-LCA, CMB-CRC, CMB-MEL; CPTAC-UCEC (TCIA multi-modal) | mixed | IX | – |
| PICMUS; CUBDL (raw signals) | phantom, carotid, mixed | J | – |

Private sets named in these papers and not in the master list: FUS2M (UltraDINO), 3M-US (USFM),
ERUS and PrivateUS (UltraFedFM), West China Hospital sets (URFM, DeblurringMIM), Cedars-Sinai echo
(EchoCLIP, EchoPrime), EchoFM's internal set, Corniche Hospital fetal set (FetalCLIP).

### Inferences
- About 35 of the names are abdominal or liver; only AUL, Open Kidney, AbdomenUS, 105US and
  USAnotAI carry masks, by these sources. RadImageNet-US, SYSU-FLL-CEUS, B-mode-and-CEUS-Liver,
  CLUST and GBUSV are large but unmasked or video-only by these sources.
- Names to merge when cross-checking a census: UDIAT = BUS Dataset B; BLUES = COVID-BLUES; BP and
  NerveUS = Kaggle US Nerve Segmentation; MuscleUS = STMUS_NDA; cardiacCCAUS = CCAUI; MASLD = Byra
  fatty liver; Fetus12K = FETAL_PLANES_DB; OTU = MMOTU.

### Gaps
- U2-Bench Table 7 was parsed from a two-column layout; about 6 of its 40 names were not recovered.
- EchoCare's 138 datasets and USFM's sources are missing from the list (not disclosed).
- Anatomy labels are as the sources give them; some are wrong (105US as pancreas in OPUS, ASUS as
  abdomen in OpenUS, CCAUI as echocardiogram in OpenUS).
