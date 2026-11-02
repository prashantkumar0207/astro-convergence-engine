"""Python process isolation, interpreter probing and code-identity attestation evaluation
(WP-RD-B, R1 s7.3 with CEO Amendment A and the implementation clarification on prefixes).

Isolation guarantee actually provided: each top-level command (one process tree) runs
with ONE fresh, empty PYTHONPYCACHEPREFIX directory and PYTHONDONTWRITEBYTECODE=1, both
inherited by every child. The prefix must still be empty afterwards. This is a
per-process-TREE guarantee, not a per-process one.

Code identity is compared structurally (canon()), never by marshal bytes.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import signal
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path

HOOK_DIR = Path(__file__).resolve().parent / "attest_hook"
HOOK_FILE = HOOK_DIR / "sitecustomize.py"

#: Base-environment variables that would defeat or alter the isolation protocol.
FORBIDDEN_ENV = (
    "PYTHONPATH",
    "PYTHONSAFEPATH",
    "PYTHONOPTIMIZE",
    "PYTHONPYCACHEPREFIX",
    "PYTHONDONTWRITEBYTECODE",
    "PYTHONINSPECT",
)
FORBIDDEN_ENV_PREFIXES = ("ACE_ATTEST_",)
#: Interpreter short flags that disable environment handling, site, or change code objects.
FORBIDDEN_SHORT_FLAGS = frozenset("IESO")
#: Modules the hook adds to sys.modules at start-up (verified by test E6).
HOOK_START_MODULES = frozenset({"sitecustomize", "atexit"})

_RECORD_NAME = re.compile(r"(\d+)\.(start|end|hookerror)\.json\Z")


class EnvironmentRefused(Exception):
    """The interpreter, command or environment does not satisfy the isolation protocol."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path) -> str:
    return sha256_bytes(Path(path).read_bytes())


# ------------------------------------------------------------------ validation

def verify_hook(hook_dir=HOOK_DIR, expected_sha256: str | None = None) -> str:
    """The hook directory must contain exactly sitecustomize.py, with the expected hash."""

    hook_dir = Path(hook_dir)
    entries = sorted(entry.name for entry in hook_dir.iterdir())
    if entries != ["sitecustomize.py"]:
        raise EnvironmentRefused(f"hook directory must contain only sitecustomize.py, found {entries}")
    digest = sha256_file(hook_dir / "sitecustomize.py")
    if expected_sha256 is not None and digest != expected_sha256:
        raise EnvironmentRefused(f"hook sha256 {digest} != registered {expected_sha256}")
    return digest


def check_argv(argv, python: str) -> None:
    """Refuse commands that would bypass the protocol (-I, -E, -S, -O, -X pycache_prefix)."""

    if not argv or str(argv[0]) != str(python):
        raise EnvironmentRefused(f"argv[0] must be the registered interpreter {python}: {argv!r}")
    index = 1
    while index < len(argv):
        arg = str(argv[index])
        if arg in ("-c", "-m") or not arg.startswith("-") or arg == "-":
            return
        if arg.startswith("--"):
            index += 1
            continue
        if arg.startswith("-X"):
            value = arg[2:] or (str(argv[index + 1]) if index + 1 < len(argv) else "")
            if value.startswith("pycache_prefix"):
                raise EnvironmentRefused(f"-X pycache_prefix is refused: {argv!r}")
            index += 1 if arg[2:] else 2
            continue
        if FORBIDDEN_SHORT_FLAGS & set(arg[1:]):
            raise EnvironmentRefused(f"interpreter flag {arg} is refused: {argv!r}")
        index += 1


def validate_base_env(env: dict) -> None:
    bad = [key for key in env if key in FORBIDDEN_ENV or key.startswith(FORBIDDEN_ENV_PREFIXES)]
    if bad:
        raise EnvironmentRefused(f"base environment contains protocol-defeating variables: {sorted(bad)}")


def fresh_dir(parent, name: str) -> Path:
    """Create a new, empty, owner-only directory; it must not already exist."""

    path = Path(parent) / name
    path.mkdir(exist_ok=False)
    os.chmod(path, 0o700)
    if any(path.iterdir()):
        raise EnvironmentRefused(f"fresh directory is not empty: {path}")
    return path


def tree_listing(path) -> list[str]:
    root = Path(path)
    return sorted(str(item.relative_to(root)) for item in root.rglob("*"))


def build_env(base_env: dict, cache_dir, attest_out=None, targets=(), phase: str = "",
              hook_dir=HOOK_DIR) -> dict:
    """The protocol environment. `targets` is an iterable of (module, qualname)."""

    validate_base_env(base_env)
    env = dict(base_env)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPYCACHEPREFIX"] = str(cache_dir)
    if attest_out is not None:
        env["PYTHONPATH"] = str(hook_dir)
        env["ACE_ATTEST_OUT"] = str(attest_out)
        env["ACE_ATTEST_TARGETS"] = ";".join(f"{module}:{qualname}" for module, qualname in targets)
        env["ACE_ATTEST_PHASE"] = phase
    return env


# ------------------------------------------------------------------ processes

@dataclass
class ProcessResult:
    argv: list
    cwd: str
    pid: int
    returncode: int
    timed_out: bool
    stdout: bytes
    stderr: bytes
    seconds: float

    def summary(self) -> dict:
        return {"argv": [str(a) for a in self.argv], "cwd": self.cwd, "pid": self.pid,
                "returncode": self.returncode, "timed_out": self.timed_out,
                "stdout_sha256": sha256_bytes(self.stdout), "stderr_sha256": sha256_bytes(self.stderr),
                "seconds": round(self.seconds, 3)}


def run_process(argv, cwd, env: dict, timeout: float) -> ProcessResult:
    """Run in a new session; on timeout or interruption kill the whole process group."""

    started = time.monotonic()
    proc = subprocess.Popen([str(a) for a in argv], cwd=str(cwd), env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, start_new_session=True)
    timed_out = False
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        _kill_group(proc.pid)
        out, err = proc.communicate()
    except BaseException:
        _kill_group(proc.pid)
        proc.communicate()
        raise
    return ProcessResult(list(argv), str(cwd), proc.pid, proc.returncode, timed_out, out, err,
                         time.monotonic() - started)


def _kill_group(pid: int) -> None:
    try:
        os.killpg(pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


# ------------------------------------------------------------------ probe

PROBE_CODE = r"""
import importlib.util, json, sys
def origin(name):
    if name in sys.modules:
        return getattr(sys.modules[name], "__file__", None)
    try:
        spec = importlib.util.find_spec(name)
    except Exception as exc:
        return "error:" + repr(exc)
    return None if spec is None else spec.origin
f = sys.flags
print(json.dumps({"version": sys.version, "executable": sys.executable,
    "flags": {"isolated": f.isolated, "ignore_environment": f.ignore_environment, "no_site": f.no_site,
              "optimize": f.optimize, "dont_write_bytecode": f.dont_write_bytecode},
    "pycache_prefix": sys.pycache_prefix,
    "sitecustomize_loaded": "sitecustomize" in sys.modules,
    "sitecustomize": origin("sitecustomize"), "usercustomize": origin("usercustomize")}))
"""


def probe_report(python, env: dict, cwd, extra_flags=(), timeout: float = 60) -> dict:
    result = run_process([python, *extra_flags, "-c", PROBE_CODE], cwd, env, timeout)
    if result.returncode != 0 or result.timed_out:
        raise EnvironmentRefused(f"interpreter probe failed: rc={result.returncode} {result.stderr[-400:]!r}")
    return json.loads(result.stdout.decode("utf-8").strip().splitlines()[-1])


def check_probe(report: dict, cache_dir, hooked: bool, hook_file=HOOK_FILE) -> list[str]:
    failures = []
    flags = report["flags"]
    for name in ("isolated", "ignore_environment", "no_site", "optimize"):
        if flags[name] != 0:
            failures.append(f"sys.flags.{name} = {flags[name]}, expected 0")
    if flags["dont_write_bytecode"] != 1:
        failures.append("sys.flags.dont_write_bytecode is not set")
    if report["pycache_prefix"] != str(cache_dir):
        failures.append(f"pycache_prefix {report['pycache_prefix']!r} != {str(cache_dir)!r}")
    if hooked:
        if not report["sitecustomize_loaded"] or report["sitecustomize"] != str(hook_file):
            failures.append(f"attestation hook not active: sitecustomize={report['sitecustomize']!r}")
    else:
        for name in ("sitecustomize", "usercustomize"):
            if report[name] is not None:
                failures.append(f"pre-existing {name} importable without the hook: {report[name]!r}")
    return failures


def preflight(python, base_env: dict, work_dir, hook_sha256: str, hook_dir=HOOK_DIR) -> dict:
    """Both probes must pass before any experiment starts (R1 s7.3.4g)."""

    verify_hook(hook_dir, hook_sha256)
    work_dir = Path(work_dir)
    plain_cache = fresh_dir(work_dir, "probe-cache-plain")
    plain = probe_report(python, build_env(base_env, plain_cache), work_dir)
    failures = check_probe(plain, plain_cache, hooked=False, hook_file=Path(hook_dir) / "sitecustomize.py")
    hooked_cache = fresh_dir(work_dir, "probe-cache-hooked")
    hooked_out = fresh_dir(work_dir, "probe-attest")
    hooked = probe_report(python, build_env(base_env, hooked_cache, hooked_out, (), "probe", hook_dir), work_dir)
    failures += check_probe(hooked, hooked_cache, hooked=True, hook_file=Path(hook_dir) / "sitecustomize.py")
    records = tree_listing(hooked_out)
    if not any(name.endswith(".start.json") for name in records) or not any(
            name.endswith(".end.json") for name in records):
        failures.append(f"attestation hook wrote no start/end record in the probe: {records}")
    for cache in (plain_cache, hooked_cache):
        if tree_listing(cache):
            failures.append(f"probe cache not empty: {cache}")
    if failures:
        raise EnvironmentRefused("; ".join(failures))
    return {"plain": plain, "hooked": hooked, "hook_sha256": hook_sha256}


# ------------------------------------------------------------------ structural identity

def canon(code):
    """Structural identity of a code object (identical to the hook's _canon)."""

    consts = tuple(canon(c) if hasattr(c, "co_code") else ("const", type(c).__name__, repr(c))
                   for c in code.co_consts)
    return (code.co_name, code.co_qualname, code.co_argcount, code.co_posonlyargcount,
            code.co_kwonlyargcount, code.co_flags, code.co_code, code.co_names, code.co_varnames,
            code.co_freevars, code.co_cellvars, code.co_firstlineno, tuple(code.co_lines()),
            tuple(code.co_positions()), consts)


def code_digest(code) -> str:
    return sha256_bytes(repr(canon(code)).encode("utf-8"))


def find_code(code, qualname: str):
    if code.co_qualname == qualname:
        return code
    for const in code.co_consts:
        if hasattr(const, "co_code"):
            found = find_code(const, qualname)
            if found is not None:
                return found
    return None


def expected_digest(source: bytes, qualname: str, filename: str = "<expected>") -> str:
    """Digest the function `qualname` would have if `source` were what the process loaded."""

    module_code = compile(source, filename, "exec", dont_inherit=True, optimize=0)
    found = find_code(module_code, qualname)
    if found is None:
        raise EnvironmentRefused(f"qualname {qualname} not found in expected source")
    return code_digest(found)


# ------------------------------------------------------------------ attestation evaluation

@dataclass(frozen=True)
class ChildExpectation:
    """Registered count of DIRECT Python children of the attested command. There is no
    default: None for the relevant case fails closed."""

    on_pass: int | None = None
    min_on_fail: int | None = None


@dataclass
class AttestationPlan:
    targets: tuple = ()                       # ((module, qualname), ...)
    expected_digests: dict = field(default_factory=dict)  # (module, qualname) -> digest
    required_load: dict = field(default_factory=dict)     # (module, qualname) -> main|child|any|none
    children: ChildExpectation = ChildExpectation()
    hook_sha256: str = ""
    cache_dir: str = ""                       # the prefix the processes must have reported
    cache_listing_path: str = ""              # where to inspect it, if the evidence has moved


@dataclass
class AttestationReport:
    ok: bool
    failures: list
    main_pid: int
    children: list
    directly_attested_children: list
    processes: dict

    def summary(self) -> dict:
        return {"ok": self.ok, "failures": self.failures, "main_pid": self.main_pid,
                "children": self.children, "directly_attested_children": self.directly_attested_children,
                "processes": self.processes}


def load_records(out_dir) -> tuple[dict, list]:
    """{pid: {"start": rec, "end": rec, "hookerror": rec}} plus a list of failures."""

    records: dict = {}
    failures: list = []
    for path in sorted(Path(out_dir).iterdir()):
        match = _RECORD_NAME.match(path.name)
        if match is None:
            failures.append(f"unexpected file in attestation directory: {path.name}")
            continue
        pid, kind = int(match.group(1)), match.group(2)
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            failures.append(f"malformed attestation record {path.name}: {exc}")
            continue
        if not isinstance(record, dict) or record.get("kind") != kind or record.get("pid") != pid:
            failures.append(f"attestation record {path.name} does not match its name")
            continue
        records.setdefault(pid, {})[kind] = record
    return records, failures


def evaluate_attestation(out_dir, main_pid: int, returncode: int, plan: AttestationPlan) -> AttestationReport:
    records, failures = load_records(out_dir)
    for pid, kinds in records.items():
        if "hookerror" in kinds:
            failures.append(f"pid {pid}: hook error {kinds['hookerror'].get('error')!r}")
    starts = {pid: kinds["start"] for pid, kinds in records.items() if "start" in kinds}
    ends = {pid: kinds["end"] for pid, kinds in records.items() if "end" in kinds}

    if main_pid not in starts:
        failures.append(f"main pid {main_pid}: missing start record")
    if main_pid not in ends:
        failures.append(f"main pid {main_pid}: missing end record (no normal interpreter shutdown)")
    for pid in sorted(set(starts) - set(ends)):
        failures.append(f"pid {pid}: start record without end record")
    for pid in sorted(set(ends) - set(starts)):
        failures.append(f"pid {pid}: end record without start record")

    for pid, start in starts.items():
        if pid == main_pid:
            continue
        seen, cursor = set(), pid
        while cursor != main_pid:
            if cursor in seen or cursor not in starts:
                failures.append(f"pid {pid}: outside the observed process tree")
                break
            seen.add(cursor)
            cursor = starts[cursor].get("ppid")

    children = sorted(pid for pid, start in starts.items() if pid != main_pid and start.get("ppid") == main_pid)
    expectation = plan.children
    if returncode == 0:
        if expectation.on_pass is None:
            failures.append("no registered child-process expectation for a passing run")
        elif len(children) != expectation.on_pass:
            failures.append(f"expected {expectation.on_pass} direct Python children, observed {len(children)}")
    else:
        if expectation.min_on_fail is None:
            failures.append("no registered child-process expectation for a failing run")
        elif len(children) < expectation.min_on_fail:
            failures.append(f"expected at least {expectation.min_on_fail} direct Python children, "
                            f"observed {len(children)}")

    for pid, start in starts.items():
        flags = start.get("flags", {})
        for name in ("isolated", "ignore_environment", "no_site", "optimize"):
            if flags.get(name) != 0:
                failures.append(f"pid {pid}: sys.flags.{name} = {flags.get(name)!r}")
        if flags.get("dont_write_bytecode") != 1:
            failures.append(f"pid {pid}: dont_write_bytecode not set")
        if start.get("pycache_prefix") != plan.cache_dir:
            failures.append(f"pid {pid}: pycache_prefix {start.get('pycache_prefix')!r} != {plan.cache_dir!r}")

    loaders = {target: set() for target in plan.targets}
    for pid, end in ends.items():
        if end.get("hook_sha256") != plan.hook_sha256:
            failures.append(f"pid {pid}: hook sha256 mismatch")
        entries = end.get("targets")
        if not isinstance(entries, list):
            failures.append(f"pid {pid}: end record has no target list")
            continue
        listed = {(e.get("module"), e.get("qualname")) for e in entries if isinstance(e, dict)}
        if listed != set(plan.targets):
            failures.append(f"pid {pid}: target list {sorted(listed)} != registered {sorted(plan.targets)}")
        for entry in entries:
            if not isinstance(entry, dict):
                failures.append(f"pid {pid}: malformed target entry")
                continue
            target = (entry.get("module"), entry.get("qualname"))
            if entry.get("loaded") is not True:
                if entry.get("loaded") is not False:
                    failures.append(f"pid {pid}: target {target} has no loaded flag")
                continue
            if entry.get("resolved") is not True:
                failures.append(f"pid {pid}: target {target} loaded but not resolvable")
                continue
            if "disk_match" not in entry or "loaded_digest" not in entry:
                failures.append(f"pid {pid}: target {target} attestation fields missing")
                continue
            if entry["loaded_digest"] != plan.expected_digests.get(target):
                failures.append(f"pid {pid}: target {target} loaded code differs from the expected text")
            if entry["disk_match"] is not True:
                failures.append(f"pid {pid}: target {target} loaded code differs from the source on disk")
            if target in loaders:
                loaders[target].add(pid)

    for target, role in plan.required_load.items():
        who = loaders.get(target, set())
        if role == "main" and main_pid not in who:
            failures.append(f"target {target} not loaded by the main process")
        elif role == "child" and not (who - {main_pid}):
            failures.append(f"target {target} not loaded by any child process")
        elif role == "any" and not who:
            failures.append(f"target {target} not loaded by any process")

    listing_path = plan.cache_listing_path or plan.cache_dir
    if listing_path and tree_listing(listing_path):
        failures.append(f"pycache prefix not empty after the run: {tree_listing(listing_path)[:5]}")

    direct = [pid for pid in children if pid in ends and pid in starts]
    processes = {str(pid): {"ppid": starts.get(pid, {}).get("ppid"), "has_start": pid in starts,
                            "has_end": pid in ends} for pid in sorted(set(starts) | set(ends))}
    return AttestationReport(not failures, failures, main_pid, children, direct, processes)
