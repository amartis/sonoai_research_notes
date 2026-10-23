# Dataset style: submit1

Copy of `{data_files_root}/dataset_styles/submit1.md` (DEC-002). Format only, no patient data.
The name `submit1` is historical; never rename it.

## Storage

- **Plain files, obfuscated labels**: images are unencrypted; label tables
  are the `(enc)` tables of `sonoai.data.obfuscation`, which is reversible
  obfuscation, **not** encryption. Trusted workstation only; never ship to
  the Windows GPU box or RunPod (DEC-001).
- No `style` file yet (DEC-002 asks for one with the line `submit1`).
- Replaces the old `SONOAI_RAW_IMGS_ROOT` / `SONOAI_RAW_LBLS_ROOT` folders
  (`imgs/` -> `images/`, `lbls/` -> `labels/`).

## Images

- `images/` is a hierarchical tree (sub-folders, original file names),
  `.png` / `.jpg` / `.bmp`, mixed channel counts. Own files, not links.
- `taskcrops_df.filepath2` is the path of an image relative to `images/`.

## Tables

`images/taskcrops_df.pkl`: one row per training sample (crop). Columns
`id`, `project_id`, `reqpath`, `task_stat`, `filepath`, `np_md5_c3`,
`datasource_id`, `top`, `bottom`, `left`, `right`, `roi_i`, `roi_cnt`,
`filepath2`. Index is not unique. No image size columns.

`labels/<name>_df(enc).pkl` for `flags`, `polygons`, `texts`:

- `label2`: label obfuscated with `enc_label` (decode with `dec_label`);
- `polygons` only: `x_2`, `y_2` = point + `p * 10` (decode with `dec_point`);
  for how the decoded `x`, `y` map to image pixels, see `plain.md`
  "Polygon coordinates";
- other columns (`project_id`, `task_id`, `annotation_id`, `tag_type`,
  `tag_group`, ...) are plain.

No extra tables.

## Derived styles

- `plain`: `scripts/make_plain_dataset.py` (see `plain.md`).
- Encrypted: via `plain`, then `enc1` (`scripts/make_enc_dataset.py`, see `enc1.md`).

## Datasets in this style

| Codename | Date | Notes |
|---|---|---|
| `261023_submit1` | 2026-10-22 | 29,468 images, 143,152 taskcrops rows |
