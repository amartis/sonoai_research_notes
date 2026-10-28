# Dataset style: plain

Copy of `{data_files_root}/dataset_styles/plain.md` (DEC-002). Format only, no patient data.

## Storage

- **Plain**: no encryption and no obfuscation. Trusted workstation only;
  never ship to the Windows GPU box or RunPod (DEC-001). The shippable copy is
  the `enc1` style (`sonoai-data make-enc`, see `enc1.md`).
- `style` file: `plain`.

## Images

- `images/` has the same hierarchical tree as the source `submit1` dataset
  (sub-folders, original file names, `.png` / `.jpg` / `.bmp`).
- Files are **hard links** to the source dataset's images (allowed for plain
  styles, DEC-002 "Reusing images of another dataset"). Do not delete or
  move the source dataset; editing an image in place changes both.
- `taskcrops_df.filepath2` is the path of an image relative to `images/`.
  Its first folder is the datasource, `dsid{datasource_id:04d}`; this holds
  for every row of `261023_plain` (72 datasources, checked 2026-10-23).
  Helpers: `sonoai.data.datasource`.

## Tables

`images/taskcrops_df.pkl`, built as in `notebooks/human/data_prep/T7-upload.ipynb`:

- source columns kept unchanged, same index and row order;
- dropped: `filepath`, `reqpath`;
- added: `np_md5_c3_current` (`md5_c3` of the image as decoded now),
  `height`, `width` (`Int64`). `np_md5_c3` (original) is kept, and the two
  may differ.

`labels/{flags,polygons}_df.pkl`, from the source
`labels/<name>_df(enc).pkl`, de-obfuscated with `sonoai.data.obfuscation`. `texts_df` was retired on 2026-10-27 (moved out of every dataset version, removed from `261023_enc1`); no dataset carries it.


- `label2` -> `label` (`dec_label`), same column position;
- `polygons_df` only: `x_2`, `y_2` -> `x`, `y` (`x = x_2 - p * 10`), in percent
  (about 0-100);
- all other columns, index and row order unchanged.

No extra tables.

## Polygon coordinates

Each `polygons_df` row is one point `p` (0-based vertex index) of a polygon
in task `task_id`, which joins to `taskcrops_df.id` (unique). The task image
the annotator saw is the crop `[left, right) x [top, bottom)` (pixels) of the
file `filepath2`; `width`/`height` are the size of that whole file.

| Columns | Space | Relation |
|---|---|---|
| `x_2`, `y_2` | obfuscated (`submit1` `(enc)` table only) | `x_2 = x + p * 10`, `y_2 = y + p * 10` |
| `x`, `y` | percent of the **crop** (Label Studio style, about 0-100) | `x = x_2 - p * 10` |
| `x_in_img`, `y_in_img` | pixels of the **whole image file** `filepath2` | `x_in_img = left + x / 100 * (right - left)`, `y_in_img = top + y / 100 * (bottom - top)` |

- `x_in_img`, `y_in_img` are not stored; compute them with
  `sonoai.data.polygons.add_pos_in_img(polygons_df, taskcrops_df)` (NaN when
  the task has no crop row).
- About 90% of crops are the whole file (`left = top = 0`, `right = width`,
  `bottom = height`), so there `x_in_img = x / 100 * width`. The rest are
  multi-ROI frames (`roi_cnt` 1 or 2, `roi_i` = which ROI); do not skip the
  offset for them.
- Values slightly outside 0-100 exist (min about -0.4, max about 101.7);
  clip if needed.
- Evidence that `x` is relative to the crop, not the file: on `roi_cnt == 2`
  frames the mean `x` is about 50 for the left crop and about 42 for the right
  one (it would be above 50 if `x` were relative to the whole file). Checked
  on `261023_plain`, 2026-10-23.
- `add_pos_in_img` replaces the old `obfuscation.get_pos_in_orig_img`, which
  expected `left_perc`/`right_perc` columns that `taskcrops_df` does not have.

Only about 85% of polygon `task_id`s are in `taskcrops_df`; the rest have no
crop box and cannot be placed in an image.

## Build and check

```bash
sonoai-data make-plain <version>_submit1 <version>_plain
sonoai-data check-plain <version>_submit1 <version>_plain --sample 0
```

The check re-encodes every change and compares with the source.

## Datasets in this style

| Codename | Built from | Date | Check |
|---|---|---|---|
| `261023_plain` | `261023_submit1` | 2026-10-22 | all passed (`--sample 0`) |
