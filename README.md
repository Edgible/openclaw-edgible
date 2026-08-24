# openclaw-edgible

OpenClaw skill for the [Edgible](https://edgible.com) CLI: list, create, and delete apps. One skill, named **`edgible`**, same idea as OpenClaw’s bundled `github` skill.

Chat: `/skill edgible` then “list my apps”, “publish port 8082 as skill-test”, “delete skill-test”.

Requires `edgible` on PATH and `edgible auth login` on the Gateway host. This repo is not Edgible signup.

## Install

`SKILL.md` is at the repo root (ClawHub / `git:` install expect that).

```bash
openclaw skills install git:Edgible/openclaw-edgible
openclaw skills list
openclaw gateway restart
```

Or copy so the folder name matches the skill name:

```bash
git clone https://github.com/Edgible/openclaw-edgible.git
mkdir -p ~/.openclaw/workspace/skills
cp -R openclaw-edgible ~/.openclaw/workspace/skills/edgible
openclaw skills list
openclaw gateway restart
```

You want **edgible** in `openclaw skills list`. Then `/new`.

If you previously copied `edgible-app-create` / `edgible-app-list` / `edgible-app-delete`, remove those folders so the agent is not choosing among four skills.

## Layout

```text
SKILL.md              ← index: dispatch list / create / delete
scripts/              ← deterministic helpers (python3 + edgible)
references/           ← create fields, Control UI aftercare, safety
```

The agent loads `name` + `description` always, `SKILL.md` when this skill is used, and `references/` only if it opens them.

## Helpers (skip the model)

Default list is **this serving device**. `--all` is the whole org. Each app line includes `DEVICE=`.

```bash
python3 -u ~/.openclaw/workspace/skills/edgible/scripts/list.py
python3 -u ~/.openclaw/workspace/skills/edgible/scripts/list.py --all

python3 -u ~/.openclaw/workspace/skills/edgible/scripts/create.py \
  --name skill-test --port 8082 --auth-modes none

python3 -u ~/.openclaw/workspace/skills/edgible/scripts/delete.py --name skill-test
```

Port **18789** with `--auth-modes none` is rejected. Existing app name → reprints `URL=`. Several serving devices and no unique hostname match → pass `--device-name` for **this** box.

## Test

A local process must already listen (this skill does not start Docker). Then in Control UI:

```text
/skill edgible List Edgible apps on this machine.
/skill edgible Create a public Edgible app named skill-test for nginx on port 8082. If it already exists, just give me the URL.
/skill edgible Delete the Edgible app named skill-test.
```

Success is `DEVICE=` / `URL=` / `STATUS=` in the **chat bubble**, not only on the tool card.

## License

MIT. Publishing a copy to [ClawHub](https://clawhub.ai) uses ClawHub’s MIT-0 terms.
