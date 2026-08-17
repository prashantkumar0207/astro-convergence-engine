"""PostToolUse hook: fast local feedback after edits to governance/certification-adjacent files.

Re-runs the existing pure-Python gate scripts (never reimplements their logic) immediately after an
Edit/Write touches a file those gates cover, so a break surfaces before commit instead of only at CI.
Scoped to the gates that are known to run on Windows (see .claude/rules/certification.md) - never
invokes a swetest-dependent certifier.

Contract: reads the PostToolUse JSON payload on stdin. Exit 0 = ok (nothing to check, or all checks
passed). Exit 2 with output on stderr = at least one gate failed; Claude is shown the output. Any
unexpected exception is swallowed and treated as ok, so a bug here never blocks normal editing.
"""

from __future__ import annotations

import json
import subprocess
import sys


def gates_for(path: str) -> list[list[str]]:
    norm = path.replace("\\", "/")
    commands: list[list[str]] = []

    if norm.endswith("docs/DECISION_LOG.md"):
        commands.append(["python", "scripts/check_adr_numbering.py"])
        commands.append(["python", "scripts/check_retired_identifiers.py"])

    if "/docs/decisions/" in norm or norm.startswith("docs/decisions/"):
        commands.append(["python", "scripts/check_identifier_families.py"])
        commands.append(["python", "scripts/check_retired_identifiers.py"])

    if "/certification/" in norm and norm.endswith(".json"):
        commands.append(["python", "scripts/check_artifact_drift.py", path])

    # De-duplicate while preserving order.
    seen = set()
    unique = []
    for cmd in commands:
        key = tuple(cmd)
        if key not in seen:
            seen.add(key)
            unique.append(cmd)
    return unique


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    if payload.get("hook_event_name") != "PostToolUse":
        return 0
    if payload.get("tool_name") not in ("Edit", "Write"):
        return 0

    file_path = (payload.get("tool_input") or {}).get("file_path") or ""
    if not file_path:
        return 0

    try:
        commands = gates_for(file_path)
    except Exception:
        return 0

    if not commands:
        return 0

    failures = []
    for cmd in commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        except Exception as exc:
            failures.append(f"$ {' '.join(cmd)}\n  could not run: {exc}")
            continue
        if result.returncode != 0:
            failures.append(f"$ {' '.join(cmd)}\n{result.stdout}{result.stderr}")

    if failures:
        sys.stderr.write(
            f"GOVERNANCE GATE FAILED after editing {file_path}:\n\n" + "\n---\n".join(failures) + "\n"
        )
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
