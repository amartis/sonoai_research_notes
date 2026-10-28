---
id: DEC-005
title: `enc1` dataset style and key handling for off-workstation training
status: accepted
created: 2026-10-22
from: []
related: [DEC-001, DEC-002]
superseded_by:
---
# DEC-005: `enc1` dataset style and key handling for off-workstation training

## Context

Training runs on machine02 (the Windows GPU box) and RunPod, which may only
hold encrypted data (DEC-001). The `plain` style (de-obfuscated tables, images
hard-linked to `submit1`) is workstation-only. T7-upload.ipynb started an
encrypted store by hand, under the old `imgs/` paths and with images only. We
need one shippable style that holds a whole dataset (images, `taskcrops_df`,
label tables) in the DEC-002 layout, plus a build and a check that prove it
equals its source.

## Decision

### Style `enc1`

- One `EncryptedStore` per dataset at `datasets/<version>_enc1/`, built from
  `<version>_plain` of the same version. **Everything is encrypted, images
  included.**
- Logical paths are the plain dataset's own paths (`images/...`,
  `images/taskcrops_df.pkl`, `labels/{flags,polygons,texts}_df.pkl`). The plain
  `style` file is not copied in.
- On disk: `style` (the line `enc1`) and `kdf.json` (scrypt salt and cost) in
  plaintext, `manifest.enc`, `blobs/xx/<hmac>.enc`. One blob per file, no links, so it survives the
  VMware share, Windows copies and rsync.
- The name is numbered like `submit1`: a later format change (another key,
  packed shards) becomes `enc2`.

### Encryption (`sonoai.secure`, unchanged)

Each file gets two independent treatments:

| | HMAC-SHA256(key, path) | AES-256-GCM(key, nonce, bytes, AAD = path) |
|---|---|---|
| Input | logical path | file contents |
| Output | blob file name | blob contents |
| Hides | what the file is called (case ids, folders) | what the file contains |
| Reversible | no (one-way) | yes, with the key |
| Deterministic | yes: same key + path → same name, so re-runs resume | no: a random nonce per write |

`manifest.enc` (AES-GCM, AAD `manifest`) maps each path to its blob, size and
plaintext sha256. Because the path is the AAD, a blob swapped with or renamed
to another fails to decrypt. Visible on disk: the number of files, blob sizes
(≈ file sizes) and timestamps.

### Key and credential handling

```
password manager ──type──▶ hidden prompt ──▶ scrypt(passphrase, salt from kdf.json) ──▶ 256-bit key in RAM ──▶ HMAC names + AES-GCM blobs ──▶ disk
```

- **A passphrase, not a raw key.** You type a passphrase of **at least 8
  characters**. It is stretched into the 256-bit key with scrypt (n = 2^18,
  r = 8, p = 1: 256 MiB and about 0.5 s per try on machine01). The same
  passphrase and salt always give the same key.
- **Salt** is 16 random bytes, made once per store and kept in plaintext in
  `kdf.json` with the scrypt cost. It isn't secret. It makes every store's key
  different even with the same passphrase, so precomputed guess tables are
  useless.
- **Strength.** Typing is easy, but security is now as strong as the
  passphrase. Anyone holding a store can guess offline, at scrypt speed. A
  random 8-character mixed passphrase holds up; a human-chosen word,
  name or date of 8 characters does not. **Prefer 3–5 random words.** The
  minimum (8) is the user's choice, enforced at creation only.
- **Typo protection.** A new store asks for the passphrase twice. Every later
  open asks once. A wrong passphrase gives a different key and fails at once
  (`DecryptionError` on the manifest). The check script asks again.
- **Same passphrase everywhere**: build, check, and every training run on
  every machine. Forgetting it makes the store unreadable; rebuild from
  `plain` with a new passphrase.
- **Entry** only through `sonoai.secure.open_store()`, which reads
  `kdf.json`, asks for the passphrase and derives the key. That means a hidden
  prompt: no echo, nothing in argv or shell history. On remote machines, type
  it into the run's tmux prompt. `SONOAI_DATA_PASSPHRASE` (e.g. a RunPod
  secret) is allowed for unattended runs and is removed from `os.environ`
  after it's read. `SONOAI_DATA_PASSPHRASE_FILE` is allowed only on a machine
  you control (chmod 600).
- **Never** in the repo, `.env`, the data root, the style docs, or a shared
  machine's disk. The derived key exists only in the RAM of the process
  using it.
- **Older stores** without `kdf.json` still open with a raw key
  (`sonoai-vault keygen`, `SONOAI_DATA_KEY`).
- **Assistants** (Claude Code) never ask for, see or store the passphrase. They
  start the command for you to type into, and read only its PASS/FAIL count output.

### Build and check

```bash
python scripts/make_enc_dataset.py <version>_plain <version>_enc1 [--root DIR]
python scripts/check_enc_dataset.py <version>_plain <version>_enc1 [--root DIR] --sample 0
```

Since DEC-008 these are `sonoai-data make-enc` and `sonoai-data check-enc`
(same arguments).

The build refuses a non-plain source, a version mismatch, an already-built
target and too little free space. It resumes if interrupted and writes `style`
last. The check asks for the passphrase again (a wrong one fails at once).
It then fails on any non-store file on disk, decrypts every blob in RAM and
compares it with the source bytes, compares every table, and decodes images
(all of them with `--sample 0`) and compares pixels and `np_md5_c3_current`.
Both print counts only. The style doc is `datasets/enc1.md`.

## Consequences

- Only `enc1` datasets are shipped (`gpu put` to machine02, rsync to RunPod
  Secure Cloud). `scripts/train.py` and the smoke config read `<version>_enc1`.
- The encrypted copy doubles disk use on the workstation (about 9.5 GB for
  `261023`). The root partition of machine01 was grown to 69 GB for this.
  `--root` can put the store on another disk; only ciphertext is written.
- Still accepted risks (DEC-001): plaintext in process RAM or GPU memory
  during runs, Windows paging, and a compromised cloud host.
- One passphrase for all datasets (each store has its own salt, so its own key).
  There's no rotation yet. Changing the passphrase means rebuilding the store and
  recording the new label.
- Security of shipped stores now depends on passphrase strength (see above),
  not on a 256-bit random key.
- Tables are pandas 2.3.3 pickles; training environments must use a
  compatible pandas.
