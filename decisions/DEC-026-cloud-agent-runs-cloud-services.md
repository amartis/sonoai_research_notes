---
id: DEC-026
title: A cloud agent runs the cloud services, with shell commands on aws-labelstud and a log of its actions
status: accepted
area: [aws]
created: 2026-10-29
from: []
related: [DEC-023, DEC-024, DEC-025]
superseded_by:
---
# DEC-026: A cloud agent runs the cloud services, with shell commands on aws-labelstud and a log of its actions

## Context

[DEC-024](DEC-024-plain-never-leaves-machine01-ec2-label-studio-decrypts-in-ram.md) and [DEC-025](DEC-025-aws-labelstud-public-https.md) kept agents out of shells on aws-labelstud (port forwarding only),
so every setup step on the instance needed the user. On 2026-10-29 the user asked for
more agent control: a subagent that handles the cloud services and does most of the
development work (start and stop instances, shell access, setting up tools), and that
leaves a brief log of what it did.

## Decision

- **Cloud agent** (`.claude/agents/cloud.md`, assignee `@cloud`): owns AWS work
  (S3 bucket, aws-labelstud, CloudFormation stacks), one task or request per run.
- **Shell commands through SSM Run Command**, not SSH: `sonoai-aws-labelstud run "<cmd>"`
  sends `AWS-RunShellScript` to instances tagged `Project=sonoai-labelstudio` only.
  Port 22 stays closed and there is no key pair. Interactive shell sessions stay denied
  to the agent.
- **Allowed without asking**: start and stop aws-labelstud, run setup and admin
  commands there (packages, services, Caddy, updates, logs of services), push code and
  config, toggle idle stop, update the two existing stacks.
- **Still asks**: creating or deleting stacks, buckets or instances; changing the
  instance type or anything else that raises cost; opening a port; uploading data
  (`push-s3`, `push-images`).
- **Still never**: reading Label Studio's database, exports or uploads; attaching to the
  image server's tmux or reading its memory; typing or handling the passphrase; creating
  Label Studio accounts or handling passwords or tokens. `run` refuses commands that name
  those places, and the patient-data hook refuses ones that name plain data.
- **Log**: every `sonoai-aws-labelstud` action appends one line (UTC time, actor, action,
  target, short detail; never command output) to `logs/cloud-agent.md` on machine01
  (not committed). Actions done another way (e.g. a stack update through the AWS MCP
  tool) are logged with `sonoai-aws-labelstud log "<text>"`. CloudTrail keeps AWS's own record.

## Consequences

- Amends DEC-024 and DEC-025 on agent shells: the agent can now run commands on the
  instance that holds the Label Studio state and, while the image server runs, the key in
  RAM. The rules above and the IAM tag condition limit this; they do not make it
  impossible for a misbehaving agent.
- The user applies the IAM policy change (Run Command) in the console.
- Fewer steps need the user; the account creation and the passphrase still do.
