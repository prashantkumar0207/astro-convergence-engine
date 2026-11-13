"""Rule-registry and RUL-issuance gate (ADR-0120 AC5; ADR-0121).

It fails when:

  G1  the pinned registry does not load: a missing file, a changed byte, a pin that differs from the
      manifest, a schema violation, a number the allocation history never issued, a number published
      for another key or school, or a duplicated or out-of-order allocation;
  G2  the committed history, snapshot and manifest are not exactly what the governed authoring process
      (scripts/author_rule_registry.py) produces from the committed source, so nothing is hand-edited;
  G3  against the base commit's registry: the allocation history is not an unchanged prefix (a number
      dropped, reused or rebound), or a version or variant published there is rewritten or withdrawn.

  python scripts/check_rule_registry.py --base HEAD^1
  python scripts/check_rule_registry.py --dir DIR --pin SHA --previous-history F --previous-snapshot F

A base revision that cannot be resolved is a failure, not a skip. A base with no registry is the first
publication and is reported as such. Exit 0 = PASS, 1 = FAIL.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import author_rule_registry as author  # noqa: E402
from engine.evidence import rule_registry as registry  # noqa: E402

RELATIVE = registry.DATA_DIR.relative_to(ROOT).as_posix()


def _option(argv, name):
    return argv[argv.index(name) + 1] if name in argv else None


def check_load(directory: Path, pin: str) -> list[str]:
    try:
        registry.load_registry(directory, pin)
    except registry.RegistryError as exc:
        return [f"G1 {exc}"]
    return []


def check_authored(directory: Path) -> list[str]:
    try:
        history, snapshot, manifest = author.build(directory)
    except SystemExit as exc:
        return [f"G2 the authoring process refuses the committed source: {exc}"]
    errors = []
    for name, expected in ((registry.HISTORY_NAME, history), (author.SNAPSHOT_NAME, snapshot),
                           (registry.MANIFEST_NAME, manifest)):
        path = directory / name
        if not path.exists() or path.read_bytes() != expected:
            errors.append(f"G2 {name} is not exactly what the authoring process produces; it was edited by hand or "
                          f"allocated outside the process")
    return errors


def check_against(previous_history: dict, previous_snapshot: dict, directory: Path) -> list[str]:
    errors = []
    current = json.loads((directory / registry.HISTORY_NAME).read_bytes())["allocations"]
    before = previous_history["allocations"]
    if current[:len(before)] != before:
        changed = [entry["number"] for entry, now in zip(before, current) if entry != now]
        errors.append(f"G3 the allocation history is not an unchanged prefix of the base's: numbers "
                      f"{changed or [len(current) + 1]} were dropped, reused or rebound; RUL numbers are never "
                      f"reused or rebound")
    published = {(item["rule"], item["version"], item["variant"]): item["content_hash"]
                 for item in json.loads((directory / author.SNAPSHOT_NAME).read_bytes())["rules"]}
    for item in previous_snapshot["rules"]:
        identity = (item["rule"], item["version"], item["variant"])
        if identity not in published:
            errors.append(f"G3 RUL {item['rule']} version {item['version']} {item['variant']!r} was published and is "
                          f"now withdrawn; a published version is never removed")
        elif published[identity] != item["content_hash"]:
            errors.append(f"G3 RUL {item['rule']} version {item['version']} {item['variant']!r} was rewritten; a "
                          f"published version is immutable, and a change is a new version")
    return errors


def _at(base: str, name: str):
    result = subprocess.run(["git", "-C", str(ROOT), "show", f"{base}:{RELATIVE}/{name}"], capture_output=True)
    return json.loads(result.stdout) if result.returncode == 0 else None


def main(argv: list[str]) -> int:
    directory = Path(_option(argv, "--dir") or registry.DATA_DIR)
    pin = _option(argv, "--pin") or registry.PINNED_SNAPSHOT_SHA256
    errors = check_load(directory, pin) + check_authored(directory)
    note = ""
    if _option(argv, "--previous-history"):
        previous = (json.loads(Path(_option(argv, "--previous-history")).read_bytes()),
                    json.loads(Path(_option(argv, "--previous-snapshot")).read_bytes()))
        errors += check_against(*previous, directory)
    elif _option(argv, "--base"):
        base = _option(argv, "--base")
        if subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--verify", "--quiet", f"{base}^{{commit}}"],
                          capture_output=True).returncode != 0:
            errors.append(f"G3 the base revision {base!r} cannot be resolved; the append-only comparison needs it")
        else:
            history, snapshot = _at(base, registry.HISTORY_NAME), _at(base, author.SNAPSHOT_NAME)
            if history is None and snapshot is None:
                note = f"; first publication: {base} has no registry"
            elif history is None or snapshot is None:
                errors.append(f"G3 the base {base} has a partial registry; refusing to compare")
            else:
                errors += check_against(history, snapshot, directory)
                note = f"; append-only against {base}"
    else:
        errors.append("G3 no base given: pass --base REF, or --previous-history and --previous-snapshot")
    if errors:
        print(f"FAIL: rule registry and RUL issuance ({len(errors)} failures)")
        for error in errors:
            print(f"    {error}")
        return 1
    print(f"PASS: the pinned registry verifies, the authoring process produced it, and RUL issuance is append-only"
          f"{note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
