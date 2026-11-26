"""Independent PARASHARI_HOUSE_LORD_V1 validator (ADR-0133 I1; PROPOSED).

A from-scratch reimplementation of the house-lord and placement facts: sign of a longitude, the whole-sign house
from the Lagna, each house's sign, its lord, and the lord's placement. It is written independently of
scripts/certify_parashari_house_lord.py, and nothing is imported from that file.

It does NOT import engine.astrology.house, engine.astrology.signs, engine.astrology.sign_lord or
engine.parashari.house_lord for its own derivation. The lordship table below is a separate hand transcription,
structured as lord -> the signs it owns (the production table and the certifier's map sign -> lord), so the same
slip is unlikely in both.

Only the Tier-0-Locked D1 kernel (engine.calculations.calculations.calculate under PARASHARI_LAHIRI) is shared: the
certified astronomical substrate, not the logic under test. The production module is imported only by the
composition check and the mutation self-check, which compare it against this file's own derivation.

Run:  python validate_parashari_house_lord_holdout.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from engine.astronomy.profile import PARASHARI_LAHIRI  # noqa: E402  (certified substrate)
from engine.calculations.calculations import calculate  # noqa: E402  (certified substrate)
from engine.models.birth_data import BirthData  # noqa: E402

GRAHAS = ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu")

#: The seven classical lords and the signs each owns (Aries = 1 ... Pisces = 12), re-typed by hand.
OWNED_SIGNS = {
    "Sun": (5,),
    "Moon": (4,),
    "Mars": (1, 8),
    "Mercury": (3, 6),
    "Jupiter": (9, 12),
    "Venus": (2, 7),
    "Saturn": (10, 11),
}

#: Synthetic birth instants (not real people). Disjoint from every other certifier's cases.
CASES = (
    {"id": "HL1_lima_1911", "date": "1911-04-02", "time": "08:15:40", "lat": -12.0464, "lon": -77.0428},
    {"id": "HL2_oslo_1938", "date": "1938-10-19", "time": "21:03:11", "lat": 59.9139, "lon": 10.7522},
    {"id": "HL3_nairobi_1957", "date": "1957-01-27", "time": "02:44:05", "lat": -1.2921, "lon": 36.8219},
    {"id": "HL4_chennai_1983", "date": "1983-06-08", "time": "11:30:00", "lat": 13.0827, "lon": 80.2707},
    {"id": "HL5_toronto_1996", "date": "1996-12-14", "time": "16:52:27", "lat": 43.6532, "lon": -79.3832},
    {"id": "HL6_seoul_2008", "date": "2008-03-21", "time": "05:05:55", "lat": 37.5665, "lon": 126.9780},
    {"id": "HL7_lagos_2019", "date": "2019-08-30", "time": "19:47:13", "lat": 6.5244, "lon": 3.3792},
    {"id": "HL8_reykjavik_2041", "date": "2041-02-11", "time": "13:13:13", "lat": 64.1466, "lon": -21.9426},
)


def lord_of_sign(sign):
    owners = [lord for lord, signs in OWNED_SIGNS.items() if sign in signs]
    if len(owners) != 1:
        raise AssertionError(f"sign {sign} has {len(owners)} owners in the validator's table")
    return owners[0]


def sign_of(longitude):
    """Sign 1-12 by plain floor division. The fixed cases are far from any sign edge, so the production
    boundary tolerance (engine.astrology.longitude_utils) never decides one of them."""

    return int((longitude % 360.0) // 30.0) + 1


def house_counted(sign, ascendant_sign):
    """Whole-sign house, by counting signs forward from the Lagna's sign, one at a time."""

    count, current = 1, ascendant_sign
    while current != sign:
        current = current % 12 + 1
        count += 1
    return count


def sign_of_house(house, ascendant_sign):
    current = ascendant_sign
    for _ in range(house - 1):
        current = current % 12 + 1
    return current


def derive(longitudes, ascendant_longitude):
    """Every fact the capability reports, derived independently from raw longitudes."""

    asc_sign = sign_of(ascendant_longitude)
    signs = {graha: sign_of(longitudes[graha]) for graha in GRAHAS}
    houses = {graha: house_counted(signs[graha], asc_sign) for graha in GRAHAS}
    lordships = []
    for house in range(1, 13):
        sign = sign_of_house(house, asc_sign)
        lord = lord_of_sign(sign)
        lordships.append((house, sign, lord, signs[lord], houses[lord]))
    return {"ascendant_sign": asc_sign, "signs": signs, "houses": houses, "lordships": tuple(lordships)}


def _birth_data(case):
    year, month, day = (int(x) for x in case["date"].split("-"))
    hour, minute, second = (int(x) for x in case["time"].split(":"))
    return BirthData(year, month, day, hour, minute, float(second), case["lat"], case["lon"], "UTC")


def _raw(case):
    snapshot = calculate(_birth_data(case), profile=PARASHARI_LAHIRI).snapshot
    return {graha: snapshot.sidereal_planets[graha].longitude for graha in GRAHAS}, snapshot.houses.ascendant, snapshot


def structural_checks():
    """The table and the counting must be self-consistent before any chart is judged."""

    failures = []
    owned = sorted(sign for signs in OWNED_SIGNS.values() for sign in signs)
    if owned != list(range(1, 13)):
        failures.append("the lordship table does not assign every sign exactly once")
    for asc in range(1, 13):
        for house in range(1, 13):
            sign = sign_of_house(house, asc)
            if house_counted(sign, asc) != house:
                failures.append(f"counting is not invertible at Lagna {asc}, house {house}")
            if sign != (asc + house - 2) % 12 + 1:
                failures.append(f"forward counting disagrees with modular counting at Lagna {asc}, house {house}")
    return failures


def frozen_expected(derived):
    """The compact form the certifier's static regression freezes."""

    return {"ascendant_sign": derived["ascendant_sign"],
            "graha_signs": [derived["signs"][graha] for graha in GRAHAS],
            "graha_houses": [derived["houses"][graha] for graha in GRAHAS],
            "lords": [item[2] for item in derived["lordships"]],
            "lord_houses": [item[4] for item in derived["lordships"]]}


def generate_static_expected():
    """Printed once, offline, to freeze the certifier's static reference values."""

    for case in CASES:
        longitudes, ascendant, _snapshot = _raw(case)
        print(case["id"], frozen_expected(derive(longitudes, ascendant)))


def verify_composition():
    """The production module's facts, field by field, against this file's own derivation."""

    import engine.parashari.house_lord as production

    mismatches = []
    for case in CASES:
        longitudes, ascendant, snapshot = _raw(case)
        expected = derive(longitudes, ascendant)
        chart = production.house_lords_from_snapshot(snapshot)
        if chart.ascendant_sign != expected["ascendant_sign"]:
            mismatches.append((case["id"], "ascendant_sign"))
        for graha in GRAHAS:
            placed = chart.placement(graha)
            if (placed.sign, placed.house) != (expected["signs"][graha], expected["houses"][graha]):
                mismatches.append((case["id"], graha))
        for got, want in zip(chart.lordships, expected["lordships"]):
            if (got.house, got.sign, got.lord, got.lord_sign, got.lord_house) != want:
                mismatches.append((case["id"], f"house {want[0]}"))
        if len(chart.lordships) != 12 or len(chart.placements) != len(GRAHAS):
            mismatches.append((case["id"], "shape"))
    return mismatches


def run_mutation_self_check():
    """Each planted corruption of the real production module must be caught by verify_composition(), and the
    module must be restored afterwards."""

    import engine.parashari.house_lord as production

    original_house, original_lord, original_sign = production.whole_sign_house, production.sign_lord, production.zodiac_sign
    corruptions = {
        "whole_sign_house argument order swapped": ("whole_sign_house", lambda lon, asc: original_house(asc, lon)),
        "sign_lord with Scorpio given to Ketu": ("sign_lord", lambda sign: "Ketu" if sign == 8 else original_lord(sign)),
        "sign_lord with Aquarius given to Rahu": ("sign_lord", lambda sign: "Rahu" if sign == 11 else original_lord(sign)),
        "zodiac_sign off by one sign": ("zodiac_sign", lambda lon: original_sign(lon) % 12 + 1),
    }
    results = {}
    for label, (name, replacement) in corruptions.items():
        setattr(production, name, replacement)
        try:
            try:
                caught = bool(verify_composition())
            except (KeyError, AssertionError):
                caught = True
        finally:
            production.whole_sign_house, production.sign_lord, production.zodiac_sign = (
                original_house, original_lord, original_sign)
        results[label] = caught
    restored = not verify_composition()
    return results, restored


def main():
    print("=" * 60)
    print("INDEPENDENT PARASHARI_HOUSE_LORD_V1 VALIDATION")
    print("=" * 60)
    failures = structural_checks()
    for case in CASES:
        longitudes, ascendant, _snapshot = _raw(case)
        derived = derive(longitudes, ascendant)
        near_edge = [graha for graha in GRAHAS if min(longitudes[graha] % 30.0, 30.0 - longitudes[graha] % 30.0) < 1e-6]
        if min(ascendant % 30.0, 30.0 - ascendant % 30.0) < 1e-6 or near_edge:
            failures.append(f"{case['id']} lies within 1e-6 degree of a sign edge; floor division could disagree")
        print(f"{case['id']}: Lagna sign {derived['ascendant_sign']}, lord houses "
              f"{[item[4] for item in derived['lordships']]}")
    if failures:
        for item in failures:
            print("FAIL:", item)
        print("RESULT: FAIL")
        sys.exit(1)
    print("RESULT: ALL INDEPENDENT PARASHARI_HOUSE_LORD_V1 CASES PASSED")

    print("=" * 60)
    print("PARASHARI_HOUSE_LORD_V1 COMPOSITION VERIFICATION")
    print("=" * 60)
    mismatches = verify_composition()
    if mismatches:
        print("mismatches:", mismatches[:10])
        print("RESULT: PARASHARI_HOUSE_LORD_V1 COMPOSITION VERIFICATION FAILED")
        sys.exit(1)
    print("RESULT: PARASHARI_HOUSE_LORD_V1 COMPOSITION VERIFICATION PASSED")

    print("=" * 60)
    print("PARASHARI_HOUSE_LORD_V1 COMPOSITION MUTATION SELF-CHECK")
    print("=" * 60)
    results, restored = run_mutation_self_check()
    for label, caught in results.items():
        print(f"{'caught  ' if caught else 'MISSED  '} {label}")
    if not all(results.values()) or not restored:
        print("RESULT: PARASHARI_HOUSE_LORD_V1 COMPOSITION MUTATION DETECTION FAILED")
        sys.exit(1)
    print("RESULT: PARASHARI_HOUSE_LORD_V1 COMPOSITION MUTATION DETECTION PASSED")


if __name__ == "__main__":
    if sys.argv[1:] == ["--generate"]:
        generate_static_expected()
    else:
        main()
