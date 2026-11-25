---
id: DIS-003
title: Project setup structure review (milestone m-0)
status: concluded
created: 2026-10-28
outcomes: [DEC-011, DEC-012, DEC-013, DEC-014, DEC-015, DEC-016]
related: [DIS-002, DEC-002, DEC-007, DEC-008, DEC-009]
---
# DIS-003: Project setup structure review (milestone m-0)

## Question

Milestone m-0 ("Project Setup") asks for a project structure we can be happy
with for the next few months. [DIS-002](DIS-002-workflow-and-folder-structure.md) settled the layout and process
([DEC-008](../decisions/DEC-008-repo-layout.md)..010); this review, with the user (2026-10-27/28), goes through what
is still unclear. Topics settled so far:

1. Should `docs/` move into `research_notes/`?
2. Where do the dataset style docs (`enc1`, `plain`, `submit1`) belong? Today
   they are copies of `{data_files_root}/dataset_styles/<style>.md` in
   `research_notes/datasets/` ([DEC-002](../decisions/DEC-002-dataset-files-structure.md)), and each mixes a format spec with a
   register of the datasets built in that style.
3. Where does the labeling-project tag table of version 261023 belong? It sits
   at the repo root, gitignored. It holds the tags of the labeling projects
   that produced the 261023 label files (label definitions, no patient data),
   and `configs/data/label_projects.yaml` is exported from it.
4. Training code layout: checked against [DEC-006](../decisions/DEC-006-losses-optim-tracking.md), which already fixes the
   `training/`, `evaluation/` and `tracking/` modules and the split of
   metrics between tasks (which metrics, `S`) and `evaluation/` (formulas on
   matrices). Not reopened. The user raised one point: losses and metrics
   overlap, since a Dice-type loss is the same measure as the metric.

## Options considered

- **`docs/` into `research_notes/`**: dropped. `CLAUDE.md` imports
  `@docs/workflow.md`, and `research_notes/` is a separate, gitignored repo
  that is absent on clones, the GPU box and RunPod; docs also change in the
  same commit as the code they describe.
- **Style specs**: (A) leave as DEC-002 has them, only fix the code
  docstrings that cite `research_notes/datasets/plain.md`; (B) split by kind:
  format specs to the code repo, the register per dataset version in notes;
  (C) `research_notes/datasets/styles/`. B chosen: the specs are "how it works
  now" and implemented by code, and C would again point code at a repo that is
  not always there.
- **Losses and metrics**: (A) one set of matrix formulas used by metrics and,
  through a soft confusion matrix, by a new loss `fdsc_ce`, while `dice_ce`
  stays the exact official TransUNet loss; (B) also rebuild `dice_ce` on the
  soft matrix (less code, but no longer the official squared-denominator Dice);
  (C) keep formulas separate as in DEC-006. A chosen.
- **Backups / remote**: neither repo has a remote. (1) bare mirror on
  machine02 via the shared folder; (2) private hosted repos (GitHub); (3) git
  bundles to the user's own storage; (4) a self-hosted git service: Forgejo
  (push mirrors, active), Gitea, or Gogs (lightest, no push mirrors, slow
  security fixes). machine01 is a VM on machine02, so anything on either
  machine shares its hardware. The user chose Gogs on machine01.
- **Results and chosen models**: runs root outside or inside the repo on
  machine01; checkpoints fetched to machine01 or left on the GPU box; chosen
  models as a models folder with a model card or only a cited run ref;
  checkpoint retention. machine01 has ~16 GB free. The user set up a common
  box on machine02 (`D:\codework\ml_research_commonbox`, shared to machine01
  and seen by the GPU box in WSL) for runs, checkpoints and models; metrics
  kept forever, unused weights pruned.
- **Off-machine copy**: everything (working copies, Gogs, the common box) sits
  on machine02's hardware. Targets: encrypted cloud storage (restic, or rclone
  with encryption), an external USB drive, a private GitHub remote (repos
  only), institution storage. Scope: both repos, Gogs data, common box `runs/`
  and `models/` (cited checkpoints), encrypted datasets only if no other copy
  of the source data exists. The user had no preference; recommended restic
  with a daily systemd user timer on machine01. The target needs the user's
  own account or drive, so it is parked.
- **Backlog's empty folders and a notes hook**: the `decisions/`, `docs/`,
  `drafts/` folders are untracked and recreated by the CLI, so deleting them
  is pointless; the risk is using those features. The code repo's hook cannot
  serve the notes (it blocks the [DEC-012](../decisions/DEC-012-dataset-docs-layout.md) tag table and has no `INDEX.md`
  check), so the notes get their own.
- **Tag table**: first read (wrongly) as plaintext patient labels; the user
  clarified it is the label definitions of version 261023, so it is
  documentation of that version and goes into its notes folder.

## Conclusion

Agreed with the user on 2026-10-28:

- [DEC-011](../decisions/DEC-011-docs-vs-research-notes.md): `docs/` (code repo) holds how things work now and is edited in
  place; `research_notes/` holds why and what was found, as dated records that
  are superseded, not rewritten. `docs/` stays in the code repo.
- DEC-012: dataset docs layout. Style specs in `docs/datasets/styles/<style>.md`
  (source of truth); one folder per dataset version in
  `research_notes/datasets/<version>/` with the register (`README.md`) and, for
  261023, the tag table as `label_projects.xlsx` (no "(plain)" in the name);
  the data-root `dataset_styles/` holds copies of the `docs/` specs; no
  `research_notes/datasets/styles/`. `label_projects.yaml` names the version
  it was exported from.
- [DEC-013](../decisions/DEC-013-shared-score-formulas-losses.md): losses reuse the matrix score formulas of
  `evaluation/scores.py` through a soft confusion matrix; new loss `fdsc_ce`
  with the task's `S`; `dice_ce` unchanged and still the default.
- Board (Triage, m-0): [TASK-011](../../backlog/archive/tasks/task-011%20-%20Dataset-style-specs-to-docs-per-version-registers-in-notes-DEC-012.md) (style specs and version registers),
  [TASK-012](../../backlog/archive/tasks/task-012%20-%20Move-the-261023-labeling-project-tag-table-into-its-notes-folder-DEC-012.md) (tag table move and `label_projects.yaml` version).
- The DEC-006 / DEC-013 implementation is development, not project setup: a
  new milestone m-1 "First Training Run" holds [TASK-014](../../backlog/tasks/task-014%20-%20Matrix-score-formulas-for-NumPy-and-torch-matrices-DEC-013.md) (shared score
  formulas), [TASK-015](../../backlog/tasks/task-015%20-%20Losses-registry-dice_ce-dice_ce_per_layer-fdsc_ce-DEC-006-DEC-013.md) (losses), [TASK-016](../../backlog/tasks/task-016%20-%20Optimisation-SGD-and-poly-schedule-gradient-accumulation-DEC-006.md) (optimisation), [TASK-017](../../backlog/tasks/task-017%20-%20Image-level-matrices-and-evaluatetask-model-loader-DEC-006.md)
  (image-level matrices, `evaluate`), [TASK-018](../../backlog/tasks/task-018%20-%20Shared-training-loop-and-segmentation-trainers-DEC-003-DEC-006.md) (shared loop and segmentation
  trainers) and [TASK-019](../../backlog/tasks/task-019%20-%20Run-tracking-to-DEC-006-eval-JSON-runs-index-display-compare_runs-DEC-006.md) (run tracking, runs index, display, `compare_runs`),
  all `method`, in Triage. [TASK-009](../../backlog/tasks/task-009%20-%20Implement-DEC-003-training-recipes-and-plans.md) gets a criterion: trainers are registered
  in `training/`, not in `scripts/train.py`.
- Stray worktrees: four under `.claude/worktrees/` (desktop-app sessions,
  2026-10-27), all fully merged; the only unique content, an uncommitted
  `brief` skill draft, is kept. No new DEC (enforces [DEC-007](../decisions/DEC-007-session-branches-no-worktrees.md)). [TASK-020](../../backlog/tasks/task-020%20-%20Remove-stray-worktrees-and-merged-branches-guard-against-new-ones-DEC-007.md)
  (`infra`, Triage, m-0): move the skill draft to the main checkout, remove the
  worktrees and merged `claude/*` branches, make `scripts/check.sh` fail on
  extra worktrees, and stop hiding `.claude/worktrees/` in `.git/info/exclude`.
  The app has no setting to turn worktrees off for new sessions (only their
  location), so the check is the guard.
- [DEC-015](../decisions/DEC-015-commonbox-runs-models.md): common box on machine02 with `runs/` ($SONOAI_RUNS_ROOT,
  checkpoints included) and `models/` ($SONOAI_MODELS_ROOT,
  `<task name>/<YYMMDD>_<slug>/` with `best.pt` and `model.json`); RunPod
  rsyncs back; prune unused weights after the user confirms; fail clearly when
  a root is missing. Board: [TASK-023](../../backlog/tasks/task-023%20-%20Set-up-the-common-box-for-runs-and-models-on-all-machines-DEC-015.md) (`infra`, m-0, box setup), [TASK-024](../../backlog/tasks/task-024%20-%20MODELS_ROOT-in-sonoai.paths-and-a-clear-error-when-a-results-root-is-missing-DEC-015.md)
  (`method`, m-0, `MODELS_ROOT` and missing-root error), [TASK-025](../../backlog/tasks/task-025%20-%20Promote-and-prune-commands-for-runs-and-chosen-models-DEC-015.md) (`method`,
  m-1, promote / prune), [TASK-026](../../backlog/tasks/task-026%20-%20Update-the-EXP-template-to-full-run-refs-and-DEC-003-recipes-DEC-015.md) (`coord`, m-0, EXP template).
- [DEC-016](../decisions/DEC-016-notes-hook-backlog-features.md): notes pre-commit hook (data and binary types refused except the
  DEC-012 tag table, 1 MB limit, `INDEX.md` check); Backlog's decision, doc
  and draft features are not used. Board: [TASK-028](../../backlog/tasks/task-028%20-%20Pre-commit-hook-for-the-research_notes-repo-DEC-016.md) (`infra`, hook),
  [TASK-029](../../backlog/tasks/task-029%20-%20Workflow-docs-do-not-use-Backlog-decisions-docs-or-drafts-DEC-016.md) (`coord`, workflow rule), both Triage, m-0.
- [DEC-014](../decisions/DEC-014-gogs-git-remote.md): Gogs on machine01, localhost only, as remote `gogs` of
  both repos. [TASK-021](../../backlog/archive/tasks/task-021%20-%20Self-hosted-Gogs-on-machine01-as-git-remote-for-both-repos.md) (`infra`, m-0) installs it; the user does the first-run
  wizard and creates the account and repos. Not a backup by itself.

## Open questions

Discussion closed by the user on 2026-10-28; what is left is on the board:

- Off-machine copy target: [TASK-027](../../backlog/tasks/task-027%20-%20Choose-and-set-up-the-off-machine-copy-repos-runs-models.md) (Parked, `needs-decision`).
- Encrypted datasets in the common box: [TASK-030](../../backlog/tasks/task-030%20-%20Decide-whether-encrypted-datasets-go-into-the-common-box-DEC-015.md) (Parked, `needs-decision`).
- Workflow docs and `CLAUDE.md` still say the repo has no remote: [TASK-022](../../backlog/tasks/task-022%20-%20Gogs-server-docs-docs-infra-gogs.md-and-the-README-setup-for-the-gogs-remote-of-both-repos-DEC-014.md).
