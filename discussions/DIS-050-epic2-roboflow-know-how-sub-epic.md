---
id: DIS-050
title: Epic 2 Roboflow know-how - how Universe serves images, per-image metadata, labels and the original unaugmented images, split into small documented pieces
status: concluded
created: 2026-11-24
outcomes: [DEC-090]
related: [DEC-081, DEC-082, DEC-052, DEC-053, DEC-072, DEC-073, DIS-041]
---
# DIS-050: Epic 2 Roboflow know-how sub-epic

## Question

The user, for epic 2 ([DEC-081](../decisions/DEC-081-epic2-mission-roboflow-universe-ultrasound-scraper.md)):
build the know-how around Roboflow Universe scraping and write it down as docs. From the user's
earlier experience, not only the images can be fetched from Universe but also per-sample metadata
(such as Roboflow's embedding vector) and the labels, by understanding how the Universe web pages
talk to the backend and by using the official API and SDK. Universe projects are versioned, and
some projects have only augmented versions, which the user does not want: there is a way to get
the original, unaugmented images instead of a version export. Getting those originals is a major
goal. The whole effort is too large for one task: break it into smaller pieces.

## What exists

- [TASK-200](../../backlog/tasks/task-200%20-%20Roboflow-API-check-for-epic-2-per-image-listing-with-image-ids-and-URLs-per-image-embedding-vectors-similar-project-suggestions-client-methods-README-findings-synthetic-tests-DEC-081.md)
  is one task for the whole check (per-image listing, embeddings, similar-project suggestions) and
  the client code; every later epic 2 task waits on it.
- The existing `fingerprint` step reads one version export per project and picks the version whose
  image count is closest to the project's raw count, to avoid augmented copies. That is a guess
  from counts, not a way to the originals.
- Claude's working picture of the API (image search, image details with an embedding field, source
  image URLs) is from memory and **unverified**; checking it is the first pieces' job.

## Options considered

**Q1. Where the know-how docs go.**

- **A (chosen): `docs/scraping/roboflow/`, one file per piece plus an index README**, and a
  "scraping" row in the context map (`docs/README.md`). Pieces edit different files, so they can
  run at once; know-how is not code documentation.
- B: sections of `src/sonoai/scraping/roboflow/README.md`. Everything next to the code, but every
  piece edits one file, so the pieces run one at a time.

**Q2. How the web pages' backend calls are studied.**

- **A (chosen): static reading by the agent** of the public Universe HTML and JavaScript (no
  browser, no login), and only if gaps remain, a HAR file the user records in their own browser,
  cut down by a small script to method, route, parameter names and the JSON key tree before
  anything reaches Claude (a Parked follow-up). No image reaches Claude this way. A browser driven
  by Claude would take screenshots of image pages, which DEC-081 rule 9.1 forbids. A raw HAR holds
  the user's session cookies and the image bytes, so it never enters the conversation.
- B: the HAR from the start. Would win if the bundles are too minified to read or the routes are
  built at run time.

**Q3. What happens to TASK-200.**

- **A (chosen): keep its ID and title, and make it the code step** after the know-how: it depends
  on the summary piece and on a new decision task about the retrieval path; its criteria on README
  findings and rate limits point at the new docs. DEC-081 links its file by name, and a new title
  would rename the file and break that link.
- B: archive it and make a new code task, at the cost of a fixed link in DEC-081.

**Undocumented endpoints.** Claude said once: calling the web app's undocumented backend
endpoints may breach Roboflow's terms of service (unverified until the terms piece reads them).
Agreed: those calls are documented as know-how; the scraper uses them only if the user decides so
in the retrieval-path decision.

## The pieces

| # | Piece | Doc | Builds on |
|---|---|---|---|
| .01 | Official REST API, from the docs only | `official-api.md` | - |
| .02 | Python SDK source map (read, never run) | `sdk.md` | - |
| .03 | Universe web app map, static reading | `universe-frontend.md` | - |
| .04 | Live check of per-image metadata on a few public projects (JSON key trees only, no image bytes) | `image-metadata.md` | .01 to .03 |
| .05 | Original unaugmented images: tell augmented versions apart, fetch the source images, compare with a version export in memory (counts only) | `original-images.md` | .04 |
| .06 | Limits, terms and licences | `limits-and-terms.md` | - |
| .07 | Summary: index README with the recommended route per need, context-map row | `README.md` | .01 to .06 |

Table 1. The know-how pieces, subtasks of one parent task (milestone m-4).

## Conclusion

The user accepted all three defaults ("ok", 2026-11-24) and asked for the research to run
autonomously with many agents in parallel.

- [DEC-090](../decisions/DEC-090-epic2-roboflow-know-how-sub-epic.md) (accepted): the sub-epic,
  its docs place, how the web app is studied, the probe rules, TASK-200 as the code step, and the
  run order.
- Board: parent [TASK-234](../../backlog/tasks/task-234%20-%20Epic-2-know-how-sub-epic-how-Roboflow-Universe-serves-images-per-image-metadata-embedding-labels-and-the-original-unaugmented-images-in-docs-scraping-roboflow-parent-of-TASK-234.01-to-TASK-234.07-DEC-090.md) with subtasks [TASK-234.01](../../backlog/tasks/task-234.01%20-%20Epic-2-know-how-1-Roboflow-REST-API-from-its-docs-project-version-image-search-image-details-exports-similar-projects-DEC-090.md) to [TASK-234.07](../../backlog/tasks/task-234.07%20-%20Epic-2-know-how-7-summary-README-with-the-recommended-route-per-need-a-scraping-row-in-the-context-map-open-choices-for-TASK-235-DEC-090.md); Parked
  [TASK-235](../../backlog/tasks/task-235%20-%20Decide-epic-2-retrieval-path-routes-for-image-listing-per-image-metadata-and-embedding-labels-original-unaugmented-images-and-similar-projects-any-undocumented-route-at-all-DEC-090-point-5.md) (decide the retrieval path) and [TASK-236](../../backlog/archive/tasks/task-236%20-%20HAR-follow-up-for-the-Universe-web-app-map-only-if-TASK-234.03-leaves-gaps-user-recorded-HAR-cut-down-by-a-reducer-before-it-reaches-Claude-DEC-090-point-6.md) (HAR follow-up, only if needed); TASK-200 now
  depends on TASK-235.

## Open questions

1. The retrieval path the scraper uses for listing, metadata, embeddings, labels and originals
   (TASK-235, after the summary piece).
2. Whether a HAR is needed (TASK-236, only if the static reading leaves gaps).

## Later (2026-11-25)

The seven pieces were written and reviewed (TASK-234.01 to TASK-234.07, branches waiting for the
user's merge). The user then decided:

1. **No HAR.** Open question 2 is closed: TASK-236 is archived. The documented API covers every
   need except similar-project suggestions, the Terms of Use exclude reverse engineering of the
   web app (section 4(a)), and `robots.txt` disallows the pages a HAR would record. [TASK-234.03](../../backlog/tasks/task-234.03%20-%20Epic-2-know-how-3-Universe-web-app-map-from-its-public-HTML-and-JavaScript-backend-routes-behind-each-view-auth-no-browser-no-images-DEC-090.md)
   keeps its criteria 1 and 2 unmet; the web app routes stay unread.
2. **Deviations accepted.** [TASK-234.04](../../backlog/tasks/task-234.04%20-%20Epic-2-know-how-4-live-check-of-per-image-metadata-on-up-to-5-public-projects-listing-image-details-labels-embedding-similar-projects-no-image-bytes-DEC-090.md) contacted a sixth Universe project with 2 read calls,
   against the cap of 5 in DEC-090 point 4.5; its results are not used. [TASK-234.05](../../backlog/tasks/task-234.05%20-%20Epic-2-know-how-5-original-unaugmented-images-spot-augmented-versions-fetch-a-projects-source-images-compare-in-memory-with-a-version-export-DEC-090.md) kept the
   Universe refs of its three check projects in a scratchpad file during its runs and deleted
   it, read against DEC-090 point 4.1 as covering image bytes and exports only. Both are recorded
   in the task notes.
3. **The retrieval path** (open question 1) stays with TASK-235, to be decided in a later consult
   session from the choices C1 to C8 of the summary README.
