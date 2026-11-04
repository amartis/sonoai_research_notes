---
id: DEC-023
title: AWS S3 hosts the enc1 dataset files; EC2 hosts the Label Studio server
status: accepted
area: [aws, data-security]
created: 2026-10-29
from: []
related: [DEC-018, DEC-019, DEC-022]
superseded_by:
---
# DEC-023: AWS S3 hosts the enc1 dataset files; EC2 hosts the Label Studio server

## Context

The AWS CLI and the Agent Toolkit for AWS were set up on machine01 (2026-10-29),
with a dedicated IAM user for agents (`claude-agent`, console sign-in through
`aws login`, no access keys). The user compared two ways of hosting files on
AWS: an S3 bucket (object storage, served over HTTPS, managed durability, pay
per GB) and the disk of an EC2 instance (block storage tied to one machine,
low latency, needs a server and upkeep).

Until now only the encrypted store (enc1) may leave machine01, and only to the
Windows GPU box or RunPod (`CLAUDE.md`). Label Studio runs on machine01
([DEC-019](DEC-019-label-studio-review-projects.md), [DEC-022](DEC-022-label-studio-open-to-outside-helpers.md)).

## Decision

- **S3** hosts static files: the enc1-style dataset files. Only enc1 files go
  to S3, never plain-style data. S3 becomes an allowed destination for the
  encrypted store, alongside the GPU box and RunPod.
- **EC2** hosts the Label Studio server.

## Consequences

- enc1 files on S3 can be fetched from anywhere the key is available (GPU box,
  RunPod, EC2) without copying them from machine01 each time.
- **Open: Label Studio data on EC2.** Label Studio shows plain images and stores
  labels. Running it on EC2 means patient images (decrypted, at least in memory)
  and labels live on an AWS machine. This goes beyond "only the encrypted store
  leaves machine01" and [DEC-018](DEC-018-plain-style-for-local-research.md). How images reach Label Studio on EC2 (decrypt
  in memory from S3, or a plain copy on the instance disk), how the key gets
  there, and HTTPS and access control must be decided before any real data is
  loaded there.
- The `claude-agent` IAM policy does not yet allow this: it has no EC2 access,
  and S3 only for buckets named `claude-agent-*`. It must be extended (and the
  `CLAUDE.md` rule on where the encrypted store may go updated) before agents
  do this work.
- Costs: S3 storage and download charges, plus the EC2 instance running while
  Label Studio is up.
