# Edgible CLI (production)

`edgible` / `edgible --help`. Alias: `app` = `application`, `dev` = `device`, `gw` = `gateway`.

If the user passed CLI-shaped text after `/skill edgible` (`whoami`, `doctor`, `--version`, `device list`, …), run `edgible` with those args **verbatim**. Never treat that token as an application name. Never fall back to `list.py`.

## Global

| Command | Notes |
| --- | --- |
| `edgible whoami` | Active session: Profile, Environment, Account, Organization |
| `edgible doctor` | Diagnostics. `/skill edgible doctor` must run this, not app list |
| `edgible --version` | CLI version on PATH |
| `edgible --help` | Groups |
| `edgible --plain` | No color (good for chat) |

## `app` / `application`

| Command | Skill |
| --- | --- |
| `app list` | Helper `list.py` (this device) or `list.py --all` |
| `app create existing` | Helper `create.py` for a local listening port |
| `app create docker-compose` | Pass-through; needs compose file + device |
| `app create managed-process` | Pass-through; agent runs a command |
| `app create vm` | Pass-through; QEMU/etc. |
| `app create docker` / `podman` | **Stubs — do not use** |
| `app get` / `status` / `info` | `--app-id` `--json` |
| `app events` | `--app-id` `--json` |
| `app update` | auth modes, name, target-state |
| `app delete` / `rm` | Helper `delete.py` |
| `app api-keys` list/create/delete | Confirm create/delete; **never paste the secret key** |
| `app short-codes` list/create/delete/toggle | Confirm mutating |
| `app ssh` | Only with `--command`; no interactive shell |

## `device` / `dev`

| Command | Skill |
| --- | --- |
| `device list` | `--json`; `--type serving` or `gateway` |
| `device health` | This box unless they named another; `--name` `--json` `--non-interactive` |
| `device application-health` | `--name` `--json` |
| `device telemetry` | `--device-id` `--json` |
| `device delete` | Confirm first |

## `auth`

| Command | Skill |
| --- | --- |
| `whoami` (top-level) | Session: profile, environment, account, org |
| `auth login` | Interactive / passwords — **do not run in chat** |
| `auth logout` | Confirm first |
| `auth select-org` | Interactive — do not run |

Never dump `config list` (can contain `devicePassword`).

## `agent` (local daemon)

`status`, `logs` (not `--follow`), `start` / `stop` / `restart` (confirm stop), `set-log-level`, `setup`, `install` (confirm), `uninstall` (confirm).

## `discover`

`tools`, `workloads --json`, `capabilities` / `caps --json`.

## `connectivity`

`connectivity test --host --port` (application-id path is unimplemented in CLI).

## `stack`

`validate`, `diff`, `status --json` are fine. `deploy` / `teardown`: confirm.

## `gateway` / `gw`

`list`, `get` are fine. `create` (EC2), `delete`, `resync`, `wipe-logs`: confirm. `ssh` / `logs`: no interactive; `logs` without follow.

## `ai` (Ollama)

`status`, `test` are fine. `setup` / `serve` / `stop` / `teardown`: confirm. Do not expose Ollama through Edgible as a public `none` app.

## `config`

`get <key>` only for non-secret keys (`email`, not `devicePassword`). Never `config list` or `config reset` without confirm (`reset` wipes login).

## Not in production builds

`debug …`, `managed-gateway …` — only if `ENABLE_DEBUG_COMMANDS=true`. Do not offer them.
