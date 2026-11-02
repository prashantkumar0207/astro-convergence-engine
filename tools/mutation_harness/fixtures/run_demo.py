"""Integrated WP-RD-B fixture demonstration (directive Phase 5). FIXTURE ONLY.

Usage:  python fixtures/run_demo.py <output-directory-under-the-system-temp-dir>

Runs seven scenarios against freshly created disposable fixture repositories and writes
every evidence tree plus summary.json under the output directory, outside the repository:

  1 DETECTED, restored, VALID          5 unknown restored bytes: INDETERMINATE, HALT
  2 UNDETECTED, restored, VALID        6 missing attestation: RESTORATION-FAILED, HALT
  3 EQUIVALENT pre-registration        7 legacy stale-cache reproduction, then prevention
  4 known restoration-verification failure: RESTORATION-FAILED, INVALID, HALT
"""

import json
import marshal
import os
import struct
import sys
from pathlib import Path

HARNESS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HARNESS_DIR))
sys.path.insert(0, str(HARNESS_DIR / "tests"))

import harness  # noqa: E402
import helpers  # noqa: E402
import pyenv  # noqa: E402
from fixtures import fixture_repo, legacy_wpn1  # noqa: E402

FIVE_SECONDS_NS = 5_000_000_000


def make_runner(root: Path, faults=None, extra_env=None):
    base = helpers.base_env()
    base["FIXTURE_FAULT_FILE"] = str(root / "FAULT")
    base.update(extra_env or {})
    for name in ("evidence", "quarantine"):
        (root / name).mkdir(exist_ok=True)
    return harness.Runner(harness.HarnessConfig(
        python=helpers.PYTHON, base_env=base, evidence_root=str(root / "evidence"),
        quarantine_dir=str(root / "quarantine"), authorized_roots=[str(root)],
        hook_sha256=pyenv.verify_hook(), allow_test_faults=bool(faults), faults=faults or {}))


def summarise(result):
    journal_path = Path(result["evidence_dir"], "journal.jsonl")
    records = [json.loads(line) for line in journal_path.read_text().splitlines()]
    s8 = [r for r in records if r["state"] == "S8" and r["action"].startswith("result ")]
    consumer = harness.validate_run_evidence(result["evidence_dir"])
    return {
        "consumer": {key: consumer[key] for key in ("state", "path", "experiment_verified", "properties", "reasons",
                                                    "limitations")},
        "outcome": result["outcome"],
        "restoration_status": result["restoration_status"],
        "experiment_validity": result["experiment_validity"],
        "batch_action": result["batch_action"],
        "s8_checks": result["s8_checks"],
        "target_sha256": result["target_sha256"],
        "quarantined": result["quarantined"],
        "cleanup_status": result["cleanup_status"],
        "journal_records": len(records),
        "journal_last": records[-1]["action"],
        "journal_sha256": pyenv.sha256_file(journal_path),
        "result_json_sha256": (pyenv.sha256_file(Path(result["evidence_dir"], "result.json"))
                               if Path(result["evidence_dir"], "result.json").exists() else None),
        "s8_attestation": {r["action"]: {"ok": r["attestation"]["ok"], "failures": r["attestation"]["failures"],
                                         "children": r["attestation"]["children"],
                                         "directly_attested_children": r["attestation"]["directly_attested_children"]}
                           for r in s8},
        "failures": result["failures"],
        "evidence_dir": result["evidence_dir"],
    }


def scenario(root: Path, name: str, kind: str, faults=None):
    work = root / name
    work.mkdir()
    repo = fixture_repo.make_fixture_repo(work / "repo")
    spec = fixture_repo.build_spec(harness, repo, name, helpers.PYTHON, kind=kind)
    results = make_runner(work, faults(work) if faults else None).run_batch([
        spec, fixture_repo.build_spec(harness, fixture_repo.make_fixture_repo(work / "repo-next"),
                                      name + "-next", helpers.PYTHON, kind="swap")])
    summary = summarise(results[0])
    summary["next_experiment_in_batch"] = results[1].get("status") or triple(results[1])
    return summary


def triple(result):
    return [result["outcome"], result["restoration_status"], result["experiment_validity"], result["batch_action"]]


def legacy_then_protocol(root: Path):
    work = root / "7-stale-cache"
    work.mkdir()
    repo = fixture_repo.make_fixture_repo(work / "legacy-repo")
    spec = fixture_repo.build_spec(harness, repo, "7-legacy", helpers.PYTHON, kind="swap")
    edit = spec.edits[0]
    target = repo / "pkg" / "target.py"
    legacy_wpn1.ENV = helpers.default_env()
    legacy_wpn1.sh([helpers.PYTHON, "fake_certifier.py"], repo)
    forced = {}

    def after_mutated():
        forced["ns"] = target.stat().st_mtime_ns + FIVE_SECONDS_NS
        os.utime(target, ns=(forced["ns"], forced["ns"]))

    legacy = legacy_wpn1.legacy_sequence(
        repo, helpers.PYTHON, [("pkg/target.py", edit.line, edit.old, edit.new)], spec.designated.argv[2],
        "fake_certifier.py", "fake_validator.py", fixture_repo.FAIL_PREFIX, spec.validator_expect,
        after_mutated=after_mutated, after_restore=lambda: os.utime(target, ns=(forced["ns"], forced["ns"])))
    pyc = next((repo / "pkg" / "__pycache__").glob("target.*.pyc")).read_bytes()
    _flags, header_mtime, header_size = struct.unpack("<III", pyc[4:16])
    cached = pyenv.code_digest(pyenv.find_code(marshal.loads(pyc[16:]), "house"))
    mutated_text = target.read_bytes().replace(edit.old.encode(), edit.new.encode())

    def force(ctx):
        stat = ctx.target_path.stat()
        ctx.forced_mtime_ns = stat.st_mtime_ns + FIVE_SECONDS_NS
        os.utime(ctx.target_path, ns=(ctx.forced_mtime_ns,) * 2)

    protocol_repo = fixture_repo.make_fixture_repo(work / "protocol-repo")
    protocol_spec = fixture_repo.build_spec(harness, protocol_repo, "7-protocol", helpers.PYTHON, kind="swap")
    protocol = make_runner(work, {"after_mutate": force,
                                  "after_restore": lambda ctx: os.utime(ctx.target_path,
                                                                        ns=(ctx.forced_mtime_ns,) * 2)}
                           ).run_experiment(protocol_spec)
    return {
        "legacy": {
            "outcome": legacy["outcome"],
            "restored_hash_matches": legacy["restored_hash_matches"],
            "restoration_ok": legacy["restoration_ok"],
            "batch_halts": legacy["batch_halts"],
            "restored_gate_rc": legacy["restored_gate_alone"]["rc"],
            "restored_gate_shows_mutated_signature":
                "house_number=10 expected=4" in legacy["restored_gate_alone"]["stdout"],
            "pyc_header_matches_restored_source": (header_mtime == int(target.stat().st_mtime)
                                                   and header_size == target.stat().st_size),
            "pyc_code_equals_mutated_text": cached == pyenv.expected_digest(mutated_text, "house"),
            "pyc_code_equals_restored_text": cached == pyenv.expected_digest(target.read_bytes(), "house"),
        },
        "protocol": summarise(protocol),
        "protocol_repo_bytecode_files": [str(p) for p in protocol_repo.rglob("*.pyc")],
    }


def main(out: Path):
    temp = Path(os.environ.get("TMPDIR", "/tmp")).resolve()
    out = out.resolve()
    if not out.is_relative_to(temp):
        raise SystemExit(f"output directory must be under {temp}")
    out.mkdir(parents=False, exist_ok=False)

    def fault_file(content):
        return lambda work: {"after_restore": lambda ctx: (work / "FAULT").write_text(content)}

    def unknown_bytes(_work):
        return {"after_restore": lambda ctx: ctx.target_path.write_bytes(
            ctx.target_path.read_bytes().replace(b"alpha", b"gamma"))}

    def missing_attestation(_work):
        def delete(ctx, phase, command, result, attest_dir):
            if phase == "S8" and command == "end_to_end":
                (attest_dir / f"{result.pid}.end.json").unlink()
        return {"after_command": delete}

    summary = {
        "python": sys.version,
        "harness_sources_sha256": {name: pyenv.sha256_file(HARNESS_DIR / name) for name in (
            "harness.py", "gitstatus.py", "pyenv.py", "attest_hook/sitecustomize.py",
            "fixtures/fixture_repo.py", "fixtures/legacy_wpn1.py", "fixtures/run_demo.py")},
        "1-detected": scenario(out, "1-detected", "swap"),
        "2-undetected": scenario(out, "2-undetected", "unused"),
        "3-equivalent": scenario(out, "3-equivalent", "equivalent"),
        "4-known-restoration-failure": scenario(out, "4-known-restoration-failure", "swap", fault_file("gate")),
        "5-unknown-hash": scenario(out, "5-unknown-hash", "swap", unknown_bytes),
        "6-missing-attestation": scenario(out, "6-missing-attestation", "swap", missing_attestation),
        "7-stale-cache": legacy_then_protocol(out),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True, default=str))
    print(json.dumps({key: (value.get("outcome"), value.get("restoration_status"), value.get("experiment_validity"),
                            value.get("batch_action"), value.get("next_experiment_in_batch"))
                      if isinstance(value, dict) and "outcome" in value else None
                      for key, value in summary.items() if key[0].isdigit()}, indent=1))
    print(json.dumps(summary["7-stale-cache"]["legacy"], indent=1))
    print("protocol:", summary["7-stale-cache"]["protocol"]["outcome"],
          summary["7-stale-cache"]["protocol"]["restoration_status"],
          summary["7-stale-cache"]["protocol"]["experiment_validity"],
          "bytecode files:", summary["7-stale-cache"]["protocol_repo_bytecode_files"])


if __name__ == "__main__":
    main(Path(sys.argv[1]))
