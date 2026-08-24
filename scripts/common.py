"""Shared helpers for the Edgible OpenClaw skill scripts."""

from __future__ import annotations

import json
import shutil
import socket
import subprocess
import sys


def log(msg: str) -> None:
    print(msg, flush=True)


def die(msg: str, code: int = 1) -> None:
    print(msg, file=sys.stderr, flush=True)
    raise SystemExit(code)


def run_edgible(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    cmd = ["edgible", *args]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if check and proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip() or f"exit {proc.returncode}"
        die(f"$ {' '.join(cmd)}\n{err}", proc.returncode or 1)
    return proc


def load_json(proc: subprocess.CompletedProcess[str]) -> dict:
    text = (proc.stdout or "").strip()
    if not text:
        die("edgible produced no JSON (are you logged in? `edgible auth login`)")
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        die(f"Could not parse edgible JSON: {exc}\n{text[:500]}")


def require_edgible() -> None:
    if not shutil.which("edgible"):
        die("edgible is not on PATH. Install and `edgible auth login` on this machine first.")


def serving_devices() -> list[dict]:
    proc = run_edgible(["device", "list", "--type", "serving", "--json"])
    return load_json(proc).get("devices") or []


def device_id_to_name(devices: list[dict]) -> dict[str, str]:
    return {
        str(d["id"]): str(d.get("name") or d["id"])
        for d in devices
        if d.get("id")
    }


def _local_hostnames() -> set[str]:
    raw = socket.gethostname().strip().lower()
    names = {raw}
    if "." in raw:
        names.add(raw.split(".")[0])
    return {n for n in names if n}


def _guess_local_device(devices: list[dict]) -> tuple[str, str] | None:
    hosts = _local_hostnames()
    matches = []
    for d in devices:
        name = str(d.get("name") or "").strip().lower()
        if name and name in hosts:
            matches.append(d)
    uniq = {str(d["id"]): d for d in matches}
    if len(uniq) != 1:
        return None
    d = next(iter(uniq.values()))
    return str(d["id"]), str(d.get("name") or d["id"])


def pick_device(
    device_id: str | None,
    device_name: str | None,
    devices: list[dict] | None = None,
    *,
    allow_all_hint: bool = False,
) -> tuple[str, str]:
    devices = devices if devices is not None else serving_devices()
    if not devices:
        die("No serving devices in this org. Register the Edgible agent first.")

    if device_id:
        for d in devices:
            if d.get("id") == device_id:
                return str(d["id"]), str(d.get("name") or d["id"])
        die(f"No serving device with id {device_id}")

    if device_name:
        matches = [d for d in devices if d.get("name") == device_name]
        if len(matches) != 1:
            names = ", ".join(d.get("name") or d.get("id") for d in devices)
            die(f"Serving device {device_name!r} not found. Known: {names}")
        d = matches[0]
        return str(d["id"]), str(d.get("name") or d["id"])

    if len(devices) == 1:
        d = devices[0]
        return str(d["id"]), str(d.get("name") or d["id"])

    guessed = _guess_local_device(devices)
    if guessed:
        return guessed

    names = ", ".join(f"{d.get('name')} ({d.get('id')})" for d in devices)
    retries = "\n".join(
        f"  --device-name {d.get('name')}" for d in devices if d.get("name")
    )
    extra = "\nOr pass --all for every app in the org." if allow_all_hint else ""
    die(
        "Several serving devices. Pass --device-name for *this* machine "
        f"(the box OpenClaw is on, not another device in the org).\nKnown: {names}\n"
        f"Retry with one of:\n{retries}{extra}"
    )


def list_apps() -> list[dict]:
    proc = run_edgible(["app", "list", "--json"])
    payload = load_json(proc)
    return payload.get("applications") or payload.get("apps") or []


def find_apps_by_name(name: str) -> list[dict]:
    return [app for app in list_apps() if app.get("name") == name]


def app_url(app_id: str, *, required: bool = True) -> str:
    proc = run_edgible(["app", "get", "--app-id", app_id, "--json"], check=required)
    if proc.returncode != 0:
        return ""
    try:
        data = json.loads((proc.stdout or "").strip() or "{}")
    except json.JSONDecodeError:
        if required:
            die("Could not parse edgible app get JSON")
        return ""
    return str(data.get("url") or "").strip()
