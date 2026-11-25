---
id: DIS-053
title: Plain words in messages to the user - no made-up labels for choices, internal words explained, the rules loaded in every session
status: concluded
created: 2026-11-24
outcomes: [DEC-095]
related: [DEC-021, DIS-006, DEC-032, DEC-078]
---
# DIS-053: Plain words in messages to the user

## Question

A lead session asked the user to choose between "wait" and "go to five". The user could not
tell what "five" meant: the lead meant "let a fifth agent run at once, one over the limit
of four". The same message used internal words with no meaning given ("writers", "touches",
"derived ready labels"). Why did this happen when [DEC-021](../decisions/DEC-021-communication-and-research-writing-standards.md) already asks for plain words, and
how do we stop it?

## Findings

- DEC-021 point 1 keeps the communication rules in the user-level `~/.claude/CLAUDE.md`. That
  file did not exist on machine01 when this discussion started, so sessions were not loading
  those rules. The user put it back during the discussion.
- The rules only ever lived on one workstation. Agents get them only through that file, and other
  team members ([DEC-078](../decisions/DEC-078-team-roles-trusted-workstations-data-root-over-smb3.md)) have their own user-level files.
- The lead and consult skills invite shorthand in what they write to the user. The lead's
  "needs the user" step gives `AC 5/5, DoD 2/2` as its model.

## Options considered

- **A: only restore the user-level file.** No other change. It fixes the missing file, but the
  rules still reach only this workstation, and the made-up label is not covered by any rule.
- **B: a short "Writing to the user" section in the project's `CLAUDE.md`, plus plain-word
  steps in the lead and consult skills.** Every session and agent loads `CLAUDE.md`, it is under
  version control, and every member gets it. The cost is a few more lines in `CLAUDE.md`.
- **C: keep the rules in mind for this session only.** No work, but the next session forgets.

## Conclusion

The user took B ("ok" to all three recommendations) and also restored the user-level file:
[DEC-095](../decisions/DEC-095-writing-to-the-user-section-in-claude-md.md). A board task
writes the section and the skill steps. `CLAUDE.md` is a guard file, so the user approves
that merge.

The user also allowed a fifth agent, as a one-off exception to the limit of four agents
at once ([DEC-032](../decisions/DEC-032-agent-roster-consult-and-lead-skills.md)), so that [TASK-237](../../backlog/tasks/task-237%20-%20Member-handle-SONOAI_MEMBER-in-.env-one-checked-helper-and-the-members-table-in-team.md-DEC-091.md) (member handle) could start next to the four
[TASK-234](../../backlog/tasks/task-234%20-%20Epic-2-know-how-sub-epic-how-Roboflow-Universe-serves-images-per-image-metadata-embedding-labels-and-the-original-unaugmented-images-in-docs-scraping-roboflow-parent-of-TASK-234.01-to-TASK-234.07-DEC-090.md) (Roboflow know-how) agents. The limit itself is unchanged.

## Open questions

None.
