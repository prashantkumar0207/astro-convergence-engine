"""Negative controls for scripts/check_rule_registry.py (ADR-0121): each plants one violation in a temporary copy of
the registry and requires the real gate to exit 1 with that violation's message. Committed files are never modified.

Controls: duplicate issuance, a reused number, an identity rebinding, a rewritten version, a withdrawn version, a
changed pin, a hand-edited snapshot byte, an allocation outside the authoring process,
a consistently re-pinned but hand-edited sourced snapshot (G2), and sourced versions rewritten or
withdrawn (G3). The G2/G3 controls also demonstrate the intended weakened-check bypass.

Exit 0 = every control was caught; 1 = a planted violation passed.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.evidence import rule_registry as registry  # noqa: E402
from scripts import check_rule_registry as gate  # noqa: E402

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

        # Stage 2 G2 control: a malicious edition-content rewrite is made internally consistent.
        # Its published content_hash and manifest pin change to match, and the normal schema loader
        # accepts those bytes under that new pin; ONLY independent governed source/output agreement
        # may reject the hand-edited sourced publication.
        sourced_edited = copy("sourced-consistently-repinned")
        sourced_path = sourced_edited / gate.author.SOURCED_SNAPSHOT_NAME
        sourced_snapshot = json.loads(sourced_path.read_bytes())
        favourable = [item for item in sourced_snapshot["rules"]
                      if item["key"].endswith("first-favourable") and item["version"] == 1]
        if len(favourable) != 2:
            print("FAIL: G2 control needs both recorded verse-109 positive editions")
            return 1
        sharma = next(item for item in favourable if item["variant"] == "sharma-1999")
        jha = next(item for item in favourable if item["variant"] == "jha-1982")
        if sharma["statement"] == jha["statement"]:
            print("FAIL: G2 control's verse-109 edition difference was already erased")
            return 1
        jha["statement"] = sharma["statement"]
        jha["content_hash"] = hashlib.sha256(registry.canonical({
            key: value for key, value in jha.items() if key != "content_hash"})).hexdigest()
        _write(sourced_path, sourced_snapshot)
        repin = hashlib.sha256(sourced_path.read_bytes()).hexdigest()
        manifest_path = sourced_edited / gate.author.SOURCED_MANIFEST_NAME
        sourced_manifest = json.loads(manifest_path.read_bytes())
        sourced_manifest["sha256"] = repin
        _write(manifest_path, sourced_manifest)
        try:
            registry.load_registry(sourced_edited, repin, gate.author.SOURCED_MANIFEST_NAME)
        except registry.RegistryError as exc:
            print(f"FAIL: planted sourced snapshot must be schema-valid under its recomputed pin: {exc}")
            return 1
        g2_errors = gate.check_authored(sourced_edited)
        if not any("G2 sourced_snapshot.json" in error for error in g2_errors):
            missed.append("G2 consistently re-pinned sourced snapshot")
        else:
            caught.append("G2 consistently re-pinned sourced snapshot")
            original = gate.author.build_all
            try:
                # Weaken only sourced-output comparison, keeping the three historic authoring
                # checks as the real implementation would. The poisoned bytes must now pass.
                def weak_build(directory):
                    built = original(directory)
                    return (*built[:3], *((directory / name).read_bytes() for name in (
                        gate.author.SOURCED_SNAPSHOT_NAME, gate.author.SOURCED_MANIFEST_NAME)))

                gate.author.build_all = weak_build
                if gate.check_authored(sourced_edited) != []:
                    missed.append("weakening the sourced G2 comparison did not admit the forgery")
                else:
                    caught.append("weakened sourced G2 comparison admits forgery")
            finally:
                gate.author.build_all = original

        # Stage 2 G3 future-merge controls: compare the real current sourced publication
        # against a previous publication, as the --base path does after Stage 2 is merged.
        # Current G1/G2 remain real and passing; a malformed historical record must be
        # rejected specifically by G3, not incidentally by an unrelated pin check.
        issued_source = json.loads((registry.DATA_DIR / gate.author.SOURCED_SNAPSHOT_NAME).read_bytes())
        _write(work / "same_sourced.json", issued_source)
        sourced_previous = ["--previous-sourced", str(work / "same_sourced.json")] + same
        code, output = _run(sourced_previous)
        if code != 0:
            missed.append("G3 baseline with identical sourced history does not pass")
        else:
            caught.append("G3 identical sourced publication baseline passes")
        rewritten = json.loads(json.dumps(issued_source))
        rewritten["rules"][0]["content_hash"] = "0" * 64
        _write(work / "previous_sourced_rewritten.json", rewritten)
        withdrawn = json.loads(json.dumps(issued_source))
        withdrawn["rules"].append(dict(issued_source["rules"][0], version=99))
        _write(work / "previous_sourced_withdrawn.json", withdrawn)
        for label, previous_name, reason in (
                ("a sourced version rewritten", "previous_sourced_rewritten.json", "was rewritten"),
                ("a sourced version withdrawn", "previous_sourced_withdrawn.json", "was withdrawn")):
            code, output = _run(["--previous-sourced", str(work / previous_name)] + same)
            if code != 1 or "G3 sourced" not in output or reason not in output:
                missed.append(label)
            else:
                caught.append(label)
                # Weakening the historical sourced-comparison path alone, by not passing
                # the previous sourced snapshot, admits the same current publication.
                weak_code, weak_output = _run(same)
                if weak_code != 0:
                    missed.append("weakened sourced G3 comparison did not admit "+label)
                else:
                    caught.append("weakened sourced G3 comparison admits "+label)

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
