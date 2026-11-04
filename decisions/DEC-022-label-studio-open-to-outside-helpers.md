---
id: DEC-022
title: Label Studio may be opened to outside helpers for a labeling session
status: proposed
area: [labeling, data-security]
created: 2026-10-29
from: []
related: [DEC-019, DEC-018]
superseded_by:
---
# DEC-022: Label Studio may be opened to outside helpers for a labeling session

## Context

The user wants third-party helpers to label review projects from their own
machines, through a port forward to a public IP (2026-10-29). [DEC-019](DEC-019-label-studio-review-projects.md) binds
Label Studio to `127.0.0.1` on machine01 only, and [DEC-018](DEC-018-plain-style-for-local-research.md) keeps plain-style data
on machine01.

Before deciding, these risks were put to the user (checked in the Label Studio
1.23.0 source):

- Helpers see plain patient images outside machine01; images and their paths
  can hold case identifiers.
- The open-source edition's project access check always allows
  (`projects/mixins.py`). Every account can open and export every project, and
  load any image under a project's local-storage folder (the dataset's whole
  `images/` folder), not only the sampled frames.
- `label-studio start` runs Django's development server over plain HTTP
  (`server.py`), so passwords, session cookies and the API token cross the
  network unencrypted.

The recommended alternative was a separate helper instance holding only the
frames cleared for helpers, behind HTTPS. The user chose to open the existing
instance and accepted the risks above. Whether these helpers may see the images
(consent, approvals, agreements) is the user's responsibility and is not
recorded here.

## Decision

- Label Studio stays bound to `127.0.0.1` by default. For a session with
  helpers, the user starts it with
  `scripts/servers.sh labelstudio --labelstudio-host 0.0.0.0 --labelstudio-port <port>`
  (first use: port 50630). The address is set per run (`SONOAI_LABELSTUDIO_BIND`,
  never in `.env`), and the script prints a warning while it is open.
- When open, `LABEL_STUDIO_HOST` is empty, so links and redirects are relative
  and work at whatever address the helper uses.
- The user sets up the port forward (router to machine02, machine02 to the
  machine01 VM) and creates one account per helper through an invite link;
  sign-up without a link stays disabled. Agents do neither, and never open the
  port unless the user asks for that run.
- The server is stopped (Ctrl-C) when the helpers are done; the next plain start
  is local only.
- This amends DEC-019 ("bound to `127.0.0.1:8080`") and DEC-018 (plain data stays
  on machine01) for the images Label Studio serves during such a session. The rest
  of both stays as it is. Implemented in [TASK-043](../../backlog/archive/tasks/task-043%20-%20Label-Studio-bind-address-option-for-outside-helpers-DEC-022.md).

## Consequences

- Helpers can label in the browser without access to machine01 itself.
- Exposure is all of Label Studio, not one project: every helper account can see
  every project and its images, and can export them.
- Traffic, including passwords and the API token, is unencrypted on the internet.
  An HTTPS reverse proxy in front, or a separate helper instance with only cleared
  frames, would reduce this; neither is in place.
- The login page is reachable by anyone while the forward is open; only the
  accounts' passwords protect it.
