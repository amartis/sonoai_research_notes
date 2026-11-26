# Public abdominal and urological ultrasound datasets: census for automated download (as of 2026-11-25/26)

Scope: liver, gallbladder and bile ducts, pancreas, spleen, kidney, adrenal, stomach and bowel
(appendix included), abdominal wall, abdominal multi-organ sets, trauma FAST (Focused Assessment
with Sonography in Trauma) and abdominal point-of-care ultrasound (POCUS), urology (bladder,
prostate, testis), simulated or CT-derived abdominal ultrasound, and abdominal subsets of
multi-organ collections. Epic 1 of the project is upper-abdomen anatomy segmentation; epic 3 is
spotting liver diseases. Epic 2 is the project's separate Roboflow scraper (decisions [DEC-081](../../decisions/DEC-081-epic2-mission-roboflow-universe-ultrasound-scraper.md) and
[DEC-096](../../decisions/DEC-096-epic2-retrieval-path-official-routes-terms-reading-fetch-budget.md)), so Roboflow-only projects are listed but not researched.

Terms used throughout. CEUS: contrast-enhanced ultrasound. EUS: endoscopic ultrasound. TRUS:
transrectal ultrasound. RF: raw radio-frequency data. NAFLD: non-alcoholic fatty liver disease.
NAS: NAFLD Activity Score (biopsy score). HCC: hepatocellular carcinoma. TCIA: The Cancer Imaging
Archive. IDC: NCI Imaging Data Commons. DUA: data use agreement.
Automation tiers (field 10): **A** scriptable with no login; **B** scriptable with a token the user
supplies once (for example a Kaggle API token); **C** needs a manual step by the user (form,
approval, click-through, emailed link); **D** not automatable now.
Closeness ratings. Epic 1: **High** = pixel masks of upper-abdominal organs; **Med** = masks of
one organ, organ boxes, or organ/view class labels; **Low** = abdominal images without anatomy
labels; **None**. Epic 3: **High** = liver disease grade or lesion type with a stated reference
standard (biopsy, pathology, cross-sectional imaging); **Med** = liver disease labels with an
unstated or clinical reference; **Low** = liver images, no disease labels; **None**.
Verification dates: pages read before the run paused are dated 2026-11-25; pages read after it
resumed are dated 2026-11-26.

## Q1. Which abdominal and urological ultrasound datasets exist, with their download facts and label closeness?

### Takeaway
About 40 public or semi-public abdominal and urological ultrasound datasets are reachable. Most
are small: only 5 hold 9,000 or more 2D images; one of those five (LUS-7Seg) is a Kaggle upload
whose origin this run could not confirm, and one (Saudi NAFLD) needs a signed agreement. Upper-abdominal organ **masks** are rare. The main sources
are AUL (liver and lesion masks, 735 images), the Open Kidney set (kidney regions, 514
patients), the Vitale "US simulation & segmentation" set (8 organs; 61 annotated real images and
926 CT-derived simulated ones), and a new Kaggle-only set, LUS-7Seg (10,507 images with liver
and gallbladder masks; origin unverified). The strongest liver-disease labels are the Saudi
NAFLD set (10,352 images, biopsy-based steatosis grade and fibrosis stage; access by signed
agreement), the Byra fatty-liver set (550 images, open), SMC-LUD (5,385 images, HCC vs
haemangioma, open, 2026) and TCIA B-mode-and-CEUS-Liver (120 patients, open).

### Cited Findings

#### Summary table

Table 1. Abdominal and urological ultrasound datasets found by 2026-11-26, grouped by organ.
"Images" counts 2D images unless stated. GB is the download size stated by the host. Access:
open, reg (registration or emailed link), DUA (signed agreement), req (on request by email),
closed. Sources for every cell are in the detailed entries below (same number).

| # | Name | Anatomy | Images or videos | GB | Host | Access | Licence | Auto | Epic 1 | Epic 3 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | AUL (Annotated Ultrasound Liver images) | liver, focal masses | 735 images | 0.07 | Zenodo | open | CC BY 4.0 in metadata; text says "subject to copyright" | A | Med (liver + mass masks) | Med (benign/malignant/normal) |
| 2 | B-mode-and-CEUS-Liver | liver masses, B-mode + CEUS | 1,859 DICOM objects, 120 patients | 272.16 | TCIA | open | CC BY 4.0 | A | Low | High (pathology or CT/MRI within 1 month) |
| 3 | Byra fatty liver (B-mode) | liver steatosis | 550 images, 55 patients | 0.05 | Zenodo | open | CC BY 4.0 | A | Low | High (biopsy) |
| 4 | Saudi NAFLD liver set | liver steatosis, fibrosis | 10,352 images, 384 patients | unknown | OSF | DUA | non-commercial; agreement | C | Low | High (biopsy NAS grade/stage) |
| 5 | SMC-LUD | liver HCC vs haemangioma | 5,385 images (5,466 in one text), 1,021 patients | 1.33 | figshare | open | CC BY 4.0, text adds "non-commercial research use only" | A | Low | Med-High (diagnosis; reference not read) |
| 6 | BEHSOF | liver NAFLD | 1,669 images, 113 people | 0.35 (Kaggle copy) | figshare (unreachable); Kaggle copy | open (copy) | "Other" on Kaggle | B | Low | Med (clinical NAFLD label) |
| 7 | SYSU-FLL-CEUS | liver CEUS lesions | 353 lesion clips (186 HCC, 109 haemangioma, 58 FNH) | ~8 to 11 (Kaggle copy) | GitHub sample + email; Kaggle copy | req | none stated (Apache-2.0 on copy) | C | None | High-Med (pre-operative cases; reference not read) |
| 8 | US-Liver (HSQformer test sets) | liver, HCC screening | 2 test subsets | 0.22 | Hugging Face | open | Apache-2.0 (stated) | A | Low | Med (labels not read) |
| 9 | Liver fibrosis F0-F4 (Joo et al. 2023) | liver fibrosis | F0 2,114, F1 861, rest not read | 0.21 or 1.89 | Kaggle (re-upload) | open (copy) | CC BY-SA 4.0 on copy | B | Low | Med-High (F0-F4; reference not read) |
| 10 | CLUST 2015 (liver tracking) | liver motion | 64 2D+t and 22 3D+t sequences | unknown | Uppsala University site | reg (paused) | challenge use only | D | Low (landmarks) | None |
| 11 | usliverseq (CLUST public subset) | liver, healthy | 7 to 9 2D sequences | unknown (mp4 copy 0.11) | ETH Zurich direct zip | open | none stated | A | Low | None |
| 12 | LUS-7Seg | liver, gallbladder planes | 10,507 images, 2,415 people | 1.09 | Kaggle only | open | CC BY-SA 4.0 (uploader's) | B | High (liver + gallbladder masks, 7 plane labels) | None |
| 13 | AD-MAGNet Liver Ultrasound | liver lesions | claims 18,000-image test set | 0.08 | Mendeley Data; Kaggle copy | open | CC BY 4.0 (MIT on Kaggle) | A | Low | Med (normal/benign/malignant; doubtful) |
| 14 | NAFLD severity + clinical data (Bangladesh) | liver | unknown (8 MB zip) | 0.008 | Mendeley Data | open | CC BY 4.0 | A | Low | Low-Med (odd labels) |
| 15 | GBCU | gallbladder | 1,255 images, 218 patients | unknown | email link | DUA | signed licence agreement | C | Med (gallbladder box) | None |
| 16 | GBUSV | gallbladder | 64 videos, 15,800 frames | unknown | email link | DUA | signed licence agreement | C | Low | None |
| 17 | UIdataGB (Gallblader Diseases Dataset) | gallbladder diseases | 10,692 images, 1,782 people | 2.04 | Mendeley Data (+ figshare, Academic Torrents) | open | CC BY 4.0 | A | Low (organ-level classes) | None |
| 18 | Open Kidney Ultrasound Data Set | kidney (native, transplant) | 514 images (534 files), 514 patients | unknown | registration, email | reg | CC BY-NC-SA | C | High (kidney region masks, view labels) | None |
| 19 | Kidney "Stone" and "No Stone" | kidney | 9,416 images | 0.23 | Mendeley Data | open | CC BY 4.0 | A | Low | None |
| 20 | CT2USforKidneySeg | kidney, CT-derived synthetic | unknown | 0.27 | Kaggle | open | GPL 2 | B | Med (kidney masks; not checked) | None |
| 21 | Sensing ULM kidney (raw RF and IQ) | kidney microvessels, rats and humans | RF .mat sequences | 34.91 (RF) + 18.68 (IQ) | Zenodo | open | CC BY 4.0 | A | None | None |
| 22 | LEPset | pancreas (EUS) | 11,500 images (3,500 labelled), 420 patients | 0.78 | Zenodo | open | CC BY 4.0 | A | None | None |
| 23 | GIST514-DB | GI tract tumours (EUS) | 514 cases | unknown | GitHub | open (per atlas) | unknown | unverified | None | None |
| 24 | C-TRUS | colon wall (transrectal) | 827 images, 13 patients | unknown | GitHub | open (per atlas) | unknown | unverified | Low | None |
| 25 | Regensburg Pediatric Appendicitis | appendix, right lower quadrant, children | 2,097 images, 782 records (paper: 1,709, 579 patients) | 0.52 | Zenodo | open | CC BY-NC 4.0 | A | Low (lower abdomen) | None |
| 26 | Abdominal Ultrasound Image Dataset (Karim and Ball; Sci Data 2026) | 10 abdominal organ classes | 5,468 unique images, 563 patients | 1.43 | Mississippi State Scholars Junction | open | CC BY 4.0 | A (unverified) | Med (organ class labels, 10 classes) | Low (normal/abnormal, ascites) |
| 27 | US simulation & segmentation (Vitale et al.; "AbdomenUS") | 8 abdominal organs, real + simulated | 617 real (61 annotated) + 926 simulated | 2.10 | Kaggle | open | "Data files © Original Authors" | B | High (8-organ masks; small real part) | None |
| 28 | Clinical Ultrasound Image Repository (MONAI) | abdomen, heart, OB/GYN | 2,000 studies (about 1/3 abdominal) | unknown | AWS open data S3 | open | CC BY-NC 4.0 | A | Low | None |
| 29 | USenhance 2023 (MICCAI challenge) | liver, kidney + 3 non-abdominal organs | 1,050 training pairs + 364 test inputs (all organs) | unknown | Grand Challenge | unverified | CC BY-SA (per atlas) | unverified | Low | None |
| 30 | M2-US (2026) | 30+ targets; abdominal: liver lesion, organ class | 67,620 images total; 5,466 liver lesion + 366 organ-class | 7.90 (all) | Zenodo | open | CC BY 4.0 | A | Med (366 organ-class images) | Med (liver lesion 2 classes) |
| 31 | Chinese ultrasound report-generation set (Li et al.) | breast, thyroid, liver; reports | 17,149 images, 7,364 records (all organs) | unknown | GitHub | open (per atlas) | none stated | unverified | Low | Low-Med (report text) |
| 32 | Paediatric FAST organ segmentation (Addo et al. 2026) | liver, kidney, spleen, bladder, diaphragm, spine | 1,807 image-mask pairs (no images released) | n/a | GitHub (weights only) | closed (data) | not stated | D | High (if released) | None |
| 33 | Prostate-MRI-US-Biopsy | prostate, 3D TRUS + MRI | 1,151 patients, 102,397 DICOM images (MR+US) | 80.21 | TCIA | open | CC BY 4.0 (older text: CC BY 3.0) | A | None | None |
| 34 | μ-RegPro (MR to TRUS registration) | prostate | 108 paired cases (65/8/35) | 0.11 to 0.12 | Zenodo | open (test hidden) | CC BY-NC-SA 4.0 | A | None | None |
| 35 | Micro-Ultrasound Prostate Segmentation | prostate, micro-US 3D | 75 patients | 3.57 | Zenodo | open | CC BY 4.0 | A | None | None |
| 36 | Annotated MRI and US volumes of the prostate (Fedorov) | prostate | 3 patients | 0.03 | Zenodo | open | CC BY-NC-SA 4.0 | A | None | None |
| 37 | CRTA-PRONOBIS prostate phantom | prostate phantoms | unknown | 1.04 | Kaggle | open | unknown | B | None | None |

No public dataset was found for spleen alone, adrenal, transabdominal pancreas, abdominal wall or
hernia, inflammatory bowel disease, intussusception, adult FAST, bladder, or testis and scrotum
(details in Gaps). Minor Kaggle uploads of unknown origin are in Table 2.

#### Detailed entries

Field numbers follow the task: 1 name/year/paper; 2 content; 3 data type; 4 size; 5 labels;
6 source; 7 host, version, checksums; 8 access; 9 licence; 10 automation; 11 overlaps;
12 burned-in text; 13 large-scale users; 14 verification; 15 epic 1 closeness; 16 liver disease
labels and reference standard.

##### Liver

**1. AUL (Annotated Ultrasound Liver images)**
- 1: AUL; Zenodo 2022-11-02; paper DOI 10.1093/bib/bbac569 (Briefings in Bioinformatics, per
  [TIanCat atlas](https://github.com/TIanCat/open-medical-ultrasound-datasets)). Creators Xu Yiming, Zheng Bowen, Liu Xiaohong, Wu Tao — [Zenodo 7272660](https://zenodo.org/records/7272660)
- 2: liver with focal masses; classes benign, malignant, normal (three archives) — [Zenodo API](https://zenodo.org/api/records/7272660)
- 3: 2D B-mode images. 4: 735 images (435 malignant, 200 benign, 100 normal per the project's
  earlier note [2026-11-18 journal](../../journal/2026/2026-11-18-public-datasets-claude.md)); 0.070 GB in 3 zips — Zenodo API
- 5: outlines of liver and liver mass regions ("annotated to show the outlines, livers, and liver
  mass regions") — Zenodo record. 6: unknown institution (Chinese author names; not stated).
- 7: Zenodo, DOI 10.5281/zenodo.7272660, md5 per file published. 8: open. 9: metadata licence
  CC BY 4.0, but the description says the data "is subject to copyright" and users should contact
  the author — conflict, flag for legal check — Zenodo record. 10: A.
- 11: Kaggle mirror orvile/annotated-ultrasound-liver-images-dataset (70.4 MB, CC BY 4.0) — [Kaggle API search](https://www.kaggle.com/api/v1/datasets/list?search=liver%20ultrasound). 12: unknown.
- 13: UltraBench 2 liver segmentation task (per the project's earlier note [epic1 models note](../epic1-anatomy-segmentation-models-and-papers.md)); rated "Bronze" in the npj survey — [Alsharid et al. 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/)
- 14: verified at the Zenodo record and API on 2026-11-25.
- 15: Med (liver and mass masks; no other organs). 16: lesion class benign/malignant; reference
  standard unknown (paper not read).

**2. B-mode-and-CEUS-Liver (TCIA)**
- 1: "Ultrasound data of a variety of liver masses"; Eisenbrey, Lyshchik, Wessner 2021; no paper
  recommended; DOI 10.7937/TCIA.2021.v4z7-tc39 — [TCIA page](https://www.cancerimagingarchive.net/collection/b-mode-and-ceus-liver/)
- 2: liver masses (HCC and others), TACE (transarterial chemoembolisation) response. 3: DICOM
  B-mode and CEUS; page says cine loops and volumes "expected" later, so current cine content is unclear.
- 4: v2 (2022-02-18): 120 patients, 120 studies, 120 series, 1,859 images, 272.16 GB; v1: 75
  patients, 1,370 images, 208.04 GB. 5: reference standards in a spreadsheet (diagnosis, follow-up,
  treatment); no masks stated. 6: Thomas Jefferson University, Philadelphia, USA; "a variety of"
  scanners with curvilinear probes.
- 7: TCIA, version 2; checksums unknown. 8: open. 9: CC BY 4.0 (one search snippet of older wiki
  text said CC BY 3.0 — current page wins). 10: A (TCIA Data Retriever manifest, or IDC portal).
- 11: v1 is a subset of v2. 12: not addressed (TCIA de-identification in general).
- 13: unknown. 14: verified at the TCIA page on 2026-11-25.
- 15: Low. 16: lesion characterisation by tissue pathology or contrast CT/MRI within 1 month;
  TACE response by pathology, angiography or later imaging — High.

**3. Byra fatty-liver dataset ("Dataset of B-mode fatty liver ultrasound images")**
- 1: Byra et al., Int J CARS 2018, DOI 10.1007/s11548-018-1843-2; Zenodo 2018-08-06 — [Zenodo 1009146](https://zenodo.org/records/1009146)
- 2: liver steatosis in severely obese bariatric-surgery patients (mean BMI 45.9, per a search
  snippet of [arXiv 2307.06507](https://arxiv.org/pdf/2307.06507); unverified). 3: 2D B-mode in one MATLAB .mat file.
- 4: 550 images, 55 patients (38 fatty, 17 not fatty; per the [2026-11-18 journal](../../journal/2026/2026-11-18-public-datasets-claude.md) and the [atlas](https://github.com/TIanCat/open-medical-ultrasound-datasets)); 0.052 GB. 5: per-patient steatosis label and fat percentage (per atlas: classification and regression).
- 6: Medical University of Warsaw and IPPT PAN, Poland — Zenodo creators. 7: Zenodo DOI
  10.5281/zenodo.1009146, md5 published. 8: open. 9: CC BY 4.0. 10: A.
- 11: 10 consecutive frames per patient (near-duplicates within a patient; search snippet,
  unverified); Kaggle mirrors shanecandoit/dataset-of-bmode-fatty-liver-ultrasound-images
  ("Unknown" licence) and mahendarbyra/b-mode-dataset — Kaggle API search. 12: unknown.
- 13: npj survey rates it "Diamond" (highest) — [Alsharid et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/). 14: verified at Zenodo API on 2026-11-25.
- 15: Low. 16: steatosis from liver biopsy (per journal note; paper not re-read) — High.

**4. Saudi NAFLD liver ultrasound dataset**
- 1: "Large annotated ultrasound dataset of non-alcoholic fatty liver from Saudi hospitals",
  Alshagathrh et al., Data in Brief 58:111266 (published 2024-12-27, issue Feb 2025), DOI
  10.1016/j.dib.2024.111266 — [PMC11774810](https://pmc.ncbi.nlm.nih.gov/articles/PMC11774810/)
- 2: NAFLD; steatosis grade 0-3 (3,283 / 2,597 / 2,283 / 1,144 images; 145 ungraded) and fibrosis
  stage 0-4 (1,751 / 7,122 / 1,015 / 203 / 174; 87 ungraded). 3: 2D B-mode PNG (8,772 grey, 1,580
  colour), padded to 768 × 1024 px.
- 4: 10,352 images, 384 patients; size not stated. 5: whole-image labels, no boxes. 6: King Saud
  University Medical City and National Guard Health Affairs, Saudi Arabia; 10 scanner models (GE,
  Philips, Hitachi, Samsung).
- 7: OSF, DOI 10.17605/OSF.IO/C2YG8; OSF API needs login (checked 2026-11-25). 8: DUA: formal
  request on OSF plus a signed confidentiality and use agreement. 9: non-commercial research only;
  commercial use needs permission; article itself CC BY-NC 4.0. 10: C.
- 11: none known. NGHA patient count inconsistent in the paper (64 vs 80). 12: images manually
  cropped to remove identifying text. 13: unknown. 14: verified at PMC on 2026-11-25.
- 15: Low. 16: High: biopsy read by three hepatopathologists, NAS scoring; biopsy-to-scan interval
  not reported.

**5. SMC-LUD (Samsung Medical Center Liver Ultrasound Dataset)**
- 1: "SMC-LUD: Large-Scale B-Mode Liver Ultrasound Dataset for HCC and Hemangioma
  Classification", Scientific Data 2026, DOI 10.1038/s41597-026-07023-7 — [Nature](https://www.nature.com/articles/s41597-026-07023-7); figshare v3 2026-02-05 — [figshare API](https://api.figshare.com/v2/articles/31112716)
- 2: HCC vs haemangioma. 3: 2D B-mode. 4: 5,385 images, 1,021 patients by table (description text
  says 5,466 — conflict in the same record); 1.33 GB single zip.
- 5: class label per image, patient folders, CSV metadata; split train 3,769 / val 1,076 / test 540.
  6: Samsung Medical Center, Seoul, Korea (2015-2024 per search snippet).
- 7: figshare DOI 10.6084/m9.figshare.31112716.v3, md5 published. 8: open. 9: CC BY 4.0 on
  figshare, but text says "non-commercial research use only" — conflict. 10: A.
- 11: M2-US subtask liver_lesion_2cls has 5,466 images (same as the SMC-LUD text count; likely a
  re-release, inference) — [M2-US site](https://m2-us.github.io/). Kaggle mirrors: tofael088 (CC BY-SA 4.0),
  krishndey ("Unknown"), mdnazmushsayeedanik (ODbL) — Kaggle API search.
- 12: yes: "Caliper" subgroups hold 1,402 haemangioma and 1,327 HCC images with calipers; "Clean"
  subgroups 1,267 and 1,389. Patients appear in both subgroups (subtotals 422 and 600 patients are
  below the sums 697 and 978) — figshare record.
- 13: M2-US (inference above). 14: verified at figshare API on 2026-11-25.
- 15: Low. 16: lesion type HCC vs haemangioma; reference standard not read (article not opened).

**6. BEHSOF**
- 1: BEHSOF; 2024 (npj survey ref. 116); original listed at figshare.com/articles/dataset/BEHSOF/26389069 per the [atlas](https://github.com/TIanCat/open-medical-ultrasound-datasets), but that page returned HTTP 403 and the figshare API returned "Entity not found" (2026-11-25).
- 2: NAFLD vs non-NAFLD. 3: original folders held .avi videos, .pdf reports and .jpeg images per patient.
- 4: 1,669 images (1,517 NAFLD, 152 non-NAFLD), 113 people; 0.35 GB Kaggle copy. 5: image class;
  metadata age, sex, BMI, steatosis stage, anthropometric and biochemical features.
- 6: unknown. 7: original host figshare (unreachable); Kaggle copy mahendarbyra/behsof-dataset,
  no checksums. 8: open copy. 9: Kaggle says "Other (specified in description)". 10: B (copy).
- 11: Kaggle copy adds preprocessing and an augmented balanced version (3,034 images). 12: unknown.
- 13: unknown. 14: Kaggle copy verified at [Kaggle API](https://www.kaggle.com/api/v1/datasets/view/mahendarbyra/behsof-dataset) on 2026-11-25; original unverified.
- 15: Low. 16: "clinical diagnosis" NAFLD label and steatosis stage; reference not stated — Med.

**7. SYSU-FLL-CEUS**
- 1: Liang et al., ISBI 2014 and IEEE TMI 2015 ("Recognizing focal liver lesions in CEUS with
  dynamically trained latent structured models"); [arXiv 1502.00750](https://arxiv.org/pdf/1502.00750)
- 2: focal liver lesions: 186 HCC, 109 haemangioma, 58 FNH (focal nodular hyperplasia); 186
  malignant, 167 benign. 3: CEUS clips, 768 × 576 px. 4: 353 lesion instances; full size unknown
  (Kaggle copy 8.2 to 11.0 GB).
- 5: lesion class per clip. 6: First Affiliated Hospital of Sun Yat-sen University, China; Toshiba
  Aplio SSA-770A; pre-operative scans — [GitHub](https://github.com/lemondan/Focal-liver-lesions-dataset-in-CEUS)
- 7: GitHub holds a small sample; full set by email for academic use; the README also lists a
  Google Drive folder (not opened). 8: req. 9: none stated. 10: C.
- 11: Kaggle copy hoangviet2302/sysu-ceus-fll (Apache-2.0 label) and Hugging Face copy
  Gokulapriyan/SYSU-CEUS — Kaggle API, [HF API](https://huggingface.co/api/datasets?search=ceus). 12: unknown.
- 13: used for a 3-class lesion task in [arXiv 2509.11752](https://arxiv.org/pdf/2509.11752) (search snippet; unverified).
- 14: verified at GitHub README on 2026-11-26. 15: None. 16: lesion type; reference standard not read (pre-operative patients suggest pathology; unverified).

**8. US-Liver (HSQformer test sets)**
- 1: Lu et al., npj Digital Medicine 8:500 (2025), "AI enhanced diagnostic accuracy and workload
  reduction in HCC screening"; [arXiv 2502.03772](https://arxiv.org/abs/2502.03772) — [HF card](https://huggingface.co/datasets/chaoyinshe/US-Liver)
- 2: B-mode liver images for HCC screening. 3: 2D B-mode. 4: two zips ("test_3", "test_7"), 0.22 GB;
  image counts not stated. 5: not read. 6: Third Affiliated Hospital of Sun Yat-sen University.
- 7: Hugging Face, LFS sha256 per file. 8: open (not gated). 9: Apache-2.0 (card). 10: A.
- 11: identical copy SNM0312/US-Liver (2026-02-10) — HF API. Only test subsets are released.
- 12: unknown. 13: unknown. 14: verified at HF API and card on 2026-11-26.
- 15: Low. 16: HCC screening labels presumed; not read — Med.

**9. Liver fibrosis F0-F4 (Joo et al. 2023), Kaggle re-upload**
- 1: Joo et al., "Classification of Liver Fibrosis From Heterogeneous Ultrasound Image", IEEE
  Access 11:9920-9930 (2023), as cited by the uploader — [Kaggle](https://www.kaggle.com/datasets/vibhingupta028/liver-histopathology-fibrosis-ultrasound-images)
- 2: METAVIR fibrosis stages F0-F4. 3: 2D JPG. 4: F0 2,114, F1 861 images (other classes not read;
  F4 27%, F1-F3 13% each per the description); size 0.21 GB (search API) or 1.89 GB (dataset API).
- 5: stage class folders. 6: Seoul St. Mary's Hospital (train/val), Eunpyeong St. Mary's Hospital (test), Korea.
- 7: Kaggle only (uploader not an author); no checksums. 8: open. 9: CC BY-SA 4.0 set by the
  uploader; the authors' terms unknown. 10: B.
- 11: augmented derivative sazzadhossain2611/liver-histopathology-ultrasound-image-augmented
  (1.48 GB); a 2026 thesis reports MD5 duplicate images in this set (search snippet; unverified).
- 12: unknown. 13: unknown. 14: Kaggle API verified 2026-11-25; primary source unverified.
- 15: Low. 16: fibrosis stage; reference standard not read (the title says "Histopathology", unverified).

**10. CLUST 2015 (Challenge on Liver Ultrasound Tracking)**
- 1: CLUST 2014/2015, MICCAI workshops; 2014 benchmark paper in Phys Med Biol ([PMC5454593](https://pmc.ncbi.nlm.nih.gov/articles/PMC5454593/))
- 2: liver of volunteers and patients under free breathing. 3: 2D+t (.png) and 3D+t (.mha).
- 4: 86 sequences: 64 2D+t, 22 3D+t; 40% training with annotations, 60% test (first-frame
  annotations only). 5: tracked landmarks (vessel points). 6: several centres (not itemised).
- 7: login-protected server at ETH; site now at Uppsala University — [CLUST data](https://caim.research.it.uu.se/clust/data.html). 8: username and password by email; the site says it is moving and "unable to process any access" requests (search snippet of the site).
- 9: data "solely for the purpose of participating" in CLUST; no sharing. 10: D (paused).
- 11: usliverseq (entry 11) is a public part. 12: unknown. 13: unknown.
- 14: verified at the CLUST data page on 2026-11-25. 15: Low. 16: None.

**11. usliverseq (2D ultrasound sequences of the liver)**
- 1: CLUST "Subset of Ultrasound Images"; cite Petrusca et al. (Invest Radiol 48(5):333-340) and De
  Luca et al. (MICCAI 2013) — [CLUST subset page](https://caim.research.it.uu.se/clust/partOfImages.html)
- 2-4: liver of healthy volunteers, free breathing 5-10 min; nine 2D sequences (page) vs seven
  (Kaggle copy text). 5: none. 6: Geneva University Hospital; Siemens Antares, CH4-1 probe (Kaggle copy).
- 7: direct zip at data.vision.ee.ethz.ch/cvl/datasets_extra/usliverseq.zip; checksums none.
  8: open. 9: none stated. 10: A.
- 11: Kaggle mp4 copy aryashah2k/2d-ultrasound-sequences-of-the-liver (CC0 label) and
  [Academic Torrents mp4](https://academictorrents.com/details/4d107e9fd4b00fa797504d6cd0131744c9f31e81). 12: unknown. 13: unknown.
- 14: verified at the CLUST subset page on 2026-11-25. 15: Low. 16: None.

**12. LUS-7Seg (Kaggle only, origin unverified)**
- 1: LUS-7Seg_Dataset, uploaded 2026-11-23 by Md. Nazmush Sayeed Anik — [Kaggle](https://www.kaggle.com/datasets/mdnazmushsayeedanik/lus-7seg-dataset)
- 2: 7 hepatobiliary standard planes of healthy people. 3: 2D. 4: 10,507 images, 2,415 people;
  1.09 GB (dataset API) or 0.87 GB (search API). 5: plane class plus pixel masks of liver
  parenchyma and gallbladder ("expert-verified"). 6: unknown.
- 7: Kaggle; no checksums. 8: open. 9: CC BY-SA 4.0 set by the uploader. 10: B.
- 11: no paper or primary repository found by two searches; the same uploader re-hosts SMC-LUD
  under ODbL, so this may also be a re-host. 12: unknown. 13: unknown.
- 14: Kaggle API verified 2026-11-25; origin unverified. 15: High if genuine. 16: None.

**13. AD-MAGNet Liver Ultrasound Dataset**
- 1: Mendeley Data v1, 2026-09-15, DOI 10.17632/74pp4d9jfg.1 — [Mendeley API](https://data.mendeley.com/public-api/datasets/74pp4d9jfg)
- 2: normal, benign (haemangioma, cyst, FNH), malignant (HCC, cholangiocarcinoma, metastases);
  liver function test metadata; Indian setting. 4: text claims an "18,000-image held-out test set",
  but the only file is a 75.9 MB archive — doubtful. 5: class labels, metadata.
- 7: Mendeley, sha256 published. 8: open. 9: CC BY 4.0 (Kaggle copy ujjwalsinha01 says MIT). 10: A.
- 11: origin unknown; may repackage other sets (unverified). 14: verified at Mendeley API on 2026-11-25.
- 15: Low. 16: lesion class; reference not stated — Med, low trust.

**14. Dataset on NAFLD Severity Classification with Ultrasound Liver Image & Clinical Data**
- 1: Mendeley Data v4, 2026-10-05, DOI 10.17632/6rg4hk6728.4; University of Frontier Technology,
  Bangladesh — [Mendeley API](https://data.mendeley.com/public-api/datasets/6rg4hk6728)
- 2: NAFLD "severity grades (Normal, Benign, Malignant)" — labels do not fit NAFLD; clinical table
  (age, sex, BMI, ALT, AST, waist, glucose, lipids). 4: one 8.2 MB zip; image count not stated.
- 7: sha256 published. 8: open. 9: CC BY 4.0. 10: A. 14: verified 2026-11-25.
- 15: Low. 16: Low-Med; reference not stated.

##### Gallbladder and bile ducts

**15. GBCU (Gallbladder Cancer Ultrasound)**
- 1: Basu et al., CVPR 2022, "Surpassing the Human Accuracy: Gallbladder Cancer Detection from USG
  with Curriculum Learning"; DOI 10.1109/CVPR52688.2022.02022 (atlas) — [GBCU page](https://gbc-iitd.github.io/data/gbcu)
- 2: normal 432, benign 558, malignant 265 images. 3: 2D B-mode, 801-1556 × 564-947 px.
- 4: 1,255 images, 218 patients; split 1,133 / 122 with no patient overlap. 5: image class
  (biopsy-confirmed); box around gallbladder plus adjacent liver; boxes on stones, wall thickening, malignancy.
- 6: PGIMER Chandigarh, India; GE Logiq S8. 7: download link emailed; size unknown.
- 8: DUA: signed licence agreement emailed to the authors; only permanent staff or faculty may sign.
  9: terms in the agreement PDF (not read). 10: C. 11: same hospital and device as GBUSV.
- 12: unknown. 13: npj survey "Silver". 14: verified at the GBCU page on 2026-11-25.
- 15: Med (gallbladder region box). 16: None (gallbladder, not liver).

**16. GBUSV (Gallbladder Ultrasound Video)**
- 1: Basu et al., MICCAI 2022; DOI 10.1007/978-3-031-16440-8_41 (atlas) — [GBUSV page](https://gbc-iitd.github.io/data/gbusv)
- 2: malignant vs non-malignant (32 + 32 videos). 3: B-mode video, 360 × 480 px.
- 4: 64 videos, 15,800 frames (12,251 malignant, 3,549 non-malignant). 5: video-level class only.
- 6: PGIMER Chandigarh; GE Logiq S8, C-1-5D probe. 7-10: as GBCU (C).
- 12: frames centre-cropped "to anonymize patient information and annotations". 14: verified 2026-11-25.
- 15: Low. 16: None.

**17. UIdataGB (Gallblader Diseases Dataset)**
- 1: Turki et al., "UIdataGB: Multi-class ultrasound images dataset for gallbladder disease
  detection", Data in Brief 2024 (search snippets); Mendeley v2 2024-07-09, DOI 10.17632/r6h24d2d3y.2 — [Mendeley API](https://data.mendeley.com/public-api/datasets/r6h24d2d3y)
- 2: 9 classes: gallstones; abdomen and retroperitoneum; cholecystitis; membranous and
  gangrenous cholecystitis; perforation; polyps and cholesterol crystals; adenomyomatosis;
  carcinoma; other wall thickening. 3: 2D, 900 × 1200 px (snippet).
- 4: 10,692 images, 1,782 people (snippets of [DOAJ record](https://doaj.org/article/cb3c2428602a465a9918e1d536a27c6e) and Academic Torrents); 2.04 GB in 9 zips (Mendeley).
- 5: class folders. 6: unknown (not in Mendeley metadata). 7: sha256 published; mirrors on
  [figshare 25020821](https://figshare.com/articles/dataset/Gallblader_Diseases_Dataset/25020821) (1.9 GB) and Academic Torrents. 8: open. 9: CC BY 4.0. 10: A.
- 11: three hosts of the same files (verify hashes before dedup). 12: unknown.
- 14: Mendeley API verified 2026-11-26; counts from snippets (unverified). 15: Low (gallbladder disease classes, one class is "abdomen and retroperitoneum"). 16: None.

##### Kidney

**18. Open Kidney Ultrasound Data Set**
- 1: Singla et al., ASMUS 2023 workshop, DOI 10.1007/978-3-031-44521-7_15; [arXiv 2206.06657](https://arxiv.org/abs/2206.06657) — [GitHub](https://github.com/rsingla92/kidneyUS)
- 2: native and transplanted kidneys of adults with chronic kidney disease, donors, transplant
  recipients; 2015-01 to 2019-09, including bedside and ICU scans.
- 3: 2D B-mode PNG (no DICOM, no cines). 4: "over 500" images, one per patient (atlas: 534 files,
  514 unique patients and images). 5: polygon masks of 4 classes, two expert sonographers; view label; native/transplant label.
- 6: approval H21-02375 (University of British Columbia); Philips, GE, Acuson, Siemens, Toshiba, SonoSite.
- 7: version 1.0; size unknown. 8: UBC Qualtrics registration, manual review against spam and
  commercial use, link by email. 9: CC BY-NC-SA (version not stated). 10: C.
- 11: none known. 12: not mentioned. 13: UltraSam US-43d ("kidneyUS") — [UltraSam GitHub](https://github.com/CAMMA-public/UltraSam); UltraBench 2 kidney task (earlier project note).
- 14: verified at GitHub README on 2026-11-25. 15: High (kidney regions; one organ). 16: None.

**19. Kidney Ultrasound Images "Stone" and "No Stone"**
- 1: Mendeley v1 2024-08-27, DOI 10.17632/h6jc4xm4py.1; Punjabi University (library account) — [Mendeley API](https://data.mendeley.com/public-api/datasets/h6jc4xm4py)
- 2: normal 4,414, stone 5,002 images. 4: 9,416 images; 225.4 MB. 6: several scan centres; Samsung RS85, HS60, RS80A, HS70A.
- 7: sha256 published. 8: open. 9: CC BY 4.0. 10: A.
- 11: Kaggle mirrors gurjeetkaurmangat (CC0), imtkaggleteam (CC BY-SA 4.0; 66,341 downloads; calls
  it a "Kidney Stone Detection Challenge" set, 512 × 512 px), makiw4. 14: verified 2026-11-26.
- 15: Low. 16: None.

**20. CT2USforKidneySeg**
- 1: MICCAI 2021 submission "CT2US: Cross-modal Transfer Learning for Kidney Segmentation in
  Ultrasound Images with Limited Data" (SIAT) — [Kaggle](https://www.kaggle.com/datasets/siatsyx/ct2usforkidneyseg)
- 2-3: CycleGAN-synthesised kidney ultrasound from CT, plus a transition set. 4: 0.27 GB; counts not read.
- 7: Kaggle; GPL 2 (an odd licence for data). 8: open. 10: B. 11: source CT set not read.
- 14: Kaggle API verified 2026-11-25. 15: Med (kidney masks expected; not checked). 16: None.

**21. Sensing ULM kidney (raw RF and IQ)**
- 1: Denis et al., "Sensing Ultrasound Localization Microscopy reveals glomeruli in rats and
  humans" — [Zenodo 11395562](https://zenodo.org/records/11395562) (RF, v2, 2024-05-30) and [Zenodo 6811910](https://zenodo.org/records/6811910) (IQ, v1)
- 3: raw RF (34.91 GB, 62 files) and IQ (18.68 GB) microbubble sequences; file names show rat
  kidney; human files not confirmed. 7: md5 published. 8: open. 9: CC BY 4.0. 10: A.
- 14: Zenodo API verified 2026-11-25. 15: None. 16: None.

##### Pancreas, stomach and bowel (including EUS)

**22. LEPset**
- 1: LEPset, Zenodo v1.0 2023-06-15, DOI 10.5281/zenodo.8041285 — [Zenodo](https://zenodo.org/records/8041285)
- 2: pancreatic cancer vs not, EUS. 4: 420 patients; 3,500 labelled images (cancer: 280 patients,
  1,680 images; non-cancer: 140 patients, 1,820 images) plus 8,000 unlabelled; 0.78 GB.
- 6: Changhai Hospital, Naval Medical University, Shanghai. 7: md5 published. 8: open. 9: CC BY 4.0. 10: A.
- 13: npj survey "Steel". 14: verified 2026-11-25. 15: None (EUS). 16: None.

**23. GIST514-DB** and **24. C-TRUS**: listed by the [atlas](https://github.com/TIanCat/open-medical-ultrasound-datasets) and the [npj survey](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/) only. GIST514-DB: EUS GI stromal tumours, 514 cases, [GitHub WuJunde/Query2](https://github.com/WuJunde/Query2), paper DOI 10.1016/j.compbiomed.2022.106424. C-TRUS: colon wall segmentation, 827 images, 13 patients, [GitHub wwu-mmll/c-trus](https://github.com/wwu-mmll/c-trus), DOI 10.1007/978-3-031-73647-6_10. Licences and automation unverified. Epic 1 and 3: None.

**25. Regensburg Pediatric Appendicitis Dataset**
- 1: Marcinkevičs et al., Med Image Anal 2023, DOI 10.1016/j.media.2023.103042 (atlas); Zenodo v1.03
  2023-02-23, DOI 10.5281/zenodo.7711412 (concept 10.5281/zenodo.7669214 resolves to the same) — [Zenodo](https://zenodo.org/records/7711412)
- 2: children with abdominal pain; views of right lower quadrant, appendix, intestines, lymph nodes,
  reproductive organs (1-15 views per child). 3: 2D B-mode.
- 4: release 782 records, 2,097 images; paper 579 patients, 1,709 images (atlas); 0.52 GB.
- 5: diagnosis, management, severity; lab values, scores, sonographic findings (tabular). 6:
  Children's Hospital St. Hedwig, Regensburg, Germany; ETH Zurich.
- 7: md5 published. 8: open. 9: CC BY-NC 4.0. 10: A.
- 11: Kaggle mirrors joebeachcapital (CC BY-NC 4.0), zsinghrahulk (CC0 label, wrong);
  ahsaniqbalai/appendicitis-ultrasound (87 MB, no description) may be a subset (unverified).
- 13: npj survey "Bronze". 14: verified 2026-11-25. 15: Low (lower abdomen). 16: None.

##### Abdominal multi-organ, FAST and POCUS

**26. Abdominal Ultrasound Image Dataset for Organ Classification and Disease Detection (Karim and Ball)**
- 1: Scientific Data, published 2026-11-23, DOI 10.1038/s41597-026-08897-3 — [Nature](https://www.nature.com/articles/s41597-026-08897-3); data DOI 10.54718/LZXF6315 — [Scholars Junction](https://scholarsjunction.msstate.edu/research-data/5/)
- 2: 10 classes: abdominal aorta, gallbladder, hepatic vein, kidneys, liver, ovaries, pancreas,
  portal vein, spleen, and a pelvic class (bladder, prostate, uterus); normal vs abnormal; ascites.
- 3: 2D JPEG. 4: 5,468 unique images (13,088 file occurrences across task folders), 563 patients;
  1,425.7 MB. 5: folder class labels; patient metadata sheet with free-text remarks; 4 JSON files
  of text-overlay boxes; no masks or boxes of organs.
- 6: MH Samorita Medical College and Hospital, Dhaka, Bangladesh; GE Voluson E6, convex 3.5-5 MHz.
- 7: Mississippi State University repository (bepress); checksums not seen. 8: open. 9: CC BY 4.0.
  10: A (single file; not tested).
- 11: Patient_Wise folder repeats 2,037 Radiologist-2 images; Radiologist-1 folders reorganise one
  master set; the article advises hash and perceptual dedup. Kaggle copy sifatkarim (5,005 images,
  CC BY-NC-SA 4.0 — licence differs) and Hugging Face copy Sif92/ultrasound-organ-dataset.
- 12: yes: scanner overlays and anatomical text retained; CRAFT text-box coordinates supplied;
  masking overlays changed cross-radiologist accuracy by only 0.72 points.
- 13: unknown (new). 14: verified at Scholars Junction and Nature on 2026-11-25.
- 15: Med (organ/view class labels for 9 upper-abdominal classes). 16: Low (normal/abnormal).

**27. US simulation & segmentation (Vitale et al.; "AbdomenUS" in UltraSam)**
- 1: Vitale, Orlando, Iarussi, Larrabide, "Improving realism in patient-specific abdominal
  ultrasound simulation using CycleGANs", Int J CARS 15(2):183-192 (2020) — [Kaggle](https://www.kaggle.com/datasets/ignaciorlando/ussimandsegm)
- 2: abdominal organs; label colours for liver, kidney, pancreas, vessels, adrenals, gallbladder,
  bones, spleen. 3: 2D real B-mode and ray-cast simulated images from CT.
- 4: 617 real images from 11 healthy volunteers (61 annotated: liver, kidneys, gallbladder, spleen,
  vessels); 926 simulated images from 13 VISCERAL Anatomy3 CT scans with silver-standard labels;
  6,151 files, 2.10 GB including a 0.46 GB pretrained model.
- 6: Argentina (Kaggle Open Data Research Grant); SonoSite M-Turbo; views include intercostal,
  subcostal, FAST right and left upper quadrant.
- 7: Kaggle, 6 versions; v6 (2026-09-22) added an "ABME26" train/val/test folder (2,072 files;
  file names suggest CT-derived images; content unknown). 8: open. 9: "Data files © Original
  Authors" (no open licence). 10: B.
- 11: Kaggle merge darsh22blc1378/abdominal-ultrasound-images (MIT label) combines it with nerve
  and breast sets. 12: unknown. 13: UltraSam US-43d ("AbdomenUS") — [UltraSam GitHub](https://github.com/CAMMA-public/UltraSam).
- 14: verified at Kaggle API on 2026-11-25. 15: High for organ set, but real annotated part is 61 images. 16: None.

**28. Clinical Ultrasound Image Repository (MONAI)** — [AWS registry](https://registry.opendata.aws/clinical-ultrasound-image-data/)
- 2,000 studies from 2,000 people, about one third each abdominal, cardiac, OB/GYN; labels, image
  count, size and format not stated; S3 bucket clinical-ultrasound-image-repository (us-west-2),
  `--no-sign-request`; CC BY-NC 4.0; static. Automation A. Burned-in text not stated.
  Verified 2026-11-26. Epic 1: Low (unlabelled abdominal studies). Epic 3: None known.

**29. USenhance 2023** — MICCAI 2023 image-enhancement challenge; thyroid, carotid, liver, breast,
kidney; 1,050 training pairs and 364 test inputs, 109 patients; "open download, CC BY-SA" per the
[atlas](https://github.com/TIanCat/open-medical-ultrasound-datasets); design DOI 10.5281/zenodo.7841250. The
[challenge page](https://ultrasoundenhance2023.grand-challenge.org/datasets/) returned HTTP 403 (2026-11-26), so all facts are unverified. Epic 1: Low. Epic 3: None.

**30. M2-US** — "A Large-scale Multi-domain and Multi-task Ultrasound Image Dataset", Zenodo
2026-10-22, DOI 10.5281/zenodo.23558392, CC BY 4.0, 7.90 GB in train/val/test zips with md5 —
[Zenodo](https://zenodo.org/records/23558392); 67,620 images from public sets and retrospective
cohorts, 26 subtasks; abdominal subtasks liver_lesion_2cls (5,466) and organ_cls (366), sources
not named — [M2-US site](https://m2-us.github.io/). Automation A. Overlap: liver subtask likely equals SMC-LUD (inference). Verified 2026-11-25/26.

**31. Chinese ultrasound report-generation set (Li et al.)** — IEEE TMI 2024, DOI
10.1109/TMI.2024.3424978; breast, thyroid, liver images with reports; paper 7,390 patients, archive
7,364 records and 17,149 images; open download, no stated licence — per [atlas](https://github.com/TIanCat/open-medical-ultrasound-datasets) and [npj survey](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/); [GitHub](https://github.com/LijunRio/Ultrasound-Report-Generation) not opened. Unverified. Epic 3: Low-Med (report text).

**32. Paediatric FAST organ segmentation (Addo et al. 2026)** — medRxiv 2026-10-29,
DOI 10.64898/2026.10.27.26366648 (per [epic1 note](../epic1-anatomy-segmentation-models-and-papers.md)): 200 clips, 1,807
image-mask pairs, one centre. The [GitHub repo](https://github.com/Kornblith-Lab/US-AbdomenSeg) releases
U-Net and EVIT-UNet weights only; test-set masks per organ: bladder 344, kidney 306, liver 445, spleen
172, spine 273, diaphragm 267; no data link (verified 2026-11-26). Automation D. Epic 1: High if released.

##### Urology

**33. Prostate-MRI-US-Biopsy (TCIA)** — [TCIA page](https://www.cancerimagingarchive.net/collection/prostate-mri-us-biopsy/)
- Natarajan et al. 2020, DOI 10.7937/TCIA.2020.A61IOC1A; v2 2023-10-20: 1,151 patients, 2,799
  studies, 4,819 series, 102,397 images (MR and US); 80.21 GB (DICOM 79.61 GB; STL 274 MB; biopsy
  overlays 333 MB). 3D TRUS (Hitachi Hi-Vision 5500 or Noblus, Artemis tracking); 3T MRI.
- Labels: prostate surface and target STL, biopsy core coordinates, Gleason grades, UCLA suspicion
  scores. UCLA Clark Urology Center. CC BY 4.0 (page); a search snippet of the old wiki says CC BY 3.0.
- Download: TCIA Data Retriever manifest or IDC (DICOM, A); STL and overlays via IBM Aspera
  (automation unverified). Derived [DICOM annotation set, Zenodo 10069911](https://zenodo.org/records/10069911)
  (0.145 GB, CC BY 4.0, md5). Kaggle copy dsptlp/prostate-mri-us-biopsy (37.8 GB, CC0 label, wrong).
  Verified 2026-11-25. Epic 1 and 3: None.

**34. μ-RegPro (MR to Ultrasound Registration for Prostate)** — MICCAI 2023 (ASMUS) — [site](https://muregpro.github.io/)
- Data: [Zenodo 7870105](https://zenodo.org/records/7870105) v1.0.0 (train.zip 109.5 MB, md5) and
  Zenodo 8004388 v1.1.0 (2023-06-05, 0.12 GB); CC BY-NC-SA 4.0; UCL. 108 paired MR-TRUS cases
  (65 train, 8 val, 35 test, per atlas); landmarks and gland labels; test labels held by organisers.
  Registration by email requested for participation. Automation A (train). Verified 2026-11-25.

**35. Micro-Ultrasound Prostate Segmentation Dataset** — [Zenodo 10475293](https://zenodo.org/records/10475293)
- Jiang et al., "MicroSegNet", Comput Med Imaging Graph 2024, DOI 10.1016/j.compmedimag.2024.102326;
  75 patients (55 train, 20 test) from micro-US-guided biopsy at University of Florida; NIfTI; expert
  and non-expert prostate masks (several reader levels in test); 3.57 GB, md5; CC BY 4.0. Automation A.
  Verified 2026-11-25.

**36. Annotated MRI and ultrasound volume images of the prostate (Fedorov et al.)** — [Zenodo 16396](https://zenodo.org/records/16396)
- 3 patients, MR and brachytherapy-planning US volumes (NRRD), whole-gland masks and fiducials;
  Brigham and Women's Hospital; 34 MB, md5; CC BY-NC-SA 4.0; paper DOI 10.1007/s11548-015-1180-7. A. Verified 2026-11-25.

**37. CRTA-PRONOBIS prostate phantom** — [Kaggle](https://www.kaggle.com/datasets/lukaiktar/crta-pronobis-prostate-phantom-ultrasound-dataset);
CIRS 053L and 070L phantoms, made with the MedAP tool; 1.04 GB; licence unknown; B. Verified 2026-11-25.

#### Minor uploads of unknown origin

Table 2. Kaggle and Hugging Face uploads in scope whose origin, counts or licence could not be
traced to a primary source (all read from the [Kaggle API](https://www.kaggle.com/api/v1/datasets/list?search=abdominal%20ultrasound) or HF API on 2026-11-25/26). Treat as low trust; likely re-uploads or scraped teaching images.

| Upload | Content stated | Size | Licence label | Flag |
|---|---|---|---|---|
| gaveshdissanayake/liver-ultrasound-dataset-normal-mild-severe | liver normal/mild/severe (fatty liver) | 33 MB | CC BY-SA 4.0 | no source, 2026 |
| nonpat/i-squared-liver-ultrasound-detection-1 | liver detection | 3.3 GB | unknown | no description |
| aneerbansaha/gallbladder-cancer | gallbladder 5 classes (abnormal, benign, malignant, normal, stone) | 156 MB | MIT | possible unlicensed GBCU-like re-upload (unverified) |
| rahult25/cholecystitis-multimodal-image-dataset | normal vs chronic cholecystitis, laparoscopic + ultrasound | 1.45 GB | CC BY-SA 4.0 | no source, 2026 |
| rahult25/multimodal-gi-disease-image-dataset | achalasia, normal, pyloric stenosis; endoscopy + ultrasound | 1.98 GB | CC BY-NC-SA 4.0 | no source, 2026 |
| zaynebnouiri/renal-data | kidney failure, "clinical AI challenge" | 17 MB | "academic, non-commercial" | challenge not named |
| shriyakathuria/pancreas-ultrasound-60-images; liver-45-ultrasound | pancreas 60, liver 45 images | 4 MB; 3 MB | unknown; CC0 | tiny |
| wangdaming1/classification-ultrasound-13-datastes | bundle of 13 classification sets | 784 MB | MIT | no description |
| InfoBayAI/Ultrasound-USG-Scans-With-Findings-Dataset (HF) | USG scans with findings | 0.01 GB | CC BY 4.0, gated | vendor sample, gated |

Roboflow only (epic 2): liver_ultrasound (400 images, 14 classes), Ultrasound Normal Kidney Image
(1,080 images; kidney, liver, spleen instance masks), Liver Ultrasound Semantic Segmentation (100
images, 12 classes), two kidney-stone-ultrasound projects — per the [atlas](https://github.com/TIanCat/open-medical-ultrasound-datasets), the [npj survey](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/) and search results.

### Inferences
- For epic 1, the only multi-organ upper-abdomen masks on real images are tiny (61 real images in
  the Vitale set) or unverified (LUS-7Seg). The realistic plan is: AUL (liver), Open Kidney
  (kidney), the Vitale set (multi-organ, mostly simulated), and, if its origin checks out,
  LUS-7Seg (liver, gallbladder). The Karim and Ball set (5,468 images) and the AWS MONAI set add
  organ-class or unlabelled abdominal images for pretraining or view classification.
- For epic 3, the steatosis and fibrosis labels with a biopsy reference are in the Saudi NAFLD set
  (needs a signed agreement, tier C) and the Byra set (open, but 55 patients). Lesion-type labels
  are in SMC-LUD, TCIA CEUS-Liver, AUL and SYSU-FLL-CEUS. The Kaggle fibrosis set is the only
  open F0-F4 set, but it is a re-upload by a non-author, so its licence is not trustworthy.
- Tier A (no login) covers Zenodo, figshare, Mendeley Data, TCIA or IDC, the AWS bucket and
  non-gated Hugging Face. Kaggle needs a user token (B). GBCU, GBUSV, Open Kidney, Saudi NAFLD and
  SYSU-FLL-CEUS need a manual request (C). CLUST is closed for now (D).
- Licence conflicts inside one record (AUL, SMC-LUD) and between mirrors (Karim and Ball:
  CC BY 4.0 vs CC BY-NC-SA 4.0; Regensburg: CC BY-NC vs CC0) mean the original host's licence
  should be recorded, not the mirror's.

### Gaps
- **Not found (searched Kaggle, Hugging Face, Zenodo and the web):** public ultrasound sets for
  spleen alone, adrenal, transabdominal pancreas, abdominal wall or hernia, inflammatory bowel
  disease (Zenodo bowel-ultrasound records found are restricted article data), intussusception,
  adult FAST, bladder (only the pelvic class of entry 26, the Karim and Ball set), testis or scrotum, liver elastography
  images, and liver RF data with MRI-PDFF (magnetic resonance proton density fat fraction).
- **Primary source not reached:** BEHSOF figshare original (HTTP 403, API "not found"); LUS-7Seg
  (no paper or repository found); Joo et al. fibrosis data (authors' own release not checked);
  USenhance 2023 (Grand Challenge 403); the Chinese report set, GIST514-DB and C-TRUS (atlas only);
  CT2US source CT and counts; the "Ultrasound Elastography" liver set from Concordia University
  (2,000 items, npj survey refs. 81-84; not opened).
- **Dead or paused:** CLUST full data (access paused while the site moves).
- **Datasets with no access route seen (abstracts do not say they are public):** liver lesion
  segmentation benchmark, Comput Med Imaging Graph 2025, DOI 10.1016/j.compmedimag.2025.102523 ([Europe PMC](https://europepmc.org/article/MED/40112652));
  kidney segmentation set of 44,880 images, Interdiscip Sci 2024, DOI 10.1007/s12539-024-00620-3
  ([Europe PMC](https://europepmc.org/article/MED/38413547)); Wang et al. 2026 upper-abdominal
  standard sections (465 videos, 5,535 frames; per the epic1 note); a private set of 34,711
  abdominal images from 2,063 patients (Frontiers in AI 2025, search snippet); Cheng et al. 2021
  FAST Morison's pouch ([PMC8494971](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8494971/)); a
  fibrosis set of 7,920 images from 933 patients (BMC Med Imaging 2024, search snippet); full
  training data behind US-Liver; paediatric FAST masks (entry 32, Addo et al. 2026).
- **Not checked:** dataset lists of SAMUS (US30K), USFM, OpenUS, USF-MAE, EchoCare, MedSAM,
  SA-Med2D-20M and BiomedParse, so field 13 is "unknown" for most entries; Science Data Bank and
  IEEE DataPort were not searched; image counts behind TCIA CEUS cine loops.

## Q2. Which are subsets, re-releases, merges or mirrors, and which have known duplicates?

### Takeaway
Most Kaggle and Hugging Face copies mirror a Zenodo, figshare, Mendeley or TCIA original, often
with a different (and sometimes wrong) licence label. Known within-dataset duplicates are in the
Karim and Ball set (task folders repeat images), SMC-LUD (patients in both "clean" and "caliper"
groups), Byra (10 frames per patient) and the Kaggle fibrosis set (MD5 duplicates reported).

### Cited Findings
Table 3. Overlap map for the dedup step (sources in the Q1 entries).

| Original | Copies, subsets or merges | Note |
|---|---|---|
| Byra fatty liver (Zenodo 1009146) | Kaggle shanecandoit; mahendarbyra/b-mode-dataset | 10 consecutive frames per patient (snippet) |
| AUL (Zenodo 7272660) | Kaggle orvile | — |
| SMC-LUD (figshare 31112716) | Kaggle tofael088, krishndey, mdnazmushsayeedanik; likely M2-US liver_lesion_2cls (5,466) | clean vs caliper groups share patients |
| BEHSOF (figshare, unreachable) | Kaggle mahendarbyra (plus augmented copy inside) | — |
| SYSU-FLL-CEUS (GitHub sample + request) | Kaggle hoangviet2302; HF Gokulapriyan/SYSU-CEUS | — |
| Joo et al. fibrosis (IEEE Access 2023) | Kaggle vibhingupta028; augmented sazzadhossain2611 | MD5 duplicates reported (unverified) |
| CLUST 2015 | usliverseq zip (public subset); Kaggle aryashah2k mp4; Academic Torrents mp4 | — |
| US-Liver (HF chaoyinshe) | HF SNM0312 (same files) | test subsets only |
| UIdataGB (Mendeley r6h24d2d3y) | figshare 25020821; Academic Torrents | — |
| Kidney stone (Mendeley h6jc4xm4py) | Kaggle gurjeetkaurmangat, imtkaggleteam, makiw4 | — |
| Karim and Ball (DOI 10.54718/LZXF6315) | Kaggle sifatkarim (5,005 images, NC licence); HF Sif92 | 13,088 files for 5,468 unique images; 2,037 Patient_Wise duplicates |
| Vitale set (Kaggle ussimandsegm) | Kaggle darsh22blc1378 merge (with nerve and breast sets) | simulated part derived from 13 VISCERAL CT scans |
| Regensburg (Zenodo 7711412) | Kaggle joebeachcapital, zsinghrahulk; possibly ahsaniqbalai | — |
| B-mode-and-CEUS-Liver v2 | v1 (75 patients) is a subset | — |
| Prostate-MRI-US-Biopsy v2 | v1 subset; Zenodo 10069911 DICOM annotations; Kaggle dsptlp copy | — |
| μ-RegPro Zenodo 7870105 v1.0.0 | Zenodo 8004388 v1.1.0 | — |
| AD-MAGNet (Mendeley) | Kaggle ujjwalsinha01 (MIT label) | origin unknown |
| GBCU and GBUSV | same hospital and scanner | patient overlap between them unknown |

### Inferences
- Dedup should run per original, then across originals with perceptual hashing: copies change
  format (BEHSOF frames from .avi, usliverseq to mp4, Kaggle resizing) so exact hashes will miss them.
- The Karim and Ball set alone needs dedup before splitting, as its paper warns.

### Gaps
- Whether M2-US's liver subtask is exactly SMC-LUD, and which public sets feed its 366-image
  organ subtask, is not confirmed (sources not named on its site).
- Whether AD-MAGNet, LUS-7Seg and the Table 2 uploads repackage other public sets is unknown.

## Q3. Which are the largest by image count, and which are open with a permissive licence?

### Takeaway
By 2D image count the largest are LEPset (11,500, EUS pancreas), UIdataGB (10,692, gallbladder),
LUS-7Seg (10,507, origin unverified), Saudi NAFLD (10,352, agreement needed) and the kidney-stone
set (9,416). Open and CC BY 4.0 with no login: Byra, B-mode-and-CEUS-Liver, UIdataGB, the
kidney-stone set, LEPset, the Karim and Ball set, M2-US, micro-ultrasound prostate and
Prostate-MRI-US-Biopsy; AUL and SMC-LUD are CC BY 4.0 in metadata but carry conflicting text.

### Cited Findings
Table 4. Largest sets by count (2D images unless stated; sources in Q1 entries).

| Rank | Dataset | Count | Access, licence |
|---|---|---|---|
| 1 | Prostate-MRI-US-Biopsy | 102,397 DICOM images (MR + 3D US), 1,151 patients | open, CC BY 4.0 |
| 2 | M2-US (all organs; abdominal part 5,832) | 67,620 images | open, CC BY 4.0 |
| 3 | LEPset | 11,500 EUS images (3,500 labelled) | open, CC BY 4.0 |
| 4 | UIdataGB | 10,692 images | open, CC BY 4.0 |
| 5 | LUS-7Seg | 10,507 images | Kaggle, CC BY-SA 4.0 (uploader) |
| 6 | Saudi NAFLD | 10,352 images | agreement, non-commercial |
| 7 | Kidney stone | 9,416 images | open, CC BY 4.0 |
| 8 | Karim and Ball | 5,468 unique images | open, CC BY 4.0 |
| 9 | SMC-LUD | 5,385 images | open, CC BY 4.0 + non-commercial text |
| 10 | GBUSV | 15,800 frames in 64 videos | agreement |

Non-commercial or restricted licences: Regensburg (CC BY-NC 4.0), Open Kidney (CC BY-NC-SA),
μ-RegPro and Fedorov prostate (CC BY-NC-SA 4.0), MONAI AWS repository (CC BY-NC 4.0), Saudi NAFLD
(agreement), GBCU and GBUSV (agreement), CLUST (challenge use only). No open licence: Vitale set
("© Original Authors"), usliverseq (none stated), SYSU-FLL-CEUS (none stated).

### Inferences
- Against the project's training set of about 20,000 images (dataset version 261023), the
  upper-abdominal sets with known counts that need no signed agreement (entries 1, 2, 3, 5, 6, 12,
  17, 18, 19, 26, 27) sum to about 48,300 images before dedup (about 37,800 without LUS-7Seg).
  Organ masks exist for only about 1,300 real images (AUL 735, Open Kidney 514, Vitale set 61) plus
  926 simulated ones, and LUS-7Seg's 10,507 if it proves genuine. This sum is my own arithmetic
  on the counts above.
- No licence seen restricts the cloud region where copies are stored; the agreements of GBCU,
  GBUSV, Saudi NAFLD and CLUST forbid sharing and may set storage terms (agreement texts not read).

### Gaps
- Exact totals for the Kaggle fibrosis set, CT2US, Open Kidney download size, GBCU/GBUSV size and
  the MONAI AWS repository size were not found.

#### Seen, other groups
- Fetal: [ACOUSLIC-AI](https://zenodo.org/records/12697994) (fetal abdomen, 38 GB, CC BY-NC-SA 4.0);
  Fetal Abdominal Structures Segmentation (Kaggle orvile copy); [3vessels + gallbladder](https://zenodo.org/records/7323401) (fetal, 253 images).
- MICCAI 2025 FLARE ultrasound subset ([HF](https://huggingface.co/datasets/jacksonyu123/MICCAI25_FLARE_Ultrasound); 4.92 GB, CC BY-NC 4.0): fetal abdomen, breast, carotid, thyroid, fetal head, heart; no adult abdomen.
- [ULTRA-SR synthetic](https://zenodo.org/records/7271766) (IEEE IUS 2022 super-resolution challenge).
- Gynaecology: MMOTU (ovary); uterine fibroid video segmentation (HF huihuixu).
- Preclinical abdomen (not human): porcine liver HIFU motion ([Zenodo 4970841](https://zenodo.org/records/4970841)); rat steatotic liver 3D ultrasound (Zenodo 16918233); mouse HCC CEUS (atlas).
- Phantom: LUSS_phantom (Leeds), listed in [UltraSam US-43d](https://github.com/CAMMA-public/UltraSam).
