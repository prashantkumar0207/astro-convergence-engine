"""Shared helpers for the harness test-suite (not a test module itself)."""

import os
import sys
from pathlib import Path

HARNESS_DIR = Path(__file__).resolve().parents[1]
if str(HARNESS_DIR) not in sys.path:
    sys.path.insert(0, str(HARNESS_DIR))

import pyenv  # noqa: E402

PYTHON = sys.executable


def base_env() -> dict:
    """The test process environment without protocol-controlled variables. The test-suite
    itself runs with PYTHONDONTWRITEBYTECODE=1; that must not leak into 'default mode'."""

    return {key: value for key, value in os.environ.items()
            if key not in pyenv.FORBIDDEN_ENV and not key.startswith(pyenv.FORBIDDEN_ENV_PREFIXES)}


def default_env() -> dict:
    """Ordinary CPython behaviour: bytecode is read from and written to __pycache__."""

    return base_env()


def run(argv, cwd, env, timeout=60):
    return pyenv.run_process(argv, cwd, env, timeout)


def protocol_env(cache_dir, attest_out=None, targets=()):
    return pyenv.build_env(base_env(), cache_dir, attest_out, targets, "test")


def plan(cache_dir, targets=(), expected=None, required=None, on_pass=0, min_on_fail=0):
    return pyenv.AttestationPlan(
        targets=tuple(targets),
        expected_digests=dict(expected or {}),
        required_load=dict(required or {}),
        children=pyenv.ChildExpectation(on_pass, min_on_fail),
        hook_sha256=pyenv.verify_hook(),
        cache_dir=str(cache_dir),
    )


def disposable_hook_dir(tmp) -> Path:
    """A byte-identical copy of the hook in a temporary directory. Default-mode (non-
    protocol) control runs MUST use this: without PYTHONDONTWRITEBYTECODE, CPython writes
    a .pyc of the hook into the hook's own directory, which verify_hook() then (correctly)
    refuses. The real hook directory is only ever used under the protocol."""

    import shutil
    target = Path(tmp) / "disposable-hook"
    target.mkdir(exist_ok=True)
    shutil.copyfile(pyenv.HOOK_FILE, target / "sitecustomize.py")
    return target


def default_env_with_hook(tmp, out, targets="fixmod:f", phase="control") -> dict:
    env = default_env()
    env.update(PYTHONPATH=str(disposable_hook_dir(tmp)), ACE_ATTEST_OUT=str(out),
               ACE_ATTEST_TARGETS=targets, ACE_ATTEST_PHASE=phase)
    return env


def end_record(out_dir, pid):
    import json
    return json.loads((Path(out_dir) / f"{pid}.end.json").read_text(encoding="utf-8"))
