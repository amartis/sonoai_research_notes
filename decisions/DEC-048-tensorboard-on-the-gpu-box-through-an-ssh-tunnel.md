---
id: DEC-048
title: Watch GPU-box runs in TensorBoard through an ssh tunnel, without copying runs
status: accepted
area: [training, infra]
created: 2026-11-10
from: [DIS-021]
related: [DEC-006, DEC-024]
superseded_by:
---
# DEC-048: TensorBoard on the GPU box through an ssh tunnel

## Context

[DIS-021](../discussions/DIS-021-training-progress-and-tensorboard-on-the-gpu-box.md). Each run writes TensorBoard event files to `<run>/tb/`
([DEC-006](DEC-006-losses-optim-tracking.md)). Runs on the GPU box stay there until `gpu fetch`; the user wants
to follow a run while it trains, without copying it to machine01.

## Decision

1. A repo script, `scripts/gpu_tensorboard.sh start|stop|status [--port N]`, starts
   TensorBoard in a tmux session inside WSL on the GPU box, over the box's runs folder, bound
   to `127.0.0.1` only (default port 6006).
2. The same script holds an ssh tunnel from machine01 (`ssh -N -L <port>:localhost:<port>
   hostos`), so the user opens `http://localhost:<port>` on machine01. `stop` ends both.
3. Runs are not copied for this. What crosses the tunnel is the TensorBoard page: aggregate
   scalars and confusion-matrix figures, no images, no sample names. Data flowing towards
   machine01 is allowed; nothing goes to any other machine or service ([DEC-024](DEC-024-plain-never-leaves-machine01-ec2-label-studio-decrypts-in-ram.md) unchanged).

## Consequences

- The server is never exposed on the Windows LAN address; only the tunnel reaches it.
- The script lives in this repo (versioned) because the `gpu` tool is not in git.
- Needs `tensorboard` (pinned 2.21.0 in requirements.txt) in the GPU box venv.
