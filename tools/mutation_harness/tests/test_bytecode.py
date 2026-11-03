"""Bytecode-isolation tests D1-D9 (R1 s7.3.5) on harmless temporary fixture modules.

Same-second staleness is FORCED with os.utime (never raced): the stale-cache condition
is "same whole-second source mtime and same source size", which these tests construct
deterministically. No ACE file, and no retained WP-N1 bytecode, is read or executed.
"""

import marshal
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import helpers  # noqa: E402
import pyenv  # noqa: E402

V1 = b"def f():\n    return 1\n"
V2 = b"def f():\n    return 2\n"
IMPORT_AND_CALL = "import fixmod; print(fixmod.f())"


def write_with_mtime(path: Path, data: bytes, mtime_ns: int) -> None:
    path.write_bytes(data)
    os.utime(path, ns=(mtime_ns, mtime_ns))


def call(cwd, env, flags=()):
    result = helpers.run([helpers.PYTHON, *flags, "-c", IMPORT_AND_CALL], cwd, env)
    assert result.returncode == 0, result.stderr
    return result.stdout.decode().strip()


def attested_call(cwd, env_builder, tmp, label, expected_source):
    """Run the import under the hook and return (value, end-record target entry, report)."""

    out = pyenv.fresh_dir(tmp, f"attest-{label}")
    cache = pyenv.fresh_dir(tmp, f"cache-{label}")
    env = env_builder(cache, out)
    result = helpers.run([helpers.PYTHON, "-c", IMPORT_AND_CALL], cwd, env)
    assert result.returncode == 0, result.stderr
    target = ("fixmod", "f")
    report = pyenv.evaluate_attestation(
        out, result.pid, result.returncode,
        helpers.plan(cache, [target], {target: pyenv.expected_digest(expected_source, "f")},
                     {target: "main"}))
    entry = helpers.end_record(out, result.pid)["targets"][0]
    return result.stdout.decode().strip(), entry, report


def stale_setup(tmp: Path, cached_text: bytes, disk_text: bytes) -> Path:
    """Compile `cached_text` into __pycache__ in default mode, then replace the source with
    `disk_text` (same length) carrying the identical mtime: a header-valid stale cache."""

    work = tmp / "work"
    work.mkdir()
    module = work / "fixmod.py"
    module.write_bytes(cached_text)
    mtime_ns = module.stat().st_mtime_ns
    assert call(work, helpers.default_env()) == cached_text.decode().split()[-1]
    assert (work / "__pycache__" / f"fixmod.{sys.implementation.cache_tag}.pyc").exists()
    assert len(cached_text) == len(disk_text)
    write_with_mtime(module, disk_text, mtime_ns)
    return work


def test_D1_legacy_default_mode_reads_stale_bytecode(tmp_path):
    work = stale_setup(tmp_path, V1, V2)
    assert call(work, helpers.default_env()) == "1"           # stale: the disk says 2

    def default_with_hook(cache, out):
        return helpers.default_env_with_hook(tmp_path, out, phase="D1")

    value, entry, report = attested_call(work, default_with_hook, tmp_path, "d1", V2)
    assert value == "1"
    assert entry["disk_match"] is False                         # the hook reports the mismatch
    assert not report.ok


def test_D2_dont_write_bytecode_alone_still_reads_stale(tmp_path):
    work = stale_setup(tmp_path, V1, V2)
    env = helpers.default_env()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    assert call(work, env) == "1"


def test_D3_fresh_prefix_alone_reads_source_but_writes_cache(tmp_path):
    work = stale_setup(tmp_path, V1, V2)
    prefix = pyenv.fresh_dir(tmp_path, "prefix")
    env = helpers.default_env()
    env["PYTHONPYCACHEPREFIX"] = str(prefix)
    assert call(work, env) == "2"
    assert any(name.endswith(".pyc") for name in pyenv.tree_listing(prefix))


def test_D4_reused_prefix_is_stale_and_attestation_detects_it(tmp_path):
    work = stale_setup(tmp_path, V1, V2)
    module = work / "fixmod.py"
    mtime_ns = module.stat().st_mtime_ns
    prefix = pyenv.fresh_dir(tmp_path, "prefix")
    env = helpers.default_env()
    env["PYTHONPYCACHEPREFIX"] = str(prefix)
    assert call(work, env) == "2"                               # prefix now caches V2
    write_with_mtime(module, V1, mtime_ns)                      # same size, same second
    assert call(work, env) == "2"                               # stale within the prefix

    def reused_prefix_with_hook(cache, out):
        reused = dict(env)
        reused.update(PYTHONPATH=str(helpers.disposable_hook_dir(tmp_path)), ACE_ATTEST_OUT=str(out),
                      ACE_ATTEST_TARGETS="fixmod:f", ACE_ATTEST_PHASE="D4")
        return reused

    value, entry, report = attested_call(work, reused_prefix_with_hook, tmp_path, "d4", V1)
    assert value == "2" and entry["disk_match"] is False and not report.ok


def test_D5_protocol_reads_source_and_writes_nothing(tmp_path):
    work = stale_setup(tmp_path, V1, V2)
    value, entry, report = attested_call(
        work, lambda cache, out: helpers.protocol_env(cache, out, [("fixmod", "f")]), tmp_path, "d5", V2)
    assert value == "2"
    assert entry["disk_match"] is True
    assert report.ok, report.failures
    assert pyenv.tree_listing(tmp_path / "cache-d5") == []
    before = sorted(p.name for p in (work / "__pycache__").iterdir())
    assert before == [f"fixmod.{sys.implementation.cache_tag}.pyc"]   # nothing new written


def test_D6_protocol_is_inherited_by_child_processes(tmp_path):
    work = stale_setup(tmp_path, V1, V2)
    (work / "parent.py").write_text(
        "import subprocess, sys\n"
        f"r = subprocess.run([sys.executable, '-c', {IMPORT_AND_CALL!r}])\n"
        "sys.exit(r.returncode)\n")
    out = pyenv.fresh_dir(tmp_path, "attest-d6")
    cache = pyenv.fresh_dir(tmp_path, "cache-d6")
    result = helpers.run([helpers.PYTHON, "parent.py"], work,
                         helpers.protocol_env(cache, out, [("fixmod", "f")]))
    assert result.returncode == 0 and result.stdout.decode().strip() == "2"
    target = ("fixmod", "f")
    report = pyenv.evaluate_attestation(
        out, result.pid, 0, helpers.plan(cache, [target], {target: pyenv.expected_digest(V2, "f")},
                                         {target: "child"}, on_pass=1))
    assert report.ok, report.failures
    assert len(report.directly_attested_children) == 1
    assert pyenv.tree_listing(cache) == []


def test_D7_isolated_mode_ignores_the_protocol_and_is_refused(tmp_path):
    cache = pyenv.fresh_dir(tmp_path, "cache-d7")
    env = helpers.protocol_env(cache)
    report = pyenv.probe_report(helpers.PYTHON, env, tmp_path, extra_flags=("-I",))
    failures = pyenv.check_probe(report, cache, hooked=False)
    assert report["pycache_prefix"] is None and report["flags"]["isolated"] == 1
    assert failures
    try:
        pyenv.check_argv([helpers.PYTHON, "-I", "-c", "pass"], helpers.PYTHON)
    except pyenv.EnvironmentRefused:
        pass
    else:
        raise AssertionError("-I was not refused")
    for refused in (["-E"], ["-S"], ["-O"], ["-OO"], ["-IB"], ["-X", "pycache_prefix=/tmp/x"],
                    ["-Xpycache_prefix=/tmp/x"]):
        try:
            pyenv.check_argv([helpers.PYTHON, *refused, "-c", "pass"], helpers.PYTHON)
        except pyenv.EnvironmentRefused:
            continue
        raise AssertionError(f"{refused} was not refused")
    pyenv.check_argv([helpers.PYTHON, "-B", "-u", "-c", "pass"], helpers.PYTHON)  # allowed


def test_D8_planted_stale_cache_is_bypassed_by_the_protocol(tmp_path):
    """The retained-S2 situation in a disposable fixture: a header-valid stale .pyc holding
    the MUTATED code sits in the source-tree __pycache__ next to the RESTORED source."""

    work = stale_setup(tmp_path, V2, V1)                        # cache = mutated (2), disk = restored (1)
    planted = work / "__pycache__" / f"fixmod.{sys.implementation.cache_tag}.pyc"
    planted_sha = pyenv.sha256_file(planted)

    def default_with_hook(cache, out):
        return helpers.default_env_with_hook(tmp_path, out, phase="D8-control")

    value, entry, _report = attested_call(work, default_with_hook, tmp_path, "d8c", V1)
    assert value == "2" and entry["disk_match"] is False        # control: stale code loaded

    value, entry, report = attested_call(
        work, lambda cache, out: helpers.protocol_env(cache, out, [("fixmod", "f")]), tmp_path, "d8p", V1)
    assert value == "1" and entry["disk_match"] is True and report.ok, report.failures
    assert pyenv.sha256_file(planted) == planted_sha            # planted file untouched


def test_D9_structural_comparison_controls():
    source = b"def g(a, b):\n    return h(a, b) + 1\n"
    first = pyenv.find_code(compile(source, "x.py", "exec", dont_inherit=True), "g")
    second = pyenv.find_code(compile(source, "y.py", "exec", dont_inherit=True), "g")
    assert pyenv.code_digest(first) == pyenv.code_digest(second)            # (a) same text
    const = pyenv.find_code(compile(source.replace(b"+ 1", b"+ 2"), "x.py", "exec"), "g")
    assert pyenv.code_digest(const) != pyenv.code_digest(first)             # (b) one constant
    column = pyenv.find_code(compile(source.replace(b"h(a, b)", b"h(a,  b)"), "x.py", "exec"), "g")
    assert column.co_code == first.co_code                                   # same bytecode ...
    assert pyenv.code_digest(column) != pyenv.code_digest(first)            # (c) ... positions differ
    swapped = pyenv.find_code(compile(source.replace(b"h(a, b)", b"h(b, a)"), "x.py", "exec"), "g")
    assert pyenv.code_digest(swapped) != pyenv.code_digest(first)           # argument order (S2 shape)
    # (d) marshal bytes are recorded for information only, never used as the decision.
    marshal_equal = marshal.dumps(first) == marshal.dumps(second)
    assert marshal_equal in (True, False)


def test_hook_and_harness_structural_identity_agree(tmp_path):
    """The hook duplicates canon() so that it imports nothing from the harness; both
    copies must produce identical digests."""

    import importlib.util
    spec = importlib.util.spec_from_file_location("attest_hook_under_test", pyenv.HOOK_FILE)
    hook = importlib.util.module_from_spec(spec)
    assert "ACE_ATTEST_OUT" not in os.environ          # the hook is inert when loaded here
    spec.loader.exec_module(hook)
    import hashlib
    sources = [V1, V2, b"class C:\n    def m(self, x):\n        return [y for y in x if y]\n",
               b"def outer():\n    def inner(q):\n        return q * 3.5\n    return inner\n"]
    for source in sources:
        module_code = compile(source, "s.py", "exec", dont_inherit=True)
        for code in [module_code] + [c for c in module_code.co_consts if hasattr(c, "co_code")]:
            ours = pyenv.code_digest(code)
            theirs = hashlib.sha256(repr(hook._canon(code)).encode("utf-8")).hexdigest()
            assert ours == theirs
