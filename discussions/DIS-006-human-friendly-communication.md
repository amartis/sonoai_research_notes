---
id: DIS-006
title: Human-friendly communication between Claude and the user, research-writing standard, and links between documents
status: concluded
created: 2026-10-28
outcomes: [DEC-021]
related: [DEC-009, DEC-011]
---
# DIS-006: Human-friendly communication between Claude and the user, research-writing standard, and links between documents

## Question

The user asked (2026-10-28) to make Claude sessions and their outputs more
human friendly: start from what people are capable of and fond of, unlike
machines (e.g. code shown with a short title, not bare); follow the
guidelines of SCI-indexed journals where an output calls for it; and link
documents to each other so browsing and reading are not painful. The aim is
efficient and effective communication that respects the user's time and keeps
the quality of the decisions made together.

What the repo showed on that date:

- No DEC body linked to another note; IDs such as DIS-005 were plain text.
  Only the id column of `INDEX.md` had links.
- No user-level `~/.claude/CLAUDE.md` and no custom output style: every
  session started from Claude's defaults.
- The EXP template recorded one `run | metric | value` per row, with no n,
  confidence interval, split or baseline, and no reporting checklist.

## Options considered

The rules start from these human traits:

| Human trait | So Claude should |
|---|---|
| Holds about four things in working memory | Lead with the answer; one decision at a time |
| Skims, reads top-down, once | Headings, bold lead words; the first sentence carries the point |
| Comes back after interruptions | Every reply stands alone, no "as above" |
| Trusts reasons and evidence, not assertions | Say why and how it was checked; mark guesses |
| Attention is the scarcest resource | Ask about hard-to-reverse decisions; decide small ones and report |
| Clicks rather than types paths | Every reference a link |
| Reads code slowly, cannot diff in the head | Code gets a title; say what changed in behaviour |

- **Where the communication rules live**:
  - (A) user-level `~/.claude/CLAUDE.md`: about the user, applies to every
    project, not committed. Chosen.
  - (B) the project `CLAUDE.md`: would only apply here and grow a file every
    session already reads.
  - (C) a custom Claude Code output style: changes the system prompt more
    strongly but is less visible. Kept as the fallback if the plain rules are
    not followed.
- **Research-writing standard**: `@`-imported into `CLAUDE.md` (costs context
  in every session) vs. `docs/writing.md`, linked from `CLAUDE.md` and read
  when writing a research output (chosen; process docs live in `docs/`,
  DEC-011). Journal style in chat was rejected: chat stays conversational,
  rigour goes into the outputs.
- **Reporting guidelines** for this project (diagnostic ultrasound AI):
  CLAIM 2024 (AI in medical imaging), STARD 2015 with its AI extension
  STARD-AI (2025, diagnostic accuracy), TRIPOD+AI (2024, prediction models).
  DOIs verified on 2026-10-28; listed in `docs/writing.md`.
- **Links**: a rule for agents vs. the index tool making them
  (`build_index.py`, enforced by `--check`). The tool was chosen: a tool does
  not forget.
- **Questions to the user**: ask about every choice vs. decide reversible,
  in-task choices and report them in one line, asking only about
  hard-to-reverse ones (data, labels, splits, metrics, departures from a DEC)
  with a recommendation. The second was chosen.
- **Length of the rules**: a full style guide vs. about 45 lines. Each extra
  rule weakens the others, so the short one was chosen, with a review date.

## Conclusion

Agreed with the user on 2026-10-28, with the proposed defaults: the
communication rules apply to all projects; Claude decides reversible in-task
choices and reports them; replies are in English. Carried by DEC-021
(accepted 2026-10-28). Board tasks: TASK-037 (`coord`: user-level rules,
`docs/writing.md`, EXP template) and TASK-038 (`infra`: auto-links and
backlinks in `build_index.py`).

Review on 2026-11-11: cut rules that changed no reply, and decide whether an
output style is needed.

## Open questions

- At the review: are the rules followed well enough from `CLAUDE.md`, or does
  this need an output style (a new DEC)?
