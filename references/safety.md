# Safety

These apply to every verb.

- Never `--auth-modes none` on port **18789** (OpenClaw Control UI). If create fails, show stderr; do not retry with `none`.
- Do not port-forward. Do not bind OpenClaw Gateway to `0.0.0.0`.
- Do not paste gateway tokens, API keys, or WhatsApp session files into chat.
- Do not publish through Edgible: WhatsApp, Telegram, Discord, or Ollama on the same box. Those are outbound clients, not websites.
- Do not set OpenClaw `gateway.auth` to none.
- Delete only the named app. Never `edgible app delete` without `--name` or `--app-id`. Do not delete serving devices, orgs, or OpenClaw config.
- Delete does not stop Docker unless they asked. The skill removes the hostname, not the container.
