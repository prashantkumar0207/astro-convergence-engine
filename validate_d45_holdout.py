"""Independent D45 Akshavedamsa holdout validator (ADR-0077, ADR-0085).

Validates the PRODUCTION, registered D45 rule (engine.astrology.varga_d45,
VARGA_D45_V1) against a reference built INDEPENDENTLY inside this file: a
per-sign lookup table constructed by direct sign-name enumeration (movable/
fixed/dual triads), not the framework's own modular-arithmetic offsets.

ADR-0085 addition: this file also verifies the COMPOSITION/PLUMBING layer -
engine.astrology.divisional_chart.divisional_chart(snapshot, 45) /
engine.astrology.varga_chart_builder.build_varga_chart() - which the
classify()-only checks above (and every gate in scripts/certify_d45.py) never
exercise. See verify_composition() and run_mutation_self_check() below. This
targets a class of defect distinct from classify()'s own correctness (already
covered by the dense/boundary batteries above and by certify_d45.py's own
gates A/B/F/G): whether build_varga_chart() correctly WIRES each already-
correct classify() result into the right VargaPosition/VargaPlanet slot for
the right body, without swapping fields or cross-wiring planets. A real,
independently-reproduced planet cross-wiring mutation was shown (this task's
own governing investigation, recorded in ADR-0085) to pass all 872 tests in
this repository's existing suite silently - this is the standing regression
guard against that specific defect class.

WP-N1 N1-G1 correction: verify_composition() takes its expected sign, division
number and fraction from reference_d45_position() below, which uses nothing
from engine.*. Production classify() is consulted only to attribute a mismatch
to its layer; it never decides pass or fail. The fraction convention rests on
engine/astrology/varga_classifier.py's documented behaviour, compared exactly;
no ratified text states it. The snapshot is production input, declared as such:
astronomical correctness is certified elsewhere.

Run:  python validate_d45_holdout.py
"""

import dataclasses
import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import engine.astrology  # noqa: F401  (registers production vargas, including D45)
from engine.astrology.varga_classifier import classify  # framework (SUBJECT)
from engine.astrology.varga_registry import (
    get_varga_rule,
    register_varga_rule,
    unregister_varga_rule,
)

SIGNS = ("Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces")

#: Independent reference, built by direct enumeration (not offset arithmetic):
#: for a movable-sign source, the 45-part sequence starts at Aries and repeats
#: the twelve signs in zodiacal order; fixed starts at Leo; dual starts at
#: Sagittarius. Materialized as an explicit 45-entry table per source sign.
_MOVABLE_START, _FIXED_START, _DUAL_START = "Aries", "Leo", "Sagittarius"
_MOVABLE, _FIXED, _DUAL = (
    {"Aries", "Cancer", "Libra", "Capricorn"},
    {"Taurus", "Leo", "Scorpio", "Aquarius"},
    {"Gemini", "Virgo", "Sagittarius", "Pisces"},
)

REFERENCE_TABLE = {}
for _source_name in SIGNS:
    if _source_name in _MOVABLE:
        _start = SIGNS.index(_MOVABLE_START)
    elif _source_name in _FIXED:
        _start = SIGNS.index(_FIXED_START)
    else:
        _start = SIGNS.index(_DUAL_START)
    REFERENCE_TABLE[_source_name] = tuple(
        SIGNS[(_start + _k) % 12] for _k in range(45)
    )


#: Independently re-derived from the engine's own documented, already-locked
#: boundary rule (engine/astrology/longitude_utils.py's own docstring: "a degree
#: within BOUNDARY_TOLERANCE below a division's edge promotes to the next
#: division"), not imported from that module - this validator applies the SAME
#: documented convention on its own terms, so it checks whether classify()
#: correctly IMPLEMENTS the documented rule, not whether it matches a naive,
#: unpromoted floor (which would spuriously "fail" at every one of D45's own
#: non-exact 2/3-degree boundaries, per ADR-0077 section 3).
_BOUNDARY_TOLERANCE = 1e-10


_REFERENCE_WIDTH = 30.0 / 45.0
_REFERENCE_COUNT = 45


def _reference_normalize(longitude: float) -> float:
    """Reduce to [0, 360). Float modulo returns exactly 360.0 for tiny negatives."""
    longitude = longitude % 360.0
    return 0.0 if longitude >= 360.0 else longitude


def reference_d45(longitude: float):
    longitude = _reference_normalize(longitude)
    source = int(longitude // 30.0)
    degree = longitude - source * 30.0
    # ADR-0112 s3: within the tolerance below the next sign, the value belongs to it,
    # at degree 0, as D1 classifies it. Pisces' top edge is not promoted.
    if source < 11 and degree + _BOUNDARY_TOLERANCE >= 30.0:
        source, degree = source + 1, 0.0
    width = 30.0 / 45.0
    division = int((degree + _BOUNDARY_TOLERANCE) / width)
    if division > 44:
        division = 44
    return SIGNS.index(REFERENCE_TABLE[SIGNS[source]][division]), division


def reference_d45_position(longitude: float):
    """Independent (sign, division_index, fraction), both indices 0-based.

    Uses nothing from engine.*: engine/tests/test_d45_reference_independence.py
    enforces that by parsing this file. The sign split promotes within the tolerance,
    as D1 does (ADR-0112 s3). A
    degree within the tolerance below a division's edge promotes to the next
    division, where it sits at fraction 0.0. The top division is clamped.
    """
    longitude = _reference_normalize(longitude)
    source = int(longitude // 30.0)
    degree = longitude - source * 30.0
    # ADR-0112 s3: within the tolerance below the next sign, the value belongs to it,
    # at degree 0, as D1 classifies it. Pisces' top edge is not promoted.
    if source < 11 and degree + _BOUNDARY_TOLERANCE >= 30.0:
        source, degree = source + 1, 0.0
    index = int((degree + _BOUNDARY_TOLERANCE) / _REFERENCE_WIDTH)
    if index >= _REFERENCE_COUNT:
        index = _REFERENCE_COUNT - 1
    fraction = (degree - index * _REFERENCE_WIDTH) / _REFERENCE_WIDTH
    if fraction < 0.0:
        fraction = 0.0
    return SIGNS.index(REFERENCE_TABLE[SIGNS[source]][index]), index, fraction


#: Real, fixed holdout birth data for the composition/plumbing check
#: (ADR-0085) - distinct from the dense/boundary sweeps above, which need no
#: real chart at all. Chosen fresh for this check, spanning both hemispheres
#: and a range of eras, never used to tune classify() or the frozen rule.
COMPOSITION_HOLDOUT = [
    {"id": "C1_delhi_1990", "year": 1990, "month": 5, "day": 15, "hour": 10,
     "minute": 30, "second": 0.0, "lat": 28.6139, "lon": 77.2090},
    {"id": "C2_newyork_1972", "year": 1972, "month": 11, "day": 3, "hour": 4,
     "minute": 17, "second": 22.0, "lat": 40.7128, "lon": -74.0060},
    {"id": "C3_johannesburg_2005", "year": 2005, "month": 2, "day": 27, "hour": 19,
     "minute": 52, "second": 8.0, "lat": -26.2041, "lon": 28.0473},
    {"id": "C4_reykjavik_2018", "year": 2018, "month": 8, "day": 9, "hour": 1,
     "minute": 3, "second": 44.0, "lat": 64.1466, "lon": -21.9426},
    {"id": "C5_singapore_1961", "year": 1961, "month": 6, "day": 21, "hour": 15,
     "minute": 40, "second": 12.0, "lat": 1.3521, "lon": 103.8198},
]


def _composition_snapshot(case):
    from engine.astronomy.profile import PARASHARI_LAHIRI
    from engine.calculations.calculations import calculate
    from engine.models.birth_data import BirthData

    bd = BirthData(case["year"], case["month"], case["day"], case["hour"],
                    case["minute"], case["second"], case["lat"], case["lon"], "UTC")
    return calculate(bd, profile=PARASHARI_LAHIRI).snapshot


def _attribute(field, chart_value, reference_value, source_longitude):
    """Diagnostic only: name the layer a field mismatch belongs to.

    A chart value that equals what classify() now returns, while the reference
    disagrees, propagated from the classification layer. Anything else arose
    in composition. The pass/fail decision never reads this.
    """
    try:
        from engine.astrology import varga_classifier, varga_registry

        rule = varga_registry.get_varga_rule(45, "parashara")
        produced = varga_classifier.classify(source_longitude, rule)
        classifier_value = {"sign": produced.d_sign,
                            "division_number": produced.division_number,
                            "fraction": produced.fraction}[field]
    except Exception as exc:  # noqa: BLE001 - a diagnostic must not mask the mismatch
        return f"undetermined ({exc!r})"
    if chart_value == classifier_value and classifier_value != reference_value:
        return "classification"
    return "composition"


def check_chart(case_id, snapshot, chart):
    """Compare one chart with its snapshot and the independent reference.

    Returns mismatch descriptions, each ending in its attribution. The
    expected values come from reference_d45_position() alone.
    """
    mismatches = []

    def composition(message):
        mismatches.append(f"{case_id}/{message} [attribution: composition]")

    if chart.varga != 45 or chart.school != "parashara":
        composition(f"chart: varga={chart.varga} school={chart.school}")
    if chart.provenance is not snapshot.provenance:
        composition("chart: provenance is not the snapshot's own provenance")
    if type(chart.ascendant).__name__ != "VargaPosition":
        composition(f"ascendant: type={type(chart.ascendant).__name__}")

    expected_names = set(snapshot.sidereal_planets)
    actual_names = set(chart.planets)
    for name in sorted(actual_names - expected_names):
        composition(f"{name}: not a snapshot body")
    for name in sorted(expected_names - actual_names):
        composition(f"{name}: missing from the chart")

    bodies = [("ascendant", snapshot.houses.ascendant, chart.ascendant)]
    for name, planet in snapshot.sidereal_planets.items():
        if name in chart.planets:
            bodies.append((name, planet.longitude, chart.planets[name]))

    for label, source_longitude, position in bodies:
        if label != "ascendant":
            if type(position).__name__ != "VargaPlanet":
                composition(f"{label}: type={type(position).__name__}")
            if position.name != label:
                composition(f"{label}: name={position.name!r}")
        if position.source_longitude != source_longitude:
            composition(f"{label}: source_longitude={position.source_longitude!r} "
                        f"expected={source_longitude!r}")
        sign, index, fraction = reference_d45_position(source_longitude)
        # division_number is 1-based, per engine/models/varga_planet.py's documented model.
        for field, reference_value in (("sign", sign), ("division_number", index + 1),
                                       ("fraction", fraction)):
            chart_value = getattr(position, field)
            if chart_value != reference_value:
                layer = _attribute(field, chart_value, reference_value, source_longitude)
                mismatches.append(f"{case_id}/{label}: {field}={chart_value!r} "
                                  f"expected={reference_value!r} [attribution: {layer}]")
    return mismatches


def verify_composition(cases=COMPOSITION_HOLDOUT):
    """
    Exercise the REAL production composition entry point -
    engine.astrology.divisional_chart.divisional_chart(snapshot, 45), which
    calls engine.astrology.varga_chart_builder.build_varga_chart() - and
    check every field of every resulting VargaPosition/VargaPlanet against
    this file's own reference, plus each planet's identity and the chart's
    set of bodies.

    A corruption inside classify() or the registered rule reaches the chart
    but not the reference, so it is caught here as well as a wiring error.

    Returns a list of mismatch descriptions; empty means every field of
    every body in every case matched exactly.
    """
    from engine.astrology.divisional_chart import divisional_chart

    mismatches = []
    for case in cases:
        snapshot = _composition_snapshot(case)
        mismatches.extend(check_chart(case["id"], snapshot, divisional_chart(snapshot, 45)))
    return mismatches


def _corrupt_build_varga_chart_field_swap():
    """A realistic wrong-implementation mistake: sign and division_number
    swapped inside the per-planet/ascendant VargaPosition/VargaPlanet
    construction. Disguised as source-level code (module/name/qualname
    preserved), matching scripts/check_mutation_detection.py's own
    established disguise convention for engine.kp.* corruptions - a wrong
    implementation actually written into the module carries exactly this
    metadata, unlike a naive runtime monkeypatch."""

    from engine.astrology.varga_classifier import classify as _classify
    from engine.models.varga_chart import VargaChart
    from engine.models.varga_planet import VargaPlanet, VargaPosition

    def corrupted(snapshot, division, rule, school):
        asc = _classify(snapshot.houses.ascendant, rule)
        ascendant = VargaPosition(
            source_longitude=snapshot.houses.ascendant,
            sign=asc.division_number,        # swapped
            division_number=asc.d_sign,       # swapped
            fraction=asc.fraction,
        )
        planets = {}
        for name, planet in snapshot.sidereal_planets.items():
            c = _classify(planet.longitude, rule)
            planets[name] = VargaPlanet(
                name=name,
                source_longitude=planet.longitude,
                sign=c.division_number,        # swapped
                division_number=c.d_sign,       # swapped
                fraction=c.fraction,
            )
        return VargaChart(varga=division, school=school, ascendant=ascendant,
                           planets=planets, provenance=snapshot.provenance)

    import engine.astrology.varga_chart_builder as builder_module
    pristine = builder_module.build_varga_chart
    corrupted.__module__ = pristine.__module__
    corrupted.__name__ = pristine.__name__
    corrupted.__qualname__ = getattr(pristine, "__qualname__", pristine.__name__)
    return pristine, corrupted


def _corrupt_build_varga_chart_cross_wiring():
    """A second, independently realistic mistake: each planet after the
    first receives the PREVIOUS planet's own classification instead of its
    own (a loop-variable-reuse error). Every field stays within its own
    valid range - unlike the field-swap corruption above, no generic range/
    convention check anywhere in this repository's own test suite happens
    to catch this one (verified directly in the governing investigation,
    ADR-0085: 872/872 tests passed under this exact corruption)."""

    from engine.astrology.varga_classifier import classify as _classify
    from engine.models.varga_chart import VargaChart
    from engine.models.varga_planet import VargaPlanet, VargaPosition

    def corrupted(snapshot, division, rule, school):
        asc = _classify(snapshot.houses.ascendant, rule)
        ascendant = VargaPosition(
            source_longitude=snapshot.houses.ascendant,
            sign=asc.d_sign, division_number=asc.division_number, fraction=asc.fraction,
        )
        planets = {}
        previous = None
        for name, planet in snapshot.sidereal_planets.items():
            c = _classify(planet.longitude, rule)
            use = previous if previous is not None else c
            planets[name] = VargaPlanet(
                name=name,
                source_longitude=planet.longitude,
                sign=use.d_sign, division_number=use.division_number, fraction=use.fraction,
            )
            previous = c
        return VargaChart(varga=division, school=school, ascendant=ascendant,
                           planets=planets, provenance=snapshot.provenance)

    import engine.astrology.varga_chart_builder as builder_module
    pristine = builder_module.build_varga_chart
    corrupted.__module__ = pristine.__module__
    corrupted.__name__ = pristine.__name__
    corrupted.__qualname__ = getattr(pristine, "__qualname__", pristine.__name__)
    return pristine, corrupted


def _corrupt_build_varga_chart_source_longitude():
    """A third, distinct corruption: source_longitude corrupted to always
    record the ASCENDANT's own longitude for every planet, while sign/
    division_number/fraction remain correctly derived from the planet's own
    real longitude - a realistic "wrong variable captured" mistake that
    leaves the classification itself right but the audit-trail field wrong."""

    from engine.astrology.varga_classifier import classify as _classify
    from engine.models.varga_chart import VargaChart
    from engine.models.varga_planet import VargaPlanet, VargaPosition

    def corrupted(snapshot, division, rule, school):
        asc = _classify(snapshot.houses.ascendant, rule)
        ascendant = VargaPosition(
            source_longitude=snapshot.houses.ascendant,
            sign=asc.d_sign, division_number=asc.division_number, fraction=asc.fraction,
        )
        planets = {}
        for name, planet in snapshot.sidereal_planets.items():
            c = _classify(planet.longitude, rule)
            planets[name] = VargaPlanet(
                name=name,
                source_longitude=snapshot.houses.ascendant,  # corrupted: wrong body's longitude
                sign=c.d_sign, division_number=c.division_number, fraction=c.fraction,
            )
        return VargaChart(varga=division, school=school, ascendant=ascendant,
                           planets=planets, provenance=snapshot.provenance)

    import engine.astrology.varga_chart_builder as builder_module
    pristine = builder_module.build_varga_chart
    corrupted.__module__ = pristine.__module__
    corrupted.__name__ = pristine.__name__
    corrupted.__qualname__ = getattr(pristine, "__qualname__", pristine.__name__)
    return pristine, corrupted


def _corrupt_build_varga_chart_name_mislabel():
    """One planet's name field carries another body's name; its values are right."""

    from engine.astrology.varga_classifier import classify as _classify
    from engine.models.varga_chart import VargaChart
    from engine.models.varga_planet import VargaPlanet, VargaPosition

    def corrupted(snapshot, division, rule, school):
        asc = _classify(snapshot.houses.ascendant, rule)
        ascendant = VargaPosition(
            source_longitude=snapshot.houses.ascendant,
            sign=asc.d_sign, division_number=asc.division_number, fraction=asc.fraction,
        )
        names = list(snapshot.sidereal_planets)
        planets = {}
        for name, planet in snapshot.sidereal_planets.items():
            c = _classify(planet.longitude, rule)
            planets[name] = VargaPlanet(
                name=names[1] if name == names[0] else name,  # corrupted
                source_longitude=planet.longitude,
                sign=c.d_sign, division_number=c.division_number, fraction=c.fraction,
            )
        return VargaChart(varga=division, school=school, ascendant=ascendant,
                           planets=planets, provenance=snapshot.provenance)

    import engine.astrology.varga_chart_builder as builder_module
    pristine = builder_module.build_varga_chart
    corrupted.__module__ = pristine.__module__
    corrupted.__name__ = pristine.__name__
    corrupted.__qualname__ = getattr(pristine, "__qualname__", pristine.__name__)
    return pristine, corrupted


def _corrupt_build_varga_chart_body_set(change):
    """The chart's set of bodies is wrong; `change` edits the finished planet dict."""

    import engine.astrology.varga_chart_builder as builder_module
    pristine = builder_module.build_varga_chart

    def corrupted(snapshot, division, rule, school):
        chart = pristine(snapshot, division, rule, school)
        planets = dict(chart.planets)
        change(planets)
        return dataclasses.replace(chart, planets=planets)

    corrupted.__module__ = pristine.__module__
    corrupted.__name__ = pristine.__name__
    corrupted.__qualname__ = getattr(pristine, "__qualname__", pristine.__name__)
    return pristine, corrupted


def _extra_planet(planets):
    first = next(iter(planets.values()))
    planets["Phantom"] = dataclasses.replace(first, name="Phantom")


def _missing_planet(planets):
    del planets[next(iter(planets))]


def _corrupt_build_varga_chart_ascendant_from_planet():
    """The ascendant is classified from the first planet's longitude."""

    import engine.astrology.varga_chart_builder as builder_module
    from engine.astrology.varga_classifier import classify as _classify
    pristine = builder_module.build_varga_chart

    def corrupted(snapshot, division, rule, school):
        chart = pristine(snapshot, division, rule, school)
        wrong = _classify(next(iter(snapshot.sidereal_planets.values())).longitude, rule)
        ascendant = dataclasses.replace(chart.ascendant, sign=wrong.d_sign,
                                        division_number=wrong.division_number,
                                        fraction=wrong.fraction)
        return dataclasses.replace(chart, ascendant=ascendant)

    corrupted.__module__ = pristine.__module__
    corrupted.__name__ = pristine.__name__
    corrupted.__qualname__ = getattr(pristine, "__qualname__", pristine.__name__)
    return pristine, corrupted


def _corrupt_build_varga_chart_fraction_complement():
    """Each planet's fraction is its complement, which stays in range."""

    import engine.astrology.varga_chart_builder as builder_module
    pristine = builder_module.build_varga_chart

    def corrupted(snapshot, division, rule, school):
        chart = pristine(snapshot, division, rule, school)
        planets = {name: dataclasses.replace(planet, fraction=1.0 - planet.fraction)
                   for name, planet in chart.planets.items()}
        return dataclasses.replace(chart, planets=planets)

    corrupted.__module__ = pristine.__module__
    corrupted.__name__ = pristine.__name__
    corrupted.__qualname__ = getattr(pristine, "__qualname__", pristine.__name__)
    return pristine, corrupted


def _corrupt_classifier(change):
    """A defect inside the classifier, which the builder and classify() both inherit."""

    import engine.astrology.varga_classifier as classifier_module
    pristine = classifier_module._classify_cyclic

    def corrupted(source_sign, degree, rule):
        return change(pristine(source_sign, degree, rule))

    corrupted.__module__ = pristine.__module__
    corrupted.__name__ = pristine.__name__
    corrupted.__qualname__ = getattr(pristine, "__qualname__", pristine.__name__)
    return pristine, corrupted


def _halve_fraction(result):
    return dataclasses.replace(result, fraction=result.fraction / 2.0)


def _shift_sign(result):
    return dataclasses.replace(result, d_sign=(result.d_sign + 1) % 12)


def _install_attribute(module_name, attribute, factory):
    """Install a corruption on a module attribute; return its restore function."""

    def install():
        module = importlib.import_module(module_name)
        pristine, corrupted = factory()
        if getattr(module, attribute) is not pristine:
            raise AssertionError(f"{module_name}.{attribute} is not pristine before the control")
        setattr(module, attribute, corrupted)

        def restore():
            setattr(module, attribute, pristine)
            if getattr(module, attribute) is not pristine:
                raise AssertionError(f"{module_name}.{attribute} was not restored")

        return restore

    return install


def _install_tampered_rule():
    """The rule registered for D45 starts every source sign one sign later."""

    original = get_varga_rule(45, "parashara")
    tampered = dataclasses.replace(
        original, start_sign=tuple((start + 1) % 12 for start in original.start_sign))
    unregister_varga_rule(45, "parashara")
    register_varga_rule(45, "parashara", tampered)

    def restore():
        unregister_varga_rule(45, "parashara")
        register_varga_rule(45, "parashara", original)
        if get_varga_rule(45, "parashara") is not original:
            raise AssertionError("the registered D45 rule was not restored")

    return restore


_BUILDER = ("engine.astrology.varga_chart_builder", "build_varga_chart")
_CLASSIFIER = ("engine.astrology.varga_classifier", "_classify_cyclic")

#: (control, install, the layer its mismatches must be attributed to). Controls
#: here are expected to be seen by verify_composition() only: they begin after
#: the sweeps have finished, so no sweep observes them.
_MUTATION_CONTROLS = (
    ("field_order_swap", _install_attribute(*_BUILDER, _corrupt_build_varga_chart_field_swap),
     "composition"),
    ("planet_cross_wiring", _install_attribute(*_BUILDER, _corrupt_build_varga_chart_cross_wiring),
     "composition"),
    ("source_longitude_corruption",
     _install_attribute(*_BUILDER, _corrupt_build_varga_chart_source_longitude), "composition"),
    ("planet_name_mislabel", _install_attribute(*_BUILDER, _corrupt_build_varga_chart_name_mislabel),
     "composition"),
    ("extra_planet_entry",
     _install_attribute(*_BUILDER, lambda: _corrupt_build_varga_chart_body_set(_extra_planet)),
     "composition"),
    ("missing_planet_entry",
     _install_attribute(*_BUILDER, lambda: _corrupt_build_varga_chart_body_set(_missing_planet)),
     "composition"),
    ("ascendant_from_planet",
     _install_attribute(*_BUILDER, _corrupt_build_varga_chart_ascendant_from_planet), "composition"),
    ("fraction_complement",
     _install_attribute(*_BUILDER, _corrupt_build_varga_chart_fraction_complement), "composition"),
    ("classifier_fraction_shared",
     _install_attribute(*_CLASSIFIER, lambda: _corrupt_classifier(_halve_fraction)), "classification"),
    ("classifier_sign_shared",
     _install_attribute(*_CLASSIFIER, lambda: _corrupt_classifier(_shift_sign)), "classification"),
    ("registered_rule_tampered", _install_tampered_rule, "classification"),
)


def _attributions(mismatches):
    return sorted({mismatch.rsplit("[attribution: ", 1)[1].rstrip("]") for mismatch in mismatches})


def run_mutation_self_check():
    """
    Genuine, real, in-process mutation detection (ADR-0085): the REAL production
    object is replaced in-process, the REAL verify_composition() is re-run
    against the corrupted code path, and a mismatch attributed to the expected
    layer must be observed. The pristine object is then restored, its identity
    confirmed, and verify_composition() confirmed clean again.

    The self-check alone cannot show that a certifier acts on a failure.
    engine/tests/test_d45_reference_independence.py observes
    scripts/certify_d45.py's real gate reaching fail() under real corruptions.

    Never touches any file on disk. Returns (all_detected: bool, results:
    list of per-control dicts).
    """
    clean = verify_composition()
    if clean:
        raise AssertionError(
            f"cannot run the mutation self-check: verify_composition() already reports "
            f"mismatches against the PRISTINE production code: {clean[:5]}"
        )

    results = []
    all_detected = True
    for control_name, install, expected_layer in _MUTATION_CONTROLS:
        restore = install()
        try:
            mismatches_under_mutation = verify_composition()
        finally:
            restore()

        layers = _attributions(mismatches_under_mutation)
        detected = bool(mismatches_under_mutation) and layers == [expected_layer]
        results.append({
            "control": control_name,
            "detected": detected,
            "mismatches": len(mismatches_under_mutation),
            "attribution": layers,
            "expected_attribution": expected_layer,
            "sample_mismatch": mismatches_under_mutation[0] if mismatches_under_mutation else None,
        })
        if not detected:
            all_detected = False

    restored = verify_composition()
    if restored:
        raise AssertionError(
            f"production code was not correctly restored after mutation "
            f"testing: {restored[:5]}"
        )

    return all_detected, results


def main() -> int:
    rule = get_varga_rule(45, "parashara")
    failures = []

    dense = 0
    step = 360.0 / 51429
    for i in range(51429):
        longitude = i * step
        result = classify(longitude, rule)
        expected_sign, expected_division = reference_d45(longitude)
        if (result.d_sign, result.division_index) != (expected_sign, expected_division):
            failures.append(("dense", longitude))
        dense += 1

    boundary = 0
    for k in range(540):  # 45 divisions x 12 signs
        base = k * (30.0 / 45.0)
        points = [base]
        up = base
        import math
        for _ in range(3):
            up = math.nextafter(up, math.inf)
            points.append(up)
        for longitude in points:
            if longitude >= 360.0:
                continue
            result = classify(longitude, rule)
            expected_sign, expected_division = reference_d45(longitude)
            if (result.d_sign, result.division_index) != (expected_sign, expected_division):
                failures.append(("boundary", longitude))
            boundary += 1

    print("=" * 60)
    print("INDEPENDENT D45 AKSHAVEDAMSA VALIDATION")
    print("=" * 60)
    print(f"Dense cases    : {dense}")
    print(f"Boundary cases : {boundary}")
    # Each section reports for itself, so a classification defect is not
    # recorded as a composition failure merely because the sweep ran first.
    # Each sentinel below is printed only when its own section passes.
    if failures:
        print(f"FAILURES: {len(failures)}; first: {failures[:5]}")
        print("RESULT: FAIL")
    else:
        print()
        print("RESULT: ALL INDEPENDENT D45 CASES PASSED")

    print()
    print("=" * 60)
    print("D45 COMPOSITION/PLUMBING VERIFICATION (ADR-0085)")
    print("=" * 60)
    composition_mismatches = verify_composition()
    print(f"Composition cases checked: {len(COMPOSITION_HOLDOUT)} charts x "
          f"(1 ascendant + N planets), every field")
    if composition_mismatches:
        print(f"FAILURES: {len(composition_mismatches)}; first: {composition_mismatches[:5]}")
        print(f"ATTRIBUTION: {_attributions(composition_mismatches)}")
        print("RESULT: D45 COMPOSITION VERIFICATION FAILED")
        print("RESULT: D45 COMPOSITION MUTATION SELF-CHECK NOT RUN - composition is not clean")
        print("=" * 60)
        return 1
    print("RESULT: D45 COMPOSITION VERIFICATION PASSED")

    print()
    print("=" * 60)
    print("D45 COMPOSITION MUTATION SELF-CHECK (ADR-0085)")
    print("=" * 60)
    all_detected, mutation_results = run_mutation_self_check()
    for result in mutation_results:
        status = "DETECTED" if result["detected"] else "MISSED (BAD)"
        print(f"  {result['control']:28s} {status} mismatches={result['mismatches']} "
              f"attribution={result['attribution']}")
        if not result["detected"]:
            print(f"    (expected a mismatch attributed to {result['expected_attribution']})")
    if not all_detected:
        print("RESULT: D45 COMPOSITION MUTATION SELF-CHECK FAILED - "
              "at least one control was not detected")
        return 1
    print("RESULT: D45 COMPOSITION MUTATION DETECTION PASSED")
    print("=" * 60)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
