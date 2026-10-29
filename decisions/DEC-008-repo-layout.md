---
id: DEC-008
title: Repo layout - dataset CLI, no empty packages, notebook areas
status: accepted
created: 2026-10-27
from: [DIS-002]
related: [DEC-002, DEC-003, DEC-005, DEC-007]
superseded_by:
---
# DEC-008: Repo layout - dataset CLI, no empty packages, notebook areas

## Context

[DIS-002](../discussions/DIS-002-workflow-and-folder-structure.md) found the README layout stale, the dataset tools spread over six
untested scripts, empty placeholder packages, and no rule for notebooks.

## Decision

- **Dataset CLI.** The dataset tools become one CLI, `sonoai-data` (also
  `python -m sonoai.data`), with subcommands `make-plain`, `check-plain`,
  `make-enc`, `check-enc`, `remove`, `label-summary`. The logic lives in
  `src/sonoai/data/` and is tested with synthetic data; behaviour and output
  (counts only) stay as they were. `scripts/` keeps only `train.py` and repo
  tools (`strip_notebook_outputs.py`, `check.sh`, ...). The old script names
  in [DEC-005](DEC-005-enc1-dataset-style.md) and earlier notes map one to one onto the subcommands.
- **No empty packages.** `src/sonoai/labeling/`, `serving/` and `viz/` are
  removed (only empty `__init__.py`, nothing imports them). A package is added
  when there is code for it.
- **Notebooks.**
  - `notebooks/human/` holds the user's own hand-written notebooks and code.
    Naming there is free. Agents read it but do not edit, move or rename files
    there unless the user asks. Outputs are still stripped before commit.
  - Notebooks made for a board task go in `notebooks/<scope>/<topic>.ipynb`
    (scope as on the board), with a first markdown cell naming the `TASK-NNN`.
  - The existing `notebooks/data_prep/T7-*.ipynb` move to
    `notebooks/human/data_prep/` (`git mv`).
- **Base branch** stays `master`. The repo has no remote, so a `main` that
  tooling proposes is only a guess.
- **Training config.** `configs/experiments/*.yaml` is the interim format
  `scripts/train.py` reads until the [DEC-003](DEC-003-trainrecipe-files-structure.md) recipes/plans are implemented,
  which comes after the labeling documentation.

## Consequences

- One entry point for dataset work, covered by `pytest`.
- The README layout and `docs/diagrams` name the CLI subcommands.
- Agents leave `notebooks/human/` alone; task notebooks are findable by scope.
