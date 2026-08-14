"""ADR numbering gate (Q14; ADR-0029 established the rule this enforces).

Asserts two properties of `docs/DECISION_LOG.md`:

  UNIQUENESS  no ADR number appears twice as an entry heading;
  ORDER       entry headings ascend, because ADR-0029 decided the register is
              ordered by IDENTIFIER rather than by append time.

Gaps are legal. ADR-0015 through ADR-0017 are reserved and unissued, and a gap
is not an ordering failure.

WHY THIS IS A SCRIPT AND NOT INLINE YAML. The check previously lived as a
heredoc inside `.github/workflows/ci.yml`, which meant a negative control would
have had to duplicate the regex and both assertions. Two copies of a rule drift.
Here the gate and its negative control run THE SAME code against different
input, so the control proves the real gate can fail rather than proving that a
copy of it can.

Usage:
    python scripts/check_adr_numbering.py [path-to-register]

Exit 0 on PASS, 1 on any violation, 2 if the register cannot be read.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DEFAULT_REGISTER = ROOT / "docs" / "DECISION_LOG.md"

#: An ENTRY heading. Four digits, then a space, so the `ADR-XXXX` template
#: heading at the foot of the register is not counted, and so an addendum using
#: a level-three heading is not counted either (ADR-0029 decision 2).
ENTRY_RE = re.compile(r"^## ADR-(\d{4}) ", re.MULTILINE)


def numbers(text: str) -> list[int]:
    return [int(m) for m in ENTRY_RE.findall(text)]


def check(text: str) -> list[str]:
    """Return a list of violations. Empty means PASS."""

    found = numbers(text)
    errors: list[str] = []
    if not found:
        errors.append(
            "no ADR entry headings found; either the register is empty or the "
            "heading format changed, and in both cases this gate is no longer "
            "checking anything"
        )
        return errors
    if len(found) != len(set(found)):
        duplicates = sorted({n for n in found if found.count(n) > 1})
        errors.append(f"duplicate ADR numbers: {duplicates}")
    if found != sorted(found):
        errors.append(f"ADR numbers not monotonic: {found}")
    return errors


def main(argv: list[str]) -> int:
    target = Path(argv[1]) if len(argv) > 1 else DEFAULT_REGISTER
    try:
        text = target.read_text()
    except OSError as exc:
        print(f"FAIL: cannot read {target}: {exc}")
        return 2

    errors = check(text)
    if errors:
        for error in errors:
            print("FAIL:", error)
        return 1

    found = numbers(text)
    print(
        f"PASS: {len(found)} ADR entries in {target.name}, unique and "
        f"monotonic: ADR-{found[0]:04d}..ADR-{found[-1]:04d}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
