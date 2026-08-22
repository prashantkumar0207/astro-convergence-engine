"""ADR numbering gate, with the negative controls Q14 recorded as missing.

ADR-0029 corrected a real numbering defect and left the gate with no negative
control, so its PASS proved only that it ran. `docs/OPEN_QUESTIONS.md` Q14
recorded that. These tests supply the controls, and they run on every default
gate rather than only in CI.

Each control constructs a register that VIOLATES one rule and requires the gate
to reject it, and every control first asserts that the same register PASSES
before the violation is introduced, so no control can pass vacuously.
"""

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import check_adr_numbering as gate  # noqa: E402

REGISTER = ROOT / "docs" / "DECISION_LOG.md"

#: A minimal well-formed register. Deliberately includes a gap (0002 to 0005)
#: because gaps are legal, and the template heading, because it must not count.
CLEAN = """\
# Decision Log (ADR register)

## ADR-0001 - first
body

## ADR-0002 - second
body

## ADR-0005 - fifth, after a legal reservation gap
body

### Evidence addendum to ADR-0005 - not an entry
body

## ADR-XXXX - <title>
template, must not be counted
"""


def test_the_real_register_passes():
    assert gate.check(REGISTER.read_text()) == []


def test_the_real_register_is_what_we_think_it_is():
    """Guards against the gate silently checking nothing."""

    found = gate.numbers(REGISTER.read_text())
    assert len(found) >= 30, f"only {len(found)} entries parsed; heading format may have changed"
    assert found[0] == 1


def test_clean_fixture_passes_so_the_controls_below_are_meaningful():
    assert gate.check(CLEAN) == []
    assert gate.numbers(CLEAN) == [1, 2, 5]


def test_addendum_and_template_headings_are_not_counted():
    """ADR-0029 decision 2. A level-three addendum is not an entry."""

    found = gate.numbers(CLEAN)
    assert found.count(5) == 1, "the addendum to ADR-0005 was counted as a second entry"
    assert 0 not in found, "the `ADR-XXXX` template heading was counted as entry zero"
    assert len(found) == 3, f"expected 3 entries, parsed {found}"


# --------------------------------------------------------------------------
# Negative controls. Each must FAIL.
# --------------------------------------------------------------------------


def test_negative_control_duplicate_number_is_rejected():
    corrupted = CLEAN + "\n## ADR-0002 - a second entry claiming an issued number\nbody\n"
    errors = gate.check(corrupted)
    assert errors, "duplicate ADR number was NOT rejected; the gate cannot fail"
    assert any("duplicate" in e for e in errors), errors


def test_negative_control_out_of_order_number_is_rejected():
    corrupted = CLEAN + "\n## ADR-0003 - filed after a higher number\nbody\n"
    errors = gate.check(corrupted)
    assert errors, "out-of-order ADR number was NOT rejected; the gate cannot fail"
    assert any("monotonic" in e for e in errors), errors


def test_negative_control_addendum_promoted_to_an_entry_is_rejected():
    """The exact defect ADR-0029 corrected: an addendum at level two."""

    corrupted = CLEAN.replace(
        "### Evidence addendum to ADR-0005 - not an entry",
        "## ADR-0005 EVIDENCE ADDENDUM - promoted by mistake",
    )
    errors = gate.check(corrupted)
    assert errors, "an addendum promoted to a level-two entry heading was NOT rejected"
    assert any("duplicate" in e for e in errors), errors


def test_negative_control_empty_register_is_rejected():
    """A gate that passes on nothing is not a gate."""

    errors = gate.check("# Decision Log\n\nno entries here\n")
    assert errors, "a register with no entries was NOT rejected"
    assert any("no ADR entry headings" in e for e in errors), errors


# --------------------------------------------------------------------------
# End to end, through the process boundary CI actually uses.
# --------------------------------------------------------------------------


def _run(target: Path) -> int:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_adr_numbering.py"), str(target)],
        capture_output=True,
        text=True,
    ).returncode


def test_cli_exits_zero_on_the_real_register():
    assert _run(REGISTER) == 0


@pytest.mark.parametrize(
    "corruption, description",
    [
        ("\n## ADR-0002 - duplicate\nbody\n", "duplicate"),
        ("\n## ADR-0003 - out of order\nbody\n", "out of order"),
    ],
)
def test_cli_exits_nonzero_on_a_corrupted_copy(tmp_path, corruption, description):
    """Copy-based. The real register is never written to."""

    before = REGISTER.read_bytes()
    probe = tmp_path / "DECISION_LOG.md"
    probe.write_text(CLEAN)
    assert _run(probe) == 0, "the clean copy must pass first, or this control is vacuous"
    probe.write_text(CLEAN + corruption)
    assert _run(probe) == 1, f"CLI did not fail on a {description} register"
    assert REGISTER.read_bytes() == before, "the real register was modified by a control"


def test_cli_exits_two_when_the_register_is_unreadable(tmp_path):
    assert _run(tmp_path / "does_not_exist.md") == 2
