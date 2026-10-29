---
id: DEC-015
title: Common box on machine02 for runs, checkpoints and chosen models
status: accepted
created: 2026-10-28
from: [DIS-003]
related: [DEC-001, DEC-003, DEC-006, DEC-010]
superseded_by:
---
# DEC-015: Common box on machine02 for runs, checkpoints and chosen models

## Context

[DEC-003](DEC-003-trainrecipe-files-structure.md) and [DEC-006](DEC-006-losses-optim-tracking.md) fix the layout of one run under `$SONOAI_RUNS_ROOT` and
say that `gpu fetch` brings back everything except checkpoints. They do not
say where the runs root is on each machine, where checkpoints end up, how a
chosen model is kept, or when weights may be deleted. machine01 (the
workstation) has about 16 GB free; the GPU box is WSL on machine02. The user
created `D:\codework\ml_research_commonbox` on machine02 to be shared by all
machines ([DIS-003](../discussions/DIS-003-project-setup-structure.md), 2026-10-28).

## Decision

- **Common box**: `D:\codework\ml_research_commonbox` on machine02 holds the
  results of every machine:
  - machine01: `/mnt/hgfs/ml_research_commonbox` (VMware shared folder)
  - GPU box (WSL on machine02): `/mnt/d/codework/ml_research_commonbox`
  - RunPod cannot mount it: runs are written to the pod volume and rsynced
    back into the box after the run.

  ```
  ml_research_commonbox/
  ├── runs/      $SONOAI_RUNS_ROOT: DEC-003/DEC-006 run layout, checkpoints included;
  │              index.jsonl (DEC-006)
  └── models/    $SONOAI_MODELS_ROOT: chosen models
      └── <task name>/<YYMMDD>_<slug>/
          ├── best.pt       copy of the source run's selected checkpoint
          └── model.json    model card: source run ref, task + fingerprint, dataset
                            version and split, best.json measures, commit, and the
                            DEC / EXP that chose it
  ```
- **Checkpoints** stay in their run folder in the box; nothing is copied to
  machine01's disk. `gpu fetch` is no longer needed for GPU-box runs.
- **Chosen model**: a promote command copies `best.pt` and writes
  `model.json`; the choice is recorded in an EXP conclusion or a DEC. A model
  folder is never changed after it is cited; a new choice is a new folder.
- **Retention**: metrics, `eval/`, `meta.json` and the other JSON of every
  run are kept. Checkpoints of runs that are neither cited in notes nor the
  source of a chosen model may be deleted once their EXP is done; `last.pt`
  may go when a run is done and will not be resumed. Deleting is done or
  confirmed by the user, from a list a prune command prints.
- **Missing mount**: when the runs or models root is missing (e.g. `/mnt/hgfs`
  dropped), code fails with a clear message instead of creating an empty
  folder on the local disk.
- **Content rules unchanged**: the box holds no plaintext patient data;
  weights and aggregates only ([DEC-001](DEC-001-encrypted-data-store.md), DEC-006). Whether encrypted datasets
  also go into the box is left open.

## Consequences

- Every machine sees the same runs and models by the same full run ref.
- machine01's small disk holds no checkpoints.
- The box is on machine02's hardware, so it is not a backup; the off-machine
  copy (DIS-003) should include `runs/` (without pruned weights) and `models/`.
- Writing checkpoints from WSL to `/mnt/d` is slower than to the WSL disk;
  if it hurts, a plan may write locally and move the run at the end.
