# Dataset style: enc1

Copy of `{data_files_root}/dataset_styles/enc1.md` (DEC-002). Format only, no patient data.

## Storage

- **Encrypted** (DEC-001, DEC-005): an `EncryptedStore` (AES-256-GCM, HMAC-named
  blobs, encrypted manifest). This is the style to ship: the Windows GPU box
  (machine02, `gpu put`) and RunPod Secure Cloud network volumes (rsync).
- Key: derived with scrypt from a passphrase (at least 8 characters) and the
  store's salt in `kdf.json` (DEC-005). The passphrase is kept in the password
  manager; record its label in the table below. Supplied at run time through
  `sonoai.secure.open_store()`, never stored with the dataset.
- On disk: `style` (the line `enc1`) and `kdf.json` (salt and scrypt cost, not
  secret) in plaintext,
  `manifest.enc`, `blobs/xx/<hmac>.enc`. Nothing else; the check fails on any
  other file. File names, folder structure and file count by folder do not
  leak; total file count and blob sizes do.
- Self-contained: one blob per file, no links, so it survives the VMware
  shared folder, Windows copies and rsync unchanged.

## Content

Exactly the content of the `plain` dataset of the same version (see
`plain.md`), under the same logical paths:

- `images/...`: the image files, byte for byte (hierarchical tree, original
  names, `.png` / `.jpg` / `.bmp`); read with `store.read_image(...)`;
- `images/taskcrops_df.pkl`: the plain taskcrops table (`filepath2` relative
  to `images/`, with `np_md5_c3_current`, `height`, `width`);
- `labels/{flags,polygons}_df.pkl`: de-obfuscated label tables
  (`label`, and `x` / `y` in percent for polygons). `texts_df` was retired on 2026-10-27 (moved out of every dataset version, removed from `261023_enc1`); no dataset carries it.

The plain dataset's own `style` file is not copied into the store. No extra
tables. Tables are pandas 2.3.3 pickles (pinned in `requirements.txt`); the
training env on every machine must read them with a compatible pandas.

## Build and check

On the trusted workstation:

```bash
python scripts/make_enc_dataset.py <version>_plain <version>_enc1 [--root DIR]
python scripts/check_enc_dataset.py <version>_plain <version>_enc1 [--root DIR] --sample 0
```

- `--root` writes to `DIR/datasets/<codename>` instead of
  `$SONOAI_DATA_FILES_ROOT`, for when the data disk is too small. `DIR` may be
  a shared or remote disk: only ciphertext is written.
- An interrupted build resumes on re-run; `style` is written last, so a store
  without it is unfinished.
- The check decrypts every blob in RAM and compares it with the plain source,
  compares every table, and decodes a sample of images (all with
  `--sample 0`). A wrong passphrase fails the check at "manifest decrypts".

## Ship

```bash
gpu put <root>/datasets/<codename> data/datasets           # machine02
rsync -az <root>/datasets/<codename> root@<pod>:/workspace/data/datasets/   # RunPod
```

Train with `data.dataset: <codename>` (or `--dataset`).

## Datasets in this style

| Codename | Built from | Passphrase label | Date | Check |
|---|---|---|---|---|
| `261023_enc1` | `261023_plain` | _(fill in)_ | 2026-10-23 | all passed (`--sample 0`): 29,472 files, 4 tables, 29,468 images. 2026-10-27: `labels/texts_df.pkl` removed (`scripts/remove_from_enc_dataset.py`); all passed (`--sample 300`): 29,471 files, 3 tables |
