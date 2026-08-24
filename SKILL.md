---
name: edgible
description: "Edgible CLI on this machine. Use for public https URLs (list/create/delete apps on this serving device), --version, device health, agent status, app get/events, and any other edgible subcommand the user names. Prefer running `edgible` with their args; use the python helpers only for app list/create-existing/delete."
version: 0.3.0
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

Default: run the **edgible CLI** with the user’s words as argv. Same idea as `/skill edgible --version` → `edgible --version`.

```bash
edgible --version
edgible device list --type serving --json
edgible app get --app-id <id> --json
edgible --help
edgible app --help
```

- If the remainder looks like CLI args (`--version`, `device health`, `app events`, `agent status`), run `edgible` plus those args. First tool call is `exec`. Do not ask again.
- Add `--json` when the command supports it and they want a list/status. Add `--non-interactive` on mutating commands **after** they confirmed (see below).
- There is **no** `edgible whoami`. If they said whoami, run `edgible --help` or `edgible config get email` (never dump `config list` — it can contain passwords).
- If unsure which subcommand, `edgible --help` or `edgible <group> --help`. Do not invent verbs.
- Interactive TTY does not work in chat: no `edgible app ssh` without `--command`, no `agent logs -f`, no interactive `auth login` / `auth select-org`.

## Helpers (only these three)

Use `{baseDir}/scripts/…` instead of raw `edgible app …` when:

| They said | Helper |
| --- | --- |
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
