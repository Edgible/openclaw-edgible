#!/usr/bin/env python3
"""List Edgible apps. Default: this serving device (OpenClaw's box). --all = whole org."""

from __future__ import annotations

import argparse

from common import (
    app_url,
    device_id_to_name,
    list_apps,
    log,
    pick_device,
    require_edgible,
    serving_devices,
)


def app_device_ids(app: dict) -> set[str]:
    ids: set[str] = set()
    wid = app.get("workloadId")
    if wid and str(wid) != "unknown":
        ids.add(str(wid))
    cfg = app.get("configuration")
    if isinstance(cfg, dict):
        raw = cfg.get("deviceIds") or cfg.get("deviceId")
        if isinstance(raw, list):
            ids.update(str(x) for x in raw if x)
        elif raw:
            ids.add(str(raw))
    return ids


def app_device_names(app: dict, id_to_name: dict[str, str]) -> str:
    ids = app_device_ids(app)
    names = [id_to_name.get(i, i) for i in sorted(ids)]
    return ",".join(names) if names else "unknown"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="List Edgible apps on this device, or the whole org with --all."
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Every app in the org (all serving devices)",
    )
    parser.add_argument("--device-id", help="Serving device id")
    parser.add_argument("--device-name", help="Serving device name (this OpenClaw box)")
    args = parser.parse_args()

    require_edgible()
    log("edgible list: starting")

    devices = serving_devices()
    id_to_name = device_id_to_name(devices)
    apps = list_apps()

    if args.all:
        scope = "org"
        device_name = "*"
        filtered = apps
        log("edgible list: scope org (all devices)")
    else:
        device_id, device_name = pick_device(
            args.device_id,
            args.device_name,
            devices,
            allow_all_hint=True,
        )
        scope = "device"
        filtered = [a for a in apps if device_id in app_device_ids(a)]
        log(f"edgible list: scope device {device_name} ({device_id})")

    print(f"SCOPE={scope}", flush=True)
    print(f"DEVICE={device_name}", flush=True)
    print(f"COUNT={len(filtered)}", flush=True)
    if not filtered:
        print("STATUS=empty", flush=True)
        return

    for app in filtered:
        name = app.get("name") or ""
        app_id = str(app.get("id") or "")
        port = app.get("port")
        status = app.get("status") or ""
        url = app_url(app_id, required=False) if app_id else ""
        app_device = app_device_names(app, id_to_name)
        print(
            f"NAME={name} DEVICE={app_device} PORT={port} STATUS={status} "
            f"URL={url} APP_ID={app_id}",
            flush=True,
        )
    print("STATUS=ok", flush=True)


if __name__ == "__main__":
    main()
