"""
PARASHARI_YOGA_V1 Gate J failure observation (WP-N1 N1-G2).

The validator's self-check never showed that the certifier acts on a failure.
These tests run scripts/certify_parashari_yoga.py's REAL
gate_j_composition_verification() and its REAL validator subprocess, and
observe the real fail() and exit code 3.

Corruptions exist only in memory: in a child process started through a temporary
sitecustomize, in a temporary copy of the validator, or in a certifier module
compiled from edited source text. No production source changes on disk, and no
certification artifact is written: these tests call Gate J alone, never the
certifier's main().
"""

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import types
from pathlib import Path

import pytest

import engine.parashari.mahapurusha_yoga as prod

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = ROOT / "validate_parashari_yoga_holdout.py"
CERTIFIER_PATH = ROOT / "scripts" / "certify_parashari_yoga.py"
ARTIFACT_PATH = ROOT / "certification" / "PARASHARI_YOGA_V1_certification.json"

SWEEP_SENTINEL = "ALL INDEPENDENT PARASHARI_YOGA_V1 CASES PASSED"
COMPOSITION_SENTINEL = "PARASHARI_YOGA_V1 COMPOSITION VERIFICATION PASSED"
MUTATION_SENTINEL = "PARASHARI_YOGA_V1 COMPOSITION MUTATION DETECTION PASSED"
COMPOSITION_FAILED = "RESULT: PARASHARI_YOGA_V1 COMPOSITION VERIFICATION FAILED"
FAIL_MESSAGE = "PARASHARI_YOGA_V1 CERTIFICATION FAIL: composition verification failed"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = _load(VALIDATOR_PATH, "validate_parashari_yoga_under_test")
certifier = _load(CERTIFIER_PATH, "certify_parashari_yoga_under_test")

_LOAD_VALIDATOR = """
import importlib.util
spec = importlib.util.spec_from_file_location("site_validator", ROOT + "/validate_parashari_yoga_holdout.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
"""

#: Run in the validator's child process, before its script starts. The first two
#: leave the real production function running and corrupt what its call sites do;
#: the last two install the validator's own whole-function corruptions.
CORRUPTIONS = {
    "none": ("", None),
    "call_site_argument_order": ("""
import engine.parashari.mahapurusha_yoga as prod
real = prod.whole_sign_house
prod.whole_sign_house = lambda first, second: real(second, first)
""", "house_number="),
    "call_site_sign_number": ("""
import engine.parashari.mahapurusha_yoga as prod
real = prod.zodiac_sign
prod.zodiac_sign = lambda longitude: real(longitude) % 12 + 1
""", "sign_number="),
    "function_argument_order": (_LOAD_VALIDATOR + """
import engine.parashari.mahapurusha_yoga as prod
prod.graha_mahapurusha_from_snapshot = module._corrupt_graha_mahapurusha_argument_order()[1]
""", "house_number="),
    "function_sign_number": (_LOAD_VALIDATOR + """
import engine.parashari.mahapurusha_yoga as prod
prod.graha_mahapurusha_from_snapshot = module._corrupt_graha_mahapurusha_sign_number()[1]
""", "sign_number="),
}
REAL_CORRUPTIONS = sorted(name for name in CORRUPTIONS if name != "none")


def _write_site(tmp_path, corruption) -> Path:
    site = tmp_path / "site"
    site.mkdir(exist_ok=True)
    code = f"import sys\nROOT = {str(ROOT)!r}\nsys.path.insert(0, ROOT)\n{CORRUPTIONS[corruption][0]}"
    (site / "sitecustomize.py").write_text(code, encoding="utf-8")
    return site


def _child_environment(tmp_path, monkeypatch, corruption, extra_path=None):
    """Make every child Python start with `corruption` applied, in memory."""

    entries = [str(_write_site(tmp_path, corruption))] + ([str(extra_path)] if extra_path else [])
    monkeypatch.setenv("PYTHONPATH", os.pathsep.join(entries))
    monkeypatch.setenv("PYTHONDONTWRITEBYTECODE", "1")


def _gate_j_must_fail(capsys, module=certifier) -> str:
    """Call the real gate. Only its real fail() can end it with exit code 3."""

    with pytest.raises(SystemExit) as raised:
        module.gate_j_composition_verification()
    assert raised.value.code == 3
    output = capsys.readouterr().out
    assert FAIL_MESSAGE in output
    return output


def _validator_copy(tmp_path, monkeypatch, old, new, module=certifier) -> Path:
    """A temporary, edited validator that the gate will run. The edit must apply
    exactly once, so a stale control cannot pass by editing nothing."""

    source = VALIDATOR_PATH.read_text(encoding="utf-8")
    assert source.count(old) == 1, old
    copy_root = tmp_path / "copy"
    copy_root.mkdir(exist_ok=True)
    copy_path = copy_root / VALIDATOR_PATH.name
    copy_path.write_text(source.replace(old, new), encoding="utf-8")
    monkeypatch.setattr(module, "ROOT", copy_root)
    _child_environment(tmp_path, monkeypatch, "none", extra_path=ROOT)
    return copy_path


def _run_validator(path: Path):
    return subprocess.run([sys.executable, str(path)], capture_output=True, text=True)


# ------------------------------------------------------------------ pristine

def test_validator_subprocess_passes_on_pristine_code(tmp_path, monkeypatch):
    _child_environment(tmp_path, monkeypatch, "none")
    result = _run_validator(VALIDATOR_PATH)
    assert result.returncode == 0, result.stdout + result.stderr
    for sentinel in (SWEEP_SENTINEL, COMPOSITION_SENTINEL, MUTATION_SENTINEL):
        assert sentinel in result.stdout


def test_gate_j_passes_on_pristine_code(tmp_path, monkeypatch):
    _child_environment(tmp_path, monkeypatch, "none")
    assert certifier.gate_j_composition_verification()["result"] == "PASS"


def test_gate_j_result_matches_the_stored_record():
    """Gate J's returned record is stored in the certification artifact. These tests
    must not change it, since that would need regeneration."""

    stored = json.loads(ARTIFACT_PATH.read_text(encoding="utf-8"))
    assert certifier.gate_j_composition_verification() == stored["gates"]["J_composition_verification"]


# ------------------------------------------------------------------ real corruptions

@pytest.mark.parametrize("corruption", REAL_CORRUPTIONS)
def test_gate_j_fails_on_a_real_corruption(corruption, tmp_path, monkeypatch, capsys):
    """The sweep shares no code with production and passes, so only the composition
    check can be what fails, and the self-check must not then claim success."""

    _child_environment(tmp_path, monkeypatch, corruption)
    output = _gate_j_must_fail(capsys)
    assert COMPOSITION_FAILED in output
    assert CORRUPTIONS[corruption][1] in output
    assert COMPOSITION_SENTINEL not in output
    assert MUTATION_SENTINEL not in output


@pytest.mark.parametrize("corruption", ["call_site_argument_order", "call_site_sign_number"])
def test_gate_j_failure_is_the_certifiers_real_process_exit(corruption, tmp_path):
    """A real certifier process, calling only Gate J, must exit 3 from fail(), and
    must leave the certification artifact's bytes alone."""

    before = hashlib.sha256(ARTIFACT_PATH.read_bytes()).hexdigest()
    driver = ("import importlib.util\n"
              f"spec = importlib.util.spec_from_file_location('certify_run', {str(CERTIFIER_PATH)!r})\n"
              "module = importlib.util.module_from_spec(spec)\n"
              "spec.loader.exec_module(module)\n"
              "module.gate_j_composition_verification()\n"
              "print('GATE J DID NOT FAIL')\n")
    environment = dict(os.environ, PYTHONPATH=str(_write_site(tmp_path, corruption)),
                       PYTHONDONTWRITEBYTECODE="1")
    result = subprocess.run([sys.executable, "-c", driver], capture_output=True, text=True, env=environment)
    assert result.returncode == 3, result.stdout + result.stderr
    assert FAIL_MESSAGE in result.stdout
    assert "GATE J DID NOT FAIL" not in result.stdout
    assert hashlib.sha256(ARTIFACT_PATH.read_bytes()).hexdigest() == before


# ------------------------------------------------------------------ non-equivalence

def _chart_rows():
    rows = {}
    for case in validator.INDEPENDENT_HOLDOUT:
        chart = prod.mahapurusha_yoga(validator._birth_data(case))
        for result in chart.results:
            rows[(case["id"], result.graha)] = (result.sign_number, result.house_number, result.present)
    return rows


def test_call_site_argument_swap_changes_house_but_never_present(monkeypatch):
    """Why this defect needs Gate J: the kendra set is symmetric, so the derived
    boolean that every earlier gate reads cannot see it."""

    pristine = _chart_rows()
    real = prod.whole_sign_house
    monkeypatch.setattr(prod, "whole_sign_house", lambda first, second: real(second, first))
    corrupted = _chart_rows()
    mismatches = validator.verify_composition()
    assert any(pristine[key][1] != corrupted[key][1] for key in pristine)
    assert all(pristine[key][2] == corrupted[key][2] for key in pristine)
    assert all(pristine[key][0] == corrupted[key][0] for key in pristine)
    assert mismatches and all("house_number=" in item for item in mismatches)


def test_call_site_sign_corruption_reaches_only_sign_number(monkeypatch):
    real = prod.zodiac_sign
    monkeypatch.setattr(prod, "zodiac_sign", lambda longitude: real(longitude) % 12 + 1)
    mismatches = validator.verify_composition()
    assert mismatches and all("sign_number=" in item for item in mismatches)


@pytest.mark.parametrize("factory,field", [
    ("_corrupt_graha_mahapurusha_argument_order", "house_number="),
    ("_corrupt_graha_mahapurusha_sign_number", "sign_number="),
])
def test_function_corruptions_reach_only_their_field(factory, field, monkeypatch):
    _pristine, corrupted = getattr(validator, factory)()
    monkeypatch.setattr(prod, "graha_mahapurusha_from_snapshot", corrupted)
    mismatches = validator.verify_composition()
    assert mismatches and all(field in item for item in mismatches)


# ------------------------------------------------------------------ sentinels and return code

SENTINEL_EDITS = {
    "composition": (f'print("RESULT: {COMPOSITION_SENTINEL}")', 'print("RESULT: DONE")', MUTATION_SENTINEL),
    "mutation": (f'print("RESULT: {MUTATION_SENTINEL}")', 'print("RESULT: DONE")', COMPOSITION_SENTINEL),
}
NONZERO_RETURN = ('    print("=" * 60)\n    return 0\n', '    print("=" * 60)\n    return 1\n')


@pytest.mark.parametrize("sentinel", sorted(SENTINEL_EDITS))
def test_gate_j_fails_closed_on_a_missing_sentinel(sentinel, tmp_path, monkeypatch, capsys):
    old, new, other = SENTINEL_EDITS[sentinel]
    copy_path = _validator_copy(tmp_path, monkeypatch, old, new)
    direct = _run_validator(copy_path)
    assert direct.returncode == 0, direct.stdout + direct.stderr
    assert "RESULT: DONE" in direct.stdout and other in direct.stdout
    _gate_j_must_fail(capsys)


def test_gate_j_fails_closed_on_a_nonzero_return_with_every_sentinel(tmp_path, monkeypatch, capsys):
    copy_path = _validator_copy(tmp_path, monkeypatch, *NONZERO_RETURN)
    direct = _run_validator(copy_path)
    assert direct.returncode == 1
    assert COMPOSITION_SENTINEL in direct.stdout and MUTATION_SENTINEL in direct.stdout
    _gate_j_must_fail(capsys)


# ------------------------------------------------------------------ the gate's clauses are each necessary

def _certifier_mutant(old, new):
    """The certifier compiled from edited source, in memory; nothing is written."""

    source = CERTIFIER_PATH.read_text(encoding="utf-8")
    assert source.count(old) == 1, old
    module = types.ModuleType("certify_parashari_yoga_mutant")
    module.__file__ = str(CERTIFIER_PATH)
    exec(compile(source.replace(old, new), str(CERTIFIER_PATH), "exec"), module.__dict__)  # noqa: S102
    return module


RETURN_CODE_CLAUSE = (f'result.returncode != 0\n            or "{COMPOSITION_SENTINEL}" not in result.stdout',
                      f'"{COMPOSITION_SENTINEL}" not in result.stdout')
COMPOSITION_CLAUSE = (f'\n            or "{COMPOSITION_SENTINEL}" not in result.stdout', "")
MUTATION_CLAUSE = (f'\n            or "{MUTATION_SENTINEL}" not in result.stdout', "")


@pytest.mark.parametrize("clause,edit", [
    (RETURN_CODE_CLAUSE, NONZERO_RETURN),
    (COMPOSITION_CLAUSE, SENTINEL_EDITS["composition"][:2]),
    (MUTATION_CLAUSE, SENTINEL_EDITS["mutation"][:2]),
], ids=["return_code", "composition_sentinel", "mutation_sentinel"])
def test_each_gate_clause_is_what_rejects_its_scenario(clause, edit, tmp_path, monkeypatch, capsys):
    """Remove one clause and the same bad validator is accepted. Each scenario
    therefore exercises that clause, and the fail-closed tests above cannot be
    passing for some other reason."""

    _validator_copy(tmp_path, monkeypatch, *edit)
    _gate_j_must_fail(capsys)

    mutant = _certifier_mutant(*clause)
    monkeypatch.setattr(mutant, "ROOT", certifier.ROOT)
    assert mutant.gate_j_composition_verification()["result"] == "PASS"


def test_a_gate_whose_fail_does_nothing_accepts_a_real_corruption(tmp_path, monkeypatch, capsys):
    """The detector disconnected: the same corruption now passes, so the failing
    tests above really do depend on the gate's fail() call."""

    _child_environment(tmp_path, monkeypatch, "call_site_argument_order")
    _gate_j_must_fail(capsys)

    mutant = _certifier_mutant('fail(f"composition verification failed:', 'print(f"composition verification failed:')
    assert mutant.gate_j_composition_verification()["result"] == "PASS"


# ------------------------------------------------------------------ restoration

def test_self_check_detects_every_control_and_restores_production():
    pristine = prod.graha_mahapurusha_from_snapshot
    all_detected, results = validator.run_mutation_self_check()
    assert prod.graha_mahapurusha_from_snapshot is pristine
    assert all_detected is True
    assert {result["control"]: result["detected"] for result in results} == {
        "argument_order_swap": True, "sign_number_wrong_body": True}
    assert validator.verify_composition() == []


def test_restoration_happens_when_a_control_raises(monkeypatch):
    pristine = prod.graha_mahapurusha_from_snapshot
    real_verify = validator.verify_composition
    calls = []

    def raising_verify():
        calls.append(1)
        if len(calls) == 2:
            assert prod.graha_mahapurusha_from_snapshot is not pristine
            raise RuntimeError("injected during a control")
        return real_verify()

    monkeypatch.setattr(validator, "verify_composition", raising_verify)
    with pytest.raises(RuntimeError, match="injected during a control"):
        validator.run_mutation_self_check()
    assert prod.graha_mahapurusha_from_snapshot is pristine


def test_self_check_refuses_a_failed_restoration(monkeypatch):
    pristine = prod.graha_mahapurusha_from_snapshot

    def never_restores():
        _real, corrupted = validator._corrupt_graha_mahapurusha_argument_order()
        return corrupted, corrupted

    monkeypatch.setattr(validator, "_MUTATION_CONTROLS", (("never_restores", never_restores),))
    try:
        with pytest.raises(AssertionError, match="not correctly restored"):
            validator.run_mutation_self_check()
        assert prod.graha_mahapurusha_from_snapshot is not pristine
    finally:
        prod.graha_mahapurusha_from_snapshot = pristine
    assert validator.verify_composition() == []


def test_gate_j_fails_if_a_validator_stops_restoring(tmp_path, monkeypatch, capsys):
    _validator_copy(tmp_path, monkeypatch,
                    "            prod.graha_mahapurusha_from_snapshot = pristine\n", "            pass\n")
    output = _gate_j_must_fail(capsys)
    assert "not correctly restored" in output
    assert MUTATION_SENTINEL not in output


def test_gate_j_fails_if_a_control_goes_undetected(tmp_path, monkeypatch, capsys):
    _validator_copy(tmp_path, monkeypatch, "_MUTATION_CONTROLS = (\n",
                    "def _inert():\n"
                    "    import engine.parashari.mahapurusha_yoga as prod\n"
                    "    return prod.graha_mahapurusha_from_snapshot, prod.graha_mahapurusha_from_snapshot\n\n\n"
                    '_MUTATION_CONTROLS = (\n    ("inert_control", _inert),\n')
    output = _gate_j_must_fail(capsys)
    assert "inert_control" in output and "MISSED (BAD)" in output
    assert "COMPOSITION MUTATION SELF-CHECK FAILED" in output
    assert MUTATION_SENTINEL not in output
