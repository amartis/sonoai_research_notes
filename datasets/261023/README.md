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

- `261023_plain` B-mode box table (cropper version 1, `derived/bmode_boxes_df.pkl`):
  29,468 images, 364 with 2 boxes, 6,717 fallback, 0 unreadable. Polygon check
  and DICOM question ([TASK-032](../../../backlog/tasks/task-032%20-%20Run-the-B-mode-cropper-on-a-dataset-version-polygon-check-reviewed-set-box-table-DEC-017.md)): [bmode_crop_check.md](bmode_crop_check.md):
  0.006 of polygon area outside the boxes (95% CI 0.003-0.009, 68
  datasources); 0.750 of two-image frames not split (n = 900, 2 datasources);
  no DICOM region tags in any datasource.

- `261023_plain` organ layer under [DEC-034](../../decisions/DEC-034-organ-layer-from-organ-polygons-only.md) ([TASK-058](../../../backlog/tasks/task-058%20-%20Count-crops-whose-diffuse-disease-polygon-has-no-organ-polygon-DEC-034.md)): [diffuse_organ_check.md](diffuse_organ_check.md):
  33.9-39.3% of eligible liver-task crops lose their organ target (steatosis 4,773
  of 14,071; cirrhosis 6,303 of 16,340; hepatoma 6,508 of 16,545), nearly all in
  the 15 of 57 datasources with no liver polygon.

- `261023_plain` choice-polygon relation table under [DEC-036](../../decisions/DEC-036-choice-polygon-relation-table.md) ([TASK-061](../../../backlog/tasks/task-061%20-%20Run-choice-check-on-261023_plain-and-write-the-choice-polygon-relation-record-DEC-036.md),
  `derived/choice_flags_df.pkl`), exploratory: [choice_polygon_check.md](choice_polygon_check.md): 116 choice
  labels on 31,252 regions; absence conflicts 0.2% (37 of 20,581 regions; 95% CI
  datasource bootstrap 0.1-0.3), presence conflicts in 35.6% of 9,420 regions
  (15.8-53.3; mostly steatosis grades, `hepatic_duct`, `hepatitis`); 75.1% of 5,066
  quality or exclusion regions still have polygons (59.9-87.7); 23.3% of choice
  pairs (6 projects) have no crop row and are not in the table.

- `261023_plain` cirrhosis v4 sample file under the [DEC-047](../../decisions/DEC-047-cirrhosis-v4-cases-per-project-group-and-liver-fallback.md) cases ([TASK-097](../../../backlog/tasks/task-097%20-%20Re-freeze-the-cirrhosis-v4-sample-file-under-the-DEC-047-cases-dataset-record-with-one-count-per-case-code-per-group-and-per-split.md),
  `derived/cirrhosis_v4_dec047_samples_df.pkl`, replaces the [TASK-087](../../../backlog/tasks/task-087%20-%20Fix-the-cirrhosis-sample-file-and-its-train-val-test-split-dataset-record-with-counts-per-split-DEC-044.md) file): [cirrhosis_v4_samples.md](cirrhosis_v4_samples.md): 13,777 samples (639
  positive, 4.6%), 53 groups; train 10,331 / val 2,068 / test 1,378 (75/15/10%); group 52+49 empty; no Qwen3-VL step.

## Label definitions

- `label_projects.xlsx`: the labeling-project tag table of this version
  (label definitions per project, no patient data; DEC-012). The code repo's
  `configs/data/label_projects.yaml` is exported from it.
