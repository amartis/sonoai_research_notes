---
id: DEC-095
title: A "Writing to the user" section in the project's CLAUDE.md - no made-up labels for choices, internal words explained, IDs with titles, questions that stand alone; lead and consult skills write to the user in plain words (amends DEC-021)
status: accepted
area: [workflow]
created: 2026-11-24
from: [DIS-053]
related: [DEC-021, DEC-032, DEC-078]
superseded_by:
---
# DEC-095: Writing to the user, in the project's CLAUDE.md

## Context

The communication rules of [DEC-021](DEC-021-communication-and-research-writing-standards.md)
point 1 live in the user-level `~/.claude/CLAUDE.md`. That file was missing on machine01 until
2026-11-24, and it never reached other team members' workstations. A lead message then asked the
user to choose "go to five" without saying what five counted, and used internal words with no
meaning given ([DIS-053](../discussions/DIS-053-plain-words-in-messages-to-the-user.md)).

## Decision

1. **The user-level file stays** the source for the general rules (DEC-021 point 1), as the user
   restored it on 2026-11-24.
2. **The project's `CLAUDE.md` gets a short "Writing to the user" section** (about 10 lines), so
   that every session, agent and team member loads it. It points to the user-level file for the
   general rules and adds these:
   - **No made-up labels for choices.** Each option is written out in full, so it makes sense to
     someone who read nothing else (not "go to five", but "let a fifth agent start now, one over
     the limit of four").
   - **No internal words without a meaning**, or plain words instead: "agent", not "writer";
     "files it changes", not "touches"; "3 of 4 checks met", not "AC 3/4".
   - **A task or record ID always comes with a few words of what it is**, e.g. "[TASK-237](../../backlog/tasks/task-237%20-%20Member-handle-SONOAI_MEMBER-in-.env-one-checked-helper-and-the-members-table-in-team.md-DEC-091.md) (member
     handle)".
   - **A question to the user restates what it is about**, so it stands alone.
3. **The lead and consult skills** write their "needs the user" and report steps in plain words
   under point 2, and drop the `AC 5/5, DoD 2/2` model.
4. Agents' reports to the lead are not messages to the user and keep their own format, but the
   lead rewrites what it passes on under point 2.

## Consequences

- One board task edits `CLAUDE.md` and the two skill files. `CLAUDE.md` is a guard file, so the
  user approves the merge ([DEC-032](DEC-032-agent-roster-consult-and-lead-skills.md)).
- Amends DEC-021 point 1: the rules are now in two places, the general ones user-level and the
  four above in the project. If they disagree, the project's `CLAUDE.md` wins in this repo.
- Reversal: cheap; a text edit.
