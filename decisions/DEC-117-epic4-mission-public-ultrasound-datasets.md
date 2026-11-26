---
id: DEC-117
title: Mission of the fourth research epic - download public ultrasound datasets that support epics 1 and 3 and later anatomical and pathological diagnosis work across organs
status: accepted
area: [datasets]
created: 2026-11-26
from: []
related: [DEC-063, DEC-065, DEC-081, DEC-082, DEC-096, DEC-100, DEC-111]
superseded_by:
---
# DEC-117: Mission of Epic 4 - public ultrasound datasets

## Context

- The project trains on about 20k images (dataset version 261023). Ultrasound foundation-model papers
  train on 100k to 5M images drawn mostly from public datasets, though most of those counts are video
  frames ([stage 1 study](../literature/epic4-public-ultrasound-datasets-study.md), Section 1).
- [DEC-111](DEC-111-epic3-more-data-261023-only.md) (epic 3 more data: 261023 only) left public
  datasets out of epic 3 for now, "maybe epic 4".
- On 2026-11-25 the user asked for an epic 4 in two stages and for a study focused on stage 1. The
  study of 2026-11-26 lists 271 census rows, proposes a download plan in three waves and an AWS design,
  and decides nothing.

## Decision

The user stated the mission on 2026-11-26, in the session that wrote the stage 1 study. Points 2 and 3
are the user's own plan from the request of 2026-11-25.

1. **Mission.** Download public ultrasound datasets that can support the current research focus,
   epic 1 ([DEC-065](DEC-065-mission-upper-abdomen-anatomy-segmentation.md), upper-abdomen anatomy
   segmentation) and epic 3 ([DEC-100](DEC-100-epic3-mission-spot-liver-diseases.md), spotting liver
   diseases), and the research focuses that follow, which could be anatomical and pathological
   diagnosis on various topics and organs. So the collection is not limited to the abdomen or the
   liver.
2. **Stage 1, the first focus.** List all public or published ultrasound datasets, from the papers
   already on the project's radar and from the Internet; make a download plan for each; download into
   a private S3 bucket, for speed and as a backup, with long-lasting access to one bucket or folder
   considered; run the download script on EC2, for speed.
3. **Stage 2, later.** Compare the public datasets with dataset 261023 for dedup; build the next
   dataset version from public sources; and a new concept, the **super-dataset**: a training set that
   code combines at runtime from several chosen, versioned datasets.
4. **Not decided here.** These stay open, with the defaults proposed in Section 7 of the study:
   - the storage rule for public ultrasound images: [DEC-063](DEC-063-public-non-patient-datasets-root.md)
     (public non-patient datasets root) asks for its own decision before they are stored, and
     [DEC-082](DEC-082-scraped-universe-images-plain-in-a-private-s3-bucket.md) (scraped Roboflow
     Universe images stored plain in a private bucket) covers Roboflow data only;
   - whether the use is commercial, which decides which licences can be used;
   - the long-lived credential for machine01 (IAM Roles Anywhere, or an IAM user key scoped to one
     prefix);
   - the boundary with epic 2 ([DEC-081](DEC-081-epic2-mission-roboflow-universe-ultrasound-scraper.md),
     the Roboflow Universe scraper): the study left Roboflow-hosted datasets to epic 2;
   - retrieval rules for epic 4: the study proposes rules after the pattern of
     [DEC-096](DEC-096-epic2-retrieval-path-official-routes-terms-reading-fetch-budget.md) (epic 2
     retrieval: official routes only, the user's reading of the terms, a fetch budget).

## Consequences

- Nothing is downloaded until the storage rule of point 4 (not decided here) is decided. Until then
  DEC-063 (public non-patient datasets root), [DEC-024](DEC-024-plain-never-leaves-machine01-ec2-label-studio-decrypts-in-ram.md) (plain-style project data never leaves machine01)
  and [DEC-052](DEC-052-privacy-covers-images-tables-readable-after-asking.md) (images are patient data; tables readable after asking) hold as they are, and no agent
  session opens or describes a public image.
- Because the mission reaches beyond epics 1 and 3, the census keeps all organs and all label types.
  Abdomen and liver sets go first while epics 1 and 3 run.
- The next sessions follow the [epic 4 relay note](../journal/2026/2026-11-26-epic4-relay-claude.md):
  a consult session on the open points of point 4, a second research round, then tasks.
