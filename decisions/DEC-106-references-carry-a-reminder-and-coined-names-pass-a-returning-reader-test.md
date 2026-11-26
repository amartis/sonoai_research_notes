---
id: DEC-106
title: Every reference to something defined elsewhere carries a short reminder of what it is, at its first use in a text and again after 5 sentences without it; numbered points get short names; coined names pass a returning-reader test (amends DEC-021, DEC-073, DEC-095)
status: proposed
area: [workflow]
created: 2026-11-25
from: [DIS-061]
related: [DEC-021, DEC-073, DEC-095, DEC-072, DEC-087]
superseded_by:
---
# DEC-106: References carry a reminder; coined names pass a returning-reader test

## Context

The user works on several missions and comes back to this project without the context an AI
session holds. Two kinds of text lose the user
([DIS-061](../discussions/DIS-061-reminders-for-references-to-records-points-and-terms.md),
the discussion of this rule):

- a bare pointer to a numbered part of another record, such as "the real score is point 4
  (metrics)" without saying it is point 4 of [DEC-065](DEC-065-mission-upper-abdomen-anatomy-segmentation.md)
  (the mission of Epic 1, upper-abdomen anatomy segmentation);
- a range of list labels from another record, such as "the candidate changes C7 to C13 continue
  the C1 to C6 of [DIS-052](../discussions/DIS-052-epic1-next-recipes-after-six-seed0-runs.md)", where the reader must open DIS-052 (the discussion of the next Epic 1
  training recipes) to learn that C1 to C6 are its six candidate changes to recipe R4.

The rules so far do not cover this. [DEC-095](DEC-095-writing-to-the-user-section-in-claude-md.md)
(the "Writing to the user" section of `CLAUDE.md`) asks for a few words with a task or record ID,
but only in messages to the user, and says nothing about point numbers, list labels or terms.
[DEC-021](DEC-021-communication-and-research-writing-standards.md) (communication and research
writing standards) asks to define abbreviations at first use. [DEC-073](DEC-073-how-new-terms-are-coined.md)
(how new terms are coined) bans names that get their meaning only from order ("first", "second"),
but not letter-and-number labels such as C7 or R8.

## Decision

1. **Scope: every text a person may read.** Messages to the user, records (discussion, decision,
   experiment and dataset records), docs, board task text and notes, commit messages, and the
   prompts written for sessions and agents.
2. **What needs a reminder: any pointer to something defined elsewhere.** A record or task ID; a
   numbered or labelled part of a record or doc ("point 4", "rule 6", "option B", "C1 to C6",
   "R7", "W3", a command-policy rule ID such as L8); a section; a run or dataset name; a project
   term or abbreviation; a code name used as a concept.
3. **When: the user's rule.** The reminder is due
   - a. at the first mention in a document, message or prompt (also in its title or a heading);
   - b. when the object was not mentioned in the last 5 sentences. A list item, a table row or a
     heading counts as one sentence.
   In between, the bare name is fine.
4. **How: enough words to tell which thing it is, without opening another file.** The writer
   chooses the length: usually a few words, at most one short clause.
   - A part of a record names its owner and its gist: "point 4 (metrics) of DEC-065 (Epic 1
     mission)", never "point 4 (metrics)" alone.
   - A range names what the items are and, when short, lists them: "C1 to C6 of DIS-052 (the
     six candidate changes to training recipe R4 in the discussion of the next Epic 1 recipes:
     weight averaging, ...)".
   - A record or task ID has its subject: "DEC-073 (how new terms are coined)".
   - A term gets its meaning in a few words or a link to its glossary row.
5. **Numbered points get a short bold name**, so that a pointer can carry it: "1. **Descriptive
   words first.**" lets others write "point 1 (descriptive words first) of DEC-073". New records
   do this; older records keep their form.
6. **Letter-and-number labels are local.** Labels such as C7, R8, P5, W3, option A or B name
   items inside one list or table. Outside that list's own section (and always outside its
   record) each use carries the words of rule 4. Such a label is never a term (DEC-073 point 2).
7. **Coining: a returning-reader test (amends DEC-073 point 2).** A coined name passes when a
   reader who comes back from other work and sees it in one sentence can tell what kind of thing
   it is and which part of the project it belongs to, without opening a file. Also:
   - a name built only from letters, numbers or an abbreviation coined in the project fails;
   - the glossary meaning of a new term starts with its kind ("A table that ...", "The rate
     of ...");
   - a project term at its first use in a text gets its meaning in a few words or a link to its
     glossary row (rule 4), even when the term has a row.
8. **Who checks.** The reviewer's writing check covers rules 3 to 6 in the added and changed
   lines of docs, records, task text and prompts, not only experiment records. The reviewer's
   terms check adds rule 7. Lead and consult sessions apply the rules to what they write to the
   user and to agent prompts.
9. **Where the rules live.** The project's `CLAUDE.md` "Writing to the user" section gets one
   short rule (rules 3 and 4, about 3 lines) that names `docs/writing.md`, since every session
   loads `CLAUDE.md`. `docs/writing.md` gets a "References and reminders" section with rules 1
   to 6 and the two examples above. `docs/glossary/README.md` (the coining rules for writers)
   gets rule 7.
10. **Existing text keeps its words**, like older terms under DEC-073 point 6 (existing terms
    wait for a harvest pass). A writer who edits a passage applies the rules to the lines it
    changes.

## Consequences

- One board task edits `CLAUDE.md`, `docs/writing.md`, `docs/glossary/README.md` and the
  reviewer agent file. `CLAUDE.md` and the agent files are guard files, so the user approves the
  merge ([DEC-032](DEC-032-agent-roster-consult-and-lead-skills.md), the agent roster).
- Amends DEC-095 (the rules now cover all text, not only messages to the user), DEC-021 (point 1,
  first use) and DEC-073 (point 2, naming rules). None is superseded.
- Texts get a little longer. The 5-sentence rule keeps repeats rare.
- Reversal: cheap; a text edit.
