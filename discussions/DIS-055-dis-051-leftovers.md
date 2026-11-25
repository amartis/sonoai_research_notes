---
id: DIS-055
title: Leftovers of DIS-051 - follow-up tasks of the multi-member work, table versions on rerun, how members share master
status: concluded
created: 2026-11-25
outcomes: [DEC-097, DEC-098]
related: [DIS-051, DEC-014, DEC-028, DEC-053, DEC-078, DEC-091, DEC-092, DEC-093, DEC-094]
---
# DIS-055: Leftovers of DIS-051

## Question

The user asked which tasks of [DIS-051](DIS-051-multi-member-work-without-conflicts.md) (several
team members working at once) are left, and to settle the ones that need a discussion.

## Facts checked

- All nine tasks DIS-051 created ([TASK-237](../../backlog/tasks/task-237%20-%20Member-handle-SONOAI_MEMBER-in-.env-one-checked-helper-and-the-members-table-in-team.md-DEC-091.md) to [TASK-245](../../backlog/tasks/task-245%20-%20research_notes-a-merge-never-needs-a-hand-resolved-INDEX.md-regenerate-it-with-build_index.py-instead.md)) were Done. Their agents left six follow-up
  tasks in Triage (TASK-250, 251, 253 to 256) and one-time steps for the user: seeding the ID ledger,
  the command-policy entry L7 for ledger pushes, the one-time move of the flat logs and runs into
  `dev01/`, and the INDEX.md merge setup per clone.
- Two older Triage tasks of [DEC-078](../decisions/DEC-078-team-roles-trusted-workstations-data-root-over-smb3.md) overlapped: TASK-187 (a GPU box folder per person, done by
  [TASK-243](../../backlog/tasks/task-243%20-%20GPU-box-one-box-folder-per-member-handle-and-a-one-run-lock-so-members-do-not-overwrite-each-others-code-or-share-the-GPU-at-once.md)) and TASK-188 (number clashes, done by [DEC-093](../decisions/DEC-093-id-ledger-number-reservations-task-claims-offline-modes.md), and the push workflow, still open).
- The `gpu` tool folder is not under git, and `gpu` loads the committed `.gpu.env` as bash, so a check
  there also runs under an old copy of the tool.
- `master` tracked GitHub `origin`; `docs/onboarding.md` said Gogs was loopback-only and to use
  GitHub only, while the ID ledger lives on Gogs.
- `task-create` stops when the board is 10 or more task numbers behind the ledger
  (`scripts/reserve_id.py`), so members must take in each other's work regularly.

## Options considered

**A rerun of a table writer (TASK-250, TASK-251).**

- **A new version per rerun, readers take the highest** (chosen,
  [DEC-097](../decisions/DEC-097-rerun-writes-a-new-table-version.md)): one rule, already used by
  sample files; nothing is lost.
- **label-summary refuses a rerun unless `--overwrite` is given by name**: one fixed report name, but
  the old content is lost when used.

**Rolling out the `gpu` tool (TASK-256).**

- **Its own git repo on Gogs, plus a version check in `.gpu.env`** (chosen; no DEC, a tooling
  choice recorded in the task): one source, updated with `git pull`; the check stops stale copies.
- **Move it into this repo**: wins only if no other project uses the tool.

**How members share `master` (TASK-188).**

- **One `master` per member on the remote (`dev01-master`, `dev02-master`)**: the user's first idea.
  Single writer per branch and no failed pushes, but no shared board or code, and each member merges
  every other member's branch. Dropped by the user: all members need to sync anyway.
- **One shared `master` (and `main`) on Gogs; each member fetches, merges, resolves and pushes; no
  pull requests** (chosen, [DEC-098](../decisions/DEC-098-shared-master-on-gogs.md)).
- Shared remote: **Gogs** (chosen: the ledger is there, it works without internet) or **GitHub
  `origin`** (wins only for work away from the team network).
- Push go-ahead: **keep it for every push**, or **no go-ahead when check.sh passed and the push is
  plain** (chosen by the user).

## Conclusion

The user agreed to DEC-097 and DEC-098 and to this triage:
[TASK-253](../../backlog/tasks/task-253%20-%20GPU-TensorBoard-script-and-services-doc-follow-the-per-member-box-folder.md)
and [TASK-254](../../backlog/tasks/task-254%20-%20exp-agent-doc-tmux-session-name-has-the-member-handle.md)
to To Do; [TASK-255](../../backlog/tasks/task-255%20-%20Clean-up-the-old-shared-box-folder-~-work-ml_research-on-the-GPU-box-user-step.md)
Parked until the user looks at the old box folder;
[TASK-187](../../backlog/archive/tasks/task-187%20-%20GPU-box-a-separate-box-folder-per-person-so-two-machines-do-not-overwrite-each-others-code.md)
archived; [TASK-250](../../backlog/tasks/task-250%20-%20Each-pull-or-import-writes-a-new-versioned-result-table-instead-of-adding-rows-to-the-existing-one-DEC-053.md)
and [TASK-251](../../backlog/tasks/task-251%20-%20label-summary-writes-a-new-version-of-its-csv-and-md-on-a-rerun-instead-of-replacing-them-DEC-053.md)
carry DEC-097; [TASK-256](../../backlog/tasks/task-256%20-%20Roll-out-the-new-gpu-tool-box-folder-per-member-run-lock-to-every-member.md)
the gpu tool choice; [TASK-188](../../backlog/tasks/task-188%20-%20Shared-master-on-Gogs-the-fetch-merge-check-and-push-flow-for-every-member-pushes-without-a-go-ahead-and-a-count-of-unmerged-commits-in-consult-and-lead.md)
and [TASK-022](../../backlog/tasks/task-022%20-%20Gogs-server-docs-docs-infra-gogs.md-and-the-README-setup-for-the-gogs-remote-of-both-repos-DEC-014.md)
carry DEC-098. The user seeded the ID ledger (run by the session at the user's request) and asked for
L7 in the command policy, which was applied. The user then asked the session to lead the ready tasks
on its own and to ask only for important decisions.

## Open questions

- The one-time move of the flat logs and runs into `dev01/` ([DEC-092](../decisions/DEC-092-logs-and-runs-one-folder-per-member-handle.md) point 6) and the INDEX.md merge
  setup on each clone are still the user's steps.
