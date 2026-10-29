---
id: DEC-025
title: aws-labelstud, the Label Studio server on EC2, is reached over public HTTPS; first project's images only; idle stop
status: accepted
created: 2026-10-29
from: []
related: [DEC-019, DEC-022, DEC-023, DEC-024]
superseded_by:
---
# DEC-025: aws-labelstud, the Label Studio server on EC2, is reached over public HTTPS; first project's images only; idle stop

## Context

[TASK-032](../../backlog/tasks/task-032%20-%20Run-the-B-mode-cropper-on-a-dataset-version-polygon-check-reviewed-set-box-table-DEC-017.md) (review of the B-mode cropper's boxes, [DEC-017](DEC-017-bmode-cropper.md)) is to be labelled by a remote
assistant, on the Label Studio server on EC2 from [DEC-023](DEC-023-aws-s3-for-enc1-and-ec2-for-label-studio.md) and [DEC-024](DEC-024-plain-never-leaves-machine01-ec2-label-studio-decrypts-in-ram.md). DEC-024 allowed
access by SSM port forwarding only, which needs AWS credentials the assistant does not
have. On 2026-10-29 the user chose the setup below in chat.

## Decision

- **Name**: the server is **aws-labelstud** (stack, instance Name tag, role, config file
  `configs/aws/aws-labelstud.yaml`, docs). Listed in `docs/services.md`.
- **Hardware**: us-east-1, Ubuntu 24.04 LTS, t3a.medium (2 vCPU, 4 GiB; $0.0376/h on
  demand, from instances.vantage.sh, a third-party price list), CPU credits `standard`
  (no surplus charges), 20 GB gp3 root volume, encrypted.
- **Access: public HTTPS**, amending DEC-024. Caddy serves port 443 with a Let's
  Encrypt certificate for `<elastic-ip>.sslip.io`. Port 443 is open to the internet
  (certificate issuance and renewal need it); the Label Studio login protects it, and
  sign-up without an invite link stays off. Images (`/img/...`) are served only to
  logged-in users (Caddy asks Label Studio first). No SSH; shells go through SSM.
- **No file names on AWS**: tasks point at `/img/<version>_enc1/<blob-id>`, the store's
  HMAC blob name; the blob-id to path table stays on machine01, in the plain dataset's
  `derived/labeling/<project>/`.
- **S3 holds only the first labeling project's encrypted blobs** (the TASK-032 sample),
  not the whole dataset.
- **Accounts**: the user creates the admin account in a shell session on the instance;
  the assistant joins through an invite link and sets their own password. Agents
  create no accounts and handle no passwords (as in [DEC-019](DEC-019-label-studio-review-projects.md)).
- **Idle stop**: `idle_stop.enabled` (default `false`) and `idle_stop.hours` in the
  config. When enabled, a timer on the instance powers it off (shutdown behaviour: stop)
  after that many hours without labeling activity. The user or an agent turns it on or
  off with `sonoai-aws-labelstud idle-stop on|off`.

## Consequences

- The login page can be reached from the internet: weak passwords are the main risk.
  Plain HTTP is never served.
- The assistant's browser displays decrypted images (as in [DEC-022](DEC-022-label-studio-open-to-outside-helpers.md)).
- Every image server start, including after an idle stop, needs the user to type the
  passphrase over SSM.
- Costs: the instance only while it runs, and the Elastic IP's public IPv4 charge even
  while stopped.
- The agent's IAM policy needs Elastic IP and security-group ingress actions; the user
  applies them.
