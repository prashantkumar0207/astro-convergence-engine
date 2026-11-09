"""EVR identifier-family uniqueness gate, and the event-class seed check (ADR-0113 s2 B, C1; ADR-0115 s5).

Part of the identifier conformance sweep. It fails when:

  V1  NAMING_STANDARD.md s2 does not register exactly one EVR row, with the pattern and width that
      engine/evidence/event_identifiers.py uses, and a scope, issuer and source of law;
  V2  a tracked production file outside the test and governance surface contains a literal EVR
      identifier, because identifiers come only from a store's issuer;
  V3  a store given with --store has an identifier outside the pattern, a revision sequence that
      does not start at 1 or has gaps, issued numbers that are not unique, not contiguous from 1 or
      above its issuer's counter, or a confirmation naming a revision that does not exist;
  V4  engine/evidence/event_classes.py's seed differs from the career event registry's s3 rows in
      identifier, name, group, origin or order, read here independently of the code's own parsing.

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

from engine.evidence.event_classes import REGISTRY_PATH, SEED  # noqa: E402
from engine.evidence.event_identifiers import FAMILY, PATTERN, WIDTH  # noqa: E402

NAMING = ROOT / "docs" / "NAMING_STANDARD.md"
REGISTRY = ROOT / REGISTRY_PATH
LITERAL = re.compile(r"(?<![A-Za-z0-9_])EVR-\d{8}(?!\d)")
#: Where literal identifiers may appear: tests, governance records and this gate.
ALLOWED_PREFIXES = ("engine/tests/", "docs/", "reports/", "scripts/check_event_identifiers.py")
_GROUP = re.compile(r"^## 3\.\d+ Group: (\w+) \((\d+) events\)\s*$")


def check_registration(text: str) -> list[str]:
    rows = [line for line in text.splitlines() if re.match(rf"^\|\s*[^|]*\|\s*`{FAMILY}-", line)]
    if len(rows) != 1:
        return [f"V1 NAMING_STANDARD.md s2 has {len(rows)} {FAMILY} rows; exactly one is required"]
    cells = [cell.strip() for cell in rows[0].strip("|").split("|")]
    errors = []
    if cells[1] != f"`{PATTERN.pattern}`":
        errors.append(f"V1 registered pattern {cells[1]} differs from the code's `{PATTERN.pattern}`")
    if cells[2] != str(WIDTH):
        errors.append(f"V1 registered width {cells[2]} differs from the code's {WIDTH}")
    if len(cells) < 6 or not all(cells[3:6]):
        errors.append(f"V1 the {FAMILY} row must state scope, issuer and source of law")
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
                errors.append(f"V2 {relative}:{lineno}: literal {match.group(0)}; identifiers come only from the issuer")
    return errors


def registry_rows(text: str) -> tuple[list[tuple], dict[str, int]]:
    """(identifier, name, group, origin) for every s3 row, in order, and each group's stated count."""

    section = text.split("\n## 4.")[0]
    rows, group, stated = [], None, {}
    for line in section.splitlines():
        heading = _GROUP.match(line)
        if heading:
            group = heading.group(1).lower()
            stated[group] = int(heading.group(2))
            continue
        if line.startswith("| EV-CAR-"):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            rows.append((cells[0], cells[1].strip("`"), group, cells[5]))
    return rows, stated


def check_seed(text: str, seed=SEED) -> list[str]:
    rows, stated = registry_rows(text)
    errors = []
    counted: dict[str, int] = {}
    for _identifier, _name, group, _origin in rows:
        counted[group] = counted.setdefault(group, 0) + 1
    if counted != stated:
        errors.append(f"V4 the registry's group headings state {stated}, but its rows give {counted}")
    code = [(entry.class_id, entry.name, entry.group, entry.origin.value) for entry in seed]
    if code != rows:
        missing = sorted(set(rows) - set(code))
        extra = sorted(set(code) - set(rows))
        errors.append(f"V4 the event-class seed differs from {REGISTRY_PATH} s3: missing {missing[:5]}, "
                      f"not in the registry {extra[:5]}" + ("" if missing or extra else ", order differs"))
    if len({row[0] for row in code}) != len(code) or len({row[1] for row in code}) != len(code):
        errors.append("V4 an event-class identifier or name appears twice in the seed")
    return errors


def check_store(path: Path) -> list[str]:
    errors = []
    db = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        rows = db.execute("SELECT event_id, revision FROM event_revisions ORDER BY event_id, revision").fetchall()
        (issued,) = db.execute("SELECT last_number FROM event_issuer WHERE family = ?", (FAMILY,)).fetchone()
        answers = db.execute("SELECT event_id, revision FROM event_confirmations").fetchall()
    finally:
        db.close()
    revisions: dict[str, list[int]] = {}
    for event_id, revision in rows:
        if PATTERN.fullmatch(event_id) is None:
            errors.append(f"V3 {event_id!r} is not an EVR identifier")
            continue
        revisions.setdefault(event_id, []).append(revision)
    for event_id, seen in revisions.items():
        if seen != list(range(1, len(seen) + 1)):
            errors.append(f"V3 {event_id} revisions are not 1..n: {seen}")
    numbers = sorted(int(event_id[len(FAMILY) + 1:]) for event_id in revisions)
    if numbers != list(range(1, len(numbers) + 1)):
        errors.append(f"V3 issued EVR numbers are not contiguous from 1: {numbers[:10]}")
    if numbers and numbers[-1] > issued:
        errors.append(f"V3 EVR {numbers[-1]} exceeds the issuer's counter {issued}")
    for event_id, revision in answers:
        if event_id not in revisions or revision not in revisions[event_id]:
            errors.append(f"V3 a confirmation names {event_id} revision {revision}, which does not exist")
    return errors


def tracked_files(root: Path) -> list[str]:
    result = subprocess.run(["git", "-C", str(root), "ls-files"], capture_output=True, text=True, check=True)
    return [line for line in result.stdout.splitlines() if line]


def main(argv: list[str]) -> int:
    naming = Path(argv[argv.index("--naming") + 1]) if "--naming" in argv else NAMING
    registry = Path(argv[argv.index("--registry") + 1]) if "--registry" in argv else REGISTRY
    errors = check_registration(naming.read_text(encoding="utf-8"))
    errors += check_literals(ROOT, tracked_files(ROOT))
    errors += check_seed(registry.read_text(encoding="utf-8"))
    if "--store" in argv:
        errors += check_store(Path(argv[argv.index("--store") + 1]))
    if errors:
        print(f"FAIL: EVR identifier family and event-class seed ({len(errors)} failures)")
        for error in errors:
            print(f"    {error}")
        return 1
    print(f"PASS: {FAMILY} family registered as `{PATTERN.pattern}` (width {WIDTH}); no literal identifiers outside "
          f"the allowed surface; {len(SEED)} seeded event classes match the registry")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
