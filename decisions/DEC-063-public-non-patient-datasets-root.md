---
id: DEC-063
title: Public non-patient datasets get their own root and may go to the GPU box and RunPod
status: accepted
area: [datasets, data-security]
created: 2026-11-17
from: [DIS-029]
related: [DEC-024, DEC-062]
superseded_by:
---
# DEC-063: Public non-patient datasets get their own root and may go to the GPU box and RunPod

## Context

The B-mode box detector ([DEC-062](DEC-062-bmode-box-detector-bmode-det-v1.md)) uses two
public datasets as negatives: MedNIST (CC BY-SA 4.0) and Imagenette-320 (Apache 2.0 per
its Hugging Face card; the fastai repo LICENSE is still to be read). They are not patient
data. The project's data rules
([DEC-024](DEC-024-plain-never-leaves-machine01-ec2-label-studio-decrypts-in-ram.md):
plain-style data never leaves machine01) cover the project's own datasets; no rule yet says
where public datasets live or whether they may go to the GPU box.

## Decision

The user accepted this on 2026-11-17 (consult session).

- Public datasets that hold no patient data live under a new root,
  `SONOAI_PUBLIC_DATA_ROOT` (`sonoai.paths.PUBLIC_DATA_ROOT`), one folder per dataset,
  outside git and outside the project's dataset folders.
- They are downloaded on machine01 (with `aria2c` for large files) and may be copied as
  they are to the GPU box and RunPod. They are not put in the encrypted store.
- Each dataset gets a short record with its source URL, version or checksum, licence,
  attribution text and image counts.
- Scraped ultrasound images are not covered here: they may hold burned-in patient text and
  stay under the scraping rules (enc1 store only).
- DEC-024 is unchanged.

## Consequences

- The infra task for the detector's public negatives adds the root, downloads MedNIST and
  Imagenette-320 and copies them to the GPU box.
- A later public dataset that may hold patient data (for example scraped ultrasound) needs
  its own decision.
