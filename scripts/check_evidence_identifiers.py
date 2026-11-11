"""EVD and RUL identifier-family uniqueness gate (ADR-0113 s2 B; ADR-0119 AC1, AC2).

Part of the identifier conformance sweep. It fails when:

  V1  NAMING_STANDARD.md s2 does not register exactly one row for each family, with the pattern and
      width that engine/evidence/evidence_identifiers.py uses, and a scope, issuer and source of law;
  V2  a tracked production file outside the test and governance surface contains a literal EVD or
      RUL identifier, because identifiers come only from a store's issuer;
  V3  a store given with --store has an identifier outside its pattern, issued numbers that are not
      unique, not contiguous from 1 or above their issuer's counter, a rule whose versions are not
      1..n, or an evidence item naming a rule version that does not exist.

Exit 0 = PASS, 1 = FAIL. Paths are injectable so the negative controls run the real checks.
"""

from __future__ import annotations

import json
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.evidence.evidence_identifiers import (  # noqa: E402
    EVD_FAMILY, EVD_PATTERN, EVD_WIDTH, RUL_FAMILY, RUL_PATTERN, RUL_WIDTH,
)

NAMING = ROOT / "docs" / "NAMING_STANDARD.md"
FAMILIES = ((EVD_FAMILY, EVD_PATTERN, EVD_WIDTH), (RUL_FAMILY, RUL_PATTERN, RUL_WIDTH))
LITERALS = {family: re.compile(rf"(?<![A-Za-z0-9_]){family}-\d{{{width}}}(?!\d)") for family, _p, width in FAMILIES}
#: Where literal identifiers may appear: tests, governance records and this gate.
ALLOWED_PREFIXES = ("engine/tests/", "docs/", "reports/", "scripts/check_evidence_identifiers.py")


def check_registration(text: str) -> list[str]:
    errors = []
    for family, pattern, width in FAMILIES:
        rows = [line for line in text.splitlines() if re.match(rf"^\|\s*[^|]*\|\s*`{family}-", line)]
        if len(rows) != 1:
            errors.append(f"V1 NAMING_STANDARD.md s2 has {len(rows)} {family} rows; exactly one is required")
            continue
        cells = [cell.strip() for cell in rows[0].strip("|").split("|")]
        if cells[1] != f"`{pattern.pattern}`":
            errors.append(f"V1 registered {family} pattern {cells[1]} differs from the code's `{pattern.pattern}`")
        if cells[2] != str(width):
            errors.append(f"V1 registered {family} width {cells[2]} differs from the code's {width}")
        if len(cells) < 6 or not all(cells[3:6]):
            errors.append(f"V1 the {family} row must state scope, issuer and source of law")
    return errors


def check_literals(root: Path, files: list[str]) -> list[str]:
    errors = []
    for relative in files:
        if relative.startswith(ALLOWED_PREFIXES):
            continue
        try:
            text = (root / relative).read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for literal in LITERALS.values():
                for match in literal.finditer(line):
                    errors.append(f"V2 {relative}:{lineno}: literal {match.group(0)}; identifiers come only from the "
                                  f"issuer")
    return errors


def _contiguous(family: str, numbers: list[int], issued: int) -> list[str]:
    errors = []
    if numbers != list(range(1, len(numbers) + 1)):
        errors.append(f"V3 issued {family} numbers are not unique and contiguous from 1: {numbers[:10]}")
    if numbers and numbers[-1] > issued:
        errors.append(f"V3 {family} {numbers[-1]} exceeds the issuer's counter {issued}")
    return errors


def check_store(path: Path) -> list[str]:
    errors = []
    db = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        issuers = dict(db.execute("SELECT family, last_number FROM evidence_issuers"))
        rules = db.execute("SELECT rule_id, version FROM rule_versions ORDER BY rule_id, version").fetchall()
        items = db.execute("SELECT evidence_id, payload FROM evidence_items ORDER BY evidence_id").fetchall()
    finally:
        db.close()
    versions: dict[str, list[int]] = {}
    for rule_id, version in rules:
        if RUL_PATTERN.fullmatch(rule_id) is None:
            errors.append(f"V3 {rule_id!r} is not a RUL identifier")
            continue
        versions.setdefault(rule_id, []).append(version)
    for rule_id, seen in versions.items():
        if seen != list(range(1, len(seen) + 1)):
            errors.append(f"V3 {rule_id} versions are not 1..n: {seen}")
    errors += _contiguous(RUL_FAMILY, sorted(int(rule_id[len(RUL_FAMILY) + 1:]) for rule_id in versions),
                          issuers[RUL_FAMILY])
    numbers = []
    for evidence_id, payload in items:
        if EVD_PATTERN.fullmatch(evidence_id) is None:
            errors.append(f"V3 {evidence_id!r} is not an EVD identifier")
            continue
        numbers.append(int(evidence_id[len(EVD_FAMILY) + 1:]))
        rule = json.loads(payload)["evidence"]["rule"]
        if rule["version"] not in versions.setdefault(rule["rule"], []):
            errors.append(f"V3 {evidence_id} names {rule['rule']} version {rule['version']}, which does not exist")
    errors += _contiguous(EVD_FAMILY, sorted(numbers), issuers[EVD_FAMILY])
    return errors


def tracked_files(root: Path) -> list[str]:
    result = subprocess.run(["git", "-C", str(root), "ls-files"], capture_output=True, text=True, check=True)
    return [line for line in result.stdout.splitlines() if line]


def main(argv: list[str]) -> int:
    naming = Path(argv[argv.index("--naming") + 1]) if "--naming" in argv else NAMING
    errors = check_registration(naming.read_text(encoding="utf-8"))
    errors += check_literals(ROOT, tracked_files(ROOT))
    if "--store" in argv:
        errors += check_store(Path(argv[argv.index("--store") + 1]))
    if errors:
        print(f"FAIL: EVD and RUL identifier families ({len(errors)} failures)")
        for error in errors:
            print(f"    {error}")
        return 1
    print(f"PASS: {EVD_FAMILY} registered as `{EVD_PATTERN.pattern}` (width {EVD_WIDTH}) and {RUL_FAMILY} as "
          f"`{RUL_PATTERN.pattern}` (width {RUL_WIDTH}); no literal identifiers outside the allowed surface")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
