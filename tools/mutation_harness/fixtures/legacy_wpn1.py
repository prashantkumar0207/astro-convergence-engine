"""Legacy WP-N1 execution method, for the C7a characterization test only.

`sha`, `sh`, `git` and `apply_edits` below are VERBATIM transcriptions of the archived
WP-N1 harness `wpn1_harness.py` (sha256 62d0a1156b336c49690a7c8a8013ef17429bf5c0777660dbeaec2098d1e8efd1,
lines L176-L177, L180-L188 and L204-L214). Their AST equality with the archived file was
checked at implementation time (IMPLEMENTATION_EVIDENCE.md). The archived file itself is
historical WP-N1 evidence and is deliberately not committed here.

`legacy_sequence` is NOT verbatim: it characterises the archived L274-L305 mutate/
observe/classify/reverse-edit/re-verify order and the L336 halt rule against the fixture
repository. Module globals are set by the caller: ENV (archived: os.environ plus
LD_LIBRARY_PATH, i.e. default bytecode behaviour) and BASE.
"""

import hashlib
import os
import subprocess
import time
from pathlib import Path

ENV = dict(os.environ)
BASE = None


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def sh(cmd, cwd, timeout=1800):
    t0 = time.time()
    p = subprocess.run(cmd, cwd=cwd, env=ENV, capture_output=True, text=True, timeout=timeout)
    return {"cmd": cmd if isinstance(cmd, str) else " ".join(cmd), "rc": p.returncode,
            "seconds": round(time.time() - t0, 2), "stdout": p.stdout, "stderr": p.stderr}


def git(*args, cwd=BASE):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()


def apply_edits(wt, edits, forward=True):
    for rel, line_no, old, new in edits:
        src, dst = (old, new) if forward else (new, old)
        path = wt / rel
        text = path.read_text(encoding="utf-8")
        lines = text.split("\n")
        hits = [i for i, l in enumerate(lines) if l == src]
        if len(hits) != 1 or hits[0] != line_no - 1:
            raise SystemExit(f"ABORT: {rel}: expected exactly one whole-line match at L{line_no}, found {hits}")
        lines[hits[0]] = dst
        path.write_bytes("\n".join(lines).encode("utf-8"))


def legacy_sequence(wt, py, edits, gate_code, certifier, validator, fail_prefix, validator_expect,
                    kind="secondary", after_mutated=None, after_restore=None):
    """Characterisation of archived L274-L305 and L336 (see module docstring)."""

    files = sorted({e[0] for e in edits})
    res = {"sha256_before": {f: sha(wt / f) for f in files}}
    apply_edits(wt, edits, forward=True)
    if after_mutated is not None:
        after_mutated()
    res["mutated_gate_alone"] = sh([py, "-c", gate_code], wt)
    res["mutated_validator"] = sh([py, validator], wt)
    res["mutated_end_to_end"] = sh([py, certifier], wt)
    g = res["mutated_gate_alone"]
    v = res["mutated_validator"]["stdout"]
    designated_fired = g["rc"] == 3 and any(
        line.startswith(fail_prefix) for line in g["stdout"].splitlines())
    validator_ok = all(s in v for s in validator_expect)
    others_failed = res["mutated_end_to_end"]["rc"] != 0
    if designated_fired and validator_ok:
        res["outcome"] = "DETECTED"
    elif g["rc"] == 0 and others_failed:
        res["outcome"] = "DETECTED-OTHER"
    elif g["rc"] == 0:
        res["outcome"] = "UNDETECTED"
    else:
        res["outcome"] = "VOID"
    apply_edits(wt, edits, forward=False)
    if after_restore is not None:
        after_restore()
    res["sha256_restored"] = {f: sha(wt / f) for f in files}
    res["restored_hash_matches"] = res["sha256_restored"] == res["sha256_before"]
    res["restored_gate_alone"] = sh([py, "-c", gate_code], wt)
    res["restored_end_to_end"] = sh([py, certifier], wt)
    res["restoration_ok"] = (res["restored_hash_matches"] and res["restored_gate_alone"]["rc"] == 0
                             and res["restored_end_to_end"]["rc"] == 0)
    res["final_target_matches_baseline"] = res["restored_hash_matches"]
    res["batch_halts"] = kind == "primary" and not res["final_target_matches_baseline"]  # archived L336
    return res
