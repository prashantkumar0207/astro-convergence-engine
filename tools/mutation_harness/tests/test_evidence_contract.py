"""WP-RD-B-F2: evidence completeness and verdict consistency of validate_run_evidence().

F2-01 .. F2-24 validate the ACTUAL consumer against evidence produced by the REAL harness on
disposable fixture repositories.

Hash-consistent tampering: `rebind()` alters evidence and then recomputes the candidate
result, the journal-prefix binding and the FINAL record, so that superficial hash checks still
pass. A test using it can only pass if the semantic check itself rejects the evidence.

COMPLETE does not mean the experiment succeeded: a correctly documented INVALID experiment is
complete historical evidence. These hashes are self-contained, so they demonstrate structural
completeness and consistency, not authenticity against someone who can rewrite every artifact.
"""

import json
import os
import shutil
import signal
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
import pyenv  # noqa: E402
from fixtures import fixture_repo  # noqa: E402
from test_state_machine import Lab, load_harness_mutant  # noqa: E402

STATES = {"COMPLETE", "PENDING", "FAILED", "INCOMPLETE"}


# ------------------------------------------------------------------ genuine evidence corpus

class Corpus:
    """Genuine evidence directories from real harness runs, built once per session."""

    def __init__(self, factory):
        self.factory = factory
        self.built = {}

    def _lab(self, kind):
        return Lab(self.factory.mktemp(f"corpus-{kind}"))

    def _run(self, lab, spec_kind, faults=None, base_extra=None, repo=None):
        repo = repo or lab.repo()
        return lab.runner(faults, base_extra).run_experiment(lab.spec(repo, spec_kind))

    def _build(self, kind):
        lab = self._lab(kind)
        if kind == "detected":
            return self._run(lab, "swap")
        if kind == "undetected":
            return self._run(lab, "unused")
        if kind == "equivalent":
            return self._run(lab, "equivalent")
        if kind == "void_baseline":
            return self._run(lab, "swap", base_extra={"FIXTURE_FORCE_FAIL": "1"})
        if kind == "void_precheck":
            return self._run(lab, "broken-precheck")
        if kind == "refused":
            repo = lab.repo()
            (repo / "engine" / "astrology").mkdir(parents=True)
            (repo / "engine" / "astrology" / "keep.txt").write_text("marker\n")
            fixture_repo.git(repo, "add", "-A")
            fixture_repo.git(repo, "commit", "-q", "-m", "marker")
            return self._run(lab, "swap", repo=repo)
        if kind == "hygiene":
            repo = lab.repo()
            (repo / "pkg" / "__pycache__").mkdir()
            (repo / "pkg" / "__pycache__" / "target.cpython-311.pyc").write_bytes(b"stale")
            return self._run(lab, "swap", repo=repo)
        if kind == "restoration_failed":
            return self._run(lab, "swap", {"after_restore": lambda ctx: lab.fault_file.write_text("gate")})
        if kind == "restoration_failed_e2e":
            return self._run(lab, "swap", {"after_restore": lambda ctx: lab.fault_file.write_text("e2e")})
        if kind == "attestation_failed":
            def delete_main_end(ctx, phase, command, result, attest_dir):
                if phase == "S8" and command == "end_to_end":
                    (attest_dir / f"{result.pid}.end.json").unlink()
            return self._run(lab, "swap", {"after_command": delete_main_end})
        if kind == "s6_attestation":
            def delete_gate_end(ctx, phase, command, result, attest_dir):
                if phase == "S6" and command == "designated_gate_j":
                    (attest_dir / f"{result.pid}.end.json").unlink()
            return self._run(lab, "swap", {"after_command": delete_gate_end})
        if kind == "unknown_hash":
            return self._run(lab, "swap", {"after_restore": lambda ctx: ctx.target_path.write_bytes(
                ctx.target_path.read_bytes().replace(b"alpha", b"gamma"))})
        if kind == "backup_corrupt":
            def corrupt(ctx):
                data = bytearray(ctx.backup_path.read_bytes())
                data[0] ^= 0xFF
                ctx.backup_path.write_bytes(bytes(data))
            return self._run(lab, "swap", {"after_backup": corrupt})
        if kind == "interrupted":
            def interrupt(ctx):
                os.kill(os.getpid(), signal.SIGTERM)
                time.sleep(5)
            return self._run(lab, "swap", {"during_s6": interrupt})
        if kind == "aborted":
            def abort(ctx, phase, command, result, attest_dir):
                if phase == "S3":
                    raise RuntimeError("injected before any mutation")
            return self._run(lab, "swap", {"after_command": abort})
        raise KeyError(kind)

    def result(self, kind):
        if kind not in self.built:
            self.built[kind] = self._build(kind)
        return self.built[kind]

    def copy(self, kind, tmp):
        target = Path(tmp) / f"copy-{kind}"
        shutil.copytree(self.result(kind)["evidence_dir"], target, symlinks=False)
        return target


@pytest.fixture(scope="session")
def corpus(tmp_path_factory):
    return Corpus(tmp_path_factory)


# ------------------------------------------------------------------ evidence manipulation

def read_records(run_dir):
    return [json.loads(line) for line in Path(run_dir, "journal.jsonl").read_text().splitlines() if line]


def dump_records(records):
    return "".join(json.dumps(record, sort_keys=True) + "\n" for record in records).encode("utf-8")


def replace_file(path, data):
    path = Path(path)
    if path.exists():
        path.unlink()
    path.write_bytes(data)


def rebind(run_dir, result_edit=None, body_edit=None, final_override=None, renumber=True, pre_bytes=None):
    """Tamper hash-consistently: edit the journal body and/or result, then recompute every
    superficial binding (S1 hash, journal prefix, candidate, pending copy, FINAL)."""

    run_dir = Path(run_dir)
    records = read_records(run_dir)
    final = dict(records[-1])
    body = records[:-1]
    if pre_bytes is not None:
        replace_file(run_dir / "pre.json", pre_bytes)
        for record in body:
            if record.get("action") == "preregistered":
                record["pre_json_sha256"] = pyenv.sha256_bytes(pre_bytes)
    if body_edit is not None:
        body = body_edit(body)
    if renumber:
        body = [dict(record, seq=index + 1) for index, record in enumerate(body)]
        final["seq"] = len(body) + 1
    result = json.loads(Path(run_dir, "result.json").read_text())
    if result_edit is not None:
        result_edit(result)
    binding = result.get("evidence_binding")
    if isinstance(binding, dict):
        binding["journal_prefix_sha256"] = pyenv.sha256_bytes(dump_records(body))
        if pre_bytes is not None:
            binding["pre_json_sha256"] = pyenv.sha256_bytes(pre_bytes)
    data = json.dumps(result, indent=2, sort_keys=True).encode("utf-8")
    replace_file(run_dir / "result.json", data)
    replace_file(run_dir / harness.PENDING_NAME, data)
    final["candidate_sha256"] = final["result_sha256"] = pyenv.sha256_bytes(data)
    if final_override:
        final.update(final_override)
    replace_file(run_dir / "journal.jsonl", dump_records(body + [final]))
    return run_dir


def without(state, *actions):
    def edit(body):
        return [r for r in body if not (r.get("state") == state and r.get("action") in actions)]
    return edit


def claim(**fields):
    def edit(result):
        result.update(fields)
    return edit


def accepted(hm, run_dir):
    status = hm.validate_run_evidence(run_dir)
    assert status["state"] == "COMPLETE" and status["complete"] is True, status["reasons"]
    assert status["reasons"] == []
    return status


def rejected(hm, run_dir, needle=None):
    status = hm.validate_run_evidence(run_dir)
    assert status["state"] in STATES and status["state"] != "COMPLETE", status
    assert status["complete"] is False and status["result"] is None
    assert status["reasons"], "a rejection must carry a diagnostic reason"
    if needle is not None:
        assert any(needle in reason for reason in status["reasons"]), status["reasons"]
    return status


def s8_result(body, command):
    return next(r for r in body if r["state"] == "S8" and r["action"] == f"result {command}")


def result_label(run_dir, state, command):
    return next(r for r in read_records(run_dir) if r["state"] == state and r["action"] == f"result {command}")["label"]


# ------------------------------------------------------------------ F2-01 .. F2-24

def detector_F2_01(hm, corpus, tmp):
    status = accepted(hm, corpus.copy("detected", tmp))
    assert status["result"]["outcome"] == "DETECTED" and status["result"]["experiment_validity"] == "VALID"
    assert status["path"] == "MUTATION_EXPERIMENT" and status["experiment_verified"] is True
    assert status["properties"] == {"publication_integrity": True, "evidence_completeness": True,
                                    "verdict_consistency": True}


def detector_F2_02(hm, corpus, tmp):
    run_dir = corpus.copy("detected", tmp)
    (run_dir / "pre.json").unlink()
    rejected(hm, run_dir, "pre.json")


def detector_F2_03(hm, corpus, tmp):
    for name, raw in (("garbage", b"{not json"), ("truncated", b'{"run_id": "x"'), ("empty", b""),
                      ("array", b"[1, 2]"), ("number", b"7"), ("null", b"null")):
        run_dir = corpus.copy("detected", Path(tmp))
        replace_file(run_dir / "pre.json", raw)
        rejected(hm, run_dir, "pre.json")
        shutil.rmtree(run_dir)
        run_dir = corpus.copy("detected", Path(tmp))
        rebind(run_dir, pre_bytes=raw)                       # hash-consistent corruption
        rejected(hm, run_dir, "pre.json")
        shutil.rmtree(run_dir)


def _pre(run_dir):
    return json.loads(Path(run_dir, "pre.json").read_text())


def _pre_bytes(pre):
    return json.dumps(pre, indent=2, sort_keys=True).encode("utf-8")


def detector_F2_04_run_id(hm, corpus, tmp):
    run_dir = corpus.copy("detected", tmp)
    pre = _pre(run_dir)
    pre["run_id"] = "another-run"
    rebind(run_dir, pre_bytes=_pre_bytes(pre))
    rejected(hm, run_dir, "pre.json")


def detector_F2_04_registration(hm, corpus, tmp):
    run_dir = corpus.copy("detected", tmp)
    pre = _pre(run_dir)
    pre["target_sha256_mutated"] = "0" * 64
    rebind(run_dir, pre_bytes=_pre_bytes(pre))
    rejected(hm, run_dir, "pre.json")


def detector_F2_04_substitution(hm, corpus, tmp):
    """A substituted pre.json with unchanged registered fields: only the journal's S1 hash
    binding can notice it."""

    run_dir = corpus.copy("detected", tmp)
    pre = _pre(run_dir)
    pre["substituted"] = True
    replace_file(run_dir / "pre.json", _pre_bytes(pre))
    rejected(hm, run_dir, "pre.json")


def detector_F2_05(hm, corpus, tmp):
    run_dir = corpus.copy("detected", tmp)
    rebind(run_dir, body_edit=without("S2", "start validator", "result validator"))
    rejected(hm, run_dir, "execution path")


def detector_F2_05_evaluation(hm, corpus, tmp):
    run_dir = corpus.copy("detected", tmp)
    rebind(run_dir, body_edit=without("S2", "baseline evaluated"))
    rejected(hm, run_dir, "execution path")


def detector_F2_06(hm, corpus, tmp):
    """A journal holding only a fabricated, correctly bound S9 FINAL record."""

    run_dir = corpus.copy("detected", tmp)
    rebind(run_dir, body_edit=lambda body: [])
    rejected(hm, run_dir, "execution path")


def detector_F2_07_mutation(hm, corpus, tmp):
    run_dir = corpus.copy("detected", tmp)
    rebind(run_dir, body_edit=without("S5", "intent: write mutated bytes", "mutation written"))
    rejected(hm, run_dir, "execution path")


def detector_F2_07_observation(hm, corpus, tmp):
    run_dir = corpus.copy("detected", tmp)

    def drop(result):
        result["observations"].pop("gate_a_alone")

    rebind(run_dir, result_edit=drop, body_edit=without("S6", "start gate_a_alone", "result gate_a_alone"))
    rejected(hm, run_dir, "execution path")


def detector_F2_08_missing(hm, corpus, tmp):
    for action in ("e_final_hash", "a_hash", "f_final_status", "restoration decided"):
        run_dir = corpus.copy("detected", tmp)
        rebind(run_dir, body_edit=without("S8", action))
        rejected(hm, run_dir, "execution path")
        shutil.rmtree(run_dir)


def detector_F2_08_inconsistent_rc(hm, corpus, tmp):
    """Raw S8 rc says the gate failed while the result reports every check ok."""

    run_dir = corpus.copy("detected", tmp)

    def edit(body):
        s8_result(body, "designated_gate_j")["process"]["returncode"] = 3
        return body

    rebind(run_dir, body_edit=edit)
    rejected(hm, run_dir)


def detector_F2_08_inconsistent_hash(hm, corpus, tmp):
    run_dir = corpus.copy("detected", tmp)

    def edit(body):
        next(r for r in body if r["state"] == "S8" and r["action"] == "e_final_hash")["hash_state"] = "mutated"
        return body

    rebind(run_dir, body_edit=edit)
    rejected(hm, run_dir)


def detector_F2_09(hm, corpus, tmp):
    run_dir = corpus.copy("detected", tmp)
    rebind(run_dir, result_edit=claim(outcome="VOID", experiment_validity="VALID", batch_action="CONTINUE"))
    rejected(hm, run_dir)


def detector_F2_10(hm, corpus, tmp):
    run_dir = corpus.copy("detected", tmp)
    rebind(run_dir, result_edit=claim(restoration_status="INDETERMINATE", experiment_validity="VALID",
                                      batch_action="CONTINUE"))
    rejected(hm, run_dir)


def detector_F2_11(hm, corpus, tmp):
    run_dir = corpus.copy("detected", tmp)
    rebind(run_dir, result_edit=claim(restoration_status="RESTORATION-FAILED", experiment_validity="VALID",
                                      batch_action="CONTINUE"))
    rejected(hm, run_dir)


def _all_checks_ok():
    return {name: "ok" for name in ("a_hash", "b_status", "c_designated", "d_end_to_end",
                                    "e_final_hash", "f_final_status")}


def _launder_restoration(run_dir):
    """Rewrite a genuine restoration-failure run so every label claims success, including the
    journal's own decision record; only the raw S8 evidence still shows the failure."""

    def edit_body(body):
        for record in body:
            if record["state"] == "S8" and record["action"] == "restoration decided":
                record["checks"] = _all_checks_ok()
                record["status"] = "RESTORED-VERIFIED"
        return body

    rebind(run_dir, body_edit=edit_body, result_edit=claim(
        restoration_status="RESTORED-VERIFIED", experiment_validity="VALID", batch_action="CONTINUE",
        s8_checks=_all_checks_ok(), quarantined=False, cleanup_eligible=True,
        cleanup_status="ELIGIBLE-RETAINED-BY-POLICY", failures=[]))


def detector_F2_11_laundered(hm, corpus, tmp):
    """Uses the end-to-end-fault run: its attestation is fully ok, so only the restoration
    re-derivation can notice that S8's raw end-to-end rc contradicts every label."""

    run_dir = corpus.copy("restoration_failed_e2e", tmp)
    _launder_restoration(run_dir)
    rejected(hm, run_dir, "restoration")


def detector_F2_11_validity_label(hm, corpus, tmp):
    """Restoration honestly reported as failed, yet VALID/CONTINUE claimed."""

    run_dir = corpus.copy("restoration_failed_e2e", tmp)
    rebind(run_dir, result_edit=claim(experiment_validity="VALID", batch_action="CONTINUE", failures=[]))
    rejected(hm, run_dir, "validity")


def detector_F2_04_consistent_registration(hm, corpus, tmp):
    """The registered mutated hash is rewritten EVERYWHERE, consistently. Only re-deriving it
    from the retained baseline bytes and the registered edits can notice."""

    run_dir = corpus.copy("detected", tmp)
    forged = "f" * 64
    pre = _pre(run_dir)
    pre["target_sha256_mutated"] = forged

    def edit_body(body):
        for record in body:
            if record.get("action") == "initialised":
                record["mutated_sha256"] = forged
            if record.get("hash_state") == "mutated":
                record["sha256"] = forged
        return body

    def edit_result(result):
        result["target_sha256"]["mutated"] = forged

    rebind(run_dir, result_edit=edit_result, body_edit=edit_body, pre_bytes=_pre_bytes(pre))
    rejected(hm, run_dir, "mutat")


def detector_F2_12(hm, corpus, tmp):
    run_dir = corpus.copy("detected", tmp)

    def edit(result):
        result["s8_checks"]["c_designated"] = "failed"

    rebind(run_dir, result_edit=edit)
    rejected(hm, run_dir)


def detector_F2_13(hm, corpus, tmp):
    run_dir = corpus.copy("detected", tmp)
    rebind(run_dir, result_edit=claim(attestation_ok=False, experiment_validity="VALID", batch_action="CONTINUE"))
    rejected(hm, run_dir)


def detector_F2_13_raw_attestation(hm, corpus, tmp):
    """Remove a child's raw attestation record but leave the journal claiming ok: the recorded
    label must be recomputed from the raw records, not trusted."""

    run_dir = corpus.copy("detected", tmp)
    label = result_label(run_dir, "S8", "designated_gate_j")
    attest = run_dir / "attest" / label
    record = next(r for r in read_records(run_dir) if r.get("label") == label)
    child = record["attestation"]["children"][0]
    (attest / f"{child}.end.json").unlink()

    def edit(body):
        target = next(r for r in body if r.get("label") == label)
        target["attestation_files"].pop(f"{child}.end.json", None)
        return body

    rebind(run_dir, body_edit=edit)
    rejected(hm, run_dir, "attestation")


def detector_F2_14(hm, corpus, tmp):
    for token in (b"[1, 2]", b'"text"', b"7", b"true", b"null"):
        for position in ("first", "middle", "last"):
            run_dir = corpus.copy("detected", tmp)
            lines = Path(run_dir, "journal.jsonl").read_bytes().splitlines()
            index = {"first": 0, "middle": len(lines) // 2, "last": len(lines) - 1}[position]
            lines[index] = token
            replace_file(run_dir / "journal.jsonl", b"\n".join(lines) + b"\n")
            rejected(hm, run_dir, "journal")
            shutil.rmtree(run_dir)
    for token in (b"[1]", b'"x"', b"null", b"3"):
        run_dir = corpus.copy("detected", tmp)
        replace_file(run_dir / "result.json", token)
        replace_file(run_dir / harness.PENDING_NAME, token)
        rejected(hm, run_dir)
        shutil.rmtree(run_dir)


@pytest.mark.parametrize("field,value", [
    ("outcome", "MAYBE"), ("outcome", None), ("outcome", 1), ("restoration_status", "SORT-OF"),
    ("restoration_status", []), ("experiment_validity", "PROBABLY"), ("experiment_validity", True),
    ("batch_action", "PROCEED"), ("batch_action", {}), ("attestation_ok", "true"), ("attestation_ok", 1),
    ("s8_checks", "ok"), ("s8_checks", {"a_hash": "fine"}), ("mutation_applied", "yes"),
    ("target_sha256", []), ("observations", []), ("failures", "none"), ("evidence_complete", "true"),
    ("finalization", []), ("finalization", {"protocol": 1}), ("evidence_schema", "other"),
    ("evidence_binding", []), ("run_id", 7),
])
def test_F2_15_unknown_or_malformed_values(corpus, tmp_path, field, value):
    run_dir = corpus.copy("detected", tmp_path)
    rebind(run_dir, result_edit=claim(**{field: value}))
    rejected(harness, run_dir)


def _set_seq(index, value):
    def edit(body):
        body[index]["seq"] = value
        return body
    return edit


@pytest.mark.parametrize("name,edit", [
    ("gap", _set_seq(5, 99)), ("duplicate", _set_seq(5, 5)), ("string", _set_seq(5, "6")),
    ("bool", _set_seq(0, True)), ("float", _set_seq(5, 6.0)), ("zero-start", _set_seq(0, 0)),
    ("null", _set_seq(5, None)),
])
def test_F2_16_invalid_sequence_numbers(corpus, tmp_path, name, edit):
    run_dir = corpus.copy("detected", tmp_path)
    rebind(run_dir, body_edit=edit, renumber=False)
    rejected(harness, run_dir, "sequence")


def test_F2_16_duplicate_terminal_records(corpus, tmp_path):
    run_dir = corpus.copy("detected", tmp_path)
    final = read_records(run_dir)[-1]
    rebind(run_dir, body_edit=lambda body: body + [dict(final)])
    rejected(harness, run_dir, "execution path")


def _io_path(run_dir, state, command, suffix):
    return Path(run_dir) / "io" / f"{result_label(run_dir, state, command)}.{suffix}"


def detector_F2_17_stderr(hm, corpus, tmp):
    run_dir = corpus.copy("detected", tmp)
    _io_path(run_dir, "S6", "gate_a_alone", "stderr").unlink()
    rejected(hm, run_dir, "missing evidence file")


def detector_F2_17_others(hm, corpus, tmp):
    def stdout(d):
        _io_path(d, "S6", "designated_gate_j", "stdout").unlink()

    def backup(d):
        (d / "backup" / "target.bin").unlink()

    def status(d):
        next(r for r in read_records(d) if r.get("action") == "b_status")
        (d / "io" / next(r for r in read_records(d) if r.get("action") == "b_status")["status_file"]).unlink()

    def attest_record(d):
        label = result_label(d, "S8", "designated_gate_j")
        next((d / "attest" / label).glob("*.start.json")).unlink()

    def attest_dir(d):
        shutil.rmtree(d / "attest" / result_label(d, "S2", "validator"))

    def cache_dir(d):
        shutil.rmtree(d / "cache" / result_label(d, "S2", "validator"))

    for remove in (stdout, backup, status, attest_record, attest_dir, cache_dir):
        run_dir = corpus.copy("detected", tmp)
        remove(run_dir)
        rejected(hm, run_dir)
        shutil.rmtree(run_dir)


def detector_F2_18_stderr(hm, corpus, tmp):
    """A change to bytes nothing else inspects: only the recorded hash can notice it."""

    run_dir = corpus.copy("detected", tmp)
    path = _io_path(run_dir, "S6", "gate_a_alone", "stderr")
    path.write_bytes(path.read_bytes() + b"altered\n")
    rejected(hm, run_dir, "hash")


def detector_F2_18_others(hm, corpus, tmp):
    def stdout(d):
        path = _io_path(d, "S6", "designated_gate_j", "stdout")
        path.write_bytes(path.read_bytes() + b"\n")

    def backup(d):
        path = d / "backup" / "target.bin"
        path.write_bytes(path.read_bytes() + b"\n")

    def status(d):
        record = next(r for r in read_records(d) if r.get("action") == "b_status")
        path = d / "io" / record["status_file"]
        path.write_bytes(path.read_bytes() + b"? x\0")

    def attest_record(d):
        label = result_label(d, "S8", "designated_gate_j")
        path = next((d / "attest" / label).glob("*.end.json"))
        path.write_text(path.read_text() + " ")

    for alter in (stdout, backup, status, attest_record):
        run_dir = corpus.copy("detected", tmp)
        alter(run_dir)
        rejected(hm, run_dir, "hash")
        shutil.rmtree(run_dir)


def detector_F2_19(hm, corpus, tmp):
    status = accepted(hm, corpus.copy("equivalent", tmp))
    result = status["result"]
    assert result["outcome"] == "EQUIVALENT" and result["restoration_status"] == "NOT-APPLICABLE"
    assert result["experiment_validity"] == "VALID" and result["mutation_applied"] is False
    assert status["path"] == "EQUIVALENT_PRECHECK"


def test_F2_19_equivalent_requires_its_own_evidence(corpus, tmp_path):
    run_dir = corpus.copy("equivalent", tmp_path)
    rebind(run_dir, body_edit=without("S3", "pre-check evaluated"))
    rejected(harness, run_dir, "execution path")
    shutil.rmtree(run_dir)
    run_dir = corpus.copy("equivalent", tmp_path)

    def admitted_true(body):
        next(r for r in body if r["action"] == "pre-check evaluated")["admitted"] = True
        return body

    rebind(run_dir, body_edit=admitted_true)
    rejected(harness, run_dir)


def test_F2_19_detected_cannot_be_relabelled_equivalent(corpus, tmp_path):
    run_dir = corpus.copy("detected", tmp_path)
    rebind(run_dir, result_edit=claim(outcome="EQUIVALENT", restoration_status="NOT-APPLICABLE", s8_checks={},
                                      mutation_applied=False))
    rejected(harness, run_dir)


@pytest.mark.parametrize("kind,path", [
    ("void_baseline", "BASELINE_VOID"), ("void_precheck", "PRECHECK_VOID"),
    ("restoration_failed", "MUTATION_EXPERIMENT"), ("attestation_failed", "MUTATION_EXPERIMENT"),
    ("s6_attestation", "MUTATION_EXPERIMENT"), ("unknown_hash", "MUTATION_EXPERIMENT"),
    ("backup_corrupt", "RESTORE_REFUSED_BACKUP_CORRUPT"), ("interrupted", "INTERRUPTED_AFTER_MUTATION_INTENT"),
    ("aborted", "ABORTED_BEFORE_MUTATION"),
])
def test_F2_20_genuine_invalid_paths_are_complete_history(corpus, tmp_path, kind, path):
    original = corpus.result(kind)
    assert original["evidence_complete"] is True, original.get("finalization")
    status = accepted(harness, corpus.copy(kind, tmp_path))
    assert status["result"]["experiment_validity"] == "INVALID" and status["result"]["batch_action"] == "HALT"
    assert status["path"] == path and status["experiment_verified"] is False


@pytest.mark.parametrize("kind,state,action", [
    ("void_baseline", "S2", "baseline evaluated"), ("void_precheck", "S3", "pre-check failed"),
    ("backup_corrupt", "S7", "backup corrupt; restore refused"), ("interrupted", "EXCEPTION", "HarnessInterrupted"),
])
def test_F2_20_path_specific_evidence_is_required(corpus, tmp_path, kind, state, action):
    run_dir = corpus.copy(kind, tmp_path)
    rebind(run_dir, body_edit=without(state, action))
    rejected(harness, run_dir, "execution path")


def test_F2_20_void_baseline_cannot_claim_clean(corpus, tmp_path):
    run_dir = corpus.copy("void_baseline", tmp_path)

    def edit(body):
        next(r for r in body if r["action"] == "baseline evaluated")["clean"] = True
        return body

    rebind(run_dir, body_edit=edit)
    rejected(harness, run_dir)


def test_F2_20_backup_corrupt_path_with_intact_backup_is_inconsistent(corpus, tmp_path):
    run_dir = corpus.copy("backup_corrupt", tmp_path)
    good = corpus.result("detected")["target_sha256"]["baseline"]
    data = bytearray((run_dir / "backup" / "target.bin").read_bytes())
    data[0] ^= 0xFF                                           # undo the injected corruption
    assert pyenv.sha256_bytes(bytes(data)) == good
    replace_file(run_dir / "backup" / "target.bin", bytes(data))
    rejected(harness, run_dir, "backup")


@pytest.mark.parametrize("kind", ["refused", "hygiene"])
def test_F2_21_genuine_refusal_is_never_a_verified_experiment(corpus, tmp_path, kind):
    original = corpus.result(kind)
    assert original["evidence_complete"] is True, original.get("finalization")
    run_dir = corpus.copy(kind, tmp_path)
    assert not (run_dir / "pre.json").exists()
    status = accepted(harness, run_dir)
    assert status["path"] == "REFUSED_BEFORE_PREREGISTRATION"
    assert status["experiment_verified"] is False
    assert status["result"]["experiment_validity"] == "INVALID" and status["result"]["outcome"] == "VOID"


@pytest.mark.parametrize("fields", [
    {"experiment_validity": "VALID", "batch_action": "CONTINUE"},
    {"outcome": "DETECTED"},
    {"outcome": "DETECTED", "experiment_validity": "VALID", "batch_action": "CONTINUE",
     "restoration_status": "RESTORED-VERIFIED"},
    {"mutation_applied": True},
])
def test_F2_21_refusal_cannot_be_relabelled(corpus, tmp_path, fields):
    run_dir = corpus.copy("refused", tmp_path)
    rebind(run_dir, result_edit=claim(**fields))
    rejected(harness, run_dir)


def test_F2_21_refusal_path_rejects_unexpected_preregistration(corpus, tmp_path):
    run_dir = corpus.copy("refused", tmp_path)
    (run_dir / "pre.json").write_bytes(b"{}")
    rejected(harness, run_dir, "pre.json")


def detector_F2_22_pending_missing(hm, corpus, tmp):
    run_dir = corpus.copy("detected", tmp)
    (run_dir / harness.PENDING_NAME).unlink()
    rejected(hm, run_dir, "pending")


def detector_F2_22_others(hm, corpus, tmp):
    def pending_differs(d):
        replace_file(d / harness.PENDING_NAME, b"{}")

    def final_mismatch(d):
        rebind(d, final_override={"candidate_sha256": "0" * 64})

    def final_run_id(d):
        rebind(d, final_override={"run_id": "other"})

    def failure_after_final(d):
        records = read_records(d)
        records.append({"seq": len(records) + 1, "state": "S9", "action": "FINALIZATION-FAILED"})
        replace_file(d / "journal.jsonl", dump_records(records))

    def prefix_mismatch(d):
        records = read_records(d)
        records[0]["run_id"] = records[0]["run_id"]
        records[1]["note"] = "edited after finalization"
        replace_file(d / "journal.jsonl", dump_records(records))

    for alter in (pending_differs, final_mismatch, final_run_id, failure_after_final, prefix_mismatch):
        run_dir = corpus.copy("detected", tmp)
        alter(run_dir)
        rejected(hm, run_dir)
        shutil.rmtree(run_dir)


def test_F2_23_f1_publication_faults_remain_fail_closed(tmp_path):
    import test_finalization as f1
    for name in ("F1_T2", "F1_T5", "F1_T7b", "F1_T8"):
        root = tmp_path / name
        root.mkdir()
        f1.DETECTORS[name](Lab(root))


def test_F2_23_states_are_defined_for_incomplete_publication(corpus, tmp_path):
    run_dir = corpus.copy("detected", tmp_path)
    (run_dir / "result.json").unlink()
    assert harness.validate_run_evidence(run_dir)["state"] == "PENDING"
    (run_dir / harness.FAILED_NAME).write_text("{}")
    assert harness.validate_run_evidence(run_dir)["state"] == "FAILED"
    (run_dir / harness.FAILED_NAME).unlink()
    (run_dir / harness.PENDING_NAME).unlink()
    assert harness.validate_run_evidence(run_dir)["state"] == "INCOMPLETE"
    assert harness.validate_run_evidence(tmp_path / "does-not-exist")["state"] == "INCOMPLETE"


def detector_F2_24(hm, corpus, tmp):
    status = accepted(hm, corpus.copy("undetected", tmp))
    assert status["result"]["outcome"] == "UNDETECTED" and status["result"]["experiment_validity"] == "VALID"
    assert status["path"] == "MUTATION_EXPERIMENT"


def detector_outcome_relabel(hm, corpus, tmp):
    """The reported outcome must agree with the raw designated-gate observation."""

    run_dir = corpus.copy("detected", tmp)

    def edit(body):
        next(r for r in body if r["action"] == "outcome recorded")["outcome"] = "UNDETECTED"
        return body

    rebind(run_dir, body_edit=edit, result_edit=claim(outcome="UNDETECTED"))
    rejected(hm, run_dir, "outcome")


def detector_journal_prefix_binding(hm, corpus, tmp):
    """An edit of an otherwise uninspected journal field, with result and FINAL left alone."""

    run_dir = corpus.copy("detected", tmp)
    records = read_records(run_dir)
    records[0]["operator_note"] = "inserted later"
    replace_file(run_dir / "journal.jsonl", dump_records(records))
    rejected(hm, run_dir, "journal prefix")


def detector_interrupted_emergency_binding(hm, corpus, tmp):
    """The interrupted path's emergency restore must be journalled (or reported as failed) and
    must agree with the reported final hash."""

    run_dir = corpus.copy("interrupted", tmp)

    def contradict(body):
        next(r for r in body if r["state"] == "EMERGENCY")["after"] = "mutated"
        return body

    rebind(run_dir, body_edit=contradict)
    rejected(hm, run_dir, "emergency")
    shutil.rmtree(run_dir)

    run_dir = corpus.copy("interrupted", tmp)
    rebind(run_dir, body_edit=lambda body: [r for r in body
                                            if r["state"] != "EMERGENCY" and r["action"] != "mutation written"])
    rejected(hm, run_dir, "emergency")


MATRIX = {name[len("detector_"):]: fn for name, fn in list(globals().items()) if name.startswith("detector_")}


@pytest.mark.parametrize("name", sorted(MATRIX))
def test_F2_matrix(name, corpus, tmp_path):
    MATRIX[name](harness, corpus, tmp_path)


# ------------------------------------------------------------------ exhaustive sweeps

#: Interpreter-probe scratch files. They are diagnostic only and are not bound to the journal:
#: every attested command's own start record re-establishes the interpreter flags and prefix.
UNBOUND_DIAGNOSTIC_PREFIX = "preflight/"


@pytest.mark.parametrize("kind", ["detected", "undetected", "equivalent", "void_baseline", "void_precheck",
                                  "restoration_failed", "backup_corrupt", "refused", "interrupted", "aborted"])
def test_every_journal_record_is_mandatory(corpus, tmp_path, kind):
    """Hash-consistently removing ANY single journal record must be rejected."""

    base = corpus.copy(kind, tmp_path)
    records = read_records(base)
    abort_point = abort_point_index(records)
    checked = 0
    for index in range(len(records) - 1):
        if index == abort_point:
            continue  # pinned separately by test_abort_point_record_cannot_upgrade_the_run
        run_dir = tmp_path / f"drop-{index}"
        shutil.copytree(base, run_dir)
        rebind(run_dir, body_edit=lambda body, i=index: body[:i] + body[i + 1:])
        status = harness.validate_run_evidence(run_dir)
        assert not status["complete"], f"journal record {index} of {kind} is not mandatory"
        shutil.rmtree(run_dir)
        checked += 1
    assert checked >= len(records) - 2


def abort_point_index(records):
    """The record just before EXCEPTION, or None on a path that did not abort."""

    for index, record in enumerate(records):
        if record["state"] == "EXCEPTION":
            return index - 1
    return None


@pytest.mark.parametrize("kind,path", [("interrupted", "INTERRUPTED_AFTER_MUTATION_INTENT"),
                                       ("aborted", "ABORTED_BEFORE_MUTATION")])
def test_abort_point_record_cannot_upgrade_the_run(corpus, tmp_path, kind, path):
    """KNOWN LIMITATION, pinned. Removing the record just before EXCEPTION leaves a journal with the
    shape of a genuine earlier abort (a signal can arrive between any two records), so a
    self-contained consumer cannot reject it. It must stay on the abort path and never read as a
    verified experiment."""

    run_dir = corpus.copy(kind, tmp_path)
    index = abort_point_index(read_records(run_dir))
    rebind(run_dir, body_edit=lambda body: body[:index] + body[index + 1:])
    status = harness.validate_run_evidence(run_dir)
    assert status["state"] == "COMPLETE", status["reasons"]
    assert status["path"] == path
    assert status["experiment_verified"] is False
    assert status["result"]["experiment_validity"] == "INVALID"
    assert status["result"]["batch_action"] == "HALT"


@pytest.mark.parametrize("kind", ["detected", "equivalent", "restoration_failed"])
def test_every_evidence_file_is_bound(corpus, tmp_path, kind):
    """Deleting or altering ANY evidence file must be rejected (probe scratch files excepted)."""

    run_dir = corpus.copy(kind, tmp_path)
    files = [p for p in sorted(run_dir.rglob("*")) if p.is_file()]
    checked = 0
    for path in files:
        relative = path.relative_to(run_dir).as_posix()
        if relative.startswith(UNBOUND_DIAGNOSTIC_PREFIX):
            continue
        original = path.read_bytes()
        path.unlink()
        assert not harness.validate_run_evidence(run_dir)["complete"], f"deleting {relative} went unnoticed"
        path.write_bytes(original + b" ")
        assert not harness.validate_run_evidence(run_dir)["complete"], f"altering {relative} went unnoticed"
        path.unlink()
        path.write_bytes(original)
        checked += 1
    assert checked > 10
    assert harness.validate_run_evidence(run_dir)["complete"], "restoring every file must restore COMPLETE"


def test_nonempty_cache_directory_is_rejected(corpus, tmp_path):
    run_dir = corpus.copy("detected", tmp_path)
    label = result_label(run_dir, "S8", "designated_gate_j")
    (run_dir / "cache" / label / "stale.pyc").write_bytes(b"x")
    rejected(harness, run_dir, "attestation")


def test_attestation_records_cannot_be_moved_between_commands(corpus, tmp_path):
    """Swapping the raw attestation of one command with another, hash-consistently."""

    run_dir = corpus.copy("detected", tmp_path)
    first, second = result_label(run_dir, "S2", "designated_gate_j"), result_label(run_dir, "S8", "designated_gate_j")
    attest = run_dir / "attest"
    (attest / first).rename(attest / "swap")
    (attest / second).rename(attest / first)
    (attest / "swap").rename(attest / second)

    def edit(body):
        one = next(r for r in body if r.get("label") == first)
        two = next(r for r in body if r.get("label") == second)
        one["attestation_files"], two["attestation_files"] = two["attestation_files"], one["attestation_files"]
        return body

    rebind(run_dir, body_edit=edit)
    rejected(harness, run_dir, "attestation")


def test_forged_phase_label_in_raw_attestation_is_rejected(corpus, tmp_path):
    run_dir = corpus.copy("detected", tmp_path)
    label = result_label(run_dir, "S8", "designated_gate_j")
    start = next((run_dir / "attest" / label).glob("*.start.json"))
    record = json.loads(start.read_text())
    record["phase"] = "99-S8-other"
    start.write_text(json.dumps(record))

    def edit(body):
        target = next(r for r in body if r.get("label") == label)
        target["attestation_files"][start.name] = pyenv.sha256_file(start)
        return body

    rebind(run_dir, body_edit=edit)
    rejected(harness, run_dir, "another phase")


# ------------------------------------------------------------------ F2 negative controls

#: (id, requirement bypassed, old snippet, new snippet, designated detector). Exact-once source
#: mutations of harness.py. Each fixture is built so that nothing else rejects it, so a killed
#: mutant shows that this specific check is connected and is not redundant on that fixture.
F2_MUTANTS = [
    ("VM-1", "preregistration requirement removed",
     '    if not pre_path.is_file():\n'
     '        reasons.append("pre.json is missing on a path requiring preregistration")\n'
     '        return\n',
     '    if not pre_path.is_file():\n'
     '        return\n', "F2_02"),
    ("VM-2", "mandatory state-path validation bypassed",
     '    completeness.extend(path_errors)\n', '    pass\n', "F2_06"),
    ("VM-3", "restoration verdict trusted from the result instead of re-derived",
     '    expected_restoration = _recompute_restoration(facts)\n',
     '    expected_restoration = {"status": result.get("restoration_status"), "checks": result.get("s8_checks")}\n',
     "F2_11_laundered"),
    ("VM-4", "attestation trusted from the journal label instead of the raw records",
     '    attestation_ok = report.ok\n', '    attestation_ok = recorded.get("ok")\n', "F2_13_raw_attestation"),
    ("VM-5", "supporting-evidence hash not verified",
     '    if pyenv.sha256_bytes(data) != expected:\n', '    if False:\n', "F2_18_stderr"),
    ("VM-6", "missing supporting evidence tolerated",
     '    if not path.is_file():\n'
     '        reasons.append(f"missing evidence file: {what}")\n'
     '        return None\n',
     '    if not path.is_file():\n'
     '        return None\n', "F2_17_stderr"),
    ("VM-7", "preregistration hash binding ignored",
     '    if pyenv.sha256_bytes(data) != facts.preregistered.get("pre_json_sha256"):\n', '    if False:\n',
     "F2_04_substitution"),
    ("VM-8", "outcome trusted from the result instead of re-derived",
     '    expected_outcome = _recompute_outcome(facts)\n', '    expected_outcome = result.get("outcome")\n',
     "outcome_relabel"),
    ("VM-9", "journal prefix binding ignored",
     '        if isinstance(binding, dict) and binding.get("journal_prefix_sha256") != pyenv.sha256_bytes(prefix):\n',
     '        if False:\n', "journal_prefix_binding"),
    ("VM-10", "reported attestation_ok not compared with the evidence",
     '    if result.get("attestation_ok") is not expected_attestation:\n', '    if False:\n', "F2_13"),
    ("VM-11", "non-object journal records not rejected explicitly (would fall to the crash net)",
     '        if not isinstance(record, dict):\n', '        if False:\n', "F2_14"),
    ("VM-12", "pending candidate no longer required",
     '    if not pending_path.is_file():\n'
     '        reasons.append("pending candidate is missing")\n',
     '    if not pending_path.is_file():\n'
     '        pass\n', "F2_22_pending_missing"),
    ("VM-13", "reported S8 checks not compared with the evidence",
     '    elif reported_checks != expected_restoration["checks"]:\n', '    elif False:\n', "F2_12"),
    ("VM-14", "reported restoration status not compared with the evidence",
     '    if result.get("restoration_status") != expected_restoration["status"]:\n', '    if False:\n', "F2_10"),
    ("VM-15", "reported outcome not compared with the evidence",
     '    if result.get("outcome") != expected_outcome:\n', '    if False:\n', "F2_09"),
    ("VM-16", "reported validity not compared with the evidence",
     '    if result.get("experiment_validity") != expected_validity:\n', '    if False:\n', "F2_11_validity_label"),
    ("VM-17", "registered mutation not re-derived from the retained baseline",
     '    if pyenv.sha256_bytes(mutated) != facts.initialised["mutated_sha256"]:\n', '    if False:\n',
     "F2_04_consistent_registration"),
    ("VM-18", "interrupted path's emergency restore not compared with the evidence",
     '        if facts.path == PATH_INTERRUPTED:  # the producer always attempts this once a mutation is intended\n',
     '        if False:\n', "interrupted_emergency_binding"),
]


@pytest.mark.parametrize("mutant", F2_MUTANTS, ids=[m[0] for m in F2_MUTANTS])
def test_f2_mutant_is_killed(mutant, corpus, tmp_path):
    mutant_id, requirement, old, new, detector_name = mutant
    detector = MATRIX[detector_name]
    (tmp_path / "pristine").mkdir()
    (tmp_path / "mutant").mkdir()
    detector(harness, corpus, tmp_path / "pristine")    # pristine control must pass
    module = load_harness_mutant(mutant_id, old, new)
    try:
        detector(module, corpus, tmp_path / "mutant")
    except AssertionError:
        return
    pytest.fail(f"{mutant_id} SURVIVED ({requirement}): detector {detector_name} passed")


@pytest.mark.parametrize("bad", [None, [], 1, "x", {}, True])
def test_consumer_never_raises_on_malformed_result_fields(corpus, tmp_path, bad):
    fields = ("run_id", "outcome", "restoration_status", "experiment_validity", "batch_action", "s8_checks",
              "attestation_ok", "mutation_applied", "target_sha256", "observations", "failures", "quarantined",
              "evidence_complete", "finalization", "evidence_schema", "evidence_binding", "cleanup_eligible")
    base = corpus.copy("detected", tmp_path)
    original = json.loads((base / "result.json").read_text())
    for field in fields:
        if original.get(field) == bad and type(original.get(field)) is type(bad):
            continue
        run_dir = tmp_path / f"f-{field}"
        shutil.copytree(base, run_dir)
        rebind(run_dir, result_edit=claim(**{field: bad}))
        rejected(harness, run_dir)
        shutil.rmtree(run_dir)
