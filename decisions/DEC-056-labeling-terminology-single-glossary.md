---
id: DEC-056
title: One glossary fixes the names of the labeling product; older docs keep their words and the glossary maps them
status: superseded
area: [labeling, datasets]
created: 2026-11-12
from: []
related: [DEC-002, DEC-021, DEC-044, DEC-045]
superseded_by: DEC-057
---
# DEC-056: One glossary fixes the names of the labeling product; older docs keep their words and the glossary maps them

## Context

The terms for the labeled data were defined in five places ([DEC-002](DEC-002-dataset-files-structure.md), label-guide.md,
task-design-261023.md, training-concepts.md, CLAUDE.md), each for its own part, with
clashes: "region" meant both an image region across projects and an outline type, "crop"
stood for a labeling task or a sample, and "task" for a labeling task, a training task or
a board task. The user asked on 2026-11-12 for fixed terminology to make communication
clearer, with one glossary, and gave the concepts.

## Decision

- `docs/glossary.md` is the single glossary for the labeling product. Its nine core terms
  (user's concepts): **labeling project**, **tag group**, **tag**, **label**, **image**,
  **sample**, **labeling task**, **labeling group**, **labeling**, with a class diagram
  (Mermaid) and the key and table of each. The user accepted the names on 2026-11-12.
- New docs, records, board tasks and replies use these names. "Labeling task" is written in
  full; "task" alone means a board task. [DEC-044](DEC-044-cirrhosis-sample-set-quality-filter-and-split.md)'s "group" is called **datasource group**.
- Older docs and records keep their wording; the glossary's "Other names" table maps their
  words to the terms. Their Terms sections link to the glossary. Rejected: rewriting older
  docs (records are not rewritten, and column names such as `label` and `taskcrops_df`
  stay fixed).
- A new term, or a changed meaning, goes into the glossary first.

## Consequences

- Context map (`docs/README.md`) lists the glossary for every area.
- Open, not decided here: a table mapping tags to labels (today labels are matched by tag
  name), and one sample key for all code (sample files key on image hash + crop box, the
  choice check on file path + region index).
