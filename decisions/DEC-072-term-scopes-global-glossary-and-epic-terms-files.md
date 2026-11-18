---
id: DEC-072
title: Term scopes - a global glossary and one terms file per research epic, under docs/glossary/
status: accepted
area: [workflow]
created: 2026-11-18
from: [DIS-035]
related: [DEC-057, DEC-056, DEC-065, DEC-073]
superseded_by:
---
# DEC-072: Term scopes - a global glossary and one terms file per research epic

## Context

[DEC-057](DEC-057-glossary-for-the-whole-research-project.md) made `docs/glossary.md` the one
glossary of the whole project, and the reviewer's terms check asks for a row for every new
term. Most new terms belong to one research epic, so the glossary grows with words few readers
need, and each terms review files another glossary task
([DIS-035](../discussions/DIS-035-term-scope-and-coining.md)).

## Decision

1. **Two scopes.**
   - A **global term** is used outside one research epic: in another epic's records, in a
     general doc (labeling, datasets, workflow, infra), or in code that more than one epic uses.
     Work that belongs to no research epic also uses global terms. The user may also ask for a
     term to be global.
   - An **epic term** is used only inside one research epic (one mission DEC and the records,
     tasks, runs and code that carry it).
   - A word needed only inside one board task is defined in that task's text and has no row
     anywhere.
2. **Files, under `docs/glossary/`.**
   - `global-glossary.md`: today's `docs/glossary.md`, moved, with its content unchanged apart
     from relative links. A short `docs/glossary.md` stays behind and points to the new
     place, so links in older records and tasks keep working.
   - One terms file per research epic, named `epic<N>-<mission topic>.md`; Epic 1 is
     `epic1-upper-abdomen-anatomy.md` ([DEC-065](DEC-065-mission-upper-abdomen-anatomy-segmentation.md)).
     One table: Term · Meaning · Other names · Defined in (the record or doc).
   - `README.md`: which file holds what, the scope test (point 1) and the coining rules
     ([DEC-073](DEC-073-how-new-terms-are-coined.md)).
   - DEC-057's rule that a long topic section may move to its own file still holds, inside
     this folder.
3. **No collision.** An epic term never reuses a global term with another meaning. If the word
   is taken, the epic term gets another name, or its row says what it is not.
4. **Promotion.** When an epic term starts to be used outside its epic, it moves to the global
   glossary; the epic file keeps a row that links there.
5. **Reviewer terms check.** "A new term with no glossary row" becomes "a new term defined
   neither in the global glossary nor in the terms file of its epic". Two more should-fix
   findings: an epic term that collides with a global term, and an epic term used outside
   its epic (promote it).

## Consequences

- Amends DEC-057: the one glossary becomes the global glossary plus epic terms files. The
  rest of DEC-057 (topics, other-names table, no glossary agent) stands.
- Board tasks: move the file and create the README and the Epic 1 terms file; update the
  reviewer agent and `/lead` (guard files: the user merges).
- Filling the Epic 1 terms file, and re-sorting the terms of the open glossary tasks, waits for
  DEC-073 (deferred by the user).
