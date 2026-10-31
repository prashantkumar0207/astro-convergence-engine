"""Fail-closed state-machine tests C1-C13 (R1 s6.6 and s6.6.1, CEO Amendment A).

Every experiment runs the real harness against a disposable fixture repository in a
temporary directory. Faults are injected only through the harness's test-only fault
points, which the harness refuses outside the system temporary directory.
"""

import ast
import itertools
import json
import marshal
import os
import signal
import struct
import subprocess
import sys
import time
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
HARNESS_DIR = HERE.parent
for entry in (str(HERE), str(HARNESS_DIR)):
    if entry not in sys.path:
        sys.path.insert(0, entry)

import harness  # noqa: E402
import helpers  # noqa: E402
import pyenv  # noqa: E402
from fixtures import fixture_repo, legacy_wpn1  # noqa: E402

FIVE_SECONDS_NS = 5_000_000_000


class Lab:
    """Test bench. `hm` is the harness module under test: the real one, or a source-level
    mutant loaded by test_harness_mutant_is_killed."""

    def __init__(self, tmp, hm=harness):
        self.hm = hm
        self.tmp = Path(tmp)
        self.evidence = self.tmp / "evidence"
        self.quarantine = self.tmp / "quarantine"
        self.control = self.tmp / "fault-control"
        for path in (self.evidence, self.quarantine, self.control):
            path.mkdir()
        self.fault_file = self.control / "FAULT"
        self.count = 0

    def repo(self):
        self.count += 1
        return fixture_repo.make_fixture_repo(self.tmp / f"repo-{self.count}")

    def runner(self, faults=None, base_extra=None, roots=None):
        base = helpers.base_env()
        base["FIXTURE_FAULT_FILE"] = str(self.fault_file)
        base.update(base_extra or {})
        return self.hm.Runner(self.hm.HarnessConfig(
            python=helpers.PYTHON, base_env=base, evidence_root=str(self.evidence),
            quarantine_dir=str(self.quarantine), authorized_roots=roots or [str(self.tmp)],
            hook_sha256=pyenv.verify_hook(), allow_test_faults=bool(faults), faults=faults or {}))

    def spec(self, repo, kind="swap", run_id=None, timeout=60.0):
        self.count += 1
        return fixture_repo.build_spec(self.hm, repo, run_id or f"run-{self.count}", helpers.PYTHON,
                                       kind=kind, timeout=timeout)

    def run(self, kind="swap", faults=None, base_extra=None, repo=None, timeout=60.0):
        repo = repo or self.repo()
        spec = self.spec(repo, kind, timeout=timeout)
        result = self.runner(faults, base_extra).run_experiment(spec)
        check_invariants(result, self)
        return result, spec, repo


@pytest.fixture
def lab(tmp_path):
    return Lab(tmp_path)


def journal(result):
    lines = Path(result["evidence_dir"], "journal.jsonl").read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines]


def check_invariants(result, lab):
    """Properties that must hold for EVERY experiment result."""

    records = journal(result)
    assert [r["seq"] for r in records] == list(range(1, len(records) + 1)), "journal has gaps"
    if result["experiment_validity"] == harness.VALID:
        assert result["outcome"] != harness.VOID
        assert result["restoration_status"] in (harness.RESTORED_VERIFIED, harness.NOT_APPLICABLE)
        assert result["attestation_ok"] is True and result["evidence_complete"] is True
        assert records[-1]["action"] == "FINAL"
        assert result["batch_action"] == harness.CONTINUE
    else:
        assert result["batch_action"] == harness.HALT
        assert result["cleanup_eligible"] is False
    if result["restoration_status"] == harness.INDETERMINATE:
        assert result["experiment_validity"] == harness.INVALID
    if result["mutation_applied"] and result["restoration_status"] != harness.RESTORED_VERIFIED:
        assert result["quarantined"] is True
        assert (lab.quarantine / f"{result['run_id']}.json").exists()
    # WP-RD-B-F1 consumer contract: the persisted result is authoritative only when
    # validate_run_evidence() reports COMPLETE, and then it must equal the returned result.
    status = harness.validate_run_evidence(result["evidence_dir"])
    if result.get("evidence_complete"):
        assert status["complete"] and status["state"] == "COMPLETE", status["reasons"]
        assert status["result"] == result
        on_disk = json.loads(Path(result["evidence_dir"], "result.json").read_text())
        for key in ("outcome", "restoration_status", "experiment_validity", "batch_action"):
            assert on_disk[key] == result[key]
        assert records[-1]["result_sha256"] == pyenv.sha256_file(Path(result["evidence_dir"], "result.json"))
    else:
        assert not status["complete"]


def triple(result):
    return result["outcome"], result["restoration_status"], result["experiment_validity"], result["batch_action"]


def no_bytecode_in(repo):
    return [str(p) for p in Path(repo).rglob("*") if p.name == "__pycache__" or p.suffix == ".pyc"]


# ------------------------------------------------------------------ C1 - C3

def test_C1_detected_and_restored_is_valid(lab):
    result, _, repo = lab.run("swap")
    assert triple(result) == (harness.DETECTED, harness.RESTORED_VERIFIED, harness.VALID, harness.CONTINUE)
    assert result["cleanup_eligible"] and result["cleanup_status"] == "ELIGIBLE-RETAINED-BY-POLICY"
    assert set(result["s8_checks"].values()) == {harness.CHECK_OK}
    assert result["target_sha256"]["final"] == result["target_sha256"]["baseline"]
    assert result["observations"]["designated_gate_j"]["returncode"] == 3
    assert no_bytecode_in(repo) == []
    assert not result["quarantined"]


def test_C1b_undetected_and_restored_is_valid(lab):
    result, _, _ = lab.run("unused")
    assert triple(result) == (harness.UNDETECTED, harness.RESTORED_VERIFIED, harness.VALID, harness.CONTINUE)


def test_C2_equivalent_is_never_applied(lab):
    result, _, _ = lab.run("equivalent")
    assert triple(result) == (harness.EQUIVALENT, harness.NOT_APPLICABLE, harness.VALID, harness.CONTINUE)
    assert result["mutation_applied"] is False
    assert result["target_sha256"]["final"] == result["target_sha256"]["baseline"]
    assert not any(r["state"] == "S5" for r in journal(result))


def test_C2b_precheck_failure_is_void_and_halts(lab):
    result, _, _ = lab.run("broken-precheck")
    assert triple(result) == (harness.VOID, harness.NOT_APPLICABLE, harness.INVALID, harness.HALT)
    assert result["mutation_applied"] is False


def test_C3_dirty_baseline_is_void_and_halts(lab):
    result, _, _ = lab.run("swap", base_extra={"FIXTURE_FORCE_FAIL": "1"})
    assert triple(result) == (harness.VOID, harness.NOT_APPLICABLE, harness.INVALID, harness.HALT)
    assert result["mutation_applied"] is False
    assert any("S2 baseline end_to_end" in f for f in result["failures"])


# ------------------------------------------------------------------ C4 - C6

def test_C4_corrupt_backup_is_indeterminate_and_nothing_is_written(lab):
    def corrupt_backup(ctx):
        data = bytearray(ctx.backup_path.read_bytes())
        data[0] ^= 0xFF
        ctx.backup_path.write_bytes(bytes(data))

    result, _, _ = lab.run("swap", faults={"after_backup": corrupt_backup})
    assert triple(result) == (harness.DETECTED, harness.INDETERMINATE, harness.INVALID, harness.HALT)
    assert result["target_sha256"]["final"] == result["target_sha256"]["mutated"]   # no write
    assert result["s8_checks"] == {}


def test_C5_unknown_restored_bytes_are_indeterminate_T10(lab):
    """Amendment A: restored bytes matching neither registered hash -> INDETERMINATE."""

    def wrong_bytes(ctx):
        data = ctx.target_path.read_bytes()
        ctx.target_path.write_bytes(data.replace(b"alpha", b"gamma"))           # same length, unknown

    result, _, _ = lab.run("swap", faults={"after_restore": wrong_bytes})
    assert triple(result) == (harness.DETECTED, harness.INDETERMINATE, harness.INVALID, harness.HALT)
    assert result["s8_checks"]["a_hash"] == harness.CHECK_INDETERMINATE
    assert all(result["s8_checks"][k] == harness.CHECK_NOT_RUN
               for k in ("b_status", "c_designated", "d_end_to_end", "e_final_hash", "f_final_status"))
    assert result["target_sha256"]["final"] not in (result["target_sha256"]["baseline"],
                                                    result["target_sha256"]["mutated"])
    assert result["quarantined"]


def test_C6_collateral_change_is_restoration_failed_T5(lab):
    def stray(ctx):
        (ctx.worktree / "pkg" / "extra.py").write_text("x = 1\n")

    result, _, _ = lab.run("swap", faults={"during_s6": stray})
    assert triple(result) == (harness.DETECTED, harness.RESTORATION_FAILED, harness.INVALID, harness.HALT)
    assert result["s8_checks"]["b_status"] == harness.CHECK_FAILED
    assert result["s8_checks"]["a_hash"] == harness.CHECK_OK


# ------------------------------------------------------------------ C7a - C7d

def _force_same_second(ctx):
    """Give the mutated and the restored source the SAME distinct mtime (forced, not raced)."""

    stat = ctx.target_path.stat()
    forced = stat.st_mtime_ns + FIVE_SECONDS_NS
    ctx.forced_mtime_ns = forced
    os.utime(ctx.target_path, ns=(forced, forced))


def test_C7a_legacy_method_reproduces_stale_bytecode(lab):
    repo = lab.repo()
    spec = lab.spec(repo, "swap")
    edit = spec.edits[0]
    legacy_wpn1.ENV = helpers.default_env()                                    # default bytecode mode
    target = repo / "pkg" / "target.py"
    baseline_run = legacy_wpn1.sh([helpers.PYTHON, "fake_certifier.py"], repo)  # legacy baseline
    assert baseline_run["rc"] == 0
    forced = {}

    def after_mutated():
        mtime = target.stat().st_mtime_ns + FIVE_SECONDS_NS                     # distinct second
        forced["ns"] = mtime
        os.utime(target, ns=(mtime, mtime))

    def after_restore():
        os.utime(target, ns=(forced["ns"], forced["ns"]))                        # same second as mutated

    gate_code = spec.designated.argv[2]
    res = legacy_wpn1.legacy_sequence(
        repo, helpers.PYTHON, [("pkg/target.py", edit.line, edit.old, edit.new)], gate_code,
        "fake_certifier.py", "fake_validator.py", fixture_repo.FAIL_PREFIX, spec.validator_expect,
        after_mutated=after_mutated, after_restore=after_restore)
    assert res["outcome"] == "DETECTED"
    assert res["restored_hash_matches"] is True
    assert res["restoration_ok"] is False                                       # the WP-N1 S2 defect
    assert res["batch_halts"] is False                                          # legacy L336: no halt
    assert "house_number=10 expected=4" in res["restored_gate_alone"]["stdout"]  # mutated signature
    # Read-only inspection of the fixture cache (the 7.1.1 method): header valid, code mutated.
    pyc = next((repo / "pkg" / "__pycache__").glob("target.*.pyc")).read_bytes()
    flags, header_mtime, header_size = struct.unpack("<III", pyc[4:16])
    source_stat = target.stat()
    assert flags == 0 and header_mtime == int(source_stat.st_mtime) and header_size == source_stat.st_size
    cached = pyenv.find_code(marshal.loads(pyc[16:]), "house")
    mutated_text = target.read_bytes().replace(edit.old.encode(), edit.new.encode())
    assert pyenv.code_digest(cached) == pyenv.expected_digest(mutated_text, "house")
    assert pyenv.code_digest(cached) != pyenv.expected_digest(target.read_bytes(), "house")


def test_C7b_protocol_prevents_stale_bytecode_under_the_same_timing(lab):
    faults = {"after_mutate": _force_same_second,
              "after_restore": lambda ctx: os.utime(ctx.target_path, ns=(ctx.forced_mtime_ns,) * 2)}
    result, _, repo = lab.run("swap", faults=faults)
    assert triple(result) == (harness.DETECTED, harness.RESTORED_VERIFIED, harness.VALID, harness.CONTINUE)
    assert no_bytecode_in(repo) == []
    caches = Path(result["evidence_dir"], "cache")
    assert all(pyenv.tree_listing(d) == [] for d in caches.iterdir())
    s8_designated = [r for r in journal(result)
                     if r["state"] == "S8" and r["action"] == "result designated_gate_j"][0]
    assert len(s8_designated["attestation"]["directly_attested_children"]) == 1
    assert s8_designated["attestation"]["ok"] is True


def _write_fault(lab, content):
    def inject(ctx):
        lab.fault_file.write_text(content)
    return inject


def _assert_preserved_evidence(result, spec, lab):
    run_dir = Path(result["evidence_dir"])
    records = journal(result)
    assert records[-1]["action"] == "FINAL"                                               # (i)
    assert pyenv.sha256_file(run_dir / "backup" / "target.bin") == result["target_sha256"]["baseline"]  # (ii)
    labels = {r["label"] for r in records if r["action"].startswith("result ")}
    for label in labels:                                                                  # (iii)
        assert (run_dir / "io" / f"{label}.stdout").exists() and (run_dir / "io" / f"{label}.stderr").exists()
    assert records[-1]["result_sha256"] == pyenv.sha256_file(run_dir / "result.json")       # (iv)
    assert (lab.quarantine / f"{result['run_id']}.json").exists()                          # (v)
    assert Path(spec.worktree).exists()                                                   # (vi)
    assert result["target_sha256"]["final"] == result["target_sha256"]["baseline"]        # (vii)


def test_C7c1_injected_gate_failure_halts_batch_and_preserves_evidence(lab):
    repo_a, repo_b = lab.repo(), lab.repo()
    spec_a, spec_b = lab.spec(repo_a, "swap"), lab.spec(repo_b, "swap")
    runner = lab.runner(faults={"after_restore": _write_fault(lab, "gate")})
    results = runner.run_batch([spec_a, spec_b])
    first = results[0]
    check_invariants(first, lab)
    assert triple(first) == (harness.DETECTED, harness.RESTORATION_FAILED, harness.INVALID, harness.HALT)
    assert first["s8_checks"]["c_designated"] == harness.CHECK_FAILED
    assert results[1]["status"] == "NOT-STARTED"                                          # C12 behaviour
    _assert_preserved_evidence(first, spec_a, lab)


def test_C7c2_corrupt_child_attestation_is_restoration_failed(lab):
    def corrupt_child(ctx, phase, command, result, attest_dir):
        if phase == "S8" and command == "designated_gate_j":
            for path in attest_dir.glob("*.end.json"):
                if json.loads(path.read_text())["ppid"] == result.pid:
                    path.write_text(path.read_text()[:25])

    result, spec, _ = lab.run("swap", faults={"after_command": corrupt_child})
    assert triple(result) == (harness.DETECTED, harness.RESTORATION_FAILED, harness.INVALID, harness.HALT)
    assert result["attestation_ok"] is False
    failures = [r for r in journal(result) if r["state"] == "S8" and r["action"] == "result designated_gate_j"]
    assert any("malformed" in f for f in failures[0]["attestation"]["failures"])
    _assert_preserved_evidence(result, spec, lab)


def test_C7c3_missing_main_attestation_is_restoration_failed(lab):
    def delete_main_end(ctx, phase, command, result, attest_dir):
        if phase == "S8" and command == "end_to_end":
            (attest_dir / f"{result.pid}.end.json").unlink()

    result, spec, _ = lab.run("swap", faults={"after_command": delete_main_end})
    assert triple(result) == (harness.DETECTED, harness.RESTORATION_FAILED, harness.INVALID, harness.HALT)
    failures = [r for r in journal(result) if r["state"] == "S8" and r["action"] == "result end_to_end"]
    assert any("missing end record" in f for f in failures[0]["attestation"]["failures"])
    _assert_preserved_evidence(result, spec, lab)


def test_C7c4_injected_end_to_end_failure_is_restoration_failed(lab):
    result, spec, _ = lab.run("swap", faults={"after_restore": _write_fault(lab, "e2e")})
    assert triple(result) == (harness.DETECTED, harness.RESTORATION_FAILED, harness.INVALID, harness.HALT)
    assert result["s8_checks"]["c_designated"] == harness.CHECK_OK
    assert result["s8_checks"]["d_end_to_end"] == harness.CHECK_FAILED
    _assert_preserved_evidence(result, spec, lab)


def test_C7d_contaminated_initial_worktree_is_refused(lab):
    repo = lab.repo()
    (repo / "pkg" / "__pycache__").mkdir()
    (repo / "pkg" / "__pycache__" / "target.cpython-311.pyc").write_bytes(b"stale")
    result, _, _ = lab.run("swap", repo=repo)
    assert triple(result) == (harness.VOID, harness.NOT_APPLICABLE, harness.INVALID, harness.HALT)
    assert result["mutation_applied"] is False
    assert any("hygiene" in f for f in result["failures"])
    assert not any(r["action"].startswith("start ") for r in journal(result))   # nothing executed


# ------------------------------------------------------------------ C8 - C11

def test_C8_timeout_with_known_hash_is_restoration_failed(lab):
    result, _, _ = lab.run("swap", faults={"after_restore": _write_fault(lab, "hang")}, timeout=6.0)
    assert triple(result) == (harness.DETECTED, harness.RESTORATION_FAILED, harness.INVALID, harness.HALT)
    timed = [r for r in journal(result) if r["state"] == "S8" and r["action"] == "result designated_gate_j"]
    assert timed[0]["process"]["timed_out"] is True
    assert result["target_sha256"]["final"] == result["target_sha256"]["baseline"]


def test_C8b_timeout_with_unknown_hash_is_indeterminate(lab):
    result, _, _ = lab.run("swap", faults={"after_restore": _write_fault(lab, "hang-corrupt")}, timeout=6.0)
    assert triple(result) == (harness.DETECTED, harness.INDETERMINATE, harness.INVALID, harness.HALT)
    assert result["s8_checks"]["c_designated"] == harness.CHECK_INDETERMINATE
    assert result["s8_checks"]["d_end_to_end"] == harness.CHECK_NOT_RUN


def test_C9_interruption_during_observation_is_indeterminate(lab):
    def interrupt(ctx):
        os.kill(os.getpid(), signal.SIGTERM)
        time.sleep(5)                       # the handler raises HarnessInterrupted before this ends

    result, _, _ = lab.run("swap", faults={"during_s6": interrupt})
    assert triple(result) == (harness.VOID, harness.INDETERMINATE, harness.INVALID, harness.HALT)
    records = journal(result)
    assert any(r["state"] == "EXCEPTION" and r["action"] == "HarnessInterrupted" for r in records)
    emergency = [r for r in records if r["state"] == "EMERGENCY"][0]
    assert emergency["before"] == "mutated" and emergency["restore_action"] == "restored from backup"
    assert not any("emergency restore failed" in f for f in result["failures"])
    assert emergency["after"] == "baseline"
    assert result["target_sha256"]["final"] == result["target_sha256"]["baseline"]
    assert result["restoration_status"] == harness.INDETERMINATE      # re-hash never upgrades


def test_C10_evidence_failure_is_invalid_and_halts(lab):
    holder = {}

    def lock_evidence(ctx):
        holder["dir"] = ctx.run_dir
        os.chmod(ctx.run_dir, 0o500)

    try:
        repo = lab.repo()
        spec = lab.spec(repo, "swap")
        result = lab.runner(faults={"before_finalize": lock_evidence}).run_experiment(spec)
    finally:
        if "dir" in holder:
            os.chmod(holder["dir"], 0o700)
    assert result["evidence_complete"] is False
    assert (result["experiment_validity"], result["batch_action"]) == (harness.INVALID, harness.HALT)
    assert result["outcome"] == harness.DETECTED
    assert result["target_sha256"]["final"] == result["target_sha256"]["baseline"]
    assert not Path(result["evidence_dir"], "result.json").exists()
    assert result["quarantined"] is True


def test_C11_status_parse_error_is_indeterminate(lab):
    def malformed_runner(ctx, check):
        if check != "b_status":
            return None
        return lambda argv, capture_output=True: subprocess.CompletedProcess(argv, 0, b"1 .M broken", b"")

    result, _, _ = lab.run("swap", faults={"s8_status_runner": malformed_runner})
    assert triple(result) == (harness.DETECTED, harness.INDETERMINATE, harness.INVALID, harness.HALT)
    assert result["s8_checks"]["b_status"] == harness.CHECK_INDETERMINATE
    assert result["s8_checks"]["c_designated"] == harness.CHECK_NOT_RUN


def test_C12_primary_restoration_failure_stops_the_batch(lab):
    def wrong_bytes(ctx):
        ctx.target_path.write_bytes(ctx.target_path.read_bytes() + b"# unknown\n")

    specs = [lab.spec(lab.repo(), "swap"), lab.spec(lab.repo(), "unused"), lab.spec(lab.repo(), "swap")]
    results = lab.runner(faults={"after_restore": wrong_bytes}).run_batch(specs)
    assert results[0]["restoration_status"] == harness.INDETERMINATE
    assert [r.get("status") for r in results[1:]] == ["NOT-STARTED", "NOT-STARTED"]
    assert not Path(specs[1].worktree, "pkg", "target.py").read_text().count("return 2")


DRIVER = r"""
import json, os, sys
sys.path[:0] = [{tests!r}, {harness_dir!r}]
import harness, helpers, pyenv
from fixtures import fixture_repo
from pathlib import Path
tmp = Path({tmp!r})
out = {{"optimize": sys.flags.optimize}}
for name, faults in (("C1", {{}}), ("C5", {{"after_restore": lambda ctx: ctx.target_path.write_bytes(b"x")}})):
    (tmp / name / "ev").mkdir(parents=True); (tmp / name / "q").mkdir()
    repo = fixture_repo.make_fixture_repo(tmp / name / "repo")
    runner = harness.Runner(harness.HarnessConfig(python=sys.executable, base_env=helpers.base_env(),
        evidence_root=str(tmp / name / "ev"), quarantine_dir=str(tmp / name / "q"),
        authorized_roots=[str(tmp)], hook_sha256=pyenv.verify_hook(), allow_test_faults=bool(faults), faults=faults))
    r = runner.run_experiment(fixture_repo.build_spec(harness, repo, name, sys.executable))
    out[name] = [r["outcome"], r["restoration_status"], r["experiment_validity"], r["batch_action"]]
print(json.dumps(out))
"""


def test_C13_identical_results_under_python_O(tmp_path):
    code = DRIVER.format(tests=str(HERE), harness_dir=str(HARNESS_DIR), tmp=str(tmp_path))
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    done = subprocess.run([helpers.PYTHON, "-O", "-c", code], capture_output=True, env=env, timeout=600)
    assert done.returncode == 0, done.stderr.decode()[-2000:]
    out = json.loads(done.stdout.decode().strip().splitlines()[-1])
    assert out["optimize"] == 1
    assert out["C1"] == [harness.DETECTED, harness.RESTORED_VERIFIED, harness.VALID, harness.CONTINUE]
    assert out["C5"] == [harness.DETECTED, harness.INDETERMINATE, harness.INVALID, harness.HALT]


def test_S6_attestation_failure_voids_the_observation(lab):
    """A mutated-phase observation whose code identity cannot be attested is VOID (it may
    not have exercised the mutation); restoration is still performed and verified."""

    def delete_main_end(ctx, phase, command, result, attest_dir):
        if phase == "S6" and command == "designated_gate_j":
            (attest_dir / f"{result.pid}.end.json").unlink()

    result, _, _ = lab.run("swap", faults={"after_command": delete_main_end})
    assert triple(result) == (harness.VOID, harness.RESTORED_VERIFIED, harness.INVALID, harness.HALT)
    assert result["attestation_ok"] is False


# ------------------------------------------------------------------ pure rules and guards

def detector_truth_table(hm):
    names = ("a_hash", "b_status", "c_designated", "d_end_to_end")
    valid = []
    for combo in itertools.product((True, False), repeat=4):
        checks = {name: hm.CHECK_OK if ok else hm.CHECK_FAILED for name, ok in zip(names, combo)}
        status = hm.decide_restoration(checks)
        validity = hm.derive_validity(hm.DETECTED, status, True, True)
        if validity == hm.VALID:
            valid.append(combo)
        if not all(combo):
            assert status == hm.RESTORATION_FAILED and validity == hm.INVALID
    assert valid == [(True, True, True, True)]


def detector_dominance(hm):
    names = ("a_hash", "b_status", "c_designated", "d_end_to_end")
    states = (hm.CHECK_OK, hm.CHECK_FAILED, hm.CHECK_INDETERMINATE, hm.CHECK_NOT_RUN)
    for combo in itertools.product(states, repeat=4):
        status = hm.decide_restoration(dict(zip(names, combo)))
        if hm.CHECK_INDETERMINATE in combo:
            assert status == hm.INDETERMINATE
        elif all(state == hm.CHECK_OK for state in combo):
            assert status == hm.RESTORED_VERIFIED
        else:
            assert status == hm.RESTORATION_FAILED
    assert hm.decide_restoration({}) == hm.RESTORATION_FAILED


def detector_validity(hm):
    statuses = (hm.NOT_APPLICABLE, hm.RESTORED_VERIFIED, hm.RESTORATION_FAILED, hm.INDETERMINATE)
    for outcome, status, attested, evidence in itertools.product(
            hm.OUTCOMES, statuses, (True, False), (True, False)):
        validity = hm.derive_validity(outcome, status, attested, evidence)
        expected = (outcome != hm.VOID and status in (hm.NOT_APPLICABLE, hm.RESTORED_VERIFIED)
                    and attested and evidence)
        assert (validity == hm.VALID) == expected


def test_16_case_restoration_validity_truth_table():
    detector_truth_table(harness)


def test_indeterminate_dominates_every_combination():
    detector_dominance(harness)


def test_precedence_is_never_downgraded():
    order = [harness.RESTORED_VERIFIED, harness.RESTORATION_FAILED, harness.INDETERMINATE]
    for current, new in itertools.product(order, repeat=2):
        combined = harness.combine_restoration(current, new)
        assert harness.PRECEDENCE[combined] == max(harness.PRECEDENCE[current], harness.PRECEDENCE[new])


def test_validity_requires_every_condition():
    detector_validity(harness)


# ------------------------------------------------------------------ restoration negative controls

#: (id, defect, old snippet, new snippet, designated detector). Exact-once source mutations
#: of harness.py; the detector must FAIL against each mutant. The pristine control for each
#: lab-based detector is the identically named test above, run unmutated in the same suite.
HARNESS_MUTANTS = [
    ("HM-1", "INDETERMINATE no longer dominates",
     "    if any(state == CHECK_INDETERMINATE for state in checks.values()):\n        return INDETERMINATE\n",
     "", "dominance"),
    ("HM-2", "a check that did not run counts as passed",
     "    if all(state == CHECK_OK for state in checks.values()):\n",
     "    if all(state in (CHECK_OK, CHECK_NOT_RUN) for state in checks.values()):\n", "dominance"),
    ("HM-3", "unknown restored bytes classified RESTORATION-FAILED (violates Amendment A)",
     '"unknown": CHECK_INDETERMINATE}[state]', '"unknown": CHECK_FAILED}[state]', "C5"),
    ("HM-4", "validity ignores the restoration status",
     "            and restoration_status in (RESTORED_VERIFIED, NOT_APPLICABLE)\n",
     "            and restoration_status is not None\n", "truth_table"),
    ("HM-5", "an interruption after mutation upgrades to RESTORED-VERIFIED",
     "        # collection only; it never upgrades the status.\n"
     "        ctx.restoration = combine_restoration(ctx.restoration, INDETERMINATE)\n",
     "        # collection only; it never upgrades the status.\n"
     "        ctx.restoration = RESTORED_VERIFIED\n", "C9"),
    ("HM-6", "S8 attestation failure ignored",
     "        elif result.returncode != 0 or not report.ok:\n",
     "        elif result.returncode != 0:\n", "C7c3"),
    ("HM-7", "S6 attestation failure does not void the observation",
     "        if invalid:\n            ctx.attestation_ok = False\n",
     "        if False:\n            ctx.attestation_ok = False\n", "S6_attestation"),
    ("HM-8", "batch continues after an INVALID experiment",
     '            if result["batch_action"] == HALT:\n', "            if False:\n", "C12"),
    ("HM-9", "S7 restores from an unverified backup",
     "        if pyenv.sha256_bytes(backup) != ctx.baseline_sha256:\n", "        if False:\n", "C4"),
    ("HM-10", "S8 timeout with an unknown hash classified as failed",
     '            if self._hash_state(ctx) == "unknown":\n                ctx.s8_checks[name] = CHECK_INDETERMINATE\n',
     "            if False:\n                ctx.s8_checks[name] = CHECK_INDETERMINATE\n", "C8b"),
]

LAB_DETECTORS = {
    "C4": lambda lab: test_C4_corrupt_backup_is_indeterminate_and_nothing_is_written(lab),
    "C5": lambda lab: test_C5_unknown_restored_bytes_are_indeterminate_T10(lab),
    "C7c3": lambda lab: test_C7c3_missing_main_attestation_is_restoration_failed(lab),
    "C8b": lambda lab: test_C8b_timeout_with_unknown_hash_is_indeterminate(lab),
    "C9": lambda lab: test_C9_interruption_during_observation_is_indeterminate(lab),
    "C12": lambda lab: test_C12_primary_restoration_failure_stops_the_batch(lab),
    "S6_attestation": lambda lab: test_S6_attestation_failure_voids_the_observation(lab),
}
PURE_DETECTORS = {"dominance": detector_dominance, "truth_table": detector_truth_table,
                  "validity": detector_validity}


def load_harness_mutant(mutant_id, old, new):
    source = (HARNESS_DIR / "harness.py").read_text(encoding="utf-8")
    if source.count(old) != 1:
        raise RuntimeError(f"{mutant_id}: mutation site occurs {source.count(old)} times")
    name = "harness_mutant_" + mutant_id.replace("-", "_").lower()
    module = type(sys)(name)
    module.__file__ = str(HARNESS_DIR / "harness.py") + f" [{mutant_id}]"
    sys.modules[name] = module
    exec(compile(source.replace(old, new, 1), module.__file__, "exec", dont_inherit=True), module.__dict__)
    return module


@pytest.mark.parametrize("mutant", HARNESS_MUTANTS, ids=[m[0] for m in HARNESS_MUTANTS])
def test_harness_mutant_is_killed(mutant, tmp_path):
    mutant_id, defect, old, new, detector_name = mutant
    if detector_name in PURE_DETECTORS:
        PURE_DETECTORS[detector_name](harness)            # pristine control in-line
    module = load_harness_mutant(mutant_id, old, new)
    try:
        if detector_name in PURE_DETECTORS:
            PURE_DETECTORS[detector_name](module)
        else:
            LAB_DETECTORS[detector_name](Lab(tmp_path, hm=module))
    except AssertionError:
        return
    pytest.fail(f"{mutant_id} SURVIVED ({defect}): detector {detector_name} passed")


def test_no_assert_statements_in_harness_source():
    for name in ("harness.py", "gitstatus.py", "pyenv.py", "attest_hook/sitecustomize.py"):
        tree = ast.parse((HARNESS_DIR / name).read_text(encoding="utf-8"))
        assert not any(isinstance(node, ast.Assert) for node in ast.walk(tree)), name


def test_ace_target_is_refused_before_anything_runs(lab):
    repo = lab.repo()
    (repo / "engine" / "astrology").mkdir(parents=True)
    (repo / "engine" / "astrology" / "keep.txt").write_text("marker\n")
    fixture_repo.git(repo, "add", "-A")
    fixture_repo.git(repo, "commit", "-q", "-m", "marker")
    result, _, _ = lab.run("swap", repo=repo)
    assert triple(result) == (harness.VOID, harness.NOT_APPLICABLE, harness.INVALID, harness.HALT)
    assert any("ACE target refused" in f for f in result["failures"])
    assert not any(r["action"].startswith("start ") for r in journal(result))


def test_faults_are_refused_outside_the_temporary_directory(lab):
    with pytest.raises(harness.HarnessRefused):
        lab.runner(faults={"after_restore": lambda ctx: None}, roots=[str(lab.tmp), str(Path.home())])
    with pytest.raises(harness.HarnessRefused):
        harness.Runner(harness.HarnessConfig(
            python=helpers.PYTHON, base_env=helpers.base_env(), evidence_root=str(lab.evidence),
            quarantine_dir=str(lab.quarantine), authorized_roots=[str(lab.tmp)],
            hook_sha256=pyenv.verify_hook(), allow_test_faults=False, faults={"x": lambda **k: None}))


def test_worktree_outside_authorized_roots_is_refused(lab, tmp_path_factory):
    outside = fixture_repo.make_fixture_repo(tmp_path_factory.mktemp("elsewhere") / "repo")
    spec = lab.spec(outside, "swap")
    result = lab.runner().run_experiment(spec)
    assert triple(result) == (harness.VOID, harness.NOT_APPLICABLE, harness.INVALID, harness.HALT)
    assert any("outside every authorized root" in f for f in result["failures"])


def test_symlinked_target_is_refused(lab):
    repo = lab.repo()
    real = repo / "pkg" / "target.py"
    (repo / "pkg" / "real_target.py").write_bytes(real.read_bytes())
    real.unlink()
    real.symlink_to("real_target.py")
    fixture_repo.git(repo, "add", "-A")
    fixture_repo.git(repo, "commit", "-q", "-m", "symlink")
    result, _, _ = lab.run("swap", repo=repo)
    assert triple(result) == (harness.VOID, harness.NOT_APPLICABLE, harness.INVALID, harness.HALT)
    assert any("symlink" in f for f in result["failures"])


def test_protocol_defeating_base_environment_is_refused(lab):
    with pytest.raises(pyenv.EnvironmentRefused):
        lab.runner(base_extra={"PYTHONPATH": "/tmp"})
