# Public breast and thyroid ultrasound datasets: census as of 2026-11-25

Scope: public or published breast and thyroid ultrasound (US) datasets, including breast-region (axillary) lymph nodes, automated breast ultrasound (ABUS) 3D volumes, breast US videos and parathyroid. Purpose: the facts needed to plan an automated download into a private cloud bucket. Research and reading only: no dataset, archive, video or image was downloaded or opened; only landing pages, repository READMEs, and small metadata records (Zenodo, figshare, Kaggle and Hugging Face JSON) were read.

Conventions used below:
- Sources were checked on 2026-11-25 and, after the run paused overnight, on 2026-11-26. Field 14 of each entry gives the date. "Unverified" means the fact came from memory, a secondary list, or a search-result summary, not from the primary page.
- Abbreviations: BUS = breast ultrasound; RF = raw radio-frequency signal; CEUS = contrast-enhanced US; BI-RADS = Breast Imaging Reporting and Data System; TI-RADS = Thyroid Imaging Reporting and Data System; FNA = fine-needle aspiration; ALN = axillary lymph node; DUA = data use agreement; HF = Hugging Face; TCIA = The Cancer Imaging Archive; CC BY / BY-NC / BY-NC-ND = Creative Commons Attribution / Attribution-NonCommercial / Attribution-NonCommercial-NoDerivatives; GB = 10^9 bytes.
- Automation tiers (from the task): A = scriptable with no login; B = scriptable with a token or cookie the user supplies once; C = needs a manual step by the user (form, approval, captcha, click-through); D = not automatable.
- Hugging Face gating (from the HF API field `gated`): "auto" = access is granted at once after the user accepts the terms on the web page (one click-through, then a token works); "manual" = the owner approves each request. This reading of the two values is standard HF behaviour, not re-checked today.
- Roboflow Universe projects are out of scope here (epic 2 runs its own Roboflow scraper under [DEC-081](../../decisions/DEC-081-epic2-mission-roboflow-universe-ultrasound-scraper.md) and [DEC-096](../../decisions/DEC-096-epic2-retrieval-path-official-routes-terms-reading-fetch-budget.md), the Roboflow scraper decisions). None of the datasets below was found only on Roboflow.
- Project context, for scale only: the project's training set today is about 20k images (dataset version 261023).

## Which breast and thyroid ultrasound datasets exist?

### Takeaway
I found 30 breast or breast-region entries and 24 thyroid entries (including collections and unreleased sets); no public parathyroid US dataset, no public breast elastography or breast CEUS dataset, and only one public ABUS volume set (TDSC-ABUS 2023). The 2024 to 2026 releases are the largest: BUS-CoT (breast, 11,439 images), ThyroidXL (thyroid, 11,635 images), ThyUS2Path (thyroid, 8,508 images), TN5000 (thyroid, 5,000 images), and the gated OpenThyroidDB collection on HF (61.8 GB, 2026).

### Cited Findings

**Table 1. Census of public breast and thyroid ultrasound datasets (status checked 2026-11-25/26).** One row per dataset; the name links to the landing page used. "Images or videos" counts what the source states; where sources disagree, the detailed entry under the next question gives both. Download size is the total of the listed files where a repository record states it.

| ID | Name | Anatomy | Images or videos (n) | Download size (GB) | Host | Access level | Licence (as written) | Automation |
|---|---|---|---|---|---|---|---|---|
| B01 | [BUSI](https://scholar.cu.edu.eg/?q=afahmy/pages/dataset) | Breast | 780 images, 600 patients | 0.266 (Kaggle copy) | Institutional site (Cairo University); Kaggle mirror | Open behind a reCAPTCHA page (original); free account (Kaggle) | Original: not seen; Kaggle mirror: "CC0: Public Domain" (set by uploader) | C (original); B (Kaggle) |
| B02 | [BUS-BRA](https://zenodo.org/records/8231412) | Breast | 1,875 images, 1,064 patients | 0.134 | Zenodo | Open direct link | CC BY 4.0 | A |
| B03 | [BrEaST (Breast-Lesions-USG)](https://www.cancerimagingarchive.net/collection/breast-lesions-usg/) | Breast | 256 images (522 files with masks), 256 patients | 0.067 | TCIA | Open direct link (TCIA Data Usage Policy) | CC BY 4.0 | A |
| B04 | [UDIAT Dataset B](https://helward.mmu.ac.uk/STAFF/M.Yap/dataset.php) | Breast | 163 images | unknown | Institutional site (Manchester Metropolitan University) | Licence agreement, manual approval (up to 10 working days) | Agreement; non-commercial research (per BrEaST Table 1) | C |
| B05 | [BUSIS](https://pmc.ncbi.nlm.nih.gov/articles/PMC9025635/) | Breast | 562 images | unknown | Institutional site (Utah State University URL) | Unknown: URL timed out 2026-11-26 | None stated | Unknown |
| B06 | [OASBUD](https://zenodo.org/records/545928) | Breast (raw RF) | 100 lesions (200 scans per one source) | 0.297 | Zenodo | Open direct link | CC BY-NC 4.0 | A |
| B07 | [BUID (QAMEBI)](https://qamebi.com/breast-ultrasound-images-database/) | Breast | 232 images | unknown | Institutional site (qamebi.com) | Open direct link (two ZIPs) | CC BY-NC 4.0 | A |
| B08 | [BUS_UC](https://data.mendeley.com/datasets/3ksd7w7jkx/1) | Breast | 811 images | unknown | Mendeley Data | Open | CC BY 4.0 (images taken from a teaching website; see entry) | A (likely) |
| B09 | [BUS-UCLM](https://data.mendeley.com/datasets/7fvgj4jsp7/3) | Breast | 683 images, 38 patients | unknown | Mendeley Data | Open | CC BY 4.0 | A (likely) |
| B10 | [BUSI_WHU](https://data.mendeley.com/datasets/k6cpmwybk3/3) | Breast | 927 images | unknown | Mendeley Data | Open | CC BY 4.0 | A (likely) |
| B11 | [Breast Ultrasound Image (Rodrigues)](https://data.mendeley.com/datasets/wmy84gzngw/1) | Breast | 250 images | unknown | Mendeley Data | Open | CC BY 4.0 | A (likely) |
| B12 | [BUSC](https://data.mendeley.com/datasets/vckdnhtw26/1) | Breast | 250 images (from B11) | unknown | Mendeley Data | Open | unverified | A (likely) |
| B13 | [BUS Synthetic](https://data.mendeley.com/datasets/r4phtn49r7/1) | Breast (synthetic) | unknown | 0.0097 (secondary) | Mendeley Data | Open | unverified | A (likely) |
| B14 | [STU-Hospital](https://github.com/xbhlk/STU-Hospital) | Breast | 42 images (84 PNG files) | 0.0006 | GitHub | Open | None stated | A |
| B15 | [S1 Data (Guo et al. 2021)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8205136/) | Breast | 200 images | 0.026 (ZIP with code) | Journal supplement (PMC) | Open | None stated for data (article CC BY 4.0) | A |
| B16 | [GDPH&SYSUCC](https://github.com/yuhaomo/HoVerTrans) | Breast | 2,405 images | unknown | OneDrive (link in GitHub README) | Open share link | None stated | A (likely, not tested) |
| B17 | [BUS-CoT](https://doi.org/10.6084/m9.figshare.30838715.v1) | Breast | 11,439 images, 4,838 patients | 6.94 | figshare | Open | CC BY 4.0 | A |
| B18 | [BCMID](https://zenodo.org/records/19402690) | Breast (US + mammography) | 332 patients (image count not stated) | 12.94 | Zenodo | Open | CC BY 4.0 | A |
| B19 | Medical Image Database (Rodtook et al. 2018) | Breast | 180 images | unknown | unknown | unknown | "Cite source" (per BrEaST Table 1) | unknown |
| BV1 | [BUSV (CVA-Net)](https://github.com/jhl-Det/CVA-Net) | Breast, video | 188 videos | unknown | Google Drive and Baidu Netdisk | Open link | Non-commercial research or education only (README) | A (Google Drive; quota risk) |
| BV2 | [FLA-Net video set](https://github.com/jhl-Det/FLA-Net) | Breast, video, ALN labels | 572 videos, 34,300 frames | n/a | none | Closed (README: under ethical review) | n/a | D |
| BV3 | [UVBLS200](https://arxiv.org/abs/2403.11699) | Breast, video | 200 videos | n/a | none found | Claimed public; no link found | unknown | D |
| BL1 | [ALN-Ultra](https://zenodo.org/records/18483501) | Breast cancer, axillary lymph nodes; images + videos | 257 patients | unknown (files hidden) | Zenodo (restricted) | Request on Zenodo, owner approval | CC BY 4.0 (record) | C |
| BL2 | [Lymph node ultrasound image dataset](https://zenodo.org/records/12702916) | Lymph node (site not stated) | unknown | 0.646 | Zenodo | Open | CC BY 4.0 | A |
| B3D1 | [TDSC-ABUS 2023](https://tdsc-abus2023.grand-challenge.org/) | Breast, ABUS 3D volumes | 200 volumes | unknown | Grand Challenge + organiser email | Signed agreement sent by email | Terms not seen | C |
| M1 | [USenhance 2023](https://ultrasoundenhance2023.grand-challenge.org) | Thyroid, carotid, liver, breast, kidney | 3,000 images (1,500 pairs) or 2,464 (sources differ) | unknown | Grand Challenge | Registration (unverified) | unknown | C (unverified) |
| M2 | Chinese ultrasound-report dataset (lijunrio.github.io) | Breast, thyroid, liver | 7,390 (unit not stated) | unknown | GitHub Pages (unverified) | unverified | unknown | unknown |
| T01 | [DDTI](http://cimalab.unal.edu.co/applications/thyroid/) | Thyroid | 99 cases, 134 images (original text); other counts in entry | 0.019 (Kaggle copy) | Institutional site (TLS error); Kaggle mirror; TN3K Google Drive | Original: unreachable 2026-11-25; mirrors open | Kaggle: "Other (specified in description)"; none stated | D (original); B (Kaggle); A (Drive) |
| T02 | [TN3K](https://github.com/haifangong/TRFE-Net-for-thyroid-nodule-segmentation) | Thyroid | 3,493 images, 2,421 patients | unknown | Google Drive and Baidu Netdisk (GitHub README) | Open link | None stated (code MIT) | A (Google Drive) |
| T03 | TG3K | Thyroid gland | 3,585 frames from 16 videos | unknown | Redistributed with TN3K-related repos (unverified) | Open (unverified) | None stated | A (unverified) |
| T04 | [TN-SCUI 2020](https://tn-scui2020.grand-challenge.org/) | Thyroid | 3,644 training images (+910 test, labels hidden) | unknown | Grand Challenge | Free account + challenge registration | Not stated | C |
| T05 | [Stanford AIMI Thyroid Ultrasound Cine-clip](https://aimi.stanford.edu/datasets/thyroid-ultrasound-cine-clip) | Thyroid, cine clips | 192 clips (nodules), 167 patients; about 17.4k frames | unknown | Stanford AIMI via Redivis | Account + research use terms (text not visible) | Not visible on page | C, then B |
| T06 | [TN5000](https://doi.org/10.6084/m9.figshare.28455641) | Thyroid | 5,000 images | 0.221 | figshare | Open | CC BY | A |
| T07 | [ThyroidXL](https://huggingface.co/datasets/VNPT-AI/ThyroidXL) | Thyroid | 11,635 images, 4,093 patients | unknown | HF (gated: auto) | Click-through terms | Not stated in card metadata | C, then B |
| T08 | [ThyUS2Path (Hou et al. 2024)](https://doi.org/10.6084/m9.figshare.27021604.v1) | Thyroid | 8,508 images, 842 patients | 1.64 | figshare | Open | CC BY 4.0 | A |
| T09 | [AUITD](https://www.kaggle.com/datasets/azouzmaroua/algeria-ultrasound-images-thyroid-dataset-auitd) | Thyroid | 3,538 images | 0.131 | Kaggle | Free account | "Unknown" | B |
| T10 | [SegThy](https://www.cs.cit.tum.de/camp/publications/segthy-dataset/) | Thyroid + neck vessels, 3D US + MRI | 28 volunteers (MRI + 3D US); 186 patients (3D US) | unknown | Institutional site (TUM) + HF mirror | Open direct link | CC BY | A |
| T11 | [Free-hand thyroid sweeps](https://huggingface.co/datasets/freehand-us-anon/freehand-thyroid-sweeps) | Thyroid, carotid, trachea; video | 29 videos, 107,614 frames (232 annotated) | about 2.8 (sum of stated parts) | HF (not gated) | Open | CC BY-NC 4.0 | A |
| T12 | [PIUR_Thyroid_segmentation](https://huggingface.co/datasets/Ultraclear/PIUR_Thyroid_segmentation) | Thyroid (card empty) | unknown | unknown | HF (not gated) | Open | CC BY-NC 4.0 | A |
| T13 | [KFGNet video data](https://github.com/NeuronXJTU/KFGNet) | Thyroid, video (per secondary sources) | 3,668 (unit not stated) | unknown | Baidu Netdisk | Open link with extraction code | None stated | D (Baidu from a cloud server; inference) |
| T14 | [Thyroid_Ultrasound_Images (FangDai)](https://huggingface.co/datasets/FangDai/Thyroid_Ultrasound_Images) | Thyroid cancer subtypes | 900 images | unknown | HF (gated: auto) | Click-through terms | Apache-2.0 (as stated by uploader) | C, then B |
| T15 | [PTC pathomics + US (Pang et al. 2024)](https://data.mendeley.com/datasets/dp7zp2pb2v/1) | Thyroid (US + cytology) | 385 cases | unknown | Mendeley Data | Open | CC BY 4.0 | A (likely) |
| T16 | [TGN dataset](https://data.mendeley.com/datasets/8gpvhrrghk/1) | Probably thyroid (not stated) | unknown | unknown | Mendeley Data | Open | CC BY 4.0 | A (likely) |
| T17 | [OpenThyroidDB](https://huggingface.co/datasets/MedXAgent/ThyroidOpenDB) | Thyroid collection (11 external sets + 4 new cohorts) | e.g. 248,194 images (new SMU-HMC cohort) | 61.8 | HF (gated: manual) | Owner approval | Not stated; source licences apply | C, then B |
| T18 | [ThyroidDataSet (Doul0414)](https://huggingface.co/datasets/Doul0414/ThyroidDataSet) | Thyroid collection | unknown | unknown | HF (gated: manual) | Owner approval | Not stated | C, then B |
| T19 | VTUS (Vivim paper) | Thyroid, video | 100 sequences | n/a | none found | unknown | unknown | D (no route found) |
| T20 | [Abnormal thyroid ultrasound images](https://ieee-dataport.org/documents/abnormal-thyroid-ultrasound-images-0) | Thyroid | 34 images (DDTI subset) | unknown | IEEE DataPort | Free IEEE account (unverified) | unknown | C (unverified) |
| P0 | Parathyroid | Parathyroid | none found | n/a | n/a | n/a | n/a | n/a |

Footnote to Table 1: "A (likely)" for Mendeley Data means public datasets show a "Download All" button and no login was asked on the landing page; an anonymous scripted download was not tested. B-tier Kaggle rows need the user's Kaggle API token. "C, then B": one manual step (click-through or approval), after which a user token makes it scriptable.

Other findings about the census itself:
- The UltraSam US-43d collection (43 datasets) contains 7 breast sets (BrEaST, BUID, BUS_UC, BUS_UCML = BUS-UCLM, BUS-BRA, Dataset B, BUSI), STU-Hospital and S1, and 6 thyroid or neck sets (DDTI, TG3K, Thyroid US Cineclip, TN3K, TNSCUI, Segthy) — [UltraSam README](https://github.com/CAMMA-public/UltraSam).
- The OpenUS pre-training table lists the same breast and thyroid sets with sizes (e.g. BUSI 1,560, Thyroid US Cineclip 17,412, Segthy 12,737) — [OpenUS README](https://github.com/XZheng0427/OpenUS).
- SAMUS's US30K uses 5 breast or thyroid sets: TN3K, DDTI, TG3K, BUSI, UDIAT (plus cardiac CAMUS and HMC-QU) — [SAMUS README](https://github.com/xianlin7/SAMUS).
- The npj Digital Medicine catalogue of 72 public US datasets (Alsharid et al. 2025, [DOI 10.1038/s41746-025-02162-4](https://doi.org/10.1038/s41746-025-02162-4)) lists 9 breast and 7 thyroid entries, lists no lymph-node or parathyroid dataset, rates TN5000 "Platinum" and BUS-BRA "Gold", and marks the Stanford cine-clip set as available on request — [PMC12722232](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/).
- The Project Imaging-X index (1,152 entries) holds only 6 breast or thyroid US entries: BUSI, BreastMNIST, TN-SCUI2020, TN3K, DDTI, TDSC-ABUS2023 — [datasets.json](https://github.com/uni-medical/Project-Imaging-X); so that survey is far from complete for this scope.
- Searches for public breast elastography, breast CEUS and parathyroid US datasets found only phantoms, simulations or private cohorts — [search on elastography found phantoms only, e.g. QIBA phantoms](https://research.repository.duke.edu/concern/datasets/qz20st03m?locale=en); [breast CEUS studies used private cohorts, e.g. PMC12729765](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12729765/); [Zenodo search "parathyroid ultrasound" on 2026-11-25 returned only paper supplements](https://zenodo.org/search?q=parathyroid%20ultrasound).

### Inferences
- Thyroid is now better served than breast by size: four thyroid sets exceed 5,000 images (ThyroidXL, ThyUS2Path, TN5000, the Stanford frames), against one breast set (BUS-CoT).
- Many entries are small (under 1,000 images) and several are re-packagings of others (see the overlap question), so the number of independent image sources is lower than the row count.
- The aggregator lists (US-43d, OpenUS, US30K, Imaging-X) all miss the 2024 to 2026 releases (BUS-CoT, BCMID, ThyroidXL, ThyUS2Path, TN5000 partly, OpenThyroidDB, the free-hand sweeps), so they cannot serve as the census on their own.

### Gaps
- Kaggle, IEEE DataPort, Science Data Bank, Synapse, PhysioNet and Baidu AI Studio were not searched systematically (only targeted lookups), so smaller sets there may be missing.
- Thyroid CEUS and thyroid elastography datasets were not searched.

## Per-dataset facts (the 14 fields)

### Takeaway
Most open sets with a clear licence sit on Zenodo, figshare, TCIA or Mendeley Data and are scriptable without login (tier A); the gated or approval-based ones (UDIAT, TN-SCUI, TDSC-ABUS, Stanford cine-clip, ALN-Ultra, ThyroidXL, OpenThyroidDB) need one manual step by the user; Baidu-only or unreleased sets cannot be automated.

### Cited Findings

Field order in every entry: 1 name, year, paper; 2 content; 3 data type; 4 size; 5 labels; 6 source; 7 where to get it, version, checksums; 8 access; 9 licence; 10 automation; 11 overlaps; 12 burned-in text; 13 large-scale use; 14 verification.

#### Breast, 2D images

**B01. BUSI (Breast Ultrasound Images Dataset)**
1. "Dataset of breast ultrasound images", 2020 (data collected 2018), Al-Dhabyani, Gomaa, Khaled, Fahmy, Data in Brief 28:104863, [DOI 10.1016/j.dib.2019.104863](https://doi.org/10.1016/j.dib.2019.104863).
2. Normal, benign and malignant breast scans of women aged 25 to 75 — [Kaggle copy of the authors' description](https://www.kaggle.com/datasets/aryashah2k/breast-ultrasound-images-dataset).
3. 2D B-mode, PNG, average about 500 x 500 pixels — same source.
4. 780 images from 600 patients — same source; 133 normal, 487 benign, 210 malignant — [BrEaST paper Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC10830496/). Kaggle copy 266,185,470 bytes — [Kaggle API record](https://www.kaggle.com/api/v1/datasets/view/aryashah2k/breast-ultrasound-images-dataset); "204MB" per [a GitHub list](https://github.com/hugofigueiras/Breast-Cancer-Imaging-Datasets) (sizes disagree).
5. Class per image; lesion masks — Kaggle description.
6. Institution and devices: Baheya Hospital, Cairo, Egypt (unverified, from memory); 2 devices per [BrEaST Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC10830496/).
7. Original: [Cairo University page](https://scholar.cu.edu.eg/?q=afahmy/pages/dataset), behind a reCAPTCHA page on 2026-11-25, so the download link was not seen. Mirror: Kaggle, version 1, updated 2021-03-14, 78,980 downloads. No dataset DOI; no checksums.
8. Original: open behind a captcha; Kaggle: free account.
9. Original licence: not seen. Kaggle: "CC0: Public Domain", chosen by the uploader, not by the authors (inference). BrEaST Table 1 lists "CC0 (public domain); cite source".
10. C (captcha) for the original; B (Kaggle token) for the mirror.
11. 155 of 780 images (about 19%) are copies of other images, some across classes; 70 images show the axilla, not the breast; usable subset at most 529 images — [Pawłowska, Karwat, Żołek 2023, Data in Brief 48:109247](https://pmc.ncbi.nlm.nih.gov/articles/PMC10293973/). Curated and mirrored copies: see the overlap question.
12. Yes: 126 text, 16 overlay, 127 measurement, 11 Doppler and 15 pictogram annotations; at least 7 images with a biopsy needle — same letter.
13. US-43d ([UltraSam](https://github.com/CAMMA-public/UltraSam)), OpenUS, US30K ([SAMUS](https://github.com/xianlin7/SAMUS)), Project Imaging-X. MedSAM, SA-Med2D-20M, BiomedParse, USFM: unverified.
14. Verified at the Kaggle API record and PMC10293973 on 2026-11-25; the original page could not be read.

**B02. BUS-BRA**
1. BUS-BRA, data posted 2023, paper 2024: Gómez-Flores, Gregorio-Calas, Pereira, Medical Physics 51:3110-3123, [DOI 10.1002/mp.16812](https://doi.org/10.1002/mp.16812).
2. Biopsy-proven tumours with BI-RADS 2, 3, 4 and 5 — [Zenodo record](https://zenodo.org/records/8231412).
3. 2D B-mode images.
4. 1,064 patients (Zenodo); 1,875 images ([npj catalogue](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/), [OpenUS README](https://github.com/XZheng0427/OpenUS)); BUSBRA.zip 133,917,740 bytes (Zenodo).
5. BI-RADS category, benign or malignant (biopsy), tumour delineations — Zenodo.
6. Copyright and distribution: Program of Biomedical Engineering, Federal University of Rio de Janeiro (PEB/COPPE-UFRJ), Brazil; Cinvestav, Mexico, co-develops — Zenodo. Devices: unknown.
7. Zenodo, version 1.0, 2023-03-13, [DOI 10.5281/zenodo.8231412](https://doi.org/10.5281/zenodo.8231412) (concept DOI 10.5281/zenodo.7730708); md5 published (1f8b2be6476d58fc97bfb5e5a1ea9bab). Code: [GitHub wgomezf/BUS-BRA](https://github.com/wgomezf/BUS-BRA).
8. Open direct link.
9. CC BY 4.0; users must cite the Medical Physics paper — Zenodo.
10. A.
11. Mirrors: [Kaggle orvile](https://www.kaggle.com/datasets/orvile/bus-bra-a-breast-ultrasound-dataset) (265,526,681 bytes, licence "Other"; about twice the Zenodo size, so repackaged), HF chehablab/BUS-BRA (2026-11-18), treasurenleanya/bus-bra-a-breast-ultrasound-dataset, BTX24/busbra-birads-processed — [HF search API](https://huggingface.co/api/datasets?search=BUS-BRA).
12. Unknown.
13. US-43d (held out as a test set — [UltraSam paper v2, via search summary](https://arxiv.org/html/2411.16222v2)), OpenUS.
14. Verified at the Zenodo API record on 2026-11-25.

**B03. BrEaST (Breast-Lesions-USG)**
1. "Curated benchmark dataset for ultrasound based breast lesion analysis", Pawłowska et al., Scientific Data 11:148 (2024), [DOI 10.1038/s41597-024-02984-z](https://doi.org/10.1038/s41597-024-02984-z); TCIA [DOI 10.7937/9WKK-Q141](https://doi.org/10.7937/9WKK-Q141).
2. 154 benign, 98 malignant, 4 normal; 33 histological diagnoses — [paper, Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC10830496/).
3. 2D B-mode PNG.
4. 256 subjects, 256 studies, 522 images (files, including masks), 266 segmented lesions; 66.67 MB — [TCIA page](https://www.cancerimagingarchive.net/collection/breast-lesions-usg/).
5. Freehand lesion masks, BI-RADS category and 7 BI-RADS descriptors, histopathology for biopsied cases, patient-level clinical data — TCIA page.
6. Medical centres in Poland, 2019 to 2022; devices Hitachi ARIETTA 70, Esaote 6150, Samsung RS85, Philips Affiniti 70 G / EPIQ 5 G — paper.
7. TCIA, version 1 (updated 2024-01-08), direct HTTP links to a ZIP (PNG images and masks) and an XLSX; checksums not mentioned. Import code: [GitHub best-ippt-pan-pl/BrEaST](https://github.com/best-ippt-pan-pl/BrEaST).
8. Open direct link, under the TCIA Data Usage Policy.
9. CC BY 4.0.
10. A.
11. The authors checked for duplicates with an algorithm — paper. No known mirrors checked.
12. Cleaned: cropped to remove device text; only images without measurement markers, pictograms or text annotations kept — paper.
13. US-43d, OpenUS (listed as 252).
14. Verified at the TCIA page and PMC10830496 on 2026-11-25.

**B04. UDIAT Dataset B**
1. Yap et al., "Automated Breast Ultrasound Lesions Detection using Convolutional Neural Networks", IEEE JBHI 22:1218-1226 (2018), [DOI 10.1109/JBHI.2017.2731873](https://doi.org/10.1109/JBHI.2017.2731873).
2. 110 benign, 53 malignant; cysts, fibroadenomas, invasive ductal carcinomas and other types — [BrEaST Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC10830496/).
3. 2D B-mode.
4. 163 images — BrEaST Table 1; patients unknown; size unknown.
5. Class; lesion masks (used for segmentation in US30K and US-43d).
6. UDIAT Diagnostic Centre, Sabadell, Spain; Siemens ACUSON Sequoia (unverified, from memory).
7. [MMU page](https://helward.mmu.ac.uk/STAFF/M.Yap/dataset.php); older URL www2.docm.mmu.ac.uk still cited by SAMUS and UltraSam. No version, no checksums.
8. Licence agreement filled with an institutional email, sent through a form; access details sent after approval, up to 10 working days — MMU page.
9. Licence agreement (PDF); non-commercial research, cite source — BrEaST Table 1.
10. C.
11. None known.
12. Unknown.
13. US30K (SAMUS), US-43d, OpenUS.
14. Verified at the MMU page on 2026-11-25.

**B05. BUSIS**
1. Zhang, Xian, Cheng et al., "BUSIS: A Benchmark for Breast Ultrasound Image Segmentation", Healthcare 10(4):729 (2022), [DOI 10.3390/healthcare10040729](https://doi.org/10.3390/healthcare10040729).
2. Breast tumours (women aged 26 to 78) — [PMC9025635](https://pmc.ncbi.nlm.nih.gov/articles/PMC9025635/).
3. 2D B-mode.
4. 562 images; patients not stated.
5. Binary masks: 3 radiologists outlined each tumour, majority vote, reviewed by a senior expert.
6. Second Affiliated Hospital of Harbin Medical University, Affiliated Hospital of Qingdao University, Second Hospital of Hebei Medical University (China); GE VIVID 7, GE LOGIQ E9, Hitachi EUB-6500, Philips iU22, Siemens ACUSON S2000.
7. Paper gives http://cvprip.cs.usu.edu/busbench (dated 1 May 2018); the URL timed out on 2026-11-26. No checksums.
8. Unknown (no request procedure in the paper).
9. None stated (the CC BY 4.0 covers the article).
10. Unknown (D if the URL is dead).
11. None reported.
12. Unknown.
13. npj catalogue ("Steel").
14. Verified at PMC9025635 on 2026-11-25; download URL not reachable 2026-11-26.

**B06. OASBUD (Open Access Series of Breast Ultrasonic Data)**
1. Piotrzkowska-Wróblewska, Dobruch-Sobczak, Byra, Nowicki, "Open access database of raw ultrasonic signals acquired from malignant and benign breast lesions", Medical Physics 44:6105-6109 (2017), [DOI 10.1002/mp.12538](https://doi.org/10.1002/mp.12538).
2. 48 benign, 52 malignant lesions; BI-RADS; histopathology — [BrEaST Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC10830496/).
3. Post-beamformed raw RF signals (one MATLAB file).
4. 100 lesions (BrEaST Table 1); "200 images with an equal split" per [the BUS-UCLM paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC11814256/) (likely two scans per lesion; inference). OASBUD.mat 296,800,010 bytes — [Zenodo](https://zenodo.org/records/545928).
5. Class, BI-RADS, lesion regions (unverified for masks).
6. Poland (IPPT PAN, Warsaw; unverified); 1 device, 1 radiologist (BrEaST Table 1).
7. Zenodo, published 2017-08-31, [DOI 10.5281/zenodo.545928](https://doi.org/10.5281/zenodo.545928); md5 published (e2b770a6ee2f06ebe480ed0962252100).
8. Open direct link.
9. CC BY-NC 4.0 (Zenodo); "non-commercial research; cite source" (BrEaST Table 1).
10. A.
11. None known.
12. Not applicable to RF data.
13. Not in US-43d or OpenUS lists.
14. Verified at the Zenodo API record on 2026-11-25.

**B07. BUID (Breast Ultrasound Images Database, QAMEBI)**
1. Abbasian Ardakani, Mohammadi, Mirza-Aghazadeh-Attari, Acharya, "An open-access breast lesion ultrasound image database", Computers in Biology and Medicine 152:106438 (2023), [DOI 10.1016/j.compbiomed.2022.106438](https://doi.org/10.1016/j.compbiomed.2022.106438).
2. Histologically proven benign and malignant lesions — [QAMEBI page](https://qamebi.com/breast-ultrasound-images-database/).
3. 2D B-mode.
4. 232 images (109 benign, 123 malignant) — [BrEaST Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC10830496/); size not stated.
5. Radiologist masks plus "fusion" images of mask and image — QAMEBI page.
6. Iran (lead author at Shahid Beheshti University of Medical Sciences; country inferred); SuperSonic Imagine Aixplorer Ultimate (author's comment on the page).
7. qamebi.com ("Quantitative Analysis in Medicine and Biology"); direct Benign.zip and Malignant.zip links; no version, no checksums.
8. Open direct link, no form.
9. CC BY-NC 4.0.
10. A.
11. None known.
12. Unknown.
13. US-43d, OpenUS (232).
14. Verified at the QAMEBI page on 2026-11-25.

**B08. BUS_UC**
1. BUS_UC, Mendeley Data 2023-10-20, Iqbal and Sharif, [DOI 10.17632/3ksd7w7jkx.1](https://doi.org/10.17632/3ksd7w7jkx.1).
2. Benign and malignant tumours — [Mendeley page](https://data.mendeley.com/datasets/3ksd7w7jkx/1).
3. 2D B-mode, 256 x 256 pixels.
4. 358 benign + 453 malignant = 811 images (OpenUS lists 810); size not stated.
5. Class; radiologist segmentation annotations (the page says the source website gave no ground truth).
6. Uploader: COMSATS Institute of Information Technology, Wah Campus. Images come from the Ultrasound Cases website (search-result summary; unverified).
7. Mendeley Data, version 1; no checksums seen.
8. Open.
9. CC BY 4.0 as posted. If the images were taken from a teaching website, that site's own terms may limit reuse (inference; site terms not checked).
10. A (likely).
11. Possible overlap with other sets scraped from the same teaching website (inference).
12. Unknown (teaching-site images often carry markers; unverified).
13. US-43d, OpenUS.
14. Verified at the Mendeley page on 2026-11-25.

**B09. BUS-UCLM**
1. Vallez, Bueno, Deniz, Rienda, Pastor, "BUS-UCLM: Breast ultrasound lesion segmentation dataset", Scientific Data 12:242 (2025), [DOI 10.1038/s41597-025-04562-3](https://doi.org/10.1038/s41597-025-04562-3).
2. 419 normal, 174 benign, 90 malignant images — [Mendeley v3](https://data.mendeley.com/datasets/7fvgj4jsp7/3) and [paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC11814256/).
3. 2D B-mode PNG (converted from DICOM).
4. 683 images, 38 patients; size not stated.
5. RGB masks: green benign, red malignant, black background; by expert radiologists.
6. University of Castilla-La Mancha and Ciudad Real General University Hospital, Spain, 2022 to 2023; Siemens ACUSON S2000.
7. Mendeley Data, version 3 of 2025-01-27, [DOI 10.17632/7fvgj4jsp7.3](https://doi.org/10.17632/7fvgj4jsp7.3) (v1 February 2024, v2 November 2024 per search summary). The v1 link used by UltraSam answered "Dataset Not Found" on 2026-11-25.
8. Open.
9. CC BY 4.0 (Mendeley page, and the paper: "The dataset is licensed under CC-BY 4.0"). A search summary had given CC BY-NC-ND 4.0; that is the article's licence, not the data's (inference from the paper text).
10. A (likely).
11. Mirror: HF treasurenleanya/bus-uclm-breast-ultrasound-dataset.
12. Patient information removed in the DICOM-to-PNG step — paper; markers unknown.
13. US-43d (as BUS_UCML), OpenUS (264; probably only lesion images, inference).
14. Verified at Mendeley v3 on 2026-11-25 and the paper full text (Europe PMC) on 2026-11-26.

**B10. BUSI_WHU**
1. BUSI_WHU, Mendeley Data version 3 of 2025-07-23, Huang, Zhang, Zhang et al., [DOI 10.17632/k6cpmwybk3.3](https://doi.org/10.17632/k6cpmwybk3.3).
2. Benign and malignant tumours; patients aged 17 to 79 — [Mendeley page](https://data.mendeley.com/datasets/k6cpmwybk3/3).
3. 2D B-mode.
4. 927 images; 816 patients per [arXiv 2603.01295 (search summary; unverified)](https://arxiv.org/abs/2603.01295).
5. Tumour regions for segmentation; class.
6. Renmin Hospital of Wuhan University, China, December 2020 to December 2022; device not stated.
7. Mendeley Data v3; no checksums seen.
8. Open. 9. CC BY 4.0. 10. A (likely).
11. Not a BUSI subset despite the name (different hospital and years; inference). Same-patient images exist (147 images from patients with more than one image, unverified).
12. Unknown. 13. Unknown.
14. Verified at the Mendeley page on 2026-11-25.

**B11. Breast Ultrasound Image (Rodrigues 2017)**
1. Paulo Sergio Rodrigues, Mendeley Data 2017-12-31, [DOI 10.17632/wmy84gzngw.1](https://doi.org/10.17632/wmy84gzngw.1).
2. 100 benign, 150 malignant — [Mendeley page](https://data.mendeley.com/datasets/wmy84gzngw/1).
3. 2D B-mode. 4. 250 images; size not stated. 5. Class only.
6. Not stated. 7. Mendeley Data v1. 8. Open. 9. CC BY 4.0. 10. A (likely).
11. BUSC (B12) re-posts it resized with added masks.
12. Unknown. 13. Unknown.
14. Verified at the Mendeley page on 2026-11-26.

**B12. BUSC.** Mendeley [DOI 10.17632/vckdnhtw26.1](https://data.mendeley.com/datasets/vckdnhtw26/1): 100 benign + 150 malignant images at 128 x 128, built from B11, with segmentation annotations added by the uploader (search-result summary; unverified). Licence, size, checksums: unverified. Automation A (likely). Verification: unverified.

**B13. BUS Synthetic Dataset.** Mendeley [r4phtn49r7 v1](https://data.mendeley.com/datasets/r4phtn49r7/1), 9.7 MB, synthetic breast images — listed by [a GitHub list](https://github.com/hugofigueiras/Breast-Cancer-Imaging-Datasets); content, method and licence unverified.

**B14. STU-Hospital**
1. GitHub repository xbhlk/STU-Hospital (description "School and Hospital"); year and paper unknown.
2. Breast lesions (OpenUS lists anatomy as breast).
3. 2D B-mode PNG.
4. 84 PNG files in one folder, 584,448 bytes in total — [GitHub tree API](https://api.github.com/repos/xbhlk/STU-Hospital/git/trees/master?recursive=1); 42 images per [OpenUS](https://github.com/XZheng0427/OpenUS), so probably 42 images + 42 masks (inference).
5. Masks (inference from the file count).
6. "STU" may mean Shantou University (not confirmed).
7. [GitHub](https://github.com/xbhlk/STU-Hospital); no release, no checksums.
8. Open. 9. None stated (no licence file seen). 10. A (git clone).
11–12. Unknown. 13. US-43d, OpenUS.
14. Verified at the GitHub API on 2026-11-25.

**B15. S1 Data (Guo et al. 2021)**
1. Supporting file S1 of Guo, Duan, Wang, Guo, "Segmentation and recognition of breast ultrasound images based on an expanded U-Net", PLoS One 16(6):e0253202 (2021), [DOI 10.1371/journal.pone.0253202](https://doi.org/10.1371/journal.pone.0253202).
2. Normal tissue, benign and malignant tumours — [PMC8205136](https://pmc.ncbi.nlm.nih.gov/articles/PMC8205136/).
3. 2D B-mode (LOGIQ P7).
4. 200 images (the paper's train/test counts do not add up exactly); OpenUS lists 201. ZIP 25.5 MB with code and results.
5. Label maps (0, 1, 2) and grey-level probability labels.
6. A partner hospital in China (not named).
7. PMC supplementary ZIP. 8. Open. 9. None stated for the data; article CC BY 4.0. 10. A.
11–12. Unknown. 13. US-43d (as "S1"), OpenUS.
14. Verified at PMC8205136 on 2026-11-25.

**B16. GDPH&SYSUCC**
1. Released with Mo et al., "HoVer-Trans: Anatomy-aware HoVer-Transformer for ROI-free Breast Cancer Diagnosis in Ultrasound Images", IEEE TMI 2023, [DOI 10.1109/TMI.2023.3236011](https://doi.org/10.1109/TMI.2023.3236011).
2. Benign (0) and malignant (1), coded in file names — [HoVerTrans README](https://github.com/yuhaomo/HoVerTrans).
3. 2D B-mode.
4. 2,405 images — [npj catalogue](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/); size unknown.
5. Class only (README).
6. Guangdong Provincial People's Hospital and Sun Yat-sen University Cancer Center (acronym expansion unverified).
7. OneDrive share link in the README; no version, no checksums.
8. Open share link. 9. None stated. 10. A (likely; OneDrive public links can usually be fetched by script; not tested).
11–12. Unknown. 13. npj catalogue.
14. Verified at the GitHub README on 2026-11-25.

**B17. BUS-CoT**
1. "A Chain-of-thought Reasoning Breast Ultrasound Dataset Covering All Histopathology Categories", Scientific Data 2026, [DOI 10.1038/s41597-026-06702-9](https://www.nature.com/articles/s41597-026-06702-9) (article not opened; authors and institution unknown).
2. Lesions of all 99 WHO-defined histopathology categories — [figshare record](https://doi.org/10.6084/m9.figshare.30838715.v1).
3. 2D B-mode (inference).
4. 11,439 images of 11,850 lesions from 4,838 patients; curated subset of 5,163 lesion-focused images; BUSCoT.zip 6,942,371,401 bytes — [figshare API](https://api.figshare.com/v2/articles/30838715).
5. Observation, feature, diagnosis and pathology labels with expert-written reasoning; lesion characteristics, US reports, BI-RADS (search summary).
6. Unknown.
7. figshare, version 1, published 2025-12-09; md5 published (832db89dd4095f49a1a4182a72c75be8).
8. Open. 9. CC BY 4.0. 10. A.
11. Unknown. 12. Unknown. 13. None seen (too new).
14. Verified at the figshare API on 2026-11-25.

**B18. BCMID (Breast Cancer Multimodal Imaging Dataset, updated)**
1. Zenodo 2026-04-04, Seddik Tawfik, Elshenawy, Nasr et al. (Arab Academy for Science, Technology and Maritime Transport), [DOI 10.5281/zenodo.19402690](https://doi.org/10.5281/zenodo.19402690); paper unknown.
2. Breast cancer cases with BI-RADS — [Zenodo record](https://zenodo.org/records/19402690).
3. US images and mammograms per patient, plus reports.
4. 332 patients in the text but 323 patient folders (the record disagrees with itself); image count not stated; BCMID.zip 12,941,046,854 bytes.
5. BI-RADS per patient (TSV); reports.
6. Ayady Almostakbal Hospital, Alexandria, Egypt.
7. Zenodo; md5 published (7b7799c3534050b9336dec773edeee3a).
8. Open. 9. CC BY 4.0. 10. A.
11–13. Unknown.
14. Verified at the Zenodo API record on 2026-11-25.

**B19. Medical Image Database (Rodtook et al. 2018).** Rodtook, Kirimasthong, Lohitvisate, Makhanov, Pattern Recognition 79:172-182 (2018), [DOI 10.1016/j.patcog.2018.01.032](https://doi.org/10.1016/j.patcog.2018.01.032): 180 images (60 cancers, 60 cysts, 60 fibroadenomas), 1 device, 3 radiologists, multi-lesion masks, "cite source" — [BrEaST Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC10830496/). Host and access route not found (gap).

#### Breast, video

**BV1. BUSV (CVA-Net dataset)**
1. Lin, Lin, Zhu, Fu, Qin, Wang, "A New Dataset and a Baseline Model for Breast Lesion Detection in Ultrasound Videos", MICCAI 2022, pp. 614-623, DOI 10.1007/978-3-031-16437-8_59 (from the README BibTeX), [arXiv 2207.00141](https://arxiv.org/abs/2207.00141). This is the "Lin et al." video set; it is MICCAI 2022, not CVPR 2022.
2. Benign and malignant lesions — [CVA-Net README](https://github.com/jhl-Det/CVA-Net).
3. B-mode video frames.
4. 188 videos (abstract); frame total not stated in the README (25,272 frames: unverified, from memory).
5. Detection annotations (train.json, val.json); box format implied, not stated.
6. Unknown.
7. Google Drive and Baidu Netdisk links in the README; no version, no checksums.
8. Open link.
9. "Available for only non-commercial use in research or educational purpose" (README); repository has a LICENSE file of unnamed type.
10. A (Google Drive by script; large shared files can hit download quotas, inference).
11. README correction (2023-03-25): one duplicate video to delete and four videos of one patient relabelled as malignant.
12. Unknown.
13. npj catalogue (as BUSV, "Silver").
14. Verified at the README and the arXiv abstract on 2026-11-25/26.

**BV2. FLA-Net video set.** Lin et al., "Shifting More Attention to Breast Lesion Segmentation in Ultrasound Videos", MICCAI 2023, [arXiv 2310.01861](https://arxiv.org/abs/2310.01861): 572 videos, 34,300 annotated frames, 222 videos with ALN metastasis labels (search summary of the paper). [FLA-Net README](https://github.com/jhl-Det/FLA-Net): "Our dataset is currently undergoing ethical review and authorization processes within the relevant hospital"; no link. Status: closed (D). Verified at the README on 2026-11-25.

**BV3. UVBLS200.** Tu, Zhu, Duan et al., [arXiv 2403.11699](https://arxiv.org/abs/2403.11699) (2024): 200 videos (80 benign, 120 malignant), called "publicly available", 10,666 annotated images (search summary); no download link on the abstract page. Status: no route found (D). Verified at the arXiv abstract on 2026-11-25.

#### Breast-region lymph nodes

**BL1. ALN-Ultra**
1. "A Breast Cancer Ultrasound Dataset with Paired Images and Videos for Axillary Lymph Node Metastasis Prediction", Hong, Zhang, Huang, Wu, Wu, Tan (journal not found). Zenodo records [15003119](https://zenodo.org/records/15003119) (2025-03-11) and [18483501](https://zenodo.org/records/18483501) (2026-02-04, Fujian Provincial Hospital). Related paper: Frontiers in Oncology 2023, [DOI 10.3389/fonc.2023.1219838](https://doi.org/10.3389/fonc.2023.1219838).
2. ALN metastasis in early-stage breast cancer; expert diagnosis and biopsy results.
3. Paired 2D images and videos.
4. 257 patients; file sizes hidden (restricted record).
5. ALN status (biopsy), expert evaluation; clinical labels in a linked Google Sheet.
6. Fujian Provincial Hospital, China (record 18483501).
7. Zenodo, two records; GitHub link Yajie-Zhang/ALN-Ultra answered 404 via the GitHub API on 2026-11-25.
8. Zenodo "restricted": request access, owner approves.
9. CC BY 4.0 (record metadata).
10. C.
11. The two Zenodo records describe the same 257-patient set (inference: same title family and count).
12–13. Unknown.
14. Verified at both Zenodo API records on 2026-11-25.

**BL2. Lymph node ultrasound image dataset.** Zenodo [10.5281/zenodo.12702916](https://zenodo.org/records/12702916), 2024-07-10, creator Jiang Shanshan, CC BY 4.0, open, dataset.zip 645,736,210 bytes (md5 7d95e8aab4316eb5f1e25e2891ca27a5); no description, so body site (axillary or cervical), labels and paper are unknown. Automation A. Verified at the Zenodo API on 2026-11-25.

Also relevant to this group: 70 BUSI images show the axilla ([letter](https://pmc.ncbi.nlm.nih.gov/articles/PMC10293973/)), and BV2 (FLA-Net) has ALN labels but is unreleased.

#### Breast, 3D (ABUS)

**B3D1. TDSC-ABUS 2023**
1. MICCAI 2023 challenge "Tumor Detection, Segmentation and Classification Challenge on Automated 3D Breast Ultrasound"; overview paper [arXiv 2501.15588](https://arxiv.org/abs/2501.15588) (2025).
2. Benign and malignant tumours: train 42 benign / 58 malignant, validation 13 / 17, test 30 / 40 — [overview paper](https://arxiv.org/html/2501.15588v1).
3. 3D ABUS volumes, 843 x 546 x 270 to 865 x 682 x 354 voxels; in-plane spacing 0.200 or 0.073 mm, slice spacing about 0.476 mm.
4. 200 volumes (100 train, 30 validation, 70 test); patients not stated; size unknown.
5. Voxel tumour masks (10 experts, Seg3D), benign or malignant per case, boxes derived from masks; validation and test labels withheld.
6. Harbin Medical University Cancer Hospital, China; GE Invenia ABUS per the challenge site (search summary; the paper names no scanner). Files are .nrrd per the site (search summary).
7. [Challenge site](https://tdsc-abus2023.grand-challenge.org/) (the fetch tool got HTTP 403); no checksums known.
8. Signed document emailed to the organisers, who send an access link (site text via search summary; paper: signed challenge rules agreement).
9. Agreement terms not seen.
10. C.
11. Unofficial loader on PyPI, tdsc-abus2023-pytorch, that "downloads the data for you" (search summary; unverified, possibly an unofficial copy). HF peymanatlylu/abus (2023) has unknown content.
12. Unknown. 13. Project Imaging-X index.
14. Partly verified at arXiv 2501.15588 (HTML) on 2026-11-25; site terms unverified.

#### Multi-organ sets that include breast and thyroid

**M1. USenhance 2023 (Ultrasound Image Enhancement Challenge, MICCAI 2023).** [Challenge site](https://ultrasoundenhance2023.grand-challenge.org): low- and high-quality image pairs of thyroid, carotid, liver, breast and kidney; 3,000 images (1,500 pairs) from 109 patients per [the Zenodo design document](https://zenodo.org/records/7841250) (search summary); 2,464 per the [npj catalogue](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/); 2,100 per a later paper (search summary). HF derivative [Jason0411202/USenhance2023_Aligned](https://huggingface.co/datasets/Jason0411202/USenhance2023_Aligned) at 64 x 64, "academic research only". Licence and access: unverified (Grand Challenge registration likely, tier C).

**M2. Chinese ultrasound-report dataset.** Listed in the npj catalogue: 7,390 items covering breast, thyroid and liver, open, host lijunrio.github.io ([PMC12722232](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/)). Not opened; all other fields unverified.

#### Thyroid, 2D images

**T01. DDTI (Digital Database of Thyroid Images; also called TDID)**
1. Pedraza, Vargas, Narváez, Durán, Muñoz, Romero, "An open access thyroid ultrasound image database", SIPAIM 2014, Proc. SPIE 9287, 92870W (2015), [DOI 10.1117/12.2073532](https://doi.org/10.1117/12.2073532).
2. Thyroid nodules with TI-RADS — [Kaggle copy of the description](https://www.kaggle.com/datasets/dasmehdixtr/ddti-thyroid-ultrasound-images).
3. 2D B-mode.
4. Counts disagree: 99 cases, 134 images (original description, Kaggle); 347 images from 299 patients ([ThyroidXL paper](https://papers.miccai.org/miccai-2025/paper/2024_paper.pdf)); 637 (preprocessed segmentation set, [OpenUS](https://github.com/XZheng0427/OpenUS)); 481 ([npj catalogue](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/)); 637 segmentation and 349 classification images ([OpenThyroidDB card](https://huggingface.co/datasets/MedXAgent/ThyroidOpenDB)). Kaggle copy 18,746,349 bytes.
5. One XML file per case with expert annotation (boundary) and patient information.
6. Universidad Nacional de Colombia, CIM@LAB and IDIME (Instituto de Diagnóstico Médico), Colombia; device unknown.
7. Original [CIM@LAB page](http://cimalab.unal.edu.co/applications/thyroid/): TLS certificate error on 2026-11-25 (WebFetch "unable to verify the first certificate"); Kaggle mirror (2021-07-29); preprocessed copy with TN3K (T02). No checksums.
8. Original: unreachable by script; mirrors open.
9. None stated by the authors; Kaggle "Other (specified in description)".
10. D (original); B (Kaggle); A (TN3K Google Drive copy).
11. Many mirrors and re-cuts (see the overlap question).
12. Handwritten diameter marks on some images — ThyroidXL paper.
13. US30K, US-43d, OpenUS, Project Imaging-X, OpenThyroidDB.
14. Verified at the Kaggle API record and the ThyroidXL paper on 2026-11-25; original page unreachable.

**T02. TN3K**
1. Gong et al., "Multi-Task Learning for Thyroid Nodule Segmentation with Thyroid Region Prior", ISBI 2021, pp. 257-261, [DOI 10.1109/ISBI48211.2021.9434087](https://doi.org/10.1109/ISBI48211.2021.9434087); extended in Computers in Biology and Medicine 155:106389 (2023).
2. Thyroid nodules, one class; benign or malignant labels added later (MICCAI 2022 "Less is More", repo chenghui-666/ACL) — [TRFE-Net README](https://github.com/haifangong/TRFE-Net-for-thyroid-nodule-segmentation).
3. 2D B-mode; JPG or PNG (the listing is inconsistent).
4. 3,493 images from 2,421 patients, January 2016 to August 2020; 2,879 train, 614 test — [openmedlab page](https://github.com/openmedlab/Awesome-Medical-Dataset/blob/main/resources/TN3K.md); size unknown.
5. Nodule masks for all images; class labels (separate repo).
6. Zhujiang Hospital, Southern Medical University, China (listed among institutions), from more than 30,000 hospital images; lymph-node images and large colour areas excluded; various devices.
7. Google Drive file and Baidu Netdisk (code given) in the README; no version, no checksums.
8. Open link. 9. None stated for the data; code MIT. 10. A.
11. The same Drive or Baidu package also carries DDTI (preprocessed) and is the source cited for TG3K by US-43d and OpenUS (inference from their links).
12. Handwritten diameter marks on some images — [ThyroidXL paper](https://papers.miccai.org/miccai-2025/paper/2024_paper.pdf).
13. US30K, US-43d, OpenUS, Project Imaging-X, OpenThyroidDB (5,347 items for segmentation and classification).
14. Verified at the README and the openmedlab page on 2026-11-25.

**T03. TG3K.** Thyroid gland segmentation set of 3,585 images from 16 US videos, introduced from Wunderling et al. 2017 (SPIE Medical Imaging, vol. 10133, "Comparison of thyroid segmentation techniques for 3D ultrasound") per the [ThyroidXL paper](https://papers.miccai.org/miccai-2025/paper/2024_paper.pdf). US-43d, OpenUS and US30K point to the TN3K repo for it; the TN3K README itself does not mention it. Masks of the gland (inference from use). Licence: none found. Automation: A if it is in the TN3K package (unverified). Verified (counts and origin) at the ThyroidXL paper on 2026-11-25.

**T04. TN-SCUI 2020 (Thyroid Nodule Segmentation and Classification in Ultrasound Images)**
1. MICCAI 2020 challenge; design document Zhou, Jia, Ni, Noble, Huang, Tan, Van, Zenodo 2020, [DOI 10.5281/zenodo.3715942](https://doi.org/10.5281/zenodo.3715942).
2. 1,641 benign, 2,003 malignant (training set) — [openmedlab page](https://github.com/openmedlab/Awesome-Medical-Dataset/blob/main/resources/TN-SCUI2020.md).
3. 2D B-mode PNG.
4. 3,644 training images (one per patient, inferred from the naming); 910 test images (400 validation + 510 final), labels hidden.
5. Binary nodule masks; benign or malignant per image (train.csv).
6. Shanghai Ruijin Hospital through the China Medical Ultrasound Artificial Intelligence Alliance; devices not stated.
7. [Challenge site](https://tn-scui2020.grand-challenge.org/) with a "Source_links" download page (the fetch tool got HTTP 403); no checksums known.
8. Free Grand Challenge account and challenge registration (inference from the Imaging-X index entry "registration").
9. Not stated.
10. C.
11. None reported; different hospital from TN3K (no overlap known).
12. "Personal labels" were removed — openmedlab page.
13. US-43d, Project Imaging-X.
14. Verified at the openmedlab page on 2026-11-25; challenge pages not readable by the fetch tool.

**T06. TN5000**
1. Zhang, Liu, Han, Niu, Sun, "TN5000: An Ultrasound Image Dataset for Thyroid Nodule Detection and Classification", Scientific Data 12:1437 (2025), [DOI 10.1038/s41597-025-05757-4](https://doi.org/10.1038/s41597-025-05757-4).
2. 3,572 malignant and 1,428 benign nodules, biopsy confirmed — [paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC12357846/).
3. 2D B-mode, mostly 718 x 500 pixels (3,974 of 5,000).
4. 5,000 images; TN5000_forReview.zip 206,183,840 bytes plus benchmark code 14,743,013 bytes — [figshare API](https://api.figshare.com/v2/articles/28455641).
5. Bounding boxes and class in PASCAL VOC format; official image-level 7:1:2 split.
6. Cancer Hospital of the Chinese Academy of Medical Sciences, Beijing; GE Logiq E9 and S7, 5-12 or 8-15 MHz.
7. figshare, version 1, 2025-08-16, [DOI 10.6084/m9.figshare.28455641](https://doi.org/10.6084/m9.figshare.28455641); md5 published (0ec07ce543f45bce651f7266da9f3a13); code at [GitHub Qingyanyichen/TN5000-2025](https://github.com/Qingyanyichen/TN5000-2025).
8. Open. 9. CC BY (figshare; the paper says permission was obtained to distribute under CC BY). The article itself is CC BY-NC-ND 4.0. 10. A.
11. Split is image level, so images of one patient may fall in train and test; a 2026 study noted patient independence cannot be verified (search summary). Mirror: HF Johnyquest7/TN5000-thyroid-nodule-classification; inside OpenThyroidDB with derived SAM2 masks.
12. Crosshair markers: 60% of images have none, 17% outside the box, 21% touching the box, 2% inside — paper Table 3.
13. npj catalogue ("Platinum"), OpenThyroidDB.
14. Verified at the figshare API on 2026-11-25 and the paper full text (Europe PMC) on 2026-11-26.

**T07. ThyroidXL**
1. Duong (Viet Hung D.) et al., "ThyroidXL: Advancing Thyroid Nodule Diagnosis with an Expert-Labeled, Pathology-Validated Dataset", MICCAI 2025, DOI 10.1007/978-3-032-05182-0_60 (from the HF card), [paper PDF](https://papers.miccai.org/miccai-2025/paper/2024_paper.pdf).
2. Benign or malignant from FNA cytology (Bethesda) and surgical pathology; ACR TI-RADS.
3. 2D B-mode PNG (frames chosen from video sequences).
4. 11,635 images from 4,093 patients; train 9,541 images / 3,354 patients, validation 2,094 / 739.
5. Class, segmentation masks (2 annotators, third senior on 8% of conflicts), boxes (OpenThyroidDB lists 11,631 items with masks and boxes).
6. Vietnam National Hospital of Endocrinology, Hanoi, with VNPT AI; Hitachi Aloka Arietta V70.
7. [HF VNPT-AI/ThyroidXL](https://huggingface.co/datasets/VNPT-AI/ThyroidXL) (moved from hunglc007/ThyroidXL, the URL in the paper), created 2025-06-27, 20,599 downloads — [HF API](https://huggingface.co/api/datasets/VNPT-AI/ThyroidXL). Checksums: HF stores file hashes (inference).
8. Gated "auto": click-through terms. 9. Not stated in the card metadata; card terms not readable without login. 10. C, then B.
11. Redistributed inside OpenThyroidDB.
12. Regions with patient information cropped; the paper claims no handwritten marks.
13. OpenThyroidDB.
14. Verified at the paper PDF (text) and HF API on 2026-11-25.

**T08. ThyUS2Path (Hou et al. 2024)**
1. Hou, Hua, Zhang et al., "An ultrasonography of thyroid nodules dataset with pathological diagnosis annotation for deep learning", Scientific Data 2024, [DOI 10.1038/s41597-024-04156-5](https://doi.org/10.1038/s41597-024-04156-5). "ThyUS2Path" is the name used by the HF collections, not by the authors.
2. Benign or malignant by histology; batch 1 has 218 benign and 383 malignant patients — [paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC11585535/).
3. 2D B-mode JPG.
4. 8,508 images from 842 patients: batch 1 6,005 images / 601 patients, batch 2 2,503 / 241; two RAR files of 733,094,233 and 906,941,808 bytes (1.64 GB) — [figshare API](https://api.figshare.com/v2/articles/27021604).
5. Pathology label per patient (no masks stated).
6. Second Affiliated Hospital of Jiaxing University, China, 2019 to 2022; Esaote MyLab (portable, 3.5 MHz probe as stated).
7. figshare, version 1, 2024-09-15, [DOI 10.6084/m9.figshare.27021604.v1](https://doi.org/10.6084/m9.figshare.27021604.v1); md5 published.
8. Open. 9. CC BY 4.0 (figshare; the article is CC BY-NC-ND 4.0). 10. A (RAR archives need an unrar tool).
11. Redistributed in OpenThyroidDB and Doul0414/ThyroidDataSet. Several images per patient: split by patient.
12. Images cropped to remove patient information — paper.
13. OpenThyroidDB.
14. Verified at the figshare API and the paper full text (Europe PMC) on 2026-11-26.

**T09. AUITD (Algerian Ultrasound Images Thyroid Dataset)**
1. Kaggle dataset by azouz maroua, updated 2022-07-16; paper unknown.
2. Benign 1,472, malignant 1,895, normal 171 — [Kaggle API record](https://www.kaggle.com/api/v1/datasets/view/azouzmaroua/algeria-ultrasound-images-thyroid-dataset-auitd).
3. 2D B-mode. 4. 3,538 images; 131,106,028 bytes. 5. Class; labelled by volunteer doctors.
6. Hospitals in Setif, Algeria. 7. Kaggle only; no checksums. 8. Free account. 9. "Unknown". 10. B.
11. Unknown. 12. Many images have "manual noise" around the nodule; only 781 clean (182 benign, 599 malignant) per a later paper (search summary; unverified).
13. U2-Bench (search summary).
14. Verified at the Kaggle API record on 2026-11-25.

**T14. Thyroid_Ultrasound_Images (FangDai, HF).** 900 images, 300 each of papillary, follicular and medullary thyroid carcinoma, tied to a paper on rare thyroid cancer subtypes; HF gated "auto", licence "apache-2.0" as declared by the uploader, created 2025-02-03 — [HF API](https://huggingface.co/api/datasets/FangDai/Thyroid_Ultrasound_Images). Source hospital unknown. Automation C, then B. Verified 2026-11-25.

**T15. PTC pathomics + US radiomics (Pang et al. 2024).** Mendeley [DOI 10.17632/dp7zp2pb2v.1](https://data.mendeley.com/datasets/dp7zp2pb2v/1), 2024-10-22: thyroid US images plus FNA cytology slide image blocks, 222 papillary carcinoma and 163 benign cases; CC BY 4.0; institution, device and file sizes not shown. Automation A (likely). Verified 2026-11-25.

**T16. TGN dataset.** Mendeley [DOI 10.17632/8gpvhrrghk.1](https://data.mendeley.com/datasets/8gpvhrrghk/1), 2024-06-17, CC BY 4.0, categories endocrinology; the description is a generic Mask R-CNN guide, so anatomy, counts and labels are not stated. Low confidence that it is a usable thyroid set. Verified 2026-11-25.

**T20. Abnormal thyroid ultrasound images (IEEE DataPort).** 34 abnormal images, a refined subset of the Kaggle DDTI copy — [IEEE DataPort](https://ieee-dataport.org/documents/abnormal-thyroid-ultrasound-images-0) (search summary; unverified). Access needs an IEEE account (unverified).

#### Thyroid, video and cine

**T05. Stanford AIMI Thyroid Ultrasound Cine-clip**
1. Stanford AIMI Center dataset, DOI [10.71718/7m5n-rh16](https://doi.org/10.71718/7m5n-rh16) (year and first paper not on the page).
2. 192 biopsy-confirmed nodules — [AIMI page](https://aimi.stanford.edu/datasets/thyroid-ultrasound-cine-clip).
3. B-mode cine clips (video).
4. 167 patients, 192 cine clips (ThyroidXL paper); about 17,412 frames ([OpenUS](https://github.com/XZheng0427/OpenUS)) or 17,417 ([OpenThyroidDB](https://huggingface.co/datasets/MedXAgent/ThyroidOpenDB)); size not stated.
5. Radiologist segmentations, TI-RADS descriptors, histopathology, demographics, lesion size and location.
6. Stanford University Medical Center, USA; device not stated.
7. Download through Redivis (stanford.redivis.com); UltraSam still links the older Azure portal (stanfordaimi.azurewebsites.net). No checksums seen.
8. Account login; the "Terms & Conditions" and "License" headings on the page were empty in the fetched text. npj lists it as "available on request".
9. Not visible (Stanford's research use agreement is usual for AIMI sets; unverified).
10. C (account and terms), then B (Redivis API token; inference).
11. Redistributed inside OpenThyroidDB as "CineClip" (check whether that respects the Stanford terms; inference).
12. Unknown.
13. US-43d, OpenUS, OpenThyroidDB.
14. Verified at the AIMI page on 2026-11-25; terms unverified.

**T11. Free-hand wireless-probe neck ultrasound sweeps (HF freehand-us-anon)**
1. Anonymous HF dataset created 2026-09-26 (anonymous account, likely under review; inference); no paper.
2. Healthy-participant neck sweeps for label-free domain adaptation; 4-class segmentation (background, thyroid, common carotid artery lumen, trachea) — [HF card](https://huggingface.co/datasets/freehand-us-anon/freehand-thyroid-sweeps).
3. Free-hand B-mode video (H.264), SonoStar 5W wireless linear probe.
4. 29 participants (16 aged 18-44, 13 aged 65+), 29 sweeps, 107,614 frames, 86 min; 20,014 unlabelled pool frames; videos 1.54 GiB, pool 960 MiB, weights 258 MiB.
5. 232 annotated frames (labelme polygons): 174 with released labels, 58 hidden test labels; scan-plane and uncertainty flags.
6. Recorded in a laboratory session and a community screening event; institution not stated.
7. HF, not gated, 2,350 downloads; SHA256SUMS file published.
8. Open. 9. CC BY-NC 4.0 (data, labels, weights); code MIT. 10. A.
11. None known.
12. Overlay text masked; de-identification record per participant (masks.json).
13. None (new).
14. Verified at the HF README on 2026-11-25.

**T13. KFGNet video data.** [NeuronXJTU/KFGNet](https://github.com/NeuronXJTU/KFGNet): README gives a Baidu Netdisk link with an extraction code for "ultrasonic data", no licence, no counts; secondary sources describe it as thyroid nodule video data, 3,668 items ([npj catalogue](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/)). Automation D from a cloud server (Baidu Netdisk usually needs a Baidu account or client; inference). Verified at the README on 2026-11-26.

**T19. VTUS.** 100 thyroid US video sequences described in the Vivim paper ([arXiv 2401.14168](https://arxiv.org/abs/2401.14168), search summary); no release found.

#### Thyroid, 3D

**T10. SegThy**
1. Krönke, Eilers, Dimova et al., "Tracked 3D ultrasound and deep neural network-based thyroid segmentation reduce interobserver variability in thyroid volumetry", PLOS ONE 2022, [DOI 10.1371/journal.pone.0268550](https://doi.org/10.1371/journal.pone.0268550).
2. Healthy thyroid (sub-dataset 1) and routine thyroid patients (sub-dataset 2) — [TUM page](https://www.cs.cit.tum.de/camp/publications/segthy-dataset/).
3. Tracked free-hand 3D US (0.12 mm isotropic voxels) and T1 VIBE MRI.
4. Sub-dataset 1: 28 volunteers, 1 MRI + 9 3D US scans each; sub-dataset 2: 186 patients, 6 3D US scans each. The HF mirror card says only the volunteer part was released (search summary; unverified).
5. Thyroid label maps for all of sub-dataset 1; being extended to trachea, carotids, jugular veins and nodules. The HF mirror labels thyroid, both common carotids and both internal jugular veins.
6. TUM (Klinikum rechts der Isar), Munich, Germany (inference from authors); Siemens Acuson NX-3 with VF12-4; electromagnetic tracking (PIUR tUS).
7. Direct ZIPs (MRI_data.zip, US_data.zip) on campar.in.tum.de; HF mirror [MedOtter/SegThy](https://huggingface.co/datasets/MedOtter/SegThy) (2026-08-05, CC BY 4.0, 162 files). No checksums seen.
8. Open direct link. 9. CC BY; "permits commercial use as long as the authors are cited". 10. A.
11. HF mirror; PIUR_Thyroid_segmentation (T12) may derive from the same system (inference only).
12. Not applicable (3D reconstructions).
13. US-43d, OpenUS (12,737, probably 2D slices; inference), npj (214 subjects).
14. Verified at the TUM page and HF API on 2026-11-25.

**T12. PIUR_Thyroid_segmentation (HF Ultraclear).** Created 2026-09-29, not gated, CC BY-NC 4.0, 263 downloads; the card holds only the licence line, so content is unknown — [HF API](https://huggingface.co/api/datasets/Ultraclear/PIUR_Thyroid_segmentation). Verified 2026-11-25.

#### Thyroid collections (re-distributions)

**T17. OpenThyroidDB (HF MedXAgent/ThyroidOpenDB)**
1. HF dataset created 2026-07-16, "supporting the ThyroidXAgent evidence workflow"; no paper citation on the card — [HF card](https://huggingface.co/datasets/MedXAgent/ThyroidOpenDB).
2. Segmentation, benign or malignant classification, report generation, malignant-lesion stratification.
3. 2D images, videos, image-report pairs.
4. 61.8 GB, 38 files. External parts (counts are curated subsets): AHU 125,896 (classification), CineClip 17,417, DDTI 637/349, KMVE 2,474 reports / 15,921 images, PKTN 1,003, TG3K, TGVideo 15,186, TN3K 5,347, TN5000 5,000 (+ SAM2-derived masks), ThyUS2Path 8,508, ThyroidXL 11,631. New MedXAgent cohorts: SMU-HMC 23,955 reports / 248,194 images (multicentre), TNVideo 148 cases (sparse boxes), ZJH-8K 7,958 images, ZJH-TS 353 reports / 4,471 images.
5. Masks, boxes, classes, free-text reports (varies by part).
6. Scanners listed: GE, Fujifilm, Hitachi Aloka, Mindray, Toshiba, Esaote, Samsung Medison, SuperSonic Imagine; institutions of the new cohorts not stated.
7. HF; file hashes held by HF (inference).
8. Gated "manual": owner approval; terms: research, education and method development only; respect source licences and redistribution limits; no re-identification; not for clinical use.
9. No repository licence; "inclusion does not relicense an external resource".
10. C, then B.
11. Re-distributes T01, T02, T03, T05, T06, T07, T08 — do not count those twice.
12. Unknown.
13. Source of the ThyroidXAgent work (no paper found).
14. Verified at the HF card and HF API on 2026-11-25.

**T18. ThyroidDataSet (HF Doul0414).** Gated "manual", created 2025-11-21; a collection of ZIP archives "TGVideo, DDTI, TN3K, 24-TMI, TN5K, ThyUS2Path…" — [HF API](https://huggingface.co/api/datasets/Doul0414/ThyroidDataSet); licence not stated; README not readable without access. Automation C, then B. Verified 2026-11-25.

### Inferences
- Several Scientific Data descriptors (TN5000, ThyUS2Path, BUS-UCLM) put the article under CC BY-NC-ND 4.0 while the data are CC BY or CC BY 4.0; aggregators that copy the article licence report the wrong data licence.
- Where a Kaggle or HF uploader set the licence (BUSI CC0, FangDai Apache-2.0, theshoaibme CC BY 4.0 for BUSI), the licence is the uploader's claim, not the authors'; treat it as unknown for the original.
- Checksums are published by Zenodo and figshare records (md5) and by one HF set (SHA256SUMS); TCIA, Mendeley, Kaggle and GitHub sources showed none.

### Gaps
- Licence terms of TDSC-ABUS, TN-SCUI 2020 and the Stanford cine-clip set were not readable (Grand Challenge returned HTTP 403 to the fetch tool; the AIMI terms text was empty).
- BUS-CoT authors, institution and devices; BUSI, TN3K, CVA-Net and Mendeley file sizes; patient counts for several sets.
- Whether SegThy's US_data.zip includes the 186-patient sub-dataset.
- Use by MedSAM, SA-Med2D-20M, BiomedParse and USFM was not checked.

## Which datasets are subsets, re-releases or merges of others, and which have known duplicates or label problems?

### Takeaway
BUSI is the most re-uploaded and the most flawed set (155 duplicate images, 70 axilla images, burned-in annotations), and at least four cleaned subsets exist; on the thyroid side, two HF collections (OpenThyroidDB and Doul0414) re-distribute almost every public thyroid set, so a dedup step must key on the original sets, not on hosts.

### Cited Findings
- BUSI duplicates and defects: 155 of 780 images (about 19%) are copies; Appendix B lists 235 duplicated lesion-image entries; 8 or 9 benign-malignant and 2 benign-normal cross-class pairs; masks of duplicates differ; 70 axilla images; at least 7 images with a biopsy needle; at least 19 images with questionable lesion type; at most 529 usable images, 399 without annotations; a CSV mapping the letter's numbering to the original file names is on [Mendeley Data, DOI 10.17632/k8t3gnx9h6.1](https://doi.org/10.17632/k8t3gnx9h6.1) — [Pawłowska, Karwat, Żołek 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10293973/).
- The BrEaST authors put BUSI's significant defects at "more than 40%" of images — [PMC10830496](https://pmc.ncbi.nlm.nih.gov/articles/PMC10830496/).
- Cleaned BUSI subsets: 450 images (64 normal, 222 benign, 164 malignant) in [caumente/multi_task_breast_cancer](https://github.com/caumente/multi_task_breast_cancer) (search summary; unverified); BUSI-A1, A2, A3 (three ways to drop one of each duplicate pair; sizes not given) — [arXiv 2508.17768](https://arxiv.org/html/2508.17768v1), which calls the non-breast images "maxilla" where the letter says axilla; a 629-image curated copy on [Zenodo 21128640](https://zenodo.org/records/21128640) (Universidad de La Rioja, 2026, CC BY 4.0 set by the re-uploaders).
- Leakage size: with a random split, about 32.5% of BUSI test images have a duplicate or same-subject image in training (search summary of [arXiv 2603.01295](https://arxiv.org/abs/2603.01295); not in the abstract, unverified).
- BUSI derivative: BreastMNIST in MedMNIST (listed in the [Project Imaging-X index](https://github.com/uni-medical/Project-Imaging-X); derivation from BUSI is from memory, unverified).
- BUSI mirrors on HF (search API, 2026-11-25): gymprathap/Breast-Cancer-Ultrasound-Images-Dataset, theshoaibme/panorgan-busi-breast-ultrasound (10,002 downloads, "CC BY 4.0"), ztroll/breast-ultrasound-images-dataset-dataset-busi, kasumi222/busigt, josedonoso/busi-dataset-v2, treasurenleanya/breast-ultrasound-images-dataset — [HF search API](https://huggingface.co/api/datasets?search=BUSI).
- Merged breast collections on HF without stated sources: BTX24/ultrasound-breast-classification-combined-pathology (3,524 train + 881 test = 4,405 images, 0.85 GB) and a "combined-birads" variant — [HF README](https://huggingface.co/datasets/BTX24/ultrasound-breast-classification-combined-pathology).
- BUSC re-posts the Rodrigues set (B11) resized, with added masks (search summary). BUS_UC images come from a teaching website (search summary).
- BUSV (CVA-Net) had one duplicate video and four mislabelled videos, corrected in the README on 2023-03-25 — [CVA-Net README](https://github.com/jhl-Det/CVA-Net).
- Thyroid re-distributions: OpenThyroidDB carries AHU, CineClip, DDTI, KMVE, PKTN, TG3K, TGVideo, TN3K, TN5000, ThyUS2Path and ThyroidXL — [HF API file list](https://huggingface.co/api/datasets/MedXAgent/ThyroidOpenDB); Doul0414/ThyroidDataSet carries TGVideo, DDTI, TN3K, 24-TMI, TN5K, ThyUS2Path — [HF API](https://huggingface.co/api/datasets/Doul0414/ThyroidDataSet); HF Johnyquest7/TN5000-thyroid-nodule-classification mirrors TN5000.
- DDTI appears with five different counts (134, 347, 481, 637, 349) depending on the cut — see entry T01; the TN3K package carries a preprocessed DDTI — [OpenUS README](https://github.com/XZheng0427/OpenUS).
- TG3K is frames from 16 videos of an earlier 3D-segmentation study (Wunderling et al. 2017) — [ThyroidXL paper](https://papers.miccai.org/miccai-2025/paper/2024_paper.pdf).
- TN5000 is split at image level, so one patient's images can sit in both train and test — [paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC12357846/).
- Burned-in marks in thyroid sets: handwritten diameter marks in DDTI and TN3K (ThyroidXL paper); crosshair markers in about 40% of TN5000 images (TN5000 paper Table 3).
- Breast image cleaning software exists: BUSClean, open-source pre-processing for BUS images — [arXiv 2407.11316](https://arxiv.org/pdf/2407.11316) (scope from the title; unverified).

### Inferences
- Dedup keys for a later step: (1) BUSI internal duplicates via the Mendeley CSV; (2) the same original set reached through Kaggle, HF, Zenodo re-uploads and the two thyroid collections; (3) DDTI and TG3K inside the TN3K package; (4) the two ALN-Ultra Zenodo records; (5) BUSC versus Rodrigues; (6) SegThy versus its HF mirror.
- Cross-dataset overlaps between independent hospital sets (for example BUSI and BUS_UC, or TN3K and TN-SCUI) are not reported anywhere I found; only a pixel-level dedup can rule them out.

### Gaps
- Overlap between BUS_UC and the teaching website's other scrapes, and between OpenThyroidDB's AHU, KMVE, PKTN, TGVideo parts and any original release, is unknown (origins of these parts not identified).
- No duplicate audit was found for BUS-BRA, BUS-UCLM, BUSI_WHU, TN3K or AUITD.

## Which are the largest by image count, and which are open with a permissive licence?

### Takeaway
The largest released single sets are ThyroidXL (11,635 images), BUS-CoT (11,439), ThyUS2Path (8,508) and TN5000 (5,000); counting gated collections and video frames, OpenThyroidDB's new SMU-HMC cohort (248,194 images) and the free-hand thyroid sweeps (107,614 frames) are larger. The open, permissive (CC BY or CC BY 4.0) and tier-A sets are BUS-CoT, BUS-BRA, BrEaST, BCMID, BUS-UCLM, BUSI_WHU, TN5000, ThyUS2Path and SegThy, plus small Mendeley sets.

### Cited Findings

**Table 2. Largest breast and thyroid ultrasound datasets by image count (released or gated; status 2026-11-25/26).** For scale: the project's current training set is about 20k images (dataset version 261023).

| Rank | Dataset | Anatomy | Images (n) | Patients (n) | Access, automation | Source |
|---|---|---|---|---|---|---|
| 1 | OpenThyroidDB, SMU-HMC cohort | Thyroid | 248,194 (with 23,955 reports) | not stated | HF manual approval, C then B | [HF card](https://huggingface.co/datasets/MedXAgent/ThyroidOpenDB) |
| 2 | OpenThyroidDB, AHU part | Thyroid | 125,896 (origin unknown) | not stated | HF manual approval, C then B | same |
| 3 | Free-hand thyroid sweeps | Thyroid, neck | 107,614 video frames (232 labelled) | 29 | Open, A | [HF card](https://huggingface.co/datasets/freehand-us-anon/freehand-thyroid-sweeps) |
| 4 | Stanford cine-clip | Thyroid | about 17,412 frames | 167 | Account + terms, C then B | [OpenUS](https://github.com/XZheng0427/OpenUS), [AIMI](https://aimi.stanford.edu/datasets/thyroid-ultrasound-cine-clip) |
| 5 | ThyroidXL | Thyroid | 11,635 | 4,093 | HF click-through, C then B | [paper](https://papers.miccai.org/miccai-2025/paper/2024_paper.pdf) |
| 6 | BUS-CoT | Breast | 11,439 | 4,838 | Open, A | [figshare](https://doi.org/10.6084/m9.figshare.30838715.v1) |
| 7 | ThyUS2Path | Thyroid | 8,508 | 842 | Open, A | [figshare](https://doi.org/10.6084/m9.figshare.27021604.v1) |
| 8 | OpenThyroidDB, ZJH-8K | Thyroid | 7,958 | not stated | HF manual approval, C then B | [HF card](https://huggingface.co/datasets/MedXAgent/ThyroidOpenDB) |
| 9 | TN5000 | Thyroid | 5,000 | not stated | Open, A | [paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC12357846/) |
| 10 | TN-SCUI 2020 | Thyroid | 3,644 (+910 unlabelled test) | 3,644 (inferred) | Challenge registration, C | [openmedlab](https://github.com/openmedlab/Awesome-Medical-Dataset/blob/main/resources/TN-SCUI2020.md) |
| 11 | TG3K | Thyroid gland | 3,585 frames | 16 videos | Open (unverified), A | [ThyroidXL paper](https://papers.miccai.org/miccai-2025/paper/2024_paper.pdf) |
| 12 | AUITD | Thyroid | 3,538 | not stated | Kaggle, B | [Kaggle API](https://www.kaggle.com/api/v1/datasets/view/azouzmaroua/algeria-ultrasound-images-thyroid-dataset-auitd) |
| 13 | TN3K | Thyroid | 3,493 | 2,421 | Open, A | [openmedlab](https://github.com/openmedlab/Awesome-Medical-Dataset/blob/main/resources/TN3K.md) |
| 14 | GDPH&SYSUCC | Breast | 2,405 | not stated | OneDrive, A (likely) | [npj](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/) |
| 15 | BUS-BRA | Breast | 1,875 | 1,064 | Open, A | [npj](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/), [Zenodo](https://zenodo.org/records/8231412) |

Breast videos and volumes, not in Table 2: FLA-Net set 572 videos / 34,300 frames (unreleased); BUSV 188 videos (open); UVBLS200 200 videos (no link); ALN-Ultra 257 patients (restricted); TDSC-ABUS 200 volumes (agreement). BCMID (12.94 GB, 332 patients) states no image count.

**Table 3. Open datasets with a permissive licence and tier-A download (status 2026-11-25/26).** Permissive here means CC BY, CC BY 4.0 or CC0 as set by the authors; non-commercial licences are listed separately below the table.

| Dataset | Anatomy | Images (n) | GB | Licence | Host | Checksums |
|---|---|---|---|---|---|---|
| BUS-CoT | Breast | 11,439 | 6.94 | CC BY 4.0 | figshare | md5 |
| ThyUS2Path | Thyroid | 8,508 | 1.64 | CC BY 4.0 | figshare | md5 |
| TN5000 | Thyroid | 5,000 | 0.22 | CC BY | figshare | md5 |
| BUS-BRA | Breast | 1,875 | 0.134 | CC BY 4.0 | Zenodo | md5 |
| BUSI_WHU | Breast | 927 | unknown | CC BY 4.0 | Mendeley | not seen |
| BUS_UC | Breast | 811 | unknown | CC BY 4.0 (source-site caveat) | Mendeley | not seen |
| BUS-UCLM | Breast | 683 | unknown | CC BY 4.0 | Mendeley | not seen |
| BrEaST | Breast | 256 | 0.067 | CC BY 4.0 | TCIA | not seen |
| Rodrigues | Breast | 250 | unknown | CC BY 4.0 | Mendeley | not seen |
| SegThy | Thyroid 3D | 28 volunteers (+186 patients) | unknown | CC BY | TUM site | not seen |
| BCMID | Breast (+ mammography) | not stated (332 patients) | 12.94 | CC BY 4.0 | Zenodo | md5 |
| PTC pathomics + US | Thyroid | 385 cases | unknown | CC BY 4.0 | Mendeley | not seen |

Sources: entries B17, T08, T06, B02, B10, B08, B09, B03, B11, T10, B18 and T15 under the per-dataset question.

- Open but non-commercial: OASBUD (CC BY-NC 4.0, [Zenodo](https://zenodo.org/records/545928)), BUID (CC BY-NC 4.0, [QAMEBI](https://qamebi.com/breast-ultrasound-images-database/)), free-hand thyroid sweeps and PIUR_Thyroid_segmentation (CC BY-NC 4.0, HF), BUSV (non-commercial research or education, [README](https://github.com/jhl-Det/CVA-Net)).
- Open but no licence stated: TN3K, TG3K, DDTI, STU-Hospital, S1, GDPH&SYSUCC — see their entries.

### Inferences
- A first automated pull of only open, permissive, tier-A sets would bring about 31,000 breast and thyroid images (sum of the Table 3 image counts that are stated, excluding BCMID and SegThy), about 1.5 times the project's current 20k-image training set; BUS-CoT, ThyUS2Path and TN5000 make up about 80% of it.
- Adding the no-licence GitHub/Drive sets (TN3K, DDTI, TG3K) would add about 7,700 images but carries licence risk; asking the authors is the safe route.
- The gated thyroid collection (OpenThyroidDB) is the single largest source, but its terms restrict use to research and its new cohorts have no stated licence; it needs a decision by the user, not automation.

### Gaps
- Image counts are missing for BCMID, the lymph node set (BL2) and USenhance's breast and thyroid parts, so they are absent from Table 2.
- Download sizes for Mendeley sets were not shown on their pages.

## Gaps: datasets mentioned but not found, dead links, and private datasets with no access route

### Takeaway
The main holes are parathyroid (nothing public), breast elastography and breast CEUS (nothing public), unreleased breast video sets (FLA-Net, UVBLS200), and several links that a script cannot use today (BUSI's captcha page, DDTI's TLS error, BUSIS timeout, Grand Challenge pages refusing the fetch tool).

### Cited Findings
- Unreleased or no route: FLA-Net 572-video set ("under ethical review", [README](https://github.com/jhl-Det/FLA-Net)); UVBLS200 ("publicly available" but no link, [arXiv 2403.11699](https://arxiv.org/abs/2403.11699)); VTUS 100 thyroid videos ([arXiv 2401.14168](https://arxiv.org/abs/2401.14168), search summary); Medical Image Database of Rodtook et al. 2018 (no host found, [DOI 10.1016/j.patcog.2018.01.032](https://doi.org/10.1016/j.patcog.2018.01.032)).
- Private datasets seen in passing (unverified): a Mayo Clinic BUS set of 160 videos from 136 patients with 22,202 extracted images (search summary for [arXiv 2210.05762](https://arxiv.org/pdf/2210.05762); paper not opened); a multicentre thyroid set from more than 20 hospitals with 9,669 images from 5,224 patients (search summary); breast CEUS cohorts of 190 tumours from two centres ([PMC9523748](https://pmc.ncbi.nlm.nih.gov/articles/PMC9523748)) and 128 ALN cases from Fujian Provincial Cancer Hospital ([PMC12729765](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12729765/)).
- Parathyroid: no public US dataset found on Zenodo, in the npj catalogue (no parathyroid entry, [PMC12722232](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722232/)) or by web search; parathyroid deep-learning papers used institutional data, e.g. [QIMS 154049](https://qims.amegroups.org/article/view/154049).
- Breast elastography: only phantoms and simulations found, e.g. [QIBA shear-wave phantoms](https://research.repository.duke.edu/concern/datasets/qz20st03m?locale=en).
- Dead or blocked links on 2026-11-25/26: BUSI original page behind reCAPTCHA ([page](https://scholar.cu.edu.eg/?q=afahmy/pages/dataset)); DDTI original TLS certificate error ([page](http://cimalab.unal.edu.co/applications/thyroid/)); BUSIS URL timed out (http://cvprip.cs.usu.edu/busbench); BUS-UCLM version 1 link "Dataset Not Found" while version 3 works ([v3](https://data.mendeley.com/datasets/7fvgj4jsp7/3)); ALN-Ultra GitHub repo not found by the GitHub API; Grand Challenge pages of TDSC-ABUS and TN-SCUI returned HTTP 403 to the fetch tool (not necessarily dead); the Stanford set moved from an Azure portal to Redivis ([AIMI page](https://aimi.stanford.edu/datasets/thyroid-ultrasound-cine-clip)).
- Unidentified parts of thyroid collections: AHU, KMVE, PKTN, TGVideo (OpenThyroidDB) and 24-TMI (Doul0414) — names only, origin not found ([HF card](https://huggingface.co/datasets/MedXAgent/ThyroidOpenDB)).

### Inferences
- For breast videos, the only scriptable public source is BUSV (188 videos, non-commercial); for ABUS, only TDSC-ABUS (agreement by email).
- Thyroid challenges on Grand Challenge: only TN-SCUI 2020 (and USenhance 2023, which includes thyroid) were found; I found no 2024 to 2026 thyroid challenge.

### Gaps
- Not checked: Science Data Bank, Synapse, PhysioNet, Baidu AI Studio, full Kaggle and IEEE DataPort searches, thyroid CEUS and elastography, and the dataset lists of MedSAM, SA-Med2D-20M, BiomedParse and USFM.
- The "Chinese ultrasound-report dataset" (M2) and USenhance 2023 (M1) were not opened at source.

#### Seen, other groups (not breast or thyroid; for the other researchers)
From the [UltraSam README](https://github.com/CAMMA-public/UltraSam) and [OpenUS README](https://github.com/XZheng0427/OpenUS) unless noted:
- Heart: [CAMUS](https://humanheart-project.creatis.insa-lyon.fr/database/#collection/6373703d73e9f0047faa1bc8g), [EchoNet-Dynamic](https://github.com/echonet/dynamic), [EchoNet-Pediatric](https://echonet.github.io/pediatric/), [CardiacUDC](https://www.kaggle.com/datasets/xiaoweixumedicalai/cardiacudc-dataset), [EchoCP](https://www.kaggle.com/datasets/xiaoweixumedicalai/echocp), [CACTUS](https://github.com/coding-groot/cactus), [HMC-QU](https://aistudio.baidu.com/aistudio/datasetdetail/102406) (from SAMUS).
- Fetal and gynaecologic: [ACOUSLIC-AI](https://acouslic-ai.grand-challenge.org/overview-and-goals/), [HC18](https://hc18.grand-challenge.org/), [FH-PS-AOP](https://zenodo.org/records/10829116), [FASS](https://data.mendeley.com/datasets/4gcpm9dsc3/1), [Fetal_Planes_DB](https://zenodo.org/records/3904280), [IUGC25](https://www.codabench.org/competitions/9735/#/phases-tab), [MMOTU](https://github.com/cv516Buaa/MMOTU_DS2Net).
- Abdomen and urology: [AbdomenUS](https://www.kaggle.com/datasets/ignaciorlando/ussimandsegm), [ASUS](https://github.com/SlicerIGT/aigt), [AUL](https://zenodo.org/records/7272660), [105US](https://www.researchgate.net/publication/329586355_100_2D_US_Images_and_Tumor_Segmentation_Masks), [kidneyUS](https://github.com/rsingla92/kidneyUS), [MicroSeg](https://zenodo.org/records/10475293), [regPro](https://muregpro.github.io/data.html), [GIST514-DB](https://github.com/howardchina/query2).
- Other: [brachial plexus](https://github.com/Regional-US/brachial_plexus), [UPBD](https://ubpd.worldwidetracing.com:9443/), [US nerve segmentation](https://www.kaggle.com/c/ultrasound-nerve-segmentation/data), [FALLMUD](https://kalisteo.cea.fr/index.php/fallmud/#), [STMUS_NDA](https://data.mendeley.com/datasets/3jykz7wz8d/1), [CCAUI](https://data.mendeley.com/datasets/d4xt63mgjm/1), [LUSS_phantom](https://archive.researchdata.leeds.ac.uk/1263/), [USAnotAI](https://github.com/ftsvd/USAnotAI).
