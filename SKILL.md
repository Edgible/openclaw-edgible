---
name: edgible
description: "Edgible CLI pass-through on this machine. /skill edgible <args> means run `edgible <args>` (whoami, doctor, --version, device, app, agent, …). Do not list apps unless they asked what is published. Python helpers only for app list/create-existing/delete."
version: 0.3.2
metadata:
  openclaw:
    requires:
      bins:
        - edgible
        - python3
    emoji: "🚪"
    homepage: https://github.com/Edgible/openclaw-edgible
---

# Edgible

OpenClaw talks to this computer. Edgible is the door. Stop if `edgible` is missing. Do not install Edgible, create an org, or register a device unless they clearly asked.

`{baseDir}` is already an **absolute** directory. Never `~` in exec. **Never set exec `workdir`.**

Full command list: `{baseDir}/references/cli.md`. Safety: `{baseDir}/references/safety.md`. Create fields: `{baseDir}/references/create.md`.

## How to exec

**Pass-through first.** `/skill edgible` plus a CLI token means run that CLI. Copy the remainder **verbatim**. Do not correct spelling into an app name (`doctor` is not `dcotr`, not an app to list).

```bash
edgible whoami
edgible doctor
edgible --version
edgible device list --type serving --json
edgible app get --app-id <id> --json
edgible --help
```

| Remainder | Exec |
| --- | --- |
| `whoami`, `doctor`, `--version`, `device …`, `app …`, `agent …`, `auth …`, `stack …`, `gateway …`, `discover …`, `config …`, `ai …`, `connectivity …`, or any other first token | `edgible` + **exact** remainder. Not `list.py`. |
| English: what’s published / my URLs / apps on this box (no CLI verb) | `list.py` |
| English: publish this port | `create.py` |
| English: take down that app URL | `delete.py` |
| Unknown English, no CLI verb | `edgible --help` — still not `list.py` |

- First tool call is `exec`. Do not ask again when the remainder is already a CLI command.
- `whoami` → paste Profile / Environment / Account / Organization.
- `doctor` → paste the doctor report. It is a real top-level command, not app list.
- `--plain` if the CLI output is colored. `--json` only when that command supports it and they want machine output.
- `--non-interactive` on mutating commands **after** they confirmed.
- No interactive TTY: no `app ssh` without `--command`, no `agent logs -f`, no `auth login` / `auth select-org`.

## Helpers (only these three)

Use `{baseDir}/scripts/…` **only** for English app list/create/delete. Never for `whoami`, `doctor`, `--version`, or any other CLI verb.

| They said | Exec |
| --- | --- |
| `whoami` / `doctor` / other CLI verb | `edgible` + exact args |
| what’s published / URLs / apps on **this** machine | `list.py` (not whole org) |
| whole org / every device | `list.py --all` |
| publish / create a URL for a **local listening port** | `create.py` (`app create existing`) |
| take down / unpublish / delete that Edgible **app** | `delete.py` |

```bash
python3 -u {baseDir}/scripts/list.py
python3 -u {baseDir}/scripts/create.py --name <name> --port <port> --auth-modes <none|org|api-key>
python3 -u {baseDir}/scripts/delete.py --name <name>
```

If a helper asks for `--device-name`, retry with **this** machine from that error, not another box. Never `--auth-modes none` on port **18789**.

**Chat reply:** paste helper `NAME=` / `URL=` / `STATUS=` / `DEVICE=` lines, or the CLI stdout. Do not stop on the tool card. Never print WhatsApp `chat_id` JSON.

## Confirm first (do not exec yet)

Ask one yes/no, then run with `--non-interactive` / `--force` only if they said yes:

- `device delete`, `gateway create` / `delete` / `resync` (EC2), `agent uninstall` / `stop`, `stack deploy` / `teardown`, `config reset`, `auth logout`, `ai teardown`, `app api-keys create` / `delete`

## Never

- Passwords, tokens, API keys, `config list`, `DEVICE_PASSWORD`, WhatsApp session files in the bubble.
- `gateway create` / AWS spend without an explicit yes.
- Publish WhatsApp / Telegram / Discord / Ollama through Edgible.
- Port-forward or bind OpenClaw Gateway to `0.0.0.0`.
- `app create docker` / `podman` (stubs). Prefer `create.py` for an existing port.
- Debug / `managed-gateway` (not in production CLI).

## Not this skill

Installing the Edgible CLI, Docker/nginx setup, Cursor ACP, WhatsApp plugin login.
