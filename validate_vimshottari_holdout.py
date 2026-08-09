"""Independent Vimshottari holdout validator (Gate 4 of ADR-DASHA-001).

Validates engine/dasha against a reference built INDEPENDENTLY inside
this file with closed-form prefix sums (no recursive subdivision, the
production construction). No reference value is imported from
engine/dasha, engine/kp, or legacy/.

Run:  python validate_vimshottari_holdout.py
"""

import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from engine.dasha.vimshottari import vimshottari_from_moon  # SUBJECT

# ------------------------------------------------------------- reference
REF_LORDS = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter",
             "Saturn", "Mercury"]
REF_YEARS = {"Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
             "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17}
REF_ABBREV = {"Ketu": "Ke", "Venus": "Ve", "Sun": "Su", "Moon": "Mo",
              "Mars": "Ma", "Rahu": "Ra", "Jupiter": "Ju", "Saturn": "Sa",
              "Mercury": "Me"}
SPAN = Fraction(40, 3)


def to_exact(value):
    from decimal import Decimal
    if isinstance(value, Fraction):
        return value
    return Fraction(Decimal(str(value)))


def reference_timeline(moon, depth):
    """Closed-form: every period as (lords, start_years, end_years)."""
    exact = to_exact(moon) % 360
    nak = int(exact // SPAN)
    elapsed = (exact - nak * SPAN) / SPAN
    seed = REF_LORDS[nak % 9]
    seed_index = REF_LORDS.index(seed)

    def cycle(start_index):
        return [REF_LORDS[(start_index + k) % 9] for k in range(9)]

    periods = []
    md_start = Fraction(0)
    for md in cycle(seed_index):
        md_years = Fraction(REF_YEARS[md])
        periods.append(((REF_ABBREV[md],), md_start, md_start + md_years))
        if depth >= 2:
            ad_start = md_start
            for ad in cycle(REF_LORDS.index(md)):
                ad_years = md_years * REF_YEARS[ad] / 120
                periods.append(((REF_ABBREV[md], REF_ABBREV[ad]),
                                ad_start, ad_start + ad_years))
                if depth >= 3:
                    pd_start = ad_start
                    for pd in cycle(REF_LORDS.index(ad)):
                        pd_years = ad_years * REF_YEARS[pd] / 120
                        periods.append(
                            ((REF_ABBREV[md], REF_ABBREV[ad], REF_ABBREV[pd]),
                             pd_start, pd_start + pd_years))
                        pd_start += pd_years
                ad_start += ad_years
        md_start += md_years

    balance = Fraction(REF_YEARS[seed]) * (1 - elapsed)
    return nak + 1, REF_ABBREV[seed], elapsed, balance, periods


def compare(moon, depth=3):
    subject = vimshottari_from_moon(moon, 2451545.0, depth=depth)
    nak, seed, elapsed, balance, ref_periods = reference_timeline(moon, depth)
    problems = []
    if subject.seed_nakshatra_number != nak:
        problems.append("nakshatra")
    if subject.seed_lord != seed:
        problems.append("seed lord")
    if subject.seed_elapsed_fraction != elapsed:
        problems.append("elapsed fraction")
    if subject.balance_years != balance:
        problems.append("balance")
    ours = [(p.lords, p.start_years, p.end_years) for p in subject.periods]
    if len(ours) != len(ref_periods):
        problems.append(f"period count {len(ours)} != {len(ref_periods)}")
    else:
        for mine, reference in zip(sorted(ours), sorted(ref_periods)):
            if mine != reference:
                problems.append(f"period {reference[0]}")
                break
    return problems


def main() -> int:
    failures = []

    dense = 0
    for i in range(1000):
        moon = i * (360.0 / 1000) + 0.123456789
        problems = compare(moon % 360.0, depth=3)
        if problems:
            failures.append((moon, problems))
        dense += 1

    boundary = 0
    eps = Fraction(1, 10**9)
    for k in range(27):
        base = SPAN * k
        for moon in (base, base + eps, (base - eps) % 360):
            problems = compare(moon, depth=3)
            if problems:
                failures.append((float(moon), problems))
            boundary += 1

    print("=" * 60)
    print("INDEPENDENT VIMSHOTTARI HOLDOUT VALIDATION")
    print("=" * 60)
    print(f"Dense moon cases     : {dense} (819 periods each, exact)")
    print(f"Boundary moon cases  : {boundary}")
    if failures:
        print(f"FAILURES: {len(failures)}; first: {failures[:3]}")
        print("RESULT: FAIL")
        return 1
    print()
    print("RESULT: ALL INDEPENDENT VIMSHOTTARI CASES PASSED")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
