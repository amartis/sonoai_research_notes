# Dataset style: plain

Copy of `{data_files_root}/dataset_styles/plain.md` (DEC-002). Format only, no patient data.

## Storage

- **Plain**: no encryption and no obfuscation. Trusted workstation only;
  never ship to the Windows GPU box or RunPod (DEC-001). The shippable copy is
  the `enc1` style (`scripts/make_enc_dataset.py`, see `enc1.md`).
- `style` file: `plain`.

## Images

- `images/` has the same hierarchical tree as the source `submit1` dataset
  (sub-folders, original file names, `.png` / `.jpg` / `.bmp`).
- Files are **hard links** to the source dataset's images (allowed for plain
  styles, DEC-002 "Reusing images of another dataset"). Do not delete or
  move the source dataset; editing an image in place changes both.
- `taskcrops_df.filepath2` is the path of an image relative to `images/`.

## Tables

`images/taskcrops_df.pkl`, built as in `notebooks/data_prep/T7-upload.ipynb`:

- source columns kept unchanged, same index and row order;
- dropped: `filepath`, `reqpath`;
- added: `np_md5_c3_current` (`md5_c3` of the image as decoded now),
  `height`, `width` (`Int64`). `np_md5_c3` (original) is kept, and the two
  may differ.

`labels/{flags,polygons,texts}_df.pkl`, from the source
`labels/<name>_df(enc).pkl`, de-obfuscated with `sonoai.data.obfuscation`:

- `label2` -> `label` (`dec_label`), same column position;
- `polygons_df` only: `x_2`, `y_2` -> `x`, `y` (`x = x_2 - p * 10`), in percent
  (about 0-100);
- all other columns, index and row order unchanged.

No extra tables.

## Build and check

```bash
python scripts/make_plain_dataset.py <version>_submit1 <version>_plain
python scripts/check_plain_dataset.py <version>_submit1 <version>_plain --sample 0
```

The check re-encodes every change and compares with the source.

## Datasets in this style

| Codename | Built from | Date | Check |
|---|---|---|---|
| `261023_plain` | `261023_submit1` | 2026-10-22 | all passed (`--sample 0`) |
