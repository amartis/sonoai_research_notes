---
id: DEC-073
title: How new terms are coined - descriptive words first, a three-part screen before a new term, and names that are descriptive and specific
status: proposed
area: [workflow]
created: 2026-11-18
from: [DIS-035]
related: [DEC-057, DEC-072, DEC-021]
superseded_by:
---
# DEC-073: How new terms are coined

## Context

Terms were coined freely while work went on, and the glossary recorded them later. Some names
are short but say little: "first set" means the four organ classes the Epic 1 anatomy model
predicts, but the name says neither "organ" nor "class". The user wants names that are
descriptive and specific: concise, but never at the cost of meaning. The user also wants a
new term or concept introduced only when it has unique value over descriptive words
([DIS-035](../discussions/DIS-035-term-scope-and-coining.md)).

## Decision

1. **Descriptive words first.** Say the concept in plain words built from existing terms,
   e.g. "the organ classes of the anatomy model". Coin a term only when all three hold:
   - a. **It recurs**: the concept is needed in more than one record or doc, or as a code,
     column or config name.
   - b. **It has unique value**: no global or epic term, standard term of the field (cited), or
     plain phrase already says it.
   - c. **A phrase does not work**: the descriptive phrase would be long or unclear each time
     it is used.
2. **A coined name is descriptive and specific.** A reader who sees the name alone can guess
   what kind of thing it is and what it belongs to.
   - The head noun names the kind of thing: classes, samples, table, column, rate, flag.
   - A qualifier names what it belongs to or is about: organ, anatomy model, split, detector.
   - A generic word is never the whole name: set, kind, state, flag, candidate, item, group,
     unit, pair, type.
   - No names whose meaning comes only from history or order ("first", "second", "new").
   - Concise, but not shorter than the meaning needs: a longer clear name beats a short vague
     one.
3. **No collision.** A new name does not reuse a global or epic term, or a common term of ML
   or medicine, with another meaning.
4. **Who decides.**
   - A **global term** is chosen with the user (in `/consult`). The proposal gives the name, how
     it passes 1a-c, the phrase it replaces, and one other name considered.
   - An **epic term** may be coined by the writer of the record or doc that needs it. The writer
     adds the row to the epic terms file ([DEC-072](DEC-072-term-scopes-global-glossary-and-epic-terms-files.md))
     and names the new term in their report. The reviewer's terms check tests it against
     points 1-3.
5. **Code identifiers are not terms.** Functions, columns and config keys follow code style and
   may be short. Prose uses the term or descriptive words, and quotes an identifier in
   backticks.
6. **Existing terms** keep their words until a harvest pass applies points 1-3 to them. For
   each term the pass decides one of three outcomes: keep it, rename it (the old name goes
   into "Other names"), or replace it with descriptive words. The user approves the result.

## Consequences

- The reviewer's terms check gets the screen (point 1), the naming rules (point 2) and the
  collision rule (point 3) as should-fix findings on new terms.
- `docs/glossary/README.md` (DEC-072) holds these rules for writers.
- A Parked harvest task covers the terms of the open glossary tasks and the Epic 1 words
  (first set, organ state, candidate, exclusion flag, pair kind and others).
