---
id: DIS-061
title: Reminders for references - when a pointer to a record, a numbered point, a list label or a term needs a few words of what it is, and coined names a returning reader can read
status: concluded
created: 2026-11-25
outcomes: [DEC-106]
related: [DIS-053, DEC-095, DEC-021, DEC-073, DIS-035]
---
# DIS-061: Reminders for references to records, points and terms

## Question

The user reads tasks, decisions, discussions and session prompts between other missions and
does not keep their context in mind. Texts written by Claude point to things defined elsewhere
with a bare label, and the user has to open several files to understand one word. The user
gave two examples (2026-11-25):

- a message said "the real score is point 4 (metrics), not yet decided". It should have said
  "point 4 (metrics) of [DEC-065](../decisions/DEC-065-mission-upper-abdomen-anatomy-segmentation.md)"
  (the mission of Epic 1, upper-abdomen anatomy segmentation);
- `literature/ssl-generative-anatomy-priors-study.md` (a study of self-supervised and
  generative anatomy priors) says "the candidate changes C7 to C13 continue the C1 to C6 of
  [DIS-052](DIS-052-epic1-next-recipes-after-six-seed0-runs.md)". A reader needs to be told what DIS-052 is (the discussion of the next Epic 1 training
  recipes) and what C1 to C6 are (its six candidate changes to recipe R4).

The user set the rule: add a description beside the word when the object was not mentioned in
the last 5 sentences, or appears for the first time in the document or prompt; the writer
chooses the length, but it must identify the object in the project. The user also asked to
improve the coining rules, so that terms stay readable for someone who comes back from another
mission.

## Findings

- [DEC-095](../decisions/DEC-095-writing-to-the-user-section-in-claude-md.md) (the "Writing to
  the user" section of `CLAUDE.md`) covers task and record IDs, but only in messages to the user.
  Records, docs, task text and prompts are not covered, nor are point numbers or list labels.
- [DEC-021](../decisions/DEC-021-communication-and-research-writing-standards.md) (communication
  and writing standards) and `docs/writing.md` only ask to define abbreviations at first use.
- [DEC-073](../decisions/DEC-073-how-new-terms-are-coined.md) (how new terms are coined) point 2
  bans names whose meaning comes only from order ("first", "second", "new"), but letter-and-number
  labels (C7, R8, W3, P5, rule IDs such as L8) are not named. Recent records use many of them
  across records: DIS-052 alone defines R, W, P and C labels, and [DEC-096](../decisions/DEC-096-epic2-retrieval-path-official-routes-terms-reading-fetch-budget.md) (the Epic 2 retrieval
  path) carries R7 and R8 in its title.
- The reviewer agent's writing check covers only experiment and dataset records; its terms
  check has no test for letter-and-number names.

## Options considered

- **A: a reminder rule for all text, plus coining additions** (the user's rule as stated, applied
  to messages, records, docs, task text and prompts; short bold names for numbered points;
  letter-and-number labels only inside their own list; a returning-reader test for coined names;
  the reviewer checks it). It covers both examples. The cost is slightly longer texts and a few
  more reviewer findings.
- **B: the reminder rule for messages to the user only**, by extending DEC-095. Smaller, but the
  user's second example is a document, not a message, so it leaves half the problem.
- **C: no rule; fix the two examples by hand.** No lasting effect.

## Conclusion

The user took A ("ok", 2026-11-25):
[DEC-106](../decisions/DEC-106-references-carry-a-reminder-and-coined-names-pass-a-returning-reader-test.md)
is accepted. Board task TASK-275 (reference reminders and the returning-reader test written into
`CLAUDE.md`, `docs/writing.md`, `docs/glossary/README.md` and the reviewer agent) carries it.

The user also said yes to the two open questions:

- the reminder rule goes into the user-level `~/.claude/CLAUDE.md` as well (2 lines, done in
  this session), so it applies in the user's other projects;
- TASK-275 also fixes the passage of the second example in
  `literature/ssl-generative-anatomy-priors-study.md` (the study of self-supervised and
  generative anatomy priors). This is a one-off exception to DEC-106 rule 10 (existing text
  keeps its words); no other older text is rewritten.

## Open questions

None.
