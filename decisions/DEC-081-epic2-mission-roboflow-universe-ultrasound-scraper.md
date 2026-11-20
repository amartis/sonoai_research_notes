---
id: DEC-081
title: Mission of the second research epic - a scraper that indexes ultrasound datasources on Roboflow Universe, checks them for ultrasound, dedups them against the project dataset and stores the kept images and labelings
status: accepted
area: [datasets, aws]
created: 2026-11-20
from: [DIS-041]
related: [DEC-024, DEC-035, DEC-052, DEC-053, DEC-063, DEC-065, DEC-072, DEC-073, DEC-074, DEC-082]
superseded_by:
---
# DEC-081: Mission of epic 2 - a Roboflow Universe ultrasound scraper

## Context

The project's models are trained on one project dataset (261023) with a limited number of
datasource groups. Public ultrasound datasets on Roboflow Universe are a source of new
datasources. A first pipeline exists in `src/sonoai/scraping/roboflow/` (discover, thumbnail
check, dHash fingerprints, shortlist of originals; [README](../../src/sonoai/scraping/roboflow/README.md)),
made on 2026-10-23 without a board task; its fingerprint and shortlist steps were never run on
the candidates, and it has no store step. Milestone m-4 (scrape-public-datasources) holds this
work.

A **research epic** is one mission DEC plus the point decisions, board tasks, runs and EXP
records that carry it ([DEC-065](DEC-065-mission-upper-abdomen-anatomy-segmentation.md)). This
DEC is the mission of **epic 2, Roboflow Universe scraping**. Its board tasks sit in milestone
m-4. Details of each function are decided later, one point DEC at a time
([DIS-041](../discussions/DIS-041-epic2-roboflow-universe-scraping.md) open questions).

## Decision

The user accepted this on 2026-11-20 (consult session, DIS-041).

### 1. Mission

Build a **scraper script** that runs on machine01 or on an AWS EC2 instance and:

1. **indexes datasources** on Roboflow Universe: finds them by keyword search and by Universe's
   similarity suggestions from datasources already indexed, checks each for ultrasound with a
   Qwen model on some of its images, and keeps a partial image index of each datasource that
   passes;
2. **dedups** them against the datasources already in the project dataset and against each
   other, by image fingerprints, dropping whole datasources or single images (a parameter);
3. **stores** the images and labelings of what is kept, in a private S3 bucket for scraped
   images or in a local folder ([DEC-082](DEC-082-scraped-universe-images-plain-in-a-private-s3-bucket.md)).

The script extends `sonoai.scraping.roboflow` (`python -m sonoai.scraping.roboflow <step>`);
it does not replace it. Every step stays resumable, as today.

### 2. When the epic is done

| # | Outcome | Shown by |
|---|---|---|
| D1 | An index of Universe datasources found by keyword and by suggestion, each with its ultrasound sample encounter rate | an aggregate report: counts per step, the histogram of the rate |
| D2 | A threshold on the rate, chosen by the user from that histogram | a point DEC |
| D3 | Dedup against the project dataset and between Universe datasources, by datasource or by image | a report of datasources and images kept and dropped, per reason (counts only) |
| D4 | The kept images and labelings stored, with a manifest | the bucket (or local folder) holds them; a dataset-style record with counts, licences and attribution |
| D5 | The same script runs on machine01 and on an EC2 instance | one run on each, logged |

Table 1. Outcomes of epic 2. Bringing a stored datasource into a project dataset (a new
`datasource_id`, labels mapped to content labels) is not part of this epic.

### 3. What one Roboflow datasource is

Each Universe **project** (`workspace/project`) is one **datasource** in the sense of the global
glossary (the user's terminology). Its versions are exports of the same images, not separate
datasources. While a datasource is only indexed it is keyed by its Universe ref
(`workspace/project`); it gets a `datasource_id` and an `images/dsidNNNN/` folder only when it
is brought into a project dataset.

### 4. What the index holds

| Level | Fields |
|---|---|
| Datasource | Universe ref, metadata (created, image count, classes, versions, project type), licence, how it was found (query, or the indexed datasource whose suggestion it came from), the ultrasound check (images checked, images called ultrasound, the rate, model version) |
| Image (partial index) | Universe image id, image URL, `np_md5_c3`, dHash, Roboflow embedding vector where the API gives one, split if known |

Table 2. Fields of the index. The fingerprints are the user's choice ([DIS-041](../discussions/DIS-041-epic2-roboflow-universe-scraping.md)
Q2): `np_md5_c3` is the exact key the project already uses (`sonoai.data.images.md5_c3`), dHash
catches re-encoded and resized copies, and the embedding is kept for later use; the user may
change this list. Whether the API gives per-image URLs and embeddings, and similar-project
suggestions, is unverified until the API spike task has checked it.

The index is a set of versioned tables under `$SONOAI_SCRAPING_ROOT/roboflow/`, named and
kept by the table rules ([DEC-053](DEC-053-table-naming-and-preservation.md)): a changed table is
a new file, never an edit. It is not in git.

### 5. Ultrasound check

A Qwen vision-language model looks at a sample of each datasource's images and says whether each
is ultrasound. The **ultrasound sample encounter rate** of a datasource is the number called
ultrasound divided by the number checked. A datasource is **ultrasound-eligible** when its rate
is at or above the threshold. The threshold is set by the user after the histogram (D2). Which
Qwen model, where it runs and how many images are checked are open (Parked tasks).

### 6. Dedup

- Against the project dataset: by `np_md5_c3` (exact) and dHash (near), with the project
  dataset's images fingerprinted on machine01.
- Between Universe datasources: the existing shortlist logic (overlap families, oldest original
  kept), on the same fingerprints.
- A parameter `dedup_unit` takes `datasource` (keep a datasource when enough of its images are
  new, as `min_novel_fraction` and `min_novel_images` do today) or `image` (keep the datasource
  but drop its images that are already covered).

### 7. Where each step may run

| Step | machine01 | scraper EC2 instance |
|---|---|---|
| discover, suggestions, image index (public metadata and fingerprints of Universe images) | yes | yes |
| ultrasound check | open (Parked) | open (Parked) |
| dedup against the project dataset | **yes, only here** | no |
| dedup between Universe datasources | yes | yes |
| store: download images and labelings to the bucket or a local folder | yes | yes |

Table 3. Where each step runs. Project dataset fingerprints are a table of the project dataset,
so they stay on machine01 ([DEC-024](DEC-024-plain-never-leaves-machine01-ec2-label-studio-decrypts-in-ram.md)).
The dedup step on machine01 writes the list of Universe datasources and images to store; that
list holds only Universe refs and image ids, so it may go to the EC2 instance.

### 8. Terms

Epic terms go in `docs/glossary/epic2-roboflow-universe-scraping.md` ([DEC-072](DEC-072-term-scopes-global-glossary-and-epic-terms-files.md)):
**ultrasound sample encounter rate** and **ultrasound-eligible datasource** (the user's
"usg-eligible") at the start; writers add more by the coining rules. "Datasource" keeps its
global meaning; point 3 says how it applies to Universe.

### 9. Fixed rules

1. Claude never opens, renders or describes a scraped image, as for any image in the project.
2. Committed text (records, board, commits) holds aggregate counts only, as for project data.
3. The Roboflow API key comes from `.env` on machine01 (`ROBOFLOW_API_KEY`) and from a secret
   store on EC2 (decided in the EC2 task); it is never committed or echoed.
4. The API is called politely: spaced requests, back-off on HTTP 429 (as the client does today).

## Consequences

- Board tasks (milestone m-4), made 2026-11-20:
  - ready: [TASK-200](../../backlog/tasks/task-200%20-%20Roboflow-API-check-for-epic-2-per-image-listing-with-image-ids-and-URLs-per-image-embedding-vectors-similar-project-suggestions-client-methods-README-findings-synthetic-tests-DEC-081.md) (Roboflow API check, method), [TASK-201](../../backlog/tasks/task-201%20-%20Private-S3-bucket-for-scraped-Universe-images-by-CloudFormation-all-Block-Public-Access-settings-server-side-encryption-TLS-only-policy-access-for-claude-agent-only-DEC-082.md) (scrape bucket, aws),
    [TASK-202](../../backlog/tasks/task-202%20-%20Rule-and-guard-texts-for-DEC-082-CLAUDE.md-plain-data-exception-for-scraped-Universe-data-command-policy-D1-patient-data-hook-check-services.md-scraping-package-docstring-m-4-milestone-text.md) (rule and guard texts for DEC-082, infra; the user merges);
  - Parked, needs-decision: [TASK-203](../../backlog/tasks/task-203%20-%20Decide-epic-2-partial-image-index-images-per-datasource-all-or-a-shortlist-how-the-shortlist-is-drawn-index-table-names-and-format-DEC-081-points-4-and-6.md) (partial image index), [TASK-204](../../backlog/tasks/task-204%20-%20Decide-epic-2-ultrasound-check-Qwen-model-where-it-runs-GPU-box-through-machine01-an-EC2-GPU-instance-or-CPU-and-images-checked-per-datasource-a-new-DEC-if-it-adds-a-place-for-plain-scraped-images-DEC-081-point-5-DEC-082-rule-2.md) (ultrasound check: model,
    place, sample count), [TASK-205](../../backlog/tasks/task-205%20-%20Decide-epic-2-licences-and-labelings-allowed-Universe-licences-how-attribution-is-kept-which-export-format-is-stored-DIS-041-open-questions-4-and-5.md) (licences and labelings), [TASK-212](../../backlog/tasks/task-212%20-%20Decide-ultrasound-sample-encounter-rate-threshold-from-the-histogram-of-the-first-index-run-DEC-081-outcome-D2.md) (rate threshold);
  - blocked To Do: [TASK-206](../../backlog/tasks/task-206%20-%20Epic-2-datasource-index-keyword-and-similar-project-discovery-partial-image-index-with-np_md5_c3-dHash-embedding-and-image-URL-versioned-index-tables-under-the-scraping-root-synthetic-tests-DEC-081.md) (index), [TASK-207](../../backlog/tasks/task-207%20-%20Epic-2-ultrasound-check-step-Qwen-on-sampled-images-per-datasource-ultrasound-sample-encounter-rate-aggregate-histogram-report-synthetic-tests-with-a-fake-model-DEC-081-point-5.md) (ultrasound check step), [TASK-208](../../backlog/tasks/task-208%20-%20Epic-2-dedup-step-against-the-project-dataset-np_md5_c3-exact-dHash-near-project-fingerprints-on-machine01-only-and-between-Universe-datasources-dedup_unit-datasource-or-image-kept-and-dropped-counts-synthetic-tests-DEC-081-point-6.md) (dedup),
    [TASK-209](../../backlog/tasks/task-209%20-%20Epic-2-store-step-download-the-images-and-labelings-of-what-dedup-kept-to-the-scrape-bucket-or-a-local-folder-under-the-scraping-root-with-a-manifest-resumable-refuses-any-other-destination-synthetic-tests-with-a-fake-S3-DEC-081-DEC-082.md) (store), [TASK-210](../../backlog/tasks/task-210%20-%20Epic-2-scraper-EC2-instance-CloudFormation-instance-and-role-with-access-to-the-scrape-bucket-only-Roboflow-API-key-in-a-secret-store-start-and-stop-through-the-aws-agent-one-test-run-DEC-081-point-7-DEC-082.md) (scraper EC2 instance), [TASK-211](../../backlog/tasks/task-211%20-%20Epic-2-first-index-run-discover-image-index-and-ultrasound-check-over-Universe-aggregate-report-with-the-histogram-of-the-ultrasound-sample-encounter-rate-for-the-user-DEC-081-outcome-D1.md) (first index run, D1),
    [TASK-213](../../backlog/tasks/task-213%20-%20Epic-2-dedup-and-store-run-fingerprint-the-project-dataset-images-on-machine01-dedup-the-eligible-Universe-datasources-store-what-is-kept-dataset-style-record-with-counts-licences-and-attribution-DEC-081-outcomes-D3-to-D5.md) (dedup and store run, D3 to D5).
- The m-4 milestone description says kept originals go into the encrypted store; DEC-082 changes
  that, so the description is updated with the board tasks.
- `src/sonoai/scraping/roboflow/README.md` is updated by the first code task.
- Alternatives not taken ([DIS-041](../discussions/DIS-041-epic2-roboflow-universe-scraping.md)):
  a datasource per project version; a `datasource_id` for every indexed datasource; a fresh
  scraper instead of extending the existing one.
