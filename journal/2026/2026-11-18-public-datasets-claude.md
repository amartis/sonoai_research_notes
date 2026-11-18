# 2026-11-18

## Done

- Listed public sources of ultrasound images: 11 hubs (Table 1), 21 named B-mode image
  datasets (Table 2), 3 raw-signal datasets (Table 3) and 1 compiled list. Every URL was
  checked on the web on 2026-11-18; the "Check" column says how.

## Observations

### Public ultrasound data sources

This is a general list. It is not tied to any project dataset or task. Counts are as the
source states them. Read each licence at the source before you download or use the data.

**Table 1. Hubs that host many public ultrasound datasets.**

| Hub | URL | What is there | Access | Check |
|---|---|---|---|---|
| Grand Challenge | [grand-challenge.org/challenges](https://grand-challenge.org/challenges/) | Labelled challenge datasets (e.g. HC18) | Free account; rules per challenge | Not opened (HTTP 403 to automated fetch) |
| Zenodo | [zenodo.org search: ultrasound datasets](https://zenodo.org/search?q=ultrasound&f=resource_type%3Adataset) | Datasets published with papers, each with a DOI | Mostly open; licence per record | Opened |
| Hugging Face Datasets | [huggingface.co/datasets?search=ultrasound](https://huggingface.co/datasets?search=ultrasound) | Mirrors and new sets; 71 results for "ultrasound" | Open or gated | Opened |
| TCIA (The Cancer Imaging Archive) | [cancerimagingarchive.net](https://www.cancerimagingarchive.net) | Curated cancer collections, some ultrasound (breast, liver) | Open; licence per collection | Opened (two collection pages) |
| Stanford AIMI shared datasets | [aimi.stanford.edu/shared-datasets](https://aimi.stanford.edu/shared-datasets) | Heart (echo) and thyroid video sets | Registration; non-commercial research use | Search |
| IEEE DataPort | [ieee-dataport.org](https://ieee-dataport.org) | Challenge and paper datasets (e.g. CUBDL) | Account; some need a signed agreement | Search |
| Academic Torrents | [academictorrents.com](https://academictorrents.com) | Mirrors of BUSI, CAMUS and AUL | Open (torrent) | Search |
| Kaggle | [kaggle.com/datasets?search=ultrasound](https://www.kaggle.com/datasets?search=ultrasound) | Many uploads, often copies of other datasets | Free account; check the original licence | Not opened (fetch blocked) |
| Roboflow Universe | [universe.roboflow.com/search?q=ultrasound](https://universe.roboflow.com/search?q=ultrasound) | Small user-labelled sets, mostly boxes | Free account; origin of images often unclear | Not opened (HTTP 403 to automated fetch) |
| Mendeley Data | [data.mendeley.com](https://data.mendeley.com) | Small datasets from papers | Open; licence per record | Not opened (DNS failure in fetch) |
| figshare | [figshare.com](https://figshare.com) | Small datasets from papers | Open; licence per record | Not opened |

AIMI: Stanford Center for Artificial Intelligence in Medicine and Imaging. DOI: digital
object identifier. Check: *Opened* = page fetched and read on 2026-11-18; *Search* = URL
and facts seen in web-search results only; *Not opened* = URL not fetched (reason given).

**Table 2. Named public B-mode ultrasound image datasets, by organ. n as stated by the source.**

| Organ | Dataset | Content | Licence and access | URL | Reference | Check |
|---|---|---|---|---|---|---|
| Breast | BUSI (Breast Ultrasound Images) | Normal, benign, malignant; lesion masks; about 780 images (count not rechecked). A 2023 letter reported 155 duplicate images (19%) and many axilla images | Not checked | Paper names a Cairo University page (now behind a CAPTCHA); mirror: [Academic Torrents](https://academictorrents.com/details/d0b7b7ae40610bbeaea385aeb51658f527c86a16) | [10.1016/j.dib.2019.104863](https://doi.org/10.1016/j.dib.2019.104863); letter: [PMC10293973](https://pmc.ncbi.nlm.nih.gov/articles/PMC10293973/) | Search |
| Breast | BUS-BRA | 1,064 patients; biopsy-proven tumours; BI-RADS 2, 3, 4, 5 | Copyright: Biomedical Engineering Program, Federal University of Rio de Janeiro; open download | [zenodo.org/record/7730708](https://zenodo.org/record/7730708) (v1.0; Zenodo shows a newer version) | [10.1002/mp.16812](https://doi.org/10.1002/mp.16812) | Search |
| Breast | BrEaST (TCIA name: BREAST-LESIONS-USG) | 256 patients (TCIA lists 522 image files); BI-RADS features; biopsy results; lesion masks | CC BY 4.0; open | [TCIA collection](https://www.cancerimagingarchive.net/collection/breast-lesions-usg/) | Data: [10.7937/9WKK-Q141](https://doi.org/10.7937/9WKK-Q141); paper: [10.1038/s41597-024-02984-z](https://doi.org/10.1038/s41597-024-02984-z) | Opened |
| Thyroid | DDTI (Digital Database of Thyroid Images) | TI-RADS labels; lesion outlines in XML; counts differ by source (347 to 480 images, about 290 patients); handwritten marks on some images | Not checked | Original host (cimalab.unal.edu.co) failed the TLS (secure connection) check; gated mirror: [MedXAgent/OpenThyroidDB](https://huggingface.co/datasets/MedXAgent/OpenThyroidDB) | [10.1117/12.2073532](https://doi.org/10.1117/12.2073532) | Not opened |
| Thyroid | TN3K | 3,493 images; nodule masks; benign or malignant | Data licence not stated; code MIT | Download links (Google Drive, Baidu) in the README of [TRFE-Net repo](https://github.com/haifangong/TRFE-Net-for-thyroid-nodule-segmentation) | TRFE-Net, ISBI 2021 (DOI not checked) | Search |
| Thyroid | Stanford Thyroid Ultrasound Cine-clip | 167 patients, 192 biopsy-confirmed nodules, 17,412 frames; masks; TI-RADS descriptors; pathology | Non-commercial research use; registration | [aimi.stanford.edu/datasets/thyroid-ultrasound-cine-clip](https://aimi.stanford.edu/datasets/thyroid-ultrasound-cine-clip) | [10.71718/7m5n-rh16](https://doi.org/10.71718/7m5n-rh16) | Search |
| Fetal | HC18 | 1,334 fetal head images (999 training, 335 test); head circumference, mm | Not checked | [hc18.grand-challenge.org](https://hc18.grand-challenge.org/); data on Zenodo | Data: [10.5281/zenodo.1322001](https://doi.org/10.5281/zenodo.1322001); van den Heuvel et al., PLoS One 2018, e0200412 | Search |
| Fetal | FETAL_PLANES_DB | 12,400 images; 6 classes (4 fetal planes, maternal cervix, other); brain sub-planes; train/test split; 2.1 GB | Not checked | [zenodo.org/record/3904280](https://zenodo.org/record/3904280) | [10.1038/s41598-020-67076-5](https://doi.org/10.1038/s41598-020-67076-5) | Search |
| Heart | CAMUS | 500 patients (450 training, 50 test); apical 2- and 4-chamber sequences; expert outlines | CC BY-NC-SA 4.0; non-commercial research only | [creatis.insa-lyon.fr/Challenge/camus](https://www.creatis.insa-lyon.fr/Challenge/camus/) | [10.1109/TMI.2019.2900516](https://doi.org/10.1109/TMI.2019.2900516) | Search |
| Heart | EchoNet-Dynamic | Over 10,000 echo videos | Research use agreement; non-commercial | [AIMI page](https://aimi.stanford.edu/datasets/echonet-dynamic-cardiac-ultrasound); [echonet.github.io/dynamic](https://echonet.github.io/dynamic/) | [10.71718/yqp5-y078](https://doi.org/10.71718/yqp5-y078) | Search |
| Heart | EchoNet-Pediatric | Echo videos, patients aged 0 to 18 years (count not checked) | As EchoNet-Dynamic; the download link must not be shared | [AIMI page](https://aimi.stanford.edu/datasets/echonet-pediatric) | [10.71718/d05h-gy43](https://doi.org/10.71718/d05h-gy43) | Search |
| Heart | EchoNet-LVH | 12,000 parasternal long-axis videos | As EchoNet-Dynamic; no redistribution | [AIMI page](https://aimi.stanford.edu/datasets/echonet-lvh) | DOI not checked | Search |
| Liver | Byra fatty-liver dataset | 550 images, 55 patients (38 fatty, 17 not fatty); steatosis from biopsy | Not checked | [zenodo.org/records/1009146](https://zenodo.org/records/1009146) | Data: [10.5281/zenodo.1009146](https://doi.org/10.5281/zenodo.1009146); paper: [10.1007/s11548-018-1843-2](https://doi.org/10.1007/s11548-018-1843-2) | Search |
| Liver | AUL (Annotated Ultrasound Liver images) | 735 images (435 malignant, 200 benign, 100 without mass); liver and mass outlines | Unclear: metadata says CC BY 4.0, the page says the data are subject to copyright | [zenodo.org/records/7272660](https://zenodo.org/records/7272660) | [10.5281/zenodo.7272660](https://doi.org/10.5281/zenodo.7272660) | Search |
| Liver | B-mode-and-CEUS-Liver | 120 patients, 1,859 images (DICOM); liver masses; B-mode and CEUS | CC BY 4.0; open | [TCIA collection](https://www.cancerimagingarchive.net/collection/b-mode-and-ceus-liver/) | [10.7937/TCIA.2021.v4z7-tc39](https://doi.org/10.7937/TCIA.2021.v4z7-tc39) | Opened |
| Gallbladder | GBCU (Gallbladder Cancer Ultrasound) | 1,255 images, 218 patients (432 normal, 558 benign, 265 malignant images) | Signed licence agreement; no commercial use, no redistribution | [gbc-iitd.github.io/data/gbcu](https://gbc-iitd.github.io/data/gbcu); video set: [gbusv](https://gbc-iitd.github.io/data/gbusv) | Basu et al., CVPR 2022; [arXiv 2204.11433](https://arxiv.org/abs/2204.11433) | Search |
| Kidney | Open Kidney Ultrasound Data Set | Images from over 500 patients; native and transplanted kidneys; multi-class masks; view labels | CC BY-NC-SA; registration | [rsingla92.github.io/kidneyUS](https://rsingla92.github.io/kidneyUS) | [arXiv 2206.06657](https://arxiv.org/abs/2206.06657) | Search |
| Lung | POCUS / COVID-19 lung ultrasound | Over 200 videos; COVID-19, bacterial pneumonia, healthy; partly collected from public web sources | No licence named ("feel free to use and cite") | [github.com/jannisborn/covid19_ultrasound](https://github.com/jannisborn/covid19_ultrasound) | [10.3390/app11020672](https://doi.org/10.3390/app11020672) | Opened |
| Lung | COVID-BLUES | 371 videos, 63 patients, prospective clinical study; the POCUS repo recommends it over POCUS | Not checked | Linked from the POCUS repo README | Wiedemann et al., IEEE JBHI 2025 (DOI not checked) | Opened (README mention only) |
| Ovary | MMOTU (Multi-Modality Ovarian Tumor Ultrasound) | 1,469 2D images and 170 CEUS images; pixel labels; tumour classes | Repo Apache-2.0; data licence not stated separately | [github.com/cv516Buaa/MMOTU_DS2Net](https://github.com/cv516Buaa/MMOTU_DS2Net) | [arXiv 2207.06799](https://arxiv.org/abs/2207.06799); [10.1016/j.patcog.2025.112311](https://doi.org/10.1016/j.patcog.2025.112311) | Search |
| Nerve (neck) | Ultrasound Nerve Segmentation (Kaggle, 2016) | 5,635 training images, 47 subjects, 420 × 580 px; brachial plexus masks; about 60% of images have no nerve | Kaggle competition rules | [kaggle.com/competitions/ultrasound-nerve-segmentation](https://www.kaggle.com/competitions/ultrasound-nerve-segmentation) | None | Not opened (fetch blocked; URL from a secondary page) |

BI-RADS: Breast Imaging Reporting and Data System. TI-RADS: Thyroid Imaging Reporting and
Data System. CEUS: contrast-enhanced ultrasound. DICOM: Digital Imaging and Communications in
Medicine (file format). CC BY: Creative Commons Attribution; NC: non-commercial; SA:
share-alike. px: pixels. Check: see Table 1.

**Table 3. Public raw-signal ultrasound datasets (data before image formation).**

| Dataset | Content | Licence and access | URL | Reference | Check |
|---|---|---|---|---|---|
| PICMUS (Plane-wave Imaging Challenge in Medical UltraSound, 2016) | Simulated, phantom and in-vivo carotid plane-wave data | Free to use; cite the challenge paper | [CREATIS open datasets](https://www.creatis.insa-lyon.fr/site/en/challenge-organization-and-open-datasets); mirror without the in-vivo part: [zeahub/picmus](https://huggingface.co/datasets/zeahub/picmus) | [10.1109/ULTSYM.2016.7728908](https://doi.org/10.1109/ULTSYM.2016.7728908) | Search |
| CUBDL (Challenge on Ultrasound Beamforming with Deep Learning, 2020) | 576 acquisition sequences | Signed user agreement; users report slow approval | [IEEE DataPort](https://ieee-dataport.org/competitions/challenge-ultrasound-beamforming-deep-learning); [cubdl.jhu.edu](https://cubdl.jhu.edu) | Data: [10.21227/f0hn-8f92](https://doi.org/10.21227/f0hn-8f92) | Search |
| OASBUD (Open Access Series of Breast Ultrasonic Data) | Raw signals from 100 breast lesions (52 malignant, 48 benign), 78 women | Not checked | [zenodo.org/record/545928](https://zenodo.org/record/545928) (that this record is OASBUD is likely, not confirmed) | [10.1002/mp.12538](https://doi.org/10.1002/mp.12538) | Search |

Check: see Table 1.

**Compiled list.** The UltraSam paper (Meyer et al., University of Strasbourg) gathered 43
open ultrasound datasets into "US-43d": over 280,000 images, with masks for over 50
anatomical structures. The README of
[github.com/CAMMA-public/UltraSam](https://github.com/CAMMA-public/UltraSam) lists all 43
with one source link each (in a collapsed table). It gives no per-dataset licences.
Paper: [arXiv 2411.16222](https://arxiv.org/abs/2411.16222);
[10.1007/s11548-025-03517-8](https://doi.org/10.1007/s11548-025-03517-8). Check: Opened.

**Cautions.**

- Licences differ. Several datasets are non-commercial or need a signed agreement (CAMUS,
  Open Kidney, the Stanford AIMI sets, GBCU, CUBDL).
- Mirrors on Kaggle, Roboflow, Hugging Face and Academic Torrents copy other datasets. Use the
  original licence, and remove duplicates when you combine sources.
- Quality: BUSI has duplicate and axilla images (letter above). DDTI and TN3K have handwritten
  marks on some images
  ([MICCAI 2025 paper](https://papers.miccai.org/miccai-2025/paper/2024_paper.pdf)).
- Teaching sites and video platforms (e.g. Radiopaedia, ultrasoundcases.info, YouTube) were
  not checked. Do not assume they allow scraping or training; read their terms first.

## Next

- Pick the datasets of interest; read each licence at the source before download.
