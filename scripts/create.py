#!/usr/bin/env python3
"""Create or reuse an Edgible app for a local listening port. Print the https URL."""

from __future__ import annotations

import argparse
import re
import time

from common import app_url, die, find_apps_by_name, log, pick_device, require_edgible, run_edgible

NAME_RE = re.compile(r"^[a-z0-9]([a-z0-9-]{0,62}[a-z0-9])?$")
ALLOWED_AUTH = {"none", "org", "api-key"}
ORG_ONLY_PORTS = {18789}
POLL_SECONDS = 5
POLL_ATTEMPTS = 18  # ~90s, first-publish cert wait


def parse_auth(raw: str) -> str:
    parts = [p.strip().lower() for p in raw.split(",") if p.strip()]
    if not parts:
        die("--auth-modes is empty")
    unknown = [p for p in parts if p not in ALLOWED_AUTH]
    if unknown:
        die(f"Unknown auth mode(s): {', '.join(unknown)}. Use none, org, and/or api-key.")
    order = ["org", "api-key", "none"]
    return ",".join(m for m in order if m in parts)


def wait_for_url(app_id: str) -> str:
    url = ""
    for _ in range(POLL_ATTEMPTS):
        url = app_url(app_id)
        if url.startswith("https://"):
            return url.rstrip("/")
        time.sleep(POLL_SECONDS)
    extra = f" last value: {url}" if url else ""
    die(
        "Certificate/URL not ready after ~90s. Check Certificates in "
        f"https://app.prod.edgible.com/ then `edgible app get --app-id {app_id}`.{extra}"
    )


def create_app(name: str, port: int, auth: str, device_id: str) -> None:
    run_edgible(
        [
            "app",
            "create",
            "existing",
            "--non-interactive",
            "--name",
            name,
            "--port",
            str(port),
            "--protocol",
            "http",
            "--https-upgrade",
            "--auth-modes",
            auth,
            "--device-id",
            device_id,
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Publish a local port through Edgible (existing workload)."
    )
    parser.add_argument("--name", required=True, help="Application name (DNS label)")
    parser.add_argument("--port", required=True, type=int, help="Local TCP port already listening")
    parser.add_argument(
        "--auth-modes",
        required=True,
        help="none (public), org (sign-in), api-key, or comma-separated",
    )
    parser.add_argument("--device-id", help="Serving device id")
    parser.add_argument("--device-name", help="Serving device name (this machine)")
    args = parser.parse_args()

    require_edgible()
    log("edgible create: starting")

    name = args.name.strip().lower()
    if not NAME_RE.match(name):
        die("--name must be a lowercase DNS label (letters, digits, hyphens).")

    port = args.port
    if port < 1 or port > 65535:
        die("--port must be 1–65535")

    auth = parse_auth(args.auth_modes)
    modes = set(auth.split(","))
    if port in ORG_ONLY_PORTS and "none" in modes:
        die(
            f"Port {port} is OpenClaw Control UI. Use --auth-modes org "
            "(never none / public)."
        )

    device_id, device_name = pick_device(args.device_id, args.device_name)
    log(f"edgible create: device {device_name} ({device_id})")
    health = run_edgible(["device", "health", "--name", device_name], check=False)
    if health.returncode != 0:
        die(
            f"Device {device_name!r} is not healthy.\n"
            f"{(health.stderr or health.stdout or '').strip()}"
        )

    existing = find_apps_by_name(name)
    if existing:
        log(f"edgible create: app {name} already exists, waiting for URL")
        app_id = str(existing[0]["id"])
        url = wait_for_url(app_id)
        print(f"Already published as {name} (auth unchanged here).", flush=True)
        print(f"URL={url}", flush=True)
        print(f"AUTH={auth}", flush=True)
        print(f"DEVICE={device_name}", flush=True)
        print(f"PORT={port}", flush=True)
        print(f"APP_ID={app_id}", flush=True)
        print("STATUS=existing", flush=True)
        return

    log(f"edgible create: creating {name} on port {port} ({auth})")
    create_app(name, port, auth, device_id)
    log("edgible create: create returned, waiting for https URL (up to ~90s)")
    created = find_apps_by_name(name)
    if not created:
        die("Create appeared to succeed but the app is not in `edgible app list`.")
    app_id = str(created[0]["id"])
    url = wait_for_url(app_id)
    print(f"Published {name} on port {port} ({auth}) via {device_name}.", flush=True)
    print(f"URL={url}", flush=True)
    print(f"AUTH={auth}", flush=True)
    print(f"DEVICE={device_name}", flush=True)
    print(f"PORT={port}", flush=True)
    print(f"APP_ID={app_id}", flush=True)
    print("STATUS=created", flush=True)


if __name__ == "__main__":
    main()
