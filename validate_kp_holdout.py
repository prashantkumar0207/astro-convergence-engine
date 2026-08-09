"""Independent KP chain holdout validator (Gate 5 of ADR-KP-001).

Validates engine/kp against a reference implementation derived
INDEPENDENTLY inside this file from the classical rule: the KP
sub-lord table is built as an explicit flat interval table (prefix
sums + bisect), a different construction from the engine's recursive
walk. No reference value is imported from engine/kp or legacy/.

Run:  python validate_kp_holdout.py
"""

import bisect
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from engine.kp.chain import kp_chain  # SUBJECT under validation

# ---------------------------------------------------------------- reference
# Vimshottari sequence per BPHS as used by KP: lords and years.
REF_LORDS = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter",
             "Saturn", "Mercury"]
REF_YEARS = {"Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
             "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17}
REF_ABBREV = {"Ketu": "Ke", "Venus": "Ve", "Sun": "Su", "Moon": "Mo",
              "Mars": "Ma", "Rahu": "Ra", "Jupiter": "Ju", "Saturn": "Sa",
              "Mercury": "Me"}
REF_SIGN_LORDS = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
                  "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
SPAN = Fraction(40, 3)          # nakshatra span, exactly 13 deg 20 min
TOTAL = Fraction(120)           # Vimshottari total years


def build_interval_table():
    """Flat [start, end) table of (NL, SB, SS) across [0, 360)."""
    table = []          # (start, nl, sb, ss)
    for nak in range(27):
        nak_start = nak * SPAN
        nl = REF_LORDS[nak % 9]
        sub_cursor = nak_start
        nl_index = REF_LORDS.index(nl)
        for s in range(9):
            sb = REF_LORDS[(nl_index + s) % 9]
            sub_width = SPAN * REF_YEARS[sb] / TOTAL
            ss_cursor = sub_cursor
            sb_index = REF_LORDS.index(sb)
            for s2 in range(9):
                ss = REF_LORDS[(sb_index + s2) % 9]
                ss_width = sub_width * REF_YEARS[ss] / TOTAL
                table.append((ss_cursor, nl, sb, ss))
                ss_cursor += ss_width
            sub_cursor += sub_width
    assert len(table) == 27 * 81
    assert table[0][0] == 0 and sub_cursor == 360
    return table


TABLE = build_interval_table()
STARTS = [row[0] for row in TABLE]


def reference_chain(exact: Fraction):
    exact = exact % 360
    row = TABLE[bisect.bisect_right(STARTS, exact) - 1]
    sign = int(exact // 30)
    return (
        REF_ABBREV[REF_SIGN_LORDS[sign]],
        REF_ABBREV[row[1]],
        REF_ABBREV[row[2]],
        REF_ABBREV[row[3]],
        sign + 1,
        int(exact // SPAN) + 1,
    )


def subject_tuple(value):
    chain = kp_chain(value)
    return (chain.sign_lord, chain.nakshatra_lord, chain.sub_lord,
            chain.sub_sub_lord, chain.sign_number, chain.nakshatra_number)


def to_exact(value):
    from decimal import Decimal
    if isinstance(value, Fraction):
        return value
    return Fraction(Decimal(str(value)))


def main() -> int:
    failures = []

    # 1. Dense sweep: 51,429 float points.
    step = 360.0 / 51429
    dense = 0
    for i in range(51429):
        lon = i * step
        if subject_tuple(lon) != reference_chain(to_exact(lon)):
            failures.append(("dense", lon))
        dense += 1

    # 2. Boundary battery: every interval start, exact, +/- 1e-9 rational.
    eps = Fraction(1, 10**9)
    boundary = 0
    for start in STARTS:
        for point in (start, start + eps, start - eps if start > 0 else None):
            if point is None:
                continue
            if subject_tuple(point) != reference_chain(point):
                failures.append(("boundary", float(point)))
            boundary += 1

    # 3. Classical anchors (hand-derived).
    anchors = [
        (Fraction(0), ("Ma", "Ke", "Ke", "Ke", 1, 1)),          # 0 Aries, Ashwini start
        (SPAN, ("Ma", "Ve", "Ve", "Ve", 1, 2)),                 # Bharani start
        (SPAN * 7 / 120, ("Ma", "Ke", "Ve", "Ve", 1, 1)),       # end of Ashwini Ketu sub
        (Fraction(30), ("Ve", "Su", "Ra", "Sa", 2, 3)),         # 0 Taurus in Krittika (Sun star)
        (Fraction(280), ("Sa", "Mo", "Mo", "Mo", 10, 22)),      # exact Shravana start (Moon star)
    ]
    anchor_count = 0
    for point, expected in anchors:
        if subject_tuple(point) != expected or reference_chain(point) != expected:
            failures.append(("anchor", float(point)))
        anchor_count += 1

    print("=" * 60)
    print("INDEPENDENT KP CHAIN HOLDOUT VALIDATION")
    print("=" * 60)
    print(f"Dense sweep cases    : {dense}")
    print(f"Boundary cases       : {boundary}")
    print(f"Classical anchors    : {anchor_count}")
    if failures:
        print(f"FAILURES: {len(failures)}; first: {failures[:5]}")
        print("RESULT: FAIL")
        return 1
    print()
    print("RESULT: ALL INDEPENDENT KP CHAIN CASES PASSED")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
