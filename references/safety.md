# Safety

These apply to every verb, including raw `edgible` pass-through.

- Never `--auth-modes none` on port **18789** (OpenClaw Control UI). If create fails, show stderr; do not retry with `none`.
- Do not port-forward. Do not bind OpenClaw Gateway to `0.0.0.0`.
- Do not paste gateway tokens, API keys, device passwords, or WhatsApp session files into chat. Never run `edgible config list` (config JSON can include `devicePassword`).
- Do not publish through Edgible: WhatsApp, Telegram, Discord, or Ollama on the same box. Those are outbound clients, not websites.
- Do not set OpenClaw `gateway.auth` to none.
- App delete: only the named app. Helper `delete.py` preferred. Do not delete serving devices, orgs, or OpenClaw config unless they confirmed `device delete` / `config reset`.
- App delete does not stop Docker unless they asked. The skill removes the hostname, not the container.
- Confirm before: `device delete`, `gateway create`/`delete`, `agent uninstall`/`stop`, `stack deploy`/`teardown`, `auth logout`, `config reset`, `ai teardown`.
- No interactive TTY: `auth login`, `auth select-org`, `app ssh` without `--command`, `agent logs --follow`.
- Never set exec `workdir`. Never use `~` in the exec command or workdir.
