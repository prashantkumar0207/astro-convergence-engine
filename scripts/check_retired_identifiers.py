"""Identifier-family conformance gate (ADR-0014).

NAMING_STANDARD.md s2 fixes the decision family as `ADR-\\d{4}`, width four,
issued only by docs/DECISION_LOG.md. ADR-0004 retired ten provisional
identifiers of other shapes. ADR-0004's rewrite was incomplete for eighteen
months of commits and nobody noticed, because nothing checked. This script is
the check.

Two independent searches, both must pass:

  PATTERN A  exact-string search for each of the ten retired identifiers.
  PATTERN B  family regex: any `ADR-` token NOT followed by exactly four digits.

Pattern B is the operative one. The defect class is an unauthorised identifier
family, not these ten particular strings, so a search that only knows the ten
would miss the eleventh invention.

Allowlisted occurrences are declared below with a reason. Anything else fails.

Run:  python scripts/check_retired_identifiers.py
Exit: 0 clean, 1 on any unauthorised occurrence.
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

#: The ten strings retired by ADR-0004. Never to be reused (ADR-0004 decision).
RETIRED = (
    "ADR-VARGA-D3-001", "ADR-VARGA-D12-001", "ADR-VARGA-D7-001",
    "ADR-VARGA-D30-001", "ADR-VARGA-D2-001", "ADR-KP-001",
    "ADR-DASHA-001", "ADR-TRANSIT-001", "ADR-ASPECT-PAR-001",
    "ADR-CONVENTION-001",
)

#: Any `ADR-` token whose suffix is not exactly four digits.
FAMILY_RE = re.compile(r"ADR-(?!\d{4}(?!\d))[A-Za-z0-9_-]+")

#: Files permitted to contain retired identifiers, each with its reason.
#: These cite the identifiers AS RETIRED; removing the citations would destroy
#: the record of what was retired.
ALLOWED_FILES = {
    "docs/DECISION_LOG.md":
        "the register itself: ADR-0004 retirement list, the 'supersedes provisional' "
        "clauses in ADR-0006/0009/0010/0011/0012 titles, and ADR-0014's replacement map",
    "reports/ALIGNMENT_REVIEW.md":
        "dated evidence: the body records the error, corrected by a superseding note",
    "scripts/check_retired_identifiers.py":
        "this gate must name what it searches for",
}

#: Non-identifier tokens that match FAMILY_RE but are not identifier claims.
ALLOWED_TOKENS = {
    "ADR-XXXX": "register template placeholder",
    "ADR-YYYY": "register template placeholder for a superseding entry",
    "ADR-style": "English prose",
    "ADR-governed": "English prose",
    "ADR-000x": "prose reference to the family in a lock record",
}

#: Deliberate supersession traceability (ADR-0014 decision 2), authorised in
#: exactly three syntactic positions and nowhere else:
#:   JSON field      "supersedes_provisional_id": "ADR-VARGA-D3-001"
#:   rendered report - Supersedes provisional identifier: ADR-VARGA-D3-001
#:   pinning test    report["supersedes_provisional_id"] == "ADR-VARGA-D3-001"
#: The match is bound to the declared key, not to a file, so a retired
#: identifier in any other position still fails wherever it appears.
#:
#: THE VALUE IS VALIDATED, not merely scrubbed. An earlier form of this regex
#: accepted `[^"]+` and `\S+`, which meant ANY token at all passed in the
#: authorised position: a freshly invented identifier family was accepted, and
#: so was a retired identifier belonging to a different varga. That is the exact
#: defect class ADR-0004 retired, surviving inside the gate meant to prevent it.
#: Only one of the ten strings ADR-0004 actually retired may appear here.
#: (The demonstrating probe strings are deliberately NOT written out in this
#: file: Pattern B would flag them, and it did on the first attempt.)
_RETIRED_ALTERNATION = "|".join(re.escape(name) for name in RETIRED)

SUPERSESSION_FIELD_RE = re.compile(
    r'supersedes_provisional_id"?\]?\s*(?::|==)\s*"(?P<json>'
    + _RETIRED_ALTERNATION
    + r')"'
    r"|- Supersedes provisional identifier: (?P<prose>"
    + _RETIRED_ALTERNATION
    + r")(?=\s|$)"
)


#: A division token in a path, e.g. `certify_d30.py`, `VARGA_D7_V1_...`,
#: `varga_d12.report.md`. Used to bind a supersession claim to the division the
#: file is actually about.
_DIVISION_RE = re.compile(r"(?:^|[^a-z0-9])d(\d+)(?:[^0-9]|$)", re.IGNORECASE)

#: Division number -> the retired varga identifier for it, DERIVED from RETIRED
#: rather than written out. Deriving it keeps one source of truth and, secondarily,
#: avoids planting a partial identifier literal in this file: Pattern B flags any
#: `ADR-` token that is not four digits, and an f-string prefix is exactly that.
#: Found the hard way, twice.
_VARGA_BY_DIVISION: dict[int, str] = {}
for _retired_name in RETIRED:
    _parts = _retired_name.split("-")
    if (
        len(_parts) == 4
        and _parts[1] == "VARGA"
        and _parts[2][:1].upper() == "D"
        and _parts[2][1:].isdigit()
    ):
        _VARGA_BY_DIVISION[int(_parts[2][1:])] = _retired_name


def authorised_supersession(rel: str) -> str | None:
    """The one retired identifier this file may claim to supersede, if known.

    ADR-0014 D1 fixed a replacement map, division by division. Permitting any
    retired identifier in the authorised position would let a D3 artifact claim
    it superseded the D12 provisional entry, which is a traceability error the
    gate exists to catch. Where a division can be read off the path, the claim
    is bound to it. Where it cannot, any retired identifier is permitted, which
    is the pre-existing behaviour and is reported as such rather than silently
    relaxed.
    """

    match = _DIVISION_RE.search(Path(rel).name)
    if not match:
        return None
    return _VARGA_BY_DIVISION.get(int(match.group(1)))


def scrub_supersession(rel: str, line: str) -> str:
    """Remove an AUTHORISED supersession claim from a line, and only that.

    A claim whose value is not a retired identifier, or is the wrong retired
    identifier for this file's division, is left in the line so the ordinary
    Pattern A and Pattern B checks flag it.
    """

    expected = authorised_supersession(rel)

    def replace(match: "re.Match[str]") -> str:
        claimed = match.group("json") or match.group("prose")
        if expected is not None and claimed != expected:
            return match.group(0)  # wrong division: leave it to be flagged
        return ""

    return SUPERSESSION_FIELD_RE.sub(replace, line)


def tracked_files() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True
    )
    return [line for line in out.stdout.splitlines() if line]


def scan() -> tuple[list[str], list[str]]:
    """Return (pattern_a_violations, pattern_b_violations)."""
    a_hits: list[str] = []
    b_hits: list[str] = []

    for rel in tracked_files():
        path = ROOT / rel
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue  # binary asset

        allowed_file = rel in ALLOWED_FILES

        for lineno, line in enumerate(text.splitlines(), start=1):
            # Deliberate structured supersession is authorised anywhere.
            scrubbed = scrub_supersession(rel, line)

            if not allowed_file:
                for retired in RETIRED:
                    if retired in scrubbed:
                        a_hits.append(f"{rel}:{lineno}: {retired}")

            for match in FAMILY_RE.finditer(scrubbed):
                token = match.group(0)
                if token in ALLOWED_TOKENS:
                    continue
                if allowed_file and token in RETIRED:
                    continue
                b_hits.append(f"{rel}:{lineno}: {token}")

    return a_hits, b_hits


def main() -> int:
    a_hits, b_hits = scan()

    print("PATTERN A  exact retired identifiers, outside the allowlist")
    print(f"  violations: {len(a_hits)}")
    for hit in a_hits:
        print(f"    {hit}")

    print("PATTERN B  ADR- tokens not matching ADR-<4 digits>")
    print(f"  violations: {len(b_hits)}")
    for hit in b_hits:
        print(f"    {hit}")

    if a_hits or b_hits:
        print()
        print("FAIL: unauthorised decision identifiers present.")
        print("Do not silence this by widening the allowlist. Either use a compliant")
        print("ADR-<4 digits> number issued by docs/DECISION_LOG.md, or, if a new")
        print("identifier family is genuinely needed, give it a NAMING_STANDARD.md s2")
        print("table entry and a decision entry first.")
        return 1

    print()
    print("PASS: every decision identifier is ADR-<4 digits>, or an allowlisted citation.")
    for rel, reason in ALLOWED_FILES.items():
        print(f"  allowlisted file: {rel}")
        print(f"    reason: {reason}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
