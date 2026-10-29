---
id: DEC-004
title: Training tasks
status: accepted
created: 2026-10-22
from: []
related: [DEC-002, DEC-003]
superseded_by:
---
# DEC-004: Training tasks

## Context

One dataset version ([DEC-002](DEC-002-dataset-files-structure.md)) carries several kinds of labels (`flags_df`,
`polygons_df`, `texts_df`) and can be used for several learning problems:
anatomy segmentation from polygons, lesion detection from the same polygons
as boxes, view classification from flags, and so on. A recipe ([DEC-003](DEC-003-trainrecipe-files-structure.md))
needs to say which of these it trains, and results are only comparable when
the labels were turned into targets the same way and the metrics were
computed the same way.

Until now this was implicit in the trainer name (`trainer="segmentation"`)
and in model arguments (`n_classes=4`), which mixes *what must be predicted*
with *which loop trains it*, and lets two recipes with different class sets
look comparable.

## Terms

| Term | Meaning |
|---|---|
| **task type** | The form of the prediction: `seg` (segmentation), `det` (detection), `cls` (classification), ... Decides the default trainer and the output form. |
| **task** | A named, versioned learning problem: task type + which labels are used + how they become targets + classes + metrics. E.g. `seg_anatomy_v1`. |
| **class map** | The ordered class list of a task and the mapping from label values to class indices, including merged and ignored values. |
| **target** | What the model is trained against for one sample (mask, boxes, class index), built by the task from the sample's label rows. |

One dataset version serves many tasks; one task is trained by many recipes.
A result is identified by **task + dataset version + split**; metrics are
comparable only when all three match.

## Decision

### Task name

```
<type>_<subject>_v<N>        e.g. seg_anatomy_v1, det_lesion_v1, cls_view_v1
```

- `type`: one of the registered task types (`seg`, `det`, `cls`, ...).
- `subject`: lowercase letters, digits and `_`, short; says what is predicted.
- `v<N>`: bumped whenever anything that changes targets or metrics changes:
  classes, class map, merge/ignore rules, sample eligibility, target
  rendering (e.g. polygon rasterisation), metric definitions. Code refactors
  that leave targets and metrics identical keep the version.
- A task name is never reused for a different definition, and old versions
  stay in the code as long as runs cite them.
- No patient, case or site identifiers in task names or class names.

### Definition in code

Tasks contain code (label-to-target conversion), so they live in the
package, registered by name like models:

```
src/sonoai/tasks/
├── __init__.py          TaskSpec, register_task, get_task, list_tasks
├── types.py             task types: output form, default trainer, default loss
├── seg_anatomy.py       seg_anatomy_v1, seg_anatomy_v2, ...
├── det_lesion.py
└── cls_view.py
```

```python
# src/sonoai/tasks/seg_anatomy.py
from . import TaskSpec, register_task

register_task(TaskSpec(
    name="seg_anatomy_v1",
    type="seg",
    labels=("polygons",),                         # DEC-002 label tables used
    classes=("background", "class_a", "class_b", "class_c"),
    class_map={"<label value>": "class_a", ...},  # every known label value -> class, or IGNORE
    eligible="has_any_polygon",                   # which samples of the dataset take part
    target=render_masks,                          # (sample row, label rows) -> target, in memory
    metrics=("dice", "iou"),                      # computed by sonoai.evaluation, same for every recipe
    ignore_index=255,
))
```

A `TaskSpec` is a frozen dataclass that resolves to plain JSON (`to_dict()`,
with functions recorded by qualified name).

### Rules

- **Unknown label values are an error.** If a dataset version contains a
  label value missing from the class map, the task refuses to build targets
  instead of silently dropping it. Adding the value means a new task version
  (or an explicit `IGNORE` entry in a new version).
- **Eligibility is part of the task.** Which samples take part (e.g. only
  samples with at least one polygon, only samples with a view flag) is
  decided by the task and applied *inside* each split, so splits stay defined
  on the dataset's samples and are shared across tasks.
- **Targets are built in memory** from the decrypted label tables
  (`EncryptedStore.read_pickle`); never cached to disk (CLAUDE.md).
- **Metrics belong to the task.** Every recipe of a task is evaluated by the
  same code with the same settings; metric names are logged as
  `<split>/<metric>` (`val/dice`).
- **The task sizes the model output.** `ctx.build_model()` passes the task's
  output size (e.g. `n_classes`) to the model builder; a recipe that sets it
  explicitly must match, or the loader refuses to start.

### Use in recipes and runs

- A recipe names exactly one task: `TrainRecipe(task="seg_anatomy_v1", ...)`.
  The trainer defaults from the task type; `trainer=` is set only for a
  different registered loop or `"custom"` (DEC-003).
- Recipes and plans are grouped by task name under `configs/train/`
  (DEC-003).
- Each run stores the resolved task spec in `task.json` and its fingerprint
  (hash of `to_dict()`) in `meta.json`. If a task's fingerprint differs from
  earlier runs of the same task name, the loader warns: the definition was
  changed without a version bump.

### Task notes

Each task gets `research_notes/tasks/<task name>.md`: purpose, class list
and class map summary, eligibility rule, metrics, and per dataset version the
**aggregate** counts (samples eligible, instances per class). No file names,
case ids or images.

## Consequences

- "Which problem was trained" is explicit, versioned and checkable; metric
  tables can be grouped by task + dataset version + split without guessing.
- A new class set or label rule costs a new task version instead of an edit,
  so old runs stay interpretable.
- Strict unknown-label checks mean a relabelled dataset version can break an
  old task; that is intended, and the fix is a new task version.
- Recipes get shorter: classes, output size, metrics and the usual trainer
  come from the task.
- Needs: `src/sonoai/tasks/`, an evaluation entry point per task type in
  `sonoai.evaluation`, `task.json` in runs, `research_notes/tasks/`, and the
  `task` field in `TrainRecipe` (DEC-003).

## Open questions

- Should the split belong to the task (a benchmark is often task + dataset +
  split) or stay in the recipe? Current proposal: recipe, with splits defined
  per dataset version (DEC-002 open question).
- Multi-task models (e.g. segmentation + view classification heads): a
  composite task with its own name built from sub-tasks, or a list of tasks
  in the recipe?
- Where the class map's label vocabulary comes from: hard-coded in the task,
  or read from a vocabulary file that DEC-002 datasets carry.
- Which tasks, if any, use `texts_df`.
