# Fetal, obstetric and gynaecologic ultrasound datasets: census as of 2026-11-25

Scope: public or published ultrasound datasets of the fetus, pregnancy, labour, cervix, placenta and
gynaecology (ovary, uterus, endometrium, pelvic floor, adnexa). Written for planning an automated
download into a private cloud bucket (epic 4 of the project: public ultrasound datasets). No dataset,
image or video was downloaded or opened; only landing pages, papers and metadata JSON were read.

Method (2026-11-25 to 2026-11-26):
- Zenodo search API, 64 queries (24 broad queries x 2 pages, 40 specific queries x 1 page; guest page
  size is 25). Record JSON (licence, files, sizes, md5) read for every relevant hit.
- Hugging Face datasets API, 20 name queries; dataset cards and file trees of the relevant ones.
- figshare search API, 17 queries; article JSON for the relevant ones.
- Mendeley Data public API for 2 records; Europe PMC for paper lookups; open full texts on PMC.
- Two curated lists: the npj Digital Medicine 2025 catalogue (72 public ultrasound datasets,
  [PMC12722232](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/)) and the GitHub atlas
  [TIanCat/open-medical-ultrasound-datasets](https://github.com/TIanCat/open-medical-ultrasound-datasets);
  a review of fetal-dataset biases ([PMC12166052](https://pmc.ncbi.nlm.nih.gov/articles/PMC12166052/));
  the UltraSam US-43d table ([CAMMA-public/UltraSam](https://github.com/CAMMA-public/UltraSam)).
- The run was cut short by a token budget. Kaggle, Science Data Bank, Grand Challenge archive pages and
  several gynaecology candidates were not checked at source; they are marked "unverified" or listed
  under Gaps.

Legend:
- Access level: open direct link / free account / click-through terms / data use agreement (DUA) with
  manual approval / credentialed / on request by email / closed or dead link.
- Automation tier (download from a cloud server): **A** scriptable with no login; **B** scriptable with
  a token or cookie the user supplies once; **C** needs a manual step by the user (form, approval,
  captcha, click-through); **D** not automatable.
- "Verified at URL on date" means the fact was read at that primary page or API on that date.
  "Secondary" means read only in a list or review. "Unverified" means not checked at any source in
  this run. "Inference" marks my own reasoning.
- GB = decimal gigabytes (1e9 bytes) as reported by the host API.

## Summary table

Table 1. All 43 datasets found, one row each. "Images / videos" is the count stated at the source
(secondary counts are marked). GB is the size of the files on the host. Automation tier A to D as in
the legend. A dash means not applicable.

| # | Name | Anatomy | Images / videos | GB | Host | Access level | Licence | Auto |
|---|---|---|---|---|---|---|---|---|
| 1 | HC18 | fetal head (head circumference) | 1,334 images | 0.18 | Zenodo (+ Grand Challenge) | open direct link | CC BY 4.0 | A |
| 2 | FETAL_PLANES_DB | fetal standard planes + maternal cervix | 12,400 images | 2.09 | Zenodo | open direct link | CC BY 4.0 | A |
| 3 | African fetal planes (MFUSPAC) | 4 fetal planes | 450 images (secondary) | 0.04 | Zenodo | open direct link | CC BY 4.0 | A |
| 4 | FASSD (fetal abdominal structures) | fetal abdomen | ~1,500 or 1,588 images | unknown | Mendeley Data | open direct link | CC BY 4.0 | A (not tested) |
| 5 | ACOUSLIC-AI 2024 | fetal abdomen, blind sweeps | 300 cases, ~252,000 frames (secondary) | 38.03 | Zenodo (+ Grand Challenge, test hidden) | open direct link | CC BY-NC-SA 4.0 | A |
| 6 | Multicentre-Fetal-Biometry (UCL, 2026) | head, abdomen, femur landmarks | 4,513 images | 1.59 | UCL Research Data Repository (figshare) | open direct link | CC BY-NC-SA 4.0 | A |
| 7 | Pixel-to-millimetre fetal head planes | fetal brain planes | 2,835 images | 0.93 | Zenodo | open direct link | CC BY 4.0 | A |
| 8 | Large-scale fetal head biometry annotations (2023) | fetal head | unknown | unknown | unknown | unknown | unknown | unverified |
| 9 | 2D foetal brain benchmark (2024) | fetal brain | 104 images | unknown | not found | unknown | unknown | unknown |
| 10 | FOCUS | fetal heart four-chamber view | 300 images | 0.06 | Zenodo | open direct link | CC BY 4.0 | A |
| 11 | DELTA (2026) | fetal echocardiography, heart disease | 3,760 images + 752 videos | 6.94 | figshare | open direct link | CC BY 4.0 | A |
| 12 | FetalCHD-MV (2026) | fetal echocardiography | no images on host (1 JSON file) | 0.001 | Hugging Face | open (no image data) | CC BY 4.0 / CC BY-NC 4.0 (two repos) | gap |
| 13 | Dataset for Fetus Framework | first trimester (11-14 weeks), nuchal translucency | 1,528 + 156 images | unknown | Mendeley Data | open direct link | CC BY 4.0 | A (not tested) |
| 14 | FUSEP (2026) | first trimester, CRL and NT views | 4,017 images | unknown | not found | unknown | unknown | unknown |
| 15 | CRL_NT (named by FADA) | crown-rump length, nuchal translucency | unknown | unknown | Mendeley Data (not located) | unknown | unknown | unknown |
| 16 | JNU-IFM | pubic symphysis + fetal head (transperineal) | 6,224 frames / 78 videos | 1.79 | figshare | open direct link | CC BY 4.0 | A |
| 17 | PSFHS | pubic symphysis + fetal head | 1,358 images | 0.13 | Zenodo | open direct link | CC BY 4.0 | A |
| 18 | PS-FH-AOP 2023 challenge | = #16 + #17 | - | - | Grand Challenge; Zenodo restricted copy | DUA with manual approval (Zenodo request) | CC BY 4.0 | C (use #16, #17: A) |
| 19 | IUGC 2024 challenge | intrapartum images and videos, AoP, HSD | unknown | unknown | Codalab | free account (unverified) | unknown | C (unverified) |
| 20 | Maternal-Fetal Ultrasound Video Dataset (2026) | intrapartum | 774 videos / 68,106 frames | 1.08 | Zenodo | open direct link | CC BY 4.0 | A |
| 21 | IUGC 2025 dataset | intrapartum landmarks | 28,919 images and videos (stated) | 1.07 | Zenodo | open direct link | CC BY 4.0 | A |
| 22 | IUGC 2025 add-on (Lanzhou) | intrapartum landmarks | 169 images | 0.03 | Zenodo | open direct link | CC BY 4.0 | A |
| 23 | FUGC 2025 (ISBI) | cervix, transvaginal | 890 images (500/90/300) | unknown | Zenodo record + email | DUA with manual approval | CC BY 4.0 (record) | C |
| 24 | FUGC pseudo-label set (2026) | cervix, transvaginal | unknown | 3.46 | Zenodo | open direct link | CC BY 4.0 | A |
| 25 | A-AFMA (ISBI 2021) | amniotic fluid, maternal bladder (video) | unknown | unknown | Zenodo (restricted) | closed | none; challenge use only | D |
| 26 | NatalIA PBF-US1 | fetal phantom, blind sweeps | unknown | 0.27 | Zenodo | open direct link | CC BY 4.0 | A |
| 27 | FPUS23 | fetal phantom | 15,728 images | unknown | Google Drive (via GitHub) | open direct link | none stated | A (fragile) |
| 28 | FU-LoRA synthetic | synthetic fetal planes | 5,000 (from file name) | 2.06 | Zenodo | open direct link | CC BY 4.0 | A |
| 29 | FADA (2026) | text descriptions of 18,935 public fetal images | 56,805 conversations | unknown | Zenodo (restricted) + GitHub | on request (Zenodo restricted) | none stated | C |
| 30 | Ultrasound Fetus Dataset (2024) | unclear (normal/benign/malignant) | unknown | ~0.64 (Kaggle mirror, unverified) | Mendeley Data | open (unverified) | unknown | unverified |
| 31 | Anal atresia case series | prenatal anomaly | unknown | unknown | Mendeley Data | unverified | unknown | unverified |
| 32 | "dataset for ultrasound pregnancy investigation" (2021) | unclear | unknown | 0.11 | Zenodo | open direct link | CC BY 4.0 | A (content unknown) |
| 33 | MMOTU | ovarian tumours (2D + contrast-enhanced) | 1,639 images | unknown | Google Drive (via GitHub) | open direct link | none stated | A (fragile) |
| 34 | MMOTU 2D curated copy (2026) | ovarian tumours | 1,469 images | 0.14 | Zenodo | open direct link | CC BY 4.0 (uploader) | A |
| 35 | PCOSGen (Auto-PCOS 2024) | ovary, polycystic ovary | 4,668 images | 0.09 | Zenodo | open direct link | CC BY 4.0 | A |
| 36 | PCOS Dataset (figshare 27682557) | polycystic ovary | 12,680 images (secondary) | unknown | figshare | unverified | unverified | unverified |
| 37 | Ovarian Ultrasound Image Dataset (Kaggle) | ovary | 6,879 images (secondary) | unknown | Kaggle | free account | unverified | B |
| 38 | PCOS "infected / notinfected" (Kaggle origin, HF mirror) | polycystic ovary | 1,924 images (HF mirror) | 0.07 | Hugging Face mirror | open direct link | none stated | A (mirror) |
| 39 | Polycystic ovary ultrasound images dataset | ovary | 54 images (secondary) | unknown | unknown | open (secondary) | unknown | unverified |
| 40 | UFUV (LGRNet, MICCAI 2024) | uterine fibroids, video | unknown | 1.59 | Hugging Face | open direct link | MIT | A |
| 41 | PFUS1 | pelvic floor, midsagittal | 110 patients (frame count unknown) | 5.81 | Zenodo | open direct link | CC BY 4.0 | A |
| 42 | UterUS (3D uterus) | uterus, 3D transvaginal | unknown | unknown | unverified | unverified | unverified | unverified |
| 43 | Clinical Ultrasound Image Repository (AWS) | multi-anatomy incl. OB/GYN | 2,000 studies (secondary) | unknown | AWS Registry of Open Data | unverified | unverified | unverified |

## Detailed entries

Each entry gives the 14 requested fields: 1 name/year/paper; 2 content; 3 data type; 4 size; 5 labels;
6 source; 7 where (host, version, checksums); 8 access; 9 licence; 10 automation; 11 overlaps;
12 burned-in text; 13 large-scale use; 14 verification.

### A. Fetal biometry, standard planes, fetal brain

#### 1. HC18 (Automated measurement of fetal head circumference)
1. HC18; 2018; van den Heuvel et al., PLOS ONE, [doi:10.1371/journal.pone.0200412](https://doi.org/10.1371/journal.pone.0200412).
2. Fetal head in the standard head-circumference plane; first, second and third trimester ([PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0200412)).
3. 2D B-mode still images, 800 x 540 pixels, pixel size 0.052 to 0.326 mm ([PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0200412)).
4. 1,334 images (999 training, 335 test) from 551 pregnant women; 0.176 GB on Zenodo (training_set.zip 0.133 GB, test_set.zip 0.044 GB, two CSV files) ([Zenodo API](https://zenodo.org/records/1327317)).
5. Ellipse of the head circumference drawn by an experienced sonographer; a second observer annotated the test set; HC in mm and pixel size in a CSV for training ([PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0200412)). Test CSV holds pixel size only (file names on [Zenodo](https://zenodo.org/records/1327317)), so test labels stay hidden behind the challenge evaluation (inference).
6. Radboud University Medical Center, Nijmegen, the Netherlands; Voluson E8 or Voluson 730 (GE); May 2014 to May 2015 ([PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0200412)).
7. Zenodo record 1327317, DOI [10.5281/zenodo.1327317](https://doi.org/10.5281/zenodo.1327317) (concept record 1322000); md5 published for all 4 files; challenge page [hc18.grand-challenge.org](https://hc18.grand-challenge.org/). Mirrors on Hugging Face: [MedOtter/HC18](https://huggingface.co/datasets/MedOtter/HC18), [harshalbhansali/HC18](https://huggingface.co/datasets/harshalbhansali/HC18) (target Zenodo).
8. Open direct link.
9. CC BY 4.0 (Zenodo record). No other terms stated.
10. A.
11. Reused in #6 Multicentre-Fetal-Biometry (landmarks derived from the HC18 ellipses) ([UCL RDR](https://rdr.ucl.ac.uk/articles/dataset/A_multi-centre_multi-device_benchmark_dataset_for_landmark-based_comprehensive_fetal_biometry/30819911)) and in #29 FADA ([Zenodo](https://zenodo.org/records/20381238)). Several images per examination exist; the paper kept one examination in one split ([PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0200412)).
12. Not stated in the paper ("anonymized"; no cropping described) ([PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0200412)).
13. UltraSam US-43d ("HC") ([UltraSam README](https://github.com/CAMMA-public/UltraSam)); Multicentre-Fetal-Biometry; FADA. Others (SAMUS US30K, MedSAM, SA-Med2D-20M, FetalCLIP): unverified.
14. Verified at https://zenodo.org/records/1327317 on 2026-11-25 and https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0200412 on 2026-11-26.

#### 2. FETAL_PLANES_DB (Common maternal-fetal ultrasound images)
1. FETAL_PLANES_DB; 2020; Burgos-Artizzu et al., Scientific Reports 10:10200, [doi:10.1038/s41598-020-67076-5](https://doi.org/10.1038/s41598-020-67076-5) (open: [PMC7311420](https://pmc.ncbi.nlm.nih.gov/articles/PMC7311420/)).
2. Six classes: fetal abdomen, brain, femur, thorax, maternal cervix, "other"; brain split into trans-thalamic, trans-cerebellum, trans-ventricular ([Zenodo](https://zenodo.org/records/3904280)). Second and third trimester ([PMC12166052](https://pmc.ncbi.nlm.nih.gov/articles/PMC12166052/)).
3. 2D B-mode still images (routine screening).
4. 12,400 images from 1,792 patients ([PMC12166052](https://pmc.ncbi.nlm.nih.gov/articles/PMC12166052/); 12,400 also in [PMC12722232](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/)); one zip of 2.089 GB ([Zenodo API](https://zenodo.org/records/3904280)).
5. Plane class per image, labelled by one expert maternal-fetal clinician; meta data (patient number, machine, operator) and the paper's train/test split ([Zenodo](https://zenodo.org/records/3904280)).
6. BCNatal (Hospital Clinic and Hospital Sant Joan de Deu, University of Barcelona), Spain ([Zenodo](https://zenodo.org/records/3904280)). Devices: text of the bias review lists 6 machines (3 Voluson E6, 1 Voluson S8, 1 Voluson S10, 1 Aloka); its Table 1 says 4 ([PMC12166052](https://pmc.ncbi.nlm.nih.gov/articles/PMC12166052/)).
7. Zenodo record 3904280, DOI [10.5281/zenodo.3904280](https://doi.org/10.5281/zenodo.3904280), version 1.0; md5 published. Hugging Face mirrors (target Zenodo): [chehablab/FETAL_PLANES_DB](https://huggingface.co/datasets/chehablab/FETAL_PLANES_DB), [Emulated-Inc/sci-fetal-planes-low-resource](https://huggingface.co/datasets/Emulated-Inc/sci-fetal-planes-low-resource) (same files in tar shards, sha256 list), [qingyuyang/Fetal_Planes_DB](https://huggingface.co/datasets/qingyuyang/Fetal_Planes_DB), [shr3m/fetal-planes-db](https://huggingface.co/datasets/shr3m/fetal-planes-db) (gated), and several others.
8. Open direct link.
9. CC BY 4.0 (Zenodo record).
10. A.
11. Same group as #3 (separate African images). "Fetal Plane (FP) dataset" images reused in #6 ([UCL RDR](https://rdr.ucl.ac.uk/articles/dataset/A_multi-centre_multi-device_benchmark_dataset_for_landmark-based_comprehensive_fetal_biometry/30819911)); #7 (2,835 head-plane images) is probably drawn from its brain classes (inference, unverified). Many images per patient: split by the patient number to avoid leakage (inference; a Hugging Face repo named [fetal-plane-leakage-audit](https://huggingface.co/datasets/AliMusaRizvi/fetal-plane-leakage-audit) exists, content unverified).
12. Unknown. The bias review excluded datasets with identifying information on frames and still included this one ([PMC12166052](https://pmc.ncbi.nlm.nih.gov/articles/PMC12166052/)); that suggests no patient text, but does not exclude calipers or machine text (inference).
13. #6 Multicentre-Fetal-Biometry. Not in the UltraSam US-43d table ([UltraSam README](https://github.com/CAMMA-public/UltraSam)); likely because it has class labels and no masks (inference). FetalCLIP and others: unverified.
14. Verified at https://zenodo.org/records/3904280 on 2026-11-25; details at https://pmc.ncbi.nlm.nih.gov/articles/PMC12166052/ (secondary review) on 2026-11-25.

#### 3. African fetal planes (Maternal fetal ultrasound planes from low-resource imaging settings in five African countries; MFUSPAC)
1. 2023; Sendra-Balcells et al., Scientific Reports, [doi:10.1038/s41598-023-29490-3](https://doi.org/10.1038/s41598-023-29490-3) (open: [PMC9932015](https://pmc.ncbi.nlm.nih.gov/articles/PMC9932015/)); preprint [arXiv 2209.09610](https://arxiv.org/abs/2209.09610).
2. Four fetal planes: abdomen, brain, femur, thorax ([Zenodo](https://zenodo.org/records/7540448)).
3. 2D B-mode still images.
4. 450 images from 125 patients, 25 patients per site ([PMC12166052](https://pmc.ncbi.nlm.nih.gov/articles/PMC12166052/); same in [TIanCat atlas](https://github.com/TIanCat/open-medical-ultrasound-datasets)); one tar.xz of 0.043 GB ([Zenodo API](https://zenodo.org/records/7540448)).
5. Plane class, patient number and train/test split in a CSV ([Zenodo](https://zenodo.org/records/7540448)).
6. Malawi, Egypt, Uganda, Ghana, Algeria; devices Mindray DC-N2, Voluson P8, ACUSON X600, EDAN DUS 60, Voluson S8 ([PMC12166052](https://pmc.ncbi.nlm.nih.gov/articles/PMC12166052/)).
7. Zenodo record 7540448, DOI [10.5281/zenodo.7540448](https://doi.org/10.5281/zenodo.7540448), version v1.0; md5 published.
8. Open direct link. 9. CC BY 4.0. 10. A.
11. Companion of #2 (same group, different images, inference). #28 FU-LoRA synthetic images were evaluated on "African cohorts" ([Zenodo](https://zenodo.org/records/13228158)).
12. Unknown.
13. Unknown.
14. Verified at https://zenodo.org/records/7540448 on 2026-11-25; counts secondary (PMC12166052).

#### 4. FASSD (Fetal Abdominal Structures Segmentation Dataset Using Ultrasonic Images)
1. 2023 (published 2023-10-18); no paper given on the record; Mendeley DOI [10.17632/4gcpm9dsc3.1](https://doi.org/10.17632/4gcpm9dsc3.1).
2. Fetal abdominal circumference plane; structures listed by the npj catalogue: fetal abdomen, liver, stomach, aorta, spine, intrahepatic umbilical vein ([PMC12722232](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/)). Term pregnancies, including labour induction, caesarean, gestational diabetes, pre-eclampsia, growth restriction ([Mendeley API](https://data.mendeley.com/datasets/4gcpm9dsc3/1)).
3. 2D B-mode still images.
4. "Nearly 1500" images from 169 subjects ([Mendeley](https://data.mendeley.com/datasets/4gcpm9dsc3/1)); 1,588 in the npj catalogue ([PMC12722232](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/)) and the [TIanCat atlas](https://github.com/TIanCat/open-medical-ultrasound-datasets); 1,500 in the bias review table ([PMC12166052](https://pmc.ncbi.nlm.nih.gov/articles/PMC12166052/)). Download size unknown.
5. Segmentation masks of abdominal structures (secondary: PMC12722232); two sonographers ([PMC12166052](https://pmc.ncbi.nlm.nih.gov/articles/PMC12166052/)).
6. University Hospital Polydoro Ernani de Sao Thiago, Florianopolis, Brazil; September 2021 to September 2023 ([Mendeley](https://data.mendeley.com/datasets/4gcpm9dsc3/1)); Siemens Acuson, Voluson 730, Philips EPIQ Elite ([PMC12166052](https://pmc.ncbi.nlm.nih.gov/articles/PMC12166052/)).
7. Mendeley Data, version 1. Checksums: unknown.
8. Open direct link (Mendeley public dataset).
9. CC BY 4.0 ([Mendeley API](https://data.mendeley.com/datasets/4gcpm9dsc3/1)).
10. A (Mendeley public files; scripted download not tested).
11. Used as a source by #29 FADA ("Fetal Abdominal Structures") ([Zenodo](https://zenodo.org/records/20381238)). Probably the "FASS" set in UltraSam US-43d (inference from the name).
12. Unknown.
13. UltraSam US-43d lists "FASS" ([UltraSam README](https://github.com/CAMMA-public/UltraSam)); FADA.
14. Verified at https://data.mendeley.com/datasets/4gcpm9dsc3/1 (public API) on 2026-11-26.

#### 5. ACOUSLIC-AI 2024 (Abdominal Circumference Operator-agnostic UltraSound measurement in Low-Income Countries)
1. MICCAI 2024 challenge; paper Sappia et al. 2025, Medical Image Analysis, [doi:10.1016/j.media.2025.103640](https://doi.org/10.1016/j.media.2025.103640) (from the TIanCat atlas; not opened).
2. Fetal abdomen; abdominal circumference ([Zenodo](https://zenodo.org/records/12697994)).
3. 2D B-mode blind-sweep cine sequences acquired by novice operators with a fixed protocol ([Zenodo](https://zenodo.org/records/12697994)).
4. 300 public cases, about 252,000 frames (secondary: [TIanCat atlas](https://github.com/TIanCat/open-medical-ultrasound-datasets)); the npj catalogue gives 600 (likely training plus test, inference) ([PMC12722232](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/)). One zip of 38.034 GB ([Zenodo API](https://zenodo.org/records/12697994)).
5. Abdomen masks in frames where AC can be measured; reference AC in mm per sweep. Version 1.1 fixed AC values that were 2x too large in version 1.0 ([Zenodo](https://zenodo.org/records/12697994)). Only the training set is on Zenodo (one file, acouslic-ai-train-set.zip), so the test set stays with Grand Challenge (inference; the challenge dataset page refused automated access, HTTP 403).
6. Creator Radboud University Medical Center ([Zenodo](https://zenodo.org/records/12697994)); acquisition countries and devices: unverified.
7. Zenodo record 12697994, DOI [10.5281/zenodo.12697994](https://doi.org/10.5281/zenodo.12697994), version 1.1 (concept 11005383); md5 published. Challenge: [acouslic-ai.grand-challenge.org](https://acouslic-ai.grand-challenge.org/). Proposal PDF: [Zenodo 10991270](https://zenodo.org/records/10991270).
8. Open direct link.
9. CC BY-NC-SA 4.0 (Zenodo): non-commercial, share-alike.
10. A (one 38 GB file).
11. Frames within one sweep are near-duplicates (inference). No cross-dataset overlap reported.
12. Unknown.
13. UltraSam US-43d ("ACOUSLIC") ([UltraSam README](https://github.com/CAMMA-public/UltraSam)).
14. Verified at https://zenodo.org/records/12697994 on 2026-11-25; frame count secondary.

#### 6. Multicentre-Fetal-Biometry (A multicentre benchmark dataset for comprehensive landmark-based fetal ultrasound biometry)
1. 2026 (version 2, 2026-06-29); Di Vece, Mao, Avisdris, Dromey, Napolitano, Ben Bashat, Vasconcelos, Stoyanov; DOI [10.5522/04/30819911.v2](https://doi.org/10.5522/04/30819911.v2). Paper: unknown.
2. Landmarks for BPD, OFD (head), TAD, APAD (abdomen), FL (femur) ([UCL RDR](https://rdr.ucl.ac.uk/articles/dataset/A_multi-centre_multi-device_benchmark_dataset_for_landmark-based_comprehensive_fetal_biometry/30819911)).
3. 2D B-mode standard planes.
4. 4,513 images, 1,904 subjects, 4 sites, 7 devices; one zip of 1.588 GB.
5. Landmark coordinates; pixel-to-mm factor, de-identified subject ID, anatomy, device ID, subject-disjoint split.
6. Derived from the "Fetal Plane (FP)" dataset, HC18 and a University College London Hospital set; GE Voluson E6, S8, S10, E8, 730 and Aloka.
7. UCL Research Data Repository (figshare platform), [record 30819911](https://rdr.ucl.ac.uk/articles/dataset/A_multi-centre_multi-device_benchmark_dataset_for_landmark-based_comprehensive_fetal_biometry/30819911); md5 published (figshare API).
8. Open direct link. 9. CC BY-NC-SA 4.0. 10. A.
11. Contains images of #1 HC18 and very probably #2 FETAL_PLANES_DB (the device list matches #1 plus #2; inference). Dedup against both is needed. The UCLH part is new.
12. "De-identified images" (record); burned-in text not described.
13. Unknown.
14. Verified at the figshare API for article 30819911 on 2026-11-25.

#### 7. Pixel-to-millimetre fetal head planes (Converting Pixel into millimeter in ultrasound images: Technique and dataset)
1. 2023; Alzubaidi (HBKU); Zenodo DOI [10.5281/zenodo.7193337](https://doi.org/10.5281/zenodo.7193337); conference paper not named on the record.
2. Three fetal head planes: trans-cerebellum, trans-thalamic, trans-ventricular; various gestational ages.
3. 2D B-mode still images.
4. 2,835 images; All-Fetal-Plane-Images.zip 0.933 GB plus a pixel-size CSV.
5. Pixel size in mm per image (mean 0.144 mm, range 0.060 to 0.330 mm).
6. Unknown (source of the images not stated on the record).
7. Zenodo record 7193337; md5 published.
8. Open direct link. 9. CC BY 4.0. 10. A.
11. Probably a subset of #2 FETAL_PLANES_DB brain planes (same three plane names; inference, unverified). Possibly related to #8 (same author).
12. Unknown. 13. Unknown.
14. Verified at https://zenodo.org/records/7193337 on 2026-11-25.

#### 8. Large-scale annotation dataset for fetal head biometry in ultrasound images
1. 2023; Alzubaidi et al., Data in Brief, [doi:10.1016/j.dib.2023.109708](https://doi.org/10.1016/j.dib.2023.109708) (open: [PMC10630602](https://pmc.ncbi.nlm.nih.gov/articles/PMC10630602/)).
2. to 14. Not read in this run (budget). Content, size, host, licence: unverified. Overlap with #2 and #7 is likely (same author as #7; inference). A Hugging Face repo [filipjovanovski1/Fetal_Head_Ultrasound](https://huggingface.co/datasets/filipjovanovski1/Fetal_Head_Ultrasound) (CC BY 4.0, 3,644 downloads, empty card) may be a mirror of a fetal head set (unverified).

#### 9. A benchmark for 2D foetal brain ultrasound analysis
1. 2024; Cabezas, Diez, Martinez-Diago, Maroto; [arXiv 2406.17250](https://arxiv.org/abs/2406.17250).
2. Fetal brain, 20th week of gestation.
3. 2D B-mode; original space plus a template space centred on the skull ellipse.
4. 104 images.
5. Landmark points of brain structures; probabilistic atlas template.
6. to 9. Institution, host and licence not stated on the arXiv page (arXiv paper licence CC BY 4.0 is the paper's, not the data's).
10. Unknown (no access route found).
11. to 13. Unknown.
14. Verified at https://arxiv.org/abs/2406.17250 on 2026-11-25 (abstract page only).

### B. Fetal heart and fetal echocardiography

#### 10. FOCUS (Four-chamber Ultrasound Image Dataset for Fetal Cardiac Biometric Measurement)
1. 2025 (record 2025-01-01); Wu, Zhang, Ye, Xie, Zeng, Sun; Zenodo DOI [10.5281/zenodo.14597550](https://doi.org/10.5281/zenodo.14597550); paper: unknown.
2. Fetal heart four-chamber view; cardiothoracic ratio for congenital heart disease screening.
3. 2D B-mode still images.
4. 300 images (217 patients, secondary: [TIanCat atlas](https://github.com/TIanCat/open-medical-ultrasound-datasets)); one zip of 0.061 GB.
5. Manual annotations of cardiac and thoracic regions (with an expert sonographer).
6. Unknown.
7. Zenodo record 14597550, version 1.0; md5 published.
8. Open direct link. 9. CC BY 4.0. 10. A.
11. Used as a source by #29 FADA.
12. Unknown.
13. FADA ([Zenodo](https://zenodo.org/records/20381238)).
14. Verified at https://zenodo.org/records/14597550 on 2026-11-25.

#### 11. DELTA (A Dual-Modality Fetal Echocardiography Dataset for Long-Tail Congenital Heart Disease Diagnosis)
1. 2026 (version 2, 2026-10-08); Zhang, Yao, Qian, Ye; figshare DOI [10.6084/m9.figshare.32358771.v2](https://doi.org/10.6084/m9.figshare.32358771.v2); paper: unknown.
2. Fetal heart: 752 cases (619 normal, 133 abnormal) covering 12 fetal congenital heart disease subtypes.
3. 2D B-mode still images of five standard screening planes plus one scan video per case.
4. 3,760 images and 752 videos; one zip of 6.940 GB.
5. Case-level diagnosis (normal or subtype); plane per image (inference from the description).
6. One high-volume tertiary centre (name and country not stated).
7. [figshare article 32358771](https://figshare.com/articles/dataset/DELTA_A_Dual-Modality_Fetal_Echocardiography_Dataset_for_Long-Tail_Congenital_Heart_Disease_Diagnosis/32358771); md5 published.
8. Open direct link. 9. CC BY 4.0. 10. A.
11. Unknown.
12. "Human-in-the-loop de-identification pipeline" (record); details unknown.
13. Unknown.
14. Verified at the figshare API for article 32358771 on 2026-11-25.

#### 12. FetalCHD-MV (A Fetal Echocardiography Dataset from a Multi-view Fusion Perspective)
1. 2026; two Hugging Face repos: [YuanZhao1230/FetalCHD-MV](https://huggingface.co/datasets/YuanZhao1230/FetalCHD-MV) (CC BY 4.0) and [dckkk/FetalCHD-MV](https://huggingface.co/datasets/dckkk/FetalCHD-MV) (CC BY-NC 4.0); paper: unknown.
2. Fetal echocardiography, congenital heart disease (from the title).
3. to 6. Unknown: the first repo holds only one JSON file (output_few_shot_final.json, 0.001 GB) and no images (HF file tree).
7. Hugging Face; no checksums beyond git LFS.
8. Open, but no image data found.
9. Conflicting: CC BY 4.0 vs CC BY-NC 4.0.
10. Not applicable until the images are located (gap).
11. to 13. Unknown.
14. Verified at https://huggingface.co/api/datasets/YuanZhao1230/FetalCHD-MV/tree/main on 2026-11-26.

### C. First trimester (nuchal translucency, crown-rump length)

#### 13. Dataset for Fetus Framework
1. 2022 (published 2022-09-21); Mendeley Data DOI [10.17632/n2rbrb9t4f.1](https://doi.org/10.17632/n2rbrb9t4f.1); paper: unknown.
2. First trimester (weeks 11 to 14), sagittal view; standard vs non-standard plane for NT measurement and Down syndrome assessment.
3. 2D B-mode still images.
4. 1,528 images of 1,519 women, plus an external test set of 156 images. Download size unknown.
5. Standard/non-standard class; boxes of nine structures (thalami, midbrain, palate, 4th ventricle, cisterna magna, nuchal translucency, nasal tip, nasal skin, nasal bone) in an Excel file.
6. Shenzhen People's Hospital, China; external set from its Longhua branch.
7. [Mendeley Data n2rbrb9t4f v1](https://data.mendeley.com/datasets/n2rbrb9t4f/1). Checksums unknown.
8. Open direct link. 9. CC BY 4.0. 10. A (not tested).
11. Possibly the "CRL_NT (Mendeley Data)" source cited by #29 FADA (unverified).
12. Unknown. 13. Unknown.
14. Verified at https://data.mendeley.com/datasets/n2rbrb9t4f/1 (public API) on 2026-11-26.

#### 14. FUSEP (A Multi-Center Benchmark for Diverse Tasks in Early Pregnancy Fetal Ultrasound Screening)
1. 2026-08-05; Pu, Yang, Wang, ... Li, Li; [arXiv 2608.04766](https://arxiv.org/abs/2608.04766).
2. Two first-trimester views: crown-rump length and nuchal translucency; 14 anatomical structures.
3. 2D B-mode still images.
4. 4,017 images; 45,820 box annotations; 3 hospitals.
5. Boxes; tasks: detection (supervised, semi-supervised, domain adaptation), plane recognition, quality control.
6. Hospitals, country and devices not stated on the abstract page.
7. No download link on the arXiv page, although the abstract calls it publicly available. #29 FADA lists "FUSEP (Fetal Brain Structures, Zenodo)" as a source, which does not match this description (conflict, unverified).
8. Unknown. 9. Unknown (arXiv CC BY 4.0 covers the paper only). 10. Unknown.
11. Source of #29 FADA (per FADA). 12. Unknown. 13. FADA.
14. Verified at https://arxiv.org/abs/2608.04766 on 2026-11-25 (abstract page only).

#### 15. CRL_NT (Mendeley Data)
Named only by #29 FADA as "CRL_NT (Crown-Rump Length / Nuchal Translucency, Mendeley Data)" ([Zenodo](https://zenodo.org/records/20381238)). Not located in this run; may be #13 (unverified). All other fields unknown.

### D. Intrapartum (labour, angle of progression)

#### 16. JNU-IFM (dataset for segmenting pubic symphysis-fetal head)
1. 2022; Lu et al., Data in Brief, [doi:10.1016/j.dib.2022.107904](https://doi.org/10.1016/j.dib.2022.107904) (open: [PMC8842023](https://pmc.ncbi.nlm.nih.gov/articles/PMC8842023/)).
2. Intrapartum transperineal view of pubic symphysis and fetal head.
3. 78 MP4 videos (1920 x 1080) and 6,224 frames (PNG, 1295 x 1026, grayscale).
4. 78 videos, 6,224 frames, 51 women; one zip of 1.791 GB plus readme ([figshare API](https://figshare.com/articles/dataset/JNU-IFM/14371652)).
5. Frame class (None 1,022; OnlySP 323; OnlyHead 1,136; SPHead 3,743); masks of symphysis pubis and fetal head; five students labelled, two radiologists reviewed.
6. NanFang Hospital of Southern Medical University, Guangzhou, China; Youkey D8 wireless probe; August 2019 to January 2020.
7. figshare DOI [10.6084/m9.figshare.14371652](https://doi.org/10.6084/m9.figshare.14371652), version 2; md5 published.
8. Open direct link.
9. Dataset CC BY 4.0 (figshare); the article itself is CC BY-NC-ND.
10. A.
11. Part of #18 PS-FH-AOP 2023 training data ([Zenodo PSFHS](https://zenodo.org/records/10969427)). Frames from the same video are near-duplicates (inference).
12. "Original toolbar and text were removed by cutting and overwriting" ([PMC8842023](https://pmc.ncbi.nlm.nih.gov/articles/PMC8842023/)).
13. UltraSam US-43d "FH-PS-AOP" (via #18) ([UltraSam README](https://github.com/CAMMA-public/UltraSam)).
14. Verified at the figshare API for article 14371652 on 2026-11-25 and https://pmc.ncbi.nlm.nih.gov/articles/PMC8842023/ on 2026-11-26.

#### 17. PSFHS (Intrapartum ultrasound image dataset for AI-based segmentation of pubic symphysis and fetal head)
1. 2024; Chen et al., Scientific Data, [doi:10.1038/s41597-024-03266-4](https://doi.org/10.1038/s41597-024-03266-4) (open: [PMC11066050](https://pmc.ncbi.nlm.nih.gov/articles/PMC11066050/)).
2. Pubic symphysis and fetal head, transperineal.
3. 2D B-mode still images, .mha files.
4. 1,358 images (1,045 Zhujiang Hospital, 313 First Affiliated Hospital of Jinan University) from 1,124 women; one zip of 0.132 GB ([Zenodo API](https://zenodo.org/records/10969427)).
5. Pixel masks: background, pubic symphysis, fetal head; two annotators per image, physician review.
6. Guangzhou, China; Esaote MyLab (Zhujiang) and ObEye (Jinan University); 3.5 MHz probe.
7. Zenodo record 10969427, DOI [10.5281/zenodo.10969427](https://doi.org/10.5281/zenodo.10969427), version V1; md5 published.
8. Open direct link. 9. CC BY 4.0. 10. A.
11. With #16 forms the #18 challenge data; also usable for #19 IUGC 2024 ([Zenodo](https://zenodo.org/records/10969427)). Zenodo 10901776 (#18) carries the same 1,358-image description under the challenge title, so it is a second copy (inference). Same hospitals and devices as #20 (possible overlap, not stated; inference).
12. "Original images were cropped to remove sensitive patient information" ([PMC11066050](https://pmc.ncbi.nlm.nih.gov/articles/PMC11066050/)).
13. UltraSam US-43d "FH-PS-AOP"; FADA ("PS-FH").
14. Verified at https://zenodo.org/records/10969427 on 2026-11-25 and https://pmc.ncbi.nlm.nih.gov/articles/PMC11066050/ on 2026-11-26.

#### 18. PS-FH-AOP 2023 (MICCAI 2023 Pubic Symphysis-Fetal Head Segmentation and Angle of Progression challenge)
1. 2023 challenge; [ps-fh-aop-2023.grand-challenge.org](https://ps-fh-aop-2023.grand-challenge.org/); proposal [Zenodo 7861699](https://zenodo.org/records/7861699) (CC BY-NC-ND 4.0, PDF).
2. to 5. Same content as #17 plus #16: "the whole dataset used for the PSFHS challenge of MICCAI2023 includes two parts: this PSFHS dataset and the JNU-IFM dataset" ([Zenodo](https://zenodo.org/records/10969427)). Hidden test set: unknown.
6. As #16 and #17.
7. Zenodo record [10901776](https://zenodo.org/records/10901776), "restricted", no files listed to guests, concept 7851338.
8. DUA with manual approval (Zenodo restricted request; conditions not shown).
9. CC BY 4.0 on the restricted record.
10. C for the restricted copy; download #16 and #17 instead (A).
11. Merge of #16 and #17 (stated).
12. As #16 and #17.
13. UltraSam US-43d "FH-PS-AOP" ([UltraSam README](https://github.com/CAMMA-public/UltraSam)).
14. Verified at https://zenodo.org/records/10901776 and https://zenodo.org/records/10969427 on 2026-11-25.

#### 19. IUGC 2024 (Intrapartum Ultrasound Grand Challenge, MICCAI 2024)
1. 2024; proposal [Zenodo 10979813](https://zenodo.org/records/10979813) (Bai, Lekadir, Ni, Slimani, Campello, Ohene-Botwe); challenge on Codalab, [competition 18413](https://codalab.lisn.upsaclay.fr/competitions/18413) (link from [Zenodo PSFHS](https://zenodo.org/records/10969427)).
2. Intrapartum images and videos; classification, segmentation, AoP and head-symphysis distance (HSD); data from Asia, Europe and Africa ([Zenodo IUGC 2025](https://zenodo.org/records/17355570)).
3. to 6. Unknown in detail.
7. Codalab (not opened).
8. Free account on Codalab (unverified).
9. Unknown.
10. C (unverified).
11. Builds on #17; #20 follows the IUGC 2024 evaluation code and may be its public release or part of it (relation not stated; inference). #20 covers only Guangzhou sites, so it cannot be the whole multi-continent set (inference).
12. to 13. Unknown.
14. Unverified (Codalab page not opened).

#### 20. Maternal-Fetal Ultrasound Video Dataset for End-to-end Intrapartum Biometry and Multi-task Learning
1. 2026; Niu, Bai, Gao, Tang, Lu, Han, Hou, Huang; Scientific Data 13:327, [doi:10.1038/s41597-026-06900-5](https://doi.org/10.1038/s41597-026-06900-5) (open: [PMC12966494](https://pmc.ncbi.nlm.nih.gov/articles/PMC12966494/)).
2. Intrapartum transperineal: pubic symphysis, fetal head, labour progress.
3. 2D B-mode videos and frames, resized to 512 x 512.
4. 774 videos, 68,106 frames, 774 women (JNU 560 videos / 61,924 frames; SYSU 121 / 3,494; Zhujiang 93 / 2,688); DatasetV3.zip 1.084 GB ([Zenodo API](https://zenodo.org/records/17655183)).
5. Plane labels per video; per-frame masks of pubic symphysis and fetal head; AoP and HSD from four landmarks.
6. First Affiliated Hospital of Jinan University, Third Affiliated Hospital of Sun Yat-sen University, Zhujiang Hospital (all Guangzhou, China); ObEye, GE Voluson P8, Esaote MyLab.
7. Zenodo record 17655183, version V3 (concept 16869287); md5 on Zenodo, SHA-256 on the article page.
8. Open direct link.
9. Dataset CC BY 4.0; article CC BY-NC-ND 4.0.
10. A.
11. Possible overlap with #17 and #16 (same group, same hospitals and devices; not stated) and with #19 (inference). Frames from one video are near-duplicates (inference).
12. "On-screen text and graphical overlays containing protected health information were digitally removed" ([PMC12966494](https://pmc.ncbi.nlm.nih.gov/articles/PMC12966494/)).
13. Unknown.
14. Verified at https://zenodo.org/records/17655183 on 2026-11-25 and https://pmc.ncbi.nlm.nih.gov/articles/PMC12966494/ on 2026-11-26.

#### 21. IUGC 2025 dataset (Intrapartum Ultrasound Grand Challenge, MICCAI 2025)
1. 2025; Zenodo [17355570](https://zenodo.org/records/17355570) (Bai); proposal [Zenodo 15172238](https://zenodo.org/records/15172238).
2. Intrapartum; landmark detection for AoP and HSD; all fetal descent stations.
3. 2D B-mode images and videos.
4. "28,919 ultrasound images and videos" from more than 20 institutions; "training set includes 300 labeled and 31,421 unlabeled cases, with 100 validation and 501 hidden test cases" (the two counts do not match; both as written); Dataset.zip 1.072 GB.
5. Landmarks (semi-supervised task); test labels hidden.
6. More than 20 clinical institutions (not named).
7. Zenodo record 17355570; md5 published.
8. Open direct link. 9. CC BY 4.0. 10. A.
11. Same challenge series as #17 to #20; overlap with them not stated (flag for dedup, inference). Participant method deposits on Zenodo (records 17140354, 17148601 to 17150116, "T1" to "T8" .rar files up to 3.4 GB) are software, not datasets.
12. Unknown. 13. Unknown.
14. Verified at https://zenodo.org/records/17355570 on 2026-11-25.

#### 22. IUGC 2025 add-on (A Dataset with 169 images for IUGC 2025)
1. 2025; Zenodo [17356295](https://zenodo.org/records/17356295); linked to Yang et al. "DSNT-DeepUNet".
2. to 5. 169 additional intrapartum cases annotated by three physicians; one zip of 0.031 GB.
6. The First Hospital of Lanzhou University, China.
7. Zenodo; md5 published. 8. Open direct link. 9. CC BY 4.0. 10. A.
11. Add-on to #21. 12. to 13. Unknown.
14. Verified at https://zenodo.org/records/17356295 on 2026-11-25.

### E. Cervix

#### 23. FUGC 2025 (Fetal Ultrasound Grand Challenge: Semi-Supervised Cervical Segmentation, ISBI 2025)
1. 2025; Zenodo [14305302](https://zenodo.org/records/14305302) (Bai, Yang, Gan, Hasan, Liang, Cai); proposal [Zenodo 14328192](https://zenodo.org/records/14328192); benchmark paper "FUGC: Benchmarking Semi-Supervised Learning Methods for Cervical Segmentation", IEEE TMI 2026 (cited on [Zenodo 18217137](https://zenodo.org/records/18217137); not opened).
2. Uterine cervix, transvaginal; segmentation.
3. 2D B-mode still images.
4. Training/validation/test = 500/90/300 images; download size unknown. 50 labelled training images (inference from the method note on Zenodo 18217137, unverified).
5. Cervix segmentation masks (labelled subset); test labels hidden (challenge, inference).
6. Unknown.
7. Zenodo record holds only a data-sharing agreement (docx) and one figure; data sent after the signed agreement is emailed to the organisers (fugc.isbi25@gmail.com, as stated on the record).
8. DUA with manual approval (by email).
9. Record licence CC BY 4.0; the agreement's terms were not read.
10. C.
11. Extends the #18 and #19 challenge series to a semi-supervised setting (same organisers); the images are cervix, not intrapartum (inference). #24 builds on it.
12. to 13. Unknown.
14. Verified at https://zenodo.org/records/14305302 on 2026-11-25.

#### 24. FUGC pseudo-label set (A Dataset with Pseudo Labels for Cervical Segmentation in FUGC, ISBI 2025)
1. 2026-01-12; Zenodo [18217137](https://zenodo.org/records/18217137) (Bai); based on Tran et al., "Human-in-the-Loop Semi-Supervised Uterine Cervix Ultrasound Image Segmentation", ISBI 2025.
2. Cervix, transvaginal.
3. 2D B-mode images (inference: two zips named FUGC2025 and FUGC2025_pretrain).
4. Two zips: 0.965 GB and 2.491 GB (3.455 GB); image count unknown.
5. Pseudo-labels from each refinement stage, refined by experts in Label Studio; code.
6. Unknown.
7. Zenodo, version V0; md5 published.
8. Open direct link. 9. CC BY 4.0. 10. A.
11. Derived from #23; may contain the #23 images openly (unverified; inspect the file list before relying on it).
12. to 13. Unknown.
14. Verified at https://zenodo.org/records/18217137 on 2026-11-25.

### F. Other obstetric: amniotic fluid, phantoms, synthetic, text, unclear sets

#### 25. A-AFMA Ultrasound Challenge Dataset (ISBI 2021)
1. 2020-12-04; Institute of Biomedical Engineering, University of Oxford; Zenodo [4305956](https://zenodo.org/records/4305956).
2. Amniotic fluid and maternal bladder; measurement from ultrasound video.
3. Video. 4. Unknown. 5. Unknown. 6. University of Oxford, UK.
7. Zenodo, restricted; registration on Grand Challenge plus email to the organiser.
8. Closed: "No publication rights are given on this data. The data may only be used for the purpose of the challenge" (ethics constraint).
9. None stated; use limited to the challenge. 10. D.
11. to 13. Unknown. Excluded from the bias review for the same reason ([PMC12166052](https://pmc.ncbi.nlm.nih.gov/articles/PMC12166052/)).
14. Verified at https://zenodo.org/records/4305956 on 2026-11-25.

#### 26. NatalIA PBF-US1 (Phantom Blind-sweeps for Fetal Ultrasound Scanning)
1. 2024-11-27; Gonzalez, Barrientos, Perez, Fajardo, Reyna, Lara; Zenodo [14193949](https://zenodo.org/records/14193949), version 1.0.0.
2. Fetal phantom; relevant fetal planes in blind-sweep videos by non-trained staff (midwives, nurses).
3. Videos (blind sweeps) of a phantom.
4. One zip of 0.266 GB; frame count 19,407 per a search snippet of a 2026 arXiv paper (unverified).
5. Unknown (plane labels, inference from the purpose).
6. BiomedLab, IIB, Universidad Galileo and DiagnostiX Integra Medical Center (Guatemala, inference from the affiliation names).
7. Zenodo; md5 published. 8. Open direct link. 9. CC BY 4.0. 10. A.
11. to 13. Unknown (phantom: no patient overlap).
14. Verified at https://zenodo.org/records/14193949 on 2026-11-25.

#### 27. FPUS23 (Ultrasound Fetus Phantom Dataset)
1. 2023; Prabakaran, Hamelmann, Ostrowski, Shafique, IEEE Access, [doi:10.1109/ACCESS.2023.3284315](https://doi.org/10.1109/ACCESS.2023.3284315); [arXiv 2303.07852](https://arxiv.org/abs/2303.07852).
2. 23-week fetal phantom (secondary: [TIanCat atlas](https://github.com/TIanCat/open-medical-ultrasound-datasets)); fetus orientation, fetal planes, anatomical features.
3. 2D B-mode still images.
4. 15,728 images ([PMC12722232](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/); TIanCat atlas); download size unknown.
5. Orientation and plane classes, boxes of anatomical features; annotations in the GitHub repo.
6. Unknown (phantom).
7. [GitHub bharathprabakaran/FPUS23](https://github.com/bharathprabakaran/FPUS23) links one Google Drive file. Checksums: none.
8. Open direct link (public Google Drive link).
9. None stated in the README.
10. A, but fragile: large Google Drive files hit quota and confirm pages.
11. Used as a source by #29 FADA.
12. Unknown.
13. FADA. The npj catalogue scores it "Steel" (its lowest quality tier shown) ([PMC12722232](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/)).
14. Verified at https://raw.githubusercontent.com/bharathprabakaran/FPUS23/main/README.md on 2026-11-26.

#### 28. FU-LoRA synthetic fetal ultrasound images
1. 2024; Wang (University College Dublin); Zenodo [13228158](https://zenodo.org/records/13228158); [arXiv 2407.20072](https://arxiv.org/abs/2407.20072).
2. Synthetic fetal standard planes from a LoRA-tuned latent diffusion model.
3. Synthetic 2D images (not real patients).
4. synthetic_train_5000.zip, 2.057 GB (5,000 images by the file name; inference).
5. Plane classes (inference).
6. Model tuned on a "high-resource settings" fetal dataset (probably #2; inference).
7. Zenodo; md5 published. 8. Open direct link. 9. CC BY 4.0. 10. A.
11. Synthetic: no real duplicates, but trained on real data (memorisation risk; inference). Keep out of real-data counts.
12. to 13. Unknown.
14. Verified at https://zenodo.org/records/13228158 on 2026-11-25.

#### 29. FADA (Fetal Ultrasound Interpretation Dataset, 56,805 expert sonographer clinical descriptions)
1. 2026 (version 2, 2026-05-25); Alzubaidi, Agus (Hamad bin Khalifa University); Zenodo [20381238](https://zenodo.org/records/20381238); code [github.com/mahmoodphd/FADA](https://github.com/mahmoodphd/FADA).
2. Text: answers to 8 clinical questions (structures, orientation, plane, measurements, gestational age, quality, normality, recommendations) for fetal images in 14 categories (abdomen, aorta, cervix, CRL view, femur, NT views, pubic symphysis/fetal head, thorax, three brain planes).
3. Structured JSON text about images.
4. 18,935 images, 56,805 conversations; size unknown.
5. Text descriptions by one sonographer with more than 10 years of experience.
6. Images from public sets: FPUS23, FUSEP, HC18, CRL_NT (Mendeley), FOCUS, Fetal Abdominal Structures, PS-FH.
7. Zenodo, restricted (no files visible to guests).
8. On request (Zenodo restricted access request).
9. None stated on the record.
10. C.
11. No new images: all from #1, #4, #10, #14, #15, #17 or #18, #27 (as listed). Treat as labels for those sets.
12. Unknown.
13. Unknown.
14. Verified at https://zenodo.org/records/20381238 on 2026-11-25.

#### 30. Ultrasound Fetus Dataset (A. Anitha, 2024)
1. 2024; [Mendeley Data yrzzw9m6kk](https://data.mendeley.com/datasets/yrzzw9m6kk/2) (versions 1 and 2); Kaggle mirror [orvile/ultrasound-fetus-dataset](https://www.kaggle.com/datasets/orvile/ultrasound-fetus-dataset) (about 643 MB, per a search snippet).
2. "Normal, benign, malignant" classes (search snippet); the description may be copied from a breast dataset (search summary); content unclear.
3. to 14. Unverified (record not opened). Flag before use.

#### 31. Anal atresia case series
[Mendeley Data t4ycf4425k](https://data.mendeley.com/datasets/t4ycf4425k/1): prenatal ultrasound images for teaching and AI work (search snippet). All fields unverified.

#### 32. "dataset for ultrasound pregnancy investigation" (2021)
1. 2021-07-16; uploader "digshv"; Zenodo [5110223](https://zenodo.org/records/5110223) (version 0.0.4) and a test-only record [5110198](https://zenodo.org/records/5110198).
2. to 6. Not described ("dataset for ultrasound pregnancy investigation"); file name suggests YOLO boxes (inference).
4. 0.108 GB (5110223) and 0.012 GB (5110198).
7. Zenodo; md5 published. 8. Open direct link. 9. CC BY 4.0. 10. A, but content and provenance unknown: low priority.
11. to 13. Unknown.
14. Verified at https://zenodo.org/records/5110223 on 2026-11-25.

### G. Gynaecology

#### 33. MMOTU (Multi-Modality Ovarian Tumor Ultrasound image dataset)
1. 2022 preprint, Zhao et al., [arXiv 2207.06799](https://arxiv.org/abs/2207.06799); journal version Pattern Recognition 2026, [doi:10.1016/j.patcog.2025.112311](https://doi.org/10.1016/j.patcog.2025.112311) (from the TIanCat atlas; not opened).
2. Ovarian tumours; eight tumour categories (secondary, search snippet).
3. 2D B-mode (OTU_2d) and contrast-enhanced ultrasound, CEUS (OTU_CEUS, folder named "OTU_3d").
4. 1,469 2D images and 170 CEUS images (1,639) ([README](https://github.com/cv516Buaa/MMOTU_DS2Net)); 294 patients (secondary: TIanCat); OTU-2D from 247 patients (secondary, search snippet). Download size unknown.
5. Pixel-wise masks and global category labels ([README](https://github.com/cv516Buaa/MMOTU_DS2Net)).
6. Beihang University group (code owner); hospital: unverified.
7. Google Drive folder linked from [GitHub cv516Buaa/MMOTU_DS2Net](https://github.com/cv516Buaa/MMOTU_DS2Net). No checksums.
8. Open direct link (public Google Drive folder).
9. None stated for the data in the README.
10. A, fragile (Google Drive folder).
11. #34 is a third-party copy of the 2D part. UltraSam's "MMOTU-3D" is the CEUS part.
12. Unknown.
13. UltraSam US-43d ("MMOTU-2D", "MMOTU-3D"); UltraSam's sample data uses MMOTU-2D ([UltraSam README](https://github.com/CAMMA-public/UltraSam)).
14. Verified at https://raw.githubusercontent.com/cv516Buaa/MMOTU_DS2Net/main/README.md on 2026-11-26.

#### 34. MMOTU 2D curated copy (2D Multi-Modality Ovarian Tumor Ultrasound)
1. 2026-07-02; Ortiz de Murua, Ines Armas, Heras (Universidad de La Rioja); Zenodo [21128657](https://zenodo.org/records/21128657); used for "Dataset Pruning for Semantic Segmentation using MedSAM".
2. to 5. 1,469 2D images with labels converted to a multilabel format for binary segmentation; one zip of 0.136 GB.
6. As #33.
7. Zenodo; md5 published. 8. Open direct link.
9. CC BY 4.0 as set by the uploader; the original authors state no licence (#33), so the right to relicense is unclear (inference).
10. A.
11. Subset (OTU_2d) of #33, labels converted. Keep one copy.
12. to 13. Unknown.
14. Verified at https://zenodo.org/records/21128657 on 2026-11-25.

#### 35. PCOSGen (Auto-PCOS classification challenge 2024)
1. 2024; Handa, Saini, Dutta, Pathak, Choudhary, Goel; preprint [doi:10.22541/au.170629258.80995260/v1](https://doi.org/10.22541/au.170629258.80995260/v1) (from TIanCat; not opened).
2. Ovary: normal vs abnormal, and polycystic ovary yes/no for abnormal images.
3. 2D ultrasound still images, mostly 300 x 300 pixels.
4. 3,200 training + 1,468 test = 4,668 images; zips 0.072 GB + 0.021 GB.
5. Two image-level labels (general and specific class).
6. Delhi Technological University, Indira Gandhi Delhi Technical University for Women, Lady Hardinge Medical College and others, India (creator affiliations).
7. Zenodo [14592001](https://zenodo.org/records/14592001) (train) and [14591782](https://zenodo.org/records/14591782) (test); md5 published. Earlier versions exist; the record says to use only the updated ones.
8. Open direct link. 9. CC BY 4.0. 10. A.
11. Earlier versions under concept records 10430726 and 10510878 (do not mix). Overlap with Kaggle PCOS sets (#38): unknown.
12. Unknown. 13. Unknown.
14. Verified at https://zenodo.org/records/14592001 and https://zenodo.org/records/14591782 on 2026-11-25.

#### 36. PCOS Dataset (figshare 27682557)
[figshare 27682557](https://figshare.com/articles/dataset/PCOS_Dataset/27682557): 12,680 images, binary classification (secondary: [TIanCat atlas](https://github.com/TIanCat/open-medical-ultrasound-datasets)). Host figshare (open, A if confirmed). Licence, source and overlaps unverified. Likely to overlap Kaggle PCOS sets (inference).

#### 37. Ovarian Ultrasound Image Dataset (Kaggle)
[kaggle.com/datasets/ucimachinelearning/ovarian-ultrasound-image-dataset](https://www.kaggle.com/datasets/ucimachinelearning/ovarian-ultrasound-image-dataset): 6,879 images, classification (secondary: TIanCat atlas). Kaggle needs an account and API token: B. Licence and origin unverified; the account name does not prove a link to the UCI repository (inference).

#### 38. PCOS "infected / notinfected" (Kaggle origin; Hugging Face mirror)
[BTX24/PCOS-ultrasound-dataset](https://huggingface.co/datasets/BTX24/PCOS-ultrasound-dataset): 1,539 training + 385 test images (1,924), classes "infected" and "notinfected", 0.068 GB (dataset card). Licence not stated. The Kaggle original was not checked (unverified). Other PCOS image repos on Hugging Face: [Celcia/pcos-image-dataset](https://huggingface.co/datasets/Celcia/pcos-image-dataset) (Apache 2.0 tag; content unverified). Verified (mirror card only) at https://huggingface.co/datasets/BTX24/PCOS-ultrasound-dataset on 2026-11-25.

#### 39. Polycystic ovary ultrasound images dataset (54 images)
Listed as open access, 54 images, "Bronze" quality tier in the npj catalogue ([PMC12722232](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/)). Host and licence not captured (unverified).

#### 40. UFUV (uterine fibroid ultrasound videos, LGRNet, MICCAI 2024)
1. 2024; Xu, Yang, Aviles-Rivero, Yang, Qin, Zhu, "LGRNet: Local-Global Reciprocal Network for Uterine Fibroid Segmentation in Ultrasound Videos", MICCAI 2024, [arXiv 2407.05703](https://arxiv.org/abs/2407.05703).
2. Uterine fibroids.
3. Ultrasound videos (B-mode, inference).
4. UFUV.zip, 1.587 GB (Hugging Face file tree); number of videos and frames unknown.
5. Segmentation masks (from the title).
6. Unknown.
7. [Hugging Face huihuixu/uterine_fibroid_ultrasound_video_segmentation](https://huggingface.co/datasets/huihuixu/uterine_fibroid_ultrasound_video_segmentation) (the author's own page); code [github.com/bio-mlhui/LGRNet](https://github.com/bio-mlhui/LGRNet). Copies by other users exist on Hugging Face (harshith123e).
8. Open direct link. 9. MIT (dataset card). 10. A.
11. to 13. Unknown.
14. Verified at https://huggingface.co/datasets/huihuixu/uterine_fibroid_ultrasound_video_segmentation on 2026-11-25 and its file tree on 2026-11-26.

#### 41. PFUS1 (Premier Pelvic Floor Ultrasound Segmentation Dataset)
1. 2024-06-10; Solis-Martin, Garcia-Mejido, Sainz-Bueno, Galan-Paez (Universidad de Sevilla); Zenodo [10800787](https://zenodo.org/records/10800787); paper: unknown.
2. Pelvic floor, midsagittal plane; eight structures, for example levator ani muscle and rectum.
3. Frames from ultrasound videos (PNG) (file naming "frame_YYY").
4. 110 patients; frame count unknown; one zip of 5.807 GB.
5. Polygon segmentation of eight structures in JSON per frame.
6. Universidad de Sevilla, Spain (creator affiliation).
7. Zenodo; md5 published. 8. Open direct link. 9. CC BY 4.0. 10. A.
11. Consecutive frames are near-duplicates (inference).
12. Unknown. 13. Unknown.
14. Verified at https://zenodo.org/records/10800787 on 2026-11-25.

#### 42. UterUS (3D transvaginal uterus volumes)
A 2024 Computers in Biology and Medicine paper from the University of Ljubljana describes a public dataset of 3D transvaginal ultrasound volumes with manual uterine-cavity annotations ([paper PDF link from search](https://lgm.fri.uni-lj.si/wp-content/uploads/2024/09/200067331.pdf)). Host, size and licence unverified. Related: UtiSeg, a PLOS ONE 2025 uterus segmentation study with code at github.com/dilaratank/UtiSeg ([PMC12611126](https://pmc.ncbi.nlm.nih.gov/articles/PMC12611126/)); whether its data are public is unverified.

#### 43. Clinical Ultrasound Image Repository (AWS Registry of Open Data)
Multi-anatomy (abdominal, cardiac, OB/GYN), clinical DICOM, 2,000 studies (secondary: [TIanCat atlas](https://github.com/TIanCat/open-medical-ultrasound-datasets)); [registry page](https://registry.opendata.aws/clinical-ultrasound-image-data/). Licence, OB/GYN share and access not checked (unverified). DICOM headers and burned-in text need checking before use (inference).

## Key question: which datasets exist?

### Takeaway
I found 43 candidates. 26 can be downloaded with no login (tier A): 17 on Zenodo, 3 on figshare, 2 on Mendeley Data, 2 on Hugging Face, 2 on Google Drive. 4 need an agreement or approval (tier C: #18, #19, #23, #29), 1 is closed (#25 A-AFMA), and 12 are unverified or have no download route. Fetal and intrapartum data dominate. Gynaecology is thin: ovary and PCOS sets, one fibroid video set and one pelvic floor set. I found no public placenta, endometrium or adnexal-mass ultrasound set. Crown-rump length appears only in FUSEP (no download link) and in a "CRL_NT" set named by FADA that I could not locate.

### Cited Findings
- A 2025 review counted 14 public fetal ultrasound databases from 2017 to 2024, sizes from 25 video sequences to 15,728 images — [PubMed 40775990](https://pubmed.ncbi.nlm.nih.gov/40775990/) (abstract only; the list itself was not obtained).
- A 2025 bias review found five public fetal datasets (FETAL_PLANES_DB, MFUSPAC, FASSD, HC18; A-AFMA excluded because restricted). It excluded intrapartum, phantom and DICOM sets and those with identifying text — [PMC12166052](https://pmc.ncbi.nlm.nih.gov/articles/PMC12166052/).
- The npj catalogue of 72 public ultrasound datasets lists eight in this scope: FETAL_PLANES_DB (12,400), FASSD (1,588), FPUS23 (15,728), HC18 (1,334), ACOUSLIC-AI (600), FOCUS (300), a 54-image PCOS set, PCOSGen (4,668). It notes that few fetal datasets are open-sourced — [PMC12722232](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/).
- 2025 and 2026 releases found: FOCUS ([Zenodo](https://zenodo.org/records/14597550)), PCOSGen updated versions ([Zenodo](https://zenodo.org/records/14592001)), IUGC 2025 data ([Zenodo](https://zenodo.org/records/17355570)), the intrapartum video dataset ([Zenodo](https://zenodo.org/records/17655183)), the FUGC pseudo-label set ([Zenodo](https://zenodo.org/records/18217137)), FADA ([Zenodo](https://zenodo.org/records/20381238)), MMOTU 2D copy ([Zenodo](https://zenodo.org/records/21128657)), Multicentre-Fetal-Biometry ([UCL RDR](https://rdr.ucl.ac.uk/articles/dataset/A_multi-centre_multi-device_benchmark_dataset_for_landmark-based_comprehensive_fetal_biometry/30819911)), DELTA ([figshare](https://figshare.com/articles/dataset/DELTA_A_Dual-Modality_Fetal_Echocardiography_Dataset_for_Long-Tail_Congenital_Heart_Disease_Diagnosis/32358771)), FetalCHD-MV ([Hugging Face](https://huggingface.co/datasets/YuanZhao1230/FetalCHD-MV)), FUSEP ([arXiv](https://arxiv.org/abs/2608.04766)).
- Zenodo searches for placenta, endometrium, uterine fibroid, adnexal mass, ectopic pregnancy and crown-rump length returned only papers, clinical tables or an animal (rat) placenta contrast study ([Zenodo 4937915](https://zenodo.org/records/4937915)); no human image dataset (my query log; Zenodo API, 2026-11-25).

### Inferences
- Candidates named in the task that do exist under these names: HC18, FETAL_PLANES_DB, the African extension, FPUS23, PSFHS, PS-FH-AOP 2023, JNU-IFM, ACOUSLIC-AI 2024, IUGC 2024, FUGC 2025, MMOTU, PCOS sets. Fetal heart, first-trimester and pelvic floor sets exist (FOCUS, DELTA, Fetus Framework, PFUS1). Placenta and endometrium sets: none found.
- For the project (training set about 20k images; epic 1 upper abdomen, epic 3 liver disease), the fetal abdomen sets (#4 FASSD with fetal liver and stomach masks, #5 ACOUSLIC-AI, the abdomen class of #2) are the closest in anatomy, but fetal anatomy differs from adult liver.

### Gaps
- The list of 14 in the SHTI 2025 review and the full Imaging-X catalogue ([GitHub](https://github.com/uni-medical/Project-Imaging-X)) were not read; they may hold sets missed here.
- Kaggle and Science Data Bank were not searched directly (budget).

## Key question: subsets, re-releases, merges and known duplicates

### Takeaway
The intrapartum family from one Jinan University group (#16 JNU-IFM, #17 PSFHS, #18 PS-FH-AOP 2023, #19 IUGC 2024, #20 video dataset, #21 and #22 IUGC 2025, and the cervix sets #23 and #24) is the main dedup risk. #6 Multicentre-Fetal-Biometry reuses HC18 and probably FETAL_PLANES_DB. FADA and the MMOTU copy add no new images.

### Cited Findings
- PS-FH-AOP 2023 data = PSFHS + JNU-IFM; PSFHS images also serve IUGC 2024 — [Zenodo 10969427](https://zenodo.org/records/10969427).
- The restricted Zenodo record 10901776 has the PSFHS description (1,358 images) under the challenge title — [Zenodo 10901776](https://zenodo.org/records/10901776).
- The IUGC series: 2023 segmentation, 2024 videos with classification, AoP and HSD and data from Asia, Europe and Africa, 2025 landmarks from more than 20 institutions — [Zenodo 17355570](https://zenodo.org/records/17355570).
- The 2026 video dataset comes from the same Guangzhou hospitals and devices as PSFHS (Zhujiang with Esaote MyLab, Jinan University with ObEye) and follows the IUGC 2024 evaluation code; image reuse is not stated — [PMC12966494](https://pmc.ncbi.nlm.nih.gov/articles/PMC12966494/); [PMC11066050](https://pmc.ncbi.nlm.nih.gov/articles/PMC11066050/).
- FUGC extends the PSFHS 2023 and IUGC 2024 challenges to semi-supervised learning — [Zenodo 14305302](https://zenodo.org/records/14305302).
- Multicentre-Fetal-Biometry is "derived from three existing sources: the Fetal Plane (FP) dataset, the HC18 head dataset, and a dataset acquired at University College London Hospital" — [UCL RDR](https://rdr.ucl.ac.uk/articles/dataset/A_multi-centre_multi-device_benchmark_dataset_for_landmark-based_comprehensive_fetal_biometry/30819911).
- FADA's 18,935 images all come from public sets (FPUS23, FUSEP, HC18, CRL_NT, FOCUS, Fetal Abdominal Structures, PS-FH) — [Zenodo 20381238](https://zenodo.org/records/20381238).
- The La Rioja MMOTU record is a curated 2D-only copy of MMOTU — [Zenodo 21128657](https://zenodo.org/records/21128657).
- PCOSGen has earlier versions that users should not download — [Zenodo 14592001](https://zenodo.org/records/14592001).
- Hugging Face mirrors of FETAL_PLANES_DB ([Emulated-Inc](https://huggingface.co/datasets/Emulated-Inc/sci-fetal-planes-low-resource), unchanged files; [chehablab](https://huggingface.co/datasets/chehablab/FETAL_PLANES_DB) and others) and HC18 ([MedOtter/HC18](https://huggingface.co/datasets/MedOtter/HC18)) exist (HF API, 2026-11-25).

### Inferences
- Treat #18 as a pointer: download #16 and #17 only.
- Hash-check #20, #21, #22 against #16 and #17 before training (same group, same hospitals).
- Within-dataset near-duplicates: video-derived sets (#5, #16, #20, #21, #26, #40, #41) hold many near-identical consecutive frames; split by patient or video.
- #7 and #8 are probably FETAL_PLANES_DB or HC18 derivatives (same author as FADA; unverified).
- PCOS sets on Kaggle, figshare and Hugging Face (#36 to #39) probably share images; their provenance is unclear.

### Gaps
- No published duplicate analysis was found for any of these sets.
- Whether #24 (FUGC pseudo-labels) contains the #23 images openly was not checked.

## Key question: largest datasets, and open ones with a permissive licence

### Takeaway
By frame count the largest are ACOUSLIC-AI (about 252,000 frames, secondary; 38 GB, non-commercial licence) and the intrapartum video dataset (68,106 frames, CC BY 4.0). The largest still-image clinical set is FETAL_PLANES_DB (12,400 images, CC BY 4.0). Most open sets are CC BY 4.0 on Zenodo or figshare with md5 checksums, which suits scripted download.

### Cited Findings
Table 2. Largest sets by image or frame count, with licence and automation tier (counts as stated at the source).

| Dataset | Images or frames | Licence | Auto | Source |
|---|---|---|---|---|
| ACOUSLIC-AI | ~252,000 frames, 300 cases (secondary) | CC BY-NC-SA 4.0 | A | [Zenodo](https://zenodo.org/records/12697994); [TIanCat](https://github.com/TIanCat/open-medical-ultrasound-datasets) |
| Intrapartum video dataset (2026) | 68,106 frames, 774 videos | CC BY 4.0 | A | [PMC12966494](https://pmc.ncbi.nlm.nih.gov/articles/PMC12966494/) |
| IUGC 2025 | 28,919 images and videos (stated) | CC BY 4.0 | A | [Zenodo](https://zenodo.org/records/17355570) |
| FPUS23 (phantom) | 15,728 images | none stated | A (fragile) | [PMC12722232](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/) |
| PCOS figshare | 12,680 images (secondary) | unverified | unverified | [TIanCat](https://github.com/TIanCat/open-medical-ultrasound-datasets) |
| FETAL_PLANES_DB | 12,400 images | CC BY 4.0 | A | [Zenodo](https://zenodo.org/records/3904280) |
| Ovarian (Kaggle) | 6,879 images (secondary) | unverified | B | [TIanCat](https://github.com/TIanCat/open-medical-ultrasound-datasets) |
| JNU-IFM | 6,224 frames | CC BY 4.0 | A | [PMC8842023](https://pmc.ncbi.nlm.nih.gov/articles/PMC8842023/) |
| PCOSGen | 4,668 images | CC BY 4.0 | A | [Zenodo](https://zenodo.org/records/14592001) |
| Multicentre-Fetal-Biometry | 4,513 images (mostly reused) | CC BY-NC-SA 4.0 | A | [UCL RDR](https://rdr.ucl.ac.uk/articles/dataset/A_multi-centre_multi-device_benchmark_dataset_for_landmark-based_comprehensive_fetal_biometry/30819911) |
| DELTA | 3,760 images + 752 videos | CC BY 4.0 | A | [figshare](https://figshare.com/articles/dataset/DELTA_A_Dual-Modality_Fetal_Echocardiography_Dataset_for_Long-Tail_Congenital_Heart_Disease_Diagnosis/32358771) |

- Open, tier A, CC BY 4.0 (permissive, attribution only): HC18, FETAL_PLANES_DB, African planes, FASSD, Fetus Framework, PSFHS, JNU-IFM, intrapartum video dataset, IUGC 2025 and add-on, FUGC pseudo-labels, FOCUS, DELTA, NatalIA PBF-US1, PCOSGen, PFUS1, pixel-to-mm set, FU-LoRA (synthetic) (per-entry sources above).
- Non-commercial: ACOUSLIC-AI and Multicentre-Fetal-Biometry (CC BY-NC-SA 4.0) ([Zenodo](https://zenodo.org/records/12697994); [UCL RDR](https://rdr.ucl.ac.uk/articles/dataset/A_multi-centre_multi-device_benchmark_dataset_for_landmark-based_comprehensive_fetal_biometry/30819911)).
- No licence stated: MMOTU original, FPUS23 ([MMOTU README](https://github.com/cv516Buaa/MMOTU_DS2Net); [FPUS23 README](https://github.com/bharathprabakaran/FPUS23)). MIT: UFUV ([Hugging Face](https://huggingface.co/datasets/huihuixu/uterine_fibroid_ultrasound_video_segmentation)).
- No checked licence restricts where copies may be stored; CC BY-NC-SA requires the same licence on derived works ("share-alike") (licence names as stated on the hosts).

### Inferences
- The tier-A, CC BY 4.0 group totals about 26 GB (24 GB without the synthetic FU-LoRA set): the sum of the host API sizes above, without FASSD and Fetus Framework (size unknown). With ACOUSLIC-AI (38 GB, non-commercial) and Multicentre-Fetal-Biometry (1.6 GB, non-commercial) the open total is about 66 GB.
- Most open data are intrapartum and fetal planes; heart (DELTA, FOCUS) and pelvic floor (PFUS1) are new in 2025 and 2026.

### Gaps
- Frame counts for PFUS1, UFUV, NatalIA and the FUGC pseudo-label set are unknown without opening the archives (not allowed in this run).

## Gaps

Datasets seen but not verified or not found:
- FUSEP (2026): claimed public, no link found ([arXiv 2608.04766](https://arxiv.org/abs/2608.04766)).
- 2D foetal brain benchmark (104 images): no host found ([arXiv 2406.17250](https://arxiv.org/abs/2406.17250)).
- CRL_NT (Mendeley) named by FADA: not located.
- FetalCHD-MV: Hugging Face repos hold no images; paper not found.
- Large-scale fetal head biometry annotations ([PMC10630602](https://pmc.ncbi.nlm.nih.gov/articles/PMC10630602/)): not read.
- IUGC 2024 data on Codalab ([competition 18413](https://codalab.lisn.upsaclay.fr/competitions/18413)): not opened.
- Ovarian and PCOS sets known only from lists or snippets: Kaggle ovarian set (#37), figshare PCOS (#36), 54-image PCOS set (#39), "OUD (Ovarian Ultrasound Dataset)" named in [arXiv 2608.25965](https://arxiv.org/pdf/2608.25965), [GitHub HananSaadat/ovarian_ultrasound_dataset](https://github.com/HananSaadat/ovarian_ultrasound_dataset) (normal, dominant follicle, polycystic ovary), Kaggle PCOS "infected/notinfected" original, USOVA3D (3D ovarian follicles, not searched), OvAi Focus ovarian and adnexal segmentation ([arXiv 2607.14179](https://arxiv.org/pdf/2607.14179); data availability unknown).
- Uterus: UterUS and UtiSeg (#42): hosts unverified. Endometrium: no public set found; the endometrium studies found used their own data (search summary, unverified).
- Placenta and adnexa: no public human ultrasound image set found.
- Other large-scale model papers (SAMUS US30K, OpenUS, USFM, MedSAM, SA-Med2D-20M, FetalCLIP): their dataset lists were not checked; field 13 relies on UltraSam US-43d and FADA only.

Dead or blocked links:
- No dead dataset link confirmed. The ACOUSLIC-AI Grand Challenge dataset page returned HTTP 403 to automated fetch; Nature article pages redirect automated clients to a login (open PMC copies used instead).

Restricted or private, no open route:
- A-AFMA (ISBI 2021): restricted to challenge participants, no publication rights ([Zenodo 4305956](https://zenodo.org/records/4305956)).
- PS-FH-AOP 2023 restricted copy ([Zenodo 10901776](https://zenodo.org/records/10901776)); FADA ([Zenodo 20381238](https://zenodo.org/records/20381238)); FUGC 2025 by signed agreement ([Zenodo 14305302](https://zenodo.org/records/14305302)).
- Often-cited private first-trimester videos (PULSE, Oxford, 250 scans) appear only in papers ([ISBI 2022 paper](<https://pcwww.liv.ac.uk/~hezhao/papers-pp/2020after/[ISBI22] End-to-end First Trimester Fetal Ultrasound Video Automated CRL and NT Segmentation.pdf>); search summary). FetalCLIP's private training images and other private sets (FAMLI, iFIND, IOTA): unverified, not checked.

Roboflow only (epic 2, the project's separate Roboflow scraper under [DEC-081](../../decisions/DEC-081-epic2-mission-roboflow-universe-ultrasound-scraper.md) and [DEC-096](../../decisions/DEC-096-epic2-retrieval-path-official-routes-terms-reading-fetch-budget.md)):
- Uterine fibroid projects, for example [siat-wklyw/uterine-fibroid](https://universe.roboflow.com/siat-wklyw/uterine-fibroid) and [capstone-project-tchuv/uterine-fibroid-detection](https://universe.roboflow.com/capstone-project-tchuv/uterine-fibroid-detection): Roboflow only (epic 2).
- Fetus brain abnormalities: Roboflow project with a Hugging Face mirror [KBayoud/roboflow-fetus-brain-abnormalities](https://huggingface.co/datasets/KBayoud/roboflow-fetus-brain-abnormalities): Roboflow only (epic 2).

## Seen, other groups

- Neonatal brain, 3D transfontanelle ultrasound (Zenodo): [zenodo.org/records/19593033](https://zenodo.org/records/19593033).
- Rat placenta contrast-enhanced ultrasound (animal): [zenodo.org/records/4937915](https://zenodo.org/records/4937915).
- Plane-wave raw data, breast and calibration phantoms: [zenodo.org/records/7986407](https://zenodo.org/records/7986407).
- Regensburg Pediatric Appendicitis Dataset (abdomen; lists reproductive organs among anatomies): in the npj catalogue ([PMC12722232](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/)).
- MICCAI 2025 FLARE ultrasound (abdomen): [huggingface.co/datasets/jacksonyu123/MICCAI25_FLARE_Ultrasound](https://huggingface.co/datasets/jacksonyu123/MICCAI25_FLARE_Ultrasound).
- Thyroid ultrasound images: [huggingface.co/datasets/FangDai/Thyroid_Ultrasound_Images](https://huggingface.co/datasets/FangDai/Thyroid_Ultrasound_Images); breast mirrors of BUSI and BUS-BRA on Hugging Face (several).
- Paired robotic and handheld lumbar spine ultrasound: [doi:10.48804/3XPCAE](https://doi.org/10.48804/3XPCAE) (in the TIanCat atlas).
- Not ultrasound (excluded): VIA cervix images ([AHFIDAILabs/via-cervix](https://huggingface.co/datasets/AHFIDAILabs/via-cervix)), UT-EndoMRI ([Zenodo 13749613](https://zenodo.org/records/13749613)).
