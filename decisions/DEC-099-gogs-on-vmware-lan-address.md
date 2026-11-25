---
id: DEC-099
title: Gogs listens on machine01's VMware LAN address instead of localhost, and runs without a login (amends DEC-014)
status: accepted
area: [infra]
created: 2026-11-24
from: []
related: [DEC-014, DEC-078]
superseded_by:
---
# DEC-099: Gogs listens on the VMware LAN address

> Number: this record was `DEC-090` until 2026-11-25. Two records had that number, made in two
> clones at once; this one, not yet shared, took a new number ([DEC-093](DEC-093-id-ledger-number-reservations-task-claims-offline-modes.md)). Commits up to then
> cite it as `DEC-090`.

## Context

[DEC-014](DEC-014-gogs-git-remote.md) binds Gogs (web and built-in SSH) to `127.0.0.1`, so
only machine01 can reach it. The user asked for Gogs to be reachable from outside
localhost (2026-11-24). Gogs takes one listen address for web and one for SSH, so it can
listen on localhost or on a LAN address, not both. machine01 has two outside interfaces: the
VMware network (`ens33`, address from VMware's DHCP) and a VPN tunnel (`tun0`).

## Decision

1. **Address.** Web (port 3000) and SSH (port 2222) listen on machine01's VMware LAN
   address, `192.168.65.131`, not on `0.0.0.0`, so the VPN side stays closed.
   `DOMAIN`, `SSH_DOMAIN`, `EXTERNAL_URL` and `LOCAL_ROOT_URL` use that address too.
2. **Remotes.** The `gogs` remotes of the code repo and `research_notes/` point at
   `ssh://git@192.168.65.131:2222/...`. The server's host key is unchanged.
3. **Always on.** Linger is enabled for the service user, so Gogs starts at boot and
   keeps running without a login session.
4. **Unchanged from DEC-014:** sign-in is required to view anything, registration is off,
   the content rules stand, and pushing still needs the user's go-ahead.

## Consequences

- Machines that can reach the VMware network (machine02 by default; others only through
  port forwarding on machine02) can open the web UI and use git over SSH. Checked from
  machine02 on 2026-11-24: web answers, SSH port open.
- Localhost no longer works: `localhost:3000` and `localhost:2222` refuse connections.
- If VMware's DHCP gives machine01 another address, Gogs fails to start and the remotes
  break. Fix: a DHCP reservation or static address, or update `app.ini` and the remotes.
- DEC-014's reason for accepting Gogs ("it listens on localhost only and has one user")
  now rests on the VMware network being private to machine02. The firewall on machine01
  was not checked (it needs `sudo`).
- Undo: restore `app.ini.bak-20261124` beside `app.ini`, restart the service, and set the
  remotes back to `localhost`.
