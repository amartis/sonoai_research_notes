# Public ultrasound datasets of the heart, lung and vessels: census as of 2026-11-25

Scope: adult and paediatric echocardiography (echo), including transoesophageal echo (TEE, a probe in the
oesophagus); lung and pleura; blood vessels (carotid, peripheral arteries and veins, deep vein thrombosis
(DVT), aorta, intravascular ultrasound (IVUS), transcranial Doppler (TCD)). Fetal echo is out of scope
(another researcher covers it). Roboflow Universe is out of scope (project epic 2, [DEC-081](../../decisions/DEC-081-epic2-mission-roboflow-universe-ultrasound-scraper.md) and [DEC-096](../../decisions/DEC-096-epic2-retrieval-path-official-routes-terms-reading-fetch-budget.md)).

Method: dataset landing pages and their machine-readable metadata were read directly where possible:
the CREATIS Girder REST API (CAMUS, TED, CETUS), the Kaggle Croissant metadata files, the Mendeley Data
public API, the Zenodo, figshare, Hugging Face (HF) and Harvard Dataverse APIs, and PhysioNet and IEEE
DataPort page text. No dataset, archive, video or image was downloaded or opened; only small licence and
split text files (under 1 KB each) were read from the CREATIS server. Facts checked before the run paused
are marked "verified ... 2026-11-25"; facts checked after the pause are marked "2026-11-26". Anything taken
from a search-result summary, a secondary list or memory is marked "unverified".

## Q1. Which heart, lung and vessel ultrasound datasets exist, and what are their 14 fields?

### Takeaway
I found 29 heart, 12 lung and 10 vessel entries (51 in all). They include simulated and phantom sets and
three credentialed PhysioNet sets (MIMIC-IV-ECHO and two subsets of it). Open, scriptable (tier A) sets are now a large share: EchoXFlow
(480 GB, 2026), EV9V (25.5 GB, 2026), ThrombUS+ (12.2 GB of DVT videos, 2025), CACTUS (13.2 GB of
phantom images), the CREATIS family (CAMUS, TED, CETUS) and the Mendeley carotid and lung sets. The best
known video sets still need a manual sign-up or approval: the Stanford EchoNet family, MIMIC-IV-ECHO,
RVENet, TMED-2 and HMC-QU.

### Cited Findings

#### Legend (used in every table and entry)
- Access level: open direct link / free account / click-through terms / data use agreement (DUA) with
  manual approval / credentialed (training and approval) / on request by email / closed or dead link.
- Automation tier from a cloud server: A = scriptable with no login; B = scriptable with a token or cookie
  the user supplies once; C = needs a manual step by the user (form, approval, captcha, click-through);
  D = not automatable. "C→B" = one manual step once (sign-up, accept terms), then token-scriptable.
- GB = decimal gigabytes (10^9 bytes), from the host's own file sizes unless marked otherwise.
- RUA = research use agreement. NC = non-commercial. ND = no derivatives. SA = share-alike.
- Terms: TTE = transthoracic echo (probe on the chest); A2C, A4C = apical 2- and 4-chamber views;
  PLAX, PSAX = parasternal long and short axis views; ED, ES = end-diastole, end-systole; EF = ejection
  fraction; LV, RV, LA = left ventricle, right ventricle, left atrium; LUS = lung ultrasound; IMT =
  intima-media thickness; NIfTI = a medical image file format; HF = Hugging Face.

#### Summary table

Table 1. Census of public heart, lung and vessel ultrasound datasets as of 2026-11-25. One row per dataset:
anatomy, size, download size, host, access level, licence and automation tier (A to D, legend above).
"unknown" = not found at the source.

| # | Name | Anatomy / content | Images or videos | GB | Host | Access level | Licence | Auto |
|---|---|---|---|---|---|---|---|---|
| H1 | CAMUS | Adult heart, apical 2- and 4-chamber (A2C, A4C) TTE | 500 patients; 1,000 half-cycle cines; 2,000 annotated ED/ES frames (inferred) | 3.83 | Institutional (CREATIS Girder) | Open direct link | CC BY-NC-SA 4.0 + NC terms | A |
| H2 | TED (subset of CAMUS) | A4C full cardiac cycle | 98 patients, 98 full-cycle cines | 5.68 | CREATIS Girder | Open direct link | CC BY-NC-SA 4.0 + NC terms | A |
| H3 | syntheticCAMUS (simulated) | Simulated A4C from 100 CAMUS patients | 100 virtual patients (.mat, with and without artefacts) | 11.74 | CREATIS Girder | Open direct link | not checked | A |
| H4 | CETUS (MICCAI 2014) | 3D TTE, left ventricle (LV) | 45 patients, 3D+time | 0.68 | CREATIS Girder | Open direct link | CC BY-NC-SA 4.0 + NC terms | A |
| H5 | Multimodality STRAUS (simulated) | Simulated 3D US + cine/tagged MRI | 18 virtual patients + 3 meshes | 14.38 | CREATIS Girder | Open direct link | not checked | A |
| H6 | DUPLEX (simulated) | Simulated colour Doppler; anatomy not stated | unknown | 0.58 | CREATIS Girder | Open direct link | not checked | A |
| H7 | EchoNet-Dynamic | Adult A4C TTE, EF | 10,030 videos, 112×112 | not stated (~7, unverified) | Stanford AIMI (Redivis) | Registration + click-through RUA | Stanford RUA: NC, no redistribution | C→B |
| H8 | EchoNet-Pediatric | Paediatric A4C + PSAX, EF | 3,176 + 4,424 videos (page total 7,643; others 7,810) | not stated | Stanford AIMI (Redivis) | Registration + RUA | Stanford RUA: NC, ND, no redistribution | C→B |
| H9 | EchoNet-LVH | Adult PLAX, wall thickness | 12,000 videos, native resolution | not stated | Stanford AIMI (Redivis) | Registration + RUA | Stanford RUA: NC, ND, no redistribution | C→B |
| H10 | EchoNet TEE View Classifier | Intraoperative TEE, adults | ~500 patients (video count not stated) | not stated | Stanford AIMI (Redivis) | Registration (terms not shown) | not shown on page | C→B |
| H11 | EchoNet-Synthetic | Synthetic A4C and PSAX videos | 10,030 + 3,284 + 4,526 synthetic videos (README targets) | unknown | GitHub + HF (models found, data link not) | unknown | not stated | unknown |
| H12 | MIMIC-IV-ECHO v1.0.1 | Adult TTE DICOM, Boston, USA | 524,137 DICOM files, 7,228 studies, 4,572 patients | not stated | PhysioNet | Credentialed (CITI training + DUA) | PhysioNet Credentialed Health Data License 1.5.0 | C→B |
| H13 | MIMIC-IV-ECHO-Ext-MIMICEchoQA | TTE video + question-answer pairs | 622 examples | unknown | PhysioNet | Credentialed | PhysioNet credentialed (unverified) | C→B |
| H14 | MIMIC-IV-ECHO-Ext-LVVOLUMES-A4C-ROI | A4C LV volumes | 1,064 studies | unknown | PhysioNet | Credentialed (unverified) | unverified | C→B |
| H15 | TMED-2 (and TMED-1) | Adult TTE stills, aortic stenosis (AS), views | 442,636 still images (sum), 6,790 studies | unknown | Tufts (by contact) | On request by email | not stated | C (or D) |
| H16 | HMC-QU | Adult A4C + A2C, myocardial infarction (MI) | 322 videos, 162 patients; 109 with LV masks | Kaggle holds 0.0009 (features only) | Kaggle (metadata) + email | On request by email | CC BY-NC-SA 3.0 IGO (Kaggle) | C |
| H17 | Unity Imaging (Echo Model Development Dataset, 2020-12-05) | Adult TTE stills, PLAX measurements | >7,500 images | not stated | Institutional (data.unityimaging.net) | Open direct link | CC BY-NC-ND 4.0 | A |
| H18 | CardiacUDA (Kaggle name "cardiacUDC") | 4 views (LVLA, PALA, LVSA, A4C) | 992 videos, ~100 patients | 4.21 | Kaggle | Free account | CC BY-NC 4.0 | B |
| H19 | EchoCP | Contrast TTE, A4C, patent foramen ovale (PFO) | 60 videos, 30 patients | 5.16 | Kaggle | Free account | CC BY-NC 4.0 | B |
| H20 | CardiacNet (PAH, ASD) | A4C, pulmonary arterial hypertension, atrial septal defect | Kaggle 507 + 243 cases; paper 496 + 231 videos | 9.74 | Kaggle (+ SharePoint, GitHub) | Free account; authors ask to be contacted first | CC BY 4.0 (Kaggle) | B |
| H21 | RVENet | A4C, right ventricle (RV) function | 3,583 DICOM videos, 831 people | not stated | GitHub Pages + Google Form | Form + RUA (manual) | RVENet RUA: NC, ND, no redistribution | C |
| H22 | MVSeg2023 | 3D TEE, mitral valve | 175 volumes (105/30/40, test hidden; unverified) | 0.61 | Hugging Face (gated) | Click-through (share contact) | CC BY-NC-ND 4.0 | C→B |
| H23 | SR-TEE | TEE stills, 9 views, image quality | 16,192 simulated + 4,427 real images | 0.78 | figshare (UCL RDR) | Open direct link | CC BY-NC-SA 4.0 | A |
| H24 | MITEA | 3D TTE LV, labels from cardiac MRI | 536 3D volumes, 134 subjects | unknown | Cardiac Atlas Project | unknown (per-dataset rules) | unknown | unknown (likely C) |
| H25 | EchoXFlow (2026) | Adult TTE in beamspace: 1D/2D/3D, Doppler, ECG | 35,377 recordings, 666 exams, 622 patients | 480.0 | Hugging Face | Open (not gated) | CC BY-NC-SA 4.0 | A |
| H26 | EV9V (2026) | Adult TTE, 9 standard views | 5,138 videos, 910,579 frames | 25.5 | Hugging Face | Open (not gated) | CC BY 4.0 (HF tag) | A |
| H27 | CAMEO (2025) | TTE, 9 standard views, ED/ES | count not stated | 7.43 | IEEE DataPort | Paid subscription | CC BY | C (paid) |
| H28 | EchoRisk (MICCAI 2026 challenge) | Cardio-oncology TTE, LVEF | 2,159 videos, 422 patients | unknown | not given | unknown | unknown | unknown |
| H29 | CACTUS (phantom) | Heart phantom, 5 views + random | 37,736 images + videos | 13.18 | FRDR (official) + Academic Torrents | Open | CC BY 4.0 | A |
| L1 | POCUS (Born et al.) | Lung: COVID-19, pneumonia, healthy | 202 videos + 59 images (216 patients) | not stated | GitHub | Open direct link | none stated | A |
| L2 | COVIDx-US v1.5 | Lung: COVID-19, pneumonia, normal, other | 242 videos → 29,651 frames | not stated | GitHub scripts + 9 web sources | Open (by scraping) | Code AGPL-3.0 or GPL-3.0; per-source CC BY-NC(-SA) | A (fragile) |
| L3 | COVID-BLUeS | Lung, 6 BLUE-protocol points | 362 videos (31,746 frames), 63 patients | 0.07 | GitHub + Hugging Face | Open direct link | CC BY-NC-ND 4.0 | A |
| L4 | ICLUS-DB | Lung, COVID-19 severity 0 to 3 | 277 videos, 58,924 frames, 35 patients | unknown | Institutional (login) | Account; no request route found | unknown | C or D |
| L5 | BEDLUS | Lung B-lines, emergency department | 1,419 videos, 188,670 frames, 113 patients | unknown | Harvard Dataverse | Access request (approval) | unknown | C |
| L6 | OpenPOCUS (2025) | Lung, adults in emergency departments | 1,874 clips, 303,977 frames (128×128), 226 patients | 5.26 | Academic Torrents (+ GitHub index) | Open | CC BY-NC-SA 4.0 | A |
| L7 | Uganda LUS classification (2025) | Lung: COVID-19, other disease, healthy | 1,062 images | 0.28 | Mendeley Data | Open direct link | CC BY 4.0 | A |
| L8 | LUS-BALD vertical artefacts (2025) | Lung B-line polygon boxes | 401 images, 255 patients | 0.06 | Mendeley Data | Open direct link | CC BY 4.0 | A |
| L9 | PedLUS (2024) | Paediatric lung, pneumonia, Zambia | not stated | unknown | not listed | unknown | unknown | unknown |
| L10 | CSLID (Zhao et al. 2024) | Lung: simulated + in vivo | 40,000 simulated + 1,132 in vivo images | unknown | GitLab (not opened) | unverified | unknown | unverified |
| L11 | Leeds LUS COVID phantom ("LUSS_phantom", LUCPD) | Lung phantom | 564 images (review) + videos | 0.23 | Leeds research data repository | Open direct link | CC BY 4.0 | A |
| L12 | FLDD | Lung: COVID-19, pneumonia, normal | 7,050 images | unknown | GitHub (not opened) | unverified | unknown | unverified |
| V1 | CUBS (2021) | Common carotid artery (CCA), intima-media thickness (IMT) | 1,088 patients; ≥1,000 TIFF images (count not on page) | ≥0.37 | Mendeley Data | Open direct link | CC BY 4.0 | A |
| V2 | CUBS technical set (2022) | CCA IMT | 500 images | 0.13 | Mendeley Data | Open direct link | CC BY 4.0 | A |
| V3 | Momot CCA images ("CCAUI") | CCA, longitudinal | 1,100 images + 1,100 masks, 11 subjects | ≥0.27 | Mendeley Data | Open direct link | CC BY 4.0 | A |
| V4 | Brno CCA set (2026 Mendeley re-upload) | CCA, transverse | 971 test + 283 labelled images (3,078 files) | 0.09 | Mendeley Data | Open direct link | CC BY 4.0 (set by uploader) | A |
| V5 | Ar-PlaqSegm1 (2025) | Carotid plaque | 541 image-mask pairs | 0.11 | Mendeley Data | Open direct link | CC BY 4.0 | A |
| V6 | ThrombUS+ Dataset #1 (2025) | Lower-limb veins, DVT compression | 2,919 videos, 742 patients | 12.19 | Zenodo | Open direct link | CC BY 4.0 | A |
| V7 | IVUS 2011 challenge (Balocco et al.) | Coronary IVUS | 435 frames at 20 MHz + 77×5 frames at 40 MHz (secondary sources) | unknown | Institutional (CVC Barcelona) | unknown (site TLS error) | unknown | unknown |
| V8 | PhysioNet CVES (TCD) | Middle cerebral artery (MCA) flow velocity + vital signs | elderly stroke and control subjects (count not checked) | 173.9 (whole project) | PhysioNet | Open direct link | ODC-By 1.0 | A |
| V9 | IEEE DataPort TCD (Philips CX50) | MCA and internal carotid TCD echo data | 16 healthy + 29 ICU recordings | 1.83 | IEEE DataPort | Free account | CC BY | B |
| V10 | PhysioNet mental-fnirs (TCD + fNIRS) | MCA flow velocity | 14 adults | unknown | PhysioNet | Open (unverified) | unverified | A (unverified) |

#### Detailed entries: heart

**H1. CAMUS** (Cardiac Acquisitions for Multi-structure Ultrasound Segmentation)
1. 2019; Leclerc et al., IEEE TMI 38(9):2198-2210, doi:10.1109/TMI.2019.2900516 — [CAMUS page](https://www.creatis.insa-lyon.fr/Challenge/camus/).
2. Adult heart, 2D apical 4- and 2-chamber views — [CAMUS page](https://www.creatis.insa-lyon.fr/Challenge/camus/); EF, sex, age and image-quality labels — [CardioBench](https://arxiv.org/html/2510.00520v1); segmented structures LV endocardium, myocardium and left atrium (from memory, unverified).
3. 2D B-mode TTE cine. Per patient and view: ED frame, ES frame and a "half_sequence" (ED to ES) as NIfTI — [patient0001 file list via Girder API](https://humanheart-project.creatis.insa-lyon.fr/database/api/v1/item?folderId=63fde57373e9f004868fb7ac).
4. 500 patient folders counted; collection size 3,833,335,494 bytes (3.83 GB) — [Girder collection JSON](https://humanheart-project.creatis.insa-lyon.fr/database/api/v1/collection/6373703d73e9f0047faa1bc8). 1,000 half-cycle cines and 2,000 annotated ED/ES frames are inferred from 2 views × 500 patients.
5. Masks (`_gt` files) for ED, ES and the half-sequence; per-view `Info_*.cfg` — [file list](https://humanheart-project.creatis.insa-lyon.fr/database/api/v1/item?folderId=63fde57373e9f004868fb7ac). Official train/val/test split lists in folder `database_split`, "a few corrections" vs the paper — [information.txt](https://humanheart-project.creatis.insa-lyon.fr/database/api/v1/item/66e28165961576b1bad4ea03/download).
6. University Hospital of St Etienne, France; GE Vivid E95 (from memory, unverified).
7. [HumanHeart database](https://humanheart-project.creatis.insa-lyon.fr/database/#collection/6373703d73e9f0047faa1bc8); host: institutional (Girder data server at CREATIS, Lyon); collection "CAMUS_public", created 2022-11-15; checksums: none published (Girder may store hashes; not checked).
8. Open direct link: collection is `"public": true` and small items download without login (tested on licence files).
9. "free of charge under CC BY-NC-SA 4.0 ... strictly only non-commercial scientific research purposes"; mandatory citation — [LICENSE_TERMS.md](https://humanheart-project.creatis.insa-lyon.fr/database/api/v1/item/66e2904d961576b1bad4ed75/download). Nothing on storage location.
10. A (Girder REST API, no login).
11. TED (H2) is 98 CAMUS patients; syntheticCAMUS (H3) simulates 100 CAMUS patients. Kaggle/HF mirrors not checked. The online evaluation platform is closed — [CAMUS page](https://www.creatis.insa-lyon.fr/Challenge/camus/).
12. unknown.
13. SAMUS US30K — [SAMUS README](https://github.com/xianlin7/SAMUS); UltraSam US-43d — [UltraSam README](https://github.com/CAMMA-public/UltraSam); OpenUS (also as downstream "CAMUS_2" LVEF task) — [OpenUS README](https://raw.githubusercontent.com/XZheng0427/OpenUS/main/README.md); CardioBench — [arXiv 2510.00520](https://arxiv.org/html/2510.00520v1); TMED's Heart2Heart (AISTATS 2023) — [TMED](https://tmed.cs.tufts.edu/).
14. Verified at the Girder API and CAMUS page on 2026-11-25.

**H2. TED** (Temporal Echocardiography Dataset)
1. 2022; Painchaud et al., "Echocardiography segmentation with enforced temporal consistency", IEEE TMI 41(10):2867-2878, doi:10.1109/TMI.2022.3173669 — [TED LICENSE_TERMS.md](https://humanheart-project.creatis.insa-lyon.fr/database/api/v1/item/66e2bf49961576b1bad5094e/download).
2-5. "98 clinical patients from the CAMUS dataset - 2D+t ... one full cardiac cycle (apical 4 chamber view ...) + manual contouring on the full cardiac cycle (left ventricle and myocardium)"; 5,679,705,938 bytes (5.68 GB) — [Girder collection list](https://humanheart-project.creatis.insa-lyon.fr/database/api/v1/collection?limit=50).
6. As CAMUS. 7. Same Girder server, collection "TED". 8. Open direct link. 9. CC BY-NC-SA 4.0 + NC-only terms + mandatory citation. 10. A.
11. Subset of CAMUS (same patients): deduplicate against H1. 12-13. unknown.
14. Verified at the Girder API on 2026-11-25.

**H3. syntheticCAMUS** (simulated)
- "Simulated 2D apical four chamber view sequences along with the reference myocardial motion field for 100 virtual patients from the CAMUS dataset"; 11.74 GB; `.mat` files, each patient with and without artefacts — [Girder collection list](https://humanheart-project.creatis.insa-lyon.fr/database/api/v1/collection?limit=50). Paper, licence, labels beyond motion field: not checked. Open, A. Derived from CAMUS (H1). Verified 2026-11-25.

**H4. CETUS** (Challenge on Endocardial Three-dimensional Ultrasound Segmentation, MICCAI 2014)
1. Bernard et al., IEEE TMI 35(4):967-977, 2016, doi:10.1109/tmi.2015.2503890 — [CETUS LICENSE_TERMS.md](https://humanheart-project.creatis.insa-lyon.fr/database/api/v1/item/66e2be5d961576b1bad508b0/download).
2-4. 3D TTE of the LV; 45 patient folders; 677,432,305 bytes (0.68 GB) — [Girder folder list](https://humanheart-project.creatis.insa-lyon.fr/database/api/v1/folder?parentType=collection&parentId=62eb991b73e9f0048c3a6c45).
5. LV endocardial reference (ED/ES meshes or masks; from memory, unverified). 6. Multi-centre, multi-vendor (unverified).
7. Girder, collection "CETUS". 8. Open. 9. CC BY-NC-SA 4.0 + NC-only + mandatory citation. 10. A. 11-13. unknown.
14. Verified at the Girder API on 2026-11-25.

**H5. Multimodality STRAUS** (simulated 3D US + cine and tagged MRI)
- Simulated sequences to benchmark strain; 18 virtual patients (healthy, LBBB, ischaemia LAD/LCX/RCA) plus 3 reference meshes; 14.38 GB; [website](http://humanheart-project.creatis.insa-lyon.fr/multimodalityStraus.html) — [Girder collection JSON](https://humanheart-project.creatis.insa-lyon.fr/database/api/v1/collection/587de6f4e1af3f30a2980a58). Licence not checked. Open, A. Verified 2026-11-25.

**H6. DUPLEX** (simulated colour Doppler)
- "Simulated color Doppler images", 0.58 GB, with a `code` folder — [Girder collection list](https://humanheart-project.creatis.insa-lyon.fr/database/api/v1/collection?limit=50). Anatomy, size in images, paper and licence: unknown. Open, A. Verified 2026-11-25.

**H7. EchoNet-Dynamic**
1. 2020; Ouyang et al., "Video-based AI for beat-to-beat assessment of cardiac function", Nature, doi:10.1038/s41586-020-2145-8; dataset DOI 10.71718/yqp5-y078 — [EchoNet-Dynamic](https://echonet.github.io/dynamic/), [AIMI page](https://aimi.stanford.edu/datasets/echonet-dynamic-cardiac-ultrasound).
2. Adult A4C; EF, end-systolic and end-diastolic volumes (ESV, EDV).
3. 2D B-mode cine, downsampled to 112×112; format not stated on page (AVI from memory, unverified).
4. 10,030 videos, one per patient, Stanford 2016-2018. Size not stated (about 7 GB per common reports, unverified, from memory).
5. EF, ESV, EDV; LV tracings by a sonographer, reviewed by a cardiologist, at ED and ES.
6. Stanford University Hospital, USA. Devices not stated.
7. Stanford AIMI shared datasets portal (now on Redivis: [AIMI on Redivis](https://stanford.redivis.com/AIMI)); checksums: unknown.
8. Registration + click-through RUA: "By registering for downloads ... you are agreeing to this Research Use Agreement".
9. "personal, non-commercial research purposes only"; "Any commercial use, sale, or other monetization is prohibited"; "YOU MAY NOT DISTRIBUTE, PUBLISH, OR REPRODUCE A COPY"; "YOU MAY NOT SHARE THE DOWNLOAD LINK"; re-identification prohibited — [EchoNet-Dynamic](https://echonet.github.io/dynamic/). No rule on storage location found.
10. C→B (Redivis sign-in and agreement; then Redivis token, unverified).
11. EchoNet-Synthetic (H11) is generated from it. Third-party copies were seen in search results (HF `AISport/EchoNetDataset`, Academic Torrents), not opened; the RUA forbids redistribution, so use the original.
12. "Each video was cropped and masked to remove text and information outside of the scanning sector."
13. US-43d, OpenUS, CardioBench (verified, links above); CardiacNet paper (evaluated on it) — [CardiacNet search result](https://arxiv.org/abs/2410.20769v1); EchoCLIP, EchoPrime, PanEcho external validation (unverified).
14. Verified at echonet.github.io/dynamic and aimi.stanford.edu on 2026-11-25.

**H8. EchoNet-Pediatric**
1. Reddy, Lopez, Ouyang, Zou, He, "Video-Based Deep Learning for Automated Assessment of Left Ventricular Ejection Fraction in Pediatric Patients", J Am Soc Echocardiogr (page says 2022; DOI not on page) — [EchoNet-Pediatric](https://echonet.github.io/pediatric/).
2. Children 0 to 18 years, 43% female; A4C and parasternal short axis (PSAX); EF, ESV, EDV.
3. 2D cine, 112×112, cropped and masked.
4. A4C 3,176 + PSAX 4,424 videos; the page states 7,643 in total, which does not match the sum (7,600) — [EchoNet-Pediatric](https://echonet.github.io/pediatric/); contradicted by CardioBench (7,810) — [arXiv 2510.00520](https://arxiv.org/html/2510.00520v1) and the EchoNet-Synthetic README (A4C 3,284 + PSAX 4,526 = 7,810) — [README](https://github.com/HReynaud/EchoNet-Synthetic). Size: not stated.
5. EF, ESV, EDV; LV endocardial tracings at ED and ES.
6. Lucile Packard Children's Hospital at Stanford, 2014-2021.
7. [Redivis dataset](https://stanford.redivis.com/datasets/1ca5-2vjyzxftf); checksums unknown.
8. Registration + RUA. 9. Stanford RUA: NC only; no copies distributed; "must not modify ... or create derivative works"; research use only, not for patient care.
10. C→B. 11. EchoNet-Synthetic Pediatric part (H11). 12. Cropped and masked to remove text outside the sector.
13. US-43d (verified), OpenUS (verified), CardioBench (verified).
14. Verified at echonet.github.io/pediatric on 2026-11-25.

**H9. EchoNet-LVH**
1. Duffy et al., "High-Throughput Precision Phenotyping of Left Ventricular Hypertrophy with Cardiovascular Deep Learning", JAMA Cardiology 2022 ([article](https://jamanetwork.com/journals/jamacardiology/fullarticle/2789370), [arXiv 2106.12511](https://arxiv.org/abs/2106.12511)) — [EchoNet-LVH](https://echonet.github.io/lvh/).
2-3. Adult parasternal long axis (PLAX) cine, native resolution, cropped and masked.
4. 12,000 videos; patient count and size not stated.
5. IVS, LVID and LVPW in systole and diastole (sonographer, verified by level 3 echocardiographer).
6. Stanford Medicine routine care. 7. [Redivis dataset](https://stanford.redivis.com/datasets/cchq-0srz1fy9a). 8. Registration + RUA.
9. Stanford EchoNet-LVH RUA: NC only, no distribution or shared links, no derivative works, no re-identification.
10. C→B. 11. none found. 12. Cropped and masked outside the sector. 13. CardioBench (verified).
14. Verified at echonet.github.io/lvh on 2026-11-25.

**H10. EchoNet TEE View Classifier**
- Intraoperative TEE videos from about 500 adult cardiac surgery patients at Stanford, used as an external test set for TEE view classification; dataset DOI 10.71718/bcyb-k484; study in [Sci Rep 2023](https://www.nature.com/articles/s41598-023-50735-8); download via Redivis; the page's "License" section is empty; video count, labels and size not stated — [AIMI page](https://aimi.stanford.edu/datasets/echonet-tee-view-classifier). Access: registration (C→B, likely the Stanford RUA, unverified). Verified 2026-11-25.

**H11. EchoNet-Synthetic** (synthetic videos)
- Reynaud et al., MICCAI 2024, [arXiv 2406.00808](https://arxiv.org/abs/2406.00808). README targets: 10,030 synthetic "Dynamic" videos (192 frames) and Pediatric A4C 3,284 + PSAX 4,526 (128 frames), EF labels; derived from EchoNet-Dynamic and EchoNet-Pediatric; models at [HF HReynaud/EchoNet-Synthetic](https://huggingface.co/HReynaud/EchoNet-Synthetic/tree/main); README says the synthetic sets are released but gives no data link; no licence stated; no mention of the EchoNet RUA — [README](https://github.com/HReynaud/EchoNet-Synthetic). Automation unknown. Verified 2026-11-26.

**H12. MIMIC-IV-ECHO** (Echocardiogram Matched Subset)
1. Versions 0.1 (2023-07-21), 1.0 (2026-03-10), 1.0.1 (2026-08-25, DOI 10.13026/307c-mr50); latest DOI 10.13026/agyq-zp57 — [PhysioNet](https://physionet.org/content/mimic-iv-echo/).
2-3. Adult TTE DICOM image sequences (one per view), GE Vivid E90, E95, S7.
4. DICOM: 524,137 files, 7,228 TTE studies, 4,572 patients. Structured measurements: 206,488 studies (179,928 TTE, 16,389 stress, 10,171 TEE) from 91,372 patients. Hidden test set withheld (358 DICOM studies, 232 patients). Total size not stated.
5. Structured measurements; cardiologist reports to be released in MIMIC-IV-Note; summary tables on BigQuery.
6. Beth Israel Deaconess Medical Center, Boston, USA (the MIMIC source; not stated on the fetched page summary, unverified).
7. PhysioNet; checksums not stated (PhysioNet usually ships SHA256SUMS; unverified).
8. Credentialed: CITI "Data or Specimens Only Research" training + signed DUA.
9. PhysioNet Credentialed Health Data License 1.5.0 (sharing with non-credentialed people is not allowed under that licence: from memory, unverified).
10. C→B (credentialing once, then wget or BigQuery with credentials).
11. Parent of H13 and H14. 12. OCR found PHI text in 69 files of 6 patients; those whole studies were omitted; other burned-in text (measurements, ECG trace) not described.
13. Pretraining of a Nature Communications echo model (search result, unverified).
14. Verified at physionet.org/content/mimic-iv-echo on 2026-11-25 and 2026-11-26.

**H13. MIMIC-IV-ECHO-Ext-MIMICEchoQA**
- Version 1.0.0, 2025-10-07, Thapa, Li, Wu, He, Sahashi, ... Ouyang, Zou; 622 TTE videos each with a question and answer, view label and split; built from discharge summaries ±7 days; credentialed; DOI 10.13026/rndk-4s36 — [PhysioNet page, via search result](https://www.physionet.org/content/mimic-iv-ext-echoqa/). Subset of MIMIC-IV-ECHO. Unverified (page not opened).

**H14. MIMIC-IV-ECHO-Ext-LVVOLUMES-A4C-ROI**
- Published 2026-02-26; credentialed subset of MIMIC-IV-ECHO v0.1 with LV volume labels for A4C views, 1,064 studies — search result naming PhysioNet ([search hit list](https://www.physionet.org/content/?topic=a4c)). Unverified (page not opened).

**H15. TMED-2** (Tufts Medical Echocardiogram Dataset, version 2) and TMED-1
1. TMED-1: Huang et al., MLHC 2021 (PMLR v149); clinical paper JASE 2023, doi:10.1016/j.echo.2023.01.006 — [TMED](https://tmed.cs.tufts.edu/).
2. AS severity (none, early, significant) and views (PLAX, PSAX, A2C, A4C, other).
3. 2D TTE still images, 112×112 PNG; Doppler, M-mode and colour images removed using DICOM metadata (TMED-2); one still per cineloop (TMED page).
4. Fully labelled: 599 studies, 577 patients, 17,270 labelled + 26,596 unlabelled images; partially labelled: 705 studies, 703 patients, 7,694 + 37,576; unlabelled: 5,486 studies, 5,287 patients, 353,500 images — [TMED-2](https://tmed.cs.tufts.edu/tmed_v2.html). Sum: 442,636 images, 6,790 studies (my arithmetic). Size unknown.
5. Image-level view labels, study-level AS labels. 6. Tufts Medical Center, Boston, USA, 2011-2020.
7. Contact page only: "Update 2025-2026: TMED remains under active development", contact Mike Hughes — [data access](https://tmed.cs.tufts.edu/data_access.html).
8. On request by email (CardioBench lists TMED-2 as "Private, on request" — [arXiv 2510.00520](https://arxiv.org/html/2510.00520v1)). 9. Not stated. 10. C, possibly D.
11. TMED-2 supersedes TMED-1 (same source, stricter filtering). 12. unknown.
13. CardioBench (verified). 14. Verified at tmed.cs.tufts.edu on 2026-11-25.

**H16. HMC-QU**
1. Degerli et al., "Early Detection of Myocardial Infarction in Low-Quality Echocardiography", IEEE Access 2021 ([arXiv 2010.02281](https://arxiv.org/pdf/2010.02281)).
2. MI per myocardial segment; LV wall segmentation.
3. 2D A4C and A2C cine, 25 fps, 422×636 to 768×1024.
4. 322 videos from 162 patients: 162 A4C (93 MI, 69 non-MI) and 160 A2C (80 MI, 80 non-MI); 109 A4C with frame-by-frame LV masks.
5. Segment-wise MI labels; LV wall masks for 109 videos.
6. Philips and GE Vivid; 2018-2019. The Kaggle text now says the data came from "Hayatabad Medical Complex (HMC) and Indus Hospital in Pakistan", while the Kaggle metadata names "Hamad Medical Corporation Heart Hospital & Qatar University & Tampere University" — sources disagree.
7. [Kaggle](https://www.kaggle.com/datasets/aysendegerli/hmcqu-dataset): version 6, modified 2024-09-22, holds only an 874 KB archive (extracted features, spreadsheet); md5 published for that archive. Baidu AI Studio copy used by SAMUS: [aistudio 102406](https://aistudio.baidu.com/aistudio/datasetdetail/102406) (not opened).
8. On request by email: "For access to the dataset, please request access by sending e-mail to mkiranyaz@qu.edu.qa".
9. CC BY-NC-SA 3.0 IGO (Kaggle field). 10. C.
11. The Baidu copy is a mirror; CardioBench counts 322 and 332 in two places. 12. unknown.
13. SAMUS US30K (verified), CardioBench (verified).
14. Verified via the [Kaggle Croissant metadata](https://www.kaggle.com/datasets/aysendegerli/hmcqu-dataset/croissant/download) on 2026-11-25.

**H17. Unity Imaging Collaborative: Echocardiography Model Development Dataset**
1. Release 2020-12-05; paper Howard et al., Circ Cardiovasc Imaging 2021 (unverified) — [Unity data](https://data.unityimaging.net/).
2-5. ">7500 image" expert-labelled TTE images; Project 1: LV measurements in PLAX; Project 2: longitudinal strain; files `png-cache.zip` (images) and `labels.zip`.
6. UK collaborative led from Imperial College London; ethics "The Imperial AI Echocardiography Dataset" (IRAS 279328); hospitals and devices not named.
7. Direct HTTP links under `files/2020-12-05/`; code at [GitHub UnityImaging](https://github.com/UnityImaging); no checksums seen.
8. Open direct link. 9. Data CC BY-NC-ND 4.0; model weights CC BY 4.0; code MIT. 10. A.
11. unknown. 12. unknown. 13. TMED Heart2Heart cross-hospital study (verified at [TMED](https://tmed.cs.tufts.edu/)).
14. Verified at data.unityimaging.net on 2026-11-25. Size not stated.

**H18. CardiacUDA** (Kaggle title "cardiacUDC_dataset")
1. Yang et al., GraphEcho, ICCV 2023, [arXiv 2309.11145](https://arxiv.org/abs/2309.11145); code [xmed-lab/GraphEcho](https://github.com/xmed-lab/GraphEcho).
2-3. 4 views per patient: LV long axis (LVLA), pulmonary artery long axis (PALA), LV short axis (LVSA), A4C; 2D cine, 800×600 or 1024×768 (Philips or Hitachi), >100 frames each.
4. 516 (site G) + 476 (site R) = 992 videos, about 100 patients; archive.zip 4.206 GB.
5. Masks: LV and RV (LVLA, LVSA), PA (PALA), LV, RV, LA, RA (A4C); training videos have 5 annotated frames each, validation and test every frame; split 8:1:1.
6. Two hospitals in China (sites G and R; from the authors' affiliations, inferred).
7. [Kaggle](https://www.kaggle.com/datasets/xiaoweixumedicalai/cardiacudc-dataset), published 2023-10-30; no md5 in metadata.
8. Free account (Kaggle). 9. CC BY-NC 4.0 (Kaggle field). 10. B (Kaggle API token).
11. Same authors as EchoCP and CardiacNet; site overlap unknown. 12. unknown. 13. UltraSam US-43d (verified).
14. Verified via [Kaggle Croissant](https://www.kaggle.com/datasets/xiaoweixumedicalai/cardiacudc-dataset/croissant/download) on 2026-11-25.

**H19. EchoCP**
1. Wang et al., MICCAI 2021 ("EchoCP: An Echocardiography Dataset in Contrast Transthoracic Echocardiography for Patent Foramen Ovale Diagnosis"; the Kaggle text cites the ImageCHD paper by mistake).
2-4. Contrast TTE (cTTE) A4C videos at rest and during the Valsalva manoeuvre for 30 patients (60 videos), each ≥10 cardiac cycles; archive.zip 5.155 GB.
5. PFO diagnosis labels; sparse segmentation of representative frames (four sonographers).
6. China (inferred from authors). 7. [Kaggle](https://www.kaggle.com/datasets/xiaoweixumedicalai/echocp), published 2023-10-31, modified 2025-09-03.
8. Free account. 9. CC BY-NC 4.0. 10. B. 11-12. unknown. 13. UltraSam US-43d (verified).
14. Verified via Kaggle Croissant on 2026-11-25.

**H20. CardiacNet** (CardiacNet-PAH and CardiacNet-ASD; Kaggle title "AbnormCardiacEchoVideos")
1. Yang et al., ECCV 2024, doi:10.1007/978-3-031-73337-6_17 — [search result](https://arxiv.org/abs/2410.20769v1); [GitHub](https://github.com/xmed-lab/CardiacNet).
2-3. A4C cine (720p per paper), NIfTI image + label per case.
4. Kaggle: PAH 507 cases, ASD 243 cases; archive 9.736 GB; four hospitals — [Kaggle](https://www.kaggle.com/datasets/xiaoweixumedicalai/abnormcardiacechovideos). Paper/GitHub: PAH 342 + 154 normal = 496 videos (44,363 frames), ASD 100 + 131 normal = 231 videos (13,471 frames) — sources disagree.
5. Disease labels (PAH confirmed by right heart catheterisation); label files per case.
6. Four collaborating hospitals (not named).
7. Kaggle (published 2024-07-16), a HKUST SharePoint folder and [XiaoweiXu/CardiacNet-dataset](https://github.com/XiaoweiXu/CardiacNet-dataset).
8. Free account; GitHub asks users to contact xiao.wei.xu@foxmail.com before downloading.
9. CC BY 4.0 on Kaggle; GitHub shows only the code's MIT licence. 10. B.
11. Same group as H18, H19. 12. unknown. 13. CardioBench (verified).
14. Verified at Kaggle Croissant and GitHub on 2026-11-26.

**H21. RVENet**
1. Magyar et al., ECCV Workshops 2022, LNCS 13803, doi:10.1007/978-3-031-25066-8_33; Tokodi et al., JACC Cardiovasc Imaging 2023 — [RVENet](https://rvenet.github.io/dataset/).
2. RV function; subgroups include healthy adults and children, athletes, heart failure, valve disease, transplant.
3. 2D A4C (standard or RV-focused) DICOM videos.
4. 3,583 videos, 944 examinations, 831 individuals (2013-2021). Size not stated.
5. RVEDV, RVESV, RVEF from 3D echo (TomTec); video quality (5 points), view, orientation, age, sex, diagnosis, 80:20 split, in one CSV.
6. Heart and Vascular Center, Semmelweis University, Budapest, Hungary.
7. GitHub Pages + Google Form; checksums not stated.
8. DUA-style: read the RUA, register by form, then a download link (manual).
9. NC only; no redistribution or link sharing; "Colleagues must register individually"; no derivative works; Hungarian/EU law.
10. C. 11. none known. 12. Only PHI DICOM tags were removed and "no other preprocessing" — burned-in overlays are likely present (inference).
13. unknown. 14. Verified at rvenet.github.io/dataset on 2026-11-26.

**H22. MVSeg2023** (MICCAI 2023 mitral valve segmentation challenge)
1. Challenge design on [Zenodo 7844870](https://zenodo.org/records/7844870) (PDF only, CC BY-NC-ND 4.0; Robarts Research Institute / Western University, Canada, and King's College Hospital, London); data derived from DeepMitral (Carnahan et al., MICCAI 2021) per the HF card.
2-3. 3D TEE, single-frame volumes; mitral leaflets (anterior and posterior classes per a later paper, unverified).
4. 105 train, 30 validation, 40 test volumes (test not public) per search sources (unverified); HF repo 608,204,543 bytes in 3 zip files — [HF API](https://huggingface.co/api/datasets/pcarnahan/MVSeg2023).
5. Leaflet segmentations. 6. Philips EPIQ (HF card per search summary, unverified).
7. [HF pcarnahan/MVSeg2023](https://huggingface.co/datasets/pcarnahan/MVSeg2023), created 2024-11-05; challenge page [synapse.org/MVSeg2023](https://www.synapse.org/MVSeg2023) (not opened); HF stores LFS hashes.
8. Click-through: HF gate "auto" (accept sharing contact information). 9. CC BY-NC-ND 4.0. 10. C→B (HF token after one click).
11. Overlap with DeepMitral data (same group). 12-13. unknown. 14. Verified at the HF API on 2026-11-25.

**H23. SR-TEE**
- MICCAI 2023 (code [SR-AQA](https://github.com/wzjialang/SR-AQA)); 16,192 simulated images (HeartWorks simulator, 38 participants) + 4,427 real TEE images (10 procedures, 2 hospitals), 9 standard TEE views; each image scored by 3 anaesthetists for two quality tasks; SR-TEE.zip 777,413,186 bytes, md5 b640f24bce1b3db23eeeb28b0b79ad4a; version 2, 2023-08-03, DOI 10.5522/04/23699736.v2; CC BY-NC-SA 4.0; open, A — [figshare API](https://api.figshare.com/v2/articles/23699736), [UCL RDR page](https://rdr.ucl.ac.uk/articles/dataset/SR-TEE_Dataset_for_Regressing_Simulation_to_Real_Unsupervised_Domain_Adaptation_for_Automated_Quality_Assessment_in_Transoesophageal_Echocardiography/23699736/2). Real data "fully anonymized". Verified 2026-11-25.

**H24. MITEA**
- Zhao et al., Front Cardiovasc Med 2023, doi:10.3389/fcvm.2022.1016703; 536 annotated 3D echo images, 134 subjects (scan and re-scan), healthy and diseased; LV labels registered from subject-specific cardiac MRI; hosted by the Cardiac Atlas Project ([CAP](https://cardiacatlasproject.isd.kcl.ac.uk)); "each dataset requires different rules to download" — [PMC9871929 via search](https://pmc.ncbi.nlm.nih.gov/articles/PMC9871929/). Unverified (pages not opened); access, licence and size unknown.

**H25. EchoXFlow** (2026)
1. Stenhede, Sulkowska, Orstad, Schirmer, Ranjbar, [arXiv 2605.05447](https://arxiv.org/abs/2605.05447) (v1 2026-05-06, v2 2026-10-21).
2. Routine adult TTE: function, motion, flow.
3. Beamspace (native acquisition geometry, not scan-converted) 1D, 2D and 3D data, several Doppler modes, synchronised ECG.
4. 35,377 recordings, 666 examinations, 622 patients; 674 files, 480,022,303,322 bytes (480.0 GB) — [HF API](https://huggingface.co/api/datasets/Ahus-AIM/EchoXFlow).
5. Guideline measurements, dense 2D myocardial contours, 3D LV endocardial meshes.
6. Akershus University Hospital (Ahus), Norway, 2025-2026 (per a search summary; the arXiv page does not name it).
7. [HF Ahus-AIM/EchoXFlow](https://huggingface.co/datasets/Ahus-AIM/EchoXFlow), tooling [GitHub Ahus-AIM/EchoXFlow](https://github.com/Ahus-AIM/EchoXFlow); created 2026-05-03, modified 2026-11-01; HF LFS hashes.
8. Open (not gated). 9. CC BY-NC-SA 4.0 (HF card). 10. A.
11. none known. 12. Beamspace data carries no rendered overlays (inference). 13. unknown (new).
14. Verified at the HF API and arXiv on 2026-11-25.

**H26. EV9V** (Echocardiographic View 9 Varieties, 2026)
- Gou et al., [arXiv 2606.17437](https://arxiv.org/abs/2606.17437) (v1 2026-06-16, v2 2026-11-02); 5,138 TTE videos, 910,579 frames, 9 standard views; First Affiliated Hospital of Chengdu Medical College, China; HF repo 25,496,097,815 bytes (2 tar files), CC BY 4.0 tag, not gated, created 2026-06-12 — [HF API](https://huggingface.co/api/datasets/bgx666/EV9V), [HF page](https://huggingface.co/datasets/bgx666/EV9V). Labels: view class. Open, A. Burned-in text: unknown. Verified 2026-11-25.

**H27. CAMEO** (Cardiac Multi-view EchO dataset)
- Lee, Lei, Chen, Huang, "Descriptor: Cardiac Multi-view EchO Dataset (CAMEO)", IEEE DataPort, DOI 10.21227/kvaz-eh57, created 2025-08-15, updated 2026-07-24; 9 standard views (apical, PLAX, PSAX, subcostal), ED/ES keywords; formats .mat, .png, .jpg, .exr; CAMEO.tar 7.43 GB; licence "Creative Commons Attribution"; but "Subscription Required: This dataset requires an IEEE DataPort Subscription" — [IEEE DataPort](https://ieee-dataport.org/documents/descriptor-cardiac-multi-view-echo-dataset-cameo). Image and patient counts not on page. Automation C (paid subscription + login), D without a subscription. Verified 2026-11-26.

**H28. EchoRisk** (MICCAI 2026 challenge)
- Kalliatakis et al., [arXiv 2607.01039](https://arxiv.org/abs/2607.01039) (2026-07-01): 422 patients, 1,123 exams, 2,159 videos, up to 5 time points, 5 European sites (EU CARDIOCARE study), plus a 280-patient baseline cohort; tasks: LVEF from cine, LV dysfunction, early cardiotoxicity. Says the data are public, but gives no link; licence unknown. Verified (abstract only) 2026-11-25.

**H29. CACTUS** (Cardiac Assessment and ClassificaTion of UltraSound; phantom)
- Elmekki et al., Comput Biol Med 190 (2025), doi:10.1016/j.compbiomed.2025.110003, [arXiv 2503.05604](https://arxiv.org/abs/2503.05604); CAE Blue Phantom scanned with GE Vivid-Q and M4S probe; 37,736 images (A4C 7,422; subcostal 6,345; PLAX 6,102; PSAX aortic valve 5,832; PSAX mitral valve 6,014; random 6,021), quality grades 0-10 by two experts, training and real-time videos; CC BY 4.0; one zip of 13.18 GB; official host Federated Research Data Repository (FRDR, frdr-dfdr.ca; not opened); project page users.encs.concordia.ca/~kadem/cactus/ — [Academic Torrents](https://academictorrents.com/details/329c0ee4a0037a2628e2f2dba826066f764f193c). Open, A. Verified 2026-11-26.

#### Detailed entries: lung

**L1. POCUS dataset** (Born et al.; repository `covid19_ultrasound`)
1. 2020-2021; Born et al., Applied Sciences 11(2):672, 2021, doi:10.3390/app11020672; POCOVID-Net preprint [arXiv 2004.12084](https://arxiv.org/abs/2004.12084) (deprecated) — [GitHub](https://github.com/jannisborn/covid19_ultrasound).
2. COVID-19, bacterial pneumonia, viral pneumonia, healthy — [review Table 1](https://arxiv.org/html/2411.05029v1).
3. 2D lung ultrasound (LUS) videos and images, convex and linear probes.
4. README: ">200 LUS videos"; review: 216 patients, 202 videos, 59 images. Size not stated.
5. Diagnosis per video; lung severity scores for 136 videos (Gare et al. 2022); segmentation for a subset (`data/PulseLab`).
6. Mostly public web sources and publications, plus contributing sites (per-source list not read; unverified).
7. GitHub `data` folder; checksums none. 8. Open direct link.
9. No licence: "Feel free to use (and cite) our dataset"; authors take no responsibility for contributed data.
10. A (git clone). 11. Draws on the same web libraries as COVIDx-US (L2), so cross-dataset duplicates are likely (inference). The README warns: split by video or patient, never by frame.
12. Web-sourced clips may carry logos and text (unverified). 13. unknown.
14. Verified at the GitHub README on 2026-11-25.

**L2. COVIDx-US**
1. 2021; Ebadi et al., [arXiv 2103.10003](https://arxiv.org/abs/2103.10003) — [GitHub](https://github.com/nrc-cnrc/COVID-US).
2. COVID-19 71, pneumonia 49, normal 28, other 94 videos.
3. 2D LUS videos converted to "processed images"; convex 190, linear 52.
4. v1.0 93 videos/10,774 images (2021-03-17) to v1.4 242 videos/29,651 images (2021-07-13); v1.5 (2022-05-30) adds a lung ultrasound score (LUSS) per video. Size not stated.
5. Class per video; LUSS (v1.5); metadata dictionary.
6. Sources: ButterflyNetwork 35, POCUS Atlas 32, GrepMed 20, LITFL 63, Radiopaedia 5, CoreUltrasound 18, publications 22, University of Florida 24, Clarius 23.
7. No data hosted ("We do not host any data"); `create_COVIDxUS.ipynb` scrapes the sources (selenium, vimeo-downloader).
8. Open (each source's own terms). 9. Code "GNU Affero General Public License 3.0" (README) vs GPL-3.0 (GitHub sidebar); POCUS Atlas CC BY-NC 4.0, LITFL CC BY-NC-SA 4.0, Radiopaedia CC BY-NC-SA 3.0; Butterfly, GrepMed, CoreUltrasound, Clarius: none stated.
10. A, but fragile (depends on third-party pages). 11. Overlaps POCUS (L1) sources (inference). 12. Web clips may carry overlays (unverified). 13. unknown.
14. Verified at the GitHub README on 2026-11-25.

**L3. COVID-BLUeS**
1. Wiedemann et al., IEEE JBHI 29(9):6301-6310, 2025, doi:10.1109/JBHI.2025.3543686; [arXiv 2509.10556](https://arxiv.org/abs/2509.10556) — [GitHub](https://github.com/NinaWie/COVID-BLUES).
2-3. LUS videos (mp4) at the 6 BLUE-protocol points; Philips Lumify convex probe.
4. 362 videos, 31,746 frames, 63 patients (33 COVID-positive, 30 negative); HF copy: 362 mp4 + 2 csv, 70,174,879 bytes — [HF API](https://huggingface.co/api/datasets/jannisborn/COVID-BLUES). The POCUS README and a search summary say 371 videos — sources disagree.
5. Severity 0-3 by two experts, A- and B-line visibility, clinical variables, PCR.
6. Maastricht University Medical Center+, Netherlands, Feb-May 2021 (prospective).
7. GitHub `lus_videos` + [HF jannisborn/COVID-BLUES](https://huggingface.co/datasets/jannisborn/COVID-BLUES) (not gated). 8. Open. 9. CC BY-NC-ND 4.0. 10. A.
11. Different patients from L1 (prospective study); no overlap stated. 12. Not mentioned. 13. unknown.
14. Verified at GitHub and the HF API on 2026-11-25.

**L4. ICLUS-DB** (Italian COVID-19 Lung Ultrasound DataBase)
- Roy et al., IEEE TMI 2020 (doi:10.1109/TMI.2020.2994459, from memory, unverified); 35 patients, 277 videos, 58,924 frames, severity 0-3 — [review Table 1](https://arxiv.org/html/2411.05029v1); centres Brescia, Rome, Lodi, Pavia, Lucca, Tione (17 RT-PCR confirmed) — [PMC10060012 via search](https://pmc.ncbi.nlm.nih.gov/articles/PMC10060012); the project site has a login and no public download or request route was found — [ICLUS](https://www.disi.unitn.it/iclus) (search summary). Licence unknown. Automation C or D. Unverified at the primary page.

**L5. BEDLUS** (Boston Emergency Department Lung UltraSound)
- Lucassen et al., IEEE JBHI 2023 ([IEEE 10143623](https://ieeexplore.ieee.org/abstract/document/10143623), [arXiv 2302.07844](https://arxiv.org/abs/2302.07844)); 1,419 videos, 113 patients, B-line present/absent per video, 15,755 B-lines on 10,371 frames; "request access", then `data.zip` — [GitHub](https://github.com/rtlucassen/b-line_detection); 188,670 frames — [review](https://arxiv.org/html/2411.05029v1). Harvard Dataverse record doi:10.7910/DVN/GLCZRB published 2022-10-26 with a guestbook; the anonymous API returns no version or file list (restricted) — [Dataverse API](https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/GLCZRB). Licence and size unknown. Automation C. Verified 2026-11-25 (API) and 2026-11-26 (GitHub).

**L6. OpenPOCUS** (2025)
- Kumar et al., medRxiv doi:10.1101/2025.05.09.25327337; 226 adults with respiratory symptoms in emergency departments (multi-centre, Mar 2020 to Apr 2022), 12- or 8-zone protocol, 1,874 clips, 303,977 frames resized to 128×128 (full text says 303,997, per search summary), labels: no abnormality, B-lines, consolidation, both, indeterminate (three reviewers, adjudicated); 50% COVID-19; identifiers removed from videos; CC BY-NC-SA 4.0; `Lung Database.zip` 5.26 GB + index spreadsheet — [Academic Torrents](https://academictorrents.com/details/63ad0470f43e022cc73407be9c760449d947cb97). The [GitHub repo](https://github.com/kumarandre/OpenPOCUS) holds only an xlsx and a docx with a link to the images. Open, A (torrent). Verified 2026-11-26.

**L7. Uganda LUS classification dataset** (2025)
- Katumba, Murindanyi, Okila, Nakatumba-Nabende, Mwikirize, Serugunda (Makerere University); 1,062 images, classes COVID-19 / other lung disease / healthy; Mulago and Kiruddu hospitals, Kampala; v2 (2025-07-10) adds raw data and scripts; 4 files, 281,456,286 bytes; sha256 per file; DOI 10.17632/hb3p34ytvx.2; CC BY 4.0 — [Mendeley public API](https://data.mendeley.com/public-api/datasets/hb3p34ytvx?version=2), [page](https://data.mendeley.com/datasets/hb3p34ytvx/2). Data in Brief doi:10.1016/j.dib.2025.112034 (search result). Open, A. Verified 2026-11-25.

**L8. LUS-BALD** (vertical artefacts, 2025)
- Same Makerere team; 401 images from 255 patients, polygon bounding boxes around vertical artefacts (B-lines); v2 2025-09-25; 1 zip, 63,667,042 bytes; DOI 10.17632/h923m366sf.2; CC BY 4.0 — [Mendeley](https://data.mendeley.com/datasets/h923m366sf/2); Sci Data 2025, doi:10.1038/s41597-025-05854-4 ([PMC12533227 via search](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12533227/)). Open, A. Verified 2026-11-25.

**L9. PedLUS**
- Etter et al., "Curated and annotated dataset of lung US images in Zambian children with clinical pneumonia", Radiology: AI 2024, doi:10.1148/ryai.230147; consolidation annotations by two radiologists; one sonographer; counts, host and licence not on the card — [RSNA Atlas](https://atlas.rsna.org/cards/4a120472-9154-40dd-8225-e7a4b90f72a3). Access unknown. Verified 2026-11-26.

**L10. CSLID** (COVID-19 Simulated and Labeled In vivo Dataset)
- Zhao et al., Commun Med 2024 ([article](https://www.nature.com/articles/s43856-024-00463-5)); 40,000 simulated images + 174 external and 958 internal in vivo images; A-line, B-line, consolidation — [review Table 1](https://arxiv.org/html/2411.05029v1); host [gitlab.com/pulselab/covid19](https://gitlab.com/pulselab/covid19) (not opened). The POCUS README mentions these simulated images and segmentation labels for a subset of POCUS (`data/PulseLab`), so the in vivo part may overlap POCUS (inference). Unverified.

**L11. Leeds lung ultrasound COVID phantom** ("LUSS_phantom" in US-43d and OpenUS; "LUCPD" in the review)
- McLaughlan, Howell, Ingram (University of Leeds), 2024, DOI 10.5518/1485; phantom videos from several scanners + frame bank; VideoClips.zip 135 MB + LUS_model.zip 91 MB + MATLAB script (~0.23 GB); CC BY 4.0; open to anyone — [Leeds repository](https://archive.researchdata.leeds.ac.uk/1263/); 564 phantom images labelled rib, pleural line, A-line, B-line, B-line confluence — [review](https://arxiv.org/html/2411.05029v1). A. Used in US-43d and OpenUS (verified). Verified 2026-11-26.

**L12. FLDD** (listed in the review as "Fictional Lumen Dissection Dataset")
- 2024, 7,050 images (pneumonia, normal, COVID), [GitHub DASARINAGAVINOD/Covid-19_Ultrasound](https://github.com/DASARINAGAVINOD/Covid-19_Ultrasound) (not opened) — [review](https://arxiv.org/html/2411.05029v1). Provenance unknown; likely a re-package of other web LUS data (inference). Unverified.

#### Detailed entries: vessels

**V1. CUBS** (Carotid Ultrasound Boundary Study, 2021)
1. Meiburger et al., Ultrasound Med Biol 2021, doi:10.1016/j.ultrasmedbio.2021.03.022; dataset DOI 10.17632/fpv535fss7.1 (v1, 2021-05-04) — [Mendeley](https://data.mendeley.com/datasets/fpv535fss7/1).
2. Common carotid artery wall; carotid IMT; clinical parameters and cardiovascular events.
3. 2D B-mode longitudinal still images (TIFF).
4. 1,088 patients, two centres. The API lists 1,000 TIFF files in `IMAGES` (343.8 MB) but caps every folder listing at 1,000 files, so the true count is higher (not stated on the page); listed total ≥0.37 GB — [Mendeley public API](https://data.mendeley.com/public-api/datasets/fpv535fss7/files?folder_id=root&version=1).
5. Lumen-intima and media-adventitia boundary tracings: manual by analysts A1, A1' (repeat), A2, A3; computerised by 5 teams (CNR, INESC TEC, POLITO, TUM, UCY); calibration factors; clinical CSV/XLSX — [folder list](https://data.mendeley.com/public-api/datasets/fpv535fss7/folders/1).
6. 12 institutions (Politecnico di Torino lead; Italy, Cyprus, Portugal, Germany, Canada, Spain).
7. Mendeley Data; sha256 per file in the API. 8. Open direct link (public download URLs). 9. CC BY 4.0. 10. A.
11. V2 comes from the same consortium; overlap unknown. 12. unknown. 13. unknown.
14. Verified at the Mendeley API on 2026-11-25.

**V2. CUBS technical considerations set** (2022)
- "the entire dataset (500 images, conversion factors for images, 3 manual segmentations, 7 computerized segmentations)" for Meiburger et al., Comput Biol Med 2022, doi:10.1016/j.compbiomed.2022.105333; CCA longitudinal B-mode; 1 zip, 132,198,234 bytes; DOI 10.17632/m7ndn58sv6.1 (2022-03-01); CC BY 4.0 — [Mendeley](https://data.mendeley.com/datasets/m7ndn58sv6/1). Open, A. Overlap with V1 unknown. Verified 2026-11-25.

**V3. Common Carotid Artery Ultrasound Images** (Momot; "CCAUI" in US-43d and OpenUS)
- Agata Momot, Silesian University of Technology (Politechnika Śląska), 2022-11-14, DOI 10.17632/d4xt63mgjm.1; 11 subjects (left and right sides), Mindray UMT-500Plus, L13-3s linear probe; DICOM time series converted to PNG and cropped, 709×749; "Each person had 100 images, making a total of 1100 images" plus expert masks (2,200 files); API lists 2,000 PNG (capped), ≥265 MB; CC BY 4.0 — [Mendeley API](https://data.mendeley.com/public-api/datasets/d4xt63mgjm?version=1), [page](https://data.mendeley.com/datasets/d4xt63mgjm/1). Open, A. Near-duplicate frames are likely (100 frames per person from cine; inference). Used in US-43d and OpenUS; OpenUS labels it "Echocardiogram" by mistake. Verified 2026-11-25.

**V4. Common Carotid Artery Data Set** (Mendeley, 2026; a re-upload of the Brno set)
- Uploader "Anitha M", institution Brno University of Technology, published 2026-03-02, DOI 10.17632/486dmdpzd7.1; 538 Ultrasonix test images (every 20th frame of 50 videos of 15 adults) + 433 Toshiba test images with artefacts (2 adults and a child) + 283 transverse images labelled with artery position and size; 3,078 files (1,255 txt, 962 png, 861 jpg), 87.7 MB; CC BY 4.0 — [Mendeley](https://data.mendeley.com/datasets/486dmdpzd7). The original is the Brno University of Technology (SPLab) carotid database (original page not checked; unverified). Prefer the original; licence set by a third-party uploader may not match the original terms. Verified 2026-11-25.

**V5. Ar-PlaqSegm1** (2025)
- Rulloni, Pérez, Dori, Borchi, Gil, de Vargas (Universidad Nacional de Córdoba, Universidad Católica de Córdoba, CONICET, Argentina); 541 B-mode image + binary plaque mask pairs (800×800), train 493 / test 48; 1,082 PNG, 111.3 MB; 2025-11-06; DOI 10.17632/8srkpz52dy.1; CC BY 4.0 — [Mendeley](https://data.mendeley.com/datasets/8srkpz52dy/1). Open, A. Verified 2026-11-25.

**V6. ThrombUS+ Ultrasound Dataset #1** (DVT, 2025)
1. Didaskalou, Portokallidis, Kaldoudi et al. (Athena RC, Democritus University of Thrace); HEALTHINF/BIOSTEC 2026, pp. 853-862, doi:10.5220/0014741500004070.
2. Lower-limb deep veins (sites starting at the common femoral vein near the inguinal ligament); DVT.
3. 2D B-mode compression ultrasound videos ("segmentation-free").
4. 2,919 videos, 742 patients suspected of DVT, 5 European hospitals (Greece, France, Italy, Lithuania; NCT06989255); training zip 9,732,783,309 bytes + testing zip 2,456,983,680 bytes = 12.19 GB.
5. Per video: vein compressibility (0 no, 1 partial, 2 yes) and thrombosis (0/1); training metadata includes age, height, weight, thigh circumference.
6. Conventional ultrasound machines (models not read).
7. [Zenodo training set](https://zenodo.org/records/17659415) (DOI 10.5281/zenodo.17659415), [Zenodo testing set](https://zenodo.org/records/17664207) (DOI 10.5281/zenodo.17664207), v1.0, 2025-11-20; md5 published (training 7c43b4ad1f2961354795747a66ca092b, testing a9e77c3a8f63b7c93115c38a39ef7c61). Zenodo records 18958474, 18894312 and 19318799 hold only papers (PDF).
8. Open direct link. 9. CC BY 4.0. 10. A.
11. none known. 12. unknown. 13. unknown (new).
14. Verified at the Zenodo API on 2026-11-25.

**V7. IVUS 2011 challenge database** (MICCAI 2011 CVII workshop)
- Balocco et al., "Standardized evaluation methodology and reference database for evaluating IVUS image segmentation", Comput Med Imaging Graph 38 (2014) (doi:10.1016/j.compmedimag.2013.07.001, from memory, unverified); accepted manuscript at [Universitat de Barcelona repository](https://diposit.ub.edu/dspace/handle/2445/53334). Secondary sources: dataset B = 435 frames at 20 MHz from 10 patients (109 train, 326 test), 4 expert annotators; dataset A = 77 groups of 5 consecutive frames at 40 MHz — search summaries, unverified. Lumen and media-adventitia contours. Host cited as [cvc.uab.es/IVUSchallenge2011/dataset.html](http://www.cvc.uab.es/IVUSchallenge2011/dataset.html): TLS certificate error on fetch on 2026-11-26, status unknown. A 2023 MedIA paper calls it the only published IVUS dataset (search summary). Licence and automation unknown.

**V8. PhysioNet "Cerebral Vasoregulation in Elderly with Stroke" (CVES)**
- Vera Novak, v1.0.0, 2018-10-04, DOI 10.13026/C2DW96; MCA blood-flow velocity by TCD with blood pressure and other signals during sitting and standing (WFDB format, per search summary); Open Data Commons Attribution License v1.0; total uncompressed 173.9 GB for the whole project (TCD is one part); ZIP, `wget -r -N` and the `physionet` package offered — [PhysioNet](https://physionet.org/content/cves/1.0.0/). Signal data, not images. Subject count not checked. Open, A. Verified 2026-11-25.

**V9. IEEE DataPort "Transcranial Doppler Ultrasound Database (Philips CX50 ultrasound system)"**
- Wadehn (ETH Zurich), Heldt (MIT); created 2020-01-28, updated 2022-05-18; DOI 10.21227/44mg-2965; MCA and internal carotid TCD echo data, healthy adults and neurocritical care patients (16 + 29 recordings per search summary); files Healthy Subjects.zip 513.12 MB, ICU Patients.zip 1.32 GB, plus code; licence "Creative Commons Attribution"; "Open Access dataset files are accessible to all logged in users ... free IEEE account" — [IEEE DataPort](https://ieee-dataport.org/open-access/transcranial-doppler-ultrasound-database-philips-cx50-ultrasound-system). Automation B (session cookie after free sign-up; unverified). Verified 2026-11-26.

**V10. PhysioNet "mental-fnirs"** (n-back mental workload)
- TCD MCA blood-flow velocity (~11 min) with fNIRS, 14 healthy young adults, University of Oklahoma 2018 — [PhysioNet, via search](https://www.physionet.org/content/mental-fnirs/). Licence and size not checked. Unverified.

### Inferences
- For a cloud bucket, the open tier-A image and video sets (CREATIS family 36.9 GB, EchoXFlow 480.0,
  EV9V 25.5, CACTUS 13.2, ThrombUS+ 12.2, OpenPOCUS 5.3, the seven Mendeley sets 1.3, SR-TEE 0.8, Leeds
  phantom 0.2, COVID-BLUeS 0.07; Unity size unknown) add up to about 575 GB. That is about 595 GB with the
  tier-B or click-through sets CardiacNet, EchoCP, CardiacUDA and MVSeg2023 (19.7 GB), and it excludes the
  173.9 GB PhysioNet CVES signal project. EchoXFlow alone is about 83% of it. This is my sum of the host
  sizes above, not a host figure.
- Stanford, RVENet and PhysioNet terms are per person ("personal ... research", "Colleagues must register
  individually", credentialed users only). A shared team bucket may breach them unless every reader
  registers or is credentialed. This is my reading of the quoted terms, not legal advice; ask the hosts.
- EchoXFlow is beamspace (not scan-converted) data, so frames need scan conversion before use with
  B-mode models (inference from the arXiv abstract).
- Most "images" in the lung sets are frames cut from a few hundred videos: COVIDx-US (29,651 frames from
  242 videos), ICLUS and OpenPOCUS. Split and deduplicate at video or patient level.

### Gaps
- Download size not stated for EchoNet-Dynamic, -Pediatric, -LVH, EchoNet TEE, MIMIC-IV-ECHO, RVENet,
  TMED-2, Unity, POCUS, COVIDx-US, ICLUS, BEDLUS. Sign-in pages (Redivis, PhysioNet) were not used,
  because the task allows no log-ins.
- Image counts are incomplete for CUBS and Momot: the Mendeley API caps each folder at 1,000 files.
- Not opened at the primary page (marked unverified above): MITEA, MIMICEchoQA, LVVOLUMES-A4C-ROI,
  CSLID, FLDD, ICLUS, mental-fnirs, the MVSeg2023 counts and device, and the IVUS 2011 counts.

## Q2. Which datasets are subsets, re-releases, merges or mirrors, and which have known duplicates?

### Takeaway
Clear parent-child links: TED and syntheticCAMUS come from CAMUS; EchoNet-Synthetic comes from EchoNet-Dynamic
and EchoNet-Pediatric; MIMICEchoQA and LVVOLUMES-A4C-ROI come from MIMIC-IV-ECHO; TMED-2 replaces TMED-1.
Expect web-source duplicates between POCUS and COVIDx-US, and dense near-duplicate frames inside every
frame-extracted set.

### Cited Findings
- TED = "98 clinical patients from the CAMUS dataset" with full-cycle contours — [Girder collection list](https://humanheart-project.creatis.insa-lyon.fr/database/api/v1/collection?limit=50).
- syntheticCAMUS simulates "100 virtual patients from the CAMUS dataset" — [same source](https://humanheart-project.creatis.insa-lyon.fr/database/api/v1/collection?limit=50).
- CAMUS ships an official split that differs slightly from the paper ("a few corrections") — [information.txt](https://humanheart-project.creatis.insa-lyon.fr/database/api/v1/item/66e28165961576b1bad4ea03/download).
- EchoNet-Synthetic is generated from models trained on EchoNet-Dynamic and EchoNet-Pediatric — [README](https://github.com/HReynaud/EchoNet-Synthetic).
- MIMICEchoQA and LVVOLUMES-A4C-ROI are credentialed subsets of MIMIC-IV-ECHO (search results naming PhysioNet; unverified) — [MIMICEchoQA](https://www.physionet.org/content/mimic-iv-ext-echoqa/).
- TMED-2 refilters the TMED-1 source (DICOM-metadata filter instead of aspect ratio) — [TMED-2](https://tmed.cs.tufts.edu/tmed_v2.html).
- HMC-QU data left Kaggle (now e-mail request); SAMUS points to a Baidu AI Studio copy — [Kaggle Croissant](https://www.kaggle.com/datasets/aysendegerli/hmcqu-dataset/croissant/download), [SAMUS README](https://github.com/xianlin7/SAMUS).
- CardiacUDA is the Kaggle "cardiacUDC_dataset" (same data, different name) — [Kaggle](https://www.kaggle.com/datasets/xiaoweixumedicalai/cardiacudc-dataset).
- CardiacNet counts differ between Kaggle (507 PAH, 243 ASD cases) and the paper or GitHub (496, 231) — [Kaggle](https://www.kaggle.com/datasets/xiaoweixumedicalai/abnormcardiacechovideos), [GitHub](https://github.com/xmed-lab/CardiacNet).
- MVSeg2023 cites the DeepMitral work by the same group as its source (HF card, per search summary; unverified) — [HF](https://huggingface.co/datasets/pcarnahan/MVSeg2023).
- COVIDx-US is built from Butterfly, POCUS Atlas, GrepMed, LITFL, Radiopaedia, CoreUltrasound, publications, University of Florida and Clarius — [COVIDx-US](https://github.com/nrc-cnrc/COVID-US). POCUS also uses public web clips (README; per-source list not read).
- The POCUS README warns that frame-level splits make the task trivial — [POCUS](https://github.com/jannisborn/covid19_ultrasound).
- The Brno carotid set was re-uploaded to Mendeley in 2026 by a third party under CC BY 4.0 — [Mendeley 486dmdpzd7](https://data.mendeley.com/datasets/486dmdpzd7).
- OpenUS lists "Cactus" as a cardiac set but links a psychology-counselling repository — [OpenUS README](https://raw.githubusercontent.com/XZheng0427/OpenUS/main/README.md), [coding-groot/cactus](https://github.com/coding-groot/cactus). The real cardiac CACTUS is H29 — [Academic Torrents](https://academictorrents.com/details/329c0ee4a0037a2628e2f2dba826066f764f193c).
- Third-party copies of EchoNet data were seen in search results (HF `AISport/EchoNetDataset`, Academic Torrents), but their RUA forbids redistribution — [EchoNet-Dynamic RUA](https://echonet.github.io/dynamic/).

### Inferences
- Dedup keys: CAMUS ⊃ TED (patient IDs); MIMIC-IV-ECHO ⊃ its extensions (study IDs); EchoNet-Synthetic is
  generated, not real data, so it is not an exact duplicate, but keep it out of any test set that uses
  EchoNet patients.
- Within-dataset near-duplicates are likely in Momot (100 cine frames per person), the Brno set (every
  10th or 20th frame), COVIDx-US, ICLUS, OpenPOCUS, CACTUS (phantom) and SR-TEE (simulator).
- Uganda LUS classification and LUS-BALD come from the same team and hospitals; patient overlap is possible.
- CSLID's in vivo images may overlap POCUS (the POCUS repository hosts PulseLab labels).

### Gaps
- No dataset publishes a duplicate audit. Overlaps between POCUS and COVIDx-US, CUBS 2021 and 2022, and
  CardiacUDA, EchoCP and CardiacNet (same group) are not quantified anywhere I found.

## Q3. Which are the largest, and which are open with a permissive licence?

### Takeaway
Largest by storage: EchoXFlow (480 GB, open, CC BY-NC-SA 4.0). Largest by count: MIMIC-IV-ECHO (524,137 DICOM
files, credentialed), EV9V (910,579 frames, open, CC BY 4.0), TMED-2 (442,636 stills, request only) and
OpenPOCUS (303,977 lung frames, NC). Open, tier A, under CC BY 4.0 or ODC-By: EV9V, CACTUS (phantom),
ThrombUS+, CUBS (both sets), Momot, Ar-PlaqSegm1, the Uganda and LUS-BALD lung sets, the Leeds phantom and
PhysioNet CVES. CardiacNet on Kaggle (CC BY 4.0) is tier B.

### Cited Findings
- EchoXFlow 480.0 GB, 35,377 recordings, CC BY-NC-SA 4.0 — [HF API](https://huggingface.co/api/datasets/Ahus-AIM/EchoXFlow).
- MIMIC-IV-ECHO 524,137 DICOM files, 7,228 studies — [PhysioNet](https://physionet.org/content/mimic-iv-echo/).
- EV9V 5,138 videos, 910,579 frames, 25.5 GB, CC BY 4.0 — [HF API](https://huggingface.co/api/datasets/bgx666/EV9V).
- TMED-2 image table (sum 442,636) — [TMED-2](https://tmed.cs.tufts.edu/tmed_v2.html).
- EchoNet-LVH 12,000 videos; EchoNet-Dynamic 10,030 — [LVH](https://echonet.github.io/lvh/), [Dynamic](https://echonet.github.io/dynamic/).
- OpenPOCUS 303,977 frames, 5.26 GB — [Academic Torrents](https://academictorrents.com/details/63ad0470f43e022cc73407be9c760449d947cb97).
- BEDLUS 1,419 videos, 188,670 frames (request) — [review](https://arxiv.org/html/2411.05029v1).
- CACTUS 37,736 phantom images, CC BY 4.0 — [Academic Torrents](https://academictorrents.com/details/329c0ee4a0037a2628e2f2dba826066f764f193c).
- ThrombUS+ 2,919 videos, 12.19 GB, CC BY 4.0: the largest vessel set found — [Zenodo](https://zenodo.org/records/17659415).

Table 2. Datasets that are open (no approval) under a permissive licence (CC BY 4.0 or ODC-By, which allow
commercial use with attribution), with download size and automation tier.

| Dataset | Licence | GB | Tier |
|---|---|---|---|
| EV9V | CC BY 4.0 (HF tag) | 25.5 | A |
| CACTUS (phantom) | CC BY 4.0 | 13.18 | A |
| ThrombUS+ #1 | CC BY 4.0 | 12.19 | A |
| CardiacNet (Kaggle) | CC BY 4.0 (Kaggle field; authors ask for contact) | 9.74 | B |
| CUBS 2021 + 2022 | CC BY 4.0 | ≥0.50 | A |
| Momot CCA | CC BY 4.0 | ≥0.27 | A |
| Uganda LUS + LUS-BALD | CC BY 4.0 | 0.34 | A |
| Leeds LUS phantom | CC BY 4.0 | 0.23 | A |
| Ar-PlaqSegm1 | CC BY 4.0 | 0.11 | A |
| PhysioNet CVES (TCD signals) | ODC-By 1.0 | 173.9 (whole project) | A |
| IEEE DataPort TCD | CC BY | 1.83 | B |

### Inferences
- CAMEO is CC BY but sits behind a paid IEEE DataPort subscription, so it is not open in practice.
- The Brno carotid re-upload (V4) is also CC BY 4.0 and tier A, but the licence was set by a third-party
  uploader; check the original Brno source before relying on it.
- CC BY-NC(-SA/-ND) covers most of the large open heart data (CAMUS, TED, CETUS, EchoXFlow, SR-TEE,
  CardiacUDA, EchoCP, Unity, MVSeg2023) and OpenPOCUS and COVID-BLUeS. That suits research, but not
  commercial use or (for ND) shared derived crops.

### Gaps
- The EV9V licence is taken from the HF tag only; the dataset card and paper were not checked for extra terms.

## Gaps (census-wide): not found, dead links, private datasets, and datasets of other groups

### Takeaway
Several often-cited items have no working public route: the large echo foundation-model corpora, most COVID
lung cohorts, the FASEN2023 aorta IVUS set (404) and possibly the IVUS 2011 site. No public neonatal lung,
abdominal aortic aneurysm (AAA) or femoral-vessel segmentation set was found.

### Cited Findings
- Mentioned but not found: SegRWMA (Kaggle, 529 videos per CardioBench — [arXiv 2510.00520](https://arxiv.org/html/2510.00520v1)); Echo One (3D TTE, 527 patients; public status unclear — [arXiv 2606.02634](https://arxiv.org/abs/2606.02634)); the EchoNet-Synthetic data link ([README](https://github.com/HReynaud/EchoNet-Synthetic)); the EchoRisk host ([arXiv 2607.01039](https://arxiv.org/abs/2607.01039)); Mus-V (3,114 carotid and femoral frames from 105 videos with probe force; release in future tense — [arXiv 2407.21394](https://arxiv.org/abs/2407.21394)); openICPSR project 241296 (HTTP 403 — [openICPSR](https://www.openicpsr.org/openicpsr/project/241296)); TIB "IVUS dataset" record (sparse — [TIB](https://service.tib.eu/ldmservice/dataset/ivus-dataset)); STACOM 2011 3D echo motion-tracking challenge (not checked).
- Dead or empty: FASEN2023 aortic-wall IVUS set (ex vivo porcine, phantom, simulated) — [doi:10.21227/gaa8-h536](https://doi.org/10.21227/gaa8-h536) resolves to a 404 page (2026-11-26); IVUS 2011 site TLS error ([cvc.uab.es](http://www.cvc.uab.es/IVUSchallenge2011/dataset.html)); CREATIS "synTEE" collection is 0 bytes ([Girder list](https://humanheart-project.creatis.insa-lyon.fr/database/api/v1/collection?limit=50)) although a paper calls synTEE (80 simulated patients) public ([arXiv 2511.02210](https://arxiv.org/html/2511.02210v1), search summary); CAMUS online evaluation closed ([CAMUS](https://www.creatis.insa-lyon.fr/Challenge/camus/)); HMC-QU data removed from Kaggle ([Kaggle](https://www.kaggle.com/datasets/aysendegerli/hmcqu-dataset)).
- Private corpora behind well-known echo models: EchoCLIP ~1.03M A4C videos, EchoPrime 12.1M videos, PanEcho 1.2M videos, EchoFM 290K videos — [CardioBench Table 4](https://arxiv.org/html/2510.00520v1).
- Private lung cohorts (21 in the review), e.g. London Health Sciences Centre 600 videos/121,381 frames; Gemelli and San Matteo 1,488 videos/314,879 frames; CHUV Lausanne 1,265 videos; ULTRACOV and Royal Melbourne "upon request" — [review Table 2](https://arxiv.org/html/2411.05029v1). Vietnam dengue LUS (60 patients) not public (search summary, [arXiv 2107.12291](https://arxiv.org/pdf/2107.12291)).
- No public neonatal LUS set found (search, 2026-11-26). No public B-mode AAA ultrasound set found; AAA-100 is CT geometry ([search](https://zenodo.org/records/10932957/files/description.pdf)). UK Biobank carotid images need an approved application ([field 30005](https://biobank.ctsu.ox.ac.uk/ukb/field.cgi?id=30005)).
- Possible raw or RF vessel data, not checked: EPFL ultrafast in vivo carotid acquisitions ([EPFL](https://www.epfl.ch/labs/lts5/?p=665)); IEEE DataPort plane-wave carotid cross-sections ("will be made publicly available" — [IEEE DataPort](https://ieee-dataport.org/documents/cpwc-75-pws-3pws-and-1pw)).
- Seen but not ultrasound images (out of scope): PhysioNet EchoNext (ECG with echo labels), CheXchoNet (chest X-ray with echo labels), EchoQA (report text, [arXiv 2503.02365](https://arxiv.org/abs/2503.02365)), RAV (retinal fundus, [arXiv 2512.17322](https://arxiv.org/abs/2512.17322)), CREATIS REVOLUS (spinning-disk simulation, 45.5 GB).
- Seen, other groups (fetal, nerve and other anatomies): FOCUS (fetal cardiac) and Fetal_Planes_DB ([Zenodo 3904280](https://zenodo.org/records/3904280)) in OpenUS; brachial plexus ([GitHub](https://github.com/Regional-US/brachial_plexus)) and UBPD ([site](https://ubpd.worldwidetracing.com:9443/)), which include artery and vein labels; Thyroid US Cineclip ([AIMI](https://stanfordaimi.azurewebsites.net/datasets/a72f2b02-7b53-4c5d-963c-d7253220bfd5)); kidneyUS ([GitHub](https://github.com/rsingla92/kidneyUS)); the breast and thyroid sets of US-43d and US30K ([UltraSam](https://github.com/CAMMA-public/UltraSam), [SAMUS](https://github.com/xianlin7/SAMUS)); EchoCareData (multi-organ, [arXiv 2509.11752](https://arxiv.org/html/2509.11752v1)) and OpenUS-46 ([arXiv 2510.22990](https://arxiv.org/pdf/2510.22990)), merged public collections whose members were not checked.

### Inferences
- The likeliest recoveries are SegRWMA (Kaggle search by name), the FRDR page for CACTUS, the Cardiac Atlas
  Project page for MITEA, and a mail to the IVUS 2011 organisers.

### Gaps
- Membership of USFM, MedSAM, SA-Med2D-20M, EchoCareData and OpenUS-46 in heart, lung or vessel sets was
  not checked.
