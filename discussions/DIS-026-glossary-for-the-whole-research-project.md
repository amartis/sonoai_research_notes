---
id: DIS-026
title: One glossary for the whole research project, not only the labeling product
status: concluded
created: 2026-11-12
outcomes: [DEC-057]
related: [DEC-056, DEC-040, DEC-032, DEC-021]
---
# DIS-026: One glossary for the whole research project, not only the labeling product

## Question

The user wants a glossary index for the whole research project. `docs/glossary.md`
([DEC-056](../decisions/DEC-056-labeling-terminology-single-glossary.md), proposed) covers
only the labeling product (labeled data). The user proposed a folder
`research-project-wiki/` with a README (scope), `glossary-index.md` and `.xlsx`,
`articles/` (one per concept), `topics/<topic>/<topic>-glossary.md` linking to articles,
and a `glossary-lookup/` (term, topic, other wordings), and asked whether a glossary
agent should review docs before they are written. The user asked for advice and wants to
keep it simple.

## Options considered

- **A: widen `docs/glossary.md`** into the glossary of the research project: one index
  table (term, topic, one-line meaning, other names, link to where it is explained),
  topic sections, and the existing "other names" table as the lookup. Articles are the
  docs that already exist (`docs/medical/`, `training-concepts.md`, `labeling.md`, DEC
  records). Pros: one place, no copies; `docs/` with its context map
  (`docs/README.md`, [DEC-040](../decisions/DEC-040-context-map-and-decision-areas.md)) already works as the wiki. Cons: the file grows; a topic
  moves to its own file when it gets too long to scan.
- **B: a `docs/glossary/` folder** now, with an index and one file per topic. Pros: room
  to grow. Cons: more files and links to keep in step while there are few terms.
- **C: the proposed `research-project-wiki/` tree.** Pros: full structure from the start.
  Cons: a second home next to `docs/` for the same knowledge (drift); `articles/` would
  copy existing docs; "project" in the name clashes with **labeling project**, the term
  DEC-056 fixed.

For review of terms:

- **Reviewer check** (chosen): add a terms check to the existing `reviewer` agent, run
  on branches that add or change docs, records or task text.
- **Glossary agent**: a new agent that revises docs before writing. Would win if words
  keep drifting after the reviewer check is in place. Cost: one more agent to spawn and
  maintain.

## Conclusion

The user accepted the recommended defaults on 2026-11-12 ("ok"):

1. Option A, recorded as [DEC-057](../decisions/DEC-057-glossary-for-the-whole-research-project.md),
   which supersedes DEC-056 and keeps its labeling names and rules.
2. No new glossary agent; a terms check in the `reviewer` agent (DEC-057).
3. First fill: collect only terms the existing docs already define, for datasets,
   training, medical, workflow and records, and infra, each with a one-line meaning and a
   link; no new definitions.

The `.xlsx` copy of the index is made by the user when wanted; the `.md` stays the source
(CLAUDE.md rule). Board tasks carry the work (see DEC-057 Consequences).

## Open questions

- When to move a topic section to its own file: left to judgement ("too long to scan"),
  not a fixed line count.
