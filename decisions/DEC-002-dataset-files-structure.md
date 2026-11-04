---
id: DEC-002
title: Dataset files structure
status: accepted
area: [datasets]
created: 2026-10-22
from: []
related: [DEC-001]
superseded_by:
---
# DEC-002: Dataset files structure

## Context

A training session reads images, the crop definitions for each training
sample, and label tables. We need to rebuild datasets (new cases, relabelling,
cleaning) and also ship them in different forms: plain on the trusted
workstation, encrypted ([DEC-001](DEC-001-encrypted-data-store.md)) on the Windows GPU box and RunPod. A single
layout and naming scheme lets code, configs and notes point at a dataset by
one name, whatever its form.

## Terms

| Term | Meaning |
|---|---|
| **dataset** | The data fed into a training session: one content version in one style. |
| **version** | Which content: the images, crops and labels as of a build date. |
| **style** | How the content is stored: plain or encrypted, flat or hierarchical image folders, and any other storage choices. Documented once in `dataset_styles/<style>.md`. |
| **codename** | `<version>_<style>`; the unique id of a dataset. |
| **components** | The parts every dataset has, whatever its version and style (below). |

The same version can exist in several styles (for example a plain copy on the
workstation and an encrypted copy on the GPU box); their content is identical.

## Decision

### Codename

```
<version>_<style>        e.g. 261022_submit1
```

- `version`: `YYMMDD`, the date the content was built.
- `style`: lowercase letters and digits only, no `_` (so the codename splits
  unambiguously at the first `_`). Short is fine.
- If two different contents are built on the same day, the second one gets a
  suffix letter on the version: `261022b_submit1`.
- Codenames and style names must not contain patient, case or site
  identifiers; they appear in configs, run names and notes.
- `submit1` is an existing name kept for historical reasons; never rename it.

### Components

1. **Images**: the source image files, plain or encrypted.
2. **`taskcrops_df.pkl`**: one row per training sample. Defines the crop area
   within its image and the image metadata (width, height, md5 of the plain
   image bytes, ...).
3. **Label tables**: `flags_df.pkl`, `polygons_df.pkl`, `texts_df.pkl`.

Extra per-sample information is added in one of two ways:

- extra columns in `taskcrops_df.pkl` (e.g. `datasource_id`), or
- an extra `<name>_df.pkl` next to `taskcrops_df.pkl`, keyed by the same
  sample id so it joins one-to-one.

Use extra columns for a few scalar fields; use a separate table when the
information is large or optional for most consumers. Either way, the style
doc lists what was added.

### Layout

```
{data_files_root}/
├── dataset_styles/
│   ├── submit1.md            one doc per style (see "Style docs")
│   └── ...
└── datasets/
    └── {codename}/
        ├── style             one line: the style name (machine-readable check)
        ├── images/
        │   ├── ...           image files, flat or in sub-folders (per style)
        │   ├── taskcrops_df.pkl
        │   └── <name>_df.pkl optional extra per-sample tables
        └── labels/
            ├── flags_df.pkl
            ├── polygons_df.pkl
            └── texts_df.pkl
```

For an encrypted style, `datasets/{codename}/` is an `EncryptedStore` root
(`manifest.enc` + `blobs/`). The tree above is then the *logical* layout:
the paths inside the store (`images/...`, `labels/...`), read with
`store.read_image(...)` / `store.read_pickle(...)`. On disk nothing of it is
visible. The `style` file is the only plaintext file and stays outside the
store.

`{data_files_root}` is `$SONOAI_DATA_FILES_ROOT`, read through `sonoai.paths`;
it is never hard-coded. Code finds a dataset by codename at
`$SONOAI_DATA_FILES_ROOT/datasets/{codename}`, whatever its style.

There is no separate root for encrypted data: encrypted is just another
style, so `SONOAI_ENC_ROOT` is retired. On the trusted workstation,
`{data_files_root}` may hold datasets of any style. On the Windows GPU box and
RunPod it holds only encrypted-style datasets (DEC-001).

### Style docs

`dataset_styles/<style>.md` records, for every dataset in that style:

- plain or encrypted; for encrypted, which key it uses (by label, e.g.
  "data key 2026-10", never the key itself),
- image folder structure (flat or hierarchical, and how files are named),
- extra columns or extra tables beyond the standard components,
- any other choice made when building it.

The doc describes the format only, so it may hold no patient data. A copy or
summary goes in `research_notes/datasets/` so the decision is versioned.

### Encryption key

Encrypted datasets follow DEC-001. Code gets the key only through
`sonoai.secure.load_key()` (`SONOAI_DATA_KEY`, `SONOAI_DATA_KEY_FILE`, or a
prompt). The key is kept in the password manager; it is never stored in the
codebase, in `{data_files_root}`, or on a shared machine.

### Reusing images of another dataset

A new version that changes only labels or crops can point at an existing
dataset's images instead of copying them. Allowed only for **plain** styles,
and only with paths relative to `{data_files_root}`:

- symlinks or hardlinks to the other dataset's files, or
- a text file in place of an image, holding the relative path to it.

Not for encrypted styles: blob names and AAD are bound to the logical path, so
a blob cannot be shared under another path. `sonoai-vault encrypt` follows
symlinks, so encrypting a linked plain dataset produces a full, self-contained
encrypted copy, which is what we want to ship.

## Consequences

- One string (the codename) identifies a dataset in configs, run metadata and
  notes; a plain and an encrypted copy of the same content share the version.
- Readers must handle flat and hierarchical image folders; the style doc and
  `taskcrops_df` are the source of truth for which files belong to a dataset,
  not a directory listing.
- Linked plain datasets break if the target dataset is moved or deleted;
  don't delete a dataset that another one links to.
- Symlinks may not survive the VMware shared folder or a Windows copy;
  build the encrypted store first and ship that.
- `.pkl` tables are tied to the pandas version that wrote them; pin pandas
  (`requirements.txt`) or rewrite the tables when upgrading.
- Retiring `SONOAI_ENC_ROOT` means changing `sonoai.paths`, `scripts/train.py`
  (choose the dataset by codename instead of a store path), `.env.example`,
  the README, `CLAUDE.md`, the experiment configs, the T7-upload notebook, and
  `deploy/` (shipping the whole store becomes shipping
  `datasets/{codename}/`).

## Open questions
- Column name of the sample id that `taskcrops_df` and extra tables join on.
- Whether label tables also key on the sample id or on the image.
- Whether the `style` file should become a small `dataset.yaml` (style,
  version, parent dataset it links to, build commit).
