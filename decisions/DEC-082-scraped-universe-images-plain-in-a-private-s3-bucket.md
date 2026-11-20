---
id: DEC-082
title: Scraped Roboflow Universe images and labelings may be stored plain in a new private S3 bucket, kept apart from project data (amends DEC-063, an exception to DEC-024)
status: accepted
area: [data-security, aws, datasets]
created: 2026-11-20
from: [DIS-041]
related: [DEC-022, DEC-023, DEC-024, DEC-025, DEC-052, DEC-063, DEC-081]
superseded_by:
---
# DEC-082: Scraped Universe images plain in a private S3 bucket

## Context

Epic 2 ([DEC-081](DEC-081-epic2-mission-roboflow-universe-ultrasound-scraper.md)) stores the
images and labelings of the Universe datasources it keeps, from machine01 or from an EC2
instance. Today the rules send scraped ultrasound images to the enc1 store only
([DEC-063](DEC-063-public-non-patient-datasets-root.md): they may hold burned-in patient text),
and only enc1 ciphertext leaves machine01 ([DEC-024](DEC-024-plain-never-leaves-machine01-ec2-label-studio-decrypts-in-ram.md)).
Encrypting in RAM on EC2 would need the passphrase typed on the instance at every start.

The user chose to store Universe images plain in a private bucket instead ([DIS-041](../discussions/DIS-041-epic2-roboflow-universe-scraping.md)
Q1): they are already public on Universe, and the scraper can then run unattended. Claude's
concern, recorded once: burned-in text can still name a patient, and an upload cannot be taken
back; the rules below limit that risk.

## Decision

The user accepted this on 2026-11-20 (consult session, DIS-041).

1. **Scope.** This DEC covers only **scraped Universe data**: images and labelings (annotation
   exports) downloaded from public Roboflow Universe projects, and the epic 2 index tables
   (Universe metadata, URLs, fingerprints and embeddings of Universe images). It does not cover
   the project dataset or anything derived from it.
2. **Where scraped Universe data may be stored plain**, and nowhere else:
   - a new private S3 bucket for scraped images, proposed name `claude-agent-sonoai-scrape`
     (the IAM policy allows only `claude-agent-*` buckets; the aws task confirms the name);
   - the scraper EC2 instance (its own disk, for the run);
   - machine01, under the scraping root (`sonoai.paths.SCRAPING_ROOT`, env `SONOAI_SCRAPING_ROOT`;
     by default the `scraping/` folder of the data files root).

   The GPU box and RunPod are not on this list. The decision on where the Qwen check runs may add
   one, by a new DEC.
3. **The bucket.** Private: all four Block Public Access settings on, server-side encryption
   (SSE-KMS or SSE-S3, chosen in the aws task), a policy that denies non-TLS requests, access
   only for the `claude-agent` IAM user and the scraper instance role, no public or shared
   presigned links. Made by CloudFormation under `deploy/aws/`, like the data bucket.
4. **Kept apart from project data.** Nothing from the project dataset goes to the scrape bucket
   or the scraper instance: no project images, tables, fingerprints, file names or folder names.
   Dedup against the project dataset runs on machine01 (DEC-081 Table 3). When a scraped
   datasource is later brought into a project dataset, that copy is project data under every
   rule (plain on machine01 only, enc1 when shipped); the scrape copy stays where it is.
5. **Unchanged.** Claude never opens, renders or describes a scraped image. Committed text holds
   aggregate counts only. DEC-024 holds for all project data; the S3 data bucket
   `claude-agent-sonoai-data` stays enc1 only, and `sonoai-data push-s3` stays enc1 only. The
   scraper uploads through its own code path, to the scrape bucket only.
6. **DEC-063 amended.** Its bullet "Scraped ultrasound images ... stay under the scraping rules
   (enc1 store only)" is replaced, for Roboflow Universe images, by this DEC. Scraped Universe
   data is not a public image collection (it is not copied to the GPU box or RunPod as it is).

## Consequences

- Guard and rule texts to change, in one infra task that the user merges (guards, [DEC-032](DEC-032-agent-roster-consult-and-lead-skills.md)):
  the CLAUDE.md hard rule on plain data (add this exception next to [DEC-022](DEC-022-label-studio-open-to-outside-helpers.md) and [DEC-025](DEC-025-aws-labelstud-public-https.md)),
  `docs/command-policy.md` rule D1, `.claude/hooks/guard_patient_data.py` if it blocks uploads to
  the scrape bucket, `docs/services.md` (Roboflow row and the new bucket),
  `src/sonoai/scraping/roboflow/README.md` and `src/sonoai/scraping/__init__.py` (they say
  "EncryptedStore only"), and the m-4 milestone description.
- The aws agent makes the bucket and, later, the scraper instance and its role.
- Alternative not taken: enc1 ciphertext encrypted in RAM (keeps today's rules; would win if the
  user decides public scrapes must be treated as patient data, or if burned-in text is found
  often in the stored images).
