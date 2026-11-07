"""
D45 Gate I independence and failure observation (WP-N1 N1-G1, N1-G2).

Two gaps are closed and pinned here:

- N1-G1: verify_composition() took its expected values from production
  classify(), so a defect inside the classifier could not be seen.
- N1-G2: the validator's self-check never showed that the certifier acts on a
  failure. The gate-level tests below run scripts/certify_d45.py's REAL Gate I
  and its REAL validator subprocess, and observe the real fail().

Corruptions exist only in memory, in a child process started through a
temporary sitecustomize, or in a temporary copy of the validator. No production
source changes on disk, and no certification artifact is written: these tests
call Gate I alone, never the certifier's main().
"""

import ast
import dataclasses
import importlib.util
import json
import math
import os
import shutil
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import pytest

from engine.astrology import varga_chart_builder, varga_classifier
from engine.astrology.divisional_chart import divisional_chart
from engine.astrology.varga_classifier import classify
from engine.astrology.varga_registry import get_varga_rule

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = ROOT / "validate_d45_holdout.py"

#: The reference section: none of these may use a name bound by an import.
REFERENCE_FUNCTIONS = ("_reference_normalize", "reference_d45", "reference_d45_position")

#: Error bound for the exact-rational audit, set from float error analysis before
#: any run: degree error <= about 6e-14 at longitudes near 360, division by
#: 2/3 gives about 1e-13, and one further order of margin is added. A test-only
#: tolerance; Gate I itself compares fraction exactly.
RATIONAL_AUDIT_BOUND = 1e-12

EXPECTED_CONTROLS = {
    "field_order_swap": "composition",
    "planet_cross_wiring": "composition",
    "source_longitude_corruption": "composition",
    "planet_name_mislabel": "composition",
    "extra_planet_entry": "composition",
    "missing_planet_entry": "composition",
    "ascendant_from_planet": "composition",
    "fraction_complement": "composition",
    "classifier_fraction_shared": "classification",
    "classifier_sign_shared": "classification",
    "registered_rule_tampered": "classification",
}


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = _load(VALIDATOR_PATH, "validate_d45_holdout_under_test")
certifier = _load(ROOT / "scripts" / "certify_d45.py", "certify_d45_under_test")


# ------------------------------------------------------------------ the reference itself

#: Typed by hand from the classical statement (movable from Aries, fixed from Leo,
#: dual from Sagittarius): the first division of each sign, and the division at
#: 10 deg 20', index 15, whose target is three signs on from the start.
HAND_TYPED = (
    ("Aries", "Aries", "Cancer"), ("Taurus", "Leo", "Scorpio"), ("Gemini", "Sagittarius", "Pisces"),
    ("Cancer", "Aries", "Cancer"), ("Leo", "Leo", "Scorpio"), ("Virgo", "Sagittarius", "Pisces"),
    ("Libra", "Aries", "Cancer"), ("Scorpio", "Leo", "Scorpio"), ("Sagittarius", "Sagittarius", "Pisces"),
    ("Capricorn", "Aries", "Cancer"), ("Aquarius", "Leo", "Scorpio"), ("Pisces", "Sagittarius", "Pisces"),
)


def test_reference_matches_a_hand_typed_table():
    for source, (source_name, first, sixteenth) in enumerate(HAND_TYPED):
        assert validator.SIGNS[source] == source_name
        sign, index, fraction = validator.reference_d45_position(source * 30.0)
        assert (validator.SIGNS[sign], index, fraction) == (first, 0, 0.0)
        sign, index, fraction = validator.reference_d45_position(source * 30.0 + 10.0 + 1.0 / 3.0)
        assert (validator.SIGNS[sign], index) == (sixteenth, 15)
        assert fraction == pytest.approx(0.5, abs=1e-9)


@pytest.mark.parametrize("longitude", [-1e-16, 0.0, 360.0, 720.0, -360.0])
def test_reference_normalization(longitude):
    assert validator.reference_d45_position(longitude) == (0, 0, 0.0)
    assert validator.reference_d45(longitude) == (0, 0)


def test_reference_promotion_and_top_edge():
    width = 30.0 / 45.0
    for k in (1, 13, 26, 29, 44):
        _sign, index, fraction = validator.reference_d45_position(k * width - 5e-11)
        assert (index, fraction) == (k, 0.0)
    # ADR-0112 s3: within the tolerance below a sign boundary the parent sign
    # promotes, as D1's does, so the value is the next sign's boundary itself.
    for degree in (29.99999999995, math.nextafter(30.0, 0.0)):
        assert validator.reference_d45_position(degree) == validator.reference_d45_position(30.0)
    # Pisces' top edge clamps instead, as D1 does: still the last division.
    for degree in (359.99999999995, math.nextafter(360.0, 0.0)):
        _sign, index, fraction = validator.reference_d45_position(degree)
        assert index == 44
        assert 0.99 < fraction < 1.0
    # Just outside the window nothing promotes.
    _sign, index, fraction = validator.reference_d45_position(30.0 - 2e-10)
    assert index == 44 and 0.99 < fraction < 1.0


def _exact_position(longitude: float):
    """The same convention over exact rationals; shares no floating-point step."""

    value = Fraction(longitude)
    source = math.floor(value / 30)
    degree = value - source * 30
    width = Fraction(2, 3)
    index = min(math.floor((degree + Fraction(1e-10)) / width), 44)
    fraction = max((degree - index * width) / width, Fraction(0))
    threshold_distance = min(abs(degree + Fraction(1e-10) - k * width) for k in (index, index + 1))
    return index, fraction, threshold_distance


def _audit_points():
    width = 30.0 / 45.0
    for source in range(12):
        base = source * 30.0
        for k in range(45):
            edge = base + k * width
            for point in (edge, edge + 1e-9, edge - 1e-9, edge + width / 2.0, edge + 5e-11, edge - 5e-11,
                          math.nextafter(edge, math.inf), math.nextafter(edge, 0.0)):
                if 0.0 <= point < 360.0 and int(point // 30.0) == source:
                    yield point


def test_exact_rational_audit_of_the_reference():
    checked = excluded = 0
    for longitude in _audit_points():
        _sign, index, fraction = validator.reference_d45_position(longitude)
        exact_index, exact_fraction, distance = _exact_position(longitude)
        if distance <= Fraction(1, 10**15):
            excluded += 1
            continue
        assert index == exact_index, longitude
        assert abs(fraction - float(exact_fraction)) <= RATIONAL_AUDIT_BOUND, longitude
        checked += 1
    assert checked > 3000
    assert excluded < checked / 10


# ------------------------------------------------------------------ enforced independence

def independence_violations(source: str) -> list:
    """Names the reference section takes from imports, or imports it makes itself."""

    tree = ast.parse(source)
    imported = set()
    for node in tree.body:
        if isinstance(node, ast.Import):
            imported.update(alias.asname or alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.update(alias.asname or alias.name for alias in node.names)
    violations = []
    # The reference's tables and constants live at module level, so a shared
    # tolerance or table would arrive there. Only the path setup and the exit
    # call may touch an imported name at module level.
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef)):
            continue
        used = {item.id for item in ast.walk(node) if isinstance(item, ast.Name)}
        for name in sorted((used & imported) - {"sys", "Path"}):
            violations.append(f"module level (line {node.lineno}): uses imported name {name}")
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    for name in REFERENCE_FUNCTIONS:
        if name not in functions:
            violations.append(f"{name}: not defined")
            continue
        for node in ast.walk(functions[name]):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                violations.append(f"{name}: imports inside the reference")
            elif isinstance(node, ast.Name) and node.id in imported:
                violations.append(f"{name}: uses imported name {node.id}")
    return violations


def test_reference_section_uses_nothing_imported():
    assert independence_violations(VALIDATOR_PATH.read_text(encoding="utf-8")) == []


def test_independence_check_can_fail():
    source = VALIDATOR_PATH.read_text(encoding="utf-8")
    # Plant the production call in the position reference's own sign split (ADR-0112 s3 promotion lines included).
    wired = source.replace("    source = int(longitude // 30.0)\n    degree = longitude - source * 30.0\n"
                           "    # ADR-0112 s3: within the tolerance below the next sign, the value belongs to it,\n",
                           "    source = classify(longitude, None)\n    degree = longitude - source * 30.0\n"
                           "    # ADR-0112 s3: within the tolerance below the next sign, the value belongs to it,\n", 1)
    assert wired != source
    assert any("uses imported name classify" in item for item in independence_violations(wired))

    local_import = source.replace("def _reference_normalize(longitude: float) -> float:\n",
                                  "def _reference_normalize(longitude: float) -> float:\n"
                                  "    from engine.astrology import longitude_utils\n", 1)
    assert any("imports inside the reference" in item for item in independence_violations(local_import))

    shared_tolerance = source.replace("_BOUNDARY_TOLERANCE = 1e-10\n",
                                      "from engine.astrology.longitude_utils import BOUNDARY_TOLERANCE\n"
                                      "_BOUNDARY_TOLERANCE = BOUNDARY_TOLERANCE\n", 1)
    assert shared_tolerance != source
    assert any("uses imported name BOUNDARY_TOLERANCE" in item for item in independence_violations(shared_tolerance))


def test_verify_composition_expected_values_do_not_read_classify():
    tree = ast.parse(VALIDATOR_PATH.read_text(encoding="utf-8"))
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    for name in ("check_chart", "verify_composition"):
        used = {node.id for node in ast.walk(functions[name]) if isinstance(node, ast.Name)}
        assert not used & {"classify", "get_varga_rule"}, name


# ------------------------------------------------------------------ composition, pristine

def test_pristine_composition_on_the_holdout_is_clean():
    assert validator.verify_composition() == []


def test_holdout_is_preserved():
    assert [case["id"] for case in validator.COMPOSITION_HOLDOUT] == [
        "C1_delhi_1990", "C2_newyork_1972", "C3_johannesburg_2005", "C4_reykjavik_2018", "C5_singapore_1961"]


def _boundary_longitudes():
    width = 30.0 / 45.0
    tolerance = 1e-10
    points = [-1e-16, 360.0, 720.0]
    for source in range(12):
        base = source * 30.0
        points.append(base + 30.0 - tolerance / 2.0)
        for k in (0, 1, 13, 26, 29, 44):
            edge = base + k * width
            points.append(edge)
            for delta in (tolerance / 2.0, 2.0 * tolerance):
                points.extend((edge + delta, edge - delta))
            up = down = edge
            for _ in range(3):
                up, down = math.nextafter(up, math.inf), math.nextafter(down, 0.0)
            points.extend((math.nextafter(edge, math.inf), up, math.nextafter(edge, 0.0), down))
    return points


def test_boundary_fixtures_compose_exactly_through_the_real_chart():
    """Fixtures, not holdout data: they exercise exact fraction agreement at the
    boundaries real charts cannot be made to land on, and they feed no tolerance."""

    snapshot = validator._composition_snapshot(validator.COMPOSITION_HOLDOUT[0])
    names = list(snapshot.sidereal_planets)
    points = _boundary_longitudes()
    checked = 0
    for start in range(0, len(points), len(names) + 1):
        batch = points[start:start + len(names) + 1]
        batch += [0.0] * (len(names) + 1 - len(batch))
        planets = {name: dataclasses.replace(snapshot.sidereal_planets[name], longitude=value)
                   for name, value in zip(names, batch[1:])}
        fixture = dataclasses.replace(snapshot, sidereal_planets=planets,
                                      houses=dataclasses.replace(snapshot.houses, ascendant=batch[0]))
        assert validator.check_chart(f"fixture-{start}", fixture, divisional_chart(fixture, 45)) == []
        checked += len(batch)
    assert checked >= len(points)


# ------------------------------------------------------------------ in-process controls

@pytest.fixture(scope="module")
def self_check():
    pristine_builder = varga_chart_builder.build_varga_chart
    pristine_classifier = varga_classifier._classify_cyclic
    pristine_rule = get_varga_rule(45, "parashara")
    all_detected, results = validator.run_mutation_self_check()
    assert varga_chart_builder.build_varga_chart is pristine_builder
    assert varga_classifier._classify_cyclic is pristine_classifier
    assert get_varga_rule(45, "parashara") is pristine_rule
    return all_detected, {result["control"]: result for result in results}


def test_every_control_is_registered(self_check):
    assert {name: result["expected_attribution"] for name, result in self_check[1].items()} == EXPECTED_CONTROLS


@pytest.mark.parametrize("control", sorted(EXPECTED_CONTROLS))
def test_control_is_detected_and_attributed(self_check, control):
    result = self_check[1][control]
    assert result["detected"] is True, result
    assert result["mismatches"] > 0
    assert result["attribution"] == [EXPECTED_CONTROLS[control]], result


def test_self_check_passes_overall(self_check):
    assert self_check[0] is True


def _control(name):
    return next(entry for entry in validator._MUTATION_CONTROLS if entry[0] == name)


def _classify_expected_mismatches():
    """The pre-correction expected-value path: classify() on each body's own longitude."""

    mismatches = []
    for case in validator.COMPOSITION_HOLDOUT:
        snapshot = validator._composition_snapshot(case)
        chart = divisional_chart(snapshot, 45)
        rule = get_varga_rule(45, "parashara")
        bodies = [(snapshot.houses.ascendant, chart.ascendant)]
        bodies += [(planet.longitude, chart.planets[name]) for name, planet in snapshot.sidereal_planets.items()]
        for longitude, position in bodies:
            expected = classify(longitude, rule)
            if (position.sign, position.division_number, position.fraction) != (
                    expected.d_sign, expected.division_number, expected.fraction):
                mismatches.append(longitude)
    return mismatches


def test_discriminator_separates_the_new_path_from_the_old():
    """The N1-G1 proof. Under a fraction defect inside the classifier, the old
    expected-value path sees nothing, and the sweeps' comparison sees nothing,
    so only the independent reference can report it."""

    _name, install, _layer = _control("classifier_fraction_shared")
    restore = install()
    try:
        assert _classify_expected_mismatches() == []
        rule = get_varga_rule(45, "parashara")
        for longitude in (0.1, 75.3, 200.7, 359.9):
            result = classify(longitude, rule)
            assert (result.d_sign, result.division_index) == validator.reference_d45(longitude)
        mismatches = validator.verify_composition()
    finally:
        restore()
    assert mismatches
    assert all("fraction=" in item and "[attribution: classification]" in item for item in mismatches)


def test_sign_defect_is_also_invisible_to_the_old_path():
    _name, install, _layer = _control("classifier_sign_shared")
    restore = install()
    try:
        assert _classify_expected_mismatches() == []
        assert validator.verify_composition()
    finally:
        restore()


def test_validator_main_fails_when_a_control_goes_undetected(monkeypatch, capsys):
    inert = ("inert_control", lambda: (lambda: None), "composition")
    monkeypatch.setattr(validator, "_MUTATION_CONTROLS", (*validator._MUTATION_CONTROLS, inert))
    assert validator.main() == 1
    output = capsys.readouterr().out
    assert "inert_control" in output and "MISSED (BAD)" in output
    assert "D45 COMPOSITION MUTATION DETECTION PASSED" not in output


def test_validator_main_fails_on_a_misattributed_control(monkeypatch, capsys):
    name, install, _layer = _control("planet_cross_wiring")
    monkeypatch.setattr(validator, "_MUTATION_CONTROLS", ((name, install, "classification"),))
    assert validator.main() == 1
    assert "D45 COMPOSITION MUTATION DETECTION PASSED" not in capsys.readouterr().out


# ------------------------------------------------------------------ the real Gate I

#: Run in the validator's child process, before its script starts.
_CORRUPTIONS = {
    "none": "",
    "builder_cross_wiring": """
import importlib.util
spec = importlib.util.spec_from_file_location("site_validator", ROOT + "/validate_d45_holdout.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
import engine.astrology.varga_chart_builder as builder
builder.build_varga_chart = module._corrupt_build_varga_chart_cross_wiring()[1]
""",
    "classifier_fraction": """
import dataclasses
import engine.astrology
import engine.astrology.varga_classifier as classifier
real = classifier._classify_cyclic
classifier._classify_cyclic = lambda s, d, r: dataclasses.replace(real(s, d, r), fraction=real(s, d, r).fraction / 2.0)
""",
    "classifier_sign": """
import dataclasses
import engine.astrology
import engine.astrology.varga_classifier as classifier
real = classifier._classify_cyclic
classifier._classify_cyclic = lambda s, d, r: dataclasses.replace(real(s, d, r), d_sign=(real(s, d, r).d_sign + 1) % 12)
""",
    "builder_fraction_only": """
import dataclasses
import engine.astrology
import engine.astrology.varga_chart_builder as builder
real = builder.build_varga_chart
def corrupted(snapshot, division, rule, school):
    chart = real(snapshot, division, rule, school)
    return dataclasses.replace(chart, ascendant=dataclasses.replace(chart.ascendant, fraction=1.0 - chart.ascendant.fraction))
builder.build_varga_chart = corrupted
""",
}


def _child_environment(tmp_path, monkeypatch, corruption, extra_path=None):
    """Make every child Python start with `corruption` applied, in memory."""

    site = tmp_path / "site"
    site.mkdir()
    code = f"import sys\nROOT = {str(ROOT)!r}\nsys.path.insert(0, ROOT)\n{_CORRUPTIONS[corruption]}"
    (site / "sitecustomize.py").write_text(code, encoding="utf-8")
    entries = [str(site)] + ([str(extra_path)] if extra_path else [])
    monkeypatch.setenv("PYTHONPATH", os.pathsep.join(entries))
    monkeypatch.setenv("PYTHONDONTWRITEBYTECODE", "1")


def _gate_i_must_fail(capsys) -> str:
    """Call the real gate. Only its real fail() can end it with exit code 3."""

    with pytest.raises(SystemExit) as raised:
        certifier.gate_i_composition_verification()
    assert raised.value.code == 3
    output = capsys.readouterr().out
    assert "D45 CERTIFICATION FAIL: composition verification failed" in output
    return output


def test_gate_i_passes_on_pristine_code(tmp_path, monkeypatch):
    _child_environment(tmp_path, monkeypatch, "none")
    result = certifier.gate_i_composition_verification()
    assert result["result"] == "PASS"


def test_gate_i_fails_on_builder_cross_wiring(tmp_path, monkeypatch, capsys):
    _child_environment(tmp_path, monkeypatch, "builder_cross_wiring")
    output = _gate_i_must_fail(capsys)
    assert "RESULT: D45 COMPOSITION VERIFICATION FAILED" in output
    assert "ATTRIBUTION: ['composition']" in output
    assert "ALL INDEPENDENT D45 CASES PASSED" in output


def test_gate_i_fails_on_a_builder_only_ascendant_fraction_defect(tmp_path, monkeypatch, capsys):
    _child_environment(tmp_path, monkeypatch, "builder_fraction_only")
    output = _gate_i_must_fail(capsys)
    assert "ATTRIBUTION: ['composition']" in output


def test_gate_i_fails_on_the_n1_g1_discriminator(tmp_path, monkeypatch, capsys):
    """The sweep compares no fraction and passes; only composition can fail."""

    _child_environment(tmp_path, monkeypatch, "classifier_fraction")
    output = _gate_i_must_fail(capsys)
    assert "ALL INDEPENDENT D45 CASES PASSED" in output
    assert "RESULT: D45 COMPOSITION VERIFICATION FAILED" in output
    assert "ATTRIBUTION: ['classification']" in output
    assert "NOT RUN" in output


def test_gate_i_attributes_a_classifier_sign_defect_to_classification(tmp_path, monkeypatch, capsys):
    _child_environment(tmp_path, monkeypatch, "classifier_sign")
    output = _gate_i_must_fail(capsys)
    assert "RESULT: FAIL" in output
    assert "ALL INDEPENDENT D45 CASES PASSED" not in output
    assert "ATTRIBUTION: ['classification']" in output


def _validator_copy(tmp_path, monkeypatch, old, new):
    """A temporary, edited validator that the real gate will run. The edit must
    apply exactly once, so a stale control cannot pass by editing nothing."""

    source = VALIDATOR_PATH.read_text(encoding="utf-8")
    assert source.count(old) == 1, old
    copy_root = tmp_path / "copy"
    copy_root.mkdir()
    shutil.copy2(VALIDATOR_PATH, copy_root / VALIDATOR_PATH.name)
    (copy_root / VALIDATOR_PATH.name).write_text(source.replace(old, new), encoding="utf-8")
    monkeypatch.setattr(certifier, "ROOT", copy_root)
    _child_environment(tmp_path, monkeypatch, "none", extra_path=ROOT)


REVERT_TO_CLASSIFY = """        sign, index, fraction = reference_d45_position(source_longitude)
"""
REVERTED = """        _expected = classify(source_longitude, get_varga_rule(45, "parashara"))
        sign, index, fraction = _expected.d_sign, _expected.division_index, _expected.fraction
"""


def test_gate_i_fails_if_independence_is_reverted(tmp_path, monkeypatch, capsys):
    """Reinstating the old expected-value path makes the discriminator go
    undetected, which the real gate must refuse."""

    _validator_copy(tmp_path, monkeypatch, REVERT_TO_CLASSIFY, REVERTED)
    output = _gate_i_must_fail(capsys)
    assert "MISSED (BAD)" in output
    assert "RESULT: D45 COMPOSITION MUTATION SELF-CHECK FAILED" in output
    assert "RESULT: D45 COMPOSITION VERIFICATION PASSED" in output


def test_gate_i_fails_without_its_sentinel_despite_a_zero_return_code(tmp_path, monkeypatch, capsys):
    _validator_copy(tmp_path, monkeypatch,
                    'print("RESULT: D45 COMPOSITION MUTATION DETECTION PASSED")', 'print("RESULT: DONE")')
    output = _gate_i_must_fail(capsys)
    assert "RESULT: DONE" in output


def test_gate_i_failure_is_the_certifiers_real_process_exit(tmp_path):
    """A real certifier process, calling only Gate I, must exit 3 from fail()."""

    site = tmp_path / "site"
    site.mkdir()
    (site / "sitecustomize.py").write_text(
        f"import sys\nROOT = {str(ROOT)!r}\nsys.path.insert(0, ROOT)\n{_CORRUPTIONS['builder_cross_wiring']}",
        encoding="utf-8")
    driver = ("import importlib.util, sys\n"
              f"spec = importlib.util.spec_from_file_location('certify_d45_run', {str(ROOT / 'scripts' / 'certify_d45.py')!r})\n"
              "module = importlib.util.module_from_spec(spec)\n"
              "spec.loader.exec_module(module)\n"
              "module.gate_i_composition_verification()\n"
              "print('GATE I DID NOT FAIL')\n")
    environment = dict(os.environ, PYTHONPATH=str(site), PYTHONDONTWRITEBYTECODE="1")
    result = subprocess.run([sys.executable, "-c", driver], capture_output=True, text=True, env=environment)
    assert result.returncode == 3, result.stdout + result.stderr
    assert "D45 CERTIFICATION FAIL:" in result.stdout
    assert "GATE I DID NOT FAIL" not in result.stdout


def test_gate_i_result_is_unchanged_so_no_artifact_regeneration_is_needed():
    """Gate I's returned record is stored in the certification artifact. Anything
    that changes it needs regeneration, so this pins it to the stored text."""

    stored = json.loads((ROOT / "certification" / "VARGA_D45_V1_certification.json").read_text(encoding="utf-8"))
    recorded = {key: value for key, value in stored["gates"]["I_composition_verification"].items() if key != "exercises"}
    assert certifier.gate_i_composition_verification() == recorded
