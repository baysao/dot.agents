#!/usr/bin/env python3
"""Evaluate a project's .paul/DEBT.toml at the PAUL entry gates.

PAUL has no daemon, so this is not a scheduler process: it is the one call the
agent makes when it already passes a gate (session entry, plan drafting, phase
exit). Derived state is never written back — flipping a row to done is an edit
to the TOML, so every discharge shows up as a diff.

  python ~/.agents/paul-framework/scripts/debt.py                report
  python ~/.agents/paul-framework/scripts/debt.py --run-checks   also run each check
  python ~/.agents/paul-framework/scripts/debt.py --gate NAME    exit 1 unless every
                                                                 row blocking=NAME is done

The project root is found by walking up from the current directory for
`.paul/DEBT.toml`. Run from inside the project, or pass `--root DIR`.
"""
from __future__ import annotations

import argparse
import datetime as dt
import subprocess
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # Python < 3.11
    sys.exit("debt.py needs Python 3.11+ (tomllib)")

NOW = dt.datetime.now(dt.timezone.utc)

# Windows consoles default to cp1252 and raise UnicodeEncodeError on non-ASCII
# titles (debt titles carry real content, e.g. Vietnamese, em dashes).
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass


def find_root(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).resolve()
    start = Path.cwd().resolve()
    for d in (start, *start.parents):
        if (d / ".paul" / "DEBT.toml").is_file():
            return d
    sys.exit(
        "no .paul/DEBT.toml in this directory or above it — run from the project, "
        "or pass --root DIR"
    )


def load(store: Path) -> list[dict]:
    if not store.is_file():
        sys.exit(f"no debt store at {store}")
    rows = tomllib.loads(store.read_text(encoding="utf-8")).get("debt", [])
    for r in rows:
        for key in ("id", "title", "kind", "owner", "check"):
            if key not in r:
                sys.exit(f"{r.get('id', '<no id>')}: missing required key {key!r}")
        if not ({"due", "trigger", "blocking"} & r.keys()):
            sys.exit(f"{r['id']}: needs a due date, a trigger, or a blocking gate — unschedulable row")
        r.setdefault("status", "open")
    return rows


def _files(root: Path, pattern: str) -> list[Path]:
    return [p for p in root.glob(pattern) if p.is_file()]


def check_ok(row: dict, root: Path) -> bool:
    """True when the row's discharge condition is met. Unverifiable is not met."""
    c = row["check"]
    kind = c["type"]
    if kind == "file_absent":
        return not _files(root, c["path"])
    if kind == "file_exists":
        return bool(_files(root, c["path"]))
    if kind in ("text_present", "text_absent"):
        files = _files(root, c["path"])
        if not files:
            return False
        hit = any(c["pattern"] in p.read_text(encoding="utf-8", errors="ignore") for p in files)
        return hit if kind == "text_present" else not hit
    if kind == "command":
        r = subprocess.run(c["run"], shell=True, cwd=root, capture_output=True, text=True)
        if r.returncode != 0:
            return False
        return c["expect"] in (r.stdout + r.stderr) if "expect" in c else True
    sys.exit(f"{row['id']}: unknown check type {kind!r}")


def state_of(row: dict, run_checks: bool, root: Path) -> str:
    """Derived, never stored. A state only ever gets quieter, never louder.

    overdue  — the date passed and nothing discharged it. Interrupt the user.
    scheduled— a date is set but has not arrived. Do not interrupt.
    waiting  — no date; the trigger has not fired. Do not interrupt.
    open     — undated and untriggered (only a blocking gate). The gate asks.
    """
    if row["status"] in ("done", "dropped"):
        return row["status"]
    if run_checks and check_ok(row, root):
        return "done"
    due = row.get("due")
    if due:
        when = dt.datetime.fromisoformat(due.replace("Z", "+00:00"))
        return "overdue" if NOW >= when else "scheduled"
    if row.get("trigger"):
        return "waiting"
    return "open"


STATES = ("overdue", "scheduled", "waiting", "open", "done", "dropped")
MARK = {
    "overdue": "!! OVERDUE  ",
    "scheduled": ".. scheduled",
    "waiting": "   waiting  ",
    "open": "·  open     ",
    "done": "OK done     ",
    "dropped": "-- dropped  ",
}


def main() -> int:
    ap = argparse.ArgumentParser(description="Report .paul/DEBT.toml state or gate on it.")
    ap.add_argument("--root", metavar="DIR", help="project root (default: nearest .paul/DEBT.toml above cwd)")
    ap.add_argument("--run-checks", action="store_true", help="execute each row's check")
    ap.add_argument("--gate", metavar="NAME", help="exit 1 unless every row blocking=NAME is done")
    args = ap.parse_args()

    root = find_root(args.root)
    rows = load(root / ".paul" / "DEBT.toml")
    for r in rows:
        r["_state"] = state_of(r, args.run_checks, root)

    if args.gate:
        held = [r for r in rows if r.get("blocking") == args.gate and r["_state"] not in ("done", "dropped")]
        if held:
            print(f"GATE {args.gate}: BLOCKED")
            for r in held:
                print(f"  {r['id']}  [{r['_state']}]  {r['title']}  (owner={r['owner']})")
            return 1
        print(f"GATE {args.gate}: clear")
        return 0

    counts: dict[str, int] = {}
    for r in rows:
        counts[r["_state"]] = counts.get(r["_state"], 0) + 1

    order = {s: i for i, s in enumerate(STATES)}
    rows.sort(key=lambda r: (order[r["_state"]], r.get("due", "9"), r["id"]))
    print("DEBT  " + "  ".join(f"{s}={counts.get(s, 0)}" for s in STATES))
    for r in rows:
        when = r.get("due") or r.get("trigger", "")
        tags = f"owner={r['owner']}"
        if r.get("blocking"):
            tags += f" blocking={r['blocking']}"
        print(f"{MARK[r['_state']]} {r['id']}  {r['title']}")
        print(f"            {when}  kind={r['kind']}  {tags}")
        if r["_state"] == "open" and args.run_checks:
            print("            check did not pass yet")
        if r["_state"] == "overdue" or (args.run_checks and r["_state"] == "done" and r["status"] == "open"):
            print('            discharged? set status = "done" in .paul/DEBT.toml')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
