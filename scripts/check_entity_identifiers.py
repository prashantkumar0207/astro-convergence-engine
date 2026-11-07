"""ENT identifier-family uniqueness gate (ADR-0111; ADR-0114 s3 AC1 and AC12; NAMING_STANDARD.md s2).

Part of the identifier conformance sweep. It fails when:

  E1  NAMING_STANDARD.md s2 does not register exactly one ENT row, with the pattern and width
      that engine/evidence/identifiers.py uses;
  E2  a tracked production file outside the test and fixture surface contains a literal ENT
      identifier, because identifiers come only from a store's issuer;
  E3  a store given with --store has an identifier outside the pattern, has a revision
      sequence that does not start at 1 or has gaps, or has issued numbers that are not unique,
      not contiguous from 1, or exceed its issuer's counter.

Exit 0 = PASS, 1 = FAIL. Paths are injectable so the negative controls run the real checks.
"""

from __future__ import annotations

import re
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.evidence.identifiers import FAMILY, PATTERN, WIDTH  # noqa: E402

NAMING = ROOT / "docs" / "NAMING_STANDARD.md"
LITERAL = re.compile(r"(?<![A-Za-z0-9_])ENT-\d{8}(?!\d)")
#: Where literal identifiers may appear: tests, fixtures, governance records and this gate.
ALLOWED_PREFIXES = ("engine/tests/", "docs/", "reports/", "scripts/check_entity_identifiers.py")


def check_registration(text: str) -> list[str]:
    rows = [line for line in text.splitlines() if re.match(rf"^\|\s*[^|]*\|\s*`{FAMILY}-", line)]
    if len(rows) != 1:
        return [f"E1 NAMING_STANDARD.md s2 has {len(rows)} {FAMILY} rows; exactly one is required"]
    cells = [cell.strip() for cell in rows[0].strip("|").split("|")]
    errors = []
    if cells[1] != f"`{PATTERN.pattern}`":
        errors.append(f"E1 registered pattern {cells[1]} differs from the code's `{PATTERN.pattern}`")
    if cells[2] != str(WIDTH):
        errors.append(f"E1 registered width {cells[2]} differs from the code's {WIDTH}")
    if len(cells) < 6 or not all(cells[3:6]):
        errors.append("E1 the ENT row must state scope, issuer and source of law")
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
            for match in LITERAL.finditer(line):
                errors.append(f"E2 {relative}:{lineno}: literal {match.group(0)}; identifiers come only from the issuer")
    return errors


def check_store(path: Path) -> list[str]:
    errors = []
    db = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        rows = db.execute("SELECT entity_id, revision FROM entity_revisions ORDER BY entity_id, revision").fetchall()
        (issued,) = db.execute("SELECT last_number FROM issuer WHERE family = ?", (FAMILY,)).fetchone()
    finally:
        db.close()
    revisions: dict[str, list[int]] = {}
    for entity_id, revision in rows:
        if PATTERN.fullmatch(entity_id) is None:
            errors.append(f"E3 {entity_id!r} is not an ENT identifier")
            continue
        revisions.setdefault(entity_id, []).append(revision)
    for entity_id, seen in revisions.items():
        if seen != list(range(1, len(seen) + 1)):
            errors.append(f"E3 {entity_id} revisions are not 1..n: {seen}")
    numbers = sorted(int(entity_id[len(FAMILY) + 1:]) for entity_id in revisions)
    if len(numbers) != len(set(numbers)):
        errors.append("E3 an ENT number is issued twice")
    if numbers != list(range(1, len(numbers) + 1)):
        errors.append(f"E3 issued ENT numbers are not contiguous from 1: {numbers[:10]}")
    if numbers and numbers[-1] > issued:
        errors.append(f"E3 ENT {numbers[-1]} exceeds the issuer's counter {issued}")
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
        print(f"FAIL: ENT identifier family ({len(errors)} failures)")
        for error in errors:
            print(f"    {error}")
        return 1
    print(f"PASS: {FAMILY} family registered as `{PATTERN.pattern}` (width {WIDTH}); no literal identifiers outside "
          f"the allowed surface")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
