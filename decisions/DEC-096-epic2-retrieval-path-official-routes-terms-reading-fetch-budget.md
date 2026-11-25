---
id: DEC-096
title: Epic 2 retrieval path - official live-checked routes only (R7 listing with embedding, Roboflow source images from the R7 url, R8 labels per kept image, like and workspace candidates), the user's reading of Roboflow's terms, and a fetch budget that works then goes idle
status: accepted
area: [datasets]
created: 2026-11-25
from: [DIS-054]
related: [DEC-090, DEC-081, DEC-082, DIS-050]
superseded_by:
---
# DEC-096: Epic 2 retrieval path, terms reading and fetch budget

## Context

[DEC-090](DEC-090-epic2-roboflow-know-how-sub-epic.md) point 5 left the retrieval path of epic 2 to the user, once the know-how sub-epic had
written its docs. The summary [README](../../docs/scraping/roboflow/README.md) of
`docs/scraping/roboflow/` ([TASK-234.07](../../backlog/tasks/task-234.07%20-%20Epic-2-know-how-7-summary-README-with-the-recommended-route-per-need-a-scraping-row-in-the-context-map-open-choices-for-TASK-235-DEC-090.md)) gives the recommended route per need (its Table 2) and
eight open choices, C1 to C8 (its section 5). C8 (no HAR) was decided on 2026-11-25
([DIS-050](../discussions/DIS-050-epic2-roboflow-know-how-sub-epic.md), "Later"). This DEC
settles C1 to C7, in [TASK-235](../../backlog/tasks/task-235%20-%20Decide-epic-2-retrieval-path-routes-for-image-listing-per-image-metadata-and-embedding-labels-original-unaugmented-images-and-similar-projects-any-undocumented-route-at-all-DEC-090-point-5.md).
Route names R1 to R11 and terms Q1 to Q9 are those of the README and of
[limits-and-terms.md](../../docs/scraping/roboflow/limits-and-terms.md) section 6.

## Decision

The user accepted this on 2026-11-25 (consult session,
[DIS-054](../discussions/DIS-054-epic2-retrieval-path.md)): the recommended option of C1, C2, C3,
C4, C5 and C7; for C6, their own reading of the terms; for terms Q9, a fetch budget with two
values of their own.

1. **Official routes only (C7).** The scraper calls only routes in Roboflow's Platform API docs.
   No route of the Universe web app, and no SDK-only parameter (`POST /`, `nocache=true`). A later
   need for one is a new DEC.
2. **Listing and per-image metadata (C1).** R7 `POST /<workspace>/<project>/search`, 250 a
   request, adding 250 to `offset` until a page is short or `offset` reaches `total`; the `fields`
   of original-images.md section 4 plus `embedding`. The step compares `total` with R4
   `project.images` and logs a gap. R8 `GET /<workspace>/<project>/images/<image_id>` only where
   one image needs more.
3. **Original unaugmented images (C1).** The Roboflow source images, fetched from the R7 `url`
   on `source.roboflow.com`, with no key and no cookie. The image format is read from the first
   bytes, not from `content-type`; the body MD5 is checked against the `ETag` or the
   `x-goog-hash` MD5. Roboflow version exports are not used for images. So the fingerprint step no
   longer picks a Roboflow version ([TASK-249](../../backlog/tasks/task-249%20-%20Epic-2-Roboflow-version-pick-use-the-Roboflow-versions-augmentation-field-empty-means-unaugmented-and-record-its-resize-step-instead-of-the-closest-image-count-live-finding-of-TASK-234.04.md) is dropped); R4 Roboflow versions with their
   preprocessing and augmentation stay as datasource metadata ([DEC-081](DEC-081-epic2-mission-roboflow-universe-ultrasound-scraper.md) Table 2).
4. **Fingerprints (C1; amends DEC-081 Table 2).** `np_md5_c3` and dHash of the image as stored,
   plus a dHash of the image with its EXIF orientation applied ([TASK-252](../../backlog/tasks/task-252%20-%20Roboflow-fingerprint-step-dHash-also-on-the-EXIF-orientation-applied-image-image-format-from-the-first-bytes-TASK-234.05-finding.md)).
5. **Roboflow labels (C2).** R8 with `include=annotation`, one request per image, in the store
   step and for kept datasources only. Which label form is stored (R8's own form, or COCO through
   `format=coco`) stays with [TASK-205](../../backlog/tasks/task-205%20-%20Decide-epic-2-licences-and-labelings-allowed-Universe-licences-how-attribution-is-kept-which-export-format-is-stored-DIS-041-open-questions-4-and-5.md).
6. **Embedding (C3).** Stored as R7 returns it, as float32; scaled to unit length only when used.
7. **Similar projects (C4).** Besides keyword search, two candidate sources: R1 `q=like:<project>`
   for each indexed datasource, and R3 `GET /<workspace>` (the other public Universe projects of
   the same workspace). Every candidate goes through the same filters and ultrasound check as a
   keyword hit and records how it was found: the query, or `like:` or workspace of which indexed
   datasource. The first index run ([TASK-211](../../backlog/tasks/task-211%20-%20Epic-2-first-index-run-discover-image-index-and-ultrasound-check-over-Universe-aggregate-report-with-the-histogram-of-the-ultrasound-sample-encounter-rate-for-the-user-DEC-081-outcome-D1.md)) reports, for each of the three sources, how many
   candidates pass. Our own embedding similarity serves ranking or dedup, not discovery.
8. **Auth and back-off (C5).** The key goes only as an `Authorization: Bearer` header, and only
   to `api.roboflow.com`; never to the image host or to export links. On HTTP 429 the client waits
   at least `Retry-After` when present, else its doubling back-off; R8 gets a read timeout and a
   retry. [TASK-246](../../backlog/tasks/task-246%20-%20Roboflow-client-send-the-API-key-in-the-Authorization-Bearer-header-not-the-api_key-query-parameter-and-wait-Retry-After-on-HTTP-429-official-api.md-findings-F1-F2.md) folds into TASK-200.
9. **Terms (C6): the user's reading, recorded instead of asking Roboflow.** It is the user's
   reading, not legal advice.
   1. **Q1 and Q4.** Calls to the documented API on `api.roboflow.com` with our own key are
      ordinary API use, which Roboflow is built to serve. This covers the URLs the API returns
      (the Roboflow source images on `source.roboflow.com`, export links) and the index of Universe
      listings that TASK-211 builds (terms Q4). The user's picture: "me browsing roboflow for data,
      but automate with script and you".
   2. **Q5.** Keeping the kept images in the private bucket of
      [DEC-082](DEC-082-scraped-universe-images-plain-in-a-private-s3-bucket.md) is not
      re-hosting; in the user's words, "we only use inside our training course". So the bucket
      stays private and the images are not re-hosted or published. Licences, attribution, and
      terms Q6 and Q7 stay with TASK-205.
   3. **Q9.** The volume matters: the scraper keeps its rate and volume low with the fetch budget
      of point 10.

   TASK-211 does not wait for a letter to Roboflow.
10. **Fetch budget (terms Q9; the user's "work-and-go-idle mechanism").** It applies to every
    request to any Roboflow host, counted together (`api.roboflow.com`, `source.roboflow.com`,
    export links):
    1. between two requests, at least 1.0 s plus a random wait of 0.2 to 0.8 s (the user's values);
    2. work for 300 requests (the user's value), then idle for 10 min;
    3. a daily cap of 20,000 requests or 2,000 MB of image bytes, whichever comes first, counted
       per UTC day across runs on that machine; at the cap the run stops cleanly, and the next run
       resumes;
    4. after any HTTP 429 or 5xx answer: wait `Retry-After` (or the back-off), then idle for
       30 min and halve the work period for the rest of the run; after 3 such events in one run,
       stop and report;
    5. before a fetching step starts, it prints a volume plan: expected requests, MB and hours,
       from the R4 image counts and the budget; for a real run the agent shows it to the user and
       waits for an ok (TASK-211, [TASK-213](../../backlog/tasks/task-213%20-%20Epic-2-dedup-and-store-run-fingerprint-the-project-dataset-images-on-machine01-dedup-the-eligible-Universe-datasources-store-what-is-kept-dataset-style-record-with-counts-licences-and-attribution-DEC-081-outcomes-D3-to-D5.md));
    6. one machine fetches at a time (machine01 or the scraper EC2 instance);
    7. steps resume where they stopped, so nothing is fetched twice within one step.

    The values sit in `configs/scraping/roboflow_universe.yaml` under `fetch_budget` and may change
    per run. The 10 min idle, the daily caps and the trouble rule are the starting values of the
    moderate preset that the user edited (they changed the wait and the work period; assumption:
    their notes edited that preset). With these values a request comes every 1.5 s on average, a
    work period lasts about 7.5 min, and about 1,000 requests go out an hour; the daily cap is
    reached after about 19 h, so 100,000 image requests take about 5 days.

## Consequences

- [TASK-200](../../backlog/tasks/task-200%20-%20Roboflow-API-check-for-epic-2-per-image-listing-with-image-ids-and-URLs-per-image-embedding-vectors-similar-project-suggestions-client-methods-README-findings-synthetic-tests-DEC-081.md)
  (client code) gets the chosen routes, the auth and back-off of point 8 (TASK-246 archived into
  it) and the fetch budget of point 10; it also marks C1 to C7 as decided in the summary README.
- [TASK-206](../../backlog/tasks/task-206%20-%20Epic-2-datasource-index-keyword-and-similar-project-discovery-partial-image-index-with-np_md5_c3-dHash-embedding-and-image-URL-versioned-index-tables-under-the-scraping-root-synthetic-tests-DEC-081.md) (index step) builds on points 2, 3, 4, 6 and 7 and depends on TASK-252 (second dHash,
  format from the first bytes), which moves to To Do. TASK-249 (Roboflow version pick) is
  archived.
- [TASK-209](../../backlog/tasks/task-209%20-%20Epic-2-store-step-download-the-images-and-labelings-of-what-dedup-kept-to-the-scrape-bucket-or-a-local-folder-under-the-scraping-root-with-a-manifest-resumable-refuses-any-other-destination-synthetic-tests-with-a-fake-S3-DEC-081-DEC-082.md) (store step) builds on points 3, 5 and 10, and its manifest records whether each image
  carries an EXIF orientation tag: the frame of R8 boxes on such images is unverified (README
  section 6).
- TASK-211 and TASK-213 (runs) show the volume plan first and fetch from one machine at a time;
  TASK-211 reports the pass counts per candidate source.
- [TASK-203](../../backlog/tasks/task-203%20-%20Decide-epic-2-partial-image-index-images-per-datasource-all-or-a-shortlist-how-the-shortlist-is-drawn-index-table-names-and-format-DEC-081-points-4-and-6.md) (partial image index) can now be decided: it depends on TASK-235 instead of TASK-200.
  Its shortlist size sets most of the index step's requests under the fetch budget.
- TASK-205 (licences and labelings) keeps terms Q6 and Q7, and the stored label form.
- [TASK-247](../../backlog/tasks/task-247%20-%20Scraping-config-max_pages_per_query-30-exceeds-the-documented-10-page-cap-of-Universe-search-align-the-config-and-the-discover-loop-found-in-TASK-234.06.md) (search page cap) moves to To Do unchanged.
- Alternatives not taken (DIS-054): Roboflow version exports for images (C1) or labels (C2);
  dropping `like:` (C4); unit-length vectors only (C3); the `api_key` query (C5); asking Roboflow
  in writing before TASK-211, or asking only Q5 before TASK-213 (C6); the moderate and gentle
  presets as offered.
