---
id: DIS-054
title: Epic 2 retrieval path - which Roboflow route the scraper uses per need, how Roboflow's terms are read, and how the scraper keeps its download volume low
status: concluded
created: 2026-11-25
outcomes: [DEC-096]
related: [DIS-050, DEC-090, DEC-081, DEC-082, DIS-041]
---
# DIS-054: Epic 2 retrieval path

## Question

[TASK-235](../../backlog/tasks/task-235%20-%20Decide-epic-2-retrieval-path-routes-for-image-listing-per-image-metadata-and-embedding-labels-original-unaugmented-images-and-similar-projects-any-undocumented-route-at-all-DEC-090-point-5.md)
([DEC-090](../decisions/DEC-090-epic2-roboflow-know-how-sub-epic.md) point 5): with the know-how docs of `docs/scraping/roboflow/` written, which route does
the scraper use for each need of epic 2 (listing, per-image metadata, embedding, Roboflow labels,
the original unaugmented images, similar projects), and does it use any undocumented route at
all? The summary [README](../../docs/scraping/roboflow/README.md) section 5 set out the choices
C1 to C8; C8 (no HAR) was already decided on 2026-11-25 ([DIS-050](DIS-050-epic2-roboflow-know-how-sub-epic.md), "Later"). Settling them unblocks
the client code task [TASK-200](../../backlog/tasks/task-200%20-%20Roboflow-API-check-for-epic-2-per-image-listing-with-image-ids-and-URLs-per-image-embedding-vectors-similar-project-suggestions-client-methods-README-findings-synthetic-tests-DEC-081.md) and the partial image index decision [TASK-203](../../backlog/tasks/task-203%20-%20Decide-epic-2-partial-image-index-images-per-datasource-all-or-a-shortlist-how-the-shortlist-is-drawn-index-table-names-and-format-DEC-081-points-4-and-6.md).

## Options considered

Consult session of 2026-11-25. Claude asked in two rounds; the user answered each question.

Table 1. The choices of the README section 5, the option Claude recommended, the best
alternative, and what the user chose.

| Choice | Recommended | Best alternative | User's choice |
|---|---|---|---|
| C1 listing and source images | R7 listing, Roboflow source images from the R7 `url` | one Roboflow version export per Universe project | recommended |
| C2 Roboflow labels | R8 `include=annotation` per kept image | one export per kept datasource, joined by file-name stem and dHash | recommended |
| C3 embedding | as returned, float32 | unit-length vectors only | recommended |
| C4 similar projects | R1 `like:` and R3 workspace as candidates, pass counts measured in [TASK-211](../../backlog/tasks/task-211%20-%20Epic-2-first-index-run-discover-image-index-and-ultrasound-check-over-Universe-aggregate-report-with-the-histogram-of-the-ultrasound-sample-encounter-rate-for-the-user-DEC-081-outcome-D1.md) | keyword search and R3 only | recommended |
| C5 auth and back-off | Bearer header only, `Retry-After` on HTTP 429 | the `api_key` query with redaction | recommended |
| C6 terms Q1, Q5, Q9 | ask Roboflow in writing before TASK-211 (Claude added Q4) | read now and ask only Q5; or read the text, no letter | the user's own reading (below) |
| C7 undocumented routes | none | the SDK-only `nocache=true` if a stale answer is seen | recommended |

C1, C2, C3, C5 and C7 were asked as one bundle, since every need had an official route checked
live: the exact key `np_md5_c3` needs the original pixels (0 of 269 export copies matched), the
source-image route works where every Roboflow version is augmented (2 of 3 check projects), and R8
covers train images with no unaugmented export copy (34 of 39 in one check project; README
sections 4 and 5).

**C6, terms.** The user answered in their own words:

- Q1: "We're fetching data from api.roboflow.com which is ordinary API request. Roboflow is
  designed to serve API."
- Q5: "We are not re-hosting any image, we only use inside our training course."
- Q9: "Important points. In order to avoid excessive downloads we will implement certain
  work-and-go-idle mechanism", details to be proposed by Claude.

Claude then asked whether the Q1 reading also covers two things the user had not named: the image
bytes, which come from `source.roboflow.com` (the URL in the API's R7 `url` field; export links
also leave `api.roboflow.com`), and terms Q4 (whether the index of Universe listings is a
"collection ... of listings" that the terms forbid on the Public Plan). The user: "Yes, both
covered. Just think of this scraping project as 'me browsing roboflow for data, but automate with
script and you', so there's no legal issue being raised."

Claude's note, said once: section 4(a) of the Terms of Use names "robots, spider/web crawler ...
or similar data gathering and extraction tools" on the Roboflow websites, so the picture of
automated browsing is close to what that clause names. The firmer ground for the reading is the
user's first reason: a documented API, our own key, used the way Roboflow's own docs describe
(limits-and-terms.md section 4.2). DEC-096 records the reading on both.

**Q9, fetch budget.** Claude proposed two presets with common rules (a volume plan shown before
each run, idle and stop after HTTP 429 or 5xx, one machine at a time, resume):

- moderate: 1.0 s between requests, work for 600 requests then idle for 10 min, daily cap 20,000
  requests or 2,000 MB;
- gentle: 1.0 s, 300 requests then 15 min idle, daily cap 5,000 requests or 500 MB.

The user picked neither and set two values: 1.0 s between requests "accompanied with random wait
from 0.2 to 0.8" s, and 300 requests per work period. The other values come from the moderate
preset, which was the one shown first (assumption: the user's notes edited it).

## Conclusion

[DEC-096](../decisions/DEC-096-epic2-retrieval-path-official-routes-terms-reading-fetch-budget.md)
(accepted): official routes only; R7 listing with the embedding; Roboflow source images from the
R7 `url`; a second dHash on the orientation-applied image; R8 labels per kept image; `like:` and
workspace candidates, measured in TASK-211; Bearer only and `Retry-After`; the user's reading of
terms Q1, Q4, Q5 and Q9; and a fetch budget of 1.0 s plus 0.2 to 0.8 s random wait, 300 requests
then 10 min idle, and a daily cap of 20,000 requests or 2,000 MB.

Board, in the same session: TASK-200 (client) gets the routes, the auth and the fetch budget, and
[TASK-246](../../backlog/tasks/task-246%20-%20Roboflow-client-send-the-API-key-in-the-Authorization-Bearer-header-not-the-api_key-query-parameter-and-wait-Retry-After-on-HTTP-429-official-api.md-findings-F1-F2.md) is archived into it; [TASK-206](../../backlog/tasks/task-206%20-%20Epic-2-datasource-index-keyword-and-similar-project-discovery-partial-image-index-with-np_md5_c3-dHash-embedding-and-image-URL-versioned-index-tables-under-the-scraping-root-synthetic-tests-DEC-081.md) (index step) gets the routes and depends on [TASK-252](../../backlog/tasks/task-252%20-%20Roboflow-fingerprint-step-dHash-also-on-the-EXIF-orientation-applied-image-image-format-from-the-first-bytes-TASK-234.05-finding.md), which
moves to To Do; [TASK-249](../../backlog/tasks/task-249%20-%20Epic-2-Roboflow-version-pick-use-the-Roboflow-versions-augmentation-field-empty-means-unaugmented-and-record-its-resize-step-instead-of-the-closest-image-count-live-finding-of-TASK-234.04.md) (Roboflow version pick) is archived; [TASK-209](../../backlog/tasks/task-209%20-%20Epic-2-store-step-download-the-images-and-labelings-of-what-dedup-kept-to-the-scrape-bucket-or-a-local-folder-under-the-scraping-root-with-a-manifest-resumable-refuses-any-other-destination-synthetic-tests-with-a-fake-S3-DEC-081-DEC-082.md) (store step), TASK-211 and
[TASK-213](../../backlog/tasks/task-213%20-%20Epic-2-dedup-and-store-run-fingerprint-the-project-dataset-images-on-machine01-dedup-the-eligible-Universe-datasources-store-what-is-kept-dataset-style-record-with-counts-licences-and-attribution-DEC-081-outcomes-D3-to-D5.md) (runs) get the volume plan and the one-machine rule; TASK-203 depends on TASK-235 instead of
TASK-200; [TASK-247](../../backlog/tasks/task-247%20-%20Scraping-config-max_pages_per_query-30-exceeds-the-documented-10-page-cap-of-Universe-search-align-the-config-and-the-discover-loop-found-in-TASK-234.06.md) moves to To Do; [TASK-205](../../backlog/tasks/task-205%20-%20Decide-epic-2-licences-and-labelings-allowed-Universe-licences-how-attribution-is-kept-which-export-format-is-stored-DIS-041-open-questions-4-and-5.md) gets a note.

## Open questions

- With `dedup_unit` set to `image`, the index step fetches every image for its fingerprints, and the
  store step fetches the kept ones again, since the index decodes images in memory only ([DEC-081](../decisions/DEC-081-epic2-mission-roboflow-universe-ultrasound-scraper.md)).
  Whether the store step may reuse bytes from the index step instead is for TASK-203.
- Terms Q6 (missing licence) and Q7 (non-commercial use, `BY-NC-SA 4.0`) stay with TASK-205.
- The unknowns of README section 6 stay open; none blocks the code tasks.
