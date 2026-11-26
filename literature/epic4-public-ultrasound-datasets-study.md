# Public ultrasound datasets for epic 4, stage 1: census, download plan and AWS design

- Date: 2026-11-26. Written by Claude (Opus 5.5) at the user's request. The user named this work
  "epic 4" (public ultrasound datasets). Stage 1, the focus here: list the public datasets, plan the
  download of each, store them in a private S3 bucket (for speed and as a backup), run the downloader
  on EC2, and give scoped long-lived access to the bucket. Stage 2 (dedup against dataset 261023, a
  next dataset version built from public data, a "super-dataset" composed at runtime) is only
  prepared for here.
- For: epic 4, whose mission is [DEC-117](../decisions/DEC-117-epic4-mission-public-ultrasound-datasets.md)
  (accepted on 2026-11-26, after this study was written; the next sessions follow the
  [epic 4 relay note](../journal/2026/2026-11-26-epic4-relay-claude.md)). It feeds epic 1
  ([DEC-065](../decisions/DEC-065-mission-upper-abdomen-anatomy-segmentation.md), upper-abdomen
  anatomy segmentation) and epic 3 ([DEC-100](../decisions/DEC-100-epic3-mission-spot-liver-diseases.md),
  spotting liver diseases). It sits beside epic 2
  ([DEC-081](../decisions/DEC-081-epic2-mission-roboflow-universe-ultrasound-scraper.md), the
  Roboflow Universe scraper), which covers Roboflow, so Roboflow-only datasets are left out here.
  Earlier in-project lists, not re-read for this study: the 2026-11-18 journal notes
  [public datasets (Claude)](../journal/2026/2026-11-18-public-datasets-claude.md) and
  [public datasets (Perplexity)](../journal/2026/2026-11-18-public-datasets-perplexity.md).
- How: eight research notes, written on 2026-11-25 and 2026-11-26 from web pages, papers, repository
  READMEs and small API metadata (Zenodo, figshare, Kaggle and Hugging Face JSON), all in
  [epic4-public-ultrasound-datasets-notes/](epic4-public-ultrasound-datasets-notes/) (Section 10 lists
  them). No dataset, archive, video or image was downloaded or opened, no account was used and no AWS
  call was made. Numbers are as the sources state them; "my sum" marks arithmetic done in the notes or
  here. The run hit the account's API spend limit twice and was finished on a token budget. This
  report was written from the notes' summaries, tables and gap sections, not from every detailed
  entry; the per-dataset fields (host, version, checksums, licence text) are in the notes.
- **Nothing is decided here.** Section 7 asks three questions, each with a default.

Terms and abbreviations used throughout:

- **Tier A to D**: how far a download can run unattended on a cloud server. A = scriptable with no
  login; B = scriptable with a token or cookie the user supplies once; C = needs a manual step by the
  user per dataset (form, approval, click-through), after which a token usually works; D = not
  automatable. These are labels of this study only.
- **Wave 1 to 3**: the download order proposed in Section 5 (wave 1 = tier A, wave 2 = tier B,
  wave 3 = tier C). Labels of this study only.
- **Release**: one version of one dataset, as its publisher published it.
- **Super-dataset**: the user's term, a training set composed at runtime by code from several chosen,
  versioned datasets.
- Licences: CC BY (Creative Commons Attribution), NC (non-commercial), SA (share-alike),
  ND (no derivatives), CC0 (public domain dedication), ODC-By (Open Data Commons Attribution).
- DUA: data use agreement. RUA: research use agreement. TCIA: The Cancer Imaging Archive.
  IDC: NCI Imaging Data Commons. HF: Hugging Face. CEUS: contrast-enhanced ultrasound.
  EUS: endoscopic ultrasound. RF: raw radio-frequency (channel) data. NAFLD: non-alcoholic fatty
  liver disease.
- AWS: S3 (object storage), EC2 (virtual machines), IAM (identity and access management),
  SSM (Systems Manager, used for shell access without open ports), NAT gateway (network address
  translation for private subnets), Object Lock (S3 write-once protection with a retention period).
- machine01: the project's trusted workstation that holds the data root.

## 0. Summary

1. **The large papers reach their scale mostly through video frames.** Ten papers or resources
   train on 100k to 5M ultrasound images drawn mostly or only from public data, for example
   SonoCorpus (456,963 images or frames, 53 datasets, 2026), OpenUS-46 (374,192 images, 46
   datasets) and OPUS (5,123,697 frames, 50 datasets). In each, a few echo, nerve and thyroid
   video sets supply 54% to 84% of the total. Counted as distinct labelled still images, the
   public pool is likely low hundreds of thousands, and the upper abdomen is about 1% to 2% of it
   (an estimate in the papers note, not a count).
2. **Census: 271 rows in five organ-group tables**, plus a master list of about 190 names from the
   papers and lists. About half the rows (about 143, my tally) look scriptable with no login
   (tier A). Section 2 gives the counts per group.
3. **For epic 1 (upper-abdomen anatomy segmentation), public organ masks are scarce.** Real images
   with upper-abdominal organ masks: about 1,300 (AUL 735 liver and mass images, Open Kidney 514,
   the Vitale set 61), plus 926 CT-simulated images. A Kaggle-only set, LUS-7Seg (10,507 images with
   liver and gallbladder masks), has no confirmed origin. Upper-abdominal images that need no signed
   agreement sum to about 48,300 before dedup (37,800 without LUS-7Seg), mostly with organ-class or
   disease labels. The one large source, RadImageNet's ultrasound part (about 259k abdominal frames
   with organ labels), is on request only.
4. **For epic 3 (spotting liver diseases)**, biopsy-graded labels are in the Saudi NAFLD set
   (10,352 images, 384 patients; signed agreement) and the Byra set (550 images, open, CC BY 4.0).
   Lesion types are in SMC-LUD (5,385 images, 2026), TCIA B-mode-and-CEUS-Liver (120 patients,
   272 GB), AUL and SYSU-FLL-CEUS (on request).
5. **Download plan in three waves** (Section 5): wave 1 takes the tier A sets, about 1.25 TB by my
   sum of stated sizes (0.77 TB without the 480 GB EchoXFlow echo set); wave 2 needs a Kaggle and a
   Hugging Face token once; wave 3 needs per-dataset applications by the user. Start from the
   SonoCorpus manifest on Zenodo (53 datasets with licences and the MD5 of every file).
6. **AWS** (Section 6): a new private bucket, written once, with versioning and Object Lock; a small
   EC2 downloader with an instance role (no key at all), no inbound ports, no NAT gateway, built by
   CloudFormation. For a long-lived credential on machine01: IAM Roles Anywhere first, a
   prefix-scoped IAM user key as the fallback; both need the user in the IAM console. One-time cost
   about $10 for 2 TB; storage $47 per month for 2 TB in S3 Standard, falling to $8 in
   Intelligent-Tiering after 90 days unread. Copying everything back to machine01 is the largest
   cost ($175 for 2 TB, $913 for 10 TB).
7. **Needs you** (Section 7): a storage rule for public ultrasound images (a new decision record),
   whether the use is commercial, and the credential type for machine01.

## 1. How the large papers reach their scale

Table 1. Papers and resources that train or benchmark ultrasound models on many images, with the
public share of their data (numbers as the papers state them; sources in the
[papers note](epic4-public-ultrasound-datasets-notes/large_scale_papers_and_lists.md), sections 1, 2
and 4).

| Paper or resource (year) | Images as stated | Datasets (n) | Public share | What it released for reuse |
|---|---|---|---|---|
| UltraSam, US-43d (2024; IJCARS 2025) | 282,321 image-mask pairs (186,894 images by the note's sum of its table) | 43 | 100% | one link per dataset, COCO converters; CC BY-NC-SA 4.0 |
| USF-MAE, OpenUS-46 (2025) | 374,192 | 46 | 100% | link table; MIT |
| OpenUS (2025) | 308,584 | 42 | 100% | link table; CC BY-NC 4.0 badge |
| SAMUS, US30K (2023) | about 30,000 images, 69,000 masks | 7 | 100% | a re-packaged copy on Google Drive with no data licence |
| UltraFedFM (npj Digit Med 2025) | 1,015,754 (782,513 public by the text) | 14 public + 2 private | 77% (text), 71% (supplement) | links, preprocessing code; Apache-2.0 |
| URFM (iScience 2025) | 1,003,465 | 6 public sources + private | 45.6% | none found |
| EchoCare, EchoCareData (2025) | over 4.5M "image-class tuples" | 138 | 100% (paper) | dataset names not found anywhere |
| UltraSAM3 (2026) | 112,634 training images | 37 | 100% | name table |
| SonoCorpus / SonoBase (2026) | 456,963 images or frames, 1,626,085 masks | 53 | 100% | Zenodo manifest: source, access, licence, split indices, MD5 of every file; dedup hashes |
| US-JEPA, OPUS (2026) | 5,123,697 frames | 50 | 100% | per-dataset table |
| UltraBench 2 (2026) | 21 tasks, at most 1,000 training examples each | 12 | 100% | `pip install ultrabench`; prepared copies of 10 sets on HF; fixed splits |

Mainly private, so useful as weights only: USFM (3M-US, sources undisclosed), UltraDINO (2M Danish
fetal images), FetalCLIP (207,943 clinical images), EchoCLIP (1,032,975 echo videos) and EchoPrime
(12,124,168 echo videos). General medical sets hold little ultrasound: SA-Med2D-20M has 2,968
ultrasound images of 4.6M, MedSAM2 used 19,232 ultrasound frames, and MedSAM's ultrasound share is
not stated.

How the counts were made (papers note, section 3):

- In US-43d, five video sets (brachial plexus, EchoNet-Dynamic, CAMUS, Stanford thyroid cine-clip,
  EchoNet-Pediatric) give 112,929 of its 186,894 images (60%, the note's sum).
- In SonoCorpus, one echo set (RVENet) gives 247,014 of 456,963 (54%); eight video or 3D sets give 84%.
- In OPUS, 79.7% of the frames come from video; EchoNet-LVH and EchoNet-Dynamic alone give 73%.
- 3D volumes are cut into slices. Phantoms and simulated images sit inside some totals (CACTUS,
  FPUS23, the Leeds lung phantom, the Vitale abdominal simulation). Augmented copies are not counted.

A fair comparison with the project's training set (about 20k labelled images, dataset version
261023): count distinct labelled still images, with the frames of one video counted once, per
anatomy. On that basis the public pool with masks is likely low hundreds of thousands, mostly heart,
nerve, thyroid, breast and fetal, and the upper abdomen is about 1% to 2% of it (estimate, papers
note section 3). Unlabelled frames for self-supervised pretraining reach millions (OPUS), but most
are highly correlated echo frames.

Reusable shortcuts, best first: the **SonoCorpus manifest**
([doi:10.5281/zenodo.22770825](https://doi.org/10.5281/zenodo.22770825); licences audited on
2026-09-14; images not re-hosted) to seed our plan and check our copies; the **UltraBench 2** loader for
its 12 datasets; the **US-43d converters** for COCO masks. None of them automates downloads behind
registration. SAMUS's US30K re-distributes CAMUS (CC BY-NC-SA) and other sets without a stated
licence, so the originals are the safer source (the papers note's judgement).

## 2. The census

Table 2. Public ultrasound datasets found by 2026-11-26, per organ group (rows as counted in each
group's note; tier A = scriptable with no login).

| Organ group (note) | Rows (n) | Tier A rows (n) | Largest or most useful open sets (licence) | Main gaps and warnings |
|---|---|---|---|---|
| Breast and thyroid ([note](epic4-public-ultrasound-datasets-notes/breast_thyroid_datasets.md)) | 54 (30 breast, 24 thyroid) | about 26 (my tally) | BUS-CoT 11,439 images (CC BY 4.0), ThyUS2Path 8,508 (CC BY 4.0), TN5000 5,000 (CC BY), BUS-BRA 1,875 (CC BY 4.0); ThyroidXL 11,635 (HF click-through) | BUSI: 155 of 780 images are duplicates; no public parathyroid, breast elastography or breast CEUS set; the gated OpenThyroidDB (61.8 GB) bundles most thyroid sets |
| Heart, lung and vessels ([note](epic4-public-ultrasound-datasets-notes/heart_lung_vessels_datasets.md)) | 51 (29 heart, 12 lung, 10 vessel) | about 26 (my tally) | EV9V 910,579 frames, 25.5 GB (CC BY 4.0); ThrombUS+ 2,919 vein videos, 12.19 GB (CC BY 4.0); EchoXFlow 480 GB (CC BY-NC-SA 4.0, beamspace data); CAMUS family (CC BY-NC-SA 4.0) | EchoNet family needs approval on Redivis (non-commercial); MIMIC-IV-ECHO (524,137 DICOM files) is credentialed; most lung "images" are frames of a few hundred videos |
| Fetal, obstetric and gynaecologic ([note](epic4-public-ultrasound-datasets-notes/fetal_obgyn_datasets.md)) | 43 | 26 | FETAL_PLANES_DB 12,400 images (CC BY 4.0); intrapartum video set 68,106 frames (CC BY 4.0); ACOUSLIC-AI about 252,000 frames, 38 GB (CC BY-NC-SA 4.0) | one Jinan University group's intrapartum sets overlap heavily; no public placenta, endometrium or adnexal set |
| Abdomen and urology ([note](epic4-public-ultrasound-datasets-notes/abdomen_urology_datasets.md)) | 37, plus 9 uploads of unknown origin | 20 (my tally) | see Table 3 | no public set for spleen alone, adrenal, transabdominal pancreas, hernia, inflammatory bowel disease, adult FAST (trauma scan), bladder or testis |
| Other anatomies and collections ([note](epic4-public-ultrasound-datasets-notes/other_anatomy_and_general_datasets.md)) | 86 (76 datasets, 7 link lists, 3 atlases) | 45 | ReMIND 43.73 GB (brain, CC BY 4.0), UltraBones100k 41.6 GB (CC BY 4.0), AHU 34.13 GB (internet videos, CC BY 4.0), knee JoCoHS 12,063 images (CC0), ROCOv2 11,429 ultrasound figures (per-image licence) | teaching atlases (POCUS Atlas, UltrasoundCases.info, Radiopaedia) do not allow bulk or ML use; raw RF collections reach 30 to 40 TB |

Footnote to Table 2: FAST = Focused Assessment with Sonography in Trauma. Some datasets appear in two
groups (for example USenhance 2023, the Chinese report sets, AbdomenUS), so the distinct count is
somewhat below 271 (not counted). The papers note's master list (about 190 names, of which about 35
abdominal or liver) is the cross-check:
[papers note, section 6](epic4-public-ultrasound-datasets-notes/large_scale_papers_and_lists.md).

Table 3. High-priority abdominal and liver datasets (for epic 1, upper-abdomen anatomy segmentation,
and epic 3, spotting liver diseases), from the abdomen and other-anatomies notes. Counts as stated by
the host; GB = download size stated by the host.

| Dataset | Content | Images (n) | GB | Host, tier | Licence | Use for epic 1 | Use for epic 3 |
|---|---|---|---|---|---|---|---|
| AUL (Annotated Ultrasound Liver) | liver, focal masses | 735 | 0.07 | Zenodo, A | CC BY 4.0 in metadata; text adds "subject to copyright" | liver and mass masks | benign, malignant, normal |
| Open Kidney Ultrasound Data Set | kidney, native and transplant | 514 patients | unknown | registration, C | CC BY-NC-SA | kidney region masks, view labels | none |
| Vitale set ("AbdomenUS") | 8 abdominal organs | 617 real (61 annotated) + 926 simulated | 2.10 | Kaggle, B | "© Original Authors" | 8-organ masks, mostly simulated | none |
| LUS-7Seg | liver and gallbladder planes | 10,507 | 1.09 | Kaggle only, B | CC BY-SA 4.0 set by the uploader | liver and gallbladder masks; origin unverified | none |
| Karim and Ball (Sci Data 2026) | 10 abdominal organ classes | 5,468 unique | 1.43 | Mississippi State repository, A | CC BY 4.0 | organ-class labels | normal or abnormal, ascites |
| UIdataGB | gallbladder diseases | 10,692 | 2.04 | Mendeley Data, A | CC BY 4.0 | organ-level classes | none |
| M2-US (2026) | 30+ targets, abdominal part 5,832 | 67,620 (all organs) | 7.90 | Zenodo, A | CC BY 4.0 | 366 organ-class images | 5,466 liver lesion images (2 classes) |
| RadImageNet, ultrasound part | liver, kidney, gallbladder, pancreas, spleen and others | about 259k abdominal frames (secondary) | unknown | on request, C | not stated | organ labels, no masks | none |
| Saudi NAFLD set | steatosis, fibrosis | 10,352, 384 patients | unknown | OSF + signed agreement, C | non-commercial agreement | none | biopsy grade and stage |
| Byra fatty liver | steatosis | 550, 55 patients | 0.05 | Zenodo, A | CC BY 4.0 | none | biopsy reference |
| SMC-LUD (2026) | hepatocellular carcinoma vs haemangioma | 5,385, 1,021 patients | 1.33 | figshare, A | CC BY 4.0; text adds "non-commercial research use only" | none | lesion type |
| B-mode-and-CEUS-Liver | liver masses, B-mode and CEUS | 120 patients, 1,859 DICOM objects | 272.16 | TCIA, A | CC BY 4.0 | none | pathology or CT/MRI reference |
| SYSU-FLL-CEUS | liver CEUS lesion clips | 353 clips | about 8 to 11 (Kaggle copy) | email request, C | none stated | none | lesion type |
| GBCU and GBUSV | gallbladder images; gallbladder videos | 1,255; 64 videos | unknown | email link + agreement, C | signed licence | gallbladder boxes (GBCU) | none |
| Regensburg paediatric appendicitis | right lower quadrant, children | 2,097 | 0.52 | Zenodo, A | CC BY-NC 4.0 | lower abdomen only | none |
| MONAI Clinical Ultrasound Image Repository | abdomen, heart, OB/GYN | 2,000 studies (about 1/3 abdominal) | unknown | AWS Open Data, A | CC BY-NC 4.0 | unlabelled | none |
| Kidney "Stone" and "No Stone" | kidney | 9,416 | 0.23 | Mendeley Data, A | CC BY 4.0 | none | none |

Footnote to Table 3: OB/GYN = obstetrics and gynaecology. Other liver sets of lower trust (BEHSOF,
the Kaggle F0-F4 fibrosis re-upload by a non-author, AD-MAGNet) and CLUST (liver tracking, access
paused) are in the [abdomen note](epic4-public-ultrasound-datasets-notes/abdomen_urology_datasets.md),
Table 1 and Gaps. Mirrors often carry a different licence from the original (for example the Kaggle
copy of the Karim and Ball set says CC BY-NC-SA 4.0), so the original host's licence is the one to
record.

What this means against the project's 20k images: the public upper-abdominal data that needs no signed
agreement is about 48,300 images before dedup (the abdomen note's sum), but almost none of it carries
organ masks. Its likely use is pretraining, view or organ classification, and liver-disease labels,
not a direct addition to the epic 1 mask training set.

## 3. Hosts: how each one is downloaded

Table 4. Download route per host, from the [hosts note](epic4-public-ultrasound-datasets-notes/hosts_access_and_terms.md)
(tier A = no login; B = token once; C = manual step per dataset, then a token; D = not automatable).

| Host | Tier | Route | Limits and pitfalls |
|---|---|---|---|
| Zenodo | A | REST API; MD5 per file | 60 requests per minute for guests; new anti-bot measures announced in January 2026 |
| figshare | A | API (`ndownloader` links); MD5 | web pages show a bot challenge; the API answers |
| Mendeley Data | A (unverified) | public API claimed | site behind Cloudflare; not tested |
| Harvard Dataverse, OSF | A | Data Access API; OSF API | Dataverse guestbook files need one extra POST |
| TCIA open, IDC | A | new TCIA Data Retriever (command line, MD5, resume) or IDC buckets in us-east-1 | IDC data can be copied inside S3 at no transfer cost |
| AWS Open Data, PhysioNet open | A | `aws s3 cp` or `sync` (server-side copy); PhysioNet also by wget | requester-pays buckets need AWS credentials |
| Hugging Face public | A | `hf` client | 3,000 file requests per 5 minutes per IP without a token |
| GitHub | A | git, releases | 60 API requests per hour without a token; Git LFS quotas of the owner |
| Academic Torrents | A | aria2c (BitTorrent) | AWS acceptable-use rules for BitTorrent not checked |
| Kaggle datasets | B | `kaggle` client with the user's token | terms bar crawling outside the API |
| Google Drive | B, often C | gdown or rclone | popular files blocked for about 24 h ("too many users") |
| Synapse, Dryad, IEEE DataPort | B | their clients with a token | Synapse needs an account even for open data; DataPort needs a subscription |
| Hugging Face gated, Kaggle competitions | C, then B | accept terms or rules once on the web page | Kaggle may ask for phone verification (unverified) |
| Grand Challenge | C, then B | join the challenge, then a token | much challenge data is also on Zenodo (tier A) |
| Stanford AIMI | C, then B | approval per dataset on Redivis, then `REDIVIS_API_TOKEN` | moved from Azure to Redivis; the old Azure links no longer apply |
| PhysioNet credentialed | C, then B | credentialing per person (training, 1 to 2 weeks; delays announced in June 2026), DUA per project | see Section 4 |
| TCIA restricted | C | dbGaP data access request per project, renewed yearly | the cloud provider must be named in the request |
| OneDrive, SharePoint | C | no anonymous API for business accounts | — |
| Baidu Netdisk, "on request by email" | D | — | Baidu needs an account and is throttled; email gives a link whose host then sets the tier |

Three points matter for the plan:

- No host documents a block on AWS addresses, but nothing was tested from EC2. One small test per
  host should run before any large download.
- Only data already in S3 (AWS Open Data, IDC, PhysioNet's open bucket) can be copied server-side.
  Everything else streams through the instance; `rclone copyurl` streams without a local temporary
  file.
- Tokens go in a header or an environment variable, never in a URL. On the instance they would come
  from Secrets Manager, filled by the user (this needs a boundary change; Section 6).

## 4. Terms that matter

This is the hosts note's reading, not legal advice
([hosts note, section 5](epic4-public-ultrasound-datasets-notes/hosts_access_and_terms.md)):

- **Stanford AIMI RUA** (the EchoNet family, the thyroid cine-clip set and others): personal,
  non-commercial research only; no redistribution; each person registers. Commercial use needs a paid
  licence ($70,000 per dataset per year in fiscal year 2025).
- **PhysioNet credentialed DUA** (MIMIC-IV-ECHO): "scientific research and no other"; no shared
  access. PhysioNet states that sending credentialed data through third-party APIs breaks the
  agreement. In this project, a table read by an agent session reaches Anthropic's API
  ([DEC-052](../decisions/DEC-052-privacy-covers-images-tables-readable-after-asking.md), images
  are patient data and tables are readable after asking), so agent sessions must never read
  credentialed PhysioNet text or tables.
- **NIH data use certification** (restricted TCIA data): name the cloud provider in the request;
  destroy all copies, cloud included, at project close.
- **TCIA open collections**: mostly CC BY, so commercial use is allowed.
- **Per-person agreements** (Stanford AIMI, PhysioNet, NIH, RVENet, Grand Challenge logins): a
  shared team bucket fits them only if every person who can read a prefix holds their own approval.
- **Licence conflicts**: several records carry CC BY 4.0 in metadata and non-commercial text in the
  description (AUL, SMC-LUD); mirrors often change the licence. Record the original host's wording.
- **Non-commercial terms are common** among the largest open sets: the CAMUS family, EchoXFlow,
  ACOUSLIC-AI, OpenPOCUS, U2-Bench and TUS-REC are all NC. No licence seen restricts the cloud region.

## 5. Proposed download plan

Rules for every dataset (proposed, after the pattern of
[DEC-096](../decisions/DEC-096-epic2-retrieval-path-official-routes-terms-reading-fetch-budget.md),
the epic 2 Roboflow retrieval rules: official routes only, the user's own reading of the terms, a
fetch budget):

1. **Official routes only.** Use each host's documented API or client (Table 4), never scraped web
   pages, and stay under its rate limits.
2. **One release, one record.** For each release, record the source URL, DOI or version, the
   licence as written at the original host, the retrieval time, the HTTP headers (ETag,
   Last-Modified, length) and the publisher's checksum.
3. **Bytes as published.** Store the archives unchanged; compute sha256 while downloading; compare
   with the publisher's MD5 where there is one; write a "complete" marker last.
4. **Original before mirror.** Take a Kaggle or HF mirror only when the original is unreachable,
   and record both.
5. **The user reads the terms** of each tier B and tier C dataset, and that reading is recorded,
   as rule 9 of DEC-096 did for Roboflow.

Table 5. The three download waves (tier letters as in the terms list: A no login, B token once,
C manual step per dataset). Sizes are the hosts' stated sizes; my sums leave out sets of unknown size.

| Wave | What it takes | Main datasets | Size | Who acts |
|---|---|---|---|---|
| 1 (tier A) | open sets whose licence allows a private research copy | abdomen: TCIA B-mode-and-CEUS-Liver (272 GB), Prostate-MRI-US-Biopsy (80 GB), M2-US, UIdataGB, Karim and Ball, SMC-LUD, AUL, Byra, LEPset, kidney stone, Regensburg, prostate sets (about 371 GB); breast and thyroid: BUS-CoT, BCMID, ThyUS2Path, TN5000, BUS-BRA, BrEaST, free-hand thyroid sweeps, Mendeley sets, TN3K (about 26 GB); heart, lung, vessels: CREATIS family (CAMUS, TED, CETUS and simulations), EV9V, CACTUS, ThrombUS+, OpenPOCUS, carotid and lung Mendeley sets, and the optional EchoXFlow (about 575 GB, 480 of it EchoXFlow); fetal and gynaecologic: FETAL_PLANES_DB, HC18, PSFHS, JNU-IFM, IUGC 2025, the intrapartum video set, DELTA, ACOUSLIC-AI, PFUS1 and others (about 66 GB); other: ReMIND, UltraBones100k, TUS-REC2024, AHU, U2-Bench, BITE, RESECT, ERDES, Oculo and others (about 208 GB) | about 1,246 GB (my sum); about 766 GB without EchoXFlow | the aws agent and the downloader, after the user's go-ahead |
| 2 (tier B) | sets behind a token the user supplies once | Vitale AbdomenUS, LUS-7Seg (after an origin check), BUSI (Kaggle mirror, with the published duplicate list), DDTI, AUITD, ThyroidXL (HF click-through), CardiacUDA, EchoCP, CardiacNet, smaller Kaggle sets | under 50 GB (estimate from the stated sizes) | the user: Kaggle and HF tokens into Secrets Manager, HF click-throughs |
| 3 (tier C) | sets behind an application or agreement | RadImageNet (abdomen, high priority), Saudi NAFLD (liver, high priority), Open Kidney (high priority), GBCU, GBUSV, SYSU-FLL-CEUS; Stanford AIMI on Redivis (EchoNet-Dynamic, -Pediatric, -LVH, TEE view, thyroid cine-clip, MRI-US prostate, CT2Echo); OpenThyroidDB; challenge sets (TN-SCUI 2020, TDSC-ABUS 2023, USenhance 2023, FUGC 2025, IUGC 2024, CuRIOUS, UUSIC 2025 and UUSIVC 2026); RVENet, HMC-QU, TMED-2, BEDLUS, MVSeg2023, Regional-US, UDIAT, ALN-Ultra, CUBDL, the Kaggle nerve competition | unknown (most hosts do not state sizes) | the user, and each team member for per-person agreements |

Not planned: tier D and barred sets (teaching atlases, the Butterfly GrandHack set, CLUST while its
access is paused, A-AFMA, UBPD, unreleased sets such as FLA-Net or ReMUD, Baidu-only sets); the
TB-scale raw RF archives (Open-H-RF about 40 TB, ULMShare about 30 TB); SA-Med2D-20M (352.8 GB for
2,968 ultrasound images, so the originals are taken instead); the PhysioNet CVES Doppler signals
(173.9 GB, not images); MIMIC-IV-ECHO until the rule in Section 4 (no agent session reads credentialed
data) has a decision behind it. Smaller RF and channel-data sets (about 206 GB: PALA, USTB, phantom
archives) are optional; they serve beamforming work, not B-mode training.

Speed. The downloader's own limit is high: instances under 32 vCPUs get up to 5 Gbps to the
internet. The publishers set the real rate. At an assumed 50 to 400 MB/s overall, 2 TB takes 1.5 to
12 h ([AWS note, section 8](epic4-public-ultrasound-datasets-notes/aws_s3_ec2_design.md); the rates
are assumptions, not measurements). Staging on a gp3 disk would cap a c6in.large at about 98 MB/s
(assumed), so stage on local NVMe (m6idn.large) or stream large files straight to S3.

## 6. AWS design

All of this section comes from the [AWS note](epic4-public-ultrasound-datasets-notes/aws_s3_ec2_design.md),
which read the project's AWS files and AWS documentation and made no AWS call.

### 6.1 Bucket and key layout

A **new bucket** (example name `claude-agent-sonoai-public`; the name is part of the decision in
Section 7) fits better than a prefix in the scrape bucket of
[DEC-082](../decisions/DEC-082-scraped-universe-images-plain-in-a-private-s3-bucket.md) (scraped
Roboflow Universe images stored plain in a private bucket), for three reasons:

- Everything in it is written once, so Object Lock can cover the whole bucket by default. In the
  scrape bucket it would also lock the scraper's working files.
- DEC-082 stays as it is, and scraper code never touches the archive.
- The bucket policy lists only the downloader role, the readers and `claude-agent`.

The name needs no IAM change (the agent's policy allows `claude-agent-*` buckets). The
[TASK-201](../../backlog/tasks/task-201%20-%20Private-S3-bucket-for-scraped-Universe-images-by-CloudFormation-all-Block-Public-Access-settings-server-side-encryption-TLS-only-policy-access-for-claude-agent-only-DEC-082.md)
draft template (the epic 2 scrape bucket, in progress) can be copied, with versioning and Object
Lock added.

**Proposed key layout (from the AWS note, section 2; nothing exists yet): look at which prefixes hold
raw bytes and which hold small indexes.**

```text
raw/<source>/<release>/files/<safe key>     bytes exactly as downloaded, written once
raw/<source>/<release>/_meta/source.json    URLs, DOI, licence, retrieval time, headers, publisher checksums
raw/<source>/<release>/_meta/SHA256SUMS     sha256 of every file
raw/<source>/<release>/_meta/COMPLETE       written last
manifests/<source>/<release>/members-v<k>.parquet   one row per archive member, with sha256
fingerprints/<source>/<release>/<method>-v<k>.parquet   perceptual hashes of the public images
curated/<name>/<version>/dataset.yaml and manifest.parquet   a versioned dataset as references, not copies
catalog/sources.jsonl, catalog/curated.jsonl   small indexes
```

How stage 2 uses it: the instance computes fingerprints of the public images only; machine01 downloads
the fingerprint and manifest files (megabytes), compares them with the project's own fingerprints
locally, and keeps the match list on machine01, as rule 4 of DEC-082 (keep scraped data apart from
project data) requires for Roboflow data. A curated version is a manifest of references, so it stays
reproducible. A super-dataset is a short YAML file of (curated name, version) pairs that code
resolves at runtime. When a public dataset enters a project dataset version, it becomes a new
datasource (one origin of images, with its own `datasource_id`) and from then on is project data
under every rule.

Publisher file names need turning into safe keys: the agent's policy refuses any key that contains
`_plain` or `_submit1`. The original name is kept in the metadata.

### 6.2 Protection as a backup

- **Versioning plus Object Lock in governance mode**, with a default retention for the whole bucket
  (365 days is the note's example).
- **Deny permanent deletes and lock bypass** in the bucket policy for everyone except the account
  root, and add the same denies to the agent's own policy, because its `s3:*` rights could otherwise
  undo every protection.
- **Not used**: compliance mode (a licence takedown could not be honoured) and MFA delete (root only,
  and not usable with lifecycle rules).
- **As in the project's other buckets**: SSE-S3 encryption, all four Block Public Access settings,
  a TLS-only policy. Server access logs go to a separate log bucket (free apart from storage).

### 6.3 Cost

Table 6. Estimated cost in us-east-1, USD (AWS note, sections 4 and 8; 1 TB = 1,024 GB; storage
prices partly from secondary sources, see Section 9).

| Item | Wave 1, 1,246 GB (my arithmetic at the note's rates) | 2 TB | 10 TB |
|---|---|---|---|
| One-time download on c6in.large On-Demand (Spot) | under 10 | 10.12 (6.12) | 26.32 (18.31) |
| Storage per month, S3 Standard ($0.023 per GB) | 28.66 | 47.10 | 235.52 |
| Storage per month, Intelligent-Tiering after 90 days unread ($0.004 per GB) | 4.98 | 8.19 | 40.96 |
| Copy everything to machine01 once ($0.090 per GB after 100 GB free per month) | 103.14 | 175.32 | 912.60 |
| The same transfer through a NAT gateway by mistake (per-GB part only) | 56.07 | 92.16 | 460.80 |

Ways to keep the copy-back cost down, cheapest first: pull only fingerprints, manifests and the chosen
members to machine01; download what machine01 needs straight from the publishers (as machine01 does
today with aria2c) and keep S3 as the backup; use the 100 GB free per month. CloudFront's Pro
flat-rate plan (about $15 per month, price unverified) would cut a full copy to about $15, but it puts
an internet-facing host name in front of the bucket and needs its own decision.

### 6.4 The EC2 downloader

- **Instance**: c6in.large ($0.1134 per hour On-Demand, about $0.030 Spot), or m6idn.large for local
  NVMe staging. Default VPC, public subnet, public IPv4 address ($0.005 per hour), **no NAT gateway**
  (the agent cannot create one anyway). No inbound ports; access through SSM only. Built by a
  CloudFormation template under `deploy/aws/`, deployed by the aws agent
  ([DEC-026](../decisions/DEC-026-cloud-agent-runs-cloud-services.md), AWS work goes to the aws
  agent) after the user's go-ahead.
- **Job**: driven by the plan file of Section 8, safe to rerun: `aria2c -c` resumes, each release is
  skipped once its "complete" marker exists, uploads never overwrite, and job state sits in DynamoDB.
- **Integrity**: three checks: the publisher's checksum, the sha256 computed while downloading, and
  S3's default CRC64NVME check on upload.
- **Tools**: aria2c for HTTP lists and torrents, rclone for cloud drives and streaming, the hosts'
  own clients where a login is involved (Table 4), and `aws s3 cp` or s5cmd for uploads with large
  parts (64 MiB parts cost $0.82 in requests for 10 TB, against $6.55 with 8 MiB parts).

### 6.5 Long-lived access to one bucket or prefix

Table 7. Ways to give scoped access, from the AWS note, section 6 (its Table 7).

| Way | Secret and lifetime | Scope to one prefix | Allowed by today's agent policy | Who acts |
|---|---|---|---|---|
| EC2 instance role (for the downloader) | no key at all; rotated role credentials | yes | yes | the aws agent builds it; the user gives the go-ahead |
| IAM Roles Anywhere (for machine01) | a certificate whose private key never leaves machine01; sessions 15 min to 12 h | yes | the role yes; the trust anchor and profile no | the user (certificate authority, trust anchor, profile); the agent (role) |
| IAM user access key (fallback for machine01) | a key valid until deleted | yes, plus a source-IP condition | no (the agent cannot create users or keys) | the user in the IAM console |
| S3 Access Points or Access Grants | needs another credential | yes | no | the user |
| Presigned URLs or POST policies | a bearer URL, at most the signing session (7 days only with user keys) | one object or key pattern | yes | the agent signs |
| AssumeRole from `aws login` | 1 h sessions while the login lasts (12 h) | yes | needs a new statement | the user adds it |

For "a long-lasting key to a specific bucket or folder", the note's recommendation is: the instance
role on EC2, and **IAM Roles Anywhere** on machine01. The IAM user key is acceptable only with all of
these: one prefix, read-only or write-only, an explicit deny of deletes, a source-IP condition when
machine01's public address is fixed, storage outside the repo and outside `.env`, rotation on a
schedule (for example 90 days) and alerts on use. Claude never sees the secret in either case.
Example policy JSON for each option is in the AWS note, section 6.

### 6.6 Changes the design needs, and corrections to the brief

Table 8. Changes to the project's IAM setup ([claude-agent-deploy.json](../../deploy/aws/claude-agent-deploy.json)
and the boundary), all made by the user in the IAM console (AWS note, section 7).

| Change | Why |
|---|---|
| Add the tag value `sonoai-download` to the two SSM statements | today SSM sessions and Run Command reach only the Label Studio server |
| Create the Spot service-linked role once | Spot requests need it |
| Add Secrets Manager read on `claude-agent-*` secrets to the boundary | only if a publisher needs a token on the instance |
| Add a deny statement protecting the archive bucket from the agent | the agent's `s3:*` could remove the protections |
| Roles Anywhere resources, or an IAM user and key | the agent has no rights for them |

The AWS note also corrected four facts in the brief: `aws login` credentials last 15 minutes each and
are refreshed for up to 12 h (the "90 days" in [deploy/aws/README.md](../../deploy/aws/README.md) was
not confirmed); the agent's EC2 rights apply to every instance, and only SSM access is limited to the
Label Studio server; that server has port 443 open, so "no inbound ports" is a new, stricter rule;
and [DEC-063](../decisions/DEC-063-public-non-patient-datasets-root.md) (the public non-patient
datasets root) itself asks for a new decision before public ultrasound images are stored.

## 7. Decisions for the user

Each question has a default that the user can accept with "ok".

1. **Storage rule for public ultrasound datasets.** May public ultrasound datasets be stored plain
   (not encrypted) in a new private S3 bucket and on the downloader instance, kept apart from project
   data, under a new decision record modelled on DEC-082 (scraped Roboflow Universe images stored
   plain in a private bucket)?
   - Default: yes. A new bucket (name to choose; `claude-agent-sonoai-public` is the example), written
     once, Object Lock in governance mode for 365 days. The record also amends the last bullet of
     DEC-063 (public non-patient datasets root), which keeps such images out until a decision exists.
   - Why: (1) DEC-063 requires a decision before storing public images that may carry patient text;
     (2) the images are already public, and DEC-082 set the same pattern for Roboflow images; (3) a
     separate bucket keeps the archive away from scraper code and allows bucket-wide Object Lock.
   - Best alternative: store them encrypted (enc1, the project's encrypted store format). It wins if
     public ultrasound images should count as patient data in every place, as the project's own images
     do under DEC-052 (images are patient data).
   - Cost to reverse: moderate. Re-encrypting or moving 1 to 2 TB is cheap in compute but adds a
     pipeline step, and locked versions stay until their retention ends (the root user can bypass
     governance mode).
2. **Commercial or non-commercial use.** Is the use of these datasets commercial, now or later?
   - Default: treat it as non-commercial research now, and record each release's licence so that a
     commercial-safe subset (CC BY, CC0, ODC-By) can be filtered later.
   - Why: (1) many of the largest open sets are NC, SA or ND (Section 4); (2) Stanford AIMI data needs
     a paid licence for commercial use; (3) recording licences now costs nothing.
   - Best alternative: take only commercial-safe licences from the start. It wins if a product or a
     paid service is planned within this epic.
   - Cost to reverse: low while only data is stored; high once models trained on NC data must be
     retrained.
3. **Long-lived credential for machine01.** Which credential should machine01 use for the bucket?
   - Default: IAM Roles Anywhere (a certificate on machine01, sessions of 1 to 12 h, revocable), and an
     EC2 instance role for the downloader (no key).
   - Why: (1) no secret key leaves machine01 or reaches Claude; (2) sessions are short and the
     certificate can be revoked; (3) AWS recommends it over access keys for workloads outside AWS.
   - Best alternative: an IAM user access key scoped to one prefix, with deletes denied, a source-IP
     condition and rotation every 90 days. It wins if the simplest setup matters most and machine01
     has a fixed public address.
   - Cost to reverse: low (switch the credential, delete the user or the trust anchor). Both options
     need the user in the IAM console.

Smaller choices, with defaults: Object Lock retention 365 days in governance mode; no CloudFront for
now; MIMIC-IV-ECHO and other credentialed PhysioNet data stay out until a rule keeps agent sessions
from reading them; only people with their own approval read the prefixes of per-person agreements; the
TB-scale raw RF archives are not downloaded.

## 8. Proposed next steps

For a `/consult` session; these are not board tasks yet.

1. **Records**: the epic 4 mission now exists ([DEC-117](../decisions/DEC-117-epic4-mission-public-ultrasound-datasets.md),
   accepted on 2026-11-26). Still needed: the storage decision of question 1 in Section 7, and
   retrieval rules for epic 4 modelled on DEC-096 (the epic 2 retrieval rules: official routes, terms
   reading, fetch budget).
2. **Download plan file**: one machine-readable row per release (dataset, source URL, host, tier,
   tool, stated size, checksum source, licence as written, wave), seeded from the SonoCorpus manifest
   and the five census tables of the notes.
3. **Bucket stack** by the aws agent: CloudFormation, copied from the TASK-201 draft (the epic 2
   scrape bucket template), with versioning and Object Lock.
4. **Downloader stack and job code**: instance role, SSM tag change by the user, the resumable job of
   Section 6.4.
5. **Host tests** from the instance: one small file per host, before any large run.
6. **Wave 1 run**, then a checklist of the user's steps for waves 2 and 3 (tokens, applications,
   per-person agreements).

## 9. Gaps and limits

- **Not tested from EC2**: no download speed was measured and no host was tried from an AWS address.
- **Conflicting counts** left open: DDTI appears with five counts (134 to 637), GIST514-DB with 514 and
  43,656, UltraFedFM's text against its supplement, USenhance 2023 with 3,000 and 2,464 images.
- **Not searched or not read**: Science Data Bank, IEEE DataPort and a full Kaggle search; the dataset
  lists of MedSAM and BiomedParse; SAMUS's supplement; EchoCare's 138 dataset names; PanEcho; the live
  terms of Mendeley Data, Harvard Dataverse and figshare; AWS's acceptable-use rules for BitTorrent;
  the agreement texts of GBCU, GBUSV and the Saudi NAFLD set.
- **Unverified prices**: S3 Standard ($0.023 per GB-month, secondary sources), the CloudFront Pro plan
  (about $15 per month), the NAT gateway per-GB rate (third-party source), Roles Anywhere pricing.
- **Unverified datasets**: LUS-7Seg's origin; the CAMUS licence (seen only on a mirror); several
  Mendeley and Google Drive sets marked "A (likely)" in the notes.
- **This report** relies on the notes' summaries and tables; the per-dataset entries were not re-read
  one by one, and two of the eight researchers stopped before their last checks (their notes say what
  remained).

## 10. Sources

The eight research notes, in [epic4-public-ultrasound-datasets-notes/](epic4-public-ultrasound-datasets-notes/):

| Note | What it covers |
|---|---|
| [large_scale_papers_and_lists.md](epic4-public-ultrasound-datasets-notes/large_scale_papers_and_lists.md) | the large papers, how they count images, released tooling, surveys and lists, a master list of about 190 names |
| [breast_thyroid_datasets.md](epic4-public-ultrasound-datasets-notes/breast_thyroid_datasets.md) | 54 breast and thyroid entries with the 14 fields, duplicates, largest and open sets |
| [heart_lung_vessels_datasets.md](epic4-public-ultrasound-datasets-notes/heart_lung_vessels_datasets.md) | 51 heart, lung and vessel entries |
| [fetal_obgyn_datasets.md](epic4-public-ultrasound-datasets-notes/fetal_obgyn_datasets.md) | 43 fetal, obstetric and gynaecologic entries |
| [abdomen_urology_datasets.md](epic4-public-ultrasound-datasets-notes/abdomen_urology_datasets.md) | 37 abdominal and urological entries, with closeness to epics 1 and 3 and an overlap map |
| [other_anatomy_and_general_datasets.md](epic4-public-ultrasound-datasets-notes/other_anatomy_and_general_datasets.md) | 86 rows: other anatomies, collections, figure-mined sets, atlases, RF data |
| [hosts_access_and_terms.md](epic4-public-ultrasound-datasets-notes/hosts_access_and_terms.md) | per-host download routes, limits, agreement clauses, tools, tiers |
| [aws_s3_ec2_design.md](epic4-public-ultrasound-datasets-notes/aws_s3_ec2_design.md) | bucket, protection, costs, downloader, credentials, IAM changes, with example policies |

Key primary sources (verified in the notes on 2026-11-25 or 2026-11-26): SonoCorpus,
[arXiv 2609.19230](https://arxiv.org/abs/2609.19230) and its manifest
[doi:10.5281/zenodo.22770825](https://doi.org/10.5281/zenodo.22770825); UltraSam US-43d,
[arXiv 2411.16222](https://arxiv.org/abs/2411.16222); OpenUS, [arXiv 2511.11510](https://arxiv.org/abs/2511.11510);
USF-MAE OpenUS-46, [arXiv 2510.22990](https://arxiv.org/abs/2510.22990); US-JEPA OPUS,
[arXiv 2602.19322](https://arxiv.org/abs/2602.19322); UltraFedFM, [arXiv 2411.16380](https://arxiv.org/abs/2411.16380);
UltraBench 2, [arXiv 2609.28610](https://arxiv.org/abs/2609.28610); the catalogue of 72 public
ultrasound datasets by Alsharid et al., npj Digital Medicine 2025,
[doi:10.1038/s41746-025-02162-4](https://doi.org/10.1038/s41746-025-02162-4); AWS prices from the
[AWS Price List for S3 in us-east-1](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonS3/current/us-east-1/index.csv)
and the [EC2 network bandwidth guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-network-bandwidth.html).
Every dataset row in the notes carries its own source link.

## 11. Details from the notes that the sections above leave out

Added on 2026-11-26 at the user's request ("record those you missed"). Each row names the note that
holds the evidence; the links and sources are there.

Table 9. Findings in the research notes, or facts from the session, that Sections 0 to 10 do not carry.

| # | Detail | Why it matters | Where |
|---|---|---|---|
| 1 | A curated GitHub atlas, [TIanCat/open-medical-ultrasound-datasets](https://github.com/TIanCat/open-medical-ultrasound-datasets), was used by two researchers; the papers note found no such list | the largest community list to cross-check in round 2 (Section 12) | fetal, abdomen notes |
| 2 | SonoCorpus's repository ([AlfredQin/sonobase](https://github.com/AlfredQin/sonobase)) publishes dedup hashes and split indices; the method is in its docs/DATA_SPLITS.md (not read) | can be reused for the stage 2 dedup | other-anatomies note, section 4 |
| 3 | Other indexes not read in full: Project Imaging-X's datasets.json (1,152 entries, only 6 breast or thyroid ultrasound entries), UMUD (an index of 14 musculoskeletal datasets, 76,124 images), the SHTI 2025 review of 14 public fetal databases, the two 2026-11-18 journal notes | possible missed datasets | breast, other-anatomies, fetal notes |
| 4 | MICCAI 2025 FLARE ultrasound subset on HF (4.92 GB, CC BY-NC 4.0: fetal abdomen, breast, carotid, thyroid, fetal head, heart; no adult abdomen) | a wave 1 candidate missing from Table 5 | abdomen note, "seen, other groups" |
| 5 | UUSIC 2025 and UUSIVC 2026 challenges, built from public sets (Fatty-Liver, KidneyUS, the appendicitis set and others) plus private data; registration on Codabench | wave 3 candidate with liver and kidney content | other-anatomies note, Table 4 |
| 6 | Mendeley Data's site footer reserves rights "for text and data mining, AI training", while many of its records say CC BY 4.0 | a legal check before bulk use of Mendeley sets | other-anatomies note, section 1 |
| 7 | BUSI: 155 of 780 images are duplicates; a mapping CSV is on Mendeley ([doi:10.17632/k8t3gnx9h6.1](https://doi.org/10.17632/k8t3gnx9h6.1)); about 32.5% of random-split test images have a duplicate or same-subject image in training (unverified); cleaned subsets and a cleaning tool (BUSClean) exist | dedup and split rules for breast data | breast note |
| 8 | Burned-in marks: handwritten diameter marks in DDTI and TN3K; crosshair markers in about 40% of TN5000 images; scanner text in the Karim and Ball set; heavy on-image annotations in LEPset | DEC-063 (public non-patient root) worries about patient text on images; marks also bias training | breast, abdomen, papers notes |
| 9 | Duplicates inside sets: Karim and Ball has 13,088 files for 5,468 unique images; SMC-LUD has patients in both its "clean" and "caliper" groups; Byra has 10 frames per patient; TN5000 is split by image, not by patient | split by patient or group, dedup before splitting | abdomen, breast notes |
| 10 | Aggregator lists hold errors: OpenUS's "Cactus" link points to an unrelated repository (the cardiac CACTUS is on FRDR and Academic Torrents); some anatomy labels are wrong (105US as pancreas in OPUS, ASUS as abdomen and CCAUI as echo in OpenUS) | check every link and label at the original source | heart note, Q2; papers note, section 6 |
| 11 | LUS-7Seg's uploader re-hosts other people's data; no paper or original host was found | do not use LUS-7Seg until its origin is known | abdomen note |
| 12 | Copies not to use: third-party copies of EchoNet data (on HF and Academic Torrents) break the Stanford RUA; HMC-QU left Kaggle and is now by email (SAMUS points to a Baidu AI Studio copy) | take only the official routes | heart note, Q2 |
| 13 | EchoXFlow is beamspace data: frames need scan conversion before B-mode models can use them | its 480 GB has a processing cost | heart note |
| 14 | How long manual steps wait: instant (HF automatic gates, Kaggle rules), days (HF manual gates, Stanford AIMI, Synapse), weeks or more (PhysioNet credentialing, dbGaP) | plan wave 3 early | hosts note, section 7 |
| 15 | Licences of model weights, if pretrained models are reused: USFM, FetalCLIP and DeblurringMIM CC BY-NC 4.0; MedSAM, SAM-Med2D, BiomedParse and UltraDINO Apache-2.0; UltraSam CC BY-NC-SA 4.0 | pretrained weights for epics 1 and 3 carry their own terms | papers note, section 4 |
| 16 | UltraBench 2 left out BUSI (data quality), LEPset (on-image annotations), Butterfly, POCUS and the Kaggle nerve set (licensing) and the Stanford thyroid set (size) | a second opinion on which sets to trust | papers note, section 2 |
| 17 | Security findings about today's AWS setup, not only epic 4: the agent's EC2 rights cover every instance, and the SSM tag guard is weak because `ec2:CreateTags` is allowed on every resource | worth a Triage task | AWS note, section 1 |
| 18 | AWS state not checked live: whether the scrape bucket exists, whether the default VPC has an S3 gateway endpoint or IPv6, and the account-level Block Public Access; the downloader must live in the default VPC (the agent cannot create a VPC or an endpoint) | first read-only checks for the aws agent | AWS note, section 1 |
| 19 | TCIA: a new Data Retriever (command line, MD5, resume) replaces the old NBIA tool; IDC buckets need no AWS account; restricted collections moved to dbGaP after an NIH change in April 2025 | the route for the TCIA sets in wave 1 | hosts note |
| 20 | Zenodo announced anti-bot measures in January 2026; figshare web pages show a bot challenge while its API works; Grand Challenge, Radiopaedia and some PMC pages refused automated fetches | use the APIs, test each host first | hosts, other-anatomies notes |
| 21 | Five of the eight researchers stopped on the 5-hour usage limit right after writing their notes, so their last self-checks may be missing (the heart note was adding acronym definitions and a wording fix) | read those notes with care | this session |
| 22 | OpenThyroidDB holds parts of unknown origin (AHU, KMVE, PKTN, TGVideo); whether its "AHU" is the AHU database of the other-anatomies note is unknown | a dedup risk inside the thyroid data | breast note |

## 12. Further research rounds

Each round is best started in a new session, which costs far less than continuing a long one; this
study, its notes and the [epic 4 relay note](../journal/2026/2026-11-26-epic4-relay-claude.md) hold
what such a session needs. Run each round inline or with at most two agents, each with a stated budget.

1. **Round 2: close the gaps that block the plan.**
   - Draft the plan file: merge the five census tables and the SonoCorpus manifest into one list of
     releases; resolve rows that sit in two groups and the aliases (for example UDIAT = BUS Dataset B,
     BLUES = COVID-BLUES, MASLD = the Byra set).
   - Check the high-priority abdomen and liver items at their source: LUS-7Seg's origin, RadImageNet's
     access terms, the agreements of the Saudi NAFLD set, GBCU, GBUSV and Open Kidney, SYSU-FLL-CEUS,
     the Concordia liver elastography set, M2-US's liver part against SMC-LUD, the size of the MONAI
     repository, the FLARE and UUSIC sets (Table 9, rows 4 and 5).
   - Search what was skipped: Science Data Bank, IEEE DataPort, a full Kaggle search through its API,
     Baidu AI Studio, Synapse; read the indexes of Table 9, rows 1 to 3; SAMUS's supplement; the
     dataset lists of MedSAM and BiomedParse; EchoCare's 138 names.
   - Read terms: Mendeley Data (Table 9, row 6), figshare, Harvard Dataverse, OSF, Dryad, the Kaggle
     nerve competition rules, CAMUS at CREATIS, AWS acceptable use for BitTorrent.
   - AWS: confirm the unverified prices of Section 9 and read the example policies of the AWS note;
     live read-only checks (Table 9, row 18) go to the aws agent, only with the user's ok.
2. **Round 3: prepare stage 2.** The dedup method (SonoCorpus's hashes; the epic 2 fingerprints of
   rule 4 of DEC-096, the epic 2 retrieval rules, so that both epics compare images alike); the
   manifest and super-dataset schema; how a public release becomes a datasource; mapping public labels
   to the project's label set; which public sets help epics 1 and 3 (pretraining, view classification
   or fine-tuning).
3. **Round 4: the later focuses of DEC-117** (anatomical and pathological diagnosis across organs). A
   census by disease and organ, for example breast BI-RADS, thyroid TI-RADS, liver, kidney,
   gallbladder, appendix, lung and heart, with the reference standard behind each label (biopsy,
   pathology, follow-up imaging or clinical).
