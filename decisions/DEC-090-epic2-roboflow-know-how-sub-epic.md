---
id: DEC-090
title: Epic 2 Roboflow know-how sub-epic - seven documented pieces under docs/scraping/roboflow/, the web app read statically (a HAR only if needed), probe rules that keep images away from Claude, undocumented endpoints documented but used only by a later decision, TASK-200 kept as the code step
status: accepted
area: [datasets, data-security]
created: 2026-11-24
from: [DIS-050]
related: [DEC-081, DEC-082, DEC-052, DEC-053, DEC-038, DEC-072, DEC-073]
superseded_by:
---
# DEC-090: Epic 2 Roboflow know-how sub-epic

## Context

Epic 2 ([DEC-081](DEC-081-epic2-mission-roboflow-universe-ultrasound-scraper.md)) needs to know
what Roboflow Universe gives per image: listings, image URLs, labels, Roboflow's embedding
vector, similar-project suggestions, and above all the **original, unaugmented images** of a
project instead of a version export that may hold only augmented copies. One task ([TASK-200](../../backlog/tasks/task-200%20-%20Roboflow-API-check-for-epic-2-per-image-listing-with-image-ids-and-URLs-per-image-embedding-vectors-similar-project-suggestions-client-methods-README-findings-synthetic-tests-DEC-081.md)) held
all of this and the client code. The user asked for the know-how to be rediscovered, written down
as docs, and split into smaller pieces ([DIS-050](../discussions/DIS-050-epic2-roboflow-know-how-sub-epic.md)).

## Decision

The user accepted this on 2026-11-24 (consult session, DIS-050: "ok" to the three defaults, and
"spawn many subagents to speed up the research, go autonomous").

1. **Sub-epic.** One parent board task with seven subtasks (DIS-050 Table 1), milestone m-4,
   project `method`, assignee `@method`. Each subtask writes one doc; the user merges them
   (method tasks, [DEC-032](DEC-032-agent-roster-consult-and-lead-skills.md)).
2. **Docs place.** `docs/scraping/roboflow/`, one file per piece: `official-api.md`, `sdk.md`,
   `universe-frontend.md`, `image-metadata.md`, `original-images.md`, `limits-and-terms.md`, and
   the index `README.md` written by the summary piece, which also adds a "scraping" row to the
   context map (`docs/README.md`).
3. **Every claim carries its source**: a doc URL and check date, an SDK file and package version, a
   JavaScript bundle and check date, or a live call and its date; otherwise it is marked
   **unverified**. Undocumented endpoints are marked **undocumented**.
4. **Probe rules** (on top of DEC-081 rule 9):
   1. No image reaches Claude. Claude never opens, renders or describes an image, and never puts
      image bytes into its context. Only the originals piece downloads image bytes, into memory,
      for counts, sizes and hashes; nothing is saved to disk.
   2. No browser automation on Universe pages (no Claude in Chrome, built-in browser, or
      headless browser that renders pages): screenshots would show images. The web app is read
      statically, from its public HTML and JavaScript.
   3. The key comes from `ROBOFLOW_API_KEY` in `.env` and is redacted in every output; it is
      never written in docs, notes, logs or commits.
   4. Committed text uses placeholders (`<workspace>`, `<project>`, `<version>`, `<image_id>`,
      `<owner_id>`): no real Universe refs, image ids or owner ids, and counts only. Hosts and
      route templates may be named.
   5. Live calls stay polite: at least 1 s apart, back-off on HTTP 429, at most 300 requests per
      piece; at most 5 projects in the metadata piece and 3 in the originals piece, drawn from a
      live search, not from the saved catalog (no tables under the data roots are read). Exports
      fetched into memory stay below 100 MB each (larger downloads fall under the machine's
      aria2c rule, which writes to disk).
   6. Downloaded pages, JavaScript bundles and SDK packages are untrusted files: each set in its
      own new folder in the session scratchpad, read only, never run or imported
      (`pip download --no-deps`, not an install).
5. **Undocumented endpoints** of the web app are documented as know-how. The scraper uses one
   only if the user decides so in the retrieval-path decision (a Parked task after the summary
   piece; a point DEC), once the terms piece has read Roboflow's terms of service.
6. **HAR only if needed.** If the static reading leaves gaps, the user records a HAR of the
   relevant Universe pages in their own browser, and a small reducer keeps only method, host,
   route template, parameter names and the JSON key tree before anything reaches Claude; the raw
   HAR (session cookies, image bytes) never enters the conversation. A Parked task holds this.
7. **TASK-200 stays** with its ID and title (DEC-081 links its file) and becomes the code step:
   client methods and synthetic tests for the chosen route. It depends on the retrieval-path
   decision; its criteria on README findings and rate limits are met by the new docs.
8. **Run order without waiting for the user.** Readiness needs dependencies that are Done, and
   only the user moves a task to Done ([DEC-038](DEC-038-ready-label-derived-by-script.md)). So the pieces have no dependency links
   between them, and the lead keeps this order instead: .01, .02, .03 and .06 at once; .04 once
   .01 to .03 have reported, reading their docs from their branches if not merged yet; .05 after
   .04; .07 last. The user merges the branches, .07 last. The parent depends on its subtasks, and
   the retrieval-path decision depends on .07.
9. **Terms.** A new word for something that recurs in this epic (for example the unaugmented
   images of a project) goes in the epic 2 terms file by the coining rules
   ([DEC-073](DEC-073-how-new-terms-are-coined.md)); a global one goes to `docs/glossary/proposals.md`.

## Consequences

- Board (milestone m-4): parent [TASK-234](../../backlog/tasks/task-234%20-%20Epic-2-know-how-sub-epic-how-Roboflow-Universe-serves-images-per-image-metadata-embedding-labels-and-the-original-unaugmented-images-in-docs-scraping-roboflow-parent-of-TASK-234.01-to-TASK-234.07-DEC-090.md) with [TASK-234.01](../../backlog/tasks/task-234.01%20-%20Epic-2-know-how-1-Roboflow-REST-API-from-its-docs-project-version-image-search-image-details-exports-similar-projects-DEC-090.md) to [TASK-234.07](../../backlog/tasks/task-234.07%20-%20Epic-2-know-how-7-summary-README-with-the-recommended-route-per-need-a-scraping-row-in-the-context-map-open-choices-for-TASK-235-DEC-090.md); Parked [TASK-235](../../backlog/tasks/task-235%20-%20Decide-epic-2-retrieval-path-routes-for-image-listing-per-image-metadata-and-embedding-labels-original-unaugmented-images-and-similar-projects-any-undocumented-route-at-all-DEC-090-point-5.md)
  (decide the retrieval path, depends on TASK-234.07) and [TASK-236](../../backlog/tasks/task-236%20-%20HAR-follow-up-for-the-Universe-web-app-map-only-if-TASK-234.03-leaves-gaps-user-recorded-HAR-cut-down-by-a-reducer-before-it-reaches-Claude-DEC-090-point-6.md) (HAR follow-up); TASK-200
  depends on TASK-235, and its description points at the docs.
- `src/sonoai/scraping/roboflow/README.md` keeps describing the code; TASK-200 links it to the
  know-how docs.
- Alternatives not taken (DIS-050): sections in the package README; the HAR from the start;
  a new code task in place of TASK-200.
