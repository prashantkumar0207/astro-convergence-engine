"""PARASHARI_HOUSE_LORD_V1 CERTIFICATION RUNNER (ADR-0133 I1, D3, D5; PROPOSED).

Certifies the production module engine/parashari/house_lord.py: for a natal D1 chart under PARASHARI_LAHIRI, each
house's whole-sign sign, its lord, the lord's sign and whole-sign house, and each of the nine grahas' sign and
whole-sign house. Every gate tests that real module directly, never a copy of its logic.

Regenerates certification/PARASHARI_HOUSE_LORD_V1_certification.json FROM SCRATCH on every run; the stored JSON is
never accepted as proof.

Gates:
  A table integrity: this file's own transcription of the seven classical lords, pinned by content hash, against the
    production table, and the production module's own content hash pinned.
  B logical enumeration: every Lagna sign x every house (144), house sign and lord against the closed form.
  B2 placement composition: synthetic snapshots through house_lords_from_snapshot(), every Lagna sign x every target
    sign, plus a spread pattern that separates each lord from every other graha.
  C external oracle: PyJHora's house-owner table (jhora.const.house_owners), and each lord's house rebuilt from it.
    PyJHora unavailable is a FAIL, never a skip.
  D independent validator: validate_parashari_house_lord_holdout.py, a separate-process reimplementation.
  E non-invasiveness and isolation.
  F boundary cases: Lagna and grahas at exact sign edges, and the 360/0 wrap.
  G static reference regression: LIVE production output on fixed synthetic charts against values frozen once from
    the independent validator.
  H negative controls: each planted corruption, in a copy, disagrees with production at a chosen case.
  I composition verification: the validator's field-by-field check and its monkeypatch mutation self-check against
    the real production module.
  J profile refusal: a non-Parashari, unprovenanced or wrong-ayanamsa snapshot is refused.

Exit code 0 = PASS, 3 = FAIL.
"""

import hashlib
import math
import subprocess
import sys
from dataclasses import replace
from datetime import date
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import certification_support as support  # noqa: E402

import engine.parashari.house_lord as production_module  # noqa: E402
from engine.astrology.house import equal_house_from_ascendant, whole_sign_house  # noqa: E402
from engine.astrology.sign_lord import SIGN_LORDS, sign_lord  # noqa: E402
from engine.astrology.signs import zodiac_sign  # noqa: E402
from engine.astronomy.profile import KP_KRISHNAMURTI, PARASHARI_LAHIRI  # noqa: E402
from engine.calculations.calculations import calculate  # noqa: E402
from engine.models.birth_data import BirthData  # noqa: E402
from engine.parashari.house_lord import (  # noqa: E402
    HOUSES,
    PLACED_GRAHAS,
    HouseLordProfileError,
    house_lord,
    house_lords,
    house_lords_from_snapshot,
    house_sign,
)

try:
    import importlib.metadata

    import jhora.const as jhora_const
    PYJHORA_VERSION = importlib.metadata.version("PyJHora")
except Exception as error:  # pragma: no cover
    print("PARASHARI_HOUSE_LORD_V1 CERTIFICATION FAIL: PyJHora oracle unavailable:", error)
    sys.exit(3)

#: Independently transcribed: sign (Aries = 1 ... Pisces = 12) -> its classical lord. Not imported from
#: engine/astrology/sign_lord.py, and structured differently from the validator's lord -> owned signs table.
CERTIFIED_SIGN_LORDS = {
    1: "Mars", 2: "Venus", 3: "Mercury", 4: "Moon", 5: "Sun", 6: "Mercury",
    7: "Venus", 8: "Mars", 9: "Jupiter", 10: "Saturn", 11: "Saturn", 12: "Jupiter",
}
#: PyJHora's planet indices, for reading its house-owner table.
PYJHORA_INDEX = {"Sun": 0, "Moon": 1, "Mars": 2, "Mercury": 3, "Jupiter": 4, "Venus": 5, "Saturn": 6}

#: Content fingerprint of this file's own frozen constants, pinned from an intentional run.
CERTIFIED_HOUSE_LORD_CONTENT_SHA256 = "58fbfa23227f35a90a83b2105b223a3e0260c6ed21dc41f7003af869a0e67850"
#: engine.parashari.house_lord.rule_content_sha256(), pinned from the real file once it existed.
CERTIFIED_PRODUCTION_CONTENT_SHA256 = "96bd191877e482d796b03c6a13bc08b84419d614b5922f5c5fda69fdc3f68465"

#: Fixed synthetic charts (not real people). Expected values frozen ONCE, offline, from
#: `python validate_parashari_house_lord_holdout.py --generate`, never from production at certification time.
HOLDOUT = [
    {"id": "HL1_lima_1911", "date": "1911-04-02", "time": "08:15:40", "lat": -12.0464, "lon": -77.0428,
     "expected": {"ascendant_sign": 11, "graha_signs": [12, 1, 10, 1, 7, 1, 1, 1, 7],
                  "graha_houses": [2, 3, 12, 3, 9, 3, 3, 3, 9],
                  "lords": ["Saturn", "Jupiter", "Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars",
                            "Jupiter", "Saturn"],
                  "lord_houses": [3, 9, 12, 3, 3, 3, 2, 3, 3, 12, 9, 3]}},
    {"id": "HL2_oslo_1938", "date": "1938-10-19", "time": "21:03:11", "lat": 59.9139, "lon": 10.7522,
     "expected": {"ascendant_sign": 4, "graha_signs": [7, 5, 6, 7, 10, 8, 12, 7, 1],
                  "graha_houses": [4, 2, 3, 4, 7, 5, 9, 4, 10],
                  "lords": ["Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter", "Mars",
                            "Venus", "Mercury"],
                  "lord_houses": [2, 4, 4, 5, 3, 7, 9, 9, 7, 3, 5, 4]}},
    {"id": "HL3_nairobi_1957", "date": "1957-01-27", "time": "02:44:05", "lat": -1.2921, "lon": 36.8219,
     "expected": {"ascendant_sign": 9, "graha_signs": [10, 9, 1, 9, 6, 9, 8, 8, 2],
                  "graha_houses": [2, 1, 5, 1, 10, 1, 12, 12, 6],
                  "lords": ["Jupiter", "Saturn", "Saturn", "Jupiter", "Mars", "Venus", "Mercury", "Moon", "Sun",
                            "Mercury", "Venus", "Mars"],
                  "lord_houses": [10, 12, 12, 10, 5, 1, 1, 1, 2, 1, 1, 5]}},
    {"id": "HL4_chennai_1983", "date": "1983-06-08", "time": "11:30:00", "lat": 13.0827, "lon": 80.2707,
     "expected": {"ascendant_sign": 8, "graha_signs": [2, 1, 2, 1, 8, 4, 7, 3, 9],
                  "graha_houses": [7, 6, 7, 6, 1, 9, 12, 8, 2],
                  "lords": ["Mars", "Jupiter", "Saturn", "Saturn", "Jupiter", "Mars", "Venus", "Mercury", "Moon", "Sun",
                            "Mercury", "Venus"],
                  "lord_houses": [7, 1, 12, 12, 1, 7, 9, 6, 6, 7, 6, 9]}},
    {"id": "HL5_toronto_1996", "date": "1996-12-14", "time": "16:52:27", "lat": 43.6532, "lon": -79.3832,
     "expected": {"ascendant_sign": 11, "graha_signs": [8, 10, 5, 9, 9, 8, 12, 6, 12],
                  "graha_houses": [10, 12, 7, 11, 11, 10, 2, 8, 2],
                  "lords": ["Saturn", "Jupiter", "Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars",
                            "Jupiter", "Saturn"],
                  "lord_houses": [2, 11, 7, 10, 11, 12, 10, 11, 10, 7, 11, 2]}},
    {"id": "HL6_seoul_2008", "date": "2008-03-21", "time": "05:05:55", "lat": 37.5665, "lon": 126.9780,
     "expected": {"ascendant_sign": 4, "graha_signs": [12, 6, 3, 11, 9, 11, 5, 11, 5],
                  "graha_houses": [9, 3, 12, 8, 6, 8, 2, 8, 2],
                  "lords": ["Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter", "Mars",
                            "Venus", "Mercury"],
                  "lord_houses": [3, 9, 8, 8, 12, 6, 2, 2, 6, 12, 8, 8]}},
    {"id": "HL7_lagos_2019", "date": "2019-08-30", "time": "19:47:13", "lat": 6.5244, "lon": 3.3792,
     "expected": {"ascendant_sign": 12, "graha_signs": [5, 5, 5, 5, 8, 5, 9, 3, 9],
                  "graha_houses": [6, 6, 6, 6, 9, 6, 10, 4, 10],
                  "lords": ["Jupiter", "Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter",
                            "Saturn", "Saturn"],
                  "lord_houses": [9, 6, 6, 6, 6, 6, 6, 6, 6, 9, 10, 10]}},
    {"id": "HL8_reykjavik_2041", "date": "2041-02-11", "time": "13:13:13", "lat": 64.1466, "lon": -21.9426,
     "expected": {"ascendant_sign": 3, "graha_signs": [10, 3, 10, 10, 7, 12, 6, 1, 7],
                  "graha_houses": [8, 1, 8, 8, 5, 10, 4, 11, 5],
                  "lords": ["Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn",
                            "Jupiter", "Mars", "Venus"],
                  "lord_houses": [8, 1, 8, 8, 10, 8, 5, 4, 4, 5, 8, 10]}},
]


def fail(message):
    print("PARASHARI_HOUSE_LORD_V1 CERTIFICATION FAIL:", message)
    sys.exit(3)


def rule_content_sha256() -> str:
    payload = repr((sorted(CERTIFIED_SIGN_LORDS.items()), sorted(PYJHORA_INDEX.items()))).encode()
    return hashlib.sha256(payload).hexdigest()


def _birth_data(case) -> BirthData:
    year, month, day = (int(x) for x in case["date"].split("-"))
    hour, minute, second = (int(x) for x in case["time"].split(":"))
    return BirthData(year, month, day, hour, minute, float(second), case["lat"], case["lon"], "UTC")


def _real_provenance():
    return calculate(_birth_data(HOLDOUT[0]), profile=PARASHARI_LAHIRI).snapshot.provenance


def _snapshot(longitudes: dict, ascendant: float, provenance):
    """A synthetic snapshot carrying exactly what house_lords_from_snapshot() reads."""

    return SimpleNamespace(provenance=provenance, houses=SimpleNamespace(ascendant=ascendant),
                           sidereal_planets={graha: SimpleNamespace(longitude=longitudes[graha])
                                             for graha in PLACED_GRAHAS})


def _closed_form(longitudes: dict, ascendant: float) -> dict:
    """The facts, from this file's own table and modular arithmetic, for checking production against."""

    asc_sign = int(ascendant % 360.0 // 30.0) + 1
    signs = {graha: int(longitudes[graha] % 360.0 // 30.0) + 1 for graha in PLACED_GRAHAS}
    houses = {graha: (signs[graha] - asc_sign) % 12 + 1 for graha in PLACED_GRAHAS}
    lordships = []
    for house in HOUSES:
        sign = (asc_sign + house - 2) % 12 + 1
        lord = CERTIFIED_SIGN_LORDS[sign]
        lordships.append((house, sign, lord, signs[lord], houses[lord]))
    return {"ascendant_sign": asc_sign, "signs": signs, "houses": houses, "lordships": lordships}


def _disagreements(chart, expected) -> list:
    found = []
    if chart.ascendant_sign != expected["ascendant_sign"]:
        found.append("ascendant_sign")
    for graha in PLACED_GRAHAS:
        placed = chart.placement(graha)
        if (placed.sign, placed.house) != (expected["signs"][graha], expected["houses"][graha]):
            found.append(graha)
    for got, want in zip(chart.lordships, expected["lordships"]):
        if (got.house, got.sign, got.lord, got.lord_sign, got.lord_house) != want:
            found.append(f"house {want[0]}")
    return found


# --------------------------------------------------------------- Gates

def gate_a_table_integrity():
    mismatches = [sign for sign in range(1, 13)
                  if SIGN_LORDS[sign] != CERTIFIED_SIGN_LORDS[sign] or sign_lord(sign) != CERTIFIED_SIGN_LORDS[sign]]
    if mismatches:
        fail(f"production sign_lord disagrees with the independently transcribed table at signs {mismatches}")
    if sorted(set(CERTIFIED_SIGN_LORDS.values())) != sorted(PYJHORA_INDEX):
        fail("the transcribed table does not name exactly the seven classical lords")
    if rule_content_sha256() != CERTIFIED_HOUSE_LORD_CONTENT_SHA256:
        fail("certifier content hash does not match the pinned value")
    if production_module.rule_content_sha256() != CERTIFIED_PRODUCTION_CONTENT_SHA256:
        fail("engine.parashari.house_lord content hash does not match the pinned value")
    return {"signs_checked": 12, "mismatches": 0, "content_sha256": rule_content_sha256(),
            "production_content_sha256": production_module.rule_content_sha256(),
            "classification": "correctness_evidence",
            "disclosure": "the transcription is implementation-independent of engine/astrology/sign_lord.py (typed "
                          "separately, never imported); it is not source-independent, since both follow the same "
                          "classical lordship. Gate C adds PyJHora's table as an external reference."}


def gate_b_logical_enumeration():
    cases = mismatches = 0
    for asc_sign in range(1, 13):
        for house in HOUSES:
            want_sign = (asc_sign + house - 2) % 12 + 1
            cases += 1
            if house_sign(house, asc_sign) != want_sign or house_lord(house, asc_sign) != CERTIFIED_SIGN_LORDS[want_sign]:
                mismatches += 1
    if cases != 144 or mismatches:
        fail(f"logical enumeration: {mismatches}/{cases} mismatches")
    return {"cases": cases, "mismatches": 0, "space": "12 Lagna signs x 12 houses = 144",
            "classification": "correctness_evidence"}


def gate_b2_placement_composition():
    provenance = _real_provenance()
    cases = mismatches = 0
    for asc_sign in range(1, 13):
        ascendant = (asc_sign - 1) * 30.0 + 7.5
        for target in range(1, 13):
            same = {graha: (target - 1) * 30.0 + 15.0 for graha in PLACED_GRAHAS}
            spread = {graha: ((target - 1 + index * 5) % 12) * 30.0 + 22.25 for index, graha in enumerate(PLACED_GRAHAS)}
            for longitudes in (same, spread):
                cases += 1
                if _disagreements(house_lords_from_snapshot(_snapshot(longitudes, ascendant, provenance)),
                                  _closed_form(longitudes, ascendant)):
                    mismatches += 1
    if mismatches:
        fail(f"placement composition: {mismatches}/{cases} snapshots disagree with the closed form")
    return {"cases": cases, "mismatches": 0,
            "space": "12 Lagna signs x 12 target signs x 2 patterns (all grahas together; grahas spread five signs apart)",
            "classification": "correctness_evidence",
            "disclosure": "the spread pattern places every graha in a different sign, so a lord's house cannot be "
                          "confused with another graha's"}


def gate_c_oracle():
    owners = list(jhora_const.house_owners)
    if len(owners) != 12:
        fail(f"PyJHora's house_owners has {len(owners)} entries, not 12")
    by_index = {index: name for name, index in PYJHORA_INDEX.items()}
    mismatches = [sign for sign in range(1, 13) if by_index.get(owners[sign - 1]) != sign_lord(sign)]
    if mismatches:
        fail(f"production sign_lord disagrees with PyJHora house_owners at signs {mismatches}")
    rebuilt = 0
    for case in HOLDOUT:
        chart = house_lords(_birth_data(case))
        for item in chart.lordships:
            oracle_lord = by_index[owners[item.sign - 1]]
            if oracle_lord != item.lord or chart.placement(oracle_lord).house != item.lord_house:
                fail(f"{case['id']} house {item.house}: the lord rebuilt from PyJHora's table disagrees")
            rebuilt += 1
    return {"package": "PyJHora", "version": PYJHORA_VERSION, "table": "jhora.const.house_owners",
            "signs_checked": 12, "lordships_rebuilt": rebuilt, "mismatches": 0,
            "classification": "external_reference",
            "disclosure": "a table-level oracle: PyJHora's lordship table, with each lord's house rebuilt from this "
                          "project's own certified placements. PyJHora does not compute the charts here, so the "
                          "astronomical substrate is not re-checked by this gate (it is Tier-0 certified)."}


def gate_d_independent_validator():
    result = subprocess.run([sys.executable, str(ROOT / "validate_parashari_house_lord_holdout.py")],
                            capture_output=True, text=True)
    if result.returncode != 0 or "ALL INDEPENDENT PARASHARI_HOUSE_LORD_V1 CASES PASSED" not in result.stdout:
        fail(f"independent validator failed: {result.stdout[-1200:]} {result.stderr[-800:]}")
    return {"result": "PASS", "classification": "corroborating_correctness_evidence",
            "note": "separate-process reimplementation; derives sign, house and lordship itself, importing no "
                    "engine.astrology module and not engine.parashari.house_lord for its own derivation"}


def gate_e_non_invasiveness():
    path = Path(production_module.__file__)
    for line_no, line in enumerate(path.read_text().splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith(("import ", "from ")) and any(
                name in stripped for name in ("drishti", "engine.kp", "jaimini", "nadi", "mahapurusha", "evidence",
                                              "interpretation")):
            fail(f"{path.name}:{line_no} imports another school's or layer's module: {stripped}")
    if production_module.whole_sign_house is not whole_sign_house or production_module.sign_lord is not sign_lord or \
            production_module.zodiac_sign is not zodiac_sign:
        fail("the production module does not use the shared production functions")
    if production_module.rule_content_sha256() != CERTIFIED_PRODUCTION_CONTENT_SHA256:
        fail("engine.parashari.house_lord content hash does not match the pinned value")
    return {"production_module": "engine/parashari/house_lord.py", "isolated": True,
            "shared_functions": ["engine.astrology.house.whole_sign_house", "engine.astrology.sign_lord.sign_lord",
                                 "engine.astrology.signs.zodiac_sign"]}


def gate_f_boundary_cases():
    provenance = _real_provenance()
    cases = mismatches = 0
    for asc_sign in range(1, 13):
        ascendant = (asc_sign - 1) * 30.0  # the exact lower edge belongs to the sign
        for target in range(1, 13):
            longitudes = {graha: (target - 1) * 30.0 for graha in PLACED_GRAHAS}
            chart = house_lords_from_snapshot(_snapshot(longitudes, ascendant, provenance))
            cases += 1
            want = (target - asc_sign) % 12 + 1
            if chart.ascendant_sign != asc_sign or any(item.lord_house != want for item in chart.lordships):
                mismatches += 1
    # The 360/0 wrap: just below 360 is Pisces (no promotion across the wrap), exactly 0 is Aries.
    near_wrap = math.nextafter(360.0, -math.inf)
    for longitude, sign in ((near_wrap, 12), (0.0, 1)):
        chart = house_lords_from_snapshot(_snapshot({graha: longitude for graha in PLACED_GRAHAS}, 0.0, provenance))
        cases += 1
        if chart.placement("Jupiter").sign != sign:
            mismatches += 1
    if mismatches:
        fail(f"boundary cases: {mismatches}/{cases}")
    return {"cases": cases, "mismatches": 0,
            "convention": "exact lower sign edges belong to the sign; the 360/0 wrap is not promoted; inherited from "
                          "engine.astrology.signs.zodiac_sign, which SIGN_CONVENTION_V1 certifies"}


def gate_g_static_reference_regression():
    cases = 0
    for case in HOLDOUT:
        chart = house_lords(_birth_data(case))
        want = case["expected"]
        got = {"ascendant_sign": chart.ascendant_sign,
               "graha_signs": [chart.placement(graha).sign for graha in PLACED_GRAHAS],
               "graha_houses": [chart.placement(graha).house for graha in PLACED_GRAHAS],
               "lords": [chart.lordship(house).lord for house in HOUSES],
               "lord_houses": [chart.lordship(house).lord_house for house in HOUSES]}
        if got != want:
            fail(f"static reference mismatch on {case['id']}: production={got} expected(static)={want}")
        cases += 1
    return {"charts": cases, "mismatches": 0, "facts_per_chart": 1 + 9 + 9 + 12 + 12,
            "methodology": "LIVE production house_lords() on fixed synthetic charts, against STATIC values frozen once "
                           "from the independent validator's own derivation",
            "classification": "correctness_evidence"}


def gate_h_negative_controls():
    case = HOLDOUT[0]
    snapshot = calculate(_birth_data(case), profile=PARASHARI_LAHIRI).snapshot
    real = house_lords_from_snapshot(snapshot)
    ascendant = snapshot.houses.ascendant
    lon = {graha: snapshot.sidereal_planets[graha].longitude for graha in PLACED_GRAHAS}

    def facts(lord_for, sign_for_house, house_for):
        return [(h, sign_for_house(h), lord_for(sign_for_house(h)), house_for(lord_for(sign_for_house(h))))
                for h in HOUSES]

    asc_sign = zodiac_sign(ascendant)
    truth = [(item.house, item.sign, item.lord, item.lord_house) for item in real.lordships]
    planted = {
        "Scorpio's lord replaced by Ketu": facts(
            lambda s: "Ketu" if s == 8 else CERTIFIED_SIGN_LORDS[s], lambda h: house_sign(h, asc_sign),
            lambda g: whole_sign_house(lon[g], ascendant)),
        "houses counted backwards from the Lagna": facts(
            lambda s: CERTIFIED_SIGN_LORDS[s], lambda h: (asc_sign - h) % 12 + 1,
            lambda g: whole_sign_house(lon[g], ascendant)),
        "house signs off by one": facts(
            lambda s: CERTIFIED_SIGN_LORDS[s], lambda h: house_sign(h, asc_sign) % 12 + 1,
            lambda g: whole_sign_house(lon[g], ascendant)),
        "lord's house by equal houses from the Lagna degree": facts(
            lambda s: CERTIFIED_SIGN_LORDS[s], lambda h: house_sign(h, asc_sign),
            lambda g: equal_house_from_ascendant(lon[g], ascendant)),
        "lord's house taken as the house it rules": facts(
            lambda s: CERTIFIED_SIGN_LORDS[s], lambda h: house_sign(h, asc_sign),
            lambda g: next(h for h in HOUSES if CERTIFIED_SIGN_LORDS[house_sign(h, asc_sign)] == g)),
    }
    controls = []
    for label, corrupted in planted.items():
        detected = corrupted != truth
        controls.append({"control": label, "case": case["id"], "detected": detected})
        if not detected:
            fail(f"negative control not detected: {label}")
    if rule_content_sha256() != CERTIFIED_HOUSE_LORD_CONTENT_SHA256 or \
            production_module.rule_content_sha256() != CERTIFIED_PRODUCTION_CONTENT_SHA256:
        fail("frozen constants were changed by the negative controls")
    return {"controls": controls, "all_detected": True, "classification": "negative_control"}


def gate_i_composition_verification():
    result = subprocess.run([sys.executable, str(ROOT / "validate_parashari_house_lord_holdout.py")],
                            capture_output=True, text=True)
    if (result.returncode != 0
            or "PARASHARI_HOUSE_LORD_V1 COMPOSITION VERIFICATION PASSED" not in result.stdout
            or "PARASHARI_HOUSE_LORD_V1 COMPOSITION MUTATION DETECTION PASSED" not in result.stdout):
        fail(f"composition verification failed: {result.stdout[-1600:]} {result.stderr[-800:]}")
    return {"result": "PASS", "classification": "correctness_evidence_and_mutation_detection",
            "scope": "house_lords_from_snapshot() field by field on the validator's 8 synthetic charts, and a monkeypatch "
                     "self-check: whole_sign_house arguments swapped, Scorpio given to Ketu, Aquarius given to Rahu, "
                     "zodiac_sign off by one; each caught, and the module restored"}


def gate_j_profile_refusal():
    real = calculate(_birth_data(HOLDOUT[0]), profile=PARASHARI_LAHIRI).snapshot
    kp = calculate(_birth_data(HOLDOUT[0]), profile=KP_KRISHNAMURTI).snapshot
    unprovenanced = SimpleNamespace(provenance=None, houses=real.houses, sidereal_planets=real.sidereal_planets)
    wrong_ayanamsa = SimpleNamespace(provenance=replace(real.provenance, ayanamsa_mode=real.provenance.ayanamsa_mode + 1),
                                     houses=real.houses, sidereal_planets=real.sidereal_planets)
    refused = []
    for label, snapshot in (("a KP snapshot", kp), ("a snapshot with no provenance", unprovenanced),
                            ("a Parashari-named snapshot with another ayanamsa", wrong_ayanamsa)):
        try:
            house_lords_from_snapshot(snapshot)
        except HouseLordProfileError:
            refused.append(label)
            continue
        fail(f"not refused: {label}")
    house_lords_from_snapshot(real)
    return {"refused": refused, "preserved": ["the PARASHARI_LAHIRI snapshot"], "classification": "negative_control"}


def main():
    tee = support.start_transcript()
    preconditions = support.preflight()
    report = {
        "schema": "parashari_house_lord_v1_certification",
        "adr": "ADR-0133 (PROPOSED)",
        "date": str(date.today()),
        "scope": ("PARASHARI_HOUSE_LORD_V1: for a natal D1 chart under the PARASHARI_LAHIRI profile, each house's "
                  "whole-sign sign, its classical lord, the lord's sign and whole-sign house, and each of the nine grahas' "
                  "sign and whole-sign house. The module under certification is engine/parashari/house_lord.py."),
        "rule": {"kind": "engine/parashari/house_lord.py - production module",
                 "convention": "whole-sign houses from the D1 Lagna (ADR-0133 D3), the seven classical sign lords",
                 "certifier_content_sha256": rule_content_sha256(),
                 "production_content_sha256": production_module.rule_content_sha256()},
        "oracle": {"package": "PyJHora", "version": PYJHORA_VERSION, "use": "the house-owner table (gate C)"},
        "gates": {
            "A_table_integrity": gate_a_table_integrity(),
            "B_logical_enumeration": gate_b_logical_enumeration(),
            "B2_placement_composition": gate_b2_placement_composition(),
            "C_oracle": gate_c_oracle(),
            "D_independent_validator": gate_d_independent_validator(),
            "E_non_invasiveness": gate_e_non_invasiveness(),
            "F_boundary_cases": gate_f_boundary_cases(),
            "G_static_reference_regression": gate_g_static_reference_regression(),
            "H_negative_controls": gate_h_negative_controls(),
            "I_composition_verification": gate_i_composition_verification(),
            "J_profile_refusal": gate_j_profile_refusal(),
        },
        "explicit_non_claims": [
            "certified support, not a production analytical input: no ratified entry serves it (ADR-0133 D5, PROPOSED)",
            "the seven classical lords only: no Rahu or Ketu co-lordship of Scorpio or Aquarius",
            "whole-sign houses only: no bhava-chalit, equal-house or cusp-based house",
            "D1 only: no varga",
            "no strength, dignity, aspect, yoga or dasha",
            "no interpretive or predictive claim: a house lord's placement is a calculated fact, never an indication",
            "every chart used is synthetic; no real person's chart is certified",
            "PyJHora is a table-level reference only; it computes no chart here",
        ],
        "environment": {"python": sys.version.split()[0]},
        "preconditions": preconditions,
        "result": "PASS",
    }
    out = support.emit(report, "PARASHARI_HOUSE_LORD_V1_certification.json", "parashari_house_lord", tee)
    print("=" * 60)
    print("PARASHARI_HOUSE_LORD_V1 CERTIFICATION (production module engine/parashari/house_lord.py)")
    print("=" * 60)
    for name, gate in report["gates"].items():
        print(f"{name}: {gate}")
    print("archived          :", out.relative_to(ROOT).as_posix())
    print("RESULT            : PASS")


if __name__ == "__main__":
    main()
