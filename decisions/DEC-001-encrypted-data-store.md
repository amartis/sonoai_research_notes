---
id: DEC-001
title: Encrypted data store for all off-workstation data
status: accepted
area: [data-security]
created: 2026-10-22
from: []
related: []
superseded_by:
---
# DEC-001: Encrypted data store for all off-workstation data

## Context

Images and labels are patient data. Training runs on a shared Windows GPU box
and on RunPod, neither of which should ever hold plaintext on disk.

## Decision

All data leaving the trusted workstation is an `EncryptedStore`
(AES-256-GCM, HMAC-named blobs, encrypted manifest; `sonoai.secure`). The key
is a random 256-bit key kept in a password manager and supplied at runtime.

## Consequences

- Decryption happens in RAM; memory scraping, Windows paging, and a compromised
  cloud host remain out of scope for now.
- RunPod: Secure Cloud only.
