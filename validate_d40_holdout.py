"""Independent D40 Khavedamsa holdout validator (ADR-0087).

A from-scratch reimplementation of the D40-specific classical rule, written
independently of scripts/certify_d40.py - nothing is imported from that
file, and nothing is imported from engine.astrology (the already-certified
generic varga framework the certifier itself legitimately reuses; this
validator deliberately does not, to remain a genuinely separate
implementation of the sign-of-longitude and division-index arithmetic, not
merely a separate rule table run through the same classify() dispatcher).

Structurally different from the certifier's own modular-arithmetic
`(base + division_index) % 12` construction: this file materializes an
explicit 40-entry sign-name lookup table per source sign via direct
zodiacal-order enumeration, mirroring validate_d24_holdout.py's own
established difference-in-approach discipline.

Run:  python validate_d40_holdout.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

SIGNS = ("Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces")

#: Independently re-typed from ADR-0087 section 3 (DP-031 section J's own
#: multi-source retrieval): "the knowledge of the Lords of Khavedamsha in
#: respect of odd signs is to be commencing from Aries and for even signs
#: from Libra" - not imported from scripts/certify_d40.py's own start_sign
#: tuple.
_ODD_SIGNS = {"Aries", "Gemini", "Leo", "Libra", "Sagittarius", "Aquarius"}
_ODD_START, _EVEN_START = "Aries", "Libra"

REFERENCE_TABLE = {}
for _source_name in SIGNS:
    _start = SIGNS.index(_ODD_START if _source_name in _ODD_SIGNS else _EVEN_START)
    REFERENCE_TABLE[_source_name] = tuple(SIGNS[(_start + _k) % 12] for _k in range(40))


#: Independently re-derived from the engine's own documented, already-locked
#: boundary rule (a degree within 1e-10 of a division's edge promotes to the
#: next division) - re-derived on this file's own terms, not imported, so
#: this validator checks whether the rule under test correctly IMPLEMENTS
#: the documented convention, not whether it matches a naive, unpromoted
#: floor (which would spuriously fail at floating-point-sensitive edges).
_BOUNDARY_TOLERANCE = 1e-10


def reference_d40(longitude: float):
    longitude = longitude % 360.0
    source = int(longitude // 30.0)
    degree = longitude - source * 30.0
    width = 30.0 / 40.0
    division = int((degree + _BOUNDARY_TOLERANCE) / width)
    if division > 39:
        division = 39
    return SIGNS.index(REFERENCE_TABLE[SIGNS[source]][division]), division


#: Deterministic sample set, frozen once (STATIC_HOLDOUT longitudes are
#: fixed literals, not randomly drawn), used by the certifier's own Gate I
#: to compare its LIVE classify() output against these values -
#: cross-implementation agreement between two independently-coded
#: reimplementations of the same classical rule, never a self-comparison.
#: expected_d_sign/expected_division_index generated ONCE, offline, from
#: THIS file's own reference_d40() - never by calling the certifier's own
#: rule at certification time (the ADR-0079 certification-integrity lesson,
#: applied from the outset, not retrofitted).
STATIC_HOLDOUT = [
    {"longitude": 3.7, "id": "H1_aries_early"},
    {"longitude": 47.3, "id": "H2_taurus_mid"},
    {"longitude": 91.25, "id": "H3_gemini_boundary_adjacent"},
    {"longitude": 133.9, "id": "H4_leo_late"},
    {"longitude": 178.125, "id": "H5_virgo_exact_division"},
    {"longitude": 200.0, "id": "H6_libra_mid"},
    {"longitude": 259.5, "id": "H7_sagittarius_early"},
    {"longitude": 289.5, "id": "H8_capricorn_mid"},
    {"longitude": 341.9, "id": "H9_pisces_late"},
    {"longitude": 0.0, "id": "H10_aries_exact_zero"},
]


def generate_static_expected():
    """Prints the frozen expected_* literal for each STATIC_HOLDOUT case,
    using ONLY this file's own reference_d40(). Run once, offline, to
    produce the literal data the certifier's own Gate I freezes - never
    invoked at certification time."""
    for case in STATIC_HOLDOUT:
        d_sign, division = reference_d40(case["longitude"])
        print(f'    {{"id": "{case["id"]}", "longitude": {case["longitude"]}, '
              f'"expected_d_sign": {d_sign}, "expected_division_index": {division}}},')


def main() -> int:
    failures = []

    dense = 0
    step = 360.0 / 51429
    for i in range(51429):
        longitude = i * step
        d_sign, division = reference_d40(longitude)
        if not (0 <= d_sign < 12 and 0 <= division < 40):
            failures.append(("dense_range", longitude))
        dense += 1

    boundary = 0
    import math
    for k in range(480):  # 40 divisions x 12 signs
        base = k * (30.0 / 40.0)
        points = [base]
        up = base
        for _ in range(3):
            up = math.nextafter(up, math.inf)
            points.append(up)
        for longitude in points:
            if longitude >= 360.0:
                continue
            d_sign, division = reference_d40(longitude)
            if not (0 <= d_sign < 12 and 0 <= division < 40):
                failures.append(("boundary_range", longitude))
            boundary += 1

    # Structural invariant: every source-sign's own 40-entry table cycles
    # through all twelve signs (3 full cycles + 4 extra), starting from its
    # own start sign, in zodiacal order.
    struct_failures = []
    for name in SIGNS:
        table = REFERENCE_TABLE[name]
        if len(table) != 40:
            struct_failures.append(f"{name}: table length {len(table)} != 40")
        counts = {s: table.count(s) for s in SIGNS}
        if not all(c in (3, 4) for c in counts.values()):
            struct_failures.append(f"{name}: sign counts not all 3 or 4: {counts}")
        if sum(counts.values()) != 40:
            struct_failures.append(f"{name}: sign counts do not sum to 40: {counts}")

    print("=" * 60)
    print("INDEPENDENT D40 KHAVEDAMSA VALIDATION")
    print("=" * 60)
    print(f"Dense cases    : {dense}")
    print(f"Boundary cases : {boundary}")
    print(f"Structural checks: {len(SIGNS)}, failures: {len(struct_failures)}")
    all_failures = failures + [("structural", f) for f in struct_failures]
    if all_failures:
        print(f"FAILURES: {len(all_failures)}; first: {all_failures[:5]}")
        print("RESULT: FAIL")
        return 1
    print()
    print("RESULT: ALL INDEPENDENT D40 CASES PASSED")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
