---
id: DIS-051
title: Several team members working at once without conflicts - member handles, logs and runs per handle, an ID ledger for record and task numbers, task claims, offline numbering, handles in branch and agent names
status: concluded
created: 2026-11-24
outcomes: [DEC-091, DEC-092, DEC-093, DEC-094]
related: [DEC-014, DEC-026, DEC-028, DEC-032, DEC-038, DEC-053, DEC-072, DEC-073, DEC-078, DEC-089]
---
# DIS-051: Several team members working at once without conflicts

## Question

`docs/onboarding.md` already sets up a second team member (a senior on machine01-senior,
[DEC-078](../decisions/DEC-078-team-roles-trusted-workstations-data-root-over-smb3.md)). The user
asked how several team members can work at the same time without conflicts: an identifier per
person, a team table, private areas in the shared `logs/` and `runs/`, and no clashes between record
and task numbers (DIS, DEC, EXP, TASK) when each member, and each worktree session, creates them.

## Facts checked

- `logs/` and `runs/` of machine01-host are mounted on machine01-senior over SMB 3.1.1 with
  encryption (`seal`), next to the data root. The logs share holds five flat files and two folders,
  one of them already named after a member; the runs share holds 12 run folders at its top level.
- Two modules use a fixed `logs/` path: the aws action-log writer (`sonoai.cloud.labelstud`) and the
  exp run-log reader (`sonoai.tracking.pending`).
- [DEC-089](../decisions/DEC-089-logs-folder-own-git-repo.md) (logs/ as its own git repo, one file
  per workstation) was never carried out: its task, [TASK-231](../../backlog/archive/tasks/task-231%20-%20logs-as-its-own-git-repo-DEC-089-one-log-file-per-workstation-a-setup-script-and-the-logs-repos-own-privacy-hook.md), is still To Do.
- `SONOAI_MACHINE` already exists: it names a machine profile for training (`ws`, `gpubox`,
  `runpod_a100`), not a person. `SONOAI_ACTOR` names an agent. Neither identifies a team member.
- DIS, DEC and EXP records are committed on `main` of `research_notes/` directly, not on worktree
  branches. Board tasks are created on worktree branches of the code repo.
- The board CLI picks task numbers itself: `backlog task create` has no option to set the number.
  `backlog/config.yml` has `check_active_branches: true` (local branches of the last 30 days) and
  `remote_operations: false` (it does not look at remote branches).
- Gogs ([DEC-014](../decisions/DEC-014-gogs-git-remote.md)) listens only on loopback of
  machine01-host today. The user will open it to the team's workstations and set up the `gogs`
  remote; that work is outside this discussion.
- The GPU box has one folder for the project (`GPU_PROJECT=ml_research` in `.gpu.env`), synced with
  `rsync --delete`, and one GPU.

## Options considered

**Name for the person and their identifier.**

- **Team member, with a member handle** (chosen). "Team member" is the existing wording of
  `team.md` and `onboarding.md`; the handle is a short identifier, by default the Linux user name.
- **Contributor, with a contributor id** (the user's first wording): a second word for the same
  person next to "team member".

**Where the handle is stored.**

- **`SONOAI_MEMBER` in `.env`** (chosen): already gitignored, per machine, linked into every
  worktree and read by code and hooks. Tools check it against the team table.
- **A gitignored `WHOAMI.md`**: needs parsing and is one more personal file to copy.

**Layout of `logs/` and `runs/`.**

- **One folder per handle, `logs/<handle>/` and `runs/<handle>/`** (chosen). One rule for both
  shares: write only in your own folder, read all. Over SMB it also prevents two machines appending
  to one file. Readers read `logs/*/<log>`.
- **One file per member inside each log type** (DEC-089's layout, e.g. `exp-runs/<member>.md`):
  same single-writer property for logs, but a different layout from `runs/`. Kept only while
  DEC-089 stood; the user dropped DEC-089.
- **A `shared/` folder next to the handle folders** (the user's first sketch): dropped, because a
  folder with several writers brings back the conflict. Text the whole team needs goes into a
  committed repo.

**Avoiding clashes between record and task numbers.**

- **Fetch every branch, take the highest number, create, push at once** (the user's first sketch):
  misses unpushed local branches of other members and deleted branches (whose numbers would be
  reused), still races between fetch and push, and pushes unfinished worktree branches.
- **An ID ledger** (chosen): an append-only list on its own branch on Gogs, one line per reserved
  number. A script fetches only that branch, appends the next numbers, commits and pushes; git
  refuses a push that would drop another member's newer line, so the script fetches again and
  retries. Files are then written on any branch and pushed whenever.
- **Numbers per member** (`DEC-dev01-001`) or **number blocks per member**: no network, but they
  break the existing ID form and its tools.

**Doing the work in a hook or a script.** A script does the network work (fetch, push, retry); a
hook only checks, without network, that a new record file uses a number reserved by this member.
A hook that fetched and pushed would run on every matching call, be slow, and push unseen.

**Two `/lead` sessions picking the same ready task.** Board status lives on branches, so a second
member's board still shows a task as To Do after the first member's lead has started it. A claim
line in the ID ledger, written before an agent is spawned, settles who works on it; `ready_tasks.py`
leaves claimed tasks out.

**When Gogs cannot be reached.** The user wants to choose whether the local environment issues
numbers itself. Modes: ask (default), stock (numbers reserved earlier while online), local
(provisional numbers, checked and renumbered on reconnect), tmp (temporary ids), stop.

**Branch and agent names.** `claude/<topic>` would clash between members on one remote; the handle
goes into the branch name and into the places where an agent name leaves the machine.

## Terms decided ([DEC-073](../decisions/DEC-073-how-new-terms-are-coined.md) point 4)

- **Member handle** (global, accepted): a team member's short identifier, e.g. `dev01`. Passes 1a
  (in `.env`, folder names under `logs/` and `runs/`, branch and agent names, the ledger), 1b (no
  term exists; `SONOAI_MACHINE` and the agent name mean other things), 1c (replaces "the team
  member's short identifier"). Other name considered: contributor id.
- **ID ledger** (global, accepted): the append-only list on the `id-ledger` branch on Gogs that
  reserves record and task numbers and holds task claims. Passes 1a (scripts, hooks, skills, docs),
  1b, 1c (replaces "the reservation list on the id-ledger branch"). Other name considered:
  reservation list.
- Task claim, provisional number and number stock: descriptive words, no terms.

## Conclusion

The user agreed to:
- member handles and a team table that the team lead or a senior edits
  ([DEC-091](../decisions/DEC-091-member-handles-and-team-table.md)); handles `dev01` (team lead)
  and `dev02` (senior);
- `logs/<handle>/` and `runs/<handle>/` on the shares, superseding DEC-089
  ([DEC-092](../decisions/DEC-092-logs-and-runs-one-folder-per-member-handle.md));
- the ID ledger with task claims and a choice of offline modes
  ([DEC-093](../decisions/DEC-093-id-ledger-number-reservations-task-claims-offline-modes.md));
- the handle in branch and agent names
  ([DEC-094](../decisions/DEC-094-member-handle-in-branch-and-agent-names.md)).

Board tasks carry the decisions: [TASK-237](../../backlog/tasks/task-237%20-%20Member-handle-SONOAI_MEMBER-in-.env-one-checked-helper-and-the-members-table-in-team.md-DEC-091.md) (DEC-091), [TASK-238](../../backlog/tasks/task-238%20-%20logs-handle-and-runs-handle-on-the-shares-roots-from-.env-and-a-one-time-move-script-DEC-092.md) (DEC-092), [TASK-239](../../backlog/tasks/task-239%20-%20ID-ledger-script-scripts-reserve_id.py-reserves-record-and-task-numbers-claims-tasks-stocks-numbers-and-handles-the-offline-modes-DEC-093.md), [TASK-240](../../backlog/tasks/task-240%20-%20ID-checks-a-hook-that-denies-unreserved-record-numbers-a-duplicate-ID-check-a-pre-push-check-for-provisional-numbers-and-the-command-policy-entry-for-ledger-pushes-DEC-093.md) and
[TASK-241](../../backlog/tasks/task-241%20-%20consult-and-lead-use-the-ID-ledger-reserve-numbers-before-writing-records-and-tasks-claim-before-spawning-ready_tasks.py-leaves-claimed-tasks-out-DEC-093.md) (DEC-093), [TASK-242](../../backlog/tasks/task-242%20-%20Member-handle-in-branch-and-agent-names-claude-handle-topic-SONOAI_ACTOR-and-note-prefix-handle-name-DEC-094.md) (DEC-094). TASK-231 (DEC-089) is archived. Three side
points became small tasks without a DEC: a GPU box folder per handle with a one-run lock ([TASK-243](../../backlog/tasks/task-243%20-%20GPU-box-one-box-folder-per-member-handle-and-a-one-run-lock-so-members-do-not-overwrite-each-others-code-or-share-the-GPU-at-once.md)),
table writers that refuse an existing file under `derived/` ([TASK-244](../../backlog/tasks/task-244%20-%20Table-writers-refuse-to-overwrite-an-existing-table-under-derived-DEC-053-now-that-members-write-to-the-shared-data-root.md), [DEC-053](../decisions/DEC-053-table-naming-and-preservation.md)), and `INDEX.md` merges that
regenerate the file instead of resolving it by hand ([TASK-245](../../backlog/tasks/task-245%20-%20research_notes-a-merge-never-needs-a-hand-resolved-INDEX.md-regenerate-it-with-build_index.py-instead.md)).

## Open questions

- Whether the board CLI, with `remote_operations: true`, takes remote branches into account when it
  picks the next task number: checked in TASK-239.
- Until the ledger runs, numbers are still taken from the local checkout; this discussion's own
  numbers were taken that way. While this discussion ran, another consult session
  cited three task numbers in its records before creating the tasks; this session's tasks waited
  until those existed, so the board CLI did not hand out the same numbers.
