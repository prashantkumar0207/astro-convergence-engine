"""Certification artifact drift gate.

ADR-0018's evidence claims that regenerating the certification artifacts leaves
them "differing from the committed artifacts in the `date` field ONLY, every gate
value byte-identical". That was a human observation. The CI step that was meant
to enforce it ran `git diff` with no `--exit-code`, so it printed any difference
into the log and the job went green regardless. A changed comparison count, a
changed maximum error, a widened tolerance or a removed case would all have
passed.

This script enforces the claim. It compares each regenerated artifact against
the committed version, ignoring ONLY the fields that are legitimately volatile,
and fails on anything else.

WHAT IS LEGITIMATELY VOLATILE, and why each one is:

  date                     the calendar date of the run;
  run.executed_utc         the run's timestamp;
  run.source_revision      the commit the run executed against, which is
                           necessarily the previous commit (ADR-0032 D1);
  run.working_tree_dirty   true before the evidence commit, false after it.

Everything else must match byte for byte, including every comparison count,
every numerical maximum, every tolerance, every case identifier, every
precondition digest and the PASS/FAIL verdict.

`swetest_cmd` is NOT on the volatile list. Q15 made it deterministic precisely so
that it could be held to this standard.

SCOPE, corrected 2026-08-13 after an independent audit. The first form checked
only `certification/*.json` and only those git reported as MODIFIED. That left
two holes: `reports/certification/`, whose contents the oracle job uploads as
certification evidence, was diffed by the step above and enforced by nothing; and
a run that regenerated NOTHING printed a PASS that read as "regenerated and
identical". Both are closed here. Every tracked evidence file is compared, whether
or not git thinks it changed, and the count is reported.

Usage:
    python scripts/check_artifact_drift.py [path ...]

With no arguments, compares EVERY tracked `certification/*.json`,
`reports/certification/*.report.md` and `reports/certification/*.console.txt`
against its committed version. Exit 0 clean, 1 on drift, 2 on a usage or git
error.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

#: Dotted paths permitted to differ in a JSON artifact. Anything not listed must
#: be identical.
VOLATILE = (
    "date",
    "run.executed_utc",
    "run.source_revision",
    "run.working_tree_dirty",
)

#: Line prefixes permitted to differ in a rendered report or console transcript.
#: These are the text renderings of the VOLATILE fields above and nothing else.
VOLATILE_LINE_PREFIXES = (
    "- Date:",
    "- source_revision:",
    "- working_tree_dirty:",
    "- executed_utc:",
)


def _prune(value, prefix: str = ""):
    """Return `value` with every VOLATILE path removed."""

    if isinstance(value, dict):
        out = {}
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else key
            if path in VOLATILE:
                continue
            out[key] = _prune(item, path)
        return out
    if isinstance(value, list):
        return [_prune(item, prefix) for item in value]
    return value


def _differences(committed, regenerated, prefix: str = "") -> list[str]:
    if isinstance(committed, dict) and isinstance(regenerated, dict):
        found = []
        for key in sorted(set(committed) | set(regenerated)):
            path = f"{prefix}.{key}" if prefix else key
            if key not in committed:
                found.append(f"{path}: added")
            elif key not in regenerated:
                found.append(f"{path}: removed")
            else:
                found += _differences(committed[key], regenerated[key], path)
        return found
    if isinstance(committed, list) and isinstance(regenerated, list):
        if len(committed) != len(regenerated):
            return [f"{prefix}: length {len(committed)} -> {len(regenerated)}"]
        found = []
        for index, (left, right) in enumerate(zip(committed, regenerated)):
            found += _differences(left, right, f"{prefix}[{index}]")
        return found
    if committed != regenerated:
        return [f"{prefix}: {committed!r} -> {regenerated!r}"]
    return []


def committed_version(relative: str) -> dict | None:
    """The artifact as committed at HEAD, or None if it is not tracked."""

    done = subprocess.run(
        ["git", "-C", str(ROOT), "show", f"HEAD:{relative}"],
        capture_output=True,
        text=True,
    )
    if done.returncode != 0:
        return None
    return json.loads(done.stdout)


def tracked_evidence() -> list[str]:
    """Every tracked evidence file, whether or not git reports it modified.

    Checking only modified files meant a run that regenerated nothing produced a
    PASS indistinguishable from a run that regenerated everything identically.
    """

    done = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files",
         "certification/*.json", "reports/certification/*"],
        capture_output=True,
        text=True,
        check=True,
    )
    return sorted(line for line in done.stdout.splitlines() if line.strip())


def _normalise_text(body: str) -> list[str]:
    return [
        line
        for line in body.splitlines()
        if not any(line.startswith(prefix) for prefix in VOLATILE_LINE_PREFIXES)
    ]


def check_text(relative: str) -> list[str]:
    """Compare a rendered report or console transcript, line by line."""

    done = subprocess.run(
        ["git", "-C", str(ROOT), "show", f"HEAD:{relative}"],
        capture_output=True,
        text=True,
    )
    if done.returncode != 0:
        return [f"{relative}: not tracked at HEAD, so drift cannot be assessed"]
    try:
        current = (ROOT / relative).read_text()
    except OSError as exc:
        return [f"{relative}: unreadable: {exc}"]

    committed_lines = _normalise_text(done.stdout)
    current_lines = _normalise_text(current)
    if committed_lines == current_lines:
        return []
    for index, (left, right) in enumerate(zip(committed_lines, current_lines), start=1):
        if left != right:
            return [f"{relative}: line {index}: {left!r} -> {right!r}"]
    return [
        f"{relative}: length {len(committed_lines)} -> {len(current_lines)} lines "
        "after removing the volatile lines"
    ]


def check(relative: str) -> list[str]:
    committed = committed_version(relative)
    if committed is None:
        return [f"{relative}: not tracked at HEAD, so drift cannot be assessed"]
    try:
        regenerated = json.loads((ROOT / relative).read_text())
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{relative}: unreadable after regeneration: {exc}"]
    return [
        f"{relative}: {difference}"
        for difference in _differences(_prune(committed), _prune(regenerated))
    ]


def main(argv: list[str]) -> int:
    targets = argv[1:] or tracked_evidence()
    if not targets:
        print("FAIL: no tracked certification evidence found; this gate is")
        print("      checking nothing, which is not the same as finding nothing wrong")
        return 1

    drift: list[str] = []
    for relative in targets:
        drift += check(relative) if relative.endswith(".json") else check_text(relative)

    if drift:
        print("FAIL: certification artifact drift outside the volatile fields")
        print(f"  volatile fields, permitted to differ: {', '.join(VOLATILE)}")
        for item in drift:
            print(f"    {item}")
        print()
        print("A regenerated artifact differing in any other field means the run")
        print("produced a different result from the committed evidence. Do not")
        print("commit the new artifact until the change is understood, decided and")
        print("recorded. Inside a locked scope it additionally requires a formal")
        print("change decision and recertification.")
        return 1

    jsons = sum(1 for name in targets if name.endswith(".json"))
    print(
        f"PASS: {len(targets)} evidence file(s) identical to the committed version "
        f"outside the volatile fields ({jsons} machine-readable, "
        f"{len(targets) - jsons} rendered)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
