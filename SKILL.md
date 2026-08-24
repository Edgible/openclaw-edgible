---
name: edgible
description: "Edgible CLI for public https URLs on this machine: list apps (this serving device by default), create/publish a local port, delete/unpublish. Use when the user wants what is published, an Edgible URL, or to take one down."
version: 0.2.0
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

OpenClaw talks to this computer. Edgible is the door: `https://<app>.<org>.edgible.com` for a **local TCP port that is already listening**. Do not install Edgible, create an org, or register a device. Stop if `edgible` is missing or not logged in.

Helpers live next to this file. Prefer `{baseDir}/scripts/…`. If that path is missing, try `$HOME/.openclaw/workspace/skills/edgible/scripts/…`.

## WhatsApp noise

OpenClaw may attach hidden JSON (`chat_id`, `message_id`, `sender`, `e164`, `inbound_event_kind`). That is **not** the user request. Never print it. Run the helper for the real task.

## Dispatch

If they already said list / create / delete (or publish / unpublish / what’s on this box), **do not ask again**. First tool call is `exec`. One short line that you are running it.

| They said | Script |
| --- | --- |
| what’s published / my URLs / apps on this machine | `list.py` (default: **this box**) |
| whole org / every device | `list.py --all` |
| publish / create / Edgible this port | `create.py` — read `{baseDir}/references/create.md` if port, auth, or Control UI (18789) is involved |
| take down / unpublish / delete the Edgible URL | `delete.py` |

Default list is **this serving device**, not the org. `--all` only if they asked for every device.

If a helper asks for `--device-name`, retry with **this** machine from that error list — not another box in the org. Do not hardcode a device name.

## List

```bash
python3 -u "{baseDir}/scripts/list.py"
python3 -u "{baseDir}/scripts/list.py" --all
```

**Chat reply:** paste `SCOPE=`, `DEVICE=`, `COUNT=`, and each `NAME=… DEVICE=… URL=…` line. Every app line must include its `DEVICE=`. Do not stop on the tool card.

## Create

Ask only if **name**, **port**, or public vs org is missing. Then:

```bash
python3 -u "{baseDir}/scripts/create.py" --name <name> --port <port> --auth-modes <none|org|api-key>
```

Idempotent: existing name reprints `URL=`.

**Chat reply:** paste `URL=` (and `AUTH=` / `STATUS=` if present). Never end the turn with only a tool result and no URL in the bubble.

Never `--auth-modes none` on port **18789**. Details: `{baseDir}/references/create.md`. Safety: `{baseDir}/references/safety.md`.

## Delete

Needs the app **name**. Do not delete `openclaw` / `openclaw-ui` unless they said that name clearly. Does **not** stop Docker.

```bash
python3 -u "{baseDir}/scripts/delete.py" --name <name>
```

**Chat reply:** paste `STATUS=` (`deleted` or `missing`) and `NAME=` if present.

## Hard rules

- Default list is this device, not `--all`.
- Do not port-forward. Do not bind OpenClaw Gateway to `0.0.0.0`.
- Do not paste tokens, API keys, or WhatsApp session files.
- Do not publish through Edgible: WhatsApp, Telegram, Discord, or Ollama.
- Do not set OpenClaw `gateway.auth` to none.
- If exec needs approval, say so. If a helper fails, show stderr. Do not “fix” 18789 by switching to `none`.

## Not this skill

Installing Edgible, device register, Docker/nginx setup, Cursor ACP, WhatsApp plugin login.
