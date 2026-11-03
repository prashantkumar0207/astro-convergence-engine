"""A disposable fixture repository that imitates the SHAPE of an ACE composition check
without any ACE code: a target module, a validator with its own hard-coded expected
values, a certifier whose designated gate runs the validator as a child process (like
ACE Gate I/J), a pre-check, and a tracked certification artifact the certifier rewrites.

Fault switches used only by the state-machine tests:
  FIXTURE_FORCE_FAIL=1          the certifier's main() fails (a dirty baseline)
  FIXTURE_FAULT_FILE=<path>     if the file exists, its content selects a fault:
      gate          the designated gate fails
      e2e           the end-to-end run fails after its gates
      hang          the designated gate hangs
      hang-corrupt  the designated gate corrupts the target file, then hangs
"""

import os
import subprocess
from pathlib import Path

TARGET_SOURCE = '''"""Fixture composition module (harmless; never ACE code)."""

# fixture marker: alpha


def sign(longitude):
    return int(longitude // 30) + 1


def house(body_lon, asc_lon):
    return (sign(body_lon) - sign(asc_lon)) % 12 + 1


def unused_helper():
    return 1
'''

VALIDATOR_SOURCE = '''"""Fixture validator: hard-coded expected values, independent of pkg.target."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pkg.target as t

CASES = [(95.0, 10.0, 4), (200.0, 10.0, 7), (10.0, 10.0, 1), (359.0, 0.5, 12)]
failures = [f"house_number={t.house(body, asc)} expected={expected}"
            for body, asc, expected in CASES if t.house(body, asc) != expected]
print(f"Composition cases checked: {len(CASES)}")
if failures:
    print(f"FAILURES: {len(failures)}; first: {failures[:3]}")
    print("RESULT: FIXTURE COMPOSITION VERIFICATION FAILED")
    sys.exit(1)
print("RESULT: FIXTURE COMPOSITION VERIFICATION PASSED")
'''

CERTIFIER_SOURCE = '''"""Fixture certifier. Exit 0 = PASS, 3 = FAIL."""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def fail(message):
    print("FIXTURE CERTIFICATION FAIL:", message)
    sys.exit(3)


def _fault():
    path = os.environ.get("FIXTURE_FAULT_FILE", "")
    if path and os.path.exists(path):
        return Path(path).read_text().strip()
    return ""


def gate_a_import():
    sys.path.insert(0, str(ROOT))
    import pkg.target as t
    if t.sign(0.0) != 1 or t.sign(359.9) != 12:
        fail("sign table broken")
    return {"result": "PASS"}


def gate_j_composition():
    fault = _fault()
    if fault == "gate":
        fail("composition verification failed: injected fault")
    if fault == "hang-corrupt":
        (ROOT / "pkg" / "target.py").write_text("# corrupted by the fixture fault\\n")
    if fault in ("hang", "hang-corrupt"):
        time.sleep(600)
    result = subprocess.run([sys.executable, str(ROOT / "fake_validator.py")], capture_output=True, text=True)
    if result.returncode != 0 or "RESULT: FIXTURE COMPOSITION VERIFICATION PASSED" not in result.stdout:
        fail(f"composition verification failed: {result.stdout[-600:]}")
    return {"result": "PASS"}


def main():
    if os.environ.get("FIXTURE_FORCE_FAIL") == "1":
        fail("forced baseline failure")
    gates = {"A": gate_a_import(), "J": gate_j_composition()}
    if _fault() == "e2e":
        fail("end-to-end: injected fault")
    artifact = ROOT / "certification" / "FIXTURE_certification.json"
    artifact.write_text(json.dumps({"result": "PASS", "gates": gates}, sort_keys=True) + "\\n")
    print("RESULT: PASS")


if __name__ == "__main__":
    main()
'''

PRECHECK_SOURCE = '''"""Fixture non-equivalence pre-check (runs on pristine code)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pkg.target as t

mode = sys.argv[1]
if mode == "swap":
    cases = [(95.0, 10.0), (200.0, 10.0), (10.0, 10.0), (359.0, 0.5)]
    differ = sum(1 for b, a in cases if (t.sign(b) - t.sign(a)) % 12 not in (0, 6))
    print(json.dumps({"admitted": differ >= 1, "pairs_that_would_change": differ}))
elif mode == "unused":
    print(json.dumps({"admitted": t.unused_helper() + 1 != t.unused_helper()}))
elif mode == "equivalent":
    print(json.dumps({"admitted": False, "reason": "comment-only edit changes no inspected value"}))
else:
    print("this is not JSON")
'''

TEMPLATE = {
    ".gitignore": "__pycache__/\n",
    "pkg/__init__.py": "",
    "pkg/target.py": TARGET_SOURCE,
    "fake_validator.py": VALIDATOR_SOURCE,
    "fake_certifier.py": CERTIFIER_SOURCE,
    "precheck.py": PRECHECK_SOURCE,
    "certification/FIXTURE_certification.json": "{}\n",
}

ARTIFACT = "certification/FIXTURE_certification.json"
FAIL_PREFIX = "FIXTURE CERTIFICATION FAIL: composition verification failed"

#: kind -> (old line, new line, qualnames attested, pre-check mode). Same-length edits.
MUTATIONS = {
    "swap": ("    return (sign(body_lon) - sign(asc_lon)) % 12 + 1",
             "    return (sign(asc_lon) - sign(body_lon)) % 12 + 1", ["house"], "swap"),
    "unused": ("    return 1", "    return 2", ["unused_helper"], "unused"),
    "equivalent": ("# fixture marker: alpha", "# fixture marker: omega", ["house"], "equivalent"),
    "broken-precheck": ("    return 1", "    return 2", ["unused_helper"], "broken"),
}


def git(repo, *args):
    env = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
    return subprocess.run(["git", "-C", str(repo), "-c", "user.name=fixture",
                           "-c", "user.email=fixture@example.invalid", *args],
                          check=True, capture_output=True, env=env)


def make_fixture_repo(root) -> Path:
    root = Path(root)
    root.mkdir(parents=True)
    for name, text in TEMPLATE.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    git(root, "init", "-q")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "fixture baseline")
    return root


def build_spec(harness, repo, run_id, python, kind="swap", timeout=60.0):
    """An ExperimentSpec for the fixture. `harness` is the harness module. `timeout`
    applies to the designated gate and the end-to-end command."""

    old, new, qualnames, mode = MUTATIONS[kind]
    lines = TARGET_SOURCE.split("\n")
    line_no = lines.index(old) + 1
    gate_code = ("import sys; sys.path.insert(0, '.'); import fake_certifier as m; "
                 "r = m.{gate}(); print('GATE_RETURNED', repr(r)[:400])")
    designated = harness.Command("designated_gate_j", [python, "-c", gate_code.format(gate="gate_j_composition")],
                                 on_pass_children=1, min_on_fail_children=1, target_load="child",
                                 timeout=timeout)
    gate_a = harness.Command("gate_a_alone", [python, "-c", gate_code.format(gate="gate_a_import")],
                             on_pass_children=0, min_on_fail_children=0, target_load="main")
    return harness.ExperimentSpec(
        run_id=run_id,
        worktree=str(repo),
        target="pkg/target.py",
        module="pkg.target",
        qualnames=qualnames,
        edits=[harness.Edit(line_no, old, new)],
        designated=designated,
        end_to_end=harness.Command("end_to_end", [python, "fake_certifier.py"], on_pass_children=1,
                                   min_on_fail_children=0, target_load="any", timeout=timeout),
        baseline_gates=[designated, gate_a],
        excluded=[gate_a],
        fail_prefix=FAIL_PREFIX,
        allow_list=[ARTIFACT],
        validator=harness.Command("validator", [python, "fake_validator.py"], on_pass_children=0,
                                  min_on_fail_children=0, target_load="main"),
        validator_expect=["RESULT: FIXTURE COMPOSITION VERIFICATION FAILED", "house_number="],
        precheck=harness.Command("precheck", [python, "precheck.py", mode], on_pass_children=0,
                                 min_on_fail_children=0, target_load="none"),
    )
