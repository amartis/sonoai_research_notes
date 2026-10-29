---
id: DEC-021
title: Communication rules for Claude, a research-writing standard, and links between notes made by the index tool
status: accepted
created: 2026-10-28
from: [DIS-006]
related: [DEC-009, DEC-011]
superseded_by:
---
# DEC-021: Communication rules for Claude, a research-writing standard, and links between notes made by the index tool

## Context

Sessions started from Claude's default style: long replies, code without
context, bare paths and IDs, and questions about small choices. Notes did not
link to each other, and the EXP template had no place for n, confidence
intervals or a baseline. The user wants communication that respects their
time and keeps the quality of joint decisions, and research outputs that meet
the standards of SCI-indexed journals. [DIS-006](../discussions/DIS-006-human-friendly-communication.md).

## Decision

1. **Communication rules** live in the user-level `~/.claude/CLAUDE.md`
   (outside any repo; applies to every project). That file is the source of
   the rule text; in short:
   - Answer, result or request first; then only what is needed to act or to
     trust it; longer material in a linked file or page. One screen by default.
   - Status as done and verified (how) / done, not verified / not done /
     needs you. Every reply stands alone. Plain English, terms defined at
     first use, one name per thing.
   - Code blocks get a title line (what, where as a file:line link, what to
     look at); commands get a line on what they do and whether they change
     anything; numbers come with units, n, a comparison and a 95% CI when there
     is one.
   - Every file, record, task, run or commit is a link, except anything the
     patient-data rules protect.
   - Claude decides reversible, low-stakes, in-task choices and reports them.
     It asks about hard-to-reverse ones (data, labels, splits, metrics,
     departures from a DEC) as question, recommendation, reasons, best
     alternative, cost to reverse; at most three questions, each with a default.
   - Confidence is stated and assumptions marked; no citation from memory
     without verification.
2. **Research-writing standard** in `docs/writing.md` for EXP records,
   dataset records, figures, tables, reports and slides (not chat or code
   docs), based on CLAIM 2024, STARD 2015 / STARD-AI and TRIPOD+AI.
   `CLAUDE.md` links it; it is not `@`-imported, so sessions that write no
   research output do not load it.
3. **EXP template** gets n, 95% CI and baseline columns and a short reporting
   checklist drawn from those guidelines.
4. **Links between notes** are made by `research_notes/tools/build_index.py`:
   the first bare mention of an ID in a note becomes a relative link,
   `INDEX.md` shows its link columns as links, and `--check` fails on
   unlinked IDs ([TASK-038](../../backlog/tasks/task-038%20-%20Auto-link-record-IDs-and-add-backlinks-in-build_index.py-DEC-021.md)).
5. **Review on 2026-11-11**: rules that changed no reply are cut (an
   amendment here); if the rules are not followed from `CLAUDE.md`, a custom
   output style is considered in a new DEC.

## Consequences

- Shorter replies and fewer questions; each remaining question carries a
  recommendation and a default.
- EXP records and figures are closer to what a journal submission needs, at
  the cost of a little more writing per experiment.
- `~/.claude/CLAUDE.md` is not under version control; changes to its rules
  are recorded here (amendment or new DEC).
- One more document to keep current (`docs/writing.md`), edited in place per
  [DEC-011](DEC-011-docs-vs-research-notes.md).
