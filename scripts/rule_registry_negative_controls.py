"""Negative controls for scripts/check_rule_registry.py (ADR-0121): each plants one violation in a temporary copy of
the registry and requires the real gate to exit 1 with that violation's message. Committed files are never modified.

Controls: duplicate issuance, a reused number, an identity rebinding, a rewritten version, a withdrawn version, a
changed pin, a hand-edited snapshot byte, and an allocation outside the authoring process.

Exit 0 = every control was caught; 1 = a planted violation passed.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.evidence import rule_registry as registry  # noqa: E402

GATE = [sys.executable, str(ROOT / "scripts" / "check_rule_registry.py")]
HISTORY, SNAPSHOT = registry.HISTORY_NAME, "snapshot.json"


def _write(path: Path, data) -> None:
    path.write_bytes((json.dumps(data, sort_keys=True, indent=1) + "\n").encode("ascii"))


def _run(args) -> tuple[int, str]:
    result = subprocess.run(GATE + args, capture_output=True, text=True)
    return result.returncode, result.stdout


def main() -> int:
    caught, missed = [], []
    with tempfile.TemporaryDirectory() as folder:
        work = Path(folder)

        def copy(name):
            target = work / name
            shutil.copytree(registry.DATA_DIR, target)
            return target

        history = json.loads((registry.DATA_DIR / HISTORY).read_bytes())
        snapshot = json.loads((registry.DATA_DIR / SNAPSHOT).read_bytes())
        _write(work / "same_history.json", history)
        _write(work / "same_snapshot.json", snapshot)
        same = ["--previous-history", str(work / "same_history.json"), "--previous-snapshot",
                str(work / "same_snapshot.json")]
        controls = []

        duplicate = copy("duplicate")
        planted = json.loads((duplicate / HISTORY).read_bytes())
        planted["allocations"][1]["number"] = 1
        _write(duplicate / HISTORY, planted)
        controls.append(("duplicate issuance", ["--dir", str(duplicate)] + same, "issued once, in order"))

        rebound = copy("rebound")
        planted = json.loads((rebound / HISTORY).read_bytes())
        planted["allocations"][2]["key"] = "synthetic.planted.other-rule"
        _write(rebound / HISTORY, planted)
        controls.append(("identity rebinding", ["--dir", str(rebound)] + same, "rebinds it"))

        longer = dict(history, allocations=history["allocations"] +
                      [{"number": len(history["allocations"]) + 1, "key": "synthetic.planted.dropped", "school": "kp"}])
        _write(work / "longer_history.json", longer)
        controls.append(("a number dropped and free for reuse",
                         ["--previous-history", str(work / "longer_history.json"), "--previous-snapshot",
                          str(work / "same_snapshot.json")], "dropped, reused or rebound"))

        rewritten = json.loads(json.dumps(snapshot))
        rewritten["rules"][0]["content_hash"] = "0" * 64
        _write(work / "rewritten_snapshot.json", rewritten)
        controls.append(("a published version rewritten",
                         ["--previous-history", str(work / "same_history.json"), "--previous-snapshot",
                          str(work / "rewritten_snapshot.json")], "was rewritten"))

        withdrawn = json.loads(json.dumps(snapshot))
        withdrawn["rules"].append(dict(snapshot["rules"][0], version=99))
        _write(work / "withdrawn_snapshot.json", withdrawn)
        controls.append(("a published version withdrawn",
                         ["--previous-history", str(work / "same_history.json"), "--previous-snapshot",
                          str(work / "withdrawn_snapshot.json")], "now withdrawn"))

        controls.append(("a changed pin", ["--pin", "0" * 64] + same, "differs from the pinned hash"))

        edited = copy("edited")
        raw = (edited / SNAPSHOT).read_bytes()
        (edited / SNAPSHOT).write_bytes(raw.replace(b"Synthetic fixture statement", b"Planted fixture statement", 1))
        controls.append(("a hand-edited snapshot byte", ["--dir", str(edited)] + same,
                         "do not match the pinned hash"))

        outside = copy("outside")
        planted = json.loads((outside / HISTORY).read_bytes())
        planted["allocations"].append({"number": len(planted["allocations"]) + 1, "key": "synthetic.planted.outside",
                                       "school": "kp"})
        _write(outside / HISTORY, planted)
        controls.append(("an allocation outside the authoring process", ["--dir", str(outside)] + same,
                         "allocated to keys the source never authored"))

        for label, args, message in controls:
            code, output = _run(args)
            (caught if code == 1 and message in output else missed).append(label)
    if missed:
        print(f"the rule-registry gate did NOT flag planted violations: {missed}")
        return 1
    print(f"negative controls passed: {len(caught)} planted violations each refused for its reason: {', '.join(caught)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
