"""Direct value-identity of the three Vimshottari tables (Q11).

ADR-0023 D3 PERMITS the Vimshottari lord and year tables to exist in three
places, `legacy/kp.py`, `engine/kp/tables.py` and `engine/dasha/tables.py`,
because each serves a different school-scoped consumer and a cross-import would
let a change made for one school silently alter another. School isolation is a
charter non-negotiable; single-source-of-truth is a standard; where they
conflict for executable normative rule data, isolation wins.

**That permission is conditional. The duplication must be TESTED rather than
removed.** `engine/tests/test_vimshottari_consistency.py` covers one leg,
`engine/dasha/tables.py` against `engine/kp/tables.py`. The legacy leg was
covered only behaviourally, by the KP equivalence sweep, so a divergence
introduced in one table could in principle survive until some behavioural case
happened to exercise it. `docs/OPEN_QUESTIONS.md` Q11 recorded that gap.

This module closes it, and closes it in the form Q11's criterion demands: the
assertion is accompanied by a demonstrated failure mode, because an assertion
with no demonstrated failure mode is not coverage.

NO CROSS-IMPORT IS CREATED. The tables are read here, in a test, which is
exactly where the comparison belongs. Nothing in `engine/` or `legacy/` gains a
dependency on anything else, and that is asserted below rather than assumed.
"""

import inspect
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from legacy import kp as legacy_kp  # noqa: E402
from engine.dasha import tables as dasha_tables  # noqa: E402
from engine.kp import tables as kp_tables  # noqa: E402

#: The three holders, and the attribute names each uses.
LORD_TABLES = (
    ("legacy/kp.py", legacy_kp, "LORDS"),
    ("engine/kp/tables.py", kp_tables, "KP_LORDS"),
    ("engine/dasha/tables.py", dasha_tables, "DASHA_LORDS"),
)

YEAR_TABLES = (
    ("legacy/kp.py", legacy_kp, "YEARS"),
    ("engine/kp/tables.py", kp_tables, "KP_YEARS"),
    ("engine/dasha/tables.py", dasha_tables, "DASHA_YEARS"),
)

#: The classical Vimshottari sequence, transcribed here independently of all
#: three modules. This is the anti-circularity element: comparing the three
#: copies with each other proves they agree, not that they are RIGHT. Three
#: identical wrong tables would pass a mutual comparison.
CLASSICAL_LORDS = ("Ke", "Ve", "Su", "Mo", "Ma", "Ra", "Ju", "Sa", "Me")
CLASSICAL_YEARS = (7, 20, 6, 10, 7, 18, 16, 19, 17)
CLASSICAL_TOTAL = 120


def _values(holder, attribute):
    """Normalise to a tuple, since legacy uses lists and engine uses tuples."""

    return tuple(getattr(holder, attribute))


# --------------------------------------------------------------------------
# The direct comparison Q11 asked for, all three pairs.
# --------------------------------------------------------------------------


@pytest.mark.parametrize("name, holder, attribute", LORD_TABLES)
def test_every_lord_table_equals_the_classical_sequence(name, holder, attribute):
    assert _values(holder, attribute) == CLASSICAL_LORDS, (
        f"{name}.{attribute} diverges from the independently transcribed "
        "classical Vimshottari lord sequence"
    )


@pytest.mark.parametrize("name, holder, attribute", YEAR_TABLES)
def test_every_year_table_equals_the_classical_sequence(name, holder, attribute):
    assert _values(holder, attribute) == CLASSICAL_YEARS, (
        f"{name}.{attribute} diverges from the independently transcribed "
        "classical Vimshottari year sequence"
    )


def test_all_three_lord_tables_are_mutually_identical():
    """The leg Q11 named: legacy against engine, by direct value comparison."""

    legacy = _values(legacy_kp, "LORDS")
    engine_kp = _values(kp_tables, "KP_LORDS")
    engine_dasha = _values(dasha_tables, "DASHA_LORDS")
    assert legacy == engine_kp, "legacy/kp.py LORDS != engine/kp/tables.py KP_LORDS"
    assert legacy == engine_dasha, "legacy/kp.py LORDS != engine/dasha/tables.py DASHA_LORDS"


def test_all_three_year_tables_are_mutually_identical():
    legacy = _values(legacy_kp, "YEARS")
    engine_kp = _values(kp_tables, "KP_YEARS")
    engine_dasha = _values(dasha_tables, "DASHA_YEARS")
    assert legacy == engine_kp, "legacy/kp.py YEARS != engine/kp/tables.py KP_YEARS"
    assert legacy == engine_dasha, "legacy/kp.py YEARS != engine/dasha/tables.py DASHA_YEARS"


def test_lord_and_year_tables_are_aligned_and_total_correctly():
    for name, holder, attribute in LORD_TABLES:
        lords = _values(holder, attribute)
        assert len(lords) == 9, f"{name}.{attribute} has {len(lords)} lords, expected 9"
        assert len(set(lords)) == 9, f"{name}.{attribute} repeats a lord"
    for name, holder, attribute in YEAR_TABLES:
        years = _values(holder, attribute)
        assert len(years) == 9, f"{name}.{attribute} has {len(years)} entries, expected 9"
        assert sum(years) == CLASSICAL_TOTAL, (
            f"{name}.{attribute} sums to {sum(years)}, not the 120-year cycle"
        )


def test_the_nakshatra_span_is_exact_in_every_holder():
    """40/3 degrees exactly, never a float, in all three."""

    from fractions import Fraction

    expected = Fraction(40, 3)
    assert legacy_kp.NAK_SPAN == expected
    assert kp_tables.NAK_SPAN == expected
    assert dasha_tables.NAK_SPAN == expected
    for holder in (legacy_kp, kp_tables, dasha_tables):
        assert isinstance(holder.NAK_SPAN, Fraction)


# --------------------------------------------------------------------------
# No cross-import: the condition under which the duplication is permitted.
# --------------------------------------------------------------------------


def test_no_holder_imports_another():
    """ADR-0023 D3: the copies are compared, never wired together."""

    kp_source = inspect.getsource(kp_tables)
    dasha_source = inspect.getsource(dasha_tables)
    legacy_source = inspect.getsource(legacy_kp)

    assert "import legacy" not in kp_source and "from legacy" not in kp_source
    assert "import legacy" not in dasha_source and "from legacy" not in dasha_source
    assert "engine.kp" not in dasha_source
    assert "engine.dasha" not in kp_source
    assert "engine." not in legacy_source, (
        "legacy/kp.py must not depend on engine/; it is the independent oracle"
    )


# --------------------------------------------------------------------------
# Negative controls. Perturbation MUST be detected.
# --------------------------------------------------------------------------


class _Perturbed:
    """A stand-in holder carrying a single altered cell."""

    def __init__(self, lords, years):
        self.LORDS = lords
        self.YEARS = years


@pytest.mark.parametrize(
    "mutate, description",
    [
        (lambda t: ("Ve",) + t[1:], "first lord swapped"),
        (lambda t: t[:-1] + ("Ke",), "last lord duplicated from the first"),
        (lambda t: t[:4] + (t[5], t[4]) + t[6:], "two adjacent lords transposed"),
    ],
)
def test_negative_control_a_perturbed_lord_table_is_detected(mutate, description):
    perturbed = mutate(CLASSICAL_LORDS)
    assert perturbed != CLASSICAL_LORDS, "the mutation did nothing; control is vacuous"
    holder = _Perturbed(perturbed, CLASSICAL_YEARS)
    with pytest.raises(AssertionError):
        assert _values(holder, "LORDS") == CLASSICAL_LORDS, description


@pytest.mark.parametrize(
    "mutate, description",
    [
        (lambda t: (8,) + t[1:], "Ketu given 8 years instead of 7"),
        (lambda t: t[:1] + (19,) + t[2:], "Venus given Saturn's 19"),
        (lambda t: t[:8] + (16,), "Mercury given 16, breaking the 120 total"),
    ],
)
def test_negative_control_a_perturbed_year_table_is_detected(mutate, description):
    perturbed = mutate(CLASSICAL_YEARS)
    assert perturbed != CLASSICAL_YEARS, "the mutation did nothing; control is vacuous"
    holder = _Perturbed(CLASSICAL_LORDS, perturbed)
    with pytest.raises(AssertionError):
        assert _values(holder, "YEARS") == CLASSICAL_YEARS, description


def test_negative_control_a_single_altered_cell_breaks_mutual_identity():
    """The realistic failure: one copy edited, the others not.

    This is the scenario ADR-0023 D3's condition exists to catch, and it is
    exercised against real table values rather than against a fixture.
    """

    real = _values(kp_tables, "KP_YEARS")
    drifted = real[:3] + (real[3] + 1,) + real[4:]
    assert drifted != real
    assert sum(drifted) != CLASSICAL_TOTAL, "a one-year drift must break the 120 total"
    with pytest.raises(AssertionError):
        assert drifted == _values(legacy_kp, "YEARS"), "drift not detected"
    with pytest.raises(AssertionError):
        assert drifted == _values(dasha_tables, "DASHA_YEARS"), "drift not detected"


def test_negative_controls_left_the_real_tables_untouched():
    assert _values(legacy_kp, "LORDS") == CLASSICAL_LORDS
    assert _values(kp_tables, "KP_YEARS") == CLASSICAL_YEARS
    assert _values(dasha_tables, "DASHA_YEARS") == CLASSICAL_YEARS
