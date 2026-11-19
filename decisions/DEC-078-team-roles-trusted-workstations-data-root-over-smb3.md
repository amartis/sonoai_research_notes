---
id: DEC-078
title: Team roles (team lead, senior, junior); machine01 is any trusted workstation; the data root is shared with a senior's workstation over encrypted SMB3
status: accepted
area: [data-security, infra, workflow]
created: 2026-11-19
from: []
related: [DEC-024, DEC-018, DEC-052, DEC-053, DEC-019, DEC-028]
superseded_by:
---
# DEC-078: Team roles; machine01 is any trusted workstation; data root over SMB3

## Context

On 2026-11-19 a second developer joined the project. Until then one person did all the work, on
one Ubuntu VM (machine01) that is a guest on the Windows host machine02. Every rule assumed this
single person ("the user") and this single machine. [DEC-024](DEC-024-plain-never-leaves-machine01-ec2-label-studio-decrypts-in-ram.md)
says plain-style data never leaves machine01. [DEC-018](DEC-018-plain-style-for-local-research.md)
says local research uses the plain style.

The user wants the new developer to work with the same privileges, and to read the data root
(`$SONOAI_DATA_FILES_ROOT`) without a second copy, to save disk space, through a Samba share.
The data root holds the plain style, so DEC-024 has to change. Asked in chat, the user:

- chose to make the second VM a trusted workstation (not a share of the enc1 style only);
- confirmed that the second VM is also a guest on machine02, on the same VMware network;
- left the junior role to be defined later.

The names "team lead" (not "lead", which already names the `/lead` session), machine01-host and
machine01-senior were proposed by Claude, not chosen by the user; accepting this DEC confirms them.

## Decision

- **Roles.** There are three roles: **lead**, **senior** and **junior**, with two privilege levels:
  - The team lead and a senior have the same privileges. Wherever the rules (`CLAUDE.md`, the command
    policy, the skills and agents) say "the user", they mean the team lead or a senior.
  - The team lead also guides onboarding and hosts shared files, first of all the data root.
  - The junior role is open. Until it is defined, a junior gets no access to patient data: no
    data share and no passphrase.
- **machine01 is a class of machine.** machine01 means any **trusted workstation**: an Ubuntu VM
  that is a guest on machine02, listed in [docs/team.md](../../docs/team.md), used by a team lead or a
  senior, and with this repo's Claude Code hooks enabled.
  - Today there are two: **machine01-host**, which hosts the data root, and
    **machine01-senior**, which mounts it.
  - Every rule that says "machine01" (DEC-024, DEC-018, `CLAUDE.md`, the hooks, the command
    policy) holds for each of them. "Plain data never leaves machine01" now means it never
    leaves the trusted workstations.
- **The data root is shared over Samba, on these terms:**
  - machine01-host serves it as one share, using SMB 3.1.1 only, with encryption required.
  - Samba listens on loopback and the VMware network interface only. It accepts only the listed
    trusted workstations: no guest access, and no address outside the list.
  - Each senior has their own Samba-only login, with no shell. Files are written as the team lead's
    user (`force user`), so the data root keeps its owner and permissions.
  - The share is read-write. [DEC-053](DEC-053-table-naming-and-preservation.md) still applies:
    a table, once written, is not changed, so two writers do not overwrite each other.
  - The senior mounts the share with encryption on (`seal`) and without the client disk cache
    (no `fsc`). Nothing from the share is copied to the senior's local disk. The rules against
    temp files, caches and exported crops apply there as on machine01-host.
- **Label Studio** ([DEC-019](DEC-019-label-studio-review-projects.md)) runs on machine01-host
  only. Its state folder sits under the data root, and two servers on one SQLite database over
  SMB would corrupt it.

## Consequences

- Amends DEC-024 and DEC-018: "machine01" is read as "any trusted workstation". The enc1-only
  rule for everything else stays: the GPU box, RunPod, S3 and EC2 still get only enc1.
- [docs/team.md](../../docs/team.md) holds the roles and the list of trusted workstations.
  Adding a workstation is a change to that list, and the team lead makes it.
- The hook needs no change. On machine01-senior, `SONOAI_DATA_FILES_ROOT` points at the mount, so
  the hook protects the share there as it protects the data root on machine01-host.
- The senior's work with data depends on machine01-host being up. The team lead's disk takes the
  senior's writes; on 2026-11-19 it had 2.2 GB free of 69 GB.
- Two people now create board tasks and records on two machines, and both use one GPU-box
  folder. ID collisions, the push workflow and a GPU-box folder per person are separate tasks.
