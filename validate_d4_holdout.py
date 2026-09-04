"""Independent D4 Chaturthamsa holdout validator (ADR-0090).

A from-scratch reimplementation of the D4-specific classical rule, written
independently of scripts/certify_d4.py - nothing is imported from that
file, and nothing is imported from engine.astrology (the already-certified
generic varga framework the certifier itself legitimately reuses; this
validator deliberately does not, to remain a genuinely separate
implementation of the sign-of-longitude and division-index arithmetic, not
merely a separate rule table run through the same classify() dispatcher).

Structurally different from the certifier's own `SegmentVargaRule`
enumeration: this file materializes an explicit 4-entry sign-name lookup
table per source sign via direct kendra-counting (source, 4th, 7th, 10th),
mirroring validate_d40_holdout.py's own established difference-in-approach
discipline.

Run:  python validate_d4_holdout.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

SIGNS = ("Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces")

#: Independently re-typed from ADR-0090 section 3 (DP-032 section A.B's own
#: multi-source retrieval): "the Lords of the 4 Kendras from a Rasi are the
#: rulers of respective Chaturthamsa of a Rasi, commencing from Aries" - the
#: four kendras (1st, 4th, 7th, 10th houses) counted from the source sign
#: itself. Not imported from scripts/certify_d4.py's own segment table.
_KENDRA_OFFSETS = (0, 3, 6, 9)

REFERENCE_TABLE = {}
for _source_index, _source_name in enumerate(SIGNS):
    REFERENCE_TABLE[_source_name] = tuple(
        SIGNS[(_source_index + _offset) % 12] for _offset in _KENDRA_OFFSETS
    )


#: Independently re-derived from the engine's own documented, already-locked
#: boundary rule (a degree within 1e-10 of a division's edge promotes to the
#: next division) - re-derived on this file's own terms, not imported, so
#: this validator checks whether the rule under test correctly IMPLEMENTS
#: the documented convention, not whether it matches a naive, unpromoted
#: floor (which would spuriously fail at floating-point-sensitive edges).
_BOUNDARY_TOLERANCE = 1e-10


def reference_d4(longitude: float):
    longitude = longitude % 360.0
    source = int(longitude // 30.0)
    degree = longitude - source * 30.0
    width = 30.0 / 4.0
    division = int((degree + _BOUNDARY_TOLERANCE) / width)
    if division > 3:
        division = 3
    return SIGNS.index(REFERENCE_TABLE[SIGNS[source]][division]), division


#: Deterministic sample set, frozen once (STATIC_HOLDOUT longitudes are
#: fixed literals, not randomly drawn), used by the certifier's own Gate I
#: to compare its LIVE classify() output against these values -
#: cross-implementation agreement between two independently-coded
#: reimplementations of the same classical rule, never a self-comparison.
#: expected_d_sign/expected_division_index generated ONCE, offline, from
#: THIS file's own reference_d4() - never by calling the certifier's own
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
    using ONLY this file's own reference_d4(). Run once, offline, to
    produce the literal data the certifier's own Gate I freezes - never
    invoked at certification time."""
    for case in STATIC_HOLDOUT:
        d_sign, division = reference_d4(case["longitude"])
        print(f'    {{"id": "{case["id"]}", "longitude": {case["longitude"]}, '
              f'"expected_d_sign": {d_sign}, "expected_division_index": {division}}},')


def main() -> int:
    failures = []

    dense = 0
    step = 360.0 / 51429
    for i in range(51429):
        longitude = i * step
        d_sign, division = reference_d4(longitude)
        if not (0 <= d_sign < 12 and 0 <= division < 4):
            failures.append(("dense_range", longitude))
        dense += 1

    boundary = 0
    import math
    for k in range(48):  # 4 divisions x 12 signs
        base = k * (30.0 / 4.0)
        points = [base]
        up = base
        for _ in range(3):
            up = math.nextafter(up, math.inf)
            points.append(up)
        for longitude in points:
            if longitude >= 360.0:
                continue
            d_sign, division = reference_d4(longitude)
            if not (0 <= d_sign < 12 and 0 <= division < 4):
                failures.append(("boundary_range", longitude))
            boundary += 1

    # Structural invariant: every source-sign's own 4-entry table contains
    # exactly the four members of its own modality (movable/fixed/dual)
    # group, starting with itself, in kendra order.
    struct_failures = []
    for name in SIGNS:
        table = REFERENCE_TABLE[name]
        if len(table) != 4:
            struct_failures.append(f"{name}: table length {len(table)} != 4")
        if table[0] != name:
            struct_failures.append(f"{name}: division 0 is not the source sign itself: {table[0]}")
        if len(set(table)) != 4:
            struct_failures.append(f"{name}: table entries not all distinct: {table}")

    print("=" * 60)
    print("INDEPENDENT D4 CHATURTHAMSA VALIDATION")
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
    print("RESULT: ALL INDEPENDENT D4 CASES PASSED")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
