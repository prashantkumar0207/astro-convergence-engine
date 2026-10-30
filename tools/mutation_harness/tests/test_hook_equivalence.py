"""Attestation-hook equivalence suite E1-E14 (R1 s7.3.7, RD-C6).

Every fixture is run twice with identical argv, cwd and protocol environment, except the
hook variables: U = unhooked, H = hooked. All fixtures are harmless disposable scripts in a
temporary directory; no ACE certifier is executed.
"""

import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import helpers  # noqa: E402
import pyenv  # noqa: E402

FIXTURES = {
    "fx_ok.py": "import sys\nprint('out-ok')\nprint('err-ok', file=sys.stderr)\n",
    "fx_exit3.py": "import sys\nprint('before-exit')\nsys.exit(3)\n",
    "fx_raise.py": "print('before-raise')\nraise ValueError('fixture failure')\n",
    "fx_probe.py": (
        "import json, sys\n"
        "json.dump({'argv': sys.argv, 'name': __name__, 'file': __file__, 'spec': repr(__spec__),\n"
        "           'path': sys.path, 'modules': sorted(sys.modules)}, open(sys.argv[1], 'w'))\n"),
    "fx_child.py": ("import subprocess, sys\n"
                    "r = subprocess.run([sys.executable, 'fx_ok.py'])\nsys.exit(r.returncode)\n"),
    "fx_child_isolated.py": ("import subprocess, sys\n"
                             "r = subprocess.run([sys.executable, '-I', 'fx_ok.py'])\nsys.exit(r.returncode)\n"),
    "fx_two_children.py": ("import subprocess, sys\n"
                           "for _ in range(2):\n    subprocess.run([sys.executable, 'fx_ok.py'], check=True)\n"),
    "fx_hang.py": "import time\ntime.sleep(60)\n",
    "fx_sleep.py": "import sys, time\nprint('ready', flush=True)\ntime.sleep(30)\n",
    "fx_osexit.py": "import os\nprint('x', flush=True)\nos._exit(5)\n",
    "fx_target.py": "import pkgx.target as t\nprint(t.f(2, 3))\n",
    "pkgx/__init__.py": "",
    "pkgx/target.py": "def f(a, b):\n    return a * 10 + b\n",
}
TARGET = ("pkgx.target", "f")
PROBE_C = ("import json, sys; json.dump({'argv': sys.argv, 'name': __name__, 'path': sys.path, "
           "'modules': sorted(sys.modules)}, open(sys.argv[1], 'w'))")


@pytest.fixture
def work(tmp_path):
    root = tmp_path / "fx"
    for name, text in FIXTURES.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    return root


class Runner:
    def __init__(self, tmp):
        self.tmp = Path(tmp)
        self.count = 0

    def run(self, args, cwd, hooked, timeout=60, targets=(TARGET,), flags=()):
        self.count += 1
        cache = pyenv.fresh_dir(self.tmp, f"cache-{self.count}")
        out = pyenv.fresh_dir(self.tmp, f"attest-{self.count}") if hooked else None
        env = helpers.protocol_env(cache, out, targets if hooked else ())
        argv = [helpers.PYTHON, *flags, *args]
        result = pyenv.run_process(argv, cwd, env, timeout)
        return result, cache, out


@pytest.fixture
def runner(tmp_path):
    return Runner(tmp_path)


def evaluate(result, cache, out, on_pass=0, min_on_fail=0, targets=(TARGET,), expected=None, required=None):
    expected = expected if expected is not None else {
        TARGET: pyenv.expected_digest(FIXTURES["pkgx/target.py"].encode(), "f")}
    return pyenv.evaluate_attestation(out, result.pid, result.returncode,
                                      helpers.plan(cache, targets, expected, required or {}, on_pass, min_on_fail))


PARITY_CASES = [
    (["fx_ok.py"], 0), (["fx_exit3.py"], 3), (["fx_raise.py"], 1), (["fx_child.py"], 0),
    (["fx_osexit.py"], 5), (["-c", "import sys; print('c-ok'); sys.exit(0)"], 0), (["fx_target.py"], 0),
]


@pytest.mark.parametrize("args,expected_rc", PARITY_CASES, ids=[c[0][0] for c in PARITY_CASES])
def test_E1_E2_E3_exit_code_stdout_stderr_parity(runner, work, args, expected_rc):
    unhooked, _, _ = runner.run(args, work, hooked=False)
    hooked, _, _ = runner.run(args, work, hooked=True)
    assert unhooked.returncode == hooked.returncode == expected_rc
    assert unhooked.stdout == hooked.stdout
    assert unhooked.stderr == hooked.stderr


def _probe(runner, work, hooked, as_command):
    dump = runner.tmp / f"probe-{runner.count + 1}.json"
    args = ["-c", PROBE_C, str(dump)] if as_command else ["fx_probe.py", str(dump)]
    result, _, _ = runner.run(args, work, hooked=hooked)
    assert result.returncode == 0, result.stderr
    return json.loads(dump.read_text())


@pytest.mark.parametrize("as_command", [False, True], ids=["script", "dash-c"])
def test_E4_E5_E6_argv_name_path_and_imports(runner, work, as_command):
    unhooked = _probe(runner, work, False, as_command)
    hooked = _probe(runner, work, True, as_command)
    # E4: argv, __name__, __file__ and __spec__ identical (the dump path differs, so
    # compare argv[0] and the arity; the dump-file argument is per-run by construction).
    assert unhooked["argv"][0] == hooked["argv"][0] and len(unhooked["argv"]) == len(hooked["argv"])
    assert unhooked["name"] == hooked["name"] == "__main__"
    if not as_command:
        assert unhooked["file"] == hooked["file"] and unhooked["spec"] == hooked["spec"] == "None"
    # E5: exactly one extra sys.path entry, the hook directory, at index 1.
    assert hooked["path"] == unhooked["path"][:1] + [str(pyenv.HOOK_DIR)] + unhooked["path"][1:]
    # E6: the hook adds only its declared start-up modules and removes none.
    assert set(hooked["modules"]) - set(unhooked["modules"]) <= pyenv.HOOK_START_MODULES
    assert set(unhooked["modules"]) - set(hooked["modules"]) == set()


def test_E6_preexisting_sitecustomize_is_refused(tmp_path):
    """An interpreter on which some other sitecustomize is importable must be refused,
    because the hook would shadow it. Simulated by an extra path entry, built directly
    (build_env itself refuses a base PYTHONPATH)."""

    other = tmp_path / "other"
    other.mkdir()
    (other / "sitecustomize.py").write_text("")
    cache = pyenv.fresh_dir(tmp_path, "cache")
    env = helpers.protocol_env(cache)
    env["PYTHONPATH"] = str(other)
    report = pyenv.probe_report(helpers.PYTHON, env, tmp_path)
    failures = pyenv.check_probe(report, cache, hooked=False)
    assert any("pre-existing sitecustomize" in failure for failure in failures)
    with pytest.raises(pyenv.EnvironmentRefused):
        pyenv.build_env(dict(helpers.base_env(), PYTHONPATH=str(other)), cache)


def test_E7_normal_sys_exit_is_attested(runner, work):
    result, cache, out = runner.run(["fx_exit3.py"], work, hooked=True)
    assert result.returncode == 3
    assert (out / f"{result.pid}.start.json").exists() and (out / f"{result.pid}.end.json").exists()
    report = evaluate(result, cache, out)
    assert report.ok, report.failures


def test_E8_uncaught_exception_still_writes_end_record(runner, work):
    result, cache, out = runner.run(["fx_raise.py"], work, hooked=True)
    assert result.returncode == 1 and b"ValueError: fixture failure" in result.stderr
    assert (out / f"{result.pid}.end.json").exists()
    assert evaluate(result, cache, out).ok


def test_E9_timeout_kill_osexit_and_sigterm_fail_closed(runner, work):
    hung, cache, out = runner.run(["fx_hang.py"], work, hooked=True, timeout=2)
    assert hung.timed_out and hung.returncode == -signal.SIGKILL
    report = evaluate(hung, cache, out)
    assert not report.ok and any("missing end record" in f for f in report.failures)

    exited, cache, out = runner.run(["fx_osexit.py"], work, hooked=True)
    assert exited.returncode == 5
    report = evaluate(exited, cache, out)
    assert not report.ok and any("missing end record" in f for f in report.failures)

    cache = pyenv.fresh_dir(runner.tmp, "cache-term")
    out = pyenv.fresh_dir(runner.tmp, "attest-term")
    proc = subprocess.Popen([helpers.PYTHON, "fx_sleep.py"], cwd=work, stdout=subprocess.PIPE,
                            env=helpers.protocol_env(cache, out, (TARGET,)), start_new_session=True)
    assert proc.stdout.readline().strip() == b"ready"
    proc.send_signal(signal.SIGTERM)
    proc.wait(timeout=30)
    proc.stdout.close()
    assert proc.returncode == -signal.SIGTERM
    report = pyenv.evaluate_attestation(out, proc.pid, proc.returncode,
                                        helpers.plan(cache, (TARGET,), {}, {}, 0, 0))
    assert not report.ok and any("missing end record" in f for f in report.failures)


def _hooked_target_run(runner, work):
    result, cache, out = runner.run(["fx_target.py"], work, hooked=True)
    assert result.returncode == 0
    assert evaluate(result, cache, out, required={TARGET: "main"}).ok
    return result, cache, out


def test_E10a_deleted_end_record_fails_closed(runner, work):
    result, cache, out = _hooked_target_run(runner, work)
    (out / f"{result.pid}.end.json").unlink()
    assert not evaluate(result, cache, out, required={TARGET: "main"}).ok


def test_E10b_truncated_record_fails_closed(runner, work):
    result, cache, out = _hooked_target_run(runner, work)
    path = out / f"{result.pid}.end.json"
    path.write_bytes(path.read_bytes()[:40])
    report = evaluate(result, cache, out, required={TARGET: "main"})
    assert not report.ok and any("malformed" in f for f in report.failures)


def test_E10c_missing_attestation_field_fails_closed(runner, work):
    result, cache, out = _hooked_target_run(runner, work)
    path = out / f"{result.pid}.end.json"
    record = json.loads(path.read_text())
    del record["targets"][0]["disk_match"]
    path.write_text(json.dumps(record))
    report = evaluate(result, cache, out, required={TARGET: "main"})
    assert not report.ok and any("fields missing" in f for f in report.failures)


def test_E10d_unknown_process_record_fails_closed(runner, work):
    result, cache, out = _hooked_target_run(runner, work)
    start = json.loads((out / f"{result.pid}.start.json").read_text())
    end = json.loads((out / f"{result.pid}.end.json").read_text())
    stranger = 999999
    for kind, record in (("start", start), ("end", end)):
        record = dict(record, pid=stranger, ppid=1)
        (out / f"{stranger}.{kind}.json").write_text(json.dumps(record))
    report = evaluate(result, cache, out, required={TARGET: "main"})
    assert not report.ok and any("outside the observed process tree" in f for f in report.failures)


def test_E10e_unwritable_attestation_directory_fails_closed_without_altering_program(runner, work):
    unhooked, _, _ = runner.run(["fx_ok.py"], work, hooked=False)
    cache = pyenv.fresh_dir(runner.tmp, "cache-ro")
    out = pyenv.fresh_dir(runner.tmp, "attest-ro")
    os.chmod(out, 0o500)
    try:
        hooked = pyenv.run_process([helpers.PYTHON, "fx_ok.py"], work,
                                   helpers.protocol_env(cache, out, (TARGET,)), 60)
    finally:
        os.chmod(out, 0o700)
    assert (hooked.returncode, hooked.stdout, hooked.stderr) == (
        unhooked.returncode, unhooked.stdout, unhooked.stderr)
    report = pyenv.evaluate_attestation(out, hooked.pid, 0, helpers.plan(cache, (TARGET,), {}, {}, 0, 0))
    assert not report.ok and any("missing start record" in f for f in report.failures)


def test_E11_loaded_versus_freshly_compiled_code(runner, work, tmp_path):
    # (a) protocol, pristine: loaded == expected and == disk
    result, cache, out = _hooked_target_run(runner, work)
    entry = helpers.end_record(out, result.pid)["targets"][0]
    assert entry["disk_match"] is True
    # (b) stale cache in default mode: the hook reports the mismatch
    source = work / "pkgx" / "target.py"
    mtime_ns = source.stat().st_mtime_ns
    default = helpers.default_env()
    assert pyenv.run_process([helpers.PYTHON, "fx_target.py"], work, default, 60).stdout.strip() == b"23"
    source.write_text("def f(a, b):\n    return b * 10 + a\n")          # same length
    os.utime(source, ns=(mtime_ns, mtime_ns))
    out_b = pyenv.fresh_dir(tmp_path, "attest-e11b")
    stale = pyenv.run_process([helpers.PYTHON, "fx_target.py"], work,
                              helpers.default_env_with_hook(tmp_path, out_b, "pkgx.target:f", "E11b"), 60)
    assert stale.stdout.strip() == b"23"                                  # stale code ran
    assert helpers.end_record(out_b, stale.pid)["targets"][0]["disk_match"] is False
    # (c) same planted stale cache, protocol run: fresh code, planted cache untouched
    planted = next((work / "pkgx" / "__pycache__").glob("target.*.pyc"))
    planted_sha = pyenv.sha256_file(planted)
    fresh, cache_c, out_c = runner.run(["fx_target.py"], work, hooked=True)
    assert fresh.stdout.strip() == b"32"
    assert helpers.end_record(out_c, fresh.pid)["targets"][0]["disk_match"] is True
    assert pyenv.sha256_file(planted) == planted_sha
    # (d) under -O the hook compiles with the same optimisation level: still a match
    optimised, _, out_d = runner.run(["fx_target.py"], work, hooked=True, flags=("-O",))
    assert helpers.end_record(out_d, optimised.pid)["targets"][0]["disk_match"] is True


def test_E12_children_directly_attested_only_with_their_own_records(runner, work):
    result, cache, out = runner.run(["fx_child.py"], work, hooked=True)
    report = evaluate(result, cache, out, on_pass=1)
    assert report.ok, report.failures
    assert len(report.children) == 1 and report.directly_attested_children == report.children
    child = report.children[0]
    assert json.loads((out / f"{child}.start.json").read_text())["ppid"] == result.pid

    isolated, cache, out = runner.run(["fx_child_isolated.py"], work, hooked=True)
    assert isolated.returncode == 0 and b"out-ok" in isolated.stdout     # the child really ran
    report = evaluate(isolated, cache, out, on_pass=1)
    assert not report.ok and report.directly_attested_children == []
    assert any("expected 1 direct Python children, observed 0" in f for f in report.failures)


def test_E13_child_count_deviation_fails_closed(runner, work):
    two, cache, out = runner.run(["fx_two_children.py"], work, hooked=True)
    assert two.returncode == 0
    assert not evaluate(two, cache, out, on_pass=1).ok
    none, cache, out = runner.run(["fx_ok.py"], work, hooked=True)
    assert not evaluate(none, cache, out, on_pass=1).ok
    missing, cache, out = runner.run(["fx_ok.py"], work, hooked=True)
    report = pyenv.evaluate_attestation(out, missing.pid, 0, pyenv.AttestationPlan(
        hook_sha256=pyenv.verify_hook(), cache_dir=str(cache)))
    assert not report.ok and any("no registered child-process expectation" in f for f in report.failures)


def test_E14_hook_integrity(runner, work, tmp_path):
    with pytest.raises(pyenv.EnvironmentRefused):
        pyenv.verify_hook(pyenv.HOOK_DIR, "0" * 64)
    result, cache, out = runner.run(["fx_ok.py"], work, hooked=True)
    bad_plan = helpers.plan(cache)
    bad_plan.hook_sha256 = "0" * 64
    report = pyenv.evaluate_attestation(out, result.pid, 0, bad_plan)
    assert not report.ok and any("hook sha256 mismatch" in f for f in report.failures)
    polluted = helpers.disposable_hook_dir(tmp_path)
    (polluted / "__pycache__").mkdir()
    with pytest.raises(pyenv.EnvironmentRefused):
        pyenv.verify_hook(polluted)


def test_preflight_passes_on_this_interpreter(tmp_path):
    report = pyenv.preflight(helpers.PYTHON, helpers.base_env(), tmp_path, pyenv.verify_hook())
    assert report["hooked"]["sitecustomize"] == str(pyenv.HOOK_FILE)
    assert report["plain"]["sitecustomize"] is None


def test_hook_is_silent_and_inert_without_its_variable(tmp_path):
    cache = pyenv.fresh_dir(tmp_path, "cache")
    env = helpers.protocol_env(cache)
    env["PYTHONPATH"] = str(pyenv.HOOK_DIR)                 # hook importable but not activated
    result = pyenv.run_process([helpers.PYTHON, "-c", "print('quiet')"], tmp_path, env, 60)
    assert result.returncode == 0 and result.stdout == b"quiet\n" and result.stderr == b""
    assert sorted(p.name for p in tmp_path.iterdir()) == ["cache"]
