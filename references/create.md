# Create (publish) an Edgible app

Runs `edgible app create existing` for a local listening port, waits until the certificate is ready, returns `https://<app>.<org>.edgible.com`.

## Collect (ask only if missing)

| Field | Notes |
| --- | --- |
| **name** | DNS label: lowercase, digits, hyphens. Examples: `hello-world`, `skill-test`, `openclaw-ui`. |
| **port** | Local listen port (nginx Hello World is often **8081**; skill-test **8082**; OpenClaw Control UI **18789**). |
| **auth** | `none` (public), `org` (must sign in), or `api-key` (Bearer). |

Defaults:

- Port **18789** → `org`. Never `none`.
- A throwaway public page (Hello World / skill-test) → `none`, but **confirm** before `none`.
- Anything that looks like a dashboard, Gateway, or private tool → `org`.

Optional: `--device-name` / `--device-id` only if the helper says there are several serving devices. Use this OpenClaw box.

## After Control UI (port 18789)

- `openclaw config set gateway.controlUi.allowedOrigins` must include `https://` + that exact hostname
- `openclaw gateway restart`
- First browser: gateway token + `openclaw devices approve`
