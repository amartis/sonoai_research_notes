---
id: DEC-057
title: One glossary for the whole research project in docs/glossary.md, checked by the reviewer agent
status: accepted
area: [workflow, labeling, datasets, training]
created: 2026-11-12
from: [DIS-026]
related: [DEC-056, DEC-040, DEC-032, DEC-021]
superseded_by:
---
# DEC-057: One glossary for the whole research project in docs/glossary.md, checked by the reviewer agent

## Context

[DEC-056](DEC-056-labeling-terminology-single-glossary.md) made `docs/glossary.md` the single
glossary of the labeling product. The user wants one glossary index for the whole research
project, and asked whether a wiki folder and a glossary agent are needed
([DIS-026](../discussions/DIS-026-glossary-for-the-whole-research-project.md)).

## Decision

- `docs/glossary.md` becomes the glossary of the whole research project (title
  "Glossary: research project"). It has:
  - a scope line;
  - one index table: **Term · Topic · Meaning (one line) · Other names · Read more**
    (link to the doc or record that explains it);
  - topic sections: labeling product (DEC-056's content, unchanged), datasets,
    training, medical, workflow and records, infra;
  - the "other names in existing docs" table, which is the lookup of other wordings.
- Articles are the existing docs (`docs/medical/`, `training-concepts.md`, `labeling.md`,
  DEC records). A new article is written only for a term with no home, in its area's
  folder. No separate wiki folder, `articles/` or `glossary-lookup/`.
- A topic section moves to `docs/glossary/<topic>.md` when it gets too long to scan;
  its index rows stay in `docs/glossary.md`.
- The `.md` is the source; the user makes an `.xlsx` copy when wanted.
- DEC-056's rules carry over to the whole project: its nine labeling names stand; new
  docs, records, tasks and replies use glossary names; older docs keep their words and
  the glossary maps them; a new term or changed meaning goes into the glossary first.
- No glossary agent. The `reviewer` agent gets a terms check: new or changed docs,
  records and task text use glossary names; a new term is in the glossary; an old word
  is mapped in the other-names table. `/lead` runs it on branches that add or change
  docs, records or task text.

## Consequences

- Supersedes DEC-056 (which stays as the record of the labeling names).
- Board tasks: widen and fill the glossary from terms already defined in existing docs
  (no new definitions); add the terms check to the reviewer agent and `/lead`. The
  second changes guard files (agents, skills), so it waits for the user's merge.
- Reopen with a glossary agent if words keep drifting after the reviewer check is in place.
