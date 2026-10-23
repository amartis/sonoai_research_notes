# DEC-003: Train recipe, plan and run files structure

- Date: 2026-10-22
- Status: proposed

## Context

We train several model families (`resenc_unet`, `transunet`, `swin_unet`, ...)
with different optimisation settings on different datasets (DEC-002), and run
the same training on the workstation, the Windows GPU box and RunPod pods.
Today an experiment is a YAML file in `configs/experiments/` that mixes what
to train (`trainer`, `trainer_args`) with where to run it (`data.store`, a
machine path). That makes a config machine-specific and gives no name to
"this exact training, wherever it ran".

We want the definition of a training in Python files, so it can be either a
plain description or a short custom training loop, split into the part that
is the same on every machine and the part that is not, plus a record of each
time it was actually executed.

## Terms

| Term | Meaning | Where |
|---|---|---|
| **task** | The learning problem: task type, labels used, classes, targets, metrics. Named and versioned (DEC-004), e.g. `seg_anatomy_v1`. | `src/sonoai/tasks/` |
| **recipe** | *What* is trained: task, dataset version and split, model, loss, optimisation, evaluation, seed. Machine-independent. A partial definition. | `configs/train/recipes/` (git) |
| **plan** | *How and where* a recipe is executed: the recipe plus machine and execution settings. A complete definition, but it says nothing about whether it was executed. | `configs/train/plans/` (git) |
| **machine profile** | Default execution settings of one machine, shared by its plans. | `configs/train/machines/` (git) |
| **run** | *One actual execution* of a plan: status, logs, metrics, checkpoints. | `$SONOAI_RUNS_ROOT/` (not in git) |
| **trainer** | A named training loop in `src/sonoai/training/` (`smoke`, `segmentation`, ...). By default chosen by the task type. | `src/` |

One task has zero or more recipes; one recipe has zero or more plans (local debugging, the GPU box, a RunPod
pod); one plan has zero or more runs (first attempt, a fresh restart after a
crash). Runs of plans of the same recipe are directly comparable.

## Decision

### Recipe vs plan: what goes where

The rule: **anything that can change the trained model or its metrics belongs
to the recipe; anything that only decides where and how fast it runs belongs
to the plan.**

| Recipe | Plan (or its machine profile) |
|---|---|
| task (`seg_anatomy_v1`): classes, targets, metrics (DEC-004) | |
| dataset version (`261022`), split / fold | dataset style used on that machine (codename `261022_submit1`, ...) |
| model name + args, init weights | machine label, device(s), number of GPUs |
| loss, optimizer, LR schedule, epochs/steps | per-device micro-batch, gradient accumulation (derived so the recipe's global batch holds) |
| **global** batch size, precision (`bf16`/`fp32`), grad clipping, EMA | `num_workers`, prefetch, pinned memory |
| augmentation, input size, crop policy | key source (prompt / env / RunPod secret) |
| validation frequency, checkpoint selection criterion (metrics come from the task) | |
| seed, trainer (when not the task type's default) | |

A plan **adds to** its recipe and never overrides it. It refers to the recipe
by name (composition), not by Python inheritance or import, and `TrainPlan`
has no recipe fields, so an override cannot be written. A different setting
means a new recipe or recipe variant. This keeps "recipe name" a reliable key
for comparing results.

### Root layout

```
configs/train/                              all training definitions (git)
├── machines/
│   ├── ws.py                               workstation (machine01)
│   ├── gpubox.py                           Windows GPU box (machine02)
│   └── runpod_a100.py
├── recipes/
│   ├── smoke.py                            machine check (replaces experiments/smoke.yaml)
│   └── <task name>/                        e.g. seg_anatomy_v1/, cls_view_v1/
│       └── <recipe name>.py
└── plans/
    ├── smoke/
    │   └── <plan name>.py
    └── <task name>/
        └── <recipe name>/                  one folder per recipe (variants share the file's folder)
            └── <plan name>.py

$SONOAI_RUNS_ROOT/                          runs (gitignored, outside the repo on remote machines)
└── <recipe name>/
    └── <plan name>/
        └── <run id>/
```

Files under `configs/train/` are loaded by path
(`importlib.util.spec_from_file_location`); the folders are not packages, and
the leading digits in names are fine.

### Names

| Id | Format | Example |
|---|---|---|
| recipe name | `<YYMMDD>_<slug>`, `+ .<variant>` | `261022_resenc_fold0`, `261022_resenc_lr.lr0.0003_s1` |
| plan name | `<YYMMDD>_<machine>[_<slug>]` | `261023_gpubox`, `261023_gpubox_mb4` |
| run id | `<YYMMDD-HHMMSS>` (start time) | `261023-213005` |
| full run ref | `<recipe name>/<plan name>/<run id>` | `261022_resenc_fold0/261023_gpubox/261023-213005` |

- `YYMMDD` is the date the file was created. Slugs and machine labels:
  lowercase letters, digits and `_`, short.
- Recipe names are unique across tasks; the task folder is not part of the
  name, but it must equal the recipe's `task` field (the loader checks this).
  Plan names are unique within a recipe.
- No patient, case or site identifiers in any name (they end up in notes).
- Once a recipe or plan has a run cited in `research_notes/`, do not change its
  meaning. Fix typos freely; for a different setting, add a variant, a new
  recipe, or a new plan. The copies kept in each run (below) are the record if
  this is broken by accident.

### Recipe files

A recipe file defines either:

- `RECIPE`: one `TrainRecipe`, or
- `RECIPES`: a `dict[str, TrainRecipe]` for variants (seeds, LR grid, folds);
  names are `<file stem>.<key>`,

and optionally a `train(ctx)` function (imperative style).

`TrainRecipe` and its parts are frozen dataclasses in
`sonoai.training.recipe`. They must resolve to plain JSON (`to_dict()`), so
every run records the full resolved recipe, also for imperative recipes.

Every recipe names exactly one task (DEC-004). The task supplies classes,
targets, metrics, the model's output size and the default trainer and loss.

**Descriptive style** (the default): name the task and describe everything
else as data.

```python
# configs/train/recipes/seg_anatomy_v1/261022_resenc_fold0.py
from sonoai.training.recipe import Data, Eval, Model, Optim, TrainRecipe

RECIPE = TrainRecipe(
    task="seg_anatomy_v1",                 # trainer "segmentation" and n_classes come from the task
    data=Data(dataset="261022", split="kfold5/0", input_size=(256, 256), augment="us_basic_v1"),
    model=Model("resenc_unet", in_channels=3),
    loss="dice_ce",
    optim=Optim("adamw", lr=3e-4, weight_decay=1e-4, global_batch=32, epochs=100,
                schedule="cosine", warmup_epochs=5, precision="bf16"),
    eval=Eval(every_epochs=1, select="val/dice:max"),
    seed=0,
)
```

**Variants**: each is its own recipe.

```python
# configs/train/recipes/seg_anatomy_v1/261022_resenc_lr.py
from sonoai.training.presets import resenc_seg_base   # shared defaults live in src/, not in configs/

RECIPES = {
    f"lr{lr:g}_s{seed}": resenc_seg_base(task="seg_anatomy_v1", dataset="261022").replace(optim__lr=lr, seed=seed)
    for lr in (1e-4, 3e-4, 1e-3)
    for seed in (0, 1, 2)
}
```

**Imperative style**: still declare `RECIPE` (task, data, model, seed, ...) so
its runs are indexed and evaluated the same way, set `trainer="custom"`, and
write the loop:

```python
# configs/train/recipes/seg_anatomy_v1/261023_transunet_twostage.py
from sonoai.training.recipe import Data, Model, TrainRecipe

RECIPE = TrainRecipe(
    task="seg_anatomy_v1",
    trainer="custom",
    data=Data(dataset="261022", split="kfold5/0", input_size=(224, 224)),
    model=Model("transunet"),
    seed=0,
    extra={"stage1_epochs": 20, "stage2_epochs": 80},
)


def train(ctx):
    """ctx: recipe, plan, task, run (sonoai.tracking.Run), dataset, device,
    build_model(), build_loader(split), evaluate(model, split)."""
    model = ctx.build_model()
    ...
```

### Machine profiles

```python
# configs/train/machines/gpubox.py
from sonoai.training.plan import Machine

MACHINE = Machine(
    label="gpubox",
    devices=1,
    workers=6,
    micro_batch=16,
    dataset_styles=("<encrypted style>",),   # styles present on this machine, in order of preference
)
```

The file name equals the label. Profiles hold defaults only; data roots still
come from env vars via `sonoai.paths`.

### Plan files

```python
# configs/train/plans/seg_anatomy_v1/261022_resenc_fold0/261023_gpubox.py
from sonoai.training.plan import TrainPlan

PLAN = TrainPlan(recipe="261022_resenc_fold0", machine="gpubox", micro_batch=8)
```

- `recipe` is a recipe name (with `.<variant>` for a variant); `machine` is a
  machine profile label. Every other field is optional and overrides the
  profile's default, never the recipe.
- The plan's folder must match its recipe (`plans/<task name>/<recipe file
  stem>/`); the loader checks this, so the folder tree can be trusted when
  browsing.
- Before training, the loader checks that `PLAN.machine` equals
  `$SONOAI_MACHINE` and refuses to start otherwise, so a GPU-box plan cannot
  run on a pod by mistake.

### Rules for all files under `configs/train/`

- Import only from `sonoai` and third-party libraries, never from another file
  under `configs/train/`. Shared defaults and helpers go in
  `src/sonoai/training/presets.py` or another module under `src/`.
- No machine paths, no key, no patient/case identifiers. A recipe names the
  dataset by its **version**; the plan (or machine profile) picks the style
  present on that machine, and the run records the full codename (DEC-002).
- No side effects at import time beyond building the spec (no data access,
  no GPU, no file writes), so tools can list and diff files without running
  them.
- Values in `extra` must be JSON-serialisable.
- When the same imperative loop appears in two recipes, move it into
  `src/sonoai/training/` as a named trainer.

### Run layout

```
$SONOAI_RUNS_ROOT/<recipe name>/<plan name>/<run id>/
├── recipe.py          copy of the recipe file source as executed
├── plan.py            copy of the plan file source
├── recipe.json        resolved recipe (TrainRecipe.to_dict())
├── task.json          resolved task spec (DEC-004); its fingerprint goes in meta.json
├── plan.json          resolved plan, with machine profile defaults filled in and
│                      derived values (gradient accumulation, dataset codename)
├── meta.json          git commit + dirty flag, machine label, host, GPU model, driver/CUDA/torch/python
│                      versions, start/end time of each attempt, status (running|done|failed|interrupted)
├── metrics.jsonl
├── train.log
└── checkpoints/       last.pt, best.pt (weights only, never images)
```

- `$SONOAI_RUNS_ROOT` is `sonoai.paths.RUNS_ROOT`. `scripts/train.py` builds
  the path; the `gpu` tool and `deploy/runpod/run.sh` set the runs root (and
  may still set `$RUN_DIR`, which wins, to that same path).
- `--resume <run id>` continues an interrupted run in its own directory and
  appends to `metrics.jsonl`; `meta.json` records each attempt. Starting a plan
  again from scratch creates a new run id.
- Fetched runs keep the same path on the workstation, so the full run ref is
  a stable reference in notes.

### Ad hoc runs

For smoke tests and debugging without writing a plan file, a recipe can be run
directly with a machine profile:

```bash
python scripts/train.py configs/train/recipes/seg_anatomy_v1/261022_resenc_fold0.py --machine ws --debug
```

These runs go to `<recipe name>/_adhoc_<machine>/<run id>/`, are marked
`"adhoc": true` in `meta.json`, and are not cited in notes. Only runs of a plan
file count as results.

### Entry point

```bash
python scripts/train.py configs/train/plans/seg_anatomy_v1/261022_resenc_fold0/261023_gpubox.py
python scripts/train.py configs/train/plans/seg_anatomy_v1/261022_resenc_fold0/261023_gpubox.py --resume 261023-213005
python scripts/train.py configs/train/recipes/seg_anatomy_v1/261022_resenc_lr.py --list   # list variants
python scripts/train.py <recipe file>[:<variant>] --machine ws --debug                 # ad hoc run
```

`scripts/train.py` loads the plan, then its recipe, the recipe's task and the
machine profile, checks the machine and the task/model fit, resolves the dataset version to a codename present on the
machine, creates the `Run`, writes the copies and resolved JSON, then calls
the trainer, or the recipe's `train(ctx)` when `trainer="custom"`.

### Referencing from notes and other recipes

- `research_notes/experiments/*.md` cite runs by full run ref and the commit
  from its `meta.json`.
- A recipe that starts from another run's weights names that run as an input,
  like a dataset:
  `Model("resenc_unet", init_from="261022_resenc_fold0/261023_gpubox/261023-213005:best")`.

## Consequences

- Recipes and plans are code-reviewed, diffable and versioned with the model
  code they use. The same recipe runs on every machine without edits; only a
  short plan file differs.
- Results of different recipes are comparable when task, dataset version and
  split match (DEC-004); results from different machines are comparable by
  recipe name. Bitwise
  equality is not expected (GPU model, cuDNN algorithms, driver versions
  differ), which is why `meta.json` records hardware and versions; running one
  recipe under two plans is also a cheap way to measure that noise.
- Python configs can run arbitrary code. Mitigated by: no import-time side
  effects, resolved JSON in every run, and source copies in the run. Nothing
  outside the repo is ever loaded as a recipe, plan or machine profile.
- Global batch in the recipe means a smaller GPU runs the same recipe with
  gradient accumulation instead of a different recipe. BatchNorm statistics
  still see the micro-batch; models sensitive to that should use
  GroupNorm/InstanceNorm, or fix the micro-batch in the recipe.
- One more file per execution setup. Machine profiles keep plan files to a
  line or two, and ad hoc runs cover quick checks.
- Replaces `configs/experiments/*.yaml`. Needs: `sonoai.training.recipe` and
  `sonoai.training.plan` (dataclasses, loaders, checks), a `scripts/train.py`
  rewrite, `Run` taking the run path, `SONOAI_MACHINE` in `.env.example` and
  the pod env, updates to `deploy/runpod/run.sh`, the `gpu train` usage in
  docs, README and CLAUDE.md ("experiments are YAML in `configs/experiments/`").

## Open questions

- Are seeds recipe variants (`.s0`, `.s1`) or repeated runs of one plan with a
  run-level seed? Current proposal: variants, so the seed stays a recipe field
  and every run is reproducible from its recipe alone.
- Should a plan file be able to cover all variants of a recipe file (`PLANS`
  dict, executed one after another), or is one plan per variant enough?
- Split definitions: inside the dataset (DEC-002 extra table, e.g.
  `splits_df.pkl`) or in `configs/data/`? The recipe only names the split
  (see also DEC-004 on whether the split belongs to the task).
- Whether to keep a small runs index (one JSON line per finished run) for
  quick comparison across machines, or always scan `$SONOAI_RUNS_ROOT`.
