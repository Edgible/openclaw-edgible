#!/usr/bin/env python3
"""Delete an Edgible application by name. Does not stop Docker or delete files."""

from __future__ import annotations

import argparse
import re

from common import die, find_apps_by_name, log, require_edgible, run_edgible

NAME_RE = re.compile(r"^[a-z0-9]([a-z0-9-]{0,62}[a-z0-9])?$")


def main() -> None:
    parser = argparse.ArgumentParser(description="Delete an Edgible application by name.")
    parser.add_argument("--name", help="Application name (DNS label)")
    parser.add_argument("--app-id", help="Application id (overrides --name)")
    args = parser.parse_args()

    require_edgible()
    log("edgible delete: starting")

    app_id = (args.app_id or "").strip() or None
    name = (args.name or "").strip().lower() or None

    if app_id:
        log(f"edgible delete: deleting id {app_id}")
        run_edgible(["app", "delete", "--app-id", app_id, "--force", "--non-interactive"])
        print(f"APP_ID={app_id}", flush=True)
        print("STATUS=deleted", flush=True)
        return

    if not name:
        die("Pass --name or --app-id")
    if not NAME_RE.match(name):
        die("--name must be a lowercase DNS label (letters, digits, hyphens).")

    existing = find_apps_by_name(name)
    if len(existing) > 1:
        ids = ", ".join(str(a.get("id")) for a in existing)
        die(f"Several apps named {name!r}. Pass --app-id. IDs: {ids}")
    if not existing:
        print(f"No Edgible app named {name}.", flush=True)
        print(f"NAME={name}", flush=True)
        print("STATUS=missing", flush=True)
        return

    app_id = str(existing[0]["id"])
    log(f"edgible delete: deleting {name} ({app_id})")
    run_edgible(["app", "delete", "--name", name, "--force", "--non-interactive"])
    print(f"NAME={name}", flush=True)
    print(f"APP_ID={app_id}", flush=True)
    print("STATUS=deleted", flush=True)


if __name__ == "__main__":
    main()
