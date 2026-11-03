"""WP-RD-B fail-closed mutation-experiment state machine (R1 s6, CEO Amendment A).

States, strictly in order (each transition is journalled before it acts):

  S0 INIT          spec, path, target-guard and hook checks; worktree hygiene; interpreter probes
  S1 PREREGISTER   pre.json written once (exclusive create) and fsynced
  S2 BASELINE      end-to-end + every gate alone + validator, all attested, on pristine code
  S3 PRECHECK      non-equivalence pre-check on pristine code
  S4 BACKUP        byte copy of the target into the evidence directory, hash-verified
  S5 MUTATE        registered mutated bytes written, hash-verified
  S6 OBSERVE       designated gate, validator, end-to-end, excluded gates (attested, mutated code)
  S7 RESTORE       byte copy back from the verified backup (never a reverse text edit)
  S8 VERIFY        hash, status, designated gate, end-to-end, final hash, final status
  S9 FINALIZE      result.json written once, fsynced and re-read; journal FINAL record

Three separate dimensions are reported: `outcome` (DETECTED, DETECTED-OTHER, UNDETECTED,
EQUIVALENT, VOID - unchanged WP-N1 vocabulary), `restoration_status` (NOT-APPLICABLE,
RESTORED-VERIFIED, RESTORATION-FAILED, INDETERMINATE; precedence INDETERMINATE >
RESTORATION-FAILED > RESTORED-VERIFIED) and `experiment_validity` (VALID, INVALID). An S6
outcome is never rewritten. The batch continues only after a VALID experiment.

No `assert` statement is used for any safety-relevant check (tests verify this).
FIXTURE TESTING ONLY: ACE targets are refused (ACE_TARGET_MARKERS).
"""

from __future__ import annotations

import json
import os
import re
import signal
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from types import SimpleNamespace

import gitstatus
import pyenv

# ------------------------------------------------------------------ vocabulary

DETECTED = "DETECTED"
DETECTED_OTHER = "DETECTED-OTHER"
UNDETECTED = "UNDETECTED"
EQUIVALENT = "EQUIVALENT"
VOID = "VOID"
OUTCOMES = (DETECTED, DETECTED_OTHER, UNDETECTED, EQUIVALENT, VOID)

NOT_APPLICABLE = "NOT-APPLICABLE"
RESTORED_VERIFIED = "RESTORED-VERIFIED"
RESTORATION_FAILED = "RESTORATION-FAILED"
INDETERMINATE = "INDETERMINATE"
#: Amendment A precedence, highest wins and is never downgraded.
PRECEDENCE = {RESTORED_VERIFIED: 0, RESTORATION_FAILED: 1, INDETERMINATE: 2}

VALID = "VALID"
INVALID = "INVALID"
CONTINUE = "CONTINUE"
HALT = "HALT"

CHECK_OK = "ok"
CHECK_FAILED = "failed"
CHECK_INDETERMINATE = "indeterminate"
CHECK_NOT_RUN = "not_run"

#: Paths whose presence identifies an ACE repository. WP-RD-B authorizes fixture testing
#: only; running against an ACE target requires a separate owner authorization and a code
#: change, deliberately not a configuration option.
ACE_TARGET_MARKERS = ("engine/astrology", "scripts/certify_d45.py")


class HarnessRefused(Exception):
    """The configuration, spec or target is not acceptable; nothing was executed."""


class IndeterminateState(Exception):
    """The on-disk state can no longer be established; no further writes are made."""


class HarnessInterrupted(BaseException):
    """Raised by the SIGTERM handler while an experiment is running."""


# ------------------------------------------------------------------ pure decision rules

def combine_restoration(current: str | None, new: str) -> str:
    if current is None or current == NOT_APPLICABLE:
        return new
    return current if PRECEDENCE[current] >= PRECEDENCE[new] else new


def decide_restoration(checks: dict) -> str:
    """Restoration status from the S8 check states. Any indeterminate check wins; every
    mandatory check must be `ok` for RESTORED-VERIFIED; a check not run counts as failed."""

    if not checks:
        return RESTORATION_FAILED
    if any(state == CHECK_INDETERMINATE for state in checks.values()):
        return INDETERMINATE
    if all(state == CHECK_OK for state in checks.values()):
        return RESTORED_VERIFIED
    return RESTORATION_FAILED


def derive_validity(outcome: str, restoration_status: str, attestation_ok: bool, evidence_ok: bool) -> str:
    if (outcome in OUTCOMES and outcome != VOID
            and restoration_status in (RESTORED_VERIFIED, NOT_APPLICABLE)
            and attestation_ok is True and evidence_ok is True):
        return VALID
    return INVALID


def classify_outcome(gate, validator, end_to_end, excluded, fail_returncode: int, fail_prefix: str,
                     validator_expect) -> str:
    """WP-N1 classification rules, unchanged."""

    gate_lines = gate.stdout.decode("utf-8", "replace").splitlines()
    designated_fired = gate.returncode == fail_returncode and any(
        line.startswith(fail_prefix) for line in gate_lines)
    validator_text = validator.stdout.decode("utf-8", "replace") if validator is not None else ""
    validator_ok = validator is None or all(text in validator_text for text in validator_expect)
    others_failed = end_to_end.returncode != 0 or any(result.returncode != 0 for result in excluded)
    if designated_fired and validator_ok:
        return DETECTED
    if gate.returncode == 0 and others_failed:
        return DETECTED_OTHER
    if gate.returncode == 0:
        return UNDETECTED
    return VOID


# ------------------------------------------------------------------ specification

@dataclass
class Command:
    name: str
    argv: list
    on_pass_children: int | None
    min_on_fail_children: int | None
    target_load: str  # main | child | any | none
    timeout: float = 120.0


@dataclass
class Edit:
    line: int
    old: str
    new: str


@dataclass
class ExperimentSpec:
    run_id: str
    worktree: str
    target: str
    module: str
    qualnames: list
    edits: list
    designated: Command
    end_to_end: Command
    baseline_gates: list
    excluded: list
    fail_prefix: str
    allow_list: list
    validator: Command | None = None
    validator_expect: list = field(default_factory=list)
    precheck: Command | None = None
    fail_returncode: int = 3


@dataclass
class HarnessConfig:
    python: str
    base_env: dict
    evidence_root: str
    quarantine_dir: str
    authorized_roots: list
    hook_sha256: str
    allow_test_faults: bool = False
    faults: dict = field(default_factory=dict)
    git: str = "git"


# ------------------------------------------------------------------ evidence

#: WP-RD-B-F1 two-phase result publication. The authoritative result file is created only
#: after the FINAL journal record binding its exact bytes is durable and verified.
RESULT_NAME = "result.json"                 # authoritative, only when validate_run_evidence() says COMPLETE
PENDING_NAME = "result.pending.json"        # candidate; never authoritative on its own
FAILED_NAME = "FINALIZATION_FAILED.json"    # failed or incomplete finalization marker
FINALIZATION_PROTOCOL = "wp-rd-b-f1-two-phase-v1"


class FinalizationError(Exception):
    """Mandatory evidence could not be finalized; a VALID result must not be published."""


def _fsync_write(path: Path, data: bytes) -> None:
    with open(path, "xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


def _fsync_dir(path: Path) -> None:
    """Make directory entries durable. POSIX only: elsewhere this raises, so finalization
    fails closed instead of claiming a durability it cannot establish."""

    if os.name != "posix":
        raise OSError("directory fsync is not supported on this platform")
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


class Journal:
    """Append-only write-ahead journal, one JSON object per line, fsynced per record."""

    def __init__(self, path: Path):
        self.path = path
        self.seq = 0
        self.last_line = ""
        _fsync_write(path, b"")
        _fsync_dir(path.parent)

    def append(self, state: str, action: str, _sync_fn=None, **data) -> dict:
        self.seq += 1
        record = {"seq": self.seq, "state": state, "action": action, **data}
        line = json.dumps(record, sort_keys=True, default=str) + "\n"
        with open(self.path, "a", encoding="utf-8") as handle:
            handle.write(line)
            handle.flush()
            (_sync_fn or os.fsync)(handle.fileno())
        self.last_line = line
        return record


# ------------------------------------------------------------------ evidence consumer (WP-RD-B-F2)
#
# validate_run_evidence() establishes three separate properties, each from independently
# inspected evidence rather than from the producer's success labels:
#   publication integrity   the F1 protocol completed for exactly these result bytes;
#   evidence completeness   every record and file this execution path requires exists and links up;
#   verdict consistency     outcome, restoration, attestation and validity are re-derived from raw
#                           evidence and must equal what the result reports.
#
# COMPLETE does not mean the experiment succeeded: a correctly documented INVALID run is complete
# history. Assurance is structural completeness, cross-artifact consistency and correctly derived
# verdicts. It is NOT authenticity: these hashes are self-contained, so someone able to rewrite
# every artifact and re-run this logic is not detected. Signed attestation, external provenance
# and independent execution are separate concerns.

EVIDENCE_SCHEMA = "wp-rd-b-f2-evidence-v1"

PATH_REFUSED = "REFUSED_BEFORE_PREREGISTRATION"
PATH_ABORTED = "ABORTED_BEFORE_MUTATION"
PATH_BASELINE_VOID = "BASELINE_VOID"
PATH_PRECHECK_VOID = "PRECHECK_VOID"
PATH_EQUIVALENT = "EQUIVALENT_PRECHECK"
PATH_MUTATION = "MUTATION_EXPERIMENT"
PATH_BACKUP_CORRUPT = "RESTORE_REFUSED_BACKUP_CORRUPT"
PATH_INTERRUPTED = "INTERRUPTED_AFTER_MUTATION_INTENT"
#: Paths on which the target was never mutated, so restoration is NOT-APPLICABLE.
_PATHS_WITHOUT_MUTATION = (PATH_REFUSED, PATH_ABORTED, PATH_BASELINE_VOID, PATH_PRECHECK_VOID, PATH_EQUIVALENT)
#: The only paths that can represent a verified experiment.
_PATHS_VERIFIABLE = (PATH_MUTATION, PATH_EQUIVALENT)

_S8_CHECKS = ("a_hash", "b_status", "c_designated", "d_end_to_end", "e_final_hash", "f_final_status")
_CHECK_STATES = (CHECK_OK, CHECK_FAILED, CHECK_INDETERMINATE, CHECK_NOT_RUN)
_RESTORATION_STATES = (NOT_APPLICABLE, RESTORED_VERIFIED, RESTORATION_FAILED, INDETERMINATE)
_HASH_CHECK_MAP = {"baseline": CHECK_OK, "mutated": CHECK_FAILED, "unknown": CHECK_INDETERMINATE}
_SHA256_TEXT = re.compile(r"[0-9a-f]{64}\Z")


def _is_int(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _is_sha256(value) -> bool:
    return isinstance(value, str) and _SHA256_TEXT.match(value) is not None


def _is_str_list(value) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


class _PathError(Exception):
    """The journal does not follow a permitted execution path."""


class _Aborted(Exception):
    """The next journal record is the EXCEPTION record ending the state sequence."""


@dataclass
class _CommandFact:
    phase: str
    spec: dict
    start: dict
    record: dict
    stdout: bytes | None = None
    stderr: bytes | None = None
    attestation_ok: bool = False


@dataclass
class _Facts:
    """What the journal says happened; raw supporting evidence is checked separately."""

    path: str | None = None
    spec: dict | None = None
    begin: dict | None = None
    initialised: dict | None = None
    preregistered: dict | None = None
    baseline: dict | None = None
    precheck_failed: dict | None = None
    precheck_evaluated: dict | None = None
    backup: dict | None = None
    mutation_written: dict | None = None
    outcome: dict | None = None
    backup_corrupt: dict | None = None
    decided: dict | None = None
    exception: dict | None = None
    emergency: dict | None = None
    mutation_intended: bool = False
    commands: list = field(default_factory=list)
    s8: dict = field(default_factory=dict)
    s8_commands: dict = field(default_factory=dict)
    s8_timeout_unknown: dict = field(default_factory=dict)
    status_states: dict = field(default_factory=dict)

    def phase(self, name: str) -> list:
        return [fact for fact in self.commands if fact.phase == name]


class _JournalWalk:
    def __init__(self, body: list):
        self.body = body
        self.index = 0

    def peek(self):
        return self.body[self.index] if self.index < len(self.body) else None

    def at(self, state: str, action: str) -> bool:
        record = self.peek()
        return record is not None and record["state"] == state and record["action"] == action

    def take(self, state: str, action: str) -> dict:
        record = self.peek()
        if record is None:
            raise _PathError(f"journal ends before {state} '{action}'")
        if record["state"] == "EXCEPTION":
            raise _Aborted()
        if record["state"] != state or record["action"] != action:
            raise _PathError(f"expected {state} '{action}', found {record['state']} '{record['action']}'")
        self.index += 1
        return record

    def end(self) -> None:
        record = self.peek()
        if record is None:
            return
        if record["state"] == "EXCEPTION":
            raise _Aborted()
        raise _PathError(f"unexpected record {record['state']} '{record['action']}' after a terminal decision")


def _command_spec_ok(command) -> bool:
    return (isinstance(command, dict) and isinstance(command.get("name"), str) and _is_str_list(command.get("argv"))
            and command.get("target_load") in ("main", "child", "any", "none")
            and (command.get("on_pass_children") is None or _is_int(command.get("on_pass_children")))
            and (command.get("min_on_fail_children") is None or _is_int(command.get("min_on_fail_children"))))


def _spec_problem(spec) -> str | None:
    if not isinstance(spec, dict):
        return "registered spec is not an object"
    if not isinstance(spec.get("run_id"), str) or not isinstance(spec.get("module"), str):
        return "registered spec lacks run_id or module"
    if not isinstance(spec.get("target"), str) or not _is_str_list(spec.get("qualnames")) or not spec["qualnames"]:
        return "registered spec lacks target or qualnames"
    edits = spec.get("edits")
    if not isinstance(edits, list) or not edits or not all(
            isinstance(e, dict) and _is_int(e.get("line")) and isinstance(e.get("old"), str)
            and isinstance(e.get("new"), str) for e in edits):
        return "registered spec has invalid edits"
    for name in ("designated", "end_to_end"):
        if not _command_spec_ok(spec.get(name)):
            return f"registered spec has an invalid {name} command"
    for name in ("baseline_gates", "excluded"):
        if not isinstance(spec.get(name), list) or not all(_command_spec_ok(c) for c in spec[name]):
            return f"registered spec has invalid {name} commands"
    for name in ("validator", "precheck"):
        if spec.get(name) is not None and not _command_spec_ok(spec[name]):
            return f"registered spec has an invalid {name} command"
    if not isinstance(spec.get("fail_prefix"), str) or not _is_int(spec.get("fail_returncode")):
        return "registered spec lacks the failure signature"
    if not _is_str_list(spec.get("allow_list")) or not _is_str_list(spec.get("validator_expect")):
        return "registered spec lacks allow_list or validator_expect"
    return None


def _initialised_problem(record: dict, spec: dict) -> str | None:
    if not _is_sha256(record.get("baseline_sha256")) or not _is_sha256(record.get("mutated_sha256")):
        return "S0 'initialised' lacks the registered target hashes"
    if not _is_sha256(record.get("hook_sha256")):
        return "S0 'initialised' lacks the hook hash"
    digests = record.get("expected_digests")
    if not isinstance(digests, dict):
        return "S0 'initialised' lacks the expected digests"
    for phase in ("baseline", "mutated"):
        table = digests.get(phase)
        if not isinstance(table, dict) or set(table) != set(spec["qualnames"]) or not all(
                _is_sha256(value) for value in table.values()):
            return f"S0 'initialised' has invalid {phase} digests"
    return None


def _walk_command(walk: _JournalWalk, facts: _Facts, phase: str, command: dict) -> _CommandFact:
    start = walk.take(phase, f"start {command['name']}")
    record = walk.take(phase, f"result {command['name']}")
    fact = _CommandFact(phase, command, start, record)
    facts.commands.append(fact)
    return fact


def _walk_states(walk: _JournalWalk, facts: _Facts) -> None:
    facts.begin = walk.take("S0", "begin")
    problem = _spec_problem(facts.begin.get("spec"))
    if problem:
        raise _PathError(problem)
    spec = facts.spec = facts.begin["spec"]
    if not isinstance(facts.begin.get("run_id"), str) or facts.begin["run_id"] != spec["run_id"]:
        raise _PathError("S0 'begin' run id does not match its registered spec")
    for refusal in ("refused", "hygiene failed", "probe refused"):
        if walk.at("S0", refusal):
            walk.take("S0", refusal)
            walk.end()
            facts.path = PATH_REFUSED
            return
    facts.initialised = walk.take("S0", "initialised")
    problem = _initialised_problem(facts.initialised, spec)
    if problem:
        raise _PathError(problem)
    facts.preregistered = walk.take("S1", "preregistered")
    if not _is_sha256(facts.preregistered.get("pre_json_sha256")):
        raise _PathError("S1 'preregistered' lacks the pre.json hash")

    for command in [spec["end_to_end"], *spec["baseline_gates"], *([spec["validator"]] if spec.get("validator") else [])]:
        _walk_command(walk, facts, "S2", command)
    facts.baseline = walk.take("S2", "baseline evaluated")
    if not isinstance(facts.baseline.get("clean"), bool):
        raise _PathError("S2 'baseline evaluated' has no boolean verdict")
    if not facts.baseline["clean"]:
        walk.end()
        facts.path = PATH_BASELINE_VOID
        return

    if spec.get("precheck") is None:
        walk.take("S3", "no pre-check registered; admitted")
    else:
        _walk_command(walk, facts, "S3", spec["precheck"])
        if walk.at("S3", "pre-check failed"):
            facts.precheck_failed = walk.take("S3", "pre-check failed")
            walk.end()
            facts.path = PATH_PRECHECK_VOID
            return
        facts.precheck_evaluated = walk.take("S3", "pre-check evaluated")
        if not isinstance(facts.precheck_evaluated.get("admitted"), bool):
            raise _PathError("S3 'pre-check evaluated' has no boolean decision")
        if not facts.precheck_evaluated["admitted"]:
            walk.end()
            facts.path = PATH_EQUIVALENT
            return

    facts.backup = walk.take("S4", "backup written")
    walk.take("S5", "intent: write mutated bytes")
    facts.mutation_intended = True
    facts.mutation_written = walk.take("S5", "mutation written")
    if facts.mutation_written.get("hash_state") != "mutated":
        record = walk.peek()
        if record is None or record["state"] != "EXCEPTION":
            raise _PathError("the mutation write was not verified and no EXCEPTION record follows")
        raise _Aborted()

    for command in [spec["designated"], *([spec["validator"]] if spec.get("validator") else []), spec["end_to_end"],
                    *spec["excluded"]]:
        _walk_command(walk, facts, "S6", command)
    facts.outcome = walk.take("S6", "outcome recorded")

    if walk.at("S7", "backup corrupt; restore refused"):
        facts.backup_corrupt = walk.take("S7", "backup corrupt; restore refused")
        walk.end()
        facts.path = PATH_BACKUP_CORRUPT
        return
    walk.take("S7", "intent: restore from backup")
    walk.take("S7", "restore written")
    _walk_s8(walk, facts, spec)
    facts.decided = walk.take("S8", "restoration decided")
    walk.end()
    facts.path = PATH_MUTATION


def _walk_s8(walk: _JournalWalk, facts: _Facts, spec: dict) -> None:
    """S8 runs a fixed order and stops early only for the reasons the state machine defines."""

    facts.s8["a_hash"] = walk.take("S8", "a_hash")
    if facts.s8["a_hash"].get("hash_state") != "baseline":
        return
    facts.s8["b_status"] = walk.take("S8", "b_status")
    if "status_error" in facts.s8["b_status"]:
        return
    for name, command in (("c_designated", spec["designated"]), ("d_end_to_end", spec["end_to_end"])):
        facts.s8_commands[name] = _walk_command(walk, facts, "S8", command)
        if walk.at("S8", name):
            facts.s8_timeout_unknown[name] = walk.take("S8", name)
            return
    facts.s8["e_final_hash"] = walk.take("S8", "e_final_hash")
    if facts.s8["e_final_hash"].get("hash_state") == "unknown":
        return
    facts.s8["f_final_status"] = walk.take("S8", "f_final_status")


def _walk_abort(walk: _JournalWalk, facts: _Facts) -> None:
    facts.exception = walk.body[walk.index]
    walk.index += 1
    if facts.exception.get("mutation_intended") is not facts.mutation_intended:
        raise _PathError("EXCEPTION record disagrees with the mutation intent in the journal")
    record = walk.peek()
    if record is not None and record["state"] == "EMERGENCY":
        if not facts.mutation_intended:
            raise _PathError("EMERGENCY record on a path that never intended a mutation")
        facts.emergency = record
        walk.index += 1
    if walk.peek() is not None:
        raise _PathError("unexpected records after the EXCEPTION record")
    facts.path = PATH_INTERRUPTED if facts.mutation_intended else PATH_ABORTED


def _walk_execution_path(records) -> tuple:
    """Classify the journal into exactly one permitted execution path, or report why not."""

    facts = _Facts()
    if records is None:
        return facts, ["execution path: the journal is not usable"]
    if len(records) < 2 or records[-1]["state"] != "S9" or records[-1]["action"] != "FINAL":
        return facts, ["execution path: the journal does not end with S9 'FINAL'"]
    if records[-2]["state"] != "S9" or records[-2]["action"] != "intent: finalize evidence (two-phase)":
        return facts, ["execution path: S9 'FINAL' is not preceded by the finalization intent"]
    walk = _JournalWalk(records[:-2])
    try:
        try:
            _walk_states(walk, facts)
        except _Aborted:
            _walk_abort(walk, facts)
    except _PathError as exc:
        facts.path = None
        return facts, [f"execution path: {exc}"]
    return facts, []


def _load_journal(path: Path, reasons: list) -> tuple:
    """Parse the journal defensively; returns (records or None, raw bytes)."""

    try:
        raw = path.read_bytes()
    except OSError as exc:
        reasons.append(f"journal unreadable: {exc}")
        return None, b""
    if not raw:
        reasons.append("journal is empty")
        return None, raw
    if not raw.endswith(b"\n"):
        reasons.append("journal ends with an incomplete record")
    records = []
    for number, line in enumerate(raw.split(b"\n"), start=1):
        if not line:
            continue
        try:
            record = json.loads(line)
        except ValueError as exc:
            reasons.append(f"journal line {number} is not valid JSON: {exc}")
            return None, raw
        if not isinstance(record, dict):
            reasons.append(f"journal line {number} is not a JSON object")
            return None, raw
        if not isinstance(record.get("state"), str) or not isinstance(record.get("action"), str):
            reasons.append(f"journal line {number} lacks a state or action")
            return None, raw
        records.append(record)
    for index, record in enumerate(records, start=1):
        if not _is_int(record.get("seq")) or record["seq"] != index:
            reasons.append(f"journal sequence is not gap-free from 1 (record {index} has {record.get('seq')!r})")
            break
    return records, raw


def _check_result_schema(result, reasons: list) -> bool:
    """Types and vocabulary of the result; fields are compared with evidence separately."""

    if not isinstance(result, dict):
        reasons.append("result.json is not a JSON object")
        return False
    before = len(reasons)
    if result.get("evidence_schema") != EVIDENCE_SCHEMA:
        reasons.append("result.json does not declare the evidence schema")
    if not isinstance(result.get("run_id"), str):
        reasons.append("result.json run_id is not a string")
    if result.get("outcome") not in OUTCOMES or not isinstance(result.get("outcome"), str):
        reasons.append(f"unknown outcome: {result.get('outcome')!r}")
    if result.get("restoration_status") not in _RESTORATION_STATES or not isinstance(result.get("restoration_status"), str):
        reasons.append(f"unknown restoration status: {result.get('restoration_status')!r}")
    if result.get("experiment_validity") not in (VALID, INVALID) or not isinstance(result.get("experiment_validity"), str):
        reasons.append(f"unknown experiment validity: {result.get('experiment_validity')!r}")
    if result.get("batch_action") not in (CONTINUE, HALT) or not isinstance(result.get("batch_action"), str):
        reasons.append(f"unknown batch action: {result.get('batch_action')!r}")
    for name in ("attestation_ok", "mutation_applied", "quarantined", "cleanup_eligible"):
        if not isinstance(result.get(name), bool):
            reasons.append(f"result.json {name} is not a boolean")
    if result.get("evidence_complete") is not True:
        reasons.append("result.json does not declare evidence_complete")
    checks = result.get("s8_checks")
    if not isinstance(checks, dict) or not all(
            name in _S8_CHECKS and isinstance(state, str) and state in _CHECK_STATES for name, state in checks.items()):
        reasons.append("result.json s8_checks is malformed")
    target = result.get("target_sha256")
    if not isinstance(target, dict) or not all(name in target for name in ("baseline", "mutated", "final")):
        reasons.append("result.json target_sha256 is malformed")
    if not isinstance(result.get("observations"), dict):
        reasons.append("result.json observations is not an object")
    if not isinstance(result.get("failures"), list):
        reasons.append("result.json failures is not a list")
    binding = result.get("evidence_binding")
    if not isinstance(binding, dict) or not _is_sha256(binding.get("journal_prefix_sha256")):
        reasons.append("result.json evidence_binding is malformed")
    return len(reasons) == before


def _check_publication_integrity(run_dir: Path, raw_journal: bytes, records, data: bytes, result, reasons: list) -> None:
    """The completed F1 protocol, for exactly these result bytes."""

    digest = pyenv.sha256_bytes(data)
    final = records[-1] if records else None
    if final is None or final.get("state") != "S9" or final.get("action") != "FINAL":
        reasons.append("journal does not end with the S9 FINAL record")
    elif final.get("candidate_sha256") != digest:
        reasons.append("FINAL record does not bind this result.json")
    elif not isinstance(result, dict) or final.get("run_id") != result.get("run_id"):
        reasons.append("FINAL record run id does not match result.json")
    pending_path = run_dir / PENDING_NAME
    if not pending_path.is_file():
        reasons.append("pending candidate is missing")
    elif pyenv.sha256_file(pending_path) != digest:
        reasons.append("pending candidate differs from result.json")
    if isinstance(result, dict):
        finalization = result.get("finalization")
        if not isinstance(finalization, dict) or finalization.get("protocol") != FINALIZATION_PROTOCOL:
            reasons.append("result.json does not declare the two-phase finalization protocol")
        binding = result.get("evidence_binding")
        prefix = raw_journal[:raw_journal.rfind(b"\n", 0, max(len(raw_journal) - 1, 0)) + 1]
        if isinstance(binding, dict) and binding.get("journal_prefix_sha256") != pyenv.sha256_bytes(prefix):
            reasons.append("journal prefix does not match the result's evidence binding")


def _validate_preregistration(run_dir: Path, facts: _Facts, result, reasons: list) -> None:
    """pre.json against the journal's independent S1 hash and the S0 registration."""

    pre_path = run_dir / "pre.json"
    binding = result.get("evidence_binding") if isinstance(result, dict) else None
    bound = binding.get("pre_json_sha256") if isinstance(binding, dict) else None
    if facts.preregistered is None:
        if pre_path.exists():
            reasons.append("pre.json exists on a path that never preregistered")
        if bound is not None:
            reasons.append("result binds a pre.json on a path that never preregistered")
        return
    if not pre_path.is_file():
        reasons.append("pre.json is missing on a path requiring preregistration")
        return
    data = pre_path.read_bytes()
    if pyenv.sha256_bytes(data) != facts.preregistered.get("pre_json_sha256"):
        reasons.append("pre.json does not match the journal's preregistration hash")
    if bound != facts.preregistered.get("pre_json_sha256"):
        reasons.append("pre.json hash in the result differs from the journal's preregistration hash")
    try:
        pre = json.loads(data)
    except ValueError as exc:
        reasons.append(f"pre.json is not valid JSON: {exc}")
        return
    if not isinstance(pre, dict):
        reasons.append("pre.json is not a JSON object")
        return
    if pre.get("run_id") != facts.begin.get("run_id"):
        reasons.append("pre.json run id differs from the journal")
    if pre.get("spec") != facts.spec:
        reasons.append("pre.json registered spec differs from the journal")
    if pre.get("target_sha256_baseline") != facts.initialised["baseline_sha256"]:
        reasons.append("pre.json registered baseline hash differs from the journal")
    if pre.get("target_sha256_mutated") != facts.initialised["mutated_sha256"]:
        reasons.append("pre.json registered mutated hash differs from the journal")
    if pre.get("expected_digests") != facts.initialised["expected_digests"]:
        reasons.append("pre.json expected digests differ from the journal")
    if pre.get("hook_sha256") != facts.initialised["hook_sha256"]:
        reasons.append("pre.json hook hash differs from the journal")


def _read_bound_file(path: Path, expected, what: str, reasons: list):
    """Read a file the journal references by hash. None means it is unavailable."""

    if not path.is_file():
        reasons.append(f"missing evidence file: {what}")
        return None
    data = path.read_bytes()
    if pyenv.sha256_bytes(data) != expected:
        reasons.append(f"evidence hash mismatch: {what}")
    return data


def _verify_command_evidence(run_dir: Path, facts: _Facts, index: int, fact: _CommandFact, reasons: list) -> None:
    """Outputs and attestation of one command, re-evaluated from its raw records."""

    name = fact.spec["name"]
    label = f"{index:02d}-{fact.phase}-{name}"
    where = f"{fact.phase} {name}"
    record, process = fact.record, fact.record.get("process")
    recorded = record.get("attestation")
    if record.get("label") != label:
        reasons.append(f"{where}: unexpected evidence label {record.get('label')!r}")
    if not isinstance(process, dict) or not isinstance(recorded, dict):
        reasons.append(f"{where}: result record lacks process or attestation data")
        return
    if not _is_int(process.get("pid")) or not _is_int(process.get("returncode")) or not isinstance(
            process.get("timed_out"), bool):
        reasons.append(f"{where}: malformed process record")
        return
    if fact.start.get("argv") != fact.spec["argv"] or process.get("argv") != fact.spec["argv"]:
        reasons.append(f"{where}: command line differs from the registered spec")
    fact.stdout = _read_bound_file(run_dir / "io" / f"{label}.stdout", process.get("stdout_sha256"),
                                   f"{where} stdout", reasons)
    fact.stderr = _read_bound_file(run_dir / "io" / f"{label}.stderr", process.get("stderr_sha256"),
                                   f"{where} stderr", reasons)
    attest_dir, cache_dir = run_dir / "attest" / label, run_dir / "cache" / label
    if not attest_dir.is_dir():
        reasons.append(f"missing evidence file: {where} attestation directory")
        return
    if not cache_dir.is_dir():
        reasons.append(f"missing evidence file: {where} cache directory")
    recorded_files = record.get("attestation_files")
    actual_files = {item.name: pyenv.sha256_file(item) for item in sorted(attest_dir.iterdir()) if item.is_file()}
    if recorded_files != actual_files:
        reasons.append(f"evidence hash mismatch: {where} attestation records differ from the journal")
    digests = facts.initialised["expected_digests"]["mutated" if fact.phase == "S6" else "baseline"]
    module = facts.spec["module"]
    targets = tuple((module, qualname) for qualname in facts.spec["qualnames"])
    plan = pyenv.AttestationPlan(
        targets=targets,
        expected_digests={(module, qualname): digests[qualname] for qualname in facts.spec["qualnames"]},
        required_load={target: fact.spec["target_load"] for target in targets if fact.spec["target_load"] != "none"},
        children=pyenv.ChildExpectation(fact.spec.get("on_pass_children"), fact.spec.get("min_on_fail_children")),
        hook_sha256=facts.initialised["hook_sha256"],
        cache_dir=str(fact.start.get("cache_dir")),
        cache_listing_path=str(cache_dir),
    )
    report = pyenv.evaluate_attestation(attest_dir, process["pid"], process["returncode"], plan)
    attestation_ok = report.ok
    if recorded.get("ok") is not attestation_ok:
        reasons.append(f"{where}: recorded attestation result disagrees with the raw attestation records")
    if recorded.get("children") != report.children:
        reasons.append(f"{where}: recorded child processes disagree with the raw attestation records")
    fact.attestation_ok = attestation_ok is True
    # Bind the raw records to this command: the hook stamps each process with the phase label,
    # and the main process reports the command line it actually received.
    raw_records, _ = pyenv.load_records(attest_dir)
    for pid, kinds in raw_records.items():
        start = kinds.get("start")
        if start is not None and start.get("phase") != label:
            reasons.append(f"{where}: attestation record of pid {pid} belongs to another phase")
    main_start = raw_records.get(process["pid"], {}).get("start")
    if main_start is not None and main_start.get("orig_argv") != fact.spec["argv"]:
        reasons.append(f"{where}: attested command line differs from the registered spec")


def _status_state(run_dir: Path, record: dict, allow_list: list, what: str, reasons: list):
    """Re-derive a git status verdict from its raw bytes."""

    filename = record.get("status_file")
    if filename is None:
        if "status_error" not in record:
            reasons.append(f"{what}: neither raw status evidence nor an error is recorded")
            return None
        return CHECK_INDETERMINATE
    if not isinstance(filename, str) or Path(filename).name != filename:
        reasons.append(f"{what}: invalid status file reference")
        return None
    raw = _read_bound_file(run_dir / "io" / filename, record.get("status_sha256"), f"{what} git status", reasons)
    if raw is None:
        return None
    try:
        verdict = gitstatus.classify(gitstatus.parse_records(gitstatus.split_records(raw)), allow_list, frozenset())
    except gitstatus.StatusParseError:
        if "status_error" not in record:
            reasons.append(f"{what}: raw status is malformed but no error is recorded")
        return CHECK_INDETERMINATE
    if "status_error" in record:
        reasons.append(f"{what}: an error is recorded but the raw status parses")
    if record.get("verdict") != json.loads(json.dumps(asdict(verdict))):
        reasons.append(f"{what}: recorded verdict differs from the raw git status")
    return CHECK_OK if verdict.clean else CHECK_FAILED


def _hash_record_state(record: dict, facts: _Facts, what: str, reasons: list):
    """A journalled hash state must agree with the journalled hash and the registration."""

    sha = record.get("sha256")
    state = record.get("hash_state")
    baseline, mutated = facts.initialised["baseline_sha256"], facts.initialised["mutated_sha256"]
    derived = "baseline" if sha == baseline else "mutated" if sha == mutated else "unknown"
    if not _is_sha256(sha) or state != derived:
        reasons.append(f"{what}: recorded hash state {state!r} disagrees with hash {sha!r}")
    return derived


def _verify_backup_and_registration(run_dir: Path, facts: _Facts, reasons: list, limitations: list) -> None:
    """The retained baseline bytes must reproduce the registered hashes and digests."""

    if facts.backup is None:
        return
    baseline = facts.initialised["baseline_sha256"]
    backup_path = run_dir / "backup" / "target.bin"
    if not backup_path.is_file():
        reasons.append("missing evidence file: backup/target.bin")
        return
    data = backup_path.read_bytes()
    actual = pyenv.sha256_bytes(data)
    expected_corrupt = (facts.backup_corrupt is not None or facts.backup.get("backup_sha256") != baseline
                        or (facts.emergency is not None and facts.emergency.get("backup_verified") is False))
    if expected_corrupt:
        if actual == baseline:
            reasons.append("backup matches the baseline although the journal records it as corrupt")
        return
    if actual != baseline or facts.backup.get("backup_sha256") != baseline:
        reasons.append("evidence hash mismatch: backup/target.bin")
        return
    try:
        mutated = _apply_edits(data, [Edit(e["line"], e["old"], e["new"]) for e in facts.spec["edits"]])
    except HarnessRefused as exc:
        reasons.append(f"registered mutation does not apply to the retained baseline: {exc}")
        return
    if pyenv.sha256_bytes(mutated) != facts.initialised["mutated_sha256"]:
        reasons.append("registered mutation does not reproduce the registered mutated hash")
    probe = facts.initialised.get("probe")
    plain = probe.get("plain") if isinstance(probe, dict) else None
    version = plain.get("version") if isinstance(plain, dict) else None
    here = f"{sys.version_info.major}.{sys.version_info.minor}."
    if not isinstance(version, str) or not version.startswith(here):
        limitations.append(f"expected digests not re-derived: evidence interpreter {version!r}, consumer {here}x")
        return
    digests = facts.initialised["expected_digests"]
    try:
        for qualname in facts.spec["qualnames"]:
            if pyenv.expected_digest(data, qualname) != digests["baseline"][qualname]:
                reasons.append(f"registered baseline digest of {qualname} is not reproducible")
            if pyenv.expected_digest(mutated, qualname) != digests["mutated"][qualname]:
                reasons.append(f"registered mutated digest of {qualname} is not reproducible")
    except (pyenv.EnvironmentRefused, SyntaxError, ValueError) as exc:
        reasons.append(f"registered digests are not reproducible: {exc}")


def _verify_supporting_evidence(run_dir: Path, facts: _Facts, reasons: list, limitations: list) -> None:
    for index, fact in enumerate(facts.commands, start=1):
        _verify_command_evidence(run_dir, facts, index, fact, reasons)
    allow_list = facts.spec["allow_list"]
    if facts.baseline is not None:
        facts.status_states["baseline"] = _status_state(run_dir, facts.baseline, allow_list, "S2 baseline", reasons)
        _hash_record_state(facts.baseline, facts, "S2 baseline", reasons)
    if facts.mutation_written is not None:
        _hash_record_state(facts.mutation_written, facts, "S5 mutation", reasons)
    if facts.outcome is not None:
        _hash_record_state(facts.outcome, facts, "S6 outcome", reasons)
    for name in ("b_status", "f_final_status"):
        if name in facts.s8:
            facts.status_states[name] = _status_state(run_dir, facts.s8[name], allow_list, f"S8 {name}", reasons)
    for name in ("a_hash", "e_final_hash"):
        if name in facts.s8:
            _hash_record_state(facts.s8[name], facts, f"S8 {name}", reasons)
    for name, record in facts.s8_timeout_unknown.items():
        _hash_record_state(record, facts, f"S8 {name}", reasons)
    _verify_backup_and_registration(run_dir, facts, reasons, limitations)


def _observation(fact: _CommandFact):
    return SimpleNamespace(returncode=fact.record["process"]["returncode"], stdout=fact.stdout or b"")


def _process_field(fact: _CommandFact, name: str):
    process = fact.record.get("process")
    return process.get(name) if isinstance(process, dict) else None


def _recompute_outcome(facts: _Facts) -> str:
    """Re-derive the outcome from raw observations with the registered classification rules."""

    if facts.path == PATH_EQUIVALENT:
        return EQUIVALENT
    if facts.outcome is None:
        return VOID
    observed = {fact.spec["name"]: fact for fact in facts.phase("S6")}
    if (facts.outcome.get("hash_state") != "mutated"
            or any(_process_field(fact, "timed_out") is not False or not fact.attestation_ok
                   for fact in observed.values())):
        return VOID
    spec = facts.spec
    validator = observed[spec["validator"]["name"]] if spec.get("validator") else None
    return classify_outcome(_observation(observed[spec["designated"]["name"]]),
                            _observation(validator) if validator is not None else None,
                            _observation(observed[spec["end_to_end"]["name"]]),
                            [_observation(observed[c["name"]]) for c in spec["excluded"]],
                            spec["fail_returncode"], spec["fail_prefix"], spec["validator_expect"])


def _recompute_s8_checks(facts: _Facts) -> dict:
    checks = {}
    for name in ("a_hash", "e_final_hash"):
        if name in facts.s8:
            sha = facts.s8[name].get("sha256")
            baseline, mutated = facts.initialised["baseline_sha256"], facts.initialised["mutated_sha256"]
            checks[name] = _HASH_CHECK_MAP["baseline" if sha == baseline else "mutated" if sha == mutated else "unknown"]
    for name in ("b_status", "f_final_status"):
        if name in facts.s8:
            state = facts.status_states.get(name)
            checks[name] = state if state is not None else CHECK_FAILED
    for name, fact in facts.s8_commands.items():
        if name in facts.s8_timeout_unknown:
            checks[name] = CHECK_INDETERMINATE
        elif (_process_field(fact, "timed_out") is not False or _process_field(fact, "returncode") != 0
              or not fact.attestation_ok):
            checks[name] = CHECK_FAILED
        else:
            checks[name] = CHECK_OK
    return checks


def _recompute_restoration(facts: _Facts) -> dict:
    """Re-derive the restoration status from the raw S8 evidence."""

    if facts.path in _PATHS_WITHOUT_MUTATION:
        return {"status": NOT_APPLICABLE, "checks": {}}
    checks = _recompute_s8_checks(facts)
    if facts.path == PATH_MUTATION:
        for name in _S8_CHECKS:
            checks.setdefault(name, CHECK_NOT_RUN)
        return {"status": decide_restoration(checks), "checks": checks}
    return {"status": INDETERMINATE, "checks": checks}


def _recompute_attestation(facts: _Facts) -> bool:
    if not all(fact.attestation_ok for fact in facts.commands):
        return False
    return facts.outcome is None or facts.outcome.get("hash_state") == "mutated"


def _check_baseline_and_precheck(facts: _Facts, reasons: list) -> None:
    """The journal's S2 and S3 decisions must follow from their raw evidence."""

    if facts.baseline is not None:
        clean = (all(_process_field(f, "returncode") == 0 and _process_field(f, "timed_out") is False and f.attestation_ok
                     for f in facts.phase("S2"))
                 and facts.baseline.get("hash_state") == "baseline" and facts.status_states.get("baseline") == CHECK_OK)
        if clean is not facts.baseline.get("clean"):
            reasons.append("S2 baseline decision disagrees with its raw evidence")
    precheck = facts.phase("S3")
    if not precheck or (facts.precheck_failed is None and facts.precheck_evaluated is None):
        return
    fact = precheck[0]
    admitted = None
    try:
        parsed = json.loads((fact.stdout or b"").decode("utf-8").strip().splitlines()[-1])
        if isinstance(parsed, dict) and isinstance(parsed.get("admitted"), bool):
            admitted = parsed["admitted"]
    except (ValueError, IndexError):
        admitted = None
    usable = (_process_field(fact, "returncode") == 0 and _process_field(fact, "timed_out") is False
              and fact.attestation_ok and admitted is not None)
    if facts.precheck_failed is not None and usable:
        reasons.append("S3 recorded a pre-check failure but its raw evidence is usable")
    if facts.precheck_evaluated is not None and (not usable or facts.precheck_evaluated.get("admitted") is not admitted):
        reasons.append("S3 pre-check decision disagrees with its raw evidence")


def _check_verdict_consistency(facts: _Facts, result: dict, reasons: list) -> None:
    """Every reported verdict is compared with one re-derived from independently inspected evidence."""

    _check_baseline_and_precheck(facts, reasons)
    expected_outcome = _recompute_outcome(facts)
    expected_restoration = _recompute_restoration(facts)
    expected_attestation = _recompute_attestation(facts)
    expected_validity = derive_validity(expected_outcome, expected_restoration["status"], expected_attestation, True)

    if result.get("outcome") != expected_outcome:
        reasons.append(f"reported outcome {result.get('outcome')!r} disagrees with the evidence ({expected_outcome})")
    if facts.outcome is not None and facts.outcome.get("outcome") != expected_outcome:
        reasons.append(f"journal outcome disagrees with the raw observations ({expected_outcome})")
    if result.get("restoration_status") != expected_restoration["status"]:
        reasons.append(f"reported restoration {result.get('restoration_status')!r} disagrees with the evidence "
                       f"({expected_restoration['status']})")
    reported_checks = result.get("s8_checks")
    if facts.path == PATH_INTERRUPTED:
        computed = expected_restoration["checks"]
        if any(computed.get(name) != state for name, state in reported_checks.items()):
            reasons.append("reported S8 checks disagree with the raw evidence")
    elif reported_checks != expected_restoration["checks"]:
        reasons.append("reported S8 checks disagree with the raw evidence")
    if facts.decided is not None and (facts.decided.get("status") != expected_restoration["status"]
                                      or facts.decided.get("checks") != expected_restoration["checks"]):
        reasons.append("journal restoration decision disagrees with the raw evidence")
    if result.get("attestation_ok") is not expected_attestation:
        reasons.append(f"reported attestation_ok disagrees with the raw attestation records ({expected_attestation})")
    if result.get("experiment_validity") != expected_validity:
        reasons.append(f"reported validity {result.get('experiment_validity')!r} disagrees with the evidence "
                       f"({expected_validity})")
    if result.get("batch_action") != (CONTINUE if result.get("experiment_validity") == VALID else HALT):
        reasons.append(f"batch action {result.get('batch_action')!r} contradicts validity "
                       f"{result.get('experiment_validity')!r}")
    if result.get("mutation_applied") is not facts.mutation_intended:
        reasons.append("reported mutation_applied disagrees with the journal")
    if result.get("experiment_validity") == VALID and (result.get("failures") or facts.path not in _PATHS_VERIFIABLE):
        reasons.append("a VALID verdict is impossible on this path or with recorded failures")
    eligible = expected_validity == VALID
    if result.get("cleanup_eligible") is not eligible or result.get("cleanup_status") != (
            "ELIGIBLE-RETAINED-BY-POLICY" if eligible else "INELIGIBLE-RETAINED"):
        reasons.append("reported cleanup eligibility disagrees with the evidence")
    must_quarantine = facts.mutation_intended and expected_restoration["status"] != RESTORED_VERIFIED
    if result.get("quarantined") is not must_quarantine and not any(
            isinstance(item, str) and "quarantine marker could not be written" in item for item in result["failures"]):
        reasons.append("reported quarantine decision disagrees with the evidence")
    _check_reported_target_and_observations(facts, result, expected_restoration["status"], reasons)


def _check_reported_target_and_observations(facts: _Facts, result: dict, restoration: str, reasons: list) -> None:
    target = result["target_sha256"]
    if facts.initialised is not None:
        baseline, mutated = facts.initialised["baseline_sha256"], facts.initialised["mutated_sha256"]
        if target.get("baseline") != baseline or target.get("mutated") != mutated:
            reasons.append("reported target hashes differ from the registration")
        untouched = facts.path == PATH_EQUIVALENT or (
            facts.path in _PATHS_WITHOUT_MUTATION and facts.baseline is not None
            and facts.baseline.get("hash_state") == "baseline" and not facts.phase("S3"))
        if (untouched or restoration == RESTORED_VERIFIED) and target.get("final") != baseline:
            reasons.append("reported final target hash is not the baseline")
        if facts.path == PATH_INTERRUPTED:  # the producer always attempts this once a mutation is intended
            if facts.emergency is None:
                if not any(isinstance(item, str) and "emergency restore failed" in item for item in result["failures"]):
                    reasons.append("the emergency restore attempt is neither journalled nor reported as failed")
            else:
                after = facts.emergency.get("after")
                final = target.get("final")
                known = {"baseline": baseline, "mutated": mutated}
                if (after in known and final != known[after]) or (
                        after == "unknown" and final in known.values()) or after not in (*known, "unknown"):
                    reasons.append("reported final target hash differs from the emergency restore record")
        if facts.path == PATH_MUTATION:  # an interruption's emergency restore may move the target later
            for name in ("e_final_hash", "a_hash"):
                if name in facts.s8 and not facts.s8_timeout_unknown:
                    if facts.s8[name].get("sha256") != target.get("final"):
                        reasons.append(f"reported final target hash differs from S8 {name}")
                    break
            for record in facts.s8_timeout_unknown.values():
                if record.get("sha256") != target.get("final"):
                    reasons.append("reported final target hash differs from the S8 timeout record")
    observed = facts.phase("S6")
    spec = facts.spec
    expected_names = [spec["designated"]["name"], *([spec["validator"]["name"]] if spec.get("validator") else []),
                      spec["end_to_end"]["name"], *[c["name"] for c in spec["excluded"]]]
    complete = [fact.spec["name"] for fact in observed] == expected_names
    expected = {fact.spec["name"]: fact.record.get("process") for fact in observed} if complete else {}
    if result.get("observations") != expected:
        reasons.append("reported observations differ from the journal")


def validate_run_evidence(run_dir) -> dict:
    """Consumer contract (WP-RD-B-F1, hardened by WP-RD-B-F2). A run's result is authoritative
    ONLY if this returns state COMPLETE, which requires publication integrity, evidence
    completeness and verdict consistency together.

      COMPLETE    all three properties hold. The experiment may still be INVALID: read
                  `experiment_verified` (and result.experiment_validity) to learn whether it
                  is a verified experiment, and `path` for how it ended.
      PENDING     no result.json but a pending candidate exists: never authoritative.
      FAILED      FINALIZATION_FAILED.json is present.
      INCOMPLETE  anything else (missing, corrupt, mismatching or contradictory evidence).

    Never raises for malformed evidence.
    """

    try:
        return _validate_run_evidence(Path(run_dir))
    except Exception as exc:  # noqa: BLE001 - a consumer defect must not become an acceptance
        return {"state": "INCOMPLETE", "complete": False, "reasons": [f"validator internal error: {exc!r}"],
                "result": None, "path": None, "experiment_verified": False,
                "properties": {"publication_integrity": False, "evidence_completeness": False,
                               "verdict_consistency": False},
                "limitations": []}


def _validate_run_evidence(run_dir: Path) -> dict:
    result_path, pending_path, failed_path = run_dir / RESULT_NAME, run_dir / PENDING_NAME, run_dir / FAILED_NAME
    publication: list = []
    completeness: list = []
    verdict: list = []
    limitations: list = []
    if failed_path.exists():
        publication.append("finalization failure marker present")
    records, raw_journal = _load_journal(run_dir / "journal.jsonl", completeness)

    def status(state: str, result, path) -> dict:
        reasons = publication + completeness + verdict
        complete = state == "COMPLETE"
        return {"state": state, "complete": complete, "reasons": reasons, "result": result if complete else None,
                "path": path,
                "experiment_verified": complete and path in _PATHS_VERIFIABLE and result.get("experiment_validity") == VALID,
                "properties": {"publication_integrity": not publication, "evidence_completeness": not completeness,
                               "verdict_consistency": complete or (not verdict and path is not None)},
                "limitations": limitations}

    if not result_path.exists():
        publication.append("no authoritative result.json")
        return status("FAILED" if failed_path.exists() else "PENDING" if pending_path.exists() else "INCOMPLETE",
                      None, None)
    try:
        data = result_path.read_bytes()
    except OSError as exc:
        publication.append(f"result.json unreadable: {exc}")
        return status("FAILED" if failed_path.exists() else "INCOMPLETE", None, None)
    result = None
    try:
        result = json.loads(data)
    except ValueError as exc:
        publication.append(f"result.json is not valid JSON: {exc}")
    _check_publication_integrity(run_dir, raw_journal, records, data, result, publication)
    schema_ok = result is not None and _check_result_schema(result, verdict)
    facts, path_errors = _walk_execution_path(records)
    completeness.extend(path_errors)
    if facts.path is not None and isinstance(result, dict):
        if result.get("run_id") != facts.begin.get("run_id"):
            completeness.append("result.json run id differs from the journal")
        if facts.preregistered is not None or (run_dir / "pre.json").exists():
            _validate_preregistration(run_dir, facts, result, completeness)
        else:
            binding = result.get("evidence_binding")
            if isinstance(binding, dict) and binding.get("pre_json_sha256") is not None:
                completeness.append("result binds a pre.json on a path that never preregistered")
        if facts.initialised is not None:
            _verify_supporting_evidence(run_dir, facts, completeness, limitations)
        if schema_ok:
            _check_verdict_consistency(facts, result, verdict)
    reasons = publication + completeness + verdict
    if not reasons:
        return status("COMPLETE", result, facts.path)
    return status("FAILED" if failed_path.exists() else "INCOMPLETE", None, facts.path)


@dataclass
class RunContext:
    spec: ExperimentSpec
    run_dir: Path
    journal: Journal
    worktree: Path = None
    target_path: Path = None
    baseline_bytes: bytes = b""
    mutated_bytes: bytes = b""
    baseline_sha256: str = ""
    mutated_sha256: str = ""
    backup_path: Path = None
    digests_baseline: dict = field(default_factory=dict)
    digests_mutated: dict = field(default_factory=dict)
    outcome: str | None = None
    restoration: str | None = None
    s8_checks: dict = field(default_factory=dict)
    attestation_ok: bool = True
    mutation_intended: bool = False
    failures: list = field(default_factory=list)
    observations: dict = field(default_factory=dict)
    mutated_mtime_ns: int | None = None
    command_seq: int = 0
    published: bool = False
    pre_json_sha256: str | None = None


# ------------------------------------------------------------------ runner

class Runner:
    def __init__(self, config: HarnessConfig):
        self.config = config
        self.roots = [Path(root).resolve() for root in config.authorized_roots]
        if not self.roots:
            raise HarnessRefused("at least one authorized root is required")
        for name in ("evidence_root", "quarantine_dir"):
            self._require_under_root(Path(getattr(config, name)), name)
        if config.faults and not config.allow_test_faults:
            raise HarnessRefused("fault points configured without allow_test_faults")
        if config.allow_test_faults:
            temp = Path(tempfile.gettempdir()).resolve()
            for root in self.roots:
                if not root.is_relative_to(temp):
                    raise HarnessRefused(f"test faults are only allowed under {temp}: {root}")
        pyenv.validate_base_env(config.base_env)
        pyenv.verify_hook(pyenv.HOOK_DIR, config.hook_sha256)

    # -------------------------------------------------------------- helpers

    def _require_under_root(self, path: Path, what: str) -> Path:
        resolved = path.resolve()
        if not any(resolved.is_relative_to(root) for root in self.roots):
            raise HarnessRefused(f"{what} {resolved} is outside every authorized root")
        return resolved

    def _fault(self, point: str, **context):
        hook = self.config.faults.get(point)
        if hook is None:
            return None
        if not self.config.allow_test_faults:
            raise HarnessRefused(f"fault point {point} without allow_test_faults")
        return hook(**context)

    def _hash_state(self, ctx: RunContext) -> str:
        current = pyenv.sha256_file(ctx.target_path)
        if current == ctx.baseline_sha256:
            return "baseline"
        if current == ctx.mutated_sha256:
            return "mutated"
        return "unknown"

    def _run_attested(self, ctx: RunContext, phase: str, command: Command, expected: dict):
        ctx.command_seq += 1
        label = f"{ctx.command_seq:02d}-{phase}-{command.name}"
        pyenv.check_argv(command.argv, self.config.python)
        cache = pyenv.fresh_dir(ctx.run_dir / "cache", label)
        out = pyenv.fresh_dir(ctx.run_dir / "attest", label)
        targets = tuple((ctx.spec.module, qualname) for qualname in ctx.spec.qualnames)
        env = pyenv.build_env(self.config.base_env, cache, out, targets, label)
        ctx.journal.append(phase, f"start {command.name}", argv=[str(a) for a in command.argv],
                           cache_dir=str(cache), attest_dir=str(out))
        result = pyenv.run_process(command.argv, ctx.worktree, env, command.timeout)
        _fsync_write(ctx.run_dir / "io" / f"{label}.stdout", result.stdout)
        _fsync_write(ctx.run_dir / "io" / f"{label}.stderr", result.stderr)
        self._fault("after_command", ctx=ctx, phase=phase, command=command.name, result=result,
                    attest_dir=out)
        plan = pyenv.AttestationPlan(
            targets=targets,
            expected_digests={(ctx.spec.module, q): expected[q] for q in ctx.spec.qualnames},
            required_load={target: command.target_load for target in targets
                           if command.target_load != "none"},
            children=pyenv.ChildExpectation(command.on_pass_children, command.min_on_fail_children),
            hook_sha256=self.config.hook_sha256,
            cache_dir=str(cache),
        )
        report = pyenv.evaluate_attestation(out, result.pid, result.returncode, plan)
        if not report.ok:
            ctx.attestation_ok = False
        ctx.journal.append(phase, f"result {command.name}", process=result.summary(),
                           attestation=report.summary(), label=label,
                           attestation_files={item.name: pyenv.sha256_file(item) for item in sorted(out.iterdir())})
        return result, report

    def _recorded_status(self, ctx: RunContext, name: str, runner=subprocess.run):
        """Run git status keeping its raw bytes as evidence (WP-RD-B-F2), so the consumer can
        re-derive the verdict instead of trusting a label."""

        try:
            raw = gitstatus.run_git_status(ctx.worktree, self.config.git, runner)
        except gitstatus.GitStatusError as exc:
            return None, {"status_error": str(exc)}
        filename = f"status-{name}.bin"
        _fsync_write(ctx.run_dir / "io" / filename, raw)
        fields = {"status_file": filename, "status_sha256": pyenv.sha256_bytes(raw)}
        try:
            verdict = gitstatus.classify(gitstatus.parse_records(gitstatus.split_records(raw)),
                                         ctx.spec.allow_list, frozenset())
        except gitstatus.StatusParseError as exc:
            return None, {**fields, "status_error": str(exc)}
        return verdict, {**fields, "verdict": asdict(verdict)}

    # -------------------------------------------------------------- batch

    def run_batch(self, specs) -> list:
        results = []
        halted = False
        for spec in specs:
            if halted:
                results.append({"run_id": spec.run_id, "status": "NOT-STARTED",
                                "reason": "batch halted by an earlier INVALID experiment"})
                continue
            result = self.run_experiment(spec)
            results.append(result)
            if result["batch_action"] == HALT:
                halted = True
        return results

    # -------------------------------------------------------------- experiment

    def run_experiment(self, spec: ExperimentSpec) -> dict:
        evidence_root = self._require_under_root(Path(self.config.evidence_root), "evidence_root")
        run_dir = pyenv.fresh_dir(evidence_root, spec.run_id)
        for sub in ("cache", "attest", "io", "backup", "preflight"):
            (run_dir / sub).mkdir()
        ctx = RunContext(spec=spec, run_dir=run_dir, journal=Journal(run_dir / "journal.jsonl"))
        ctx.journal.append("S0", "begin", run_id=spec.run_id, spec=_spec_dict(spec))

        def on_sigterm(signum, frame):
            raise HarnessInterrupted(f"signal {signum}")

        previous = signal.signal(signal.SIGTERM, on_sigterm)
        try:
            try:
                self._experiment_body(ctx)
            except BaseException as exc:  # noqa: BLE001 - every exit path is journalled and fail-closed
                self._on_exception(ctx, exc)
            # WP-RD-B-F1: finalization also runs with the SIGTERM handler installed, so an
            # interruption there is caught by _finalize's fail-closed path.
            return self._finalize(ctx)
        finally:
            signal.signal(signal.SIGTERM, previous)

    def _experiment_body(self, ctx: RunContext) -> None:
        if not self._s0_init(ctx):
            return
        self._s1_preregister(ctx)
        if not self._s2_baseline(ctx):
            return
        if not self._s3_precheck(ctx):
            return
        self._s4_backup(ctx)
        self._s5_mutate(ctx)
        self._s6_observe(ctx)
        if self._s7_restore(ctx):
            self._s8_verify(ctx)

    # S0 ---------------------------------------------------------------

    def _s0_init(self, ctx: RunContext) -> bool:
        spec = ctx.spec
        try:
            ctx.worktree = self._require_under_root(Path(spec.worktree), "worktree")
            for marker in ACE_TARGET_MARKERS:
                if (ctx.worktree / marker).exists():
                    raise HarnessRefused(f"ACE target refused (marker {marker}); WP-RD-B is fixture-only")
            unresolved = ctx.worktree / spec.target
            ctx.target_path = unresolved.resolve()
            if unresolved.is_symlink() or not ctx.target_path.is_relative_to(ctx.worktree):
                raise HarnessRefused(f"target {spec.target} escapes the worktree or is a symlink")
            if not ctx.target_path.is_file():
                raise HarnessRefused(f"target {spec.target} is not a file")
            for command in self._all_commands(spec):
                pyenv.check_argv(command.argv, self.config.python)
                if command.target_load not in ("main", "child", "any", "none"):
                    raise HarnessRefused(f"command {command.name}: invalid target_load")
            pyenv.verify_hook(pyenv.HOOK_DIR, self.config.hook_sha256)
            if gitstatus.git_version(self.config.git) < gitstatus.MIN_GIT_VERSION:
                raise HarnessRefused("git is older than the required minimum")
            ctx.baseline_bytes = ctx.target_path.read_bytes()
            ctx.mutated_bytes = _apply_edits(ctx.baseline_bytes, spec.edits)
            ctx.baseline_sha256 = pyenv.sha256_bytes(ctx.baseline_bytes)
            ctx.mutated_sha256 = pyenv.sha256_bytes(ctx.mutated_bytes)
            if ctx.baseline_sha256 == ctx.mutated_sha256:
                raise HarnessRefused("the registered edits do not change the target")
            for qualname in spec.qualnames:
                ctx.digests_baseline[qualname] = pyenv.expected_digest(ctx.baseline_bytes, qualname)
                ctx.digests_mutated[qualname] = pyenv.expected_digest(ctx.mutated_bytes, qualname)
        except (HarnessRefused, pyenv.EnvironmentRefused, gitstatus.GitStatusError, OSError) as exc:
            ctx.failures.append(f"S0 refused: {exc}")
            ctx.journal.append("S0", "refused", error=str(exc))
            ctx.outcome, ctx.restoration = VOID, NOT_APPLICABLE
            return False

        hygiene = self._hygiene_findings(ctx)
        if hygiene:
            ctx.failures.append(f"S0 worktree hygiene: {hygiene}")
            ctx.journal.append("S0", "hygiene failed", findings=hygiene)
            ctx.outcome, ctx.restoration = VOID, NOT_APPLICABLE
            return False
        try:
            report = pyenv.preflight(self.config.python, self.config.base_env, ctx.run_dir / "preflight",
                                     self.config.hook_sha256)
        except pyenv.EnvironmentRefused as exc:
            ctx.failures.append(f"S0 interpreter probe refused: {exc}")
            ctx.journal.append("S0", "probe refused", error=str(exc))
            ctx.outcome, ctx.restoration = VOID, NOT_APPLICABLE
            return False
        ctx.journal.append("S0", "initialised", baseline_sha256=ctx.baseline_sha256,
                           mutated_sha256=ctx.mutated_sha256, probe=report,
                           expected_digests={"baseline": ctx.digests_baseline, "mutated": ctx.digests_mutated},
                           hook_sha256=self.config.hook_sha256)
        return True

    def _hygiene_findings(self, ctx: RunContext) -> list:
        findings = []
        for path in ctx.worktree.rglob("*"):
            relative = path.relative_to(ctx.worktree)
            if relative.parts and relative.parts[0] == ".git":
                continue
            if path.name == "__pycache__" or path.suffix in (".pyc", ".pyo"):
                findings.append(str(relative))
        try:
            verdict = gitstatus.status_verdict(ctx.worktree, frozenset(), frozenset(), self.config.git)
        except (gitstatus.GitStatusError, gitstatus.StatusParseError) as exc:
            findings.append(f"status unavailable: {exc}")
        else:
            if not verdict.clean:
                findings.append({"outside": verdict.outside, "ignored": verdict.ignored_new})
        return findings

    # S1 ---------------------------------------------------------------

    def _s1_preregister(self, ctx: RunContext) -> None:
        pre = {
            "run_id": ctx.spec.run_id,
            "spec": _spec_dict(ctx.spec),
            "target_sha256_baseline": ctx.baseline_sha256,
            "target_sha256_mutated": ctx.mutated_sha256,
            "expected_digests": {"baseline": ctx.digests_baseline, "mutated": ctx.digests_mutated},
            "hook_sha256": self.config.hook_sha256,
            "vocabulary": {"outcome": list(OUTCOMES),
                           "restoration_status": [NOT_APPLICABLE, *sorted(PRECEDENCE, key=PRECEDENCE.get)],
                           "experiment_validity": [VALID, INVALID]},
        }
        data = json.dumps(pre, indent=2, sort_keys=True).encode("utf-8")
        _fsync_write(ctx.run_dir / "pre.json", data)
        ctx.pre_json_sha256 = pyenv.sha256_bytes(data)
        ctx.journal.append("S1", "preregistered", pre_json_sha256=ctx.pre_json_sha256)

    # S2 ---------------------------------------------------------------

    def _s2_baseline(self, ctx: RunContext) -> bool:
        spec = ctx.spec
        commands = [spec.end_to_end, *spec.baseline_gates]
        if spec.validator is not None:
            commands.append(spec.validator)
        ok = True
        for command in commands:
            result, report = self._run_attested(ctx, "S2", command, ctx.digests_baseline)
            if result.returncode != 0 or result.timed_out or not report.ok:
                ok = False
                ctx.failures.append(f"S2 baseline {command.name}: rc={result.returncode} "
                                    f"timed_out={result.timed_out} attestation={report.failures}")
        hash_state = self._hash_state(ctx)
        if hash_state != "baseline":
            ok = False
            ctx.failures.append("S2 baseline changed the target file")
        verdict, status_fields = self._recorded_status(ctx, "S2-baseline")
        if verdict is None:
            ok = False
            ctx.failures.append(f"S2 status unavailable: {status_fields['status_error']}")
        elif not verdict.clean:
            ok = False
            ctx.failures.append(f"S2 baseline left changes outside the allow-list: {verdict}")
        ctx.journal.append("S2", "baseline evaluated", clean=ok, hash_state=hash_state,
                           sha256=pyenv.sha256_file(ctx.target_path), **status_fields)
        if not ok:
            ctx.outcome, ctx.restoration = VOID, NOT_APPLICABLE
        return ok

    # S3 ---------------------------------------------------------------

    def _s3_precheck(self, ctx: RunContext) -> bool:
        if ctx.spec.precheck is None:
            ctx.journal.append("S3", "no pre-check registered; admitted")
            return True
        result, report = self._run_attested(ctx, "S3", ctx.spec.precheck, ctx.digests_baseline)
        admitted = None
        try:
            parsed = json.loads(result.stdout.decode("utf-8").strip().splitlines()[-1])
            if isinstance(parsed, dict) and isinstance(parsed.get("admitted"), bool):
                admitted = parsed["admitted"]
        except (ValueError, IndexError, UnicodeDecodeError):
            admitted = None
        if result.returncode != 0 or result.timed_out or not report.ok or admitted is None:
            ctx.failures.append(f"S3 pre-check failed to execute: rc={result.returncode} "
                                f"attestation={report.failures}")
            ctx.journal.append("S3", "pre-check failed")
            ctx.outcome, ctx.restoration = VOID, NOT_APPLICABLE
            return False
        ctx.journal.append("S3", "pre-check evaluated", admitted=admitted)
        if not admitted:
            ctx.outcome, ctx.restoration = EQUIVALENT, NOT_APPLICABLE
            return False
        return True

    # S4 / S5 ----------------------------------------------------------

    def _s4_backup(self, ctx: RunContext) -> None:
        ctx.backup_path = ctx.run_dir / "backup" / "target.bin"
        _fsync_write(ctx.backup_path, ctx.baseline_bytes)
        backup_sha = pyenv.sha256_file(ctx.backup_path)
        stat = ctx.target_path.stat()
        ctx.journal.append("S4", "backup written", backup_sha256=backup_sha,
                           target_mode=oct(stat.st_mode), target_mtime_ns=stat.st_mtime_ns)
        if backup_sha != ctx.baseline_sha256:
            raise HarnessRefused("backup hash does not equal the baseline hash")
        self._fault("after_backup", ctx=ctx)

    def _s5_mutate(self, ctx: RunContext) -> None:
        ctx.mutation_intended = True
        ctx.journal.append("S5", "intent: write mutated bytes", mutated_sha256=ctx.mutated_sha256)
        with open(ctx.target_path, "wb") as handle:
            handle.write(ctx.mutated_bytes)
            handle.flush()
            os.fsync(handle.fileno())
        ctx.mutated_mtime_ns = ctx.target_path.stat().st_mtime_ns
        self._fault("after_mutate", ctx=ctx)
        state = self._hash_state(ctx)
        ctx.journal.append("S5", "mutation written", hash_state=state, sha256=pyenv.sha256_file(ctx.target_path))
        if state != "mutated":
            raise IndeterminateState(f"target hash after the mutation write is {state}")

    # S6 ---------------------------------------------------------------

    def _s6_observe(self, ctx: RunContext) -> None:
        spec = ctx.spec
        self._fault("during_s6", ctx=ctx)
        observations = {}
        invalid = []
        for command in [spec.designated, *([spec.validator] if spec.validator else []), spec.end_to_end,
                        *spec.excluded]:
            result, report = self._run_attested(ctx, "S6", command, ctx.digests_mutated)
            observations[command.name] = result
            if result.timed_out:
                invalid.append(f"{command.name} timed out")
            if not report.ok:
                invalid.append(f"{command.name} attestation: {report.failures}")
        ctx.observations = {name: result.summary() for name, result in observations.items()}
        state = self._hash_state(ctx)
        if state == "unknown":
            ctx.outcome = VOID
            ctx.failures.append("S6 left the target in an unknown state")
            raise IndeterminateState("target hash unknown after S6")
        if state != "mutated":
            invalid.append(f"target hash during S6 was {state}, not the registered mutated hash")
        if invalid:
            ctx.attestation_ok = False
            ctx.outcome = VOID
            ctx.failures.append(f"S6 observation invalidated: {invalid}")
        else:
            ctx.outcome = classify_outcome(
                observations[spec.designated.name],
                observations.get(spec.validator.name) if spec.validator else None,
                observations[spec.end_to_end.name],
                [observations[c.name] for c in spec.excluded],
                spec.fail_returncode, spec.fail_prefix, spec.validator_expect)
        ctx.journal.append("S6", "outcome recorded", outcome=ctx.outcome, invalidations=invalid,
                           hash_state=state, sha256=pyenv.sha256_file(ctx.target_path))

    # S7 ---------------------------------------------------------------

    def _s7_restore(self, ctx: RunContext) -> bool:
        backup = ctx.backup_path.read_bytes()
        if pyenv.sha256_bytes(backup) != ctx.baseline_sha256:
            ctx.failures.append("S7 backup no longer matches the baseline hash; nothing written")
            ctx.journal.append("S7", "backup corrupt; restore refused")
            ctx.restoration = combine_restoration(ctx.restoration, INDETERMINATE)
            return False
        ctx.journal.append("S7", "intent: restore from backup")
        with open(ctx.target_path, "wb") as handle:
            handle.write(backup)
            handle.flush()
            os.fsync(handle.fileno())
        ctx.journal.append("S7", "restore written")
        self._fault("after_restore", ctx=ctx)
        return True

    # S8 ---------------------------------------------------------------

    def _s8_hash_check(self, ctx: RunContext, name: str) -> bool:
        state = self._hash_state(ctx)
        ctx.s8_checks[name] = {"baseline": CHECK_OK, "mutated": CHECK_FAILED,
                               "unknown": CHECK_INDETERMINATE}[state]
        ctx.journal.append("S8", name, hash_state=state, sha256=pyenv.sha256_file(ctx.target_path))
        return state != "unknown"

    def _s8_status_check(self, ctx: RunContext, name: str) -> bool:
        runner = self._fault("s8_status_runner", ctx=ctx, check=name) or subprocess.run
        verdict, status_fields = self._recorded_status(ctx, f"S8-{name}", runner)
        if verdict is None:
            ctx.s8_checks[name] = CHECK_INDETERMINATE
            ctx.journal.append("S8", name, **status_fields)
            return False
        ctx.s8_checks[name] = CHECK_OK if verdict.clean else CHECK_FAILED
        ctx.journal.append("S8", name, **status_fields)
        return True

    def _s8_command_check(self, ctx: RunContext, name: str, command: Command) -> bool:
        self._fault("before_" + name, ctx=ctx)
        result, report = self._run_attested(ctx, "S8", command, ctx.digests_baseline)
        if result.timed_out:
            if self._hash_state(ctx) == "unknown":
                ctx.s8_checks[name] = CHECK_INDETERMINATE
                ctx.journal.append("S8", name, timed_out=True, hash_state="unknown",
                                   sha256=pyenv.sha256_file(ctx.target_path))
                return False
            ctx.s8_checks[name] = CHECK_FAILED
        elif result.returncode != 0 or not report.ok:
            ctx.s8_checks[name] = CHECK_FAILED
        else:
            ctx.s8_checks[name] = CHECK_OK
        return True

    def _s8_verify(self, ctx: RunContext) -> None:
        ordered = [
            ("a_hash", lambda: self._s8_hash_check(ctx, "a_hash")),
            ("b_status", lambda: self._s8_status_check(ctx, "b_status")),
            ("c_designated", lambda: self._s8_command_check(ctx, "c_designated", ctx.spec.designated)),
            ("d_end_to_end", lambda: self._s8_command_check(ctx, "d_end_to_end", ctx.spec.end_to_end)),
            ("e_final_hash", lambda: self._s8_hash_check(ctx, "e_final_hash")),
            ("f_final_status", lambda: self._s8_status_check(ctx, "f_final_status")),
        ]
        stop = False
        for name, check in ordered:
            if stop:
                ctx.s8_checks[name] = CHECK_NOT_RUN
                continue
            if not check():
                stop = True  # an indeterminate state: no further code runs in this worktree
            elif name == "a_hash" and ctx.s8_checks[name] == CHECK_FAILED:
                stop = True  # restore did not happen; do not run gates on mutated code
        ctx.restoration = combine_restoration(ctx.restoration, decide_restoration(ctx.s8_checks))
        ctx.journal.append("S8", "restoration decided", checks=ctx.s8_checks, status=ctx.restoration)

    # exceptions ---------------------------------------------------------

    def _on_exception(self, ctx: RunContext, exc: BaseException) -> None:
        ctx.failures.append(f"{type(exc).__name__}: {exc}")
        try:
            ctx.journal.append("EXCEPTION", type(exc).__name__, error=str(exc),
                               mutation_intended=ctx.mutation_intended)
        except BaseException:  # noqa: BLE001
            pass
        if ctx.outcome is None:
            ctx.outcome = VOID
        if not ctx.mutation_intended:
            ctx.restoration = ctx.restoration or NOT_APPLICABLE
            return
        # Amendment A: an interruption or exception after the mutation write was intended
        # is INDETERMINATE. The emergency restore below is a safety action and evidence
        # collection only; it never upgrades the status.
        ctx.restoration = combine_restoration(ctx.restoration, INDETERMINATE)
        try:
            self._emergency_restore(ctx)
        except BaseException as inner:  # noqa: BLE001
            ctx.failures.append(f"emergency restore failed: {inner!r}")

    def _emergency_restore(self, ctx: RunContext) -> None:
        state = self._hash_state(ctx)
        backup_ok = (ctx.backup_path is not None and ctx.backup_path.exists()
                     and pyenv.sha256_file(ctx.backup_path) == ctx.baseline_sha256)
        restore_action = "none"
        if state == "mutated" and backup_ok:
            with open(ctx.target_path, "wb") as handle:
                handle.write(ctx.backup_path.read_bytes())
                handle.flush()
                os.fsync(handle.fileno())
            restore_action = "restored from backup"
        after = self._hash_state(ctx)
        ctx.journal.append("EMERGENCY", "restore attempt (evidence only, no status upgrade)",
                           before=state, backup_verified=backup_ok, restore_action=restore_action,
                           after=after)

    # S9 ---------------------------------------------------------------

    def _finalize(self, ctx: RunContext) -> dict:
        if ctx.restoration is None:
            ctx.restoration = INDETERMINATE if ctx.mutation_intended else NOT_APPLICABLE
        if ctx.outcome is None:
            ctx.outcome = VOID
        quarantined = False
        if ctx.mutation_intended and ctx.restoration != RESTORED_VERIFIED:
            quarantined = self._quarantine(ctx)
        target_final = None
        if ctx.target_path is not None and ctx.target_path.exists():
            target_final = pyenv.sha256_file(ctx.target_path)
        result = {
            "evidence_schema": EVIDENCE_SCHEMA,
            "run_id": ctx.spec.run_id,
            "outcome": ctx.outcome,
            "restoration_status": ctx.restoration,
            "experiment_validity": None,
            "batch_action": None,
            "s8_checks": ctx.s8_checks,
            "attestation_ok": ctx.attestation_ok,
            "mutation_applied": ctx.mutation_intended,
            "target_sha256": {"baseline": ctx.baseline_sha256, "mutated": ctx.mutated_sha256,
                              "final": target_final},
            "observations": ctx.observations,
            "failures": ctx.failures,
            "quarantined": quarantined,
            "evidence_dir": str(ctx.run_dir),
            "validity_condition": "authoritative only when validate_run_evidence() reports COMPLETE: "
                                  "journal.jsonl must end with the S9 FINAL record whose candidate_sha256 "
                                  "equals this file's sha256, and FINALIZATION_FAILED.json must be absent",
        }
        provisional = derive_validity(ctx.outcome, ctx.restoration, ctx.attestation_ok, True)
        result["experiment_validity"] = provisional
        result["batch_action"] = CONTINUE if provisional == VALID else HALT
        result["cleanup_eligible"] = provisional == VALID and ctx.restoration in (RESTORED_VERIFIED,
                                                                                    NOT_APPLICABLE)
        result["cleanup_status"] = ("ELIGIBLE-RETAINED-BY-POLICY" if result["cleanup_eligible"]
                                    else "INELIGIBLE-RETAINED")
        result["evidence_complete"] = True
        result["finalization"] = {"protocol": FINALIZATION_PROTOCOL, "authoritative_name": RESULT_NAME,
                                  "binding": "journal.jsonl last record S9/FINAL candidate_sha256"}
        # WP-RD-B-F1 two-phase publication. Stage A: pending candidate. Stage B: durable,
        # verified FINAL record binding the candidate. Stage C: atomic no-replace
        # publication. Stage D: consumer-contract confirmation. A VALID result.json can
        # only exist after Stage B has succeeded.
        stage = "prepare"
        try:
            ctx.journal.append("S9", "intent: finalize evidence (two-phase)", provisional_validity=provisional)
            self._fault("before_finalize", ctx=ctx)
            # WP-RD-B-F2: bind the journal so far (FINAL is excluded, so nothing is circular).
            result["evidence_binding"] = {"journal_prefix_sha256": pyenv.sha256_file(ctx.journal.path),
                                          "pre_json_sha256": ctx.pre_json_sha256}
            data = json.dumps(result, indent=2, sort_keys=True, default=str).encode("utf-8")
            candidate = json.loads(data)
            candidate_sha = pyenv.sha256_bytes(data)
            stage = "pending-write"
            pending = ctx.run_dir / PENDING_NAME
            replacement = self._fault("pending_write", ctx=ctx, data=data)
            _fsync_write(pending, data if replacement is None else replacement)
            _fsync_dir(ctx.run_dir)
            self._fault("after_pending", ctx=ctx, path=pending)
            stage = "pending-verify"
            if pyenv.sha256_file(pending) != candidate_sha:
                raise FinalizationError("pending candidate does not match the intended result bytes")
            stage = "final-journal"
            self._append_final(ctx, candidate_sha)
            stage = "final-verify"
            self._verify_journal_tail(ctx)
            self._fault("after_final", ctx=ctx)
            stage = "publish"
            self._publish(ctx, pending)
            stage = "confirm"
            status = validate_run_evidence(ctx.run_dir)
            if not status["complete"] or status["result"] != candidate:
                raise FinalizationError(f"published result failed the consumer contract: {status['reasons']}")
        except BaseException as exc:  # noqa: BLE001 - every failure is fail-closed below
            return self._finalization_failed(ctx, result, stage, exc, quarantined)
        return candidate

    def _append_final(self, ctx: RunContext, candidate_sha: str) -> dict:
        def sync(fd):
            self._fault("final_fsync", ctx=ctx, fd=fd)
            os.fsync(fd)

        return ctx.journal.append(
            "S9", "FINAL", _sync_fn=sync, run_id=ctx.spec.run_id, candidate_sha256=candidate_sha,
            result_sha256=candidate_sha,
            meaning="mandatory evidence finalized; result.json is published only AFTER this record "
                    "is durable, as a hard link to the bound pending candidate")

    def _verify_journal_tail(self, ctx: RunContext) -> None:
        expected = ctx.journal.last_line.encode("utf-8")
        if not expected or not ctx.journal.path.read_bytes().endswith(expected):
            raise FinalizationError("the FINAL record is not durably present at the end of the journal")

    def _publish(self, ctx: RunContext, pending: Path) -> None:
        result_path = ctx.run_dir / RESULT_NAME
        self._fault("publish", ctx=ctx)
        os.link(pending, result_path)  # atomic, same directory; refuses an existing result.json
        ctx.published = True
        self._fault("after_publish", ctx=ctx)
        _fsync_dir(ctx.run_dir)
        if not os.path.samefile(pending, result_path):
            raise FinalizationError("result.json is not the bound pending candidate")

    def _finalization_failed(self, ctx: RunContext, result: dict, stage: str, exc: BaseException,
                             quarantined: bool) -> dict:
        """Fail closed: INVALID / HALT. Never leave a newly published VALID result.json behind."""

        ctx.failures.append(f"S9 evidence finalisation failed at {stage}: {exc!r}")
        failure = dict(result)
        failure["failures"] = ctx.failures
        failure["evidence_complete"] = False
        failure["experiment_validity"] = derive_validity(ctx.outcome, ctx.restoration, ctx.attestation_ok, False)
        failure["batch_action"] = HALT
        failure["cleanup_eligible"] = False
        failure["cleanup_status"] = "INELIGIBLE-RETAINED"
        if ctx.mutation_intended and not quarantined:
            failure["quarantined"] = self._quarantine(ctx)
        detail = {"protocol": FINALIZATION_PROTOCOL, "state": "FAILED", "stage": stage, "error": repr(exc),
                  "published_before_failure": ctx.published}
        if ctx.published:
            # Retract our own just-published result (its bytes stay in the pending candidate).
            try:
                os.unlink(ctx.run_dir / RESULT_NAME)
                _fsync_dir(ctx.run_dir)
                detail["retracted_published_result"] = True
            except BaseException as inner:  # noqa: BLE001
                detail["retracted_published_result"] = False
                detail["retraction_error"] = repr(inner)
        failure["finalization"] = detail
        try:
            _fsync_write(ctx.run_dir / FAILED_NAME,
                         json.dumps(failure, indent=2, sort_keys=True, default=str).encode("utf-8"))
            detail["failure_marker_written"] = True
        except BaseException as inner:  # noqa: BLE001
            detail["failure_marker_written"] = False
            detail["failure_marker_error"] = repr(inner)
        try:
            ctx.journal.append("S9", "FINALIZATION-FAILED", stage=stage, error=repr(exc))
        except BaseException:  # noqa: BLE001
            pass
        if (ctx.published and not detail.get("retracted_published_result")
                and not detail["failure_marker_written"]):
            detail["state"] = "UNCERTAIN"
        return failure

    def _quarantine(self, ctx: RunContext) -> bool:
        quarantine = self._require_under_root(Path(self.config.quarantine_dir), "quarantine_dir")
        marker = {"run_id": ctx.spec.run_id, "worktree": str(ctx.worktree),
                  "restoration_status": ctx.restoration, "evidence_dir": str(ctx.run_dir),
                  "instruction": "Do not reuse this worktree; removal requires owner authorization."}
        try:
            _fsync_write(quarantine / f"{ctx.spec.run_id}.json",
                         json.dumps(marker, indent=2, sort_keys=True).encode("utf-8"))
        except OSError as exc:
            ctx.failures.append(f"quarantine marker could not be written: {exc}")
            return False
        return True

    @staticmethod
    def _all_commands(spec: ExperimentSpec) -> list:
        commands = [spec.designated, spec.end_to_end, *spec.baseline_gates, *spec.excluded]
        if spec.validator is not None:
            commands.append(spec.validator)
        if spec.precheck is not None:
            commands.append(spec.precheck)
        return commands


# ------------------------------------------------------------------ registration helpers

def _apply_edits(baseline: bytes, edits) -> bytes:
    """Apply registered whole-line edits in memory. Each `old` line must occur exactly
    once, at its registered line number."""

    lines = baseline.split(b"\n")
    for edit in edits:
        old, new = edit.old.encode("utf-8"), edit.new.encode("utf-8")
        hits = [index for index, line in enumerate(lines) if line == old]
        if hits != [edit.line - 1]:
            raise HarnessRefused(f"edit at L{edit.line}: expected exactly one whole-line match there, "
                                 f"found {[h + 1 for h in hits]}")
        lines[edit.line - 1] = new
    return b"\n".join(lines)


def _spec_dict(spec: ExperimentSpec) -> dict:
    return json.loads(json.dumps(asdict(spec), default=str))
