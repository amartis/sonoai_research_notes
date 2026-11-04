---
id: DEC-027
title: The cloud agent has SSH access to aws-labelstud, through SSM (no open port)
status: accepted
area: [aws]
created: 2026-10-29
from: []
related: [DEC-025, DEC-026]
superseded_by:
---
# DEC-027: The cloud agent has SSH access to aws-labelstud, through SSM (no open port)

## Context

[DEC-026](DEC-026-cloud-agent-runs-cloud-services.md) gave the cloud agent shell commands on aws-labelstud through SSM Run Command,
which cannot answer prompts, and kept SSH out ("no SSH, port 22 closed"). Creating the
Label Studio admin account needs an interactive prompt that the user answers. On
2026-10-29 the user asked that the agent have SSH access, and chose SSH through SSM over
plain SSH on port 22 after comparing them (no open port, works when machine01's VPN
address changes, AWS sign-in needed as well as the key).

## Decision

- **SSH through SSM**: `ssh aws-labelstud` uses the `AWS-StartSSHSession` document as a
  proxy. Port 22 stays closed; the security group keeps 443 only ([DEC-025](DEC-025-aws-labelstud-public-https.md)).
- **IAM** (deploy policy, version v5 in IAM): `ssm:StartSession` with `AWS-StartSSHSession` or
  `AWS-StartPortForwardingSession`, only on instances tagged `Project=sonoai-labelstudio`.
  Other session documents (interactive SSM shells) stay denied.
- **On machine01**: the Session Manager plugin in `~/.local/bin` (no root), a key made for
  this only (`~/.ssh/aws-labelstud`, never printed or copied off machine01), and an
  `~/.ssh/config` entry, all made by `sonoai-aws-labelstud ssh-setup`. The public key is
  in `/home/ubuntu/.ssh/authorized_keys` on the instance.
- **Use**: `sonoai-aws-labelstud ssh ["<command>"]` logs the session to
  `logs/cloud-agent.md`, refuses the commands that `run` refuses, and connects. For prompts
  that need the user (passwords), the agent opens the session in a terminal tab and the
  user types the answer; the agent does not read the terminal while they do.
- The DEC-026 limits stay: no Label Studio data, image server session or memory,
  passphrase, accounts or passwords.

## Consequences

- AWS records that a session started (CloudTrail) but not what happens in it; our log
  has one line per session. Commands typed inside an interactive session are not checked
  by `run`'s guard: the agent's rules are the only limit there.
- To revoke: remove the key from `authorized_keys` (or restore an older policy version); delete
  `~/.ssh/aws-labelstud` and the config entry on machine01.
- If the stack is recreated, the instance ID changes: run `ssh-setup` again.
