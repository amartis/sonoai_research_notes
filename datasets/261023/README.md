# Dataset version 261023

Register of the styles built for version `261023` ([DEC-002](../../decisions/DEC-002-dataset-files-structure.md), [DEC-012](../../decisions/DEC-012-dataset-docs-layout.md)): codenames,
what each was built from, dates and check results. Aggregates only; no patient
data, file names or identifiers.

The format of each style is specified in the code repo,
[`docs/datasets/styles/<style>.md`](../../../docs/datasets/styles/) (source of truth; the data-root
`dataset_styles/` holds copies). How notes, decisions and board tasks fit
together: [`docs/workflow.md`](../../../docs/workflow.md) in the code repo.

## Styles built

| Codename | Style | Built from | Date | Check / notes |
|---|---|---|---|---|
| `261023_submit1` | `submit1` | - | 2026-10-22 | 29,468 images, 143,152 taskcrops rows |
| `261023_plain` | `plain` | `261023_submit1` | 2026-10-22 | all passed (`--sample 0`) |
| `261023_enc1` | `enc1` | `261023_plain` | 2026-10-23 | all passed (`--sample 0`): 29,472 files, 4 tables, 29,468 images |

`261023_enc1` passphrase label: _(fill in)_.

## History

- 2026-10-27: `texts_df` retired from every style of this version;
  `labels/texts_df.pkl` removed from `261023_enc1`
  (`scripts/remove_from_enc_dataset.py`, now `sonoai-data remove`). Check
  all passed (`--sample 300`): 29,471 files, 3 tables.

## Statistics

- `261023_plain`: 72 datasources; every `taskcrops_df.filepath2` starts with
  its datasource folder (checked 2026-10-23).

## Label definitions

- `label_projects.xlsx`: the labeling-project tag table of this version
  (label definitions per project, no patient data; DEC-012). The code repo's
  `configs/data/label_projects.yaml` is exported from it.
