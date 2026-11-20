---
id: DIS-041
title: Epic 2 - a scraper for ultrasound datasources on Roboflow Universe (index, ultrasound check, dedup, private S3 store)
status: open
created: 2026-11-20
outcomes: [DEC-081, DEC-082]
related: [DEC-024, DEC-035, DEC-052, DEC-063, DEC-065, DEC-072, DEC-073, DEC-074]
---
# DIS-041: Epic 2 - a scraper for ultrasound datasources on Roboflow Universe

## Question

The user wants a second research epic: a script that finds ultrasound datasets on Roboflow
Universe (universe.roboflow.com), indexes them, removes the ones (or the images) the project
already has, and stores the images and their labelings in a private S3 bucket or on local disk.
The script runs on machine01 or on an AWS EC2 instance. This session settles the gist only; the
details are discussed later, task by task.

The script has three functions (the user's list):

1. **Datasource indexing.** Find datasources on Universe by keyword and by Universe's
   similarity suggestions from datasources already indexed. Check each one for ultrasound: a
   Qwen model looks at some of its images, and the share it calls ultrasound is the
   **ultrasound sample encounter rate** (the user's name). The threshold is set later, after the
   user has seen the histogram of this rate over the index. For each datasource that passes, keep
   a partial image index: fingerprints of a shortlist of its images, Roboflow's embedding
   vectors where Universe gives them, and image URLs.
2. **Dedup.** Compare fingerprints with the datasources already in the project dataset, and
   keep datasources with enough unique images. A behaviour parameter can instead drop single
   images rather than whole datasources.
3. **Store.** Download the images (and labelings) to disk, or put them in a new private S3
   bucket for scraped images.

Terminology (the user's): each dataset on Universe is a **datasource** in the sense of the
global glossary.

## What already exists

The repo already has a first version of this pipeline in `src/sonoai/scraping/roboflow/`
(5 commits on 2026-10-23, no board task; milestone m-4, scrape-public-datasources):

- `discover` searches Universe with the queries in `configs/scraping/roboflow_universe.yaml`
  and fetches project metadata; keyword relevance filters and a thumbnail colour check
  (`thumbcheck`, `modality.py`) left 216 candidates.
- `fingerprint` downloads one version export per candidate into memory and stores a 64-bit
  dHash per image; `shortlist` finds near-duplicates across datasources (Hamming distance
  ≤ 4), groups overlap families and keeps the oldest original of each.
- Not done then: running `fingerprint` and `shortlist` on the candidates, and the ingest step.

The new epic extends this code; it does not start over.

## Options considered

**Q1. Storage form of the scraped images in S3.**

- **A: enc1 ciphertext, encrypted in RAM** (the existing rule, [DEC-063](../decisions/DEC-063-public-non-patient-datasets-root.md): scraped ultrasound
  images may hold burned-in patient text and go to the enc1 store only). Keeps [DEC-024](../decisions/DEC-024-plain-never-leaves-machine01-ec2-label-studio-decrypts-in-ram.md) as it
  is. Cost: the passphrase must be typed on EC2 over SSM each time the scraper starts.
- **B: plain images in a private bucket** (server-side encryption, Block Public Access). Treats
  Universe images as already public. Simpler, and the scraper can run unattended on EC2. Needs a
  new DEC that amends DEC-063 and makes a narrow exception to DEC-024's wording.
- **The user chose B.** Claude's concern, said once: burned-in text in public ultrasound images
  can still name patients, and an upload cannot be taken back. The bucket rules in DEC-082 are
  there to limit that risk.

**Q2. Fingerprints in the index.**

- **A: np_md5_c3 only.** An exact pixel hash (`sonoai.data.images.md5_c3`), the project's own
  image key. Misses copies that were re-encoded or resized, which is how Universe forks are
  expected to differ (the reason the existing pipeline uses dHash; not measured on Universe yet).
- **B: np_md5_c3 plus dHash.** Exact key plus the perceptual hash the existing dedup uses.
- **C (the user's choice): np_md5_c3, dHash and Roboflow's embedding vector**, where the API
  gives one. The user may change this later. Whether and how the API returns per-image
  embeddings is **unverified**: a spike task checks it.

**Q3. What one Roboflow datasource is.**

- **A (chosen): one Universe project** (`workspace/project`). Keyed by that ref while it is
  only indexed; it gets a `datasource_id` and an `images/dsidNNNN/` folder only when its images
  are brought into the project. Versions of a project are re-exports of the same images, so a
  version is not a datasource.
- **B:** a `datasource_id` for every indexed project at once: one id space from day one, but
  ids for hundreds of datasources that are later dropped.
- **C:** one datasource per project version: splits one origin into several.

## Conclusion

- [DEC-081](../decisions/DEC-081-epic2-mission-roboflow-universe-ultrasound-scraper.md)
  (proposed): the mission of epic 2, its three functions, the datasource grain (Q3 A), the
  fingerprints (Q2 C), and where each step may run.
- [DEC-082](../decisions/DEC-082-scraped-universe-images-plain-in-a-private-s3-bucket.md)
  (proposed): scraped Universe images and their labelings may be stored plain in a new private
  bucket (Q1 B), with the rules that keep them apart from project data.
- Board tasks: named in DEC-081 Consequences once the user accepts.

## Open questions

Each is a Parked `needs-decision` task until the user takes it up.

1. **Where Qwen runs** for the ultrasound check. The GPU box runs Qwen3-VL-8B today ([DEC-035](../decisions/DEC-035-qwen3-vl-second-annotator-on-gpu-box.md))
   but has no internet, so sample images would pass through machine01 first. Other options: an
   EC2 GPU instance next to the scraper, or a smaller model on CPU.
2. **The ultrasound sample encounter rate threshold**, after the user has seen the histogram;
   also how many images per datasource the check looks at.
3. **How large the partial image index is** per datasource (all images or a shortlist), and how
   the shortlist is drawn. Dedup by single images (the behaviour parameter) needs fingerprints
   of every image that would be kept.
4. **Licences**: which Universe licences are allowed, and how attribution is kept.
5. **Labelings**: which export format is stored, and how Universe classes map to the project's
   content labels (needed only when a datasource is brought into a project dataset).
6. **Bringing a datasource into a project dataset**: a separate step under the full project
   data rules (DEC-082 rule 4); outside this epic's first scope.
