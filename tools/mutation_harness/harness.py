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
import signal
import subprocess
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path

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

def _fsync_write(path: Path, data: bytes) -> None:
    with open(path, "xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


class Journal:
    """Append-only write-ahead journal, one JSON object per line, fsynced per record."""

    def __init__(self, path: Path):
        self.path = path
        self.seq = 0
        _fsync_write(path, b"")

    def append(self, state: str, action: str, **data) -> dict:
        self.seq += 1
        record = {"seq": self.seq, "state": state, "action": action, **data}
        line = json.dumps(record, sort_keys=True, default=str) + "\n"
        with open(self.path, "a", encoding="utf-8") as handle:
            handle.write(line)
            handle.flush()
            os.fsync(handle.fileno())
        return record


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
        ctx.journal.append(phase, f"result {command.name}", process=result.summary(),
                           attestation=report.summary(), label=label)
        return result, report

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
            self._experiment_body(ctx)
        except BaseException as exc:  # noqa: BLE001 - every exit path is journalled and fail-closed
            self._on_exception(ctx, exc)
        finally:
            signal.signal(signal.SIGTERM, previous)
        return self._finalize(ctx)

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
                           mutated_sha256=ctx.mutated_sha256, probe=report)
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
        ctx.journal.append("S1", "preregistered", pre_json_sha256=pyenv.sha256_bytes(data))

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
        if self._hash_state(ctx) != "baseline":
            ok = False
            ctx.failures.append("S2 baseline changed the target file")
        try:
            verdict = gitstatus.status_verdict(ctx.worktree, spec.allow_list, frozenset(), self.config.git)
            if not verdict.clean:
                ok = False
                ctx.failures.append(f"S2 baseline left changes outside the allow-list: {verdict}")
        except (gitstatus.GitStatusError, gitstatus.StatusParseError) as exc:
            ok = False
            ctx.failures.append(f"S2 status unavailable: {exc}")
        ctx.journal.append("S2", "baseline evaluated", clean=ok)
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
        ctx.journal.append("S5", "mutation written", hash_state=state)
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
        ctx.journal.append("S6", "outcome recorded", outcome=ctx.outcome, invalidations=invalid)

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
        ctx.journal.append("S8", name, hash_state=state)
        return state != "unknown"

    def _s8_status_check(self, ctx: RunContext, name: str) -> bool:
        runner = self._fault("s8_status_runner", ctx=ctx, check=name) or subprocess.run
        try:
            verdict = gitstatus.status_verdict(ctx.worktree, ctx.spec.allow_list, frozenset(),
                                               self.config.git, runner)
        except (gitstatus.GitStatusError, gitstatus.StatusParseError) as exc:
            ctx.s8_checks[name] = CHECK_INDETERMINATE
            ctx.journal.append("S8", name, error=str(exc))
            return False
        ctx.s8_checks[name] = CHECK_OK if verdict.clean else CHECK_FAILED
        ctx.journal.append("S8", name, verdict=asdict(verdict))
        return True

    def _s8_command_check(self, ctx: RunContext, name: str, command: Command) -> bool:
        self._fault("before_" + name, ctx=ctx)
        result, report = self._run_attested(ctx, "S8", command, ctx.digests_baseline)
        if result.timed_out:
            if self._hash_state(ctx) == "unknown":
                ctx.s8_checks[name] = CHECK_INDETERMINATE
                ctx.journal.append("S8", name, timed_out=True, hash_state="unknown")
                return False
            ctx.s8_checks[name] = CHECK_FAILED
        elif result.returncode != 0 or not report.ok:
            ctx.s8_checks[name] = CHECK_FAILED
        else:
            ctx.s8_checks[name] = CHECK_OK
        if not report.ok:
            ctx.attestation_ok = False
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
            "validity_condition": "VALID only if journal.jsonl ends with a FINAL record carrying this "
                                  "file's sha256",
        }
        provisional = derive_validity(ctx.outcome, ctx.restoration, ctx.attestation_ok, True)
        result["experiment_validity"] = provisional
        result["batch_action"] = CONTINUE if provisional == VALID else HALT
        result["cleanup_eligible"] = provisional == VALID and ctx.restoration in (RESTORED_VERIFIED,
                                                                                    NOT_APPLICABLE)
        result["cleanup_status"] = ("ELIGIBLE-RETAINED-BY-POLICY" if result["cleanup_eligible"]
                                    else "INELIGIBLE-RETAINED")
        evidence_ok = True
        try:
            ctx.journal.append("S9", "intent: write result.json", provisional_validity=provisional)
            self._fault("before_finalize", ctx=ctx)
            data = json.dumps(result, indent=2, sort_keys=True, default=str).encode("utf-8")
            _fsync_write(ctx.run_dir / "result.json", data)
            reread = pyenv.sha256_file(ctx.run_dir / "result.json")
            if reread != pyenv.sha256_bytes(data):
                raise OSError("result.json re-read hash mismatch")
            ctx.journal.append("S9", "FINAL", result_sha256=reread)
        except BaseException as exc:  # noqa: BLE001
            evidence_ok = False
            ctx.failures.append(f"S9 evidence finalisation failed: {exc!r}")
        if not evidence_ok:
            result["failures"] = ctx.failures
            result["evidence_complete"] = False
            result["experiment_validity"] = derive_validity(ctx.outcome, ctx.restoration,
                                                            ctx.attestation_ok, False)
            result["batch_action"] = HALT
            result["cleanup_eligible"] = False
            result["cleanup_status"] = "INELIGIBLE-RETAINED"
            if ctx.mutation_intended and not quarantined:
                result["quarantined"] = self._quarantine(ctx)
        else:
            result["evidence_complete"] = True
        return result

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
