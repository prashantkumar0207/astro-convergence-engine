"""SIGN_CONVENTION_V1 CERTIFICATION RUNNER (ADR-0012).

Regenerates certification/SIGN_CONVENTION_V1_certification.json FROM
SCRATCH on every run; the stored JSON is never accepted as proof.

Gates:
  A  NON-INVASIVENESS, weighted highest: SHA-256 over dense plus
     ULP-adversarial output sweeps of the certified D9 and D10
     modules and of all five registry vargas, for cross-commit
     comparison against published main.
  B  Sign type exhaustive correctness.
  C  DECLARATION PROOF by discriminating witness: for every declared
     sign index field, observed values must lie inside its declared
     range AND include the value that is IMPOSSIBLE under the other
     convention (0 proves zero-based, 12 proves one-based). That pair
     of conditions is necessary and sufficient, so the gate proves
     each declaration rather than merely sampling it; a field whose
     witness never appears fails as NOT PROVEN. Coverage breadth is
     recorded as data, never used to weaken the proof.
  D  Cross-layer agreement between the two certified conventions.

The declaration registry itself is recorded in the artifact, so a
future reader sees the project's conventions as evidence rather than
prose. Exit 0 = PASS, 3 = FAIL.
"""

import dataclasses
import hashlib
import json
import math
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

sys.path.insert(0, str(ROOT / "scripts"))
import certification_support as support  # noqa: E402

from engine.astrology.chart_factory import build_master_chart  # noqa: E402
from engine.astrology.dashamsa_chart import (  # noqa: E402
    dashamsa_chart, dashamsa_longitude, dashamsa_sign,
)
from engine.astrology.divisional_chart import divisional_chart  # noqa: E402
from engine.astrology.navamsa_chart import (  # noqa: E402
    navamsa_chart, navamsa_longitude, navamsa_sign,
)
from engine.astrology.sign import SIGN_COUNT, Sign, SignConventionError  # noqa: E402
from engine.astrology.sign_conventions import (  # noqa: E402
    ONE_BASED, SIGN_FIELD_CONVENTIONS, SIGN_FUNCTION_CONVENTIONS,
    ZERO_BASED, declared, is_index,
)
from engine.astrology.sign_names import SIGN_NAMES  # noqa: E402
from engine.astrology.signs import zodiac_sign  # noqa: E402
from engine.astrology.varga_classifier import classify  # noqa: E402
from engine.astrology.varga_registry import get_varga_rule, registered_vargas  # noqa: E402
from engine.calculations.calculations import calculate  # noqa: E402
from engine.kp.chain import kp_chain  # noqa: E402
from engine.kp.chart import kp_chart  # noqa: E402
from engine.models.birth_data import BirthData  # noqa: E402
from engine.parashari.drishti import aspected_signs, parashari_drishti  # noqa: E402


def fail(message):
    print("SIGN CONVENTION CERTIFICATION FAIL:", message)
    sys.exit(3)


def _sweep_points():
    step = 360.0 / 51429
    points = [i * step for i in range(51429)]
    for k in range(0, 121):
        for base in (k * (10.0 / 3.0), k * 3.0, k * 2.5, k * (30.0 / 7.0), k * 10.0):
            if not (0.0 <= base < 360.0):
                continue
            points.append(base)
            down = up = base
            for _ in range(3):
                down = math.nextafter(down, -math.inf)
                up = math.nextafter(up, math.inf)
                points.extend(p for p in (down, up) if 0.0 <= p < 360.0)
    return points


def gate_a_non_invasiveness():
    points = _sweep_points()
    d9 = hashlib.sha256()
    d10 = hashlib.sha256()
    for longitude in points:
        d9.update(repr((navamsa_sign(longitude), navamsa_longitude(longitude))).encode())
        d10.update(repr((dashamsa_sign(longitude), dashamsa_longitude(longitude))).encode())

    registry_hashes = {}
    for division, school in registered_vargas():
        rule = get_varga_rule(division, school)
        digest = hashlib.sha256()
        for longitude in points:
            result = classify(longitude, rule)
            digest.update(repr((result.d_sign, result.division_index, result.fraction)).encode())
        registry_hashes[f"D{division}_{school}"] = digest.hexdigest()

    return {
        "sweep_points": len(points),
        "d9_sweep_sha256": d9.hexdigest(),
        "d10_sweep_sha256": d10.hexdigest(),
        "registry_varga_sweep_sha256": registry_hashes,
        "note": ("compare against published main; this phase must change no "
                 "certified value (Decision SC-B)"),
    }


def gate_b_sign_type():
    for index in range(SIGN_COUNT):
        sign = Sign.from_zero_based(index)
        if sign.one_based != index + 1 or sign.name != SIGN_NAMES[index + 1]:
            fail(f"sign {index} accessors")
        if Sign.from_one_based(index + 1) != sign:
            fail(f"sign {index} round trip")
    for bad in (-1, 12, "3", 3.0, None, True):
        try:
            Sign.from_zero_based(bad)
            fail(f"accepted bad zero-based input {bad!r}")
        except SignConventionError:
            pass
    for attribute in ("__int__", "__index__", "__add__", "__sub__"):
        if hasattr(Sign.from_zero_based(0), attribute):
            fail(f"Sign exposes {attribute}; it must stay inert")
    return {"signs": SIGN_COUNT, "mismatches": 0, "inert": True}


def _walk(roots):
    seen, found, stack = set(), [], list(roots)
    while stack:
        obj = stack.pop()
        if id(obj) in seen:
            continue
        seen.add(id(obj))
        if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
            found.append(obj)
            for field in dataclasses.fields(obj):
                stack.append(getattr(obj, field.name))
        elif isinstance(obj, dict):
            stack.extend(obj.keys()); stack.extend(obj.values())
        elif isinstance(obj, (list, tuple, set, frozenset)):
            stack.extend(obj)
    return found


def gate_c_declaration_coverage():
    observed = {}
    charts = 0
    places = ((25.6, 85.1333, "Asia/Kolkata"), (-33.8688, 151.2093, "Australia/Sydney"))
    for latitude, longitude, zone in places:
      for month in range(1, 13):
        for hour in range(0, 24, 3):
            birth = BirthData(1990, month, 15, hour, 0, 0.0, latitude, longitude, zone)
            snapshot = calculate(birth).snapshot
            roots = [
                build_master_chart(snapshot),
                navamsa_chart(snapshot),
                dashamsa_chart(snapshot),
                kp_chart(birth),
                parashari_drishti(birth),
            ]
            roots += [divisional_chart(snapshot, d) for d, _s in registered_vargas()]
            charts += 1
            for instance in _walk(roots):
                model = type(instance).__name__
                for field in dataclasses.fields(instance):
                    declaration = declared(model, field.name)
                    if declaration is None or not is_index(declaration[0]):
                        continue
                    value = getattr(instance, field.name)
                    key = f"{model}.{field.name}"
                    bucket = observed.setdefault(key, set())
                    if isinstance(value, int):
                        bucket.add(value)
                    elif isinstance(value, dict):
                        ints = [v for v in value.values() if isinstance(v, int)]
                        bucket.update(ints or [k for k in value.keys() if isinstance(k, int)])
                    elif isinstance(value, (tuple, list)):
                        bucket.update(v for v in value if isinstance(v, int))

    index_fields = {k: v for k, v in SIGN_FIELD_CONVENTIONS.items() if is_index(v[0])}
    missing = sorted(set(index_fields) - set(observed))
    if missing:
        fail(f"declared index fields never observed on real charts: {missing}")

    per_field = {}
    for key, values in sorted(observed.items()):
        convention = index_fields[key][0]
        allowed = set(range(12)) if convention == ZERO_BASED else set(range(1, 13))
        witness = 0 if convention == ZERO_BASED else 12
        outside = sorted(values - allowed)
        if outside:
            fail(f"{key}: declared {convention} but observed out-of-range {outside}")
        if witness not in values:
            fail(f"{key}: declared {convention} NOT PROVEN; the discriminating "
                 f"witness {witness} never appeared (observed {sorted(values)})")
        per_field[key] = {
            "convention": convention,
            "discriminating_witness": witness,
            "distinct_values_observed": len(values),
            "full_zodiac_coverage": values == allowed,
            "min": min(values), "max": max(values),
        }
    return {"charts_swept": charts, "fields_proven": len(per_field),
            "mismatches": 0,
            "proof": ("each declaration proven by a value impossible under the "
                      "other convention, plus range containment"),
            "fields": per_field}


def gate_d_cross_layer():
    step = 360.0 / 4999
    checked = 0
    for i in range(4999):
        longitude = i * step + 0.0007
        one_based = [zodiac_sign(longitude), kp_chain(longitude).sign_number]
        one_based += list(aspected_signs("Saturn", zodiac_sign(longitude)))
        zero_based = [navamsa_sign(longitude), dashamsa_sign(longitude)]
        for division, school in registered_vargas():
            zero_based.append(classify(longitude, get_varga_rule(division, school)).d_sign)
        for value in one_based:
            if not 1 <= value <= 12 or Sign.from_one_based(value).zero_based != value - 1:
                fail(f"one-based surface at {longitude}: {value}")
            checked += 1
        for value in zero_based:
            if not 0 <= value <= 11 or Sign.from_zero_based(value).one_based != value + 1:
                fail(f"zero-based surface at {longitude}: {value}")
            checked += 1
        if Sign.from_one_based(zodiac_sign(longitude)) != \
           Sign.from_one_based(kp_chain(longitude).sign_number):
            fail(f"D1 and KP disagree on rashi at {longitude}")
    return {"surface_checks": checked, "mismatches": 0,
            "surfaces": len(SIGN_FUNCTION_CONVENTIONS)}


def main():
    tee = support.start_transcript()
    preconditions = support.preflight()
    report = {
        "schema": "sign_convention_v1_certification",
        "adr": "ADR-0012",
        "date": str(date.today()),
        "scope": ("explicit, machine-checked sign-index conventions across every "
                  "layer; no certified value renumbered"),
        "decisions": {
            "SC-A": "inert Sign value type as the shared convention carrier",
            "SC-B": "purely additive adoption; no certified value or field changed",
            "SC-C": "declaration registry enforced by a collected gate",
        },
        "certified_conventions": {
            "varga_level": "zero_based (Aries = 0), certified and locked",
            "rashi_level": "one_based (Aries = 1), certified and locked",
        },
        "declaration_registry": {
            key: {"convention": value[0], "shape": value[1], "accessor": value[2]}
            for key, value in sorted(SIGN_FIELD_CONVENTIONS.items())
        },
        "function_registry": dict(sorted(SIGN_FUNCTION_CONVENTIONS.items())),
        "gates": {
            "A_non_invasiveness": gate_a_non_invasiveness(),
            "B_sign_type": gate_b_sign_type(),
            "C_declaration_coverage": gate_c_declaration_coverage(),
            "D_cross_layer_agreement": gate_d_cross_layer(),
        },
        "explicit_non_claims": [
            "no renumbering of any certified sign value",
            "no deprecation of existing fields in V1",
            "house-number conventions are out of scope for V1",
            "nakshatra and division-index conventions are out of scope for V1",
        ],
        "environment": {"python": sys.version.split()[0]},
        "preconditions": preconditions,
        "result": "PASS",
    }
    out = support.emit(report, "SIGN_CONVENTION_V1_certification.json", "sign_convention", tee)
    gates = report["gates"]
    print("=" * 60)
    print("SIGN_CONVENTION_V1 CERTIFICATION")
    print("=" * 60)
    print(f"A_non_invasiveness   : {gates['A_non_invasiveness']['sweep_points']} points, "
          f"D9 {gates['A_non_invasiveness']['d9_sweep_sha256'][:16]}..., "
          f"D10 {gates['A_non_invasiveness']['d10_sweep_sha256'][:16]}..., "
          f"{len(gates['A_non_invasiveness']['registry_varga_sweep_sha256'])} registry vargas hashed")
    print(f"B_sign_type          : {gates['B_sign_type']}")
    print(f"C_declaration_coverage: {gates['C_declaration_coverage']['fields_proven']} fields proven "
          f"over {gates['C_declaration_coverage']['charts_swept']} charts, 0 mismatches")
    print(f"D_cross_layer        : {gates['D_cross_layer_agreement']['surface_checks']} checks, 0 mismatches")
    print("archived             :", out.relative_to(ROOT).as_posix())
    print("RESULT               : PASS")


if __name__ == "__main__":
    main()
