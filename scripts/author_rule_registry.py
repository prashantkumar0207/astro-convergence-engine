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
SOURCED_SOURCE_NAME = "sourced_source.json"
SOURCED_SNAPSHOT_NAME = "sourced_snapshot.json"
SOURCED_MANIFEST_NAME = "SOURCED_MANIFEST.json"
SOURCED_SOURCE_SCHEMA = "ace-sourced-rule-source-v1"
VARIANT_FIELDS = ("variant", "citation", "statement", "condition", "activation_conditions", "effect", "polarity",
                  "domain", "known_variants", "certification", "declared_strength", "synthetic")


def pretty(data) -> bytes:
    return (json.dumps(data, sort_keys=True, indent=1, ensure_ascii=True) + "\n").encode("ascii")


def allocate(source: dict, history: dict, sourced_rules=()) -> dict:
    """Extend the history with one new number per new rule key. Existing allocations are never changed."""

    allocations = list(history["allocations"])
    bound = {entry["key"]: entry for entry in allocations}
    authored = {rule["key"] for rule in source["rules"]} | {rule["key"] for rule in sourced_rules}
    if len(authored) != len(source["rules"]) + len(sourced_rules):
        raise SystemExit("FAIL: a rule key is authored more than once across the two sources")
    orphans = sorted(entry["number"] for entry in allocations if entry["key"] not in authored)
    if orphans:
        raise SystemExit(f"FAIL: RUL numbers {orphans} are allocated to keys the source never authored; every "
                         f"allocation comes from the authoring process, and a published rule is never withdrawn")
    for rule in [*source["rules"], *sourced_rules]:
        if rule["key"] in bound:
            if bound[rule["key"]]["school"] != rule["school"]:
                raise SystemExit(f"FAIL: {rule['key']!r} is bound to school {bound[rule['key']]['school']!r}; a rule "
                                 f"key's school never changes")
            continue
        entry = {"number": len(allocations) + 1, "key": rule["key"], "school": rule["school"]}
        allocations.append(entry)
        bound[rule["key"]] = entry
    return {"schema": registry.HISTORY_SCHEMA, "allocations": allocations}


def publish(source: dict, history: dict, sources=(), verifications=()) -> bytes:
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
                registry.rule_from_record(record, tuple(registry.source_from_record(item) for item in sources))
                records.append(record)
    if sources:
        return pretty({"schema": registry.SOURCED_SNAPSHOT_SCHEMA, "rules": records,
                       "sources": list(sources), "verifications": list(verifications)})
    return pretty({"schema": registry.SNAPSHOT_SCHEMA, "rules": records})


def manifest(snapshot: bytes, name: str = SNAPSHOT_NAME) -> bytes:
    return pretty({"schema": registry.MANIFEST_SCHEMA, "snapshot": name,
                   "sha256": hashlib.sha256(snapshot).hexdigest()})


def build_all(directory: Path):
    """Build both immutable publications from one append-only RUL allocation history."""
    source = json.loads((directory / SOURCE_NAME).read_bytes())
    sourced = json.loads((directory / SOURCED_SOURCE_NAME).read_bytes())
    if set(source) != {"schema", "rules"} or source["schema"] != SOURCE_SCHEMA:
        raise SystemExit("FAIL: not a synthetic rule source of this schema")
    if set(sourced) != {"schema", "rules", "sources", "verifications"} or \
            sourced["schema"] != SOURCED_SOURCE_SCHEMA or not sourced["rules"] or \
            len(sourced["sources"]) != 2 or sourced["verifications"] != []:
        raise SystemExit("FAIL: not the provisional two-witness source of this schema")
    if any(record["synthetic"] is not False for rule in sourced["rules"]
           for version in rule["versions"] for record in version["variants"]):
        raise SystemExit("FAIL: a sourced rule cannot be synthetic")
    if any(record["synthetic"] is not True for rule in source["rules"]
           for version in rule["versions"] for record in version["variants"]):
        raise SystemExit("FAIL: a fixture rule must remain synthetic")
    history_path = directory / registry.HISTORY_NAME
    history = json.loads(history_path.read_bytes()) if history_path.exists() else \
        {"schema": registry.HISTORY_SCHEMA, "allocations": []}
    extended = allocate(source, history, sourced["rules"])
    synthetic_snapshot = publish(source, extended)
    sourced_snapshot = publish(sourced, extended, sourced["sources"], sourced["verifications"])
    # Validate the generated genuine publication against the same pin and schema that readers use.
    return (pretty(extended), synthetic_snapshot, manifest(synthetic_snapshot), sourced_snapshot,
            manifest(sourced_snapshot, SOURCED_SNAPSHOT_NAME))


def build(directory: Path):
    """Legacy three-file interface retained for Gate M's historical checks."""
    return build_all(directory)[:3]


def main(argv: list[str]) -> int:
    directory = Path(argv[argv.index("--dir") + 1]) if "--dir" in argv else registry.DATA_DIR
    produced = build_all(directory)
    files = (registry.HISTORY_NAME, SNAPSHOT_NAME, registry.MANIFEST_NAME,
             SOURCED_SNAPSHOT_NAME, SOURCED_MANIFEST_NAME)
    if "--write" in argv:
        for name, content in zip(files, produced):
            (directory / name).write_bytes(content)
        print(f"published: {SNAPSHOT_NAME} sha256 {hashlib.sha256(produced[1]).hexdigest()}")
        print(f"published: {SOURCED_SNAPSHOT_NAME} sha256 {hashlib.sha256(produced[3]).hexdigest()}")
        return 0
    errors = [name for name, expected in zip(files, produced)
              if not (directory / name).exists() or (directory / name).read_bytes() != expected]
    if errors:
        print("FAIL: the committed registry files are not exactly what the governed authoring process produces:")
        for name in errors:
            print("   ", name)
        return 1
    print("PASS: both snapshots, both manifests and one RUL history were generated by the authoring process")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
