---
id: DEC-020
title: New default venv on machine01, matching the GPU box training env and running Label Studio
status: proposed
created: 2026-10-28
from: [DIS-005]
related: [DEC-019]
superseded_by:
---
# DEC-020: New default venv on machine01, matching the GPU box training env and running Label Studio

## Context

machine01 uses `py310_for_ml` (Python 3.10). The GPU box (machine02) trains in
`~/venvs/torch`: Python 3.12.3, torch 2.11.0+cu128, and this repo's
dependencies (checked 2026-10-28; pillow there is 13.0.0, `requirements.txt`
pins 12.3.0). Label Studio (DEC-019) needs its own packages. DIS-005.

## Decision

- A new venv `~/Documents/codework/py312_for_ml` becomes the default on
  machine01: Python 3.12, torch 2.11.0 (CPU build unless machine01 has a
  usable GPU), the versions in `requirements.txt` aligned with the GPU box,
  plus Label Studio (`requirements-labeling.txt`, exact pins).
- `requirements.txt` stays the single source of exact pins and matches the GPU
  box; drift between the two is fixed by updating one or the other, recorded
  in the infra task.
- The project moves to Python 3.12 (`CLAUDE.md` conventions, commands, the
  `/venv` skill, README, `scripts/offline_install.sh`). `py310_for_ml` is kept
  until the new venv passes `scripts/check.sh`, then retired.
- Packages are installed on machine01 directly (`CLAUDE.local.md`, 2026-10-28).

## Consequences

- Code tested locally runs on the same Python and library versions as on the
  GPU box.
- One venv for notebooks, `sonoai-data`, tests and Label Studio; if Label
  Studio's pins ever clash with training, it moves to its own venv (a new DEC).
