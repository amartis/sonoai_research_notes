---
id: DIS-070
title: Epic status pages and hand-over between members - one page per research epic as status board and starting point of an epic session, the scope rule, edits by several sessions, and taking over a task from another member
status: concluded
created: 2026-11-26
outcomes: [DEC-123]
related: [DEC-028, DEC-032, DEC-054, DEC-072, DEC-093, DEC-094, DEC-098, DEC-100]
---
# DIS-070: Epic status pages and hand-over between members

## Question

Where does the status of a research epic live, so that it is always current (ongoing, paused or
complete), and so that a session the user limits to "epic N" has one place to start reading? And how
does a member (e.g. dev01) who stops in the middle of a task (rest, usage limit) hand the work to
another member (e.g. dev02)?

Why now: on 2026-11-26 the status of epic 3 (spot liver diseases,
[DEC-100](../decisions/DEC-100-epic3-mission-spot-liver-diseases.md)) was kept by adding a section to
that day's hand-over note in `journal/`, which no rule asks for. Within hours the note was out of
date again: [DIS-067](DIS-067-epic3-model-and-optimisation.md) and [DEC-115](../decisions/DEC-115-epic3-model-balancing-loss-augmentation-precision-length.md) (epic 3 model and optimisation) and [DIS-068](DIS-068-shift-test-fit-scale-contrast-mean-grid-name.md) and [DEC-116](../decisions/DEC-116-shift-test-fit-scale-levels-on-crop-pixels-grid-name-kept.md) (brightness
shift test of fit-scale runs) were concluded after it. A session of epic 4 (public ultrasound
datasets; its mission `DEC-117` is reserved by dev02 and not yet in these notes) read epics 1 and 3
and guessed that epic 4 serves them.

## Options considered

Where the status lives:

- **A. Keep dated hand-over notes in `journal/`.** Nothing new. But each note goes stale, a reader
  must find the latest one, and nothing says who updates it.
- **B. One page per epic in `research_notes/epics/`** (chosen, choice 3 below). Sessions may edit
  `research_notes/` in the main checkout without a worktree (the main-checkout guard, [DEC-054](../decisions/DEC-054-main-checkout-guard-hook.md)), and
  the page sits beside the records it links to.
- **C. One page per epic in `docs/epics/`.** Changes would be reviewed and merged like code, so
  the page would change less freely. Better if review matters more than speed.

What the scope of an epic session limits:

- **Reads and changes** (the first proposal): a session reads only what the page's scope map links
  to. The user pointed out that it would stop epic 4 from reading epics 1 and 3, and asked whether
  web reading would need approval.
- **Changes only** (chosen): the session reads anything, the web included, as today; it changes only
  its epic's tasks, records and page and the files its task lists. Relations between epics are
  written on the page, so a session does not need to guess them.

How the page stays current when several sessions end at once:

- **Each session edits the page**: conflicts between members on the same lines through Gogs (the
  shared git server).
- **Sessions do not edit it; a script writes the task blocks, only `/consult` writes the rest**
  (chosen). Progress stays in each task's board notes on its own branch. The one conflict left, in
  the generated blocks, is fixed by running the script again (choice 2 below). Two sessions on one
  machine are already safe: the edit tool refuses a write to a file that changed after it was read.

How a task moves to another member:

- **A hand-over note written at the end**: lost when a usage limit stops the session without
  warning.
- **A commit and a push at the end of each plan step** (chosen), with `/handover` when there is time
  and `/pickup` for the member who takes over. The push of a member's own branch needs no go-ahead
  (choice 1 below); otherwise the work stays on the first member's workstation until they approve
  a push.

## Conclusion

The user liked the plan as a whole and raised four points: epic 4 reading other epics, web reading,
several sessions editing the page at once, and hand-over between members. The answers are in
[DEC-123](../decisions/DEC-123-epic-status-pages-scope-rule-and-hand-over.md) (proposed), points 2 and 3
(scope and relations between epics), 4 to 6 (who writes the page, conflicts) and 7 to 9 (hand-over).
The user accepted DEC-123 on 2026-11-26 with the three defaults below; the board tasks are listed under Board tasks.

Three choices for the user to confirm, each with its default:

1. A plain push of a member's own `claude/<handle>/*` branch to Gogs needs no go-ahead. Default:
   yes. With no, a hand-over works only after a push the member approved.
2. A git conflict only inside the generated blocks of a page is fixed by running the script again.
   Default: yes. With no, [DEC-098](../decisions/DEC-098-shared-master-on-gogs.md) point 3 stays strict and such a conflict goes to the member.
3. The pages live in `research_notes/epics/`. Default: yes. The alternative is `docs/epics/`,
   reviewed and merged like code.

## Board tasks

Created on 2026-11-26 from DEC-123: [TASK-302](../../backlog/tasks/task-302%20-%20Epic-status-script-the-Tasks-and-Active-work-blocks-of-an-epic-page-from-the-board-the-ID-ledger-claims-and-the-branches-between-marker-lines-synthetic-tests-DEC-123.md) (status script for the generated blocks), [TASK-303](../../backlog/tasks/task-303%20-%20Hand-over-between-members-scripts-worktree.sh-adopt-branch-the-handover-and-pickup-skills-the-task-claim-moved-in-the-ID-ledger-DEC-123.md) (`worktree.sh adopt`, `/handover` and
`/pickup`), [TASK-304](../../backlog/tasks/task-304%20-%20Rules-for-DEC-123-CLAUDE.md-scope-line-and-per-step-commit-and-push-command-policy-rule-for-the-push-of-a-members-own-branch-conflict-exception-for-generated-blocks-docs-and-skill-updates.md) (rules in CLAUDE.md, the command policy and the docs; waits for TASK-302 and
TASK-303; the user merges), [TASK-305](../../backlog/tasks/task-305%20-%20Epic-status-pages-for-epics-1-2-and-3-in-research_notes-epics-from-their-records-and-the-board-epic-3-from-the-2026-11-26-hand-over-note-brought-up-to-date-DEC-123.md) (pages for epics 1 to 3; waits for TASK-302) and [TASK-306](../../backlog/tasks/task-306%20-%20Board-labels-epic1-and-epic3-on-the-existing-tasks-of-epics-1-and-3-DEC-123-point-5.md) (labels
`epic1` and `epic3` on existing tasks).

## Open questions

- The epic 4 page waits until `DEC-117` (epic 4 mission, public ultrasound datasets) is merged into
  these notes.
- Whether a `/epic N` skill is worth having once the "scope: epic N" line has been used for a while.
- The hand-over note of 2026-11-26 for epic 3 has a section "Update, later on 2026-11-26"; it is
  already behind (it still names the model and optimisation consult as next). Its content, brought up
  to date, moves to the epic 3 page.
