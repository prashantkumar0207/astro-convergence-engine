from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GATE = ROOT / "scripts" / "check_identifier_families.py"


def gate():
    return subprocess.run(
        [sys.executable, str(GATE)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def test_registered_family_passes():
    result = gate()
    assert result.returncode == 0, result.stdout + result.stderr


def test_unknown_family_token_is_rejected():
    probe = ROOT / "docs" / "decisions" / "_dp_gate_probe.md"

    try:
        probe.write_text(
            "Planted unknown decision paper: DP-999.\n",
            encoding="utf-8",
        )

        # The production gate intentionally scans tracked files using
        # `git ls-files`. Make the temporary probe visible to that tracked-file
        # enumeration without staging its contents.
        subprocess.run(
            [
                "git",
                "add",
                "--intent-to-add",
                str(probe.relative_to(ROOT)),
            ],
            cwd=ROOT,
            check=True,
        )

        result = gate()

        assert result.returncode == 1, (
            "Expected identifier-family gate to reject DP-999.\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
        assert "DP-999" in result.stdout

    finally:
        # Remove the intent-to-add index entry and temporary probe.
        subprocess.run(
            [
                "git",
                "reset",
                "--",
                str(probe.relative_to(ROOT)),
            ],
            cwd=ROOT,
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        if probe.exists():
            probe.unlink()


def test_duplicate_index_allocation_is_rejected(tmp_path):
    index = ROOT / "docs" / "decisions" / "README.md"
    text = index.read_text(encoding="utf-8")

    assert "| DP-009 |" in text

    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "dp_gate",
        GATE,
    )
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    probe = text.replace(
        "| DP-009 |",
        "| DP-009 | duplicate probe | x | probe |\n| DP-009 |",
        1,
    )

    assert module.registered_ids(probe).count("DP-009") == 2
