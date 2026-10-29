---
id: EXP-NNN
title: <title>
status: planned       # planned | running | done | dropped
created: YYYY-MM-DD
from: []              # DEC-NNN that call for it (board TASK-NNN go in the text)
related: []
---
# EXP-NNN: <title>

- Date: YYYY-MM-DD
- Code commit: `<sha>`
- Config: `configs/experiments/<file>.yaml`
- Runs: `<run-name>`, ...
- Data: store version / label version / split (by datasource or patient)

Writing standard: [docs/writing.md](../../docs/writing.md) (DEC-021).

## Question / hypothesis

State whether the experiment is exploratory or confirmatory.

## Setup

## Results

| run | split | n (per class) | metric | value (95% CI) | baseline |
|-----|-------|---------------|--------|----------------|----------|

## Analysis

Including failure cases, in aggregate (no images or file names).

## Limitations

## Conclusion and next steps

## Reporting checklist

Tick each item or mark it N/A. Drawn from CLAIM 2024, STARD-AI and TRIPOD+AI
(details in `docs/writing.md`).

- [ ] Data: datasources, inclusion and exclusion, counts per class per split
- [ ] Split by datasource or patient; no overlap between splits; test set
      untouched until the final evaluation
- [ ] Reference standard: what the labels mean, who labelled, how
      disagreements were resolved
- [ ] Model and training: config, preprocessing, augmentation, seeds
- [ ] Metrics with 95% CI (method named) next to the baseline
- [ ] Operating point: how the threshold was chosen, on which split
- [ ] Subgroups (datasource, device) where n allows
- [ ] Limitations, and whether the result is exploratory or confirmatory
