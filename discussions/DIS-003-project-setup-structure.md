---
id: DIS-003
title: Project setup structure review (milestone m-0)
status: open
created: 2026-10-28
outcomes: [DEC-011, DEC-012]
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
- Board (Triage, m-0): TASK-011 (style specs and version registers),
  TASK-012 (tag table move and `label_projects.yaml` version).

## Open questions

Still to discuss for m-0:

- Where training code goes: trainers are registered in `scripts/train.py`,
  `src/sonoai/training/` is nearly empty, and losses/optimisers (DEC-006) have
  no agreed home.
- Metrics in two places: `src/sonoai/tasks/` (DEC-004) and `evaluation/`.
- Backups: neither repo has a remote.
- Backlog's own `decisions/`, `docs/`, `drafts/` folders are empty and overlap
  with DEC records.
- Where results and chosen models go once runs start.
- Stray git worktrees under `.claude/worktrees/` (against DEC-007).
- Guards: the notes repo has no pre-commit hook.
