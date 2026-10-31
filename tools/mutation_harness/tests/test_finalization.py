"""WP-RD-B-F1: durable evidence finalization and fail-closed result publication.

F1-T1 .. F1-T10 exercise the real harness on disposable fixture repositories and check
BOTH the returned result and the persisted files. FM-1 .. FM-6 are exact-once source
mutations of harness.py that must be killed by their designated F1 detector.

F1-T1 deliberately uses only facilities that also exist in the original commit 4318b31
(Journal.append, Runner.run_batch, result.json), so it can be - and was - run against
that commit's harness.py to demonstrate that it fails there (IMPLEMENTATION_EVIDENCE.md).
"""

import contextlib
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
from test_state_machine import Lab, journal, load_harness_mutant  # noqa: E402

VALID, INVALID, CONTINUE, HALT = "VALID", "INVALID", "CONTINUE", "HALT"


@pytest.fixture
def lab(tmp_path):
    return Lab(tmp_path)


@contextlib.contextmanager
def patched(obj, name, replacement):
    original = getattr(obj, name)
    setattr(obj, name, replacement)
    try:
        yield original
    finally:
        setattr(obj, name, original)


def run_batch(lab, faults=None, kind="swap", count=2):
    specs = [lab.spec(lab.repo(), kind) for _ in range(count)]
    results = lab.runner(faults).run_batch(specs)
    return results, specs


def persisted_result(result):
    path = Path(result["evidence_dir"], "result.json")
    return json.loads(path.read_text()) if path.exists() else None


def assert_no_authoritative_valid(result):
    """Neither the returned nor ANY persisted result.json may claim VALID or CONTINUE, and
    the consumer contract must not accept the run as COMPLETE-and-VALID."""

    assert result["experiment_validity"] == INVALID and result["batch_action"] == HALT
    on_disk = persisted_result(result)
    if on_disk is not None:
        assert on_disk.get("experiment_validity") != VALID, "persisted result.json claims VALID"
        assert on_disk.get("batch_action") != CONTINUE, "persisted result.json claims CONTINUE"


def assert_consumer_rejects(lab, result):
    status = lab.hm.validate_run_evidence(result["evidence_dir"])
    assert not status["complete"] and status["result"] is None, status
    return status


def assert_evidence_preserved(result):
    run_dir = Path(result["evidence_dir"])
    assert (run_dir / "journal.jsonl").exists() and (run_dir / "pre.json").exists()
    if result["mutation_applied"]:
        assert pyenv.sha256_file(run_dir / "backup" / "target.bin") == result["target_sha256"]["baseline"]
    assert any((run_dir / "io").iterdir())


# ------------------------------------------------------------------ detectors

def detector_F1_T1(lab):
    """FINAL journal append fails. Original 4318b31: result.json already says VALID."""

    hm = lab.hm
    seen = {}
    original_append = hm.Journal.append

    def failing_append(self, state, action, *args, **kwargs):
        if action == "FINAL":
            seen["result_existed_when_final_attempted"] = (self.path.parent / "result.json").exists()
            raise OSError("injected: FINAL journal append failed")
        return original_append(self, state, action, *args, **kwargs)

    with patched(hm.Journal, "append", failing_append):
        results, _ = run_batch(lab)
    first = results[0]
    assert seen.get("result_existed_when_final_attempted") is False, \
        "an authoritative result.json existed before the FINAL record was attempted"
    assert_no_authoritative_valid(first)
    assert not Path(first["evidence_dir"], "result.json").exists()
    assert results[1].get("status") == "NOT-STARTED"
    assert first["outcome"] == "DETECTED" and first["restoration_status"] == "RESTORED-VERIFIED"
    assert_evidence_preserved(first)


def detector_F1_T2(lab):
    def fsync_fails(ctx, fd):
        raise OSError("injected: FINAL fsync failed")

    results, _ = run_batch(lab, {"final_fsync": fsync_fails})
    first = results[0]
    assert_no_authoritative_valid(first)
    assert not Path(first["evidence_dir"], "result.json").exists()
    assert results[1].get("status") == "NOT-STARTED"
    actions = [r["action"] for r in journal(first)]
    assert actions[-2:] == ["FINAL", "FINALIZATION-FAILED"]     # written, not durable: superseded
    assert first.get("finalization", {}).get("stage") == "final-journal"
    assert assert_consumer_rejects(lab, first)["state"] == "FAILED"
    assert_evidence_preserved(first)


def detector_F1_T2b(lab):
    """FINAL 'succeeds' but is not durably on disk (lost write): verification must catch it."""

    def lose_final(ctx, fd):
        path = ctx.journal.path
        data = path.read_bytes()
        cut = data.rstrip(b"\n").rfind(b"\n") + 1
        with open(path, "r+b") as handle:
            handle.truncate(cut)

    results, _ = run_batch(lab, {"final_fsync": lose_final})
    first = results[0]
    assert_no_authoritative_valid(first)
    assert not Path(first["evidence_dir"], "result.json").exists()
    assert first.get("finalization", {}).get("stage") == "final-verify"
    assert_consumer_rejects(lab, first)


def detector_F1_T3(lab):
    truncated, _ = run_batch(lab, {"pending_write": lambda ctx, data: data[: len(data) // 2]}, count=1)
    first = truncated[0]
    assert_no_authoritative_valid(first)
    assert first.get("finalization", {}).get("stage") == "pending-verify"
    assert not Path(first["evidence_dir"], "result.json").exists()
    assert "FINAL" not in [r["action"] for r in journal(first)]
    assert assert_consumer_rejects(lab, first)["state"] == "FAILED"

    def write_fails(ctx, data):
        raise OSError("injected: pending write failed")

    failed, _ = run_batch(lab, {"pending_write": write_fails}, count=1)
    assert_no_authoritative_valid(failed[0])
    assert failed[0].get("finalization", {}).get("stage") == "pending-write"
    assert not Path(failed[0]["evidence_dir"], "result.json").exists()


def detector_F1_T4(lab):
    def corrupt(ctx, path):
        data = bytearray(path.read_bytes())
        data[10] ^= 0x01
        os.chmod(path, 0o600)
        path.write_bytes(bytes(data))

    results, _ = run_batch(lab, {"after_pending": corrupt})
    first = results[0]
    assert_no_authoritative_valid(first)
    assert first.get("finalization", {}).get("stage") == "pending-verify", first.get("finalization")
    assert "FINAL" not in [r["action"] for r in journal(first)]   # a corrupt candidate is never bound
    marker = json.loads(Path(first["evidence_dir"], harness.FAILED_NAME).read_text())
    assert "does not match the intended result bytes" in marker["finalization"]["error"]
    assert results[1].get("status") == "NOT-STARTED"


def detector_F1_T5(lab):
    def publish_fails(ctx):
        raise OSError("injected: publication failed")

    results, _ = run_batch(lab, {"publish": publish_fails})
    first = results[0]
    assert_no_authoritative_valid(first)
    assert not Path(first["evidence_dir"], "result.json").exists()
    records = journal(first)
    finals = [r for r in records if r["action"] == "FINAL"]
    assert len(finals) == 1 and records[-1]["action"] == "FINALIZATION-FAILED"   # FINAL preserved
    status = assert_consumer_rejects(lab, first)
    assert status["state"] == "FAILED" and "no authoritative result.json" in status["reasons"]
    assert results[1].get("status") == "NOT-STARTED"


def detector_F1_T6(lab):
    order = {}

    def observe(ctx):
        order["journal_tail_at_publish"] = journal_tail(ctx.journal.path)
        order["result_existed_at_publish"] = (ctx.run_dir / "result.json").exists()

    results, _ = run_batch(lab, {"publish": observe})
    first = results[0]
    assert (first["experiment_validity"], first["batch_action"]) == (VALID, CONTINUE)
    assert order["journal_tail_at_publish"] == "FINAL" and order["result_existed_at_publish"] is False
    run_dir = Path(first["evidence_dir"])
    on_disk = persisted_result(first)
    assert on_disk == first
    status = lab.hm.validate_run_evidence(run_dir)
    assert status["state"] == "COMPLETE" and status["result"] == first
    final = journal(first)[-1]
    assert final["action"] == "FINAL" and final["candidate_sha256"] == pyenv.sha256_file(run_dir / "result.json")
    assert final["run_id"] == first["run_id"]
    assert os.path.samefile(run_dir / "result.json", run_dir / harness.PENDING_NAME)
    assert not (run_dir / harness.FAILED_NAME).exists()
    assert results[1]["experiment_validity"] == VALID


def journal_tail(path):
    lines = [line for line in Path(path).read_text().splitlines() if line]
    return json.loads(lines[-1])["action"] if lines else None


def detector_F1_T7a(lab):
    """Interruption (a real SIGTERM) after FINAL but before publication."""

    def interrupt(ctx):
        os.kill(os.getpid(), signal.SIGTERM)
        time.sleep(5)

    results, _ = run_batch(lab, {"after_final": interrupt})
    first = results[0]
    assert_no_authoritative_valid(first)
    assert "HarnessInterrupted" in first["finalization"]["error"]
    run_dir = Path(first["evidence_dir"])
    assert not (run_dir / "result.json").exists()
    assert (run_dir / harness.PENDING_NAME).exists()
    assert results[1].get("status") == "NOT-STARTED"
    assert_consumer_rejects(lab, first)


def detector_F1_T7b(lab):
    """Interruption immediately after publication, before directory sync/confirmation."""

    def interrupt(ctx):
        raise lab.hm.HarnessInterrupted("injected after publication")

    results, _ = run_batch(lab, {"after_publish": interrupt})
    first = results[0]
    assert_no_authoritative_valid(first)
    detail = first["finalization"]
    assert detail["published_before_failure"] is True and detail["retracted_published_result"] is True
    run_dir = Path(first["evidence_dir"])
    assert not (run_dir / "result.json").exists()                 # our own publication retracted
    assert (run_dir / harness.PENDING_NAME).exists()              # its bytes preserved
    assert assert_consumer_rejects(lab, first)["state"] == "FAILED"
    assert results[1].get("status") == "NOT-STARTED"


def detector_F1_T8(lab):
    foreign = b'{"foreign": "pre-existing result of another writer"}\n'

    def plant(ctx):
        (ctx.run_dir / "result.json").write_bytes(foreign)

    results, _ = run_batch(lab, {"before_finalize": plant})
    first = results[0]
    assert_no_authoritative_valid(first)
    run_dir = Path(first["evidence_dir"])
    assert (run_dir / "result.json").exists() and (run_dir / "result.json").read_bytes() == foreign  # not overwritten
    assert first.get("finalization", {}).get("stage") == "publish"
    assert first.get("finalization", {}).get("published_before_failure") is False
    assert_consumer_rejects(lab, first)
    assert results[1].get("status") == "NOT-STARTED"


def _variants(base: Path, root: Path):
    """Copies of a genuinely complete run directory, each with one defect."""

    def copy(name):
        target = root / name
        shutil.copytree(base, target)
        return target

    def rewrite_journal(target, transform):
        path = target / "journal.jsonl"
        lines = [json.loads(line) for line in path.read_text().splitlines() if line]
        path.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in transform(lines)))

    out = {"complete": copy("complete")}
    v = copy("result-missing-pending-present")
    (v / "result.json").unlink()
    out[v.name] = v
    v = copy("final-missing")
    rewrite_journal(v, lambda lines: lines[:-1])
    out[v.name] = v
    v = copy("final-binds-other-bytes")
    rewrite_journal(v, lambda lines: lines[:-1] + [dict(lines[-1], candidate_sha256="0" * 64)])
    out[v.name] = v
    v = copy("result-bytes-changed")
    (v / "result.json").unlink()
    (v / "result.json").write_bytes((v / harness.PENDING_NAME).read_bytes().replace(b'"VALID"', b'"INVALID"'))
    (v / harness.PENDING_NAME).unlink()
    out[v.name] = v
    v = copy("failure-marker-present")
    (v / harness.FAILED_NAME).write_text("{}")
    out[v.name] = v
    v = copy("journal-partial-trailing-record")
    with open(v / "journal.jsonl", "ab") as handle:
        handle.write(b'{"seq": 999, "state": "S9"')
    out[v.name] = v
    v = copy("journal-sequence-gap")
    rewrite_journal(v, lambda lines: lines[:3] + lines[4:])
    out[v.name] = v
    v = copy("record-after-final")
    rewrite_journal(v, lambda lines: lines + [{"seq": len(lines) + 1, "state": "S9", "action": "NOTE"}])
    out[v.name] = v
    v = copy("evidence-complete-false")
    data = json.loads((v / "result.json").read_text())
    data["evidence_complete"] = False
    raw = json.dumps(data, indent=2, sort_keys=True).encode()
    for name in ("result.json", harness.PENDING_NAME):
        (v / name).unlink()
        (v / name).write_bytes(raw)
    rewrite_journal(v, lambda lines: lines[:-1] + [dict(lines[-1], candidate_sha256=pyenv.sha256_bytes(raw))])
    out[v.name] = v
    v = copy("result-corrupt-json")
    (v / "result.json").unlink()
    (v / "result.json").write_bytes(b"{not json")
    (v / harness.PENDING_NAME).unlink()
    out[v.name] = v
    v = copy("pending-differs")
    (v / harness.PENDING_NAME).unlink()
    (v / harness.PENDING_NAME).write_bytes(b"{}")
    out[v.name] = v
    v = copy("final-run-id-mismatch")
    rewrite_journal(v, lambda lines: lines[:-1] + [dict(lines[-1], run_id="another-run")])
    out[v.name] = v
    return out


def detector_F1_T9(lab):
    results, _ = run_batch(lab, count=1)
    base = Path(results[0]["evidence_dir"])
    assert results[0]["experiment_validity"] == VALID
    variants = _variants(base, lab.tmp / "variants")
    accepted = {name for name, path in variants.items() if lab.hm.validate_run_evidence(path)["complete"]}
    assert accepted == {"complete"}, accepted
    assert lab.hm.validate_run_evidence(variants["result-missing-pending-present"])["state"] == "PENDING"
    assert lab.hm.validate_run_evidence(variants["failure-marker-present"])["state"] == "FAILED"


def detector_F1_T10(lab):
    """Finalization failure leaves outcome and restoration status (and their precedence)
    untouched; only experiment validity and batch action become INVALID/HALT."""

    def wrong_bytes(ctx):
        ctx.target_path.write_bytes(ctx.target_path.read_bytes().replace(b"alpha", b"gamma"))

    def fsync_fails(ctx, fd):
        raise OSError("injected")

    indeterminate, _ = run_batch(lab, {"after_restore": wrong_bytes, "final_fsync": fsync_fails}, count=1)
    r = indeterminate[0]
    assert (r["outcome"], r["restoration_status"], r["experiment_validity"], r["batch_action"]) == (
        "DETECTED", "INDETERMINATE", INVALID, HALT)
    verified, _ = run_batch(lab, {"final_fsync": fsync_fails}, count=1)
    r = verified[0]
    assert (r["outcome"], r["restoration_status"], r["experiment_validity"], r["batch_action"]) == (
        "DETECTED", "RESTORED-VERIFIED", INVALID, HALT)
    for current, new in ((lab.hm.RESTORED_VERIFIED, lab.hm.INDETERMINATE),
                         (lab.hm.INDETERMINATE, lab.hm.RESTORATION_FAILED),
                         (lab.hm.RESTORATION_FAILED, lab.hm.RESTORED_VERIFIED)):
        combined = lab.hm.combine_restoration(current, new)
        assert lab.hm.PRECEDENCE[combined] == max(lab.hm.PRECEDENCE[current], lab.hm.PRECEDENCE[new])


DETECTORS = {name[len("detector_"):]: fn for name, fn in globals().items() if name.startswith("detector_")}


# ------------------------------------------------------------------ tests

def test_F1_T1_final_append_failure_publishes_no_valid_result(lab):
    detector_F1_T1(lab)


def test_F1_T2_final_fsync_failure(lab):
    detector_F1_T2(lab)


def test_F1_T2b_non_durable_final_record_is_detected(lab):
    detector_F1_T2b(lab)


def test_F1_T3_pending_write_failure_or_truncation(lab):
    detector_F1_T3(lab)


def test_F1_T4_pending_verification_failure(lab):
    detector_F1_T4(lab)


def test_F1_T5_publication_failure(lab):
    detector_F1_T5(lab)


def test_F1_T6_success_path_publishes_only_after_final(lab):
    detector_F1_T6(lab)


def test_F1_T7a_interruption_after_final_before_publication(lab):
    detector_F1_T7a(lab)


def test_F1_T7b_interruption_after_publication(lab):
    detector_F1_T7b(lab)


def test_F1_T8_pre_existing_result_is_not_overwritten(lab):
    detector_F1_T8(lab)


def test_F1_T9_consumer_accepts_only_genuinely_complete_runs(lab):
    detector_F1_T9(lab)


def test_F1_T10_classification_and_precedence_preserved(lab):
    detector_F1_T10(lab)


# ------------------------------------------------------------------ F1 negative controls

#: (id, defect, old, new, designated detector). Exact-once source mutations of harness.py.
F1_MUTANTS = [
    ("FM-1", "original premature ordering: publish result.json before the FINAL record",
     '            self._append_final(ctx, candidate_sha)\n'
     '            stage = "final-verify"\n'
     '            self._verify_journal_tail(ctx)\n'
     '            self._fault("after_final", ctx=ctx)\n'
     '            stage = "publish"\n'
     '            self._publish(ctx, pending)\n',
     '            stage = "publish"\n'
     '            self._publish(ctx, pending)\n'
     '            self._append_final(ctx, candidate_sha)\n'
     '            stage = "final-verify"\n'
     '            self._verify_journal_tail(ctx)\n'
     '            self._fault("after_final", ctx=ctx)\n', "F1_T1"),
    ("FM-2", "FINAL durability verification removed",
     '            self._verify_journal_tail(ctx)\n', '            pass\n', "F1_T2b"),
    ("FM-3", "pending-candidate integrity check bypassed",
     '            if pyenv.sha256_file(pending) != candidate_sha:\n', '            if False:\n', "F1_T4"),
    ("FM-4", "consumer contract ignores the FINAL binding",
     '    elif final.get("candidate_sha256") != digest:\n', '    elif False:\n', "F1_T9"),
    ("FM-5", "publication overwrites an existing result.json",
     '        os.link(pending, result_path)  # atomic, same directory; refuses an existing result.json\n',
     '        shutil.copyfile(pending, result_path)\n', "F1_T8"),
    ("FM-6", "a published result is not retracted after a later failure",
     '        if ctx.published:\n            # Retract', '        if False:\n            # Retract', "F1_T7b"),
]


@pytest.mark.parametrize("mutant", F1_MUTANTS, ids=[m[0] for m in F1_MUTANTS])
def test_f1_mutant_is_killed(mutant, tmp_path):
    mutant_id, defect, old, new, detector_name = mutant
    module = load_harness_mutant(mutant_id, old, new)
    if mutant_id == "FM-5":
        module.shutil = shutil                       # the mutant body needs shutil in scope
    try:
        DETECTORS[detector_name](Lab(tmp_path, hm=module))
    except AssertionError:
        return
    pytest.fail(f"{mutant_id} SURVIVED ({defect}): detector {detector_name} passed")
