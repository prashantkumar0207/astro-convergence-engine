"""The governed rule-registry authoring process: the only RUL issuer (ADR-0121; ADR-0120 s4).

  python scripts/author_rule_registry.py --write   allocate RUL numbers for new rule keys and publish the snapshot
  python scripts/author_rule_registry.py --check   prove the committed history, snapshot and manifest are exactly
                                                   what this process produces from the committed source

Allocation: a rule key that has no RUL number gets the next one. The history is persistent and append-only:
numbers are contiguous from 1, a number is never reused, and a number is never rebound to another key or school.
Publication: the snapshot lists every authored rule version under its issued RUL number, with its content hash.
A snapshot only publishes identities the history has issued; it never allocates. After --write, the printed
SHA-256 must be set as PINNED_SNAPSHOT_SHA256 in engine/evidence/rule_registry.py, in the same reviewed commit.

Exit 0 = PASS, 1 = FAIL.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.evidence import rule_registry as registry  # noqa: E402

SOURCE_SCHEMA = "ace-rule-source-v1"
SOURCE_NAME = "source.json"
SNAPSHOT_NAME = "snapshot.json"
VARIANT_FIELDS = ("variant", "citation", "statement", "condition", "activation_conditions", "effect", "polarity",
                  "domain", "known_variants", "certification", "declared_strength", "synthetic")


def pretty(data) -> bytes:
    return (json.dumps(data, sort_keys=True, indent=1, ensure_ascii=True) + "\n").encode("ascii")


def allocate(source: dict, history: dict) -> dict:
    """Extend the history with one new number per new rule key. Existing allocations are never changed."""

    allocations = list(history["allocations"])
    bound = {entry["key"]: entry for entry in allocations}
    authored = {rule["key"] for rule in source["rules"]}
    orphans = sorted(entry["number"] for entry in allocations if entry["key"] not in authored)
    if orphans:
        raise SystemExit(f"FAIL: RUL numbers {orphans} are allocated to keys the source never authored; every "
                         f"allocation comes from the authoring process, and a published rule is never withdrawn")
    for rule in source["rules"]:
        if rule["key"] in bound:
            if bound[rule["key"]]["school"] != rule["school"]:
                raise SystemExit(f"FAIL: {rule['key']!r} is bound to school {bound[rule['key']]['school']!r}; a rule "
                                 f"key's school never changes")
            continue
        entry = {"number": len(allocations) + 1, "key": rule["key"], "school": rule["school"]}
        allocations.append(entry)
        bound[rule["key"]] = entry
    return {"schema": registry.HISTORY_SCHEMA, "allocations": allocations}


def publish(source: dict, history: dict) -> bytes:
    """The snapshot: every authored version and variant under its issued RUL number, each validated and hashed."""

    numbers = {entry["key"]: entry["number"] for entry in history["allocations"]}
    records = []
    for rule in sorted(source["rules"], key=lambda item: numbers[item["key"]]):
        for version in rule["versions"]:
            for variant in version["variants"]:
                if set(variant) != set(VARIANT_FIELDS):
                    raise SystemExit(f"FAIL: {rule['key']} v{version['version']}: a variant carries exactly "
                                     f"{VARIANT_FIELDS}")
                record = {"rule": numbers[rule["key"]], "key": rule["key"], "version": version["version"],
                          "school": rule["school"], **variant}
                record["content_hash"] = hashlib.sha256(registry.canonical(record)).hexdigest()
                registry.rule_from_record(record)  # Refuse anything the registry would refuse.
                records.append(record)
    return pretty({"schema": registry.SNAPSHOT_SCHEMA, "rules": records})


def manifest(snapshot: bytes) -> bytes:
    return pretty({"schema": registry.MANIFEST_SCHEMA, "snapshot": SNAPSHOT_NAME,
                   "sha256": hashlib.sha256(snapshot).hexdigest()})


def build(directory: Path):
    source = json.loads((directory / SOURCE_NAME).read_bytes())
    if set(source) != {"schema", "rules"} or source["schema"] != SOURCE_SCHEMA:
        raise SystemExit("FAIL: not a rule source of this schema")
    history_path = directory / registry.HISTORY_NAME
    history = json.loads(history_path.read_bytes()) if history_path.exists() else \
        {"schema": registry.HISTORY_SCHEMA, "allocations": []}
    extended = allocate(source, history)
    snapshot = publish(source, extended)
    return pretty(extended), snapshot, manifest(snapshot)


def main(argv: list[str]) -> int:
    directory = Path(argv[argv.index("--dir") + 1]) if "--dir" in argv else registry.DATA_DIR
    history, snapshot, manifest_bytes = build(directory)
    if "--write" in argv:
        (directory / registry.HISTORY_NAME).write_bytes(history)
        (directory / SNAPSHOT_NAME).write_bytes(snapshot)
        (directory / registry.MANIFEST_NAME).write_bytes(manifest_bytes)
        print(f"published: {SNAPSHOT_NAME} sha256 {hashlib.sha256(snapshot).hexdigest()}")
        return 0
    errors = []
    for name, expected in ((registry.HISTORY_NAME, history), (SNAPSHOT_NAME, snapshot),
                           (registry.MANIFEST_NAME, manifest_bytes)):
        path = directory / name
        if not path.exists() or path.read_bytes() != expected:
            errors.append(f"{name} is not exactly what the authoring process produces from {SOURCE_NAME}")
    if errors:
        print("FAIL: the published rule registry was not produced by the governed authoring process")
        for error in errors:
            print(f"    {error}")
        return 1
    print(f"PASS: the history, snapshot and manifest are exactly the authoring process's output "
          f"(snapshot sha256 {hashlib.sha256(snapshot).hexdigest()})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
