# Public Sources for Ultrasound Images and Videos

## Overview

Public ultrasound datasets include still images, video clips, and complete clinical studies. Choose a source according to anatomy, annotation type, access conditions, and intended use. Counts of images, videos, and studies are not directly comparable.

## Downloadable Datasets

### 1. Clinical Ultrasound Image Repository — AWS Open Data

- **Data:** Clinical ultrasound studies, including abdominal, cardiac, and obstetric/gynecological imaging.
- **Access:** Public AWS S3 repository; consult the registry for current contents and access instructions.
- **Registry URL:** https://registry.opendata.aws/clinical-ultrasound-image-data/
- **S3 location:** `s3://clinical-ultrasound-image-repository/`
- **Example command:**

```bash
aws s3 ls --no-sign-request s3://clinical-ultrasound-image-repository/
```

### 2. BUSI — Breast Ultrasound Images

- **Data:** 780 breast ultrasound images in the original dataset.
- **Annotations:** Normal, benign, and malignant categories, with segmentation masks.
- **Applications:** Breast-image classification and lesion segmentation.
- **Dataset catalog:** https://datasetcatalog.nlm.nih.gov/dataset?q=0001971209
- **Dataset documentation:** https://github.com/openmedlab/Awesome-Medical-Dataset/blob/main/resources/BUSI.md
- **Kaggle mirror:** https://www.kaggle.com/datasets/subhajournal/busi-breast-ultrasound-images-dataset
- **Note:** Verify a mirror against the original release and review the applicable reuse terms.

### 3. EchoNet-Dynamic — Stanford

- **Data:** 10,030 labeled echocardiography videos.
- **Annotations:** Cardiac-function measurements and expert ventricular tracings.
- **Applications:** Cardiac video analysis, ventricular segmentation, and function estimation.
- **Project and access information:** https://echonet.github.io/dynamic/
- **Stanford dataset page:** https://aimi.stanford.edu/datasets/echonet-dynamic-cardiac-ultrasound
- **Code and documentation:** https://github.com/echonet/dynamic
- **Access considerations:** Registration and a research-use agreement apply. Review the current terms, including non-commercial research restrictions, before downloading or using the data.

### 4. FETAL_PLANES_DB — Zenodo

- **Data:** Approximately 12,400 maternal-fetal ultrasound still images.
- **Annotations:** Anatomical-plane categories, including fetal abdomen, brain, femur, thorax, maternal cervix, and other views; fetal brain images also have more detailed plane labels.
- **Applications:** Anatomical-plane classification and fetal ultrasound research.
- **Original dataset record and downloads:** https://zenodo.org/records/3904280

## Directories for Finding Additional Datasets

| Resource | What it provides | URL |
|---|---|---|
| Ultrasound Open Access Datasets | Curated directory with modality, clinical application, and licence filters | https://ultrasound-open-access.nidusai.ca/ |
| Open Medical Ultrasound Dataset Atlas | Catalog of public ultrasound resources with source links, task descriptions, and access information | https://github.com/TIanCat/open-medical-ultrasound-datasets |
| Academic Torrents — Ultrasound | Collection of ultrasound image and video datasets | https://academictorrents.com/collection/ultrasound |
| Kaggle ultrasound search | Dataset discovery and community-hosted mirrors | https://www.kaggle.com/datasets?search=ultrasound |

## Selection and Collection Checklist

- Match the anatomy and acquisition type to your project.
- Distinguish individual images, video clips, patients, and complete studies when comparing dataset sizes.
- Check whether annotations provide diagnostic labels, segmentation masks, anatomical views, or physiological measurements.
- Prefer original releases; verify the provenance and completeness of mirrors.
- Review the dataset licence and any data-use agreement. Public availability does not automatically permit commercial use or redistribution.
- Confirm current download instructions and access requirements on the linked source pages.

## Source Note

This Markdown report reformats the sources and findings identified in the preceding conversation. URLs point to source pages or clearly labeled mirrors; access conditions and repository contents may change. No new verification of the linked pages was performed for this file-generation request.
