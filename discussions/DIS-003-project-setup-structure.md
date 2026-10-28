---
id: DIS-003
title: Project setup structure review (milestone m-0)
status: open
created: 2026-10-28
outcomes: [DEC-011, DEC-012, DEC-013, DEC-014, DEC-015]
related: [DIS-002, DEC-002, DEC-007, DEC-008, DEC-009]
---
# DIS-003: Project setup structure review (milestone m-0)

## Question

Milestone m-0 ("Project Setup") asks for a project structure we can be happy
with for the next few months. DIS-002 settled the layout and process
(DEC-008..010); this review, with the user (2026-10-27/28), goes through what
is still unclear. Topics settled so far:

1. Should `docs/` move into `research_notes/`?
2. Where do the dataset style docs (`enc1`, `plain`, `submit1`) belong? Today
   they are copies of `{data_files_root}/dataset_styles/<style>.md` in
   `research_notes/datasets/` (DEC-002), and each mixes a format spec with a
   register of the datasets built in that style.
3. Where does the labeling-project tag table of version 261023 belong? It sits
   at the repo root, gitignored. It holds the tags of the labeling projects
   that produced the 261023 label files (label definitions, no patient data),
   and `configs/data/label_projects.yaml` is exported from it.
4. Training code layout: checked against DEC-006, which already fixes the
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
- **Tag table**: first read (wrongly) as plaintext patient labels; the user
  clarified it is the label definitions of version 261023, so it is
  documentation of that version and goes into its notes folder.

## Conclusion

Agreed with the user on 2026-10-28:

- DEC-011: `docs/` (code repo) holds how things work now and is edited in
  place; `research_notes/` holds why and what was found, as dated records that
  are superseded, not rewritten. `docs/` stays in the code repo.
- DEC-012: dataset docs layout. Style specs in `docs/datasets/styles/<style>.md`
  (source of truth); one folder per dataset version in
  `research_notes/datasets/<version>/` with the register (`README.md`) and, for
  261023, the tag table as `label_projects.xlsx` (no "(plain)" in the name);
  the data-root `dataset_styles/` holds copies of the `docs/` specs; no
  `research_notes/datasets/styles/`. `label_projects.yaml` names the version
  it was exported from.
- DEC-013: losses reuse the matrix score formulas of
  `evaluation/scores.py` through a soft confusion matrix; new loss `fdsc_ce`
  with the task's `S`; `dice_ce` unchanged and still the default.
- Board (Triage, m-0): TASK-011 (style specs and version registers),
  TASK-012 (tag table move and `label_projects.yaml` version).
- The DEC-006 / DEC-013 implementation is development, not project setup: a
  new milestone m-1 "First Training Run" holds TASK-014 (shared score
  formulas), TASK-015 (losses), TASK-016 (optimisation), TASK-017
  (image-level matrices, `evaluate`), TASK-018 (shared loop and segmentation
  trainers) and TASK-019 (run tracking, runs index, display, `compare_runs`),
  all `method`, in Triage. TASK-009 gets a criterion: trainers are registered
  in `training/`, not in `scripts/train.py`.
- Stray worktrees: four under `.claude/worktrees/` (desktop-app sessions,
  2026-10-27), all fully merged; the only unique content, an uncommitted
  `brief` skill draft, is kept. No new DEC (enforces DEC-007). TASK-020
  (`infra`, Triage, m-0): move the skill draft to the main checkout, remove the
  worktrees and merged `claude/*` branches, make `scripts/check.sh` fail on
  extra worktrees, and stop hiding `.claude/worktrees/` in `.git/info/exclude`.
  The app has no setting to turn worktrees off for new sessions (only their
  location), so the check is the guard.
- DEC-015: common box on machine02 with `runs/` ($SONOAI_RUNS_ROOT,
  checkpoints included) and `models/` ($SONOAI_MODELS_ROOT,
  `<task name>/<YYMMDD>_<slug>/` with `best.pt` and `model.json`); RunPod
  rsyncs back; prune unused weights after the user confirms; fail clearly when
  a root is missing. Board: TASK-023 (`infra`, m-0, box setup), TASK-024
  (`method`, m-0, `MODELS_ROOT` and missing-root error), TASK-025 (`method`,
  m-1, promote / prune), TASK-026 (`coord`, m-0, EXP template).
- DEC-014: Gogs on machine01, localhost only, as remote `gogs` of
  both repos. TASK-021 (`infra`, m-0) installs it; the user does the first-run
  wizard and creates the account and repos. Not a backup by itself.

## Open questions

Still to discuss for m-0:

- Off-machine copy of the repos and of the common box (`runs/`, `models/`):
  Gogs and the box share machine02's hardware.
- Workflow docs and `CLAUDE.md` still say the repo has no remote.
- Backlog's own `decisions/`, `docs/`, `drafts/` folders are empty and overlap
  with DEC records.
- Whether encrypted datasets also go into the common box (DEC-015).
- Guards: the notes repo has no pre-commit hook.
