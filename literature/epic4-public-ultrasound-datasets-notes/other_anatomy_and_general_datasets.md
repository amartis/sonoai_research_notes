# Public ultrasound datasets outside the four organ groups: other anatomies, general collections and special data types (census, checks of 2026-11-25)

**Scope.** This census covers public or published ultrasound (US) datasets that are not about breast and thyroid; heart, lung and vessels; fetal, obstetric and gynaecologic; or abdomen and urology. It covers musculoskeletal (MSK) sets, peripheral nerves and regional anaesthesia, brain, eye, skin, dental and oral (with tongue imaging), head and neck, multi-organ collections and benchmarks, vision-language sets, video libraries and teaching atlases, figure sets mined from PubMed Central (PMC), raw radio-frequency (RF) and channel data, simulation and phantom sets, needle and robotics sets, 3D freehand reconstruction and probe tracking, and image quality and enhancement.

**Method.** Web search first, then the primary page of each dataset: landing pages, repository JSON APIs (Zenodo, Hugging Face, Kaggle, Harvard Dataverse, OSF, figshare), READMEs and papers. No dataset, archive, video or image was downloaded or opened. Checks ran on 2026-11-25. After an interruption, the last six checks ran on 2026-11-26; field 14 says which. Roboflow Universe was not searched: it is out of scope under DEC-081 and DEC-096 (the project's decisions on the epic 2 Roboflow scraper). No dataset below was found to exist only on Roboflow.

**Priority flag.** "HIGH PRIORITY" marks abdomen or liver content inside a collection. It serves epic 1 (upper-abdomen anatomy segmentation) and epic 3 (spotting liver diseases). For scale: the project's training set today, dataset version 261023, holds about 20k images.

**Access levels (field 8):** open direct link; free account; click-through terms; data use agreement (DUA) with manual approval; credentialed (training and approval); on request by email; closed or dead link.

**Automation tiers (field 10):** A = scriptable with no login; B = scriptable with a token or cookie the user supplies once; C = needs a manual step by the user (form, approval, captcha, click-through); D = not automatable, or barred by the terms. A tier is inferred from the host's access model and the stated terms. No download was tried (task rule), so no tier is a tested fact. "A?" and "C?" mean the inference is weak.

Table 1. Census summary, one row per dataset or resource (86 rows). "?" = not found. Size is in GB (10^9 bytes) as stated by the host or summed from its file list.

| Dataset (year) | Anatomy and content | Images or videos (n) | Size (GB) | Host | Access level | Licence | Tier |
|---|---|---|---|---|---|---|---|
| **Musculoskeletal** | | | | | | | |
| FALLMUD (2020) | Lower-leg muscles; fascicle and aponeurosis masks | 812 images (813 in OpenUS) | ? | Institutional site (CEA, France) | Open direct link (per a survey; page not reachable) | ? | A? |
| Transverse muscle CSA, "STMUS_NDA" (2021) | Biceps brachii, tibialis anterior, gastrocnemius medialis; neuromuscular disease; CSA masks | 3,917 images, 1,283 subjects (4,355 in OpenUS) | ? | Mendeley Data | Open direct link | CC BY 4.0 | A |
| FSHD Heckmatt grading (2025) | Several muscles in FSHD; masks, Heckmatt grades | ? | ? | Mendeley Data | Open direct link | CC BY 4.0 | A |
| DeepACSA (2022) | Rectus femoris, vastus lateralis, gastrocnemii; panoramic CSA | 1,772 images, 153 participants (preprint) | ? | Mendeley Data | Open direct link | CC BY 4.0 | A |
| DL_Track_US examples (2023) | Lower-limb muscle architecture; example and test data, trained models | ? | 1.06 | Zenodo (newer copy on OSF) | Open direct link | CC BY 4.0 | A |
| deepMTJ (2021) | Muscle-tendon junction, gastrocnemii | 1,344 images (survey); 161 participants (UMUD) | ? | OSF | On request (per survey) | Not named | C? |
| UMUD index (2026) | Index of 14 MSK datasets | 76,124 images and/or 2,674 videos, 1,901 participants (index totals) | n/a | Streamlit app, GitHub | Open (metadata only) | Code GPL-3.0; datasets keep their own | n/a |
| LUMINOUS (2020) | Lumbar multifidus at L5; masks | 341 images (survey); 109 participants (UMUD) | ? | data.sonography.ai | Unclear: site timed out | ? | ? |
| Knee US, JoCoHS cohort (2023; v6 2024) | Knee, 7 views per side | 12,063 images (7,571 in survey) | 1.41 | Harvard Dataverse | Open direct link | CC0 1.0 | A |
| Hip dysplasia US, TOBB ETU Hospital (2024) | Infant hip; masks of 5 regions | ? | ? | Mendeley Data | Written consent of the publisher | CC BY-NC-ND 4.0, research only | C |
| open-hip-dysplasia (Retuve, 2025) | Infant hip, US and X-ray | 172 US images | ? | GitHub, Zenodo | Open direct link | "Creative Commons" (version not named) | A |
| UltraBones100k (2025) | Ex vivo lower-limb bone surface; tracked US with CT | about 100,000 frames, 14 limbs | 41.6 | Hugging Face | Open direct link | CC BY 4.0 | A |
| Spine US-CT registration database (2021) | Lumbar vertebrae (simulated US); canine and lamb vertebra phantoms | 3 sets | 0.149 | Zenodo | Open direct link | CC BY 4.0 | A |
| Paired robotic and handheld lumbar spine US (2025) | Lumbar spine L1-L5; tracked probe; CT | 63 volunteers | ? | ? | ? | CC BY 4.0 (per a later paper) | ? |
| Porcine spinal cord US (under review) | Pig spinal cord before and after injury; boxes, masks | 10,223 images, 25 pigs | ? | Google Drive (via GitHub) | Open link | None stated | A |
| Biceps M-mode US with EMG (2017) | Biceps brachii, M-mode clips | 10 participants | ? | Zenodo | Open direct link | CC BY 4.0 | A |
| **Peripheral nerves and regional anaesthesia** | | | | | | | |
| Kaggle Ultrasound Nerve Segmentation (2016) | Brachial plexus (neck); nerve masks, test masks hidden | 11,143 images (5,635 train, 5,508 test), 47 patients | ? | Kaggle competition | Free account and rules acceptance | Competition rules (not read) | C |
| Regional-US brachial plexus videos (2024) | Brachial plexus; boxes, contour masks, needle labels | 227 videos (40,788 frames in OpenUS) | ? | GitHub | DUA, non-commercial | Non-commercial DUA | C |
| UBPD (2020) | Brachial plexus; nerve, artery, vein, muscle masks | 1,055 images, 101 patients | ? | Institutional site | Closed or dead link | ? | D |
| Femoral nerve block set (2019) | Femoral nerve region | 562 images | ? | None found | "Shared" per paper; no route | ? | D |
| **Brain** | | | | | | | |
| RESECT (2017) | Low-grade glioma surgery; pre-op MRI, 3D iUS, landmarks | 23 patients | 3.34 | Sigma2 NIRD archive | Open (login not stated) | CC BY 4.0 | A? |
| RESECT-SEG (2022; 2024) | Labels on RESECT iUS: tumour, cavity, sulci, falx | 23 patients | ? | OSF | Open | None set on OSF | A |
| CuRIOUS 2018, 2019, 2022 challenges | Registration and segmentation on RESECT | ? | ? | Grand Challenge | ? (page refused automated fetch) | ? | C? |
| BITE (2012) | Brain tumour; pre/post MR, 2D and 3D iUS, landmarks | 14 patients | about 7.9 | Institutional site (MNI) | Open direct link | None stated | A |
| ReMIND (2023 data; 2024 paper) | Brain resection; MRI, iMRI, 3D iUS, segmentations | 114 patients; 85,733 DICOM images | 43.73 | TCIA | Open (TCIA usage policy) | CC BY 4.0 | A |
| ReMIND2Reg (2024) | MR-to-iUS registration subset of ReMIND | 104 patients | 3.20 | Zenodo | Open direct link | CC BY 4.0 | A |
| BraTioUS (2025) | Glioma 2D iUS, tumour masks; 6 hospitals, 5 countries | 1,669 images, 142 patients | 0.243 | Zenodo | Open direct link | CC BY 4.0 | A |
| Neonatal 3D transfontanellar US (2025; v2 2026) | Neonatal brain 3D US volumes | 4 volumes in v2 (5 in survey) | 0.040 | Zenodo | Open direct link | CC BY 4.0 | A |
| Mouse GL261 brain tumour US (2025) | Mouse glioblastoma; masks | 1,856 images | ? | ? | ? | ? | ? |
| **Eye** | | | | | | | |
| Oculo (2026) | Ocular B-scan; multi-label abnormalities | 1,630 images, 1,242 patients | 0.358 | Hugging Face | Open direct link | CC BY-SA 4.0 | A |
| ERDES (2025; files 2026) | Ocular B-scan clips; retinal detachment, macula status | 5,381 clips | 1.94 | Hugging Face, Zenodo | Open direct link | CC BY 4.0 | A |
| Ophthalmic US report set (2024) | Eye images with Chinese reports and blood-flow values | 4,858 images, 2,417 patients | ? | ? | ? | ? | ? |
| **Skin** | | | | | | | |
| Dermatologic US images (Kaggle, 2022) | Skin lesions; B-mode and colour Doppler; diagnosis | 202 images (survey) | 0.015 | Kaggle | Free account (API token) | "Unknown" | B |
| HFUS skin layers in AD and psoriasis (2021) | Skin at 75 MHz; epidermis and SLEB masks | 380 images, 380 patients | ? | Mendeley Data | Open direct link | CC BY 4.0 | A |
| HFUS skin layer expert masks (2025; v2 2026) | Skin at 20 MHz in AD; entry echo, SLEB, dermis masks | ? | ? | Mendeley Data | Open direct link | CC BY 4.0 | A |
| HFUS atopic dermatitis staging (2025) | AD severity (IGA scale) | 78 patients | ? | Mendeley Data | Open (not checked) | ? | A? |
| HFUS facial skin image quality (2022) | Facial skin; quality labels | 17,425 images, 44 patients | ? | ? | "Shared" per paper; no route | ? | ? |
| **Dental, oral and tongue** | | | | | | | |
| UltraSuite, with the TaL corpus (2018-2021) | Tongue US with audio (TaL adds lip video); speech | 7 sets: 152 children, 82 adults | ? | Institutional server (rsync) | Open | CC BY-NC 4.0 | A |
| **Head and neck** | | | | | | | |
| LymphUs (2023; 2026) | Cervical lymph nodes in papillary thyroid cancer; masks, features | 338 patients, 2 centres | ? | Institutional site (qamebi.com) | Open direct link | CC BY-NC 4.0 | A |
| **Multi-organ collections and benchmarks** | | | | | | | |
| RadImageNet, US part (2022). HIGH PRIORITY | CT, MRI, US; US organs include liver, gallbladder, pancreas, spleen, kidney | about 389,884 US frames (secondary); liver 78,535 | ? | Institutional site | On request | ? | C |
| Butterfly MIT GrandHack 2018. HIGH PRIORITY | 9 classes, incl. Morison's pouch, bladder, IVC | 41,076 images, 31 patients | ? | GitHub releases | Open link | Hackathon use only; no re-publishing | D (terms) |
| AbdomenUS, "US simulation & segmentation" (2019). HIGH PRIORITY | Abdomen: real and CT-simulated scans; liver, kidney, gallbladder, spleen, vessel labels | 617 real, 926 simulated | 2.10 | Kaggle | Free account (API token) | "Data files © Original Authors" | B |
| AHU database (2025). HIGH PRIORITY | 13 anomaly types; heart, thyroid, abdomen, kidney, lung; from internet videos | 1,833 items (videos and images) | 34.13 | figshare | Open direct link | CC BY 4.0 | A |
| USAnotAI (2019). HIGH PRIORITY | Abdominal organ classification | 366 images (OpenUS) | ? | GitHub | Open | None stated | A |
| UUSIC 2025 and UUSIVC 2026 challenges. HIGH PRIORITY | Breast, thyroid, liver (fatty liver), kidney, fetal head, heart, appendix | ? | ? | Codabench | Challenge registration | Not stated | C |
| US-43d (UltraSam, 2024) | 43 public datasets | over 280,000 masks | n/a | GitHub (converters) | Links only | None for the collection | n/a |
| OpenUS (2025) | 42 public datasets, plus 3 downstream | over 308K images | n/a | GitHub | Links only | Repository CC BY-NC 4.0 | n/a |
| OpenUS-46 (USF-MAE, 2025) | 46 public datasets | about 370,000 images | n/a | GitHub | Links only | Sources keep their own | n/a |
| SonoCorpus (SonoBase, 2026) | 53 public datasets; manifest, split indices, dedup hashes | 456,963 images, 1,626,085 masks | n/a | GitHub, Zenodo manifest | Links only | Manifest CC BY 4.0 | n/a |
| OPUS corpus and UltraBench (US-JEPA, 2026) | 50 public datasets (pretraining), 10 benchmark sets | 5,123,697 frames | n/a | GitHub | Links only | ? | n/a |
| US30K (SAMUS, 2023) | 7 public sets (breast, thyroid, heart) | about 30K images, 69K masks | ? | Google Drive | Open link | None stated | A |
| SA-Med2D-20M, US part (2023) | 10 modalities | 2,968 US images of 4.6M | 352.8 (whole set) | Hugging Face | Open direct link | CC BY-NC-SA 4.0 | A |
| EchoAtlas (EchoCare, 2025) | 9 body regions, 52 organs | 4.5M images | ? | ? | No route found | ? | ? |
| **Vision-language** | | | | | | | |
| U2-Bench (2025) | 15 anatomical regions; 8 tasks incl. report generation | 7,241 cases | 18.9 | Hugging Face | Open direct link | CC BY-NC-ND 4.0 | A |
| Chinese US report sets: breast, thyroid, liver (2024). HIGH PRIORITY | Image-report pairs, 2 images per report | 3,521 + 2,474 + 1,395 patients | ? | Google Drive (via GitHub) | Open link | None stated | A |
| ReMUD (2025) | US question answering (breast, liver, thyroid named) | over 45,000 items | ? | Not released | Closed (pending) | ? | D |
| **Figure sets mined from PMC** | | | | | | | |
| ROCOv2 (2024) | PMC figures with captions and UMLS concepts | 11,429 US of 79,789 images | ? | Zenodo | Open direct link | Per image: CC BY or CC BY-NC | A |
| PMC-OA (2023) | PMC subfigure-caption pairs | 1.65M pairs (US share ?) | 37.6 | Hugging Face | Open direct link | Not stated | A |
| PMC-15M (2023) | PMC figure-caption pairs | 15,282,336 pairs (US share ?) | n/a | Scripts only | Rebuild from PMC | Per article | n/a |
| BIOMEDICA (2025) | PMC image-caption archive | 24,076,288 images (US share ?) | ? | Hugging Face (gated) | Click-through terms | Per article, 3 groups | C |
| MedTrinity-25M (2024) | 25M images, 10 modalities, over 90 sources | US share ? | ? | ? | ? | ? | ? |
| **Video libraries and teaching atlases** | | | | | | | |
| The POCUS Atlas. HIGH PRIORITY content | Teaching images and videos; biliary, aorta, GI, renal, MSK, ocular, nerve blocks | ? | n/a | Website | View only; no bulk route | CC BY-NC 4.0 | D |
| UltrasoundCases.info. HIGH PRIORITY content | Teaching cases in 10 categories, incl. abdomen | ? | n/a | Website (SonoSkills) | Permission needed | All rights reserved | D |
| Radiopaedia US cases | Teaching cases | ? | n/a | Website | Terms bar ML datasets and bulk download (secondary) | CC BY-NC-SA 3.0 as modified by terms | D |
| **Raw RF and channel data** | | | | | | | |
| PICMUS (2016) | Plane-wave simulation, phantom, in vivo carotid | a few acquisitions | ? | CREATIS site; mirrors on Zenodo (USTB) and Hugging Face (zea) | Open | Free to use with citation (secondary) | A |
| CUBDL (2020-2021) | Plane-wave and focused channel data, phantoms and in vivo | ? | ? | IEEE DataPort | DUA with manual approval | CC BY plus release agreement | C |
| USTB datasets (Zenodo record 2026) | 51 channel and beamformed sets: phantoms, carotid, heart, Field II, SWE | 53 files | 28.97 | Zenodo | Open direct link | CC BY 4.0 | A |
| Open-H-RF (2026) | Raw channel data from 39 institutions; in vivo, phantom, simulated | 19,332 acquisitions | about 40,000 | Hugging Face | Open direct link | CC BY 4.0 | A |
| zea mirrors (zeahub, 2026) | RF and IQ sets in zea format (PICMUS, phantoms, simulations, carotid, us4us) | 19 repositories | ? | Hugging Face | Open direct link | Mixed: CC BY 4.0, "other", CC BY-NC-SA 4.0 | A |
| PALA (2020) | ULM IQ data: rat brain, rat kidney, mouse tumour, in silico | 12 files | 55.65 | Zenodo | Open, with a "request on data" note | CC BY 4.0 | A |
| ULTRA-SR (2022) | Simulated microvascular flow for ULM | ? | ? | Zenodo | Open | ? | A |
| ULMShare (2026) | Mouse whole-brain transcranial ULM raw data | 99 acquisitions, 61 mice | about 30,000 | FRDR, GitHub | Open (per paper) | Not stated for the data | ? |
| Plane-wave 75-angle phantom raw data (2023) | Breast and calibration phantoms | 2 archives | 8.53 | Zenodo | Open direct link | Not stated | A |
| 3D US matrix imaging RF (2023) | Pork tissue, head phantom | 5 files | about 35 | Zenodo | Open direct link | CC BY 4.0 | A |
| Vasculature chips for ULM (2025) | Phantom chip; beamformed IQ | 200 files of 400 frames | about 39.5 | Zenodo | Open direct link | CC BY 4.0 | A |
| USCT phantom dataset (2026) | US tomography of 3 sound-speed phantoms | 3 phantoms | 38.13 | Zenodo | Open direct link | CC BY 4.0 | A |
| **Simulation, phantom and synthetic** | | | | | | | |
| Lung COVID phantom, "LUS_model" (2024) | Lung phantom videos and labelled frames | ? (564 frames in OpenUS) | 0.23 | Leeds data repository | Open direct link | CC BY 4.0 | A |
| ArteryPhantom-42k (2026) | Vessel phantom in beef; probe alignment classes | 42,266 frames (6,612 labelled) | 5.47 | Zenodo | Open direct link | CC BY 4.0 | A |
| Thoracolumbar fascia phantom ground truth (2025) | Gel-pad phantoms; deformation, shear | ? | 1.25 | Zenodo | Open direct link | CC BY 4.0 | A |
| **Needle guidance and robotics** | | | | | | | |
| Motion-informed needle segmentation (2024) | Needle videos of the femoral area | 17 videos (secondary) | ? | Not found | ? | ? | ? |
| Vicomtech robotic phantom sequences (2016) | Phantoms; robot arm, optical tracking, force control | ? | ? | Vicomtech site | "Publicly available" (secondary) | ? | ? |
| ForceU-VLA and US-VLA (2026 preprints) | Robotic scanning demonstrations; US-VLA is abdominal | 450 and 320 trajectories | ? | ? | Release not stated | ? | ? |
| **3D freehand reconstruction and probe tracking** | | | | | | | |
| TUS-REC2024 (2024) | Forearms; optically tracked freehand frames | 1,200 train scans, 50 subjects | 43.4 (train part 1) | Zenodo | Open direct link | CC BY-NC-SA 4.0 | A |
| TUS-REC2025 (2025) | Forearms, with rotation and tilt; tracked | 170 scans of 85 volunteers (100 in train) | ? | Zenodo (restricted files) | Restricted, request | CC BY-NC-SA 4.0; challenge use, no commercial use | C |
| **Image quality and enhancement** | | | | | | | |
| USenhance 2023 challenge. HIGH PRIORITY | Low- and high-quality pairs: thyroid, carotid, liver, breast, kidney | 3,000 images (1,500 pairs), 109 patients (2,464 in survey) | ? | Grand Challenge | Registration and signed rules by email | Challenge use only | C |
| USenhance2023_Aligned (derivative) | Aligned pairs at 64 × 64 | ? | ? | Hugging Face | Open direct link | "other" (academic use) | A |

Footnote to Table 1. AD = atopic dermatitis. CSA = cross-sectional area. CT = computed tomography. DUA = data use agreement. EMG = electromyography. FRDR = Federated Research Data Repository (Canada). FSHD = facioscapulohumeral muscular dystrophy. GI = gastrointestinal. HFUS = high-frequency ultrasound. IGA = investigator's global assessment. iMRI = intraoperative MRI. iUS = intraoperative ultrasound. IQ = in-phase and quadrature (demodulated RF) data. IVC = inferior vena cava. ML = machine learning. MNI = Montreal Neurological Institute. NIRD = the national research data archive run by Sigma2 (Norway). PMC = PubMed Central. RF = radio-frequency. SLEB = subepidermal low-echogenic band. SWE = shear-wave elastography. TCIA = The Cancer Imaging Archive. ULM = ultrasound localization microscopy. UMLS = Unified Medical Language System. UMUD = Universal Musculoskeletal Ultrasonography Database. USCT = ultrasound computed tomography. "Survey" = the npj Digital Medicine survey of public US datasets (Alsharid et al. 2025, [doi:10.1038/s41746-025-02162-4](https://doi.org/10.1038/s41746-025-02162-4)). Licence abbreviations: CC = Creative Commons; BY = attribution; NC = non-commercial; SA = share-alike; ND = no derivatives.

## 1. Which datasets exist, with the 14 fields for each

### Takeaway
The census holds 86 rows: 76 datasets or challenge sets, 7 link-list collections or indexes, and 3 teaching atlases. About half (45 rows) look scriptable without a login (tier A, mostly Zenodo, Hugging Face, Mendeley Data and Harvard Dataverse). Many 2024 to 2026 releases are open and well documented, with md5 checksums: BraTioUS, ReMIND2Reg, ERDES, Oculo, UltraBones100k, open-hip-dysplasia, LymphUs, Open-H-RF, USTB on Zenodo, TUS-REC2024. Abdomen or liver content in this scope sits mainly in RadImageNet (on request; about 259k abdominal frames per a secondary table), AbdomenUS, AHU, USenhance 2023, the Chinese report sets, the UUSIC challenges and two teaching atlases. Butterfly's terms bar its use.

### Cited Findings

#### Musculoskeletal

##### FALLMUD
- **1 Name, year, paper:** FALLMUD, "FAscicle Lower Leg Muscle Ultrasound Dataset". It is presented with the AW-Net paper ("AW-Net: Automatic muscle structure analysis on B-mode ultrasound images for injury prevention"); I found no DOI. Year 2020 in the survey — [CEA page, search snippet](https://kalisteo.cea.fr/?p=3568); [survey Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/)
- **2-3 Content, data type:** Lower-leg muscles; UMUD lists gastrocnemius medialis and soleus; 2D B-mode, static, longitudinal — [UMUD paper Table 1](https://jyx.jyu.fi/bitstreams/ee8f740d-8d88-45e1-a942-b40a87cfdd18/download)
- **4-5 Size, labels:** 812 images ([CEA snippet](https://kalisteo.cea.fr/?p=3568), [survey](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/)); 813 in [OpenUS README](https://raw.githubusercontent.com/XZheng0427/OpenUS/main/README.md). One fascicle mask and one aponeurosis mask per image. UMUD lists "FALLMUD, Cunningham et al. 2017" with 8 participants, which seems to describe one source part. GB unknown.
- **6 Source:** Merges two earlier sets (Cunningham et al.; Cronin) with added annotations; CEA (France); devices unknown — [CEA snippet](https://kalisteo.cea.fr/?p=3568)
- **7-8 Where, access:** [kalisteo.cea.fr/index.php/fallmud](https://kalisteo.cea.fr/index.php/fallmud/); institutional site; one zip; no version, DOI or checksum found. Open per the survey; my fetch failed with a TLS certificate error.
- **9-10 Licence, tier:** Unknown; A? (if the zip link is direct).
- **11-13 Overlaps, burned-in text, used by:** Contains the Cunningham and Cronin sets. Burned-in text unknown. Used in [US-43d](https://github.com/CAMMA-public/UltraSam), [OpenUS](https://raw.githubusercontent.com/XZheng0427/OpenUS/main/README.md) and [OpenUS-46](https://github.com/Yusufii9/USF-MAE).
- **14 Verification:** Unverified at the landing page (TLS error on 2026-11-25); facts from a search snippet of the CEA page and from collection READMEs.

##### Transverse muscle CSA set of Marzola et al. ("STMUS_NDA" in collections)
- **1 Name, year, paper:** "DATASET for 'Deep learning segmentation of transverse musculoskeletal ultrasound images for neuromuscular disease assessment'", v1, 2021-07-06; paper in Computers in Biology and Medicine, [doi:10.1016/j.compbiomed.2021.104623](https://doi.org/10.1016/j.compbiomed.2021.104623) — [Mendeley record](https://data.mendeley.com/datasets/3jykz7wz8d/1)
- **2-3 Content, data type:** Biceps brachii, tibialis anterior, gastrocnemius medialis; healthy versus abnormal muscle; 2D B-mode transverse — [Mendeley record](https://data.mendeley.com/datasets/3jykz7wz8d/1)
- **4-5 Size, labels:** 3,917 images of 1,283 subjects (mean age 50 ± 21 years, 729 male); CSA masks; record says it holds "the entire dataset and code". OpenUS lists 4,355 images; UMUD lists 1,238 participants. GB unknown.
- **6 Source:** Authors from Radboudumc and Politecnico di Torino (institutions shown on the same group's 2025 record, [Mendeley](https://data.mendeley.com/datasets/yzg86vb895/1)); devices not stated.
- **7-8 Where, access:** Mendeley Data, DOI 10.17632/3jykz7wz8d.1; open; checksums not shown.
- **9-10 Licence, tier:** CC BY 4.0; results must cite the article. The Mendeley site footer reserves rights "for text and data mining, AI training and similar technologies", while open content falls under CC terms. Tier A.
- **11-13:** Same group as the FSHD Heckmatt set below (patient overlap unknown). Burned-in text unknown. Used in US-43d, OpenUS, OpenUS-46.
- **14:** Verified at [Mendeley](https://data.mendeley.com/datasets/3jykz7wz8d/1) on 2026-11-25.

##### FSHD Heckmatt grading set
- **1:** "Machine learning-driven Heckmatt grading in facioscapulohumeral muscular dystrophy: A novel pathway for musculoskeletal ultrasound analysis", Marzola, van Alfen, Doorduin, Meiburger; v1, 2025-02-11; DOI 10.17632/yzg86vb895.1 — [Mendeley](https://data.mendeley.com/datasets/yzg86vb895/1)
- **2-5:** MSK US images of "various muscle groups" in FSHD, with segmentation masks, model configurations and subject information; counts not stated; GB unknown. A companion record holds model weights only ([Mendeley 7bcsvh6nfv](https://data.mendeley.com/datasets/7bcsvh6nfv/1), per search).
- **6:** Radboudumc; Politecnico di Torino; device not stated.
- **7-10:** Mendeley Data; open; CC BY 4.0, with the same site footer on AI training; code at the [GitHub repository](https://github.com/frmrz/Machine-learning-driven-Heckmatt-grading-in-facioscapulohumeral-muscular-dystrophy) named on the record. Tier A.
- **11-13:** Possible patient overlap with the 2021 set of the same group (inference). Burned-in text unknown. Large-scale use unknown.
- **14:** Verified at [Mendeley](https://data.mendeley.com/datasets/yzg86vb895/1) on 2026-11-26.

##### DeepACSA
- **1:** DeepACSA, v1, 2022-04-20, DOI 10.17632/cjztczmd4w.1 ([Mendeley](https://data.mendeley.com/datasets/cjztczmd4w)); paper Ritsche et al., Med Sci Sports Exerc 2022 ([PubMed 35941517](https://pubmed.ncbi.nlm.nih.gov/35941517/)).
- **2-5:** Panoramic transverse images of rectus femoris, vastus lateralis, gastrocnemius medialis and lateralis; training and test images plus trained networks; CSA labels. The preprint reports 1,772 images from 153 participants ([medRxiv](https://www.medrxiv.org/content/10.1101/2021.12.27.21268258.full.pdf), search snippet). GB unknown.
- **6:** University of Basel; devices unknown.
- **7-10:** Mendeley Data; open; CC BY 4.0; tier A.
- **11-13:** Probably among UMUD's "LabTrainData" re-offered sets (UMUD cites three published training sets; which ones was not confirmed). Used in large-scale papers: unknown.
- **14:** Verified at [Mendeley](https://data.mendeley.com/datasets/cjztczmd4w) on 2026-11-25 (counts unverified).

##### DL_Track_US examples
- **1:** "DL_Track_US - Examples", Ritsche, Seynnes, Cronin; v1.2, 2023-04-06; DOI 10.5281/zenodo.7866598 (concept 10.5281/zenodo.7318088) — [Zenodo](https://zenodo.org/api/records/7866598)
- **2-5:** Longitudinal images of lower-limb muscles; pre-trained aponeurosis and fascicle networks, example and test data; one 7z archive of 1.06 GB with md5.
- **6:** University of Basel, Norwegian School of Sport Sciences, University of Jyväskylä.
- **7-10:** Zenodo, open, CC BY 4.0, md5 given; the record says newer files moved to [OSF 7mjsc](https://osf.io/7mjsc/). Tier A.
- **11-13:** Two copies (Zenodo and OSF). UMUD lists DL_Track_US. Large-scale use unknown.
- **14:** Verified at [Zenodo API](https://zenodo.org/api/records/7866598) on 2026-11-25.

##### deepMTJ (muscle-tendon junction tracking)
- **1-5:** OSF project "deepMTJ, Muscle-Tendon Junction Tracking in Ultrasound Images", created 2021-11-25, public ([OSF API](https://api.osf.io/v2/nodes/wgy4d/)). The survey lists 1,344 images, "available on request" ([survey](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/)). UMUD lists Leitner et al. 2021, 161 participants, gastrocnemius medialis and lateralis, longitudinal static images ([UMUD](https://jyx.jyu.fi/bitstreams/ee8f740d-8d88-45e1-a942-b40a87cfdd18/download)). Labels: junction landmarks (tags "anatomical landmark", "muscle tendon junction").
- **6-10:** Institution and devices not checked. Licence type not named on the OSF record. Tier C? (on request).
- **11-14:** Overlaps unknown. Verified at the [OSF API](https://api.osf.io/v2/nodes/wgy4d/) on 2026-11-25 for the record only; file access not checked.

##### UMUD index and the other MSK datasets it lists
- **1:** UMUD, Universal Musculoskeletal Ultrasonography Database; Ritsche et al., BMC Medical Imaging 2026;26:139, [doi:10.1186/s12880-026-02170-0](https://doi.org/10.1186/s12880-026-02170-0); web app [universalmuscledatabase.streamlit.app](https://universalmuscledatabase.streamlit.app/); code [github.com/PaulRitsche/UMUD](https://github.com/PaulRitsche/UMUD) under GPL-3.0 — [UMUD PDF](https://jyx.jyu.fi/bitstreams/ee8f740d-8d88-45e1-a942-b40a87cfdd18/download)
- **2-5:** A metadata index of public MSK datasets hosted on OSF and Zenodo; v0.1.0 lists 14 datasets. The abstract gives 76,124 images and/or 2,674 videos from 1,901 participants ([search snippet of the abstract](https://eprints.glos.ac.uk/15848/)). It also offers benchmark sets: MultExpData (35 muscle architecture and 30 panoramic CSA images analysed by six experts), ExpDrawnData (250 images with fascicles drawn by an expert, vastus lateralis of 40 young and 85 older adults) and three labelled training sets from published papers.
- **Other datasets in UMUD Table 1 (name, paper, year, participants, data type):** BicepsFem3DUS (Andrews et al., 2024, 12, volumes); GasFasTrack (Drazan et al., 2019, 5, video); HEELRAISE (Niemi, 2017, 13, video); Leg3dUS (Duque et al., 2024, 44, volumes); NeuAge_OLD (Sarto et al., 2024, 88, panoramic and static images); NeuAge_YOUNG (Sarto et al., 2024, 42, images); SimpleMuscleArchitectureAnalysis (Seynnes and Cronin, 2019, 15, images); UltraTimTrack (van der Zee et al., 2024, 8, video). Their hosts, sizes and licences were not checked — [UMUD Table 1](https://jyx.jyu.fi/bitstreams/ee8f740d-8d88-45e1-a942-b40a87cfdd18/download)
- **14:** Table 1 verified in the UMUD paper PDF on 2026-11-25; the live app was not opened.

##### LUMINOUS
- **1-5:** LUMINOUS database, Belasso et al., BMC Musculoskelet Disord 2020;21:703, [doi:10.1186/s12891-020-03679-3](https://doi.org/10.1186/s12891-020-03679-3). Lumbar multifidus at L5, prone and standing, left and right, with binary masks; 109 young athletes from Concordia University varsity teams ([PMC7585198, search snippet](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7585198/)). The survey lists 341 images.
- **6-10:** Host data.sonography.ai per the paper; my fetch timed out on 2026-11-25. Licence and access unknown; tier unknown.
- **11-13:** Indexed by UMUD as "LuminousMultifidus". Large-scale use unknown.
- **14:** Unverified (paper facts from a search snippet; host unreachable).

##### Knee ultrasound, Johnston County Health Study (JoCoHS)
- **1:** "Development of an AI/ML-ready knee ultrasound dataset in a population-based cohort", Amanda Nelson (UNC Chapel Hill); first published 2023-04-14, version 6 released 2024-10-30; [doi:10.7910/DVN/SKP9IB](https://doi.org/10.7910/DVN/SKP9IB). Related protocol paper: Yerich et al., ACR Open Rheumatology 2020, [doi:10.1002/acr2.11159](https://doi.org/10.1002/acr2.11159) — [Dataverse API](https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/SKP9IB)
- **2-5:** Knee, seven views per side, lossless PNG, one image per subject per archive. Archive counts sum to 12,063 images (right 6,034, left 6,029); 835 to 867 images per archive, so roughly 850 participants (my inference). The survey lists 7,571. Labels: views; a subject table and an image reference table. 25 files, 1.41 GB.
- **6:** UNC Chapel Hill (USA); device not stated; funded by NIAMS grant R01AR077060.
- **7-10:** Harvard Dataverse; files unrestricted; md5 for every file; CC0 1.0. Tier A.
- **11-13:** No overlap known. Burned-in text unknown. Large-scale use unknown.
- **14:** Verified at the [Dataverse API](https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/SKP9IB) on 2026-11-25.

##### Hip dysplasia set of TOBB ETU Hospital
- **1:** "Deep Learning for Evaluation of Ultrasound Images in Developmental Hip Dysplasia", Onay, Yilmaz, Colak; v1, 2024-12-02; DOI 10.17632/rg4g629stx.1 — [Mendeley](https://data.mendeley.com/datasets/rg4g629stx/1)
- **2-5:** Infant hip; masks of ilium, ischium, labrum, femoral head and acetabular roof made in CVAT; COCO and segmentation-mask formats, partly converted to YOLO; JPEG images anonymised and cropped to 640 × 640. Counts and GB not stated.
- **6:** TOBB ETU Hospital; Philips EPIQ 5G.
- **7-10:** Mendeley Data. Licence CC BY-NC-ND 4.0, and "can be used only for scientific research purposes with the written consent of the publisher"; site footer reserves AI-training rights. Tier C (written consent).
- **11-13:** Overlaps unknown. Burned-in text: images cropped after anonymisation. Large-scale use unknown.
- **14:** Verified at [Mendeley](https://data.mendeley.com/datasets/rg4g629stx/1) on 2026-11-25.

##### open-hip-dysplasia (Retuve)
- **1:** Released with "Retuve: Automated Multi-Modality Analysis of Hip Dysplasia with Open Source AI" ([arXiv 2504.06422](https://arxiv.org/html/2504.06422v2)); [GitHub radoss-org/open-hip-dysplasia](https://github.com/radoss-org/open-hip-dysplasia); [Zenodo doi:10.5281/zenodo.15086603](https://doi.org/10.5281/zenodo.15086603).
- **2-5:** "172 2D ultrasounds from Radiopedia and Hong Kong Polytechnic University", plus X-ray from the MTDDH dataset (2,156 initial, 1,878 used after filtering in the paper); expert annotations; label types per modality not specified; GB unknown.
- **6:** Dataset authors at University of Alberta, NHS Lothian and Insight Softmax Consulting; devices not stated.
- **7-10:** GitHub and Zenodo; open. Licence: "Creative Commons licensed", version not named. Part of the US images come from Radiopaedia, whose own terms apply to them (see section 3). Tier A.
- **11-13:** Overlaps Radiopaedia cases. Large-scale use unknown.
- **14:** Verified at the [arXiv paper](https://arxiv.org/html/2504.06422v2) on 2026-11-25; the Zenodo record was not opened.

##### UltraBones100k
- **1:** UltraBones100k, Wu et al., Computers in Biology and Medicine 2025 ([PubMed 40472504](https://pubmed.ncbi.nlm.nih.gov/40472504/); [arXiv 2502.03783](https://arxiv.org/abs/2502.03783v3)).
- **2-5:** About 100,000 ex vivo B-mode frames from 14 cadaveric lower limbs; bone-surface labels of tibia, fibula and foot; "Labels" (visible surface) and "Labels_full" (adds the surface in acoustic shadow). Labels come from tracked CT bone models laid over tracked US images (search snippet of the paper). 14 zip files, 41.6 GB.
- **6:** ETH Zurich and University Hospital Balgrist (Switzerland).
- **7-10:** [Hugging Face luohwu/UltraBones100k](https://huggingface.co/api/datasets/luohwu/UltraBones100k), not gated, CC BY 4.0, created 2026-06-27; also [GitHub](https://github.com/luohwu/UltraBones100k). Tier A.
- **11-13:** No overlap known. Large-scale use unknown.
- **14:** Verified at the [Hugging Face API](https://huggingface.co/api/datasets/luohwu/UltraBones100k) on 2026-11-25.

##### Spine US-CT registration database (Masoumi et al.)
- **1:** "Multimodal 3D ultrasound and CT in image-guided spinal surgery: public database and new registration algorithms", Masoumi, Belasso, Ahmad, Benali, Xiao, Rivaz; v3, 2021-03-08; DOI 10.5281/zenodo.4813508 (concept 10.5281/zenodo.2483401) — [Zenodo API](https://zenodo.org/api/records/4813508)
- **2-5:** Three sets: three human lumbar vertebrae patients with US simulated from CT; a phantom of post-mortem canine cervical and thoracic vertebrae; a phantom of lamb lumbar vertebrae. 21 landmark pairs per phantom set; fiducial silver standard. Data.zip, 148.6 MB, md5 given.
- **7-10:** Zenodo, open, CC BY 4.0, tier A.
- **11-14:** Several record versions under one concept DOI. Verified at the [Zenodo API](https://zenodo.org/api/records/4813508) on 2026-11-25.

##### Paired robotic and handheld lumbar spine US with CT
- **1-6:** "A large, paired dataset of robotic and handheld lumbar spine ultrasound with ground-truth CT benchmarking", Scientific Data, 2025-11-10, DOI 10.1038/s41597-025-06047-9. 63 healthy volunteers; handheld and robot-assisted scans with synchronised 3D probe positions; CT and CT-based models of L1 to L5; demographics (search snippets of [PMC12603223](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12603223/)). A related Balgrist trial is [NCT05904418](https://clinicaltrials.gov/study/NCT05904418).
- **7-10:** Repository not found (the PMC page showed a captcha). A later paper says it used the data under CC BY 4.0 ([UltraVoxelGS, arXiv 2611.11951](https://arxiv.org/pdf/2611.11951), search snippet). Tier unknown.
- **14:** Unverified (search snippets only).

##### Porcine spinal cord US
- **1-6:** GitHub [HEPIUSLAB/ultrasound_spinal_cord_dataset](https://github.com/HEPIUSLAB/ultrasound_spinal_cord_dataset), a fork of avishakumar21/ultrasound-spinal-cord-dataset; Johns Hopkins University; paper "under review", no DOI. 25 pigs; spinal cord before and after contusion injury; 10,223 B-mode PNG images (segmentation subset) and 2,245 (localisation subset), cropped to 690 × 275; boxes in XML and semantic masks. Device not stated.
- **7-10:** Two Google Drive links; licence not stated; tier A (Drive quotas may break scripts).
- **11-13:** Fork and original hold the same data. Used in OpenUS-46 ("Porcine, spinal cord").
- **14:** Verified at the [GitHub README](https://github.com/HEPIUSLAB/ultrasound_spinal_cord_dataset) on 2026-11-25.

##### Biceps M-mode US with EMG
- **1-10:** "Spatial variation and inconsistency between estimates of onset of muscle activation from EMG and ultrasound", Zenodo DOI 10.5281/zenodo.232032, 2017-01-06, CC BY 4.0, open. M-mode clips (.tvd) and DICOM onset images of the biceps brachii of ten healthy men during isometric elbow flexion at 20% to 70% of maximal force. Image count not stated. Tier A — [Zenodo search result](https://zenodo.org/api/records?q=ultrasound%20muscle%20images&size=25&type=dataset)
- **14:** Verified at the Zenodo search API on 2026-11-25.

#### Peripheral nerves and regional anaesthesia

##### Kaggle Ultrasound Nerve Segmentation
- **1:** Kaggle competition "Ultrasound Nerve Segmentation", 2016 — [kaggle.com/c/ultrasound-nerve-segmentation](https://www.kaggle.com/c/ultrasound-nerve-segmentation)
- **2-5:** Brachial plexus in the neck; binary nerve masks; some images contain no nerve. 11,143 images ([arXiv 2602.00763](https://arxiv.org/html/2602.00763v1)): 5,635 training and 5,508 test images of 420 × 580 pixels from 47 patients ([UCSD course report](https://noiselab.ucsd.edu/ECE228_2019/Reports/Report9.pdf), secondary). Test masks were never released (search snippet). Other counts: 11,134 ([OpenUS README](https://raw.githubusercontent.com/XZheng0427/OpenUS/main/README.md)); 16,778 ([survey](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/)). GB unknown.
- **6:** Data from Halyard Health (UCSD report, secondary); devices unknown.
- **7-10:** Kaggle competition data; needs a Kaggle account and acceptance of the competition rules before the API works (standard Kaggle behaviour; rules not read, since Kaggle pages need JavaScript and the competitions API needs a login). Licence: competition rules, unknown. Tier C, then B.
- **11-13:** Many GitHub and Kaggle mirrors. A pruned subset of 2,323 images removes images with inconsistent annotations ([gcpds docs](https://gcpds-image-segmentation.readthedocs.io/en/latest/_modules/image_segmentation/datasets/segmentation/ultrasound_nerve_brachial_plexus.html)). Burned-in text unknown. Used in US-43d ("US nerve Segmentation"), OpenUS (11,134) and OpenUS-46 ("BP").
- **14:** Unverified at Kaggle (page not machine-readable); counts from secondary sources.

##### Regional-US brachial plexus videos
- **1:** GitHub [Regional-US/brachial_plexus](https://github.com/Regional-US/brachial_plexus); paper "Nerve Block Target Localization and Needle Guidance for Autonomous Robotic Ultrasound Guided Regional Anesthesia", submitted to IROS 2024; no DOI on the page.
- **2-5:** "a deidentified set of 227 ultrasound videos of brachial plexus region and their ground truth annotations", from three US machines (one folder named Sonosite). Labels: nerve plexus boxes, active-contour masks for each frame, needle annotations (Sonosite folder). Frame count not stated; OpenUS counts 40,788 images; the survey lists 277 (probably a typo of 227; my inference). A thesis from IIIT Hyderabad describes 227 subjects and 41,000 annotated frames ([IIIT thesis, search snippet](https://cdn.iiit.ac.in/cdn/cvit.iiit.ac.in/images/Thesis/MS/Abhishek_Tyagi/Thesis_Abhishek_Tyagi_20173067.pdf)).
- **6:** Institution not stated on the page (IIIT Hyderabad per the snippet; unverified).
- **7-10:** "shared with a non-commerical data use agreement"; the page gives no download route. Tier C.
- **11-13:** Frames of one video are near-duplicates. Used in US-43d ("brachial plexus, github"), OpenUS and OpenUS-46.
- **14:** Verified at the [GitHub README](https://github.com/Regional-US/brachial_plexus) on 2026-11-25.

##### UBPD (Ultrasound Brachial Plexus Dataset)
- **1-5:** Ding et al., "Multiple Instance Segmentation in Brachial Plexus Ultrasound Image Using BPMSegNet" ([arXiv 2012.12012](https://arxiv.org/pdf/2012.12012)). 1,055 images with masks of nerve, muscle, vein and artery (1,052 in arXiv v1), from videos of 101 patients; 955 training images from 91 patients and 97 test images from 10 patients (search snippets of the paper).
- **7-10:** Host [ubpd.worldwidetracing.com:9443](https://ubpd.worldwidetracing.com:9443/) gave a DNS failure on 2026-11-25: closed or dead link. Licence unknown. Tier D.
- **11-13:** Same dataset as "UPBD" in US-43d, OpenUS (955 images) and OpenUS-46 (same host URL).
- **14:** Dead link confirmed on 2026-11-25; paper facts from search snippets.

##### Femoral nerve block set
- **1-5:** Huang et al., "Applying deep learning in recognizing the femoral nerve block region on ultrasound images", Ann Transl Med 2019;7(18), doi:10.21037/atm.2019.08.61; 562 images; the abstract says the authors "constructed and shared a dataset", but no location is given — [ATM article](https://atm.amegroups.org/article/view/29596)
- **7-14:** No access route found; tier D. Verified at the [article page](https://atm.amegroups.org/article/view/29596) on 2026-11-25.

#### Brain

##### RESECT
- **1:** "RESECT: a clinical database of pre-operative MRI and intra-operative ultrasound in low-grade glioma surgeries", Xiao, Fortin, Unsgård, Rivaz, Reinertsen; release 2017-05-30; [doi:10.11582/2017.00004](https://doi.org/10.11582/2017.00004); paper Med Phys 2017;44(7):3875-3882, [doi:10.1002/mp.12268](https://doi.org/10.1002/mp.12268) — [Sigma2 record](https://archive.sigma2.no/dataset/5D6BFC33-F58D-4F56-88E8-C40AF269D6F2)
- **2-5:** 23 patients with low-grade glioma; pre-operative MRI and intra-operative US; homologous landmarks in MINC .tag files; NIfTI and MINC; 3,335.7 MB.
- **6:** Contact Ingerid Reinertsen, SINTEF (Norway); devices not checked.
- **7-10:** Sigma2 NIRD archive; "Download full dataset" option; a sign-in link exists, but the page does not say a login is needed for the files. CC BY 4.0. Tier A? (login status unverified).
- **11-13:** Base of RESECT-SEG and of the CuRIOUS challenges. Large-scale use unknown.
- **14:** Verified at the [Sigma2 record](https://archive.sigma2.no/dataset/5D6BFC33-F58D-4F56-88E8-C40AF269D6F2) on 2026-11-25.

##### RESECT-SEG
- **1-5:** Behboodi et al., "RESECT-SEG: Open access annotations of intra-operative brain tumor ultrasound images" ([arXiv 2207.07494](https://arxiv.org/abs/2207.07494v1)); 2024 version in Med Phys, doi:10.1002/mp.17317 (search snippet). Labels on RESECT iUS: tumour and resection cavity (2022), plus sulci and falx cerebri (2024); 3D NIfTI.
- **7-10:** OSF project "RESECT-Segmentation-All-Labels", created 2023-08-04, modified 2024-08-30, public, no licence set ([OSF API](https://api.osf.io/v2/nodes/jv8bk/)). Tier A (public OSF files; download not tried).
- **11-13:** Labels only; images come from RESECT. Training data of CuRIOUS-SEG 2022 (search snippet).
- **14:** Verified at the [OSF API](https://api.osf.io/v2/nodes/jv8bk/) on 2026-11-25.

##### CuRIOUS challenges (2018, 2019, 2022)
- **1-13:** MICCAI challenges on MR-to-iUS registration and on iUS segmentation built on RESECT; the 2022 data page says RESECT-SEG is provided in addition to the original database (search snippet of [curious2022.grand-challenge.org/data](https://curious2022.grand-challenge.org/data/)). Test-set source and licence unknown. Tier C? (Grand Challenge registration).
- **14:** Unverified: the [CuRIOUS 2019](https://curious2019.grand-challenge.org/) and 2022 pages returned HTTP 403 to automated fetches on 2026-11-25.

##### BITE (Brain Images of Tumors for Evaluation)
- **1:** Mercier et al., "Online database of clinical MR and ultrasound images of brain tumors", Med Phys 2012;39(6):3253-61 ([doi:10.1118/1.4709600](https://doi.org/10.1118/1.4709600)) — [BITE page](https://nist.mni.mcgill.ca/?p=672)
- **2-5:** 14 brain tumour patients, MNI, 2010; pre- and post-operative T1 MR with gadolinium; 2D and 3D B-mode iUS before and after resection; landmarks. Group 1, 4.6 GB (US pre/post); group 2, 2.1 GB (MR and pre-resection US); group 3, 565 MB (MR pre/post); group 4, 591 MB (MR and post-resection US, about 15 landmarks per patient; cite Rivaz et al. 2015). Total about 7.9 GB (my sum).
- **6:** Montreal Neurological Institute (Canada); devices not stated on the page.
- **7-10:** Direct .tar.gz and .zip links on bic.mni.mcgill.ca; no form. No licence stated; patients consented to online distribution (NEU-09-010). Tier A (links not tested).
- **11-13:** Groups are views of one 14-patient set. A "BITE2" extension is mentioned in a book chapter (search snippet). Large-scale use unknown.
- **14:** Verified at the [BITE page](https://nist.mni.mcgill.ca/?p=672) on 2026-11-25.

##### ReMIND (Brain Resection Multimodal Imaging Database)
- **1:** TCIA collection, [doi:10.7937/3RAG-D070](https://doi.org/10.7937/3RAG-D070), version 1, updated 2023-09-26; paper Juvekar et al., Scientific Data 2024, [doi:10.1038/s41597-024-03295-z](https://doi.org/10.1038/s41597-024-03295-z) — [TCIA page](https://www.cancerimagingarchive.net/collection/remind/)
- **2-5:** 114 subjects treated 2018 to 2022 (92 gliomas, 11 metastases, 11 other per a search snippet of the paper); 228 studies, 1,346 series, 85,733 images; MR, US and segmentations; 43.73 GB in total (43.53 GB images and segmentations; 208 MB NRRD segmentations).
- **6:** Brigham and Women's Hospital (Boston, USA); tracked 2D neuro-cranial curvilinear transducer (model not given); 3T intraoperative MRI.
- **7-10:** TCIA Data Retriever for DICOM, Aspera for NRRD, direct CSV; Imaging Data Commons search linked. CC BY 4.0 under the TCIA Data Usage Policy. Tier A (public TCIA collection; download not tried).
- **11-13:** Parent of ReMIND2Reg and the Learn2Reg task. Large-scale use unknown.
- **14:** Verified at the [TCIA page](https://www.cancerimagingarchive.net/collection/remind/) on 2026-11-25.

##### ReMIND2Reg and the Learn2Reg task
- **1:** "ReMIND2Reg dataset (2023)", Dorent, Wells, Kapur (Harvard Medical School); v2.1, 2024-05-29; DOI 10.5281/zenodo.11387725 — [Zenodo API](https://zenodo.org/api/records/11387725)
- **2-5:** Pre-operative ceT1 and T2 MRI and post-resection 3D iUS; 104 patients (99 training, 5 validation); NIfTI cropped to 256³ at 0.5 mm; landmarks for target registration error. One zip, 3.20 GB, md5 given.
- **7-10:** Zenodo, open, CC BY 4.0; tier A.
- **11-13:** Pre-processed subset of ReMIND. Learn2Reg 2025 used 99 training, 5 validation and 10 private test cases ([Learn2Reg 2025](https://learn2reg.grand-challenge.org/learn2reg-2025/); [arXiv 2508.09649](https://arxiv.org/abs/2508.09649v1), search snippets).
- **14:** Verified at the [Zenodo API](https://zenodo.org/api/records/11387725) on 2026-11-25.

##### BraTioUS (Brain Tumor Intraoperative Ultrasound Dataset)
- **1:** Esteban-Sinovas et al. (14 creators, last Cepeda), Zenodo 2025-08-16, DOI 10.5281/zenodo.16887363 (concept 10.5281/zenodo.16887362); data paper in Data in Brief 2026 ([PMC12874095](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12874095/), search snippet) — [Zenodo API](https://zenodo.org/api/records/16887363)
- **2-5:** 1,669 B-mode 2D iUS images from 142 glioma patients (2018 to 2023), each with a tumour mask; files 239 MB (images), 3.8 MB (masks), 15 KB (metadata), md5 given.
- **6:** Six hospitals in Spain, India, France, Italy (two) and the USA; Hitachi, Esaote, BK, Supersonic and Sonowand systems with linear or curved neuro probes.
- **7-10:** Zenodo, open, CC BY 4.0; tier A. The record is not the latest version: check the concept DOI before download.
- **11-13:** The USA site's overlap with ReMIND (also Boston) is unknown. Burned-in text unknown.
- **14:** Verified at the [Zenodo API](https://zenodo.org/api/records/16887363) on 2026-11-25.

##### Neonatal 3D transfontanellar US (Universidad de Cádiz)
- **1:** "Dataset of 3D ultrasound neuroimages" (2025-02-24, DOI 10.5281/zenodo.14917169) and "Dataset of 3D ultrasound neuroimages and Supporting info" (Version 2, 2026-04-15, DOI 10.5281/zenodo.19555871); concept DOI 10.5281/zenodo.14917168; creator Lionel Cervera Gontard; described by a presentation, DOI 10.5281/zenodo.14917011 — [Zenodo v1 API](https://zenodo.org/api/records/14917169); [Zenodo v2 API](https://zenodo.org/api/records/19555871)
- **2-5:** "2D slices of 3D US of the brain of neonates"; used to train a GAN. Version 2 holds four NRRD volumes, two MP4 videos, a PDF and a MATLAB slicer, about 40 MB in total; the earlier version holds one 44.9 MB zip. The survey lists 5 volumes. No labels.
- **7-10:** Zenodo, open, CC BY 4.0, md5 given; tier A.
- **11-13:** Versions overlap. NRRD file names contain dates (my observation from the file list); whether they hold identifiers is unknown.
- **14:** Verified at the Zenodo APIs on 2026-11-25.

##### Mouse GL261 brain tumour US
- **1-5:** Dorosti et al., "High-Resolution Ultrasound Data for AI-Based Segmentation in Mouse Brain Tumor", Scientific Data 2025;12:1322, [doi:10.1038/s41597-025-05619-z](https://doi.org/10.1038/s41597-025-05619-z); 1,856 annotated images of GL261 glioblastoma in live and post-mortem mice ([library record](https://library.kab.ac.ug/Record/doaj-art-a9b220397db743b9a3a7513ca675caa7/Description); news item from Dalhousie University, search snippet).
- **7-14:** Repository not found (nature.com redirected to a login). Unverified.

#### Eye

##### Oculo
- **1:** Oculo, Sankara Eye Hospital, Hugging Face, created 2026-06-25; linked to a MICCAI 2026 paper (search snippet) — [HF API](https://huggingface.co/api/datasets/SankaraEyeHospital/Oculo)
- **2-5:** B-scan images with multi-label abnormality labels (vitreous echoes, retinal detachment, mass lesions per a search snippet); 1,630 PNG images plus data.csv; 1,242 patients (search snippet); 358 MB; fixed train, validation and test split.
- **6:** Sankara Eye Hospital (India per the hospital name; unverified).
- **7-10:** Hugging Face, not gated, CC BY-SA 4.0; tier A.
- **11-14:** No overlap known. Verified at the [HF API](https://huggingface.co/api/datasets/SankaraEyeHospital/Oculo) on 2026-11-25.

##### ERDES
- **1:** "ERDES: A Benchmark Video Dataset for Retinal Detachment and Macular Status Classification in Ocular Ultrasound", Ozkut et al., [arXiv 2508.04735](https://arxiv.org/pdf/2508.04735), under review at Scientific Data — [project page](https://osupcvlab.github.io/ERDES)
- **2-5:** 5,381 B-scan clips, about 5 h 10 min; clip-level labels: Normal 4,233, posterior vitreous detachment 646, retinal detachment 502 (macula intact 199, macula detached 303); three expert labellers and one reviewer. Zenodo files total 1.94 GB with md5.
- **6:** University of Arizona Emergency Department (USA), with Ohio State's Photogrammetric Computer Vision Lab; 5 to 12 MHz linear probes of Mindray/Zonare, Philips, GE and Sonosite.
- **7-10:** [Hugging Face pcvlab/erdes](https://huggingface.co/api/datasets/pcvlab/erdes) (not gated) and [Zenodo 18644370](https://zenodo.org/api/records/18644370); CC BY 4.0; tier A.
- **11-13:** Same release on two hosts. Burned-in text: health information and annotations at the sides were removed by cropping each frame to the globe found by a YOLOv8 detector.
- **14:** Verified at the project page, HF API and Zenodo API on 2026-11-25.

##### Ophthalmic US report set (Wang et al.)
- **1-5:** "A Labeled Ophthalmic Ultrasound Dataset with Medical Report Generation Based on Cross-modal Deep Learning", Wang et al., [arXiv 2407.18667](https://arxiv.org/abs/2407.18667) (2024-07-26). 4,858 images of 2,417 patients from one ophthalmology hospital in Shenyang, China, 2018; each with a free-text Chinese report, 15 finding types with locations and nine blood-flow values.
- **7-14:** No data availability statement on the abstract page; access unknown. Verified (abstract only) on 2026-11-25.

#### Skin

##### Dermatologic Ultrasound Images (Kaggle)
- **1-5:** "Dermatologic Ultrasound Images for classification", owner Dr F. Alfageme; paper Laverde-Saad et al., Skin Res Technol 2022, [doi:10.1111/srt.13086](https://doi.org/10.1111/srt.13086); "Images labelled with diagnosis, malignancy in B mode and Color Doppler"; 14.6 MB; updated 2023-04-02 — [Kaggle API](https://www.kaggle.com/api/v1/datasets/view/alfageme/dermatologic-ultrasound-images). The survey lists 202 images.
- **7-10:** [Kaggle](https://www.kaggle.com/datasets/alfageme/dermatologic-ultrasound-images); licence "Unknown"; tier B (Kaggle token).
- **14:** Verified at the [Kaggle API](https://www.kaggle.com/api/v1/datasets/view/alfageme/dermatologic-ultrasound-images) on 2026-11-25.

##### HFUS skin layers in atopic dermatitis and psoriasis (Czajkowska et al. 2021)
- **1-5:** "Data for: Deep Learning Approach to Skin Layers Segmentation in Inflammatory Dermatoses", Czajkowska, Badura, Płatkowska-Szczerek, Korzekwa; v1, 2021-08-20; DOI 10.17632/5p7fxjt7vs.1; reference paper [doi:10.1016/j.ultras.2021.106412](https://doi.org/10.1016/j.ultras.2021.106412). 380 images of 380 patients (AD 303, psoriasis 77); DUB SkinScanner75 at 75 MHz; 2067 × 1555 pixels; masks of the entry echo (epidermis) and SLEB; trained models included — [Mendeley](https://data.mendeley.com/datasets/5p7fxjt7vs)
- **6-10:** Silesian University of Technology (Politechnika Śląska, Poland); CC BY 4.0; tier A.
- **14:** Verified at [Mendeley](https://data.mendeley.com/datasets/5p7fxjt7vs) on 2026-11-25.

##### HFUS skin layer expert masks (Slian, Czajkowska et al.)
- **1-5:** "Segmentation of skin layers on HFUS images using the attention mechanism - exper masks", v2, 2026-01-05, DOI 10.17632/68y7cppct8.2; paper Comput Methods Programs Biomed 2025;263, [doi:10.1016/j.cmpb.2025.108668](https://doi.org/10.1016/j.cmpb.2025.108668). AD patients; DermaScan C (Cortex Technology), 20 MHz; 224 × 224 images with entry echo, SLEB and dermis masks; two time points per image ID; counts not stated — [Mendeley](https://data.mendeley.com/datasets/68y7cppct8/2)
- **7-10:** CC BY 4.0; tier A.
- **14:** Verified at [Mendeley](https://data.mendeley.com/datasets/68y7cppct8/2) on 2026-11-26.

##### HFUS atopic dermatitis staging and HFUS facial skin image quality
- Staging: Mendeley record "High frequency ultrasound - atopic dermatitis staging", 78 patients scored on the IGA scale by two experts, linked to a 2025 Scientific Reports paper (search snippet of [Mendeley 5x322f4r2r](https://data.mendeley.com/datasets/5x322f4r2r)). Licence not checked. Unverified.
- Image quality: Czajkowska et al., Sensors 2022;22(4):1478, doi:10.3390/s22041478; 17,425 facial HFUS images from 516 measurements of 44 patients, each marked correct or not by two experts; the paper says the database was shared, but no location was found ([DOAJ record](https://doaj.org/article/12a4cd99501941759dd8568cfad4bba0), search snippets). Unverified.

#### Dental, oral and tongue

##### UltraSuite and the TaL corpus
- **1:** UltraSuite repository: Eshky et al., "Ultrasuite: A repository of ultrasound and acoustic data from child speech therapy sessions", Interspeech 2018; TaL: Ribeiro et al., "TaL: a synchronised multi-speaker corpus of ultrasound tongue imaging, audio, and lip videos", IEEE SLT 2021 — [UltraSuite site](https://ultrasuite.github.io/)
- **2-5:** Ultrasound tongue imaging with audio. UXTD (58 typically developing children), UXSSD (8 children with speech sound disorders), UPX (20 children), Cleft (29 children with cleft lip and palate), UX2020 (37 children), TaL1 (one adult voice talent, six sessions), TaL80 (81 adults); TaL adds lip video. Hours and GB not stated on the page.
- **6:** University of Edinburgh group (per the papers; affiliation not stated on the page).
- **7-10:** Download via rsync (sample, single utterance, full set, labels, whole repository). Datasets under CC BY-NC 4.0; code Apache 2.0. Tier A (rsync; login not mentioned).
- **11-14:** No overlap known. Verified at the [UltraSuite site](https://ultrasuite.github.io/) on 2026-11-25.
- **Dental:** No public intraoral or periodontal US dataset was found. A 2025 study used 158 intraoral US videos of 30 orthodontic patients ([PubMed 41413674](https://pubmed.ncbi.nlm.nih.gov/41413674/), search snippet); an MDPI 2022 study used in-house sets of 3,417 and 2,135 files ([MDPI Sensors](https://www.mdpi.com/1424-8220/22/19/7101/html), search snippet). Neither states a release.

#### Head and neck

##### LymphUs
- **1:** LymphUs, a multicentre cervical lymph node US database in papillary thyroid cancer; Mohammadi et al., Data in Brief 2026, doi:10.1016/j.dib.2026.112694; Abbasian Ardakani et al., J Ultrasound Med 2023, doi:10.1002/jum.16131 — [LymphUs page](https://qamebi.com/cervical-lymph-node/)
- **2-5:** 338 patients with suspected node metastasis: centre 1, 180 (81 malignant, 99 benign); centre 2, 158 (82 malignant, 76 benign). Images with segmentation masks, fusion images and imaging features in Excel. Image count and GB not stated.
- **6:** Two centres; devices and country not stated.
- **7-10:** Direct links to Center-1.zip and Center-2.zip; no form. CC BY-NC 4.0, "freely accessible for research purposes". Tier A.
- **11-13:** The thyroid researcher may list it too (lymph nodes of thyroid cancer patients). Large-scale use unknown.
- **14:** Verified at the [LymphUs page](https://qamebi.com/cervical-lymph-node/) on 2026-11-25.
- **Salivary glands:** No public set was found. Vukicevic et al. 2021 used 1,184 images of 287 patients and released model files only; the Brest GSID database (210 cases) states no release; a Dryad Sjögren record holds scores, not images ([PMC10668981](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10668981/), [Dryad doi:10.5061/dryad.953dh](https://datadryad.org/dataset/doi:10.5061/dryad.953dh), search snippets).

#### Multi-organ collections and benchmarks

##### RadImageNet, US part. HIGH PRIORITY
- **1:** RadImageNet; GitHub [BMEII-AI/RadImageNet](https://github.com/BMEII-AI/RadImageNet); paper "RadImageNet: An Open Radiologic Deep Learning Research Dataset for Effective Transfer Learning" ([RSNA atlas card](https://atlas.rsna.org/cards/bb89e649-b6cc-47fb-9634-b087cc7c6df2)).
- **2-5:** "1.35 million annotated CT, MRI, and ultrasound images" (README); collected 2005 to 2020 from 131,872 patients at one outpatient radiology facility (atlas card, search snippet). US frames by organ in the US-JEPA table (secondary): kidney 111,252; thyroid 92,598; liver 78,535; gallbladder 39,743; pancreas 21,645; heart 19,062; uterus 13,312; spleen 6,520; ovary 3,595; fibroid 2,095; portal vein 769; bladder 758. These sum to 389,884 frames, of which 259,222 are abdominal (kidney, liver, gallbladder, pancreas, spleen, portal vein, bladder; my sums) — [US-JEPA Table A.1](https://arxiv.org/html/2602.19322). Labels: organ-level classes (pathology classes not checked).
- **6:** One outpatient facility (USA per the authors' institution; not checked); devices unknown.
- **7-10:** "available by request" at [radimagenet.com](https://www.radimagenet.com/); if no reply, e-mail the team. No dataset licence stated (MIT badge covers the repository). Tier C.
- **11-13:** Used in the OPUS pretraining corpus of US-JEPA. Burned-in text unknown.
- **14:** Access verified at the [GitHub README](https://github.com/BMEII-AI/RadImageNet) on 2026-11-25; US counts are secondary (US-JEPA), not confirmed at RadImageNet.

##### Butterfly MIT GrandHack 2018. HIGH PRIORITY
- **1-5:** [ButterflyNetwork/MITGrandHack2018](https://github.com/ButterflyNetwork/MITGrandHack2018): 9 classes (Morison's pouch, bladder, heart PLAX, heart 4-chamber, heart 2-chamber, IVC, carotid artery, lungs, thyroid); Butterfly iQ; 31 individuals; PNG in patient folders. Image counts: 41,076 (28,053 train, 6,272 validation, 6,751 test) per [US-JEPA](https://arxiv.org/html/2602.19322) and [UltraBench wiki](https://github.com/adamtupper/ultrabench/wiki/Datasets).
- **7-10:** GitHub release tarballs (v.0.0.1). Terms: "may be used solely for the MIT GrandHack 2018"; images "may not be re-published without the express written permission of Butterfly Network Inc." Repository archived on 2024-01-26. Tier D (terms), although the links are scriptable.
- **11-13:** Frames from 31 people: strong near-duplicates within patients (inference). Used in UltraBench and US-JEPA.
- **14:** Verified at the [GitHub README](https://github.com/ButterflyNetwork/MITGrandHack2018) on 2026-11-25.

##### AbdomenUS ("US simulation & segmentation"). HIGH PRIORITY
- **1-5:** Kaggle "US simulation & segmentation", owner José Ignacio Orlando, creator Santiago Vitale; cite Vitale et al., "Improving realism in patient-specific abdominal ultrasound simulation using CycleGANs", Int J Comput Assist Radiol Surg 2019;15(2):183-192. 617 real scans, 61 of them with manual masks of liver, kidneys, gallbladder, spleen and vessels; 926 scans simulated by ray casting from 13 CT scans, with silver-standard masks (liver, pancreas, adrenals, gallbladder, spleen, vessels, bones); 2.10 GB; updated 2026-09-22 — [Kaggle API](https://www.kaggle.com/api/v1/datasets/view/ignaciorlando/ussimandsegm)
- **7-10:** [Kaggle](https://www.kaggle.com/datasets/ignaciorlando/ussimandsegm); licence "Data files © Original Authors"; tier B.
- **11-13:** Used in US-43d, OpenUS (617) and OpenUS-46. The abdomen researcher may cover it too.
- **14:** Verified at the [Kaggle API](https://www.kaggle.com/api/v1/datasets/view/ignaciorlando/ussimandsegm) on 2026-11-25.

##### AHU (An annotated heterogeneous ultrasound database). HIGH PRIORITY
- **1:** Yang et al., Scientific Data 2025;12:148, [doi:10.1038/s41597-025-04464-4](https://doi.org/10.1038/s41597-025-04464-4); figshare [doi:10.6084/m9.figshare.26889334.v1](https://doi.org/10.6084/m9.figshare.26889334.v1), 2025-01-26 — [figshare API](https://api.figshare.com/v2/articles/26889334)
- **2-5:** 1,833 US items (videos and still images), 13 anomaly types; organs include heart, thyroid, abdomen, kidneys and lungs (search snippet of the paper). Raw Data 26.6 GB, Filtered Data 6.46 GB, Processed Data 1.06 GB; 34.13 GB in total; md5 given.
- **6:** "derived from publicly available data on the Internet", mainly from 31 video creators affiliated with hospitals in 16 provinces of China (search snippet).
- **7-10:** figshare, open, CC BY 4.0; tier A. The creators' own rights in the source videos are not addressed (see section 2).
- **11-13:** Internet-sourced, so overlap with other scraped sets is possible (inference). "All data have been anonymized" ([GitHub README](https://github.com/Bean-Young/AHU-Database)); watermarks not reported.
- **14:** Verified at the [figshare API](https://api.figshare.com/v2/articles/26889334) on 2026-11-26; the project page ahudataset.github.io returned 404 on 2026-11-25.

##### USAnotAI. HIGH PRIORITY
- **1-10:** [ftsvd/USAnotAI](https://github.com/ftsvd/USAnotAI), "Organ Classification on Abdominal Ultrasound using Javascript", SIIM 2019 Innovation Challenge winner; train and test folders of PNG files named by organ; no licence; no DOI. OpenUS counts 366 images ([README](https://raw.githubusercontent.com/XZheng0427/OpenUS/main/README.md)). Tier A (in the Git repository).
- **14:** Verified at the [GitHub page](https://github.com/ftsvd/USAnotAI) on 2026-11-25; organ list not shown.

##### UUSIC 2025 and UUSIVC 2026 challenges. HIGH PRIORITY
- **1-5:** Universal UltraSound Image Challenge 2025 ([uusic2025.github.io](https://uusic2025.github.io), [arXiv 2512.17279](https://arxiv.org/abs/2512.17279v1)) and the Universal UltraSound Image and Video Analysis Challenge at MICCAI 2026 ([UUSIVC 2026](https://uusivc2026-sudo.github.io/uusivc2026.github.io/)). Tasks: breast nodule classification and segmentation, thyroid nodule segmentation, fatty liver classification, kidney contour, fetal head contour, cardiac contour, appendicitis classification. Public sources: BUSI, BUSIS, BUS-BRA, DDTI, Fatty-Liver, KidneyUS, Fetal HC, CAMUS and a Regensburg paediatric appendicitis set; private data from Hangzhou First People's Hospital and the Netherlands Cancer Institute.
- **7-10:** Codabench ([2025](https://www.codabench.org/competitions/9106/), [2026](https://www.codabench.org/competitions/17263/)); training and validation released on registration (2025-06-20; 2026-06-29); validation and test mostly private and not disclosed; no extra training data allowed; licence not stated. Tier C.
- **14:** Verified at both challenge pages on 2026-11-25.

##### Link-list collections: US-43d, OpenUS, OpenUS-46, SonoCorpus, OPUS and UltraBench, US30K
- **US-43d (UltraSam):** 43 open datasets, "over 280,000 annotated segmentation masks", 2D and 3D; converter scripts; no download scripts; no licence for the collection — [GitHub](https://github.com/CAMMA-public/UltraSam); [arXiv 2411.16222](https://arxiv.org/html/2411.16222v1). In-scope members: FALLMUD, STMUS_NDA, brachial plexus (Regional-US), UPBD (UBPD), US nerve Segmentation (Kaggle), AbdomenUS, LUSS_phantom. Verified 2026-11-25.
- **OpenUS:** "more than 308K images from 42 public datasets" ([arXiv 2511.11510](https://arxiv.org/abs/2511.11510v1), search snippet); README table of 42 datasets with sizes and links, plus downstream BrainBenchmark, USenhance and FOCUS; repository badge CC BY-NC 4.0; links only — [README](https://raw.githubusercontent.com/XZheng0427/OpenUS/main/README.md). In-scope members with README sizes: brachial plexus 40,788; US nerve Segmentation 11,134; STMUS_NDA 4,355; UPBD 955; FALLMUD 813; AbdomenUS 617; LUSS_phantom 564; USAnotAI 366. Verified 2026-11-25.
- **OpenUS-46 (USF-MAE):** 46 datasets; "370,000 2D and 3D ultrasound images" (the README also says "360K ... from 43 datasets"); "All datasets remain under their original licenses"; links only — [GitHub](https://github.com/Yusufii9/USF-MAE). In-scope members: BP (Kaggle), Brachial Plexus (Regional-US), FALLMUD, Porcine spinal cord, STMUS_NDA, UPBD, LUSS_phantom, AbdomenUS. Verified 2026-11-25.
- **SonoCorpus (SonoBase):** "53 public datasets, 456,963 images and frames, 1,626,085 expert masks, 24 clinical applications, 17 countries"; releases checkpoints, data-split indices, deduplication hashes and a Zenodo manifest ([doi:10.5281/zenodo.22770825](https://doi.org/10.5281/zenodo.22770825), CC BY 4.0); "no images or masks are re-hosted"; weights CC BY-NC 4.0; code MIT — [GitHub](https://github.com/AlfredQin/sonobase); [arXiv 2609.19230](https://arxiv.org/abs/2609.19230). The dataset list is in the paper's Supplementary Table S1 (not read). Verified 2026-11-25.
- **OPUS and UltraBench (US-JEPA):** "5,123,697 frames curated from 50 distinct publicly available datasets" for pretraining; UltraBench downstream sets AUL, BUS-BRA, Butterfly, Fatty Liver, GBCU, MMOTU, POCUS, TN5000 — [arXiv 2602.19322](https://arxiv.org/html/2602.19322); [UltraBench wiki](https://github.com/adamtupper/ultrabench/wiki/Datasets). Verified 2026-11-25.
- **US30K (SAMUS):** "about 30K images and 69K masks covering 6 categories" from TN3K, DDTI, TG3K, BUSI, UDIAT, CAMUS and HMC-QU; a pre-processed copy on [Google Drive](https://drive.google.com/file/d/13MUXQIyCXqNscIKTLRIEHKtpak6MJby_/view); no licence for US30K; code MIT — [GitHub](https://github.com/xianlin7/SAMUS). No member is in this note's scope. Verified 2026-11-25.

##### SA-Med2D-20M, US part
- **1-10:** Ye et al., [arXiv 2311.11969](https://arxiv.org/pdf/2311.11969): 4.6M 2D images and 19.7M masks in 10 modalities; the paper's table lists 2,968 US images (search snippet). Hugging Face [OpenGVLab/SA-Med2D-20M](https://huggingface.co/api/datasets/OpenGVLab/SA-Med2D-20M): not gated, CC BY-NC-SA 4.0, 352.8 GB, split zip "SA-Med2D-16M"; only a 16M-mask subset is public "due to data privacy and ethical requirements" (search snippet). Tier A. Which public sets the US images come from was not checked.
- **14:** HF metadata verified on 2026-11-25; the US count is from a search snippet of the paper.

##### EchoAtlas (EchoCare)
- **1-10:** EchoCare ([GitHub](https://github.com/CAIR-HKISI/EchoCare); [arXiv 2509.11752](https://arxiv.org/pdf/2509.11752)) trains on EchoAtlas: 4.5 million images from 23 centres on 5 continents, 38 devices, 9 regions (abdomen, back, fetus, head and neck, lower limb, other, pelvis, thorax, upper limb) and 52 organs. The README calls it "publicly available" but gives no download route; weights on SharePoint; no licence. Tier unknown.
- **14:** Verified at the [GitHub README](https://github.com/CAIR-HKISI/EchoCare) on 2026-11-25.

##### npj Digital Medicine survey of public US datasets (catalogue, not a dataset)
- Alsharid et al., "On the public dissemination and open sourcing of ultrasound resources, datasets and deep learning models", npj Digit Med 2025;8:777, [doi:10.1038/s41746-025-02162-4](https://doi.org/10.1038/s41746-025-02162-4): 72 public US datasets and 56 open models; dataset web pages "will be made available online upon paper acceptance" — [PMC12722232](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/). Its Table 1 also lists a "Reconstructing 2D US into a 3D volume" set (forearms, 2,400, on request, no link). Verified 2026-11-25 (first 100,000 characters read).

#### Vision-language sets

##### U2-Bench
- **1-5:** Le et al., "U2-BENCH: Benchmarking Large Vision-Language Models on Ultrasound Understanding", ICLR 2026 ([proceedings](https://proceedings.iclr.cc/paper_files/paper/2026/hash/0df3d25c2eee3910864e721a312c384b-Abstract-Conference.html); [arXiv 2505.17779](https://arxiv.org/abs/2505.17779v2)); 7,241 cases, 15 anatomical regions, 8 tasks (diagnosis, view recognition, lesion localisation, clinical value estimation, report generation and others), 50 scenarios (search snippets). Per-task TSV files; 18.9 GB.
- **7-10:** [Hugging Face DolphinAI/u2-bench](https://huggingface.co/api/datasets/DolphinAI/u2-bench), not gated, CC BY-NC-ND 4.0; tier A.
- **11-13:** Probably built from public sets (not checked); abdomen or liver content not checked.
- **14:** HF metadata verified on 2026-11-25; content counts from search snippets.

##### Chinese US report sets (breast, thyroid, liver). HIGH PRIORITY
- **1-5:** Li et al., [arXiv 2406.00644](https://arxiv.org/html/2406.00644) (extends a conference paper); [project page](https://lijunrio.github.io/Ultrasound-Report-Generation/). Three Chinese image-report sets: breast 3,521 patients, thyroid 2,474, liver 1,395; two doctor-selected JPEG images per report; split 7:1:2 without overlap.
- **6:** Ultrasound department database of the PLA General Hospital (China); IRB YSB-2020-Y0902.
- **7-10:** "The ultrasound dataset is available at" a Google Drive link in the [GitHub README](https://github.com/LijunRio/Ultrasound-Report-Generation) (the link text and target IDs differ); no licence or usage terms. Tier A (if the Drive link works). Redistribution terms are unclear for hospital data with no licence.
- **14:** Verified at the README and arXiv on 2026-11-25.

##### ReMUD
- [ShiDaizi/ReMUD](https://github.com/ShiDaizi/ReMUD): "will be publicly released upon acceptance of the paper"; only the ReMUD-7B model is public; the paper reports over 45,000 QA and VQA items ([arXiv 2506.07837](https://arxiv.org/html/2506.07837v1), search snippet). Closed for now; tier D. Verified 2026-11-25.

#### Figure sets mined from PMC (see section 2 for counts and licences)
- ROCOv2, PMC-OA, PMC-15M, BIOMEDICA and MedTrinity-25M are described in section 2, Table 2.

#### Raw RF and channel data

##### PICMUS (Plane-wave Imaging Challenge in Medical UltraSound)
- **1-5:** IEEE IUS 2016 challenge; Liebgott et al., [doi:10.1109/ULTSYM.2016.7728908](https://doi.org/10.1109/ULTSYM.2016.7728908). Simulated and experimental phantom data for resolution and contrast, plus in vivo carotid cross-section and longitudinal views (Verasonics Vantage 256, L11 probe per one source, L11-4v per another) (search snippets of the [zea converter](https://zea.readthedocs.io/en/latest/_modules/zea/data/convert/picmus.html) and [USTB example](https://unioslo.github.io/USTB/examples/picmus/invivo_carotid_long.html)). HDF5; the official archive is final.
- **7-10:** [CREATIS site](https://www.creatis.insa-lyon.fr/Challenge/IEEE_IUS_2016/) (content did not load in my fetch); PICMUS files are also in the USTB Zenodo record and in [zeahub/picmus](https://huggingface.co/api/datasets?author=zeahub&limit=100) (licence "other"). Free to use with citation (zea converter, secondary). Tier A.
- **14:** Mirrors verified on 2026-11-25; terms secondary.

##### CUBDL (Challenge on Ultrasound Beamforming with Deep Learning)
- **1-10:** Hyun et al., "Deep Learning for Ultrasound Image Formation: CUBDL Evaluation Framework and Open Datasets", IEEE TUFFC 2021;68(12):3466-3483, doi:10.1109/TUFFC.2021.3094849 ([PMC8818124](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8818124/)). IEEE DataPort, [DOI 10.21227/f0hn-8f92](https://ieee-dataport.org/competitions/challenge-ultrasound-beamforming-deep-learning): a Creative Commons Attribution licence, but files need a login and a signed CUBDL Data Release Agreement, and only approved participants get access; users report missing approval e-mails ([DataPort node](https://ieee-dataport.org/node/1745)). Tier C.
- **14:** From search snippets of the DataPort pages; [cubdl.jhu.edu/data](https://cubdl.jhu.edu/data/) returned HTTP 403 on 2026-11-25. Partly verified.

##### USTB datasets
- **1-10:** Zenodo "USTB datasets", creator Ole Marius Hoel Rindal, publication 2019, record created 2026-05-18, DOI 10.5281/zenodo.20261898; 53 files, 28.97 GB, md5 per file, CC BY 4.0, open ([Zenodo API](https://zenodo.org/api/records/20261898)). The [USTB page](https://unioslo.github.io/USTB/datasets.html) lists 51 sets in HDF5-based UFF: channel data from Verasonics and Alpinion probes (L7-4, L3-8, P4, P2-4), phantoms (CIRS, hypoechoic, dynamic range), in vivo carotid (PICMUS and L7 cross-sections), in vivo heart (parasternal long axis, apical four-chamber), Field II simulations, ARFI and shear-wave elastography; citation details sit inside each file. Tier A.
- **14:** Verified at both pages on 2026-11-25.

##### Open-H-RF
- **1:** Stevens et al. (187 authors, 39 institutions), "Open-H-RF: A Large-Scale Ultrasound Raw Channel Dataset Initiative", [arXiv 2610.13616](https://arxiv.org/abs/2610.13616), v1 2026-10-09, v3 2026-11-17; dataset v1.1.
- **2-5:** "approximately 40 TB of medical ultrasound raw channel data in 19,332 acquisitions" (arXiv); the site gives 19,336 files; in vivo, phantom and simulated; tasks include reconstruction, speed of sound, aberration correction, flow, motion, quantitative US and interpretation; goals cover "echocardiography, general, fetal and transcranial imaging" ([site](https://open-h.github.io/Open-H-RF)).
- **6:** Led by Stanford, TU Eindhoven and NVIDIA; visible contributor folders on HF include colorado-boulder and concordia.
- **7-10:** [Hugging Face nvidia/Open-H-RF](https://huggingface.co/api/datasets/nvidia/Open-H-RF), not gated, CC BY 4.0; zea toolbox streaming and a "Generate download script" button. Tier A. Abdomen content not confirmed.
- **14:** Verified at arXiv, the site and the HF API on 2026-11-25.

##### zea mirrors on Hugging Face (zeahub)
- 19 public repositories, none gated: picmus, phantoms, simulations, zea-rotating-disk, zea-cardiac-2026 and DehazingEcho2025 (licence "other"); zea-carotid-2023 and us4us (CC BY 4.0); camus, camus-sample, cetus-miccai-2014, cetus-miccai-2014-polar and echoxflow (CC BY-NC-SA 4.0); echonet-dynamic, plax and zea-fat-layer-2025 (no licence tag) — [HF API listing](https://huggingface.co/api/datasets?author=zeahub&limit=100). Heart sets belong to another group. Tier A. Verified 2026-11-25.

##### PALA (Open Platform for Ultrasound Localization Microscopy)
- **1-10:** "OPULM PALA", Chavignon, Heiles, Hingot, Lopez, Teston, Couture; v1.1, 2020-12-17; DOI 10.5281/zenodo.4343435 (concept 10.5281/zenodo.3901636); open, CC BY 4.0. In vivo rat brain (240 files of 800 frames at 1 kHz with microbubbles), rat brain boluses (213 files), rat kidney, mouse tumour, in silico flow (including RF) and PSF; 12 files, 55.65 GB, md5 per file; the record also says "Request on data" with an e-mail address. Paper: Heiles et al., Nature Biomedical Engineering. Supplement: [doi:10.5281/zenodo.7883227](https://doi.org/10.5281/zenodo.7883227) (B-mode frames per a search snippet; not opened) — [Zenodo API](https://zenodo.org/api/records/4343435). Tier A.
- **14:** Verified at the [Zenodo API](https://zenodo.org/api/records/4343435) on 2026-11-25.

##### ULTRA-SR and ULMShare
- **ULTRA-SR:** IEEE IUS 2022 challenge (Imperial College London, Heriot-Watt); synthetic microvascular flow at low and high frequency on [Zenodo 7271766](https://zenodo.org/record/7271766); results in IEEE TMI 2024;43(8):2970-2987 ([PubMed 38607705](https://pubmed.ncbi.nlm.nih.gov/38607705/)), which also used in vivo mouse brain and human lymph node data for expert review (release of those not checked). Search snippets only; unverified. Tier A.
- **ULMShare:** Rauby et al., [arXiv 2606.07851](https://arxiv.org/abs/2606.07851) (2026-06-05): 99 whole-brain transcranial ULM acquisitions from 61 healthy mice, about 30 TB of raw data, hosted on the Federated Research Data Repository with a GitHub repository; open per the paper; dataset licence and URLs not on the abstract page. Tier unknown. Verified (abstract) 2026-11-25.

##### Other open RF and channel sets found on Zenodo
- Plane-wave raw data, 75 angles, breast and calibration phantoms (DOI 10.5281/zenodo.7986407, 2023-06-19; 7.23 + 1.30 GB; licence not shown); Three-Dimensional Ultrasound Matrix Imaging (DOI 10.5281/zenodo.8159177, 2023; pork tissue and head phantom RF; about 35 GB; CC BY 4.0); Versatile Vasculature Chips for ULM (DOI 10.5281/zenodo.15614916, 2025-12-01; 200 files of 400 beamformed IQ frames; five zips of about 7.9 GB; CC BY 4.0); USCT phantom dataset (DOI 10.5281/zenodo.20426578, 2026-06-02; 38.13 GB; CC BY 4.0) — [Zenodo search API](https://zenodo.org/api/records?q=ultrasound%20phantom%20dataset&size=25&type=dataset). All open; tier A. Verified 2026-11-25 (search result metadata).

#### Simulation, phantom and synthetic
- **Lung COVID phantom ("LUS_model", "LUSS_phantom" in collections):** McLaughlan, Howell, Ingram (University of Leeds), 2024, [doi:10.5518/1485](https://doi.org/10.5518/1485), CC BY 4.0; VideoClips.zip (135 MB) of 2 s phantom scans from several systems, LUS_model.zip (91 MB) of labelled training and test frames, and a MATLAB frame extractor; counts not stated — [Leeds record](https://archive.researchdata.leeds.ac.uk/1263/). Used in US-43d, OpenUS (564) and OpenUS-46. Tier A. Verified 2026-11-25.
- **ArteryPhantom-42k:** DOI 10.5281/zenodo.20606968, 2026-06-09; 42,266 B-mode frames of a vessel phantom in beef, 6,612 labelled in three probe-to-vessel alignment classes; frames.zip 4.09 GB, videos.zip 1.38 GB; data CC BY 4.0, tools MIT — [Zenodo search API](https://zenodo.org/api/records?q=ultrasound%20phantom%20dataset&size=25&type=dataset). Tier A. Verified 2026-11-25.
- **Thoracolumbar fascia phantom ground truth:** DOI 10.5281/zenodo.15606741, 2025-06-06; gel-pad phantoms, distance and speed ground truth, 1.25 GB, CC BY 4.0 — same source. Tier A. Verified 2026-11-25.
- **Also in other entries:** the simulated part of AbdomenUS; the spine US-CT database (US simulated from CT); Field II sets in USTB; ULTRA-SR and the PALA in silico files.
- **Software only:** SonoSpadePP, CT-to-US synthesis for teaching simulators, Zenodo DOI 10.5281/zenodo.24548096, dated 2026-11-26, Apache 2.0, resource type software ([Zenodo search API](https://zenodo.org/api/records?q=ultrasound%20needle&size=25&sort=mostrecent)).

#### Needle guidance and robotics
- **Regional-US needle labels:** needle annotations in the Sonosite folder of the brachial plexus videos (see the nerve entry) — [GitHub](https://github.com/Regional-US/brachial_plexus). The only needle labels with a stated release route that I found (DUA).
- **Motion-informed needle segmentation:** Goel et al., ISBI 2024, [arXiv 2312.01239](https://arxiv.org/abs/2312.01239); 17 videos of the femoral area of different participants, Butterfly probe, needle masks (search snippet); no release stated on the abstract page. Unverified.
- **Vicomtech robotic phantom sequences:** Cortes et al., "Ultrasound Image Dataset for Image Analysis Algorithms Evaluation": tracked sequences of phantoms with robot arm and optical tracker, with spatial and force control; no links or terms on the [project page](https://www.vicomtech.org/demos/us_tracked_dataset/UsTrackedDataset.htm); "publicly available" per a search snippet of the [EAFIT record](https://repository.eafit.edu.co/handle/10784/29481). Unverified.
- **2026 robotic scanning preprints:** ForceU-VLA (450 expert trajectories with a six-axis force sensor; [arXiv 2608.15009](https://arxiv.org/pdf/2608.15009)) and US-VLA, "embodied abdominal" scanning (320 trajectories, about 80,000 timesteps; [arXiv 2608.16074](https://arxiv.org/pdf/2608.16074)); release not stated (search snippets). US-VLA would be HIGH PRIORITY if released. Unverified.
- **Also in other entries:** the paired robotic and handheld lumbar spine set (MSK).

#### 3D freehand reconstruction and probe tracking

##### TUS-REC2024 (Trackerless 3D Freehand Ultrasound Reconstruction Challenge 2024)
- **1-5:** Li, Saeed, Huang, Barratt, Clarkson, Hu (UCL), Vercauteren (KCL); train part 1, v1.0.0, 2024-05-12, DOI 10.5281/zenodo.11178509; MICCAI 2024. Forearms of volunteers, left and right; "1200 scans in total, 24 scans associated with each subject", 50 subject folders; frames 480 × 640 at 20 fps with a 4 × 4 transform per frame from an optical tracker; train_part1.zip 43.4 GB and calib_matrix.csv, md5 given — [Zenodo API](https://zenodo.org/api/records/11178509). Train part 2: [Zenodo 11180795](https://zenodo.org/records/11180795); validation: [doi:10.5281/zenodo.12979481](https://zenodo.org/doi/10.5281/zenodo.12979481) (72 scans; search snippet).
- **6:** Ultrasonix machine (BK) with a 4DC7-3/40 curvilinear probe.
- **7-10:** Zenodo, open, CC BY-NC-SA 4.0; tier A.
- **14:** Part 1 verified at the Zenodo API on 2026-11-25; parts 2 and validation from search snippets.

##### TUS-REC2025
- **1-5:** Train set, v1.0.0, 2025-04-28, DOI 10.5281/zenodo.15224704: "100 scans in total, 2 scans associated with each subject, around 1600 frames for each scan", 50 subjects ([Zenodo API](https://zenodo.org/api/records/15224704)). The challenge describes 85 volunteers and 170 scans with more rotation and tilt; split 50, 3 and 32 subjects (100, 6 and 64 scans; about 164k, 9k and 90k frames); optical tracker NDI Polaris Vicra; validation on [doi:10.5281/zenodo.15699958](https://doi.org/10.5281/zenodo.15699958); test set not released ([data page](https://github-pages.ucl.ac.uk/tus-rec-challenge/data.html)).
- **7-10:** Zenodo with restricted files; CC BY-NC-SA 4.0; use "within the research scope of this challenge", commercial use prohibited. Tier C.
- **14:** Verified at the Zenodo API and data page on 2026-11-25.

#### Image quality and enhancement

##### USenhance 2023 (Ultrasound Image Enhancement Challenge, MICCAI 2023). HIGH PRIORITY
- **1-5:** [ultrasoundenhance2023.grand-challenge.org](https://ultrasoundenhance2023.grand-challenge.org): five organs (thyroid, carotid artery, liver, breast, kidney); 3,000 images (1,500 pairs of low- and high-quality images) from 109 patients (search snippet of the page). The survey lists 2,464 images. Challenge design on [Zenodo 7841250](https://zenodo.org/records/7841250).
- **7-10:** Register on Grand Challenge, then sign the rule agreement form and e-mail it; the organisers send the training link; "currently only available for challenge use" (search snippet). Tier C.
- **11-13:** OpenUS uses it as a downstream task. Derivative below.
- **14:** Partly verified: from a search snippet of the challenge page (direct fetch of Grand Challenge pages returned HTTP 403).

##### USenhance2023_Aligned (derivative)
- [Hugging Face Jason0411202/USenhance2023_Aligned](https://huggingface.co/api/datasets/Jason0411202/USenhance2023_Aligned): pixel-aligned low- and high-quality pairs with 64 × 64 low-resolution copies (train and test folders; file names such as breast_1215.png); not gated; licence "other" ("usenhance2023-academic" in a LICENSE file); modified 2026-05-12. Tier A. Whether the organisers allowed this re-hosting is unknown. Verified 2026-11-25.

##### HFUS facial skin image quality
- See the skin entries (17,425 images, quality labels; host not found).

### Inferences
- Tier counts in Table 1 (my tally of 86 rows): A 45, A? 3, B 2, C or C? 11, D 7, not a download (link lists, indexes, rebuild scripts) 7, unknown 11. So about half of the census could be scripted into a cloud bucket without a user step, once the licence allows it.
- The largest open in-scope sources are RF and channel collections (Open-H-RF about 40 TB, ULMShare about 30 TB, PALA 55.65 GB, USTB 28.97 GB). They suit beamforming work, not B-mode segmentation training.
- For epic 1 (upper-abdomen anatomy segmentation) and epic 3 (liver diseases), the only large abdominal source in this scope is RadImageNet: about 259k abdominal frames (liver 78,535), about 13 times the project's 20k images. It is on request, has no stated licence, and has organ-level labels, not masks (labels per the US-JEPA table; not confirmed at the source).
- Image counts from videos overstate diversity: Regional-US gives 40,788 frames from 227 videos; Butterfly gives 41,076 images from 31 people. Splits and dedup must work by video or patient.
- Several Mendeley records carry CC BY 4.0, while the Mendeley site footer reserves rights "for text and data mining, AI training". The record licence should prevail for open content, but a legal check is prudent before bulk use.
- Non-commercial terms are common in 2024 to 2026 releases (TUS-REC, U2-Bench, LymphUs, UltraSuite, Regional-US, SA-Med2D-20M). That matters if any model trained on them is used commercially.

### Gaps
- **Not found, or no access route:** EASY-RESECT (no trace found); a public median nerve set (studies by Festen et al. 2021 with 5,560 images and others, none released: [PMC8169596](https://pmc.ncbi.nlm.nih.gov/articles/PMC8169596), search snippet); the femoral nerve block set (562 images); public salivary gland, dental and periodontal, RA synovitis, shoulder or rotator cuff, and forearm gesture US sets; the mouse GL261 repository; the repository of the paired lumbar spine set; the host of the HFUS facial image-quality set; LUMINOUS access; the ophthalmic report set's access; a vitreous haemorrhage set (446 images, Tel Aviv; [arXiv 2602.01444](https://arxiv.org/pdf/2602.01444), not public); the Alder Hey hip set ([arXiv 2211.04350](https://arxiv.org/pdf/2211.04350), no release seen); large neonatal cranial cohorts (an RSNA 2026 report and Stein et al. use private data; search snippets).
- **Dead links or blocked fetches (2026-11-25):** UBPD host (DNS failure); data.sonography.ai (timeout); FALLMUD page (TLS certificate error); Grand Challenge pages of CuRIOUS and USenhance (HTTP 403); cubdl.jhu.edu (HTTP 403); radiopaedia.org (HTTP 402); several PMC article pages (captcha); Kaggle competition pages (need JavaScript; the competitions API needs a login); nature.com (login redirect); ahudataset.github.io (HTTP 404).
- **Often cited, no access route found:** RadImageNet is on request only; EchoAtlas of EchoCare (4.5M images) has no download route; ReMUD is not yet released; USFM's corpus was not checked.
- **Not checked for lack of time:** Kaggle competition rules of the nerve set; the licence of the AD staging record; the SonoCorpus dataset list (Supplementary Table S1) and its dedup method (docs/DATA_SPLITS.md); MedSAM, BiomedParse, IMed-361M and MedSegBench US content; the GitHub USFM corpus; EPFL ultrafast datasets ([EPFL page](https://www.epfl.ch/labs/lts5/research/us/epfl-ultrafast-ultrasound-datasets/)); a Mendeley set "Demodulated IQ Ultrasound Data of Human Hand and Arm Tissue" ([Mendeley tm9tjpg542](https://data.mendeley.com/datasets/tm9tjpg542)); NVIDIA Holoscan scoliosis sample data ([NGC](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/clara-holoscan/resources/holoscan_ultrasound_sample_data)); a Dryad soleus fascicle set ([doi:10.5061/dryad.vq83bk3rp](https://datadryad.org/dataset/doi:10.5061/dryad.vq83bk3rp)); Project Imaging-X, a survey of 1000+ open datasets ([arXiv 2603.27460](https://arxiv.org/pdf/2603.27460)).
- **Roboflow:** none of the datasets above was found only on Roboflow. Roboflow was not searched (out of scope under DEC-081 and DEC-096, the epic 2 Roboflow scraper decisions).

## 2. Multi-organ collections and figure-mined sets: ultrasound counts, origin and licence

### Takeaway
Most multi-organ "collections" are link lists with converter scripts, not copies (US-43d, OpenUS, OpenUS-46, SonoCorpus, OPUS). Only a few re-host images: US30K (Google Drive), SA-Med2D-20M (2,968 US images, CC BY-NC-SA 4.0) and AHU (internet videos, CC BY 4.0). Among figure-mined sets, only ROCOv2 states a US count: 11,429 of 79,789 images (14.3%), each with its own article licence (CC BY or CC BY-NC). PMC-OA, PMC-15M, BIOMEDICA and MedTrinity-25M give no US count.

### Cited Findings

Table 2. Ultrasound content, origin and licence of multi-organ collections and figure-mined sets (n = number of images or frames as stated by each source)

| Collection | How it was built | Total (n) | US part (n) | Abdomen or liver part | Collection licence | Licence of the underlying images |
|---|---|---|---|---|---|---|
| RadImageNet | One outpatient facility, 2005-2020 | 1.35M (CT, MRI, US) | about 389,884 frames (secondary) | about 259k abdominal; liver 78,535 (secondary). HIGH PRIORITY | Not stated; on request | Same (institutional) |
| Butterfly MIT GrandHack 2018 | Butterfly iQ scans of 31 people | 41,076 | all | Morison's pouch, bladder, IVC classes. HIGH PRIORITY | Hackathon use only | Same |
| AHU | Internet videos of 31 creators, filtered and annotated | 1,833 items | all | Abdomen among organs. HIGH PRIORITY | CC BY 4.0 (figshare) | Creators' rights not addressed |
| US-43d | Links and converters for 43 public sets | over 280,000 masks | all | AbdomenUS and other abdomen sets | None stated | Each source's own |
| OpenUS | Links for 42 public sets | over 308K | all | AbdomenUS, ASUS, AUL, 105US, kidneyUS | Repo CC BY-NC 4.0 | Each source's own |
| OpenUS-46 | Links for 46 public sets | about 370,000 | all | Same kind | Sources keep theirs | Each source's own |
| SonoCorpus | Manifest, split indices, dedup hashes for 53 sets | 456,963 images, 1,626,085 masks | all | Not checked | Manifest CC BY 4.0 | Each source's own |
| OPUS (US-JEPA) | 50 public sets incl. RadImageNet | 5,123,697 frames | all | RadImageNet abdomen | Not stated | Each source's own |
| US30K | Re-packaged copy of 7 sets | about 30K | all | None | None stated | Each source's own |
| SA-Med2D-20M | Merge of public sets, 10 modalities | 4.6M | 2,968 | Not checked | CC BY-NC-SA 4.0 | Each source's own |
| EchoAtlas | 23 centres, 38 devices | 4.5M | all | Abdomen among 9 regions | Not stated | Not stated |
| ROCOv2 | PMC OA via FTP (archives to 2022-10-27); CC BY and CC BY-NC articles only | 79,789 | 11,429 (14.3%) | Not stated | No separate licence stated | Per image, in license_information.csv |
| PMC-OA | PMC OA as of 2022-09-16; subfigure alignment | 1.65M pairs | ? | ? | Not stated on HF | Per article |
| PMC-15M | PMC articles | 15,282,336 pairs | ? | ? | Scripts only | Per article |
| BIOMEDICA | PMC OA; 6,042,494 articles | 24,076,288 | ? | ? | Gated; per-article groups | Commercial (CC0, BY, BY-SA, BY-ND), non-commercial (BY-NC variants), other |
| MedTrinity-25M | Over 90 sources incl. PMC-OA and PMC-VQA | over 25M | ? | ? | ? | Each source's own |

- RadImageNet: 1.35 million CT, MRI and US images; on request — [GitHub README](https://github.com/BMEII-AI/RadImageNet); collection years and patients — [RSNA atlas card](https://atlas.rsna.org/cards/bb89e649-b6cc-47fb-9634-b087cc7c6df2) (search snippet); US frames by organ — [US-JEPA Table A.1](https://arxiv.org/html/2602.19322) (secondary).
- Butterfly terms and classes — [GitHub README](https://github.com/ButterflyNetwork/MITGrandHack2018); counts — [UltraBench wiki](https://github.com/adamtupper/ultrabench/wiki/Datasets).
- AHU sources: "derived from publicly available data on the Internet"; 31 video creators from hospitals in 16 provinces of China (search snippet of the paper); CC BY 4.0 on figshare — [figshare API](https://api.figshare.com/v2/articles/26889334).
- US-43d gives no licence and no download scripts — [GitHub](https://github.com/CAMMA-public/UltraSam). OpenUS lists sources with links; badge CC BY-NC 4.0 — [README](https://raw.githubusercontent.com/XZheng0427/OpenUS/main/README.md). OpenUS-46: "All datasets remain under their original licenses" — [GitHub](https://github.com/Yusufii9/USF-MAE). SonoCorpus: "no images or masks are re-hosted" — [GitHub](https://github.com/AlfredQin/sonobase).
- SA-Med2D-20M: US row of 2,968 images ([arXiv 2311.11969](https://arxiv.org/pdf/2311.11969), search snippet); HF licence CC BY-NC-SA 4.0, 352.8 GB — [HF API](https://huggingface.co/api/datasets/OpenGVLab/SA-Med2D-20M).
- ROCOv2: 11,429 images with the Ultrasonography concept (C0041618) of 79,789; split totals 59,958, 9,904 and 9,927; built from the full PMC OA subset via FTP; only CC BY-licensed articles (CC BY-NC included; CC BY-ND and CC BY-SA excluded); per-image licence and attribution in license_information.csv; Zenodo DOI 10.5281/zenodo.10821435 — [arXiv 2405.10004](https://arxiv.org/html/2405.10004v2). Older Zenodo versions carry a warning not to use them (search snippet of [Zenodo](https://zenodo.org/record/10821435)).
- PMC-OA: 1.65M image-text pairs from 2,478,267 papers and 12,211,907 extracted figure-caption pairs, PMC as of 2022-09-16 ([ar5iv 2303.07240](https://ar5iv.labs.arxiv.org/html/2303.07240), search snippet); HF repository not gated, no licence field, 37.6 GB — [HF API](https://huggingface.co/api/datasets/axiong/pmc_oa).
- PMC-15M: 15,282,336 image-caption pairs; models and reproduction scripts at aka.ms/biomedclip; ultrasound not named in the excerpts I saw — [arXiv 2303.00915](https://arxiv.org/abs/2303.00915v3) (search snippet).
- BIOMEDICA: 24,076,288 images and captions from 6,042,494 articles (5,050,473 with images) — [CVPR 2025 supplement](https://openaccess.thecvf.com/content/CVPR2025/supplemental/Lozano_BIOMEDICA_An_Open_CVPR_2025_supplemental.pdf) (search snippet); gated on HF with per-article licence groups; split as of June 2024: commercial 4.2M articles, non-commercial 1.6M, other 414k — [HF card](https://huggingface.co/datasets/BIOMEDICA/biomedica_webdataset_24M), [ETL repository](https://github.com/minwoosun/biomedica-etl) (search snippets).
- MedTrinity-25M: over 25 million images, 10 modalities, over 90 sources incl. PMC-OA and PMC-VQA; US appears only inside shared multi-modality rows — [arXiv 2408.02900](https://arxiv.org/abs/2408.02900v3) (search snippet).

### Inferences
- For figure-mined sets, the dataset licence is not the image licence. Each PMC figure keeps its article's licence; ROCOv2 shows this per image, and BIOMEDICA groups articles into commercial, non-commercial and "other" (no machine-readable licence). A copy in a private bucket for research is the least risky use; redistribution or commercial use needs per-image filtering.
- ROCOv2 is the only figure-mined set where a US subset can be selected without extra labelling (UMLS concept C0041618). Its 11,429 US figures are publication figures: often cropped, annotated, with arrows and calipers, sometimes multi-panel (an inference from the figure source; not reported by the authors).
- PMC-OA, PMC-15M, BIOMEDICA and MedTrinity-25M come from the same PMC OA pool, so the same US figure can appear in all of them (inference).
- AHU's CC BY 4.0 covers the authors' release; the rights of the original video creators are not addressed in the record. Treat it like scraped web content (inference).

### Gaps
- No US counts were found for PMC-OA, PMC-15M, BIOMEDICA or MedTrinity-25M. MedICaT, PubMedVision, Open-PMC and PMC-VQA were not checked.
- Whether the ROCOv2 Zenodo record holds the image files themselves was not checked.
- RadImageNet's own US counts, labels and terms were not found at the source.

## 3. Video libraries and teaching atlases: machine-learning use and bulk download

### Takeaway
None of the teaching atlases checked allows machine-learning use or bulk download. The POCUS Atlas is CC BY-NC 4.0 and silent on ML and bulk use. UltrasoundCases.info is all rights reserved, with personal non-commercial use only. Radiopaedia's terms (seen through a secondary source) say the site is not an ML dataset and not for bulk download. Open clinical video sets do exist, with explicit licences: ERDES (CC BY 4.0), AHU (CC BY 4.0, internet-sourced), UltraSuite and TaL (CC BY-NC 4.0), Regional-US (non-commercial DUA), TUS-REC (CC BY-NC-SA 4.0).

### Cited Findings

Table 3. Terms of teaching atlases and video libraries for machine-learning use (ML) and bulk download

| Library | In-scope content | Licence or terms | ML use stated | Bulk download | Tier |
|---|---|---|---|---|---|
| The POCUS Atlas | Image atlas (incl. aorta, biliary, GI, MSK, ocular, renal, soft tissue), nerve block atlas, paediatric atlas | CC BY-NC 4.0 | Not addressed | No route | D (C if the team grants permission) |
| UltrasoundCases.info | 10 categories incl. abdomen, head and neck, MSK, nerves | Copyright; reproduction needs SonoSkills' permission; personal non-commercial download only | Not addressed | Not allowed ("multiple distribution" prohibited) | D |
| Radiopaedia | Cases of all modalities | CC BY-NC-SA 3.0 as modified by the terms | Terms say not meant as an ML/AI dataset (secondary) | Not available (secondary) | D |
| Butterfly MIT GrandHack 2018 | 9 POCUS classes | Hackathon use only; no re-publishing | Not allowed beyond the hackathon | Links exist | D |
| ERDES | Ocular clips | CC BY 4.0 | Allowed by the licence | Yes (HF, Zenodo) | A |
| AHU | Mixed videos and images | CC BY 4.0 (creators' rights unclear) | Allowed by the licence | Yes (figshare) | A |
| UltraSuite and TaL | Tongue videos | CC BY-NC 4.0 | Non-commercial | Yes (rsync) | A |
| Regional-US | Brachial plexus videos | Non-commercial DUA | Non-commercial | Not stated | C |

- POCUS Atlas licence: "Our content is licensed under the Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)"; no text on ML, scraping or bulk download; questions go to the team's e-mail — [Legal page](https://www.thepocusatlas.com/legal). Categories from the site menus — [home page](https://www.thepocusatlas.com/).
- UltrasoundCases.info: "All images and content of this website are protected by copyright and may not be reproduced without permission of SonoSkills"; download for "personal, non-commercial use" only, with source and copyright notice; "Commercial reproduction or multiple distribution" prohibited; ML not mentioned — [FAQ](https://www.ultrasoundcases.info/more/faq/). SonoSkills took over the site in 2018; started in 2004 by Dr Taco Geertsma — [About](https://UltrasoundCases.info/more/about-us/) (search snippet).
- Radiopaedia: a Hugging Face discussion quotes the terms as saying the site is not meant as an ML/AI imaging dataset and is not available for bulk download; content is CC BY-NC-SA 3.0 as modified by the terms; use outside the licence needs prior written permission — [HF discussion](https://huggingface.co/datasets/GoodBaiBai88/M3D-Cap/discussions/1) (secondary); [radiopaedia.org/terms](https://radiopaedia.org/terms?lang=gb) returned HTTP 402 to my fetch.
- Butterfly terms — [GitHub README](https://github.com/ButterflyNetwork/MITGrandHack2018). ERDES — [project page](https://osupcvlab.github.io/ERDES). UltraSuite — [site](https://ultrasuite.github.io/). Regional-US — [GitHub](https://github.com/Regional-US/brachial_plexus).

### Inferences
- The POCUS Atlas and UltrasoundCases.info both hold abdomen and liver teaching material (HIGH PRIORITY content), but neither can be bulk-copied for training without the owners' written consent. Asking the POCUS Atlas team for permission is the realistic route; UltrasoundCases.info needs SonoSkills' permission.
- Datasets that already include atlas or Radiopaedia content carry those terms with them: open-hip-dysplasia (partly Radiopaedia images) and, in other organ groups, COVID lung video sets (not checked here).

### Gaps
- GrepMed's terms were not found. Other POCUS libraries (for example SonoWorld or university atlases) were not checked.
- Radiopaedia's terms were not read at the source (HTTP 402); the wording is from a secondary quote.

## 4. Subsets, re-releases, merges and known duplicates

### Takeaway
Overlap is heavy among the general collections: US-43d, OpenUS, OpenUS-46, SonoCorpus and OPUS point to the same public sources, and SonoCorpus publishes deduplication hashes and split indices that a dedup step could reuse. In this scope, the main parent-child chains are RESECT to RESECT-SEG to CuRIOUS, and ReMIND to ReMIND2Reg to Learn2Reg. RF data repeats across hosts (PICMUS in CREATIS, USTB and zea). The Kaggle nerve set has known inconsistent masks (a pruned 2,323-image subset).

### Cited Findings

Table 4. Known overlaps, re-releases and duplicates (relation of the first dataset to the others)

| Dataset | Relation | Other dataset or host | Evidence |
|---|---|---|---|
| FALLMUD | Merge, with added masks | Cunningham et al. set; Cronin set | [CEA page, search snippet](https://kalisteo.cea.fr/?p=3568) |
| RESECT-SEG | Labels on the same images | RESECT | [arXiv 2207.07494](https://arxiv.org/abs/2207.07494v1) |
| CuRIOUS 2018, 2019, 2022 | Challenge re-use | RESECT, RESECT-SEG | [CuRIOUS 2022 data page, snippet](https://curious2022.grand-challenge.org/data/) |
| ReMIND2Reg | Pre-processed subset (104 of 114 patients) | ReMIND (TCIA); Learn2Reg 2024 and 2025 task | [Zenodo](https://zenodo.org/api/records/11387725) |
| BITE groups 1 to 4 | Four views of one 14-patient set | BITE | [BITE page](https://nist.mni.mcgill.ca/?p=672) |
| Kaggle nerve set | Mirrors; pruned subset of 2,323 images without inconsistent masks | GitHub and Kaggle copies; "BP" and "US nerve Segmentation" in collections | [gcpds docs](https://gcpds-image-segmentation.readthedocs.io/en/latest/_modules/image_segmentation/datasets/segmentation/ultrasound_nerve_brachial_plexus.html) |
| UBPD | Same set under another name | "UPBD" in US-43d, OpenUS, OpenUS-46 | Same host URL in [OpenUS README](https://raw.githubusercontent.com/XZheng0427/OpenUS/main/README.md) |
| Regional-US | Frames of 227 videos | 40,788 frames in OpenUS | [GitHub](https://github.com/Regional-US/brachial_plexus); [OpenUS README](https://raw.githubusercontent.com/XZheng0427/OpenUS/main/README.md) |
| Butterfly | 41,076 frames of 31 people | UltraBench, OPUS | [UltraBench wiki](https://github.com/adamtupper/ultrabench/wiki/Datasets) |
| AbdomenUS | Real (617) and CT-simulated (926) parts | US-43d, OpenUS, OpenUS-46 | [Kaggle API](https://www.kaggle.com/api/v1/datasets/view/ignaciorlando/ussimandsegm) |
| Lung COVID phantom (Leeds) | Same set | "LUSS_phantom" in US-43d, OpenUS, OpenUS-46 | Same link in [OpenUS README](https://raw.githubusercontent.com/XZheng0427/OpenUS/main/README.md) |
| USenhance 2023 | Derivative re-host (aligned, 64 × 64) | Hugging Face USenhance2023_Aligned | [HF API](https://huggingface.co/api/datasets/Jason0411202/USenhance2023_Aligned) |
| PICMUS | Same acquisitions on three hosts | USTB Zenodo (UFF), zeahub/picmus (HF) | [USTB page](https://unioslo.github.io/USTB/datasets.html); [zea listing](https://huggingface.co/api/datasets?author=zeahub&limit=100) |
| ERDES | Same release on two hosts | HF and Zenodo | [project page](https://osupcvlab.github.io/ERDES) |
| DL_Track_US | Two copies | Zenodo v1.2 and OSF 7mjsc | [Zenodo API](https://zenodo.org/api/records/7866598) |
| Neonatal 3D US | Several versions under one concept DOI | Zenodo 14917169 and 19555871 | [Zenodo API](https://zenodo.org/api/records/19555871) |
| Porcine spinal cord | Fork with the same data | avishakumar21 repository | [GitHub](https://github.com/HEPIUSLAB/ultrasound_spinal_cord_dataset) |
| open-hip-dysplasia | Contains Radiopaedia images | Radiopaedia cases | [arXiv 2504.06422](https://arxiv.org/html/2504.06422v2) |
| UUSIC 2025 and UUSIVC 2026 | Built from public sets plus private data | BUSI, BUSIS, BUS-BRA, DDTI, Fatty-Liver, KidneyUS, HC18, CAMUS, appendicitis set | [UUSIC 2025](https://uusic2025.github.io) |
| SA-Med2D-20M, US30K | Re-packaged copies of public sets | Their sources | [HF API](https://huggingface.co/api/datasets/OpenGVLab/SA-Med2D-20M); [SAMUS](https://github.com/xianlin7/SAMUS) |
| US-43d, OpenUS, OpenUS-46, SonoCorpus, OPUS | Overlapping link lists of the same public sources | Each other | READMEs above |
| ROCOv2, PMC-OA, PMC-15M, BIOMEDICA, MedTrinity-25M | Mined from the same PMC OA pool; MedTrinity includes PMC-OA and PMC-VQA | Each other | [arXiv 2405.10004](https://arxiv.org/html/2405.10004v2); [arXiv 2408.02900](https://arxiv.org/abs/2408.02900v3) |
| STMUS_NDA and FSHD Heckmatt set | Same research group (possible shared patients) | Each other | [Mendeley 2021](https://data.mendeley.com/datasets/3jykz7wz8d/1); [Mendeley 2025](https://data.mendeley.com/datasets/yzg86vb895/1) |
| TUS-REC2024 and TUS-REC2025 | Same lab, device and anatomy; new scans in 2025 | Each other | [TUS-REC data page](https://github-pages.ucl.ac.uk/tus-rec-challenge/data.html) |

- SonoCorpus releases "deduplication hashes" and "data-split indices"; the method is in docs/DATA_SPLITS.md of the repository (not read); counts of duplicates are not in the README — [GitHub](https://github.com/AlfredQin/sonobase); manifest [doi:10.5281/zenodo.22770825](https://doi.org/10.5281/zenodo.22770825).
- UMUD only indexes metadata; it states no re-hosting, but it offers three labelled training sets taken from published papers — [UMUD PDF](https://jyx.jyu.fi/bitstreams/ee8f740d-8d88-45e1-a942-b40a87cfdd18/download).

### Inferences
- For the later dedup step, reuse SonoCorpus's hashes and split indices for the 53 sets it covers, and dedup by source dataset before merging collections. Treat US-43d, OpenUS and OpenUS-46 as lists of sources, never as extra data.
- Within-dataset near-duplicates are certain for any video-derived set (Regional-US, Butterfly, ERDES clips, TUS-REC frames, Lung COVID phantom frames). Group by video or patient when splitting.
- The BraTioUS USA site and ReMIND (also Boston) may share patients; nothing in the records rules it out (inference only).

### Gaps
- No duplicate counts were found for any collection.
- The CuRIOUS test-set sources and TUS-REC subject overlap between years were not found.

#### Seen, other groups (not researched; listed for the other researchers)
- **Breast:** BUSI, BUS-BRA, BrEaST (TCIA), BUID, BUS_UC, BUS_UCML, BUS Dataset B, S1, STU-Hospital, TN5000 is thyroid (below) — links in the [OpenUS README](https://raw.githubusercontent.com/XZheng0427/OpenUS/main/README.md); plane-wave breast phantom raw data ([Zenodo 7986407](https://doi.org/10.5281/zenodo.7986407)) and a USCT breast simulation ([Zenodo 7876210](https://doi.org/10.5281/zenodo.7876210)).
- **Thyroid:** DDTI, TN3K, TG3K, TNSCUI, Segthy, Stanford thyroid cine-clips (AIMI), TN5000 — [OpenUS README](https://raw.githubusercontent.com/XZheng0427/OpenUS/main/README.md); [US-JEPA](https://arxiv.org/html/2602.19322).
- **Heart, lung and vessels:** CAMUS, EchoNet-Dynamic, EchoNet-Pediatric, CardiacUDC, EchoCP, CACTUS, CCAUI (carotid), POCUS COVID set (Born et al.), COVID-BLUES, COVIDx-US ([GitHub](https://github.com/nrc-cnrc/covid-us)), MIMICEchoQA ([PhysioNet](https://www.physionet.org/content/mimic-iv-ext-echoqa/)), EchoVQA, DehazingEcho2025 and CETUS (zea), MICCAI 2026 mitral valve challenge — [OpenUS-46 list](https://github.com/Yusufii9/USF-MAE).
- **Fetal, obstetric and gynaecologic:** ACOUSLIC-AI, HC18, FH-PS-AOP, PSFHS, JNU-IFM, DFHI, FASS, Fast-U-Net, FEFT, Fetal_Planes_DB, IUGC 2024 and 2025, FU_Biometry (MICCAI 2026), FUSEP ([arXiv 2608.04766](https://arxiv.org/pdf/2608.04766)), FETAL-GAUGE ([arXiv 2512.22278](https://arxiv.org/abs/2512.22278v1)), NatalIA PBF-US1 fetal phantom ([Zenodo 14193949](https://doi.org/10.5281/zenodo.14193949)), FPUS23, MMOTU (ovary) — [OpenUS-46 list](https://github.com/Yusufii9/USF-MAE).
- **Abdomen and urology:** 105US and AUL (liver), Fatty Liver (Byra et al.), GBCU and GBUSV (gallbladder), GIST514-DB (endoscopic US), kidneyUS / Open Kidney, MicroSeg and regPro (prostate), ASUS (listed as abdomen, 2,865 images, linked to SlicerIGT/aigt; not checked), the Regensburg paediatric appendicitis set, an "Abdominal Ultrasound Image Dataset" on Academic Torrents ([link](https://academictorrents.com/details/fb252da63e5ba59bea91821018e5c83d172346ba)) — [OpenUS README](https://raw.githubusercontent.com/XZheng0427/OpenUS/main/README.md); [UltraBench wiki](https://github.com/adamtupper/ultrabench/wiki/Datasets).
