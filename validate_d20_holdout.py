"""Independent D20 Vimsamsa holdout validator (ADR-0095).

A from-scratch reimplementation of the D20-specific classical rule, written
independently of scripts/certify_d20.py - nothing is imported from that
file, and nothing is imported from engine.astrology (the already-certified
generic varga framework the certifier itself legitimately reuses; this
validator deliberately does not, to remain a genuinely separate
implementation of the sign-of-longitude and division-index arithmetic, not
merely a separate rule table run through the same classify() dispatcher).

Structurally different from the certifier's own modular-arithmetic
`(start_sign + division_index) % 12` construction: this file materializes an
explicit 20-entry sign-NAME lookup table per source sign by direct zodiacal
enumeration, keyed by sign name rather than by integer index, mirroring
validate_d16_holdout.py's own established difference-in-approach discipline.

ADR-0095 records that this selection is NOT proof of the historical original
text: no verbatim Sanskrit was located, and primary-source uncertainty is
not eliminated. This validator checks conformance to the SELECTED reading
(Reading E), not historical correctness, and cannot speak to the latter.

Run:  python validate_d20_holdout.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

SIGNS = ("Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces")

#: Independently re-typed from ADR-0095 section 1's own classical statement
#: ("From Aries for a Movable Rasi, from Sagittarius for a Fixed Rasi and
#: from Leo for a Common Rasi"), NOT imported from scripts/certify_d20.py's
#: own start_sign tuple and not copied from that tuple's integer form.
_MOVABLE_SIGNS = {"Aries", "Cancer", "Libra", "Capricorn"}
_FIXED_SIGNS = {"Taurus", "Leo", "Scorpio", "Aquarius"}
_DUAL_SIGNS = {"Gemini", "Virgo", "Sagittarius", "Pisces"}
_MOVABLE_START, _FIXED_START, _DUAL_START = "Aries", "Sagittarius", "Leo"

#: ADR-0095's explicitly EXCLUDED variant, retained here by name only so the
#: certifier's own Gate H negative control can plant it. It is never used by
#: reference_d20() and is not offered as a selectable methodology. Recorded
#: as attested and NOT refuted - see ADR-0095 section 3.
EXCLUDED_VARIANT_F_STARTS = {"movable": "Aries", "fixed": "Leo", "dual": "Sagittarius"}


def _start_for(source_name: str) -> str:
    if source_name in _MOVABLE_SIGNS:
        return _MOVABLE_START
    if source_name in _FIXED_SIGNS:
        return _FIXED_START
    return _DUAL_START


REFERENCE_TABLE = {}
for _source_name in SIGNS:
    _start = SIGNS.index(_start_for(_source_name))
    REFERENCE_TABLE[_source_name] = tuple(SIGNS[(_start + _k) % 12] for _k in range(20))


#: Independently re-derived from the engine's own documented, already-locked
#: boundary rule (a degree within 1e-10 of a division's edge promotes to the
#: next division) - re-derived on this file's own terms, not imported, so
#: this validator checks whether the rule under test correctly IMPLEMENTS
#: the documented convention, not whether it matches a naive, unpromoted
#: floor.
_BOUNDARY_TOLERANCE = 1e-10

#: D20-specific: 30/20 = 1.5 exactly, and every internal boundary k*1.5 for
#: k in 1..19 is an exact binary fraction (all are multiples of 0.5). Unlike
#: D7/D9/D27 there is NO representability error here, so a boundary
#: disagreement indicates a convention or table defect, never float drift.
_WIDTH = 30.0 / 20.0


def reference_d20(longitude: float):
    longitude = longitude % 360.0
    source = int(longitude // 30.0)
    degree = longitude - source * 30.0
    division = int((degree + _BOUNDARY_TOLERANCE) / _WIDTH)
    if division > 19:
        division = 19
    return SIGNS.index(REFERENCE_TABLE[SIGNS[source]][division]), division


#: Deterministic sample set, frozen once (STATIC_HOLDOUT longitudes are
#: fixed literals, not randomly drawn), used by the certifier's own Gate I
#: to compare its LIVE classify() output against these values -
#: cross-implementation agreement between two independently-coded
#: reimplementations of the same classical rule, never a self-comparison.
#: expected_* generated ONCE, offline, from THIS file's own reference_d20()
#: - never by calling the certifier's own rule at certification time (the
#: ADR-0079 certification-integrity lesson, applied from the outset).
STATIC_HOLDOUT = [
    {"longitude": 2.9, "id": "H1_aries_early"},
    {"longitude": 43.5, "id": "H2_taurus_exact_division"},
    {"longitude": 76.4, "id": "H3_gemini_mid"},
    {"longitude": 105.75, "id": "H4_cancer_boundary_adjacent"},
    {"longitude": 139.5, "id": "H5_leo_exact_division"},
    {"longitude": 168.2, "id": "H6_virgo_late"},
    {"longitude": 195.0, "id": "H7_libra_exact_division"},
    {"longitude": 244.8, "id": "H8_sagittarius_mid"},
    {"longitude": 317.25, "id": "H9_aquarius_late"},
    {"longitude": 0.0, "id": "H10_aries_exact_zero"},
]


def generate_static_expected():
    """Prints the frozen expected_* literal for each STATIC_HOLDOUT case,
    using ONLY this file's own reference_d20(). Run once, offline, to
    produce the literal data the certifier's own Gate I freezes - never
    invoked at certification time."""
    for case in STATIC_HOLDOUT:
        d_sign, division = reference_d20(case["longitude"])
        print(f'    {{"id": "{case["id"]}", "longitude": {case["longitude"]}, '
              f'"expected_d_sign": {d_sign}, "expected_division_index": {division}}},')


def main() -> int:
    failures = []

    dense = 0
    step = 360.0 / 51429
    for i in range(51429):
        longitude = i * step
        d_sign, division = reference_d20(longitude)
        if not (0 <= d_sign < 12 and 0 <= division < 20):
            failures.append(("dense_range", longitude))
        dense += 1

    boundary = 0
    import math
    for k in range(240):  # 20 divisions x 12 signs
        base = k * _WIDTH
        points = [base]
        up = base
        for _ in range(3):
            up = math.nextafter(up, math.inf)
            points.append(up)
        for longitude in points:
            if longitude >= 360.0:
                continue
            d_sign, division = reference_d20(longitude)
            if not (0 <= d_sign < 12 and 0 <= division < 20):
                failures.append(("boundary_range", longitude))
            boundary += 1

    # Structural invariant: every source sign's own 20-entry table runs one
    # full zodiacal cycle plus eight, so every sign appears once or twice
    # and the counts sum to 20.
    struct_failures = []
    for name in SIGNS:
        table = REFERENCE_TABLE[name]
        if len(table) != 20:
            struct_failures.append(f"{name}: table length {len(table)} != 20")
        counts = {s: table.count(s) for s in SIGNS}
        if not all(c in (1, 2) for c in counts.values()):
            struct_failures.append(f"{name}: sign counts not all 1 or 2: {counts}")
        if sum(counts.values()) != 20:
            struct_failures.append(f"{name}: sign counts do not sum to 20: {counts}")
        if table[0] != _start_for(name):
            struct_failures.append(f"{name}: first entry {table[0]} != start {_start_for(name)}")

    # D20-specific: exact binary representability of every internal boundary.
    from fractions import Fraction
    repr_failures = [k for k in range(1, 20)
                     if Fraction(k * _WIDTH) != Fraction(3 * k, 2)]

    print("=" * 60)
    print("INDEPENDENT D20 VIMSAMSA VALIDATION")
    print("=" * 60)
    print(f"Dense cases    : {dense}")
    print(f"Boundary cases : {boundary}")
    print(f"Structural checks: {len(SIGNS)}, failures: {len(struct_failures)}")
    print(f"Exact-representability failures (k*1.5): {len(repr_failures)}")
    all_failures = (failures
                    + [("structural", f) for f in struct_failures]
                    + [("representability", k) for k in repr_failures])
    if all_failures:
        print(f"FAILURES: {len(all_failures)}; first: {all_failures[:5]}")
        print("RESULT: FAIL")
        return 1
    print()
    print("RESULT: ALL INDEPENDENT D20 CASES PASSED")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
