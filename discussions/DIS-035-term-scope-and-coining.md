---
id: DIS-035
title: Term scope (global or research epic) and how new terms are coined
status: concluded
created: 2026-11-18
outcomes: [DEC-072, DEC-073]
related: [DEC-057, DEC-056, DEC-065, DEC-069, DEC-071]
---
# DIS-035: Term scope (global or research epic) and how new terms are coined

## Question

Raised by the user on [TASK-165](../../backlog/tasks/task-165%20-%20Glossary-rows-for-the-Epic-1-candidate-terms-pair-kind-first-set-candidate-exclusion-flag-DEC-069-DEC-057.md) (glossary rows for the Epic 1 candidate terms): most new
terms belong to one board task or one research epic. Putting every one of them into the
project glossary is not efficient and confuses readers. Do terms have a scope?

Finding: they did not. [DEC-057](../decisions/DEC-057-glossary-for-the-whole-research-project.md)
has one scope (the whole project), and the reviewer's terms check makes every new term
without a glossary row a should-fix finding. On 2026-11-18 the board held 12 glossary tasks,
10 of them open, and `docs/glossary.md` had 423 lines. The six terms of TASK-165 and [TASK-172](../../backlog/tasks/task-172%20-%20Glossary-rows-for-first-set-and-organ-state-DEC-066-DEC-070-from-the-TASK-159-terms-review.md)
(pair kind, first set, candidate, exclusion flag, organ state) were already defined in
[DEC-066](../decisions/DEC-066-epic1-model-task-label-set-softmax.md), [DEC-069](../decisions/DEC-069-epic1-data-preparation.md), [DEC-070](../decisions/DEC-070-anatomy-label-set-task-states-in-sample-file.md) or `docs/datasets/styles/derived.md`.

The user then widened the question: how are new terms coined? Names should be descriptive and
specific ("first set" is too general); conciseness must not cost meaning; and a new term or
concept should be introduced only when it has unique value over descriptive words.

## Options considered

- **Scope.**
  - **A, one glossary for every term** (DEC-057 as it is): one place to look; but it grows with
    each epic and mixes short-lived epic words with project words.
  - **B, two scopes, global and epic** (chosen): project words in a global glossary; epic words
    in that epic's own terms file. The reviewer still catches a word that collides with a global
    term.
- **Home of an epic term.**
  - **B1, in the record that introduces it**: no new file; but Epic 1 already spreads about 20
    terms over DEC-066, DEC-069, DEC-070, [DEC-071](../decisions/DEC-071-epic1-splitting-parameterised-split-method.md) and derived.md.
  - **B2, one terms file per research epic** (the user's choice): one place to read an epic's
    words, next to the global glossary under `docs/glossary/`.
- **Coining.**
  - **C1, no rule** (as now): writers name concepts as they go; the glossary records them after.
  - **C2, a screen and naming rules before a term exists** (proposed in DEC-073).

## Conclusion

- [DEC-072](../decisions/DEC-072-term-scopes-global-glossary-and-epic-terms-files.md)
  (accepted, the user said yes to B and chose B2): global glossary at
  `docs/glossary/global-glossary.md`, one terms file per research epic in the same folder.
- [DEC-073](../decisions/DEC-073-how-new-terms-are-coined.md) (accepted 2026-11-18): the screen and the
  naming rules for new terms.
- Harvesting the terms of the open glossary tasks is deferred by the user until the policy is
  settled; it becomes one Parked board task.

## Open questions

- None. The user accepted DEC-073 on 2026-11-18.
