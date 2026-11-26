---
id: DEC-123
title: One status page per research epic under research_notes/epics/ - the scope of an epic session limits what it changes, not what it reads; relations between epics written on the page; generated task blocks; per-step commits and pushes of a member's own branch so another member can take a task over (/handover, /pickup)
status: accepted
area: [workflow]
created: 2026-11-26
from: [DIS-070]
related: [DEC-028, DEC-032, DEC-054, DEC-072, DEC-093, DEC-094, DEC-098, DEC-104]
superseded_by:
---
# DEC-123: Epic status pages and hand-over between members

## Context

The status of a research epic lives only in dated hand-over notes in `journal/` (for epic 3, the
spot liver diseases epic of [DEC-100](DEC-100-epic3-mission-spot-liver-diseases.md): the note of
2026-11-26), with no rule for keeping it current. Board milestones do not match epics (epic 1 and
epic 3 tasks are both under m-1), and only epic 2 tasks carry an epic label (`epic2`). A session
limited to one epic has no fixed place to start reading, and a session of one epic guessed that
another epic serves it. When a member (e.g. dev01) stops in the middle of a task (rest, usage
limit), another member (e.g. dev02) cannot reach the work: the branch is local, and every push other
than the shared master needs a go-ahead ([DEC-098](DEC-098-shared-master-on-gogs.md), the shared
master on Gogs, point 4).

## Decision

1. **One status page per research epic** (location: choice 3 of [DIS-070](../discussions/DIS-070-epic-status-pages-and-hand-over-between-members.md)): `research_notes/epics/epic<N>-<topic>.md`, the same name
   as the epic's terms file in `docs/glossary/` ([DEC-072](DEC-072-term-scopes-global-glossary-and-epic-terms-files.md),
   term scopes). Sections, in this order: Header (state: planned, ongoing, paused or complete; last
   updated, date and session; mission DEC; terms file; board label) · Goal and bar · Serves and uses ·
   Points · Tasks (generated) · Active work (generated) · Next · Open issues · Scope map.
2. **The scope of an epic session.** A session the user limits to epic N ("scope: epic N") starts at
   that epic's page and reads in the order of its scope map (mission DEC, accepted DECs of the epic,
   dataset records, terms file, code and configs). The scope limits what the session **changes**:
   epic N's tasks, records and page, and the files its task lists (`touches`). It may **read**
   anything in the repo and the records, and the web as today. A change outside the scope needs
   the user's ok. The patient-data rules are unchanged.
3. **Relations between epics are written, never guessed.** "Serves and uses" names the other epics
   this one serves or draws on, with links to their pages. A session that thinks there is a relation
   the page does not name reports it as an open question and does not act on it.
4. **Who writes what.** Only `/consult` edits the hand-written sections (Header state, Goal and bar,
   Serves and uses, Points, Next, Open issues, Scope map), when a discussion of the epic concludes or
   a DEC of the epic is accepted. Sessions do not edit the page to report progress: a task's progress
   stays in its board notes, on its branch. A script writes the Tasks and Active work blocks between
   marker lines, from the board, the ID ledger's claims and the branches; `/consult` and `/lead` run
   it at their start and end.
5. **Board label per epic.** Every task of an epic carries the label `epic<N>`, as epic 2 already
   does. The script selects tasks by that label.
6. **Conflicts on the page** (choice 2 of DIS-070). A git conflict only inside the generated blocks is fixed by taking
   either side and running the script again; this is an exception to DEC-098 point 3 (an agent never
   resolves a conflict alone). Any other conflict on the page goes to the member, as DEC-098 says.
7. **A hand-over is always current** (the push without a go-ahead: choice 1 of DIS-070). Each step of a task's implementation plan ends with a commit
   on the task's branch, and its board note says what was done, the next step, open questions and
   anything left uncommitted. Then the branch is pushed to Gogs: a plain push (no `--force`) of the
   member's own `claude/<handle>/*` branch to the `gogs` remote needs no go-ahead (an exception to
   DEC-098 point 4 and command-policy A4, through a new command-policy rule).
8. **`/handover TASK-NNN`** (the member who stops, when there is time): writes a hand-over note on
   the task (state, next step, how to check the work so far), commits, pushes, and releases the
   task's claim in the ID ledger ([DEC-093](DEC-093-id-ledger-number-reservations-task-claims-offline-modes.md),
   point 6). Without it, the last step commit and note are the hand-over.
9. **`/pickup TASK-NNN`** (the member who takes over): fetches the branch, makes a worktree for it
   with a new `scripts/worktree.sh adopt <branch>`, takes the claim (`release --force` of a claim
   left by the other member, then `claim`), reads the task notes and the epic page, and continues
   from the next step. The branch keeps its name (with the first member's handle); notes from then
   on carry the new member's handle ([DEC-094](DEC-094-member-handle-in-branch-and-agent-names.md),
   handle in branch and agent names), and a note records the take-over.
10. **Journal notes stay dated logs.** A hand-over note in `journal/` links to the epic page instead
    of repeating its status.

The user accepted this decision on 2026-11-26 with the three defaults of DIS-070: the push of a
member's own branch needs no go-ahead (point 7), a conflict only inside the generated blocks is fixed
by running the script again (point 6), and the pages live in `research_notes/epics/` (point 1).

## Consequences

- Board tasks (DIS-070): epic pages for epics 1, 2 and 3 (epic 4 once its mission DEC, `DEC-117` reserved by dev02 and not yet in these notes, is merged); epic
  labels on existing tasks; the status script with synthetic tests; `worktree.sh adopt` with the
  `/handover` and `/pickup` skills; CLAUDE.md, `docs/README.md`, `docs/workflow.md`,
  `docs/agents.md` and the command-policy entry (guard files: the user merges).
- Points 6 and 7 take effect when the CLAUDE.md lines and the command-policy entry are in place;
  until then DEC-098 points 3 and 4 and A4 hold.
- Amends DEC-098 (points 3 and 4, as above) and [DEC-032](DEC-032-agent-roster-consult-and-lead-skills.md) (agents and skills: two new skills; `/consult`
  and `/lead` run the status script).
- Own branches on Gogs become visible to every member; they hold code and board text only (the
  patient-data rules already keep data, file names and identifiers out of commits).
