"""EVIDENCE_FOUNDATIONS_V1 gate I: its selection controls are wrong by construction, for every seed the store draws.

Before this fix, the "another seed" and "first-k" controls were fixed records. When the store's random seed happened to
select the same set (about 1 draw in 105 for one or the other), the planted record was correct, the reproduction
check rightly accepted it, and the gate failed spuriously (CI run 42786854405, attempt 1). The production selection
procedure is unchanged; only the controls are.
"""

from __future__ import annotations

import dataclasses
import secrets
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import certify_evidence_foundations as certifier  # noqa: E402
from engine.evidence import ledger as model  # noqa: E402
from engine.evidence.event_identifiers import EventRecordId  # noqa: E402
from engine.evidence.ledger import PROCEDURE, Holdout, content_hash, ordered_selection, selection_hash  # noqa: E402

MEMBERS = tuple(EventRecordId.from_number(number) for number in range(1, 11))
SIZE = 4


def holdout_for(seed, members=MEMBERS, size=SIZE):
    selected = ordered_selection(seed, members, size)
    return Holdout(criteria="ten", members=members, content_hash=content_hash(members), seed=seed, procedure=PROCEDURE,
                   size=size, selected=selected, selection_hash=selection_hash(selected))


def seed_where(predicate, limit=200_000):
    """A seed from a fixed sequence whose selection satisfies `predicate`: reproducible adversarial draws."""

    for index in range(limit):
        seed = f"{index:064x}"[::-1]
        if predicate(ordered_selection(seed, MEMBERS, SIZE)):
            return seed
    raise AssertionError("no such seed in the search range")


#: The two draws that defeated the old controls.
FIRST_K_DRAW = seed_where(lambda selected: selected == MEMBERS[:SIZE])
OLD_OTHER_SEED_DRAW = seed_where(lambda selected: selected == ordered_selection("0" * 64, MEMBERS, SIZE))
#: A draw that is neither the first nor the last members.
ORDINARY_DRAW = seed_where(lambda selected: selected not in (MEMBERS[:SIZE], MEMBERS[-SIZE:]))


def assert_controls_wrong(holdout):
    assert certifier.record_reproduces(holdout)
    planted = certifier.planted_selections(holdout)
    assert [label for label, _ in planted] == ["another seed", "a fixed identifier order instead of the hash order"]
    for _label, record in planted:
        assert not certifier.record_reproduces(record)
        assert ordered_selection(record.seed, record.members, record.size) != record.selected
    another, fixed = (record for _label, record in planted)
    assert another.selected == holdout.selected and another.seed != holdout.seed
    assert fixed.seed == holdout.seed and fixed.selected != holdout.selected
    assert fixed.selection_hash == selection_hash(fixed.selected)


def assert_gate_fails(call, capsys, message):
    """The gate must exit through fail(), with `message`. On Windows, deleting the open SQLite file on the way out
    raises PermissionError with the SystemExit as its context; the SystemExit must still be in the chain."""

    with pytest.raises(BaseException) as info:
        call()
    chain, error = [], info.value
    while error is not None:
        chain.append(error)
        error = error.__context__
    assert any(isinstance(error, SystemExit) and error.code == 3 for error in chain), chain
    assert message in capsys.readouterr().out


# ------------------------------------------------------------------ guaranteed wrong

def test_the_old_controls_were_defeated_by_these_draws():
    """The regression: the fixed records the gate used to plant are correct for these seeds."""

    assert ordered_selection(FIRST_K_DRAW, MEMBERS, SIZE) == MEMBERS[:SIZE]
    old = holdout_for(OLD_OTHER_SEED_DRAW)
    assert certifier.record_reproduces(dataclasses.replace(old, seed="0" * 64))


@pytest.mark.parametrize("seed", [FIRST_K_DRAW, OLD_OTHER_SEED_DRAW], ids=["first-k draw", "old other-seed draw"])
def test_the_new_controls_are_wrong_on_the_draws_that_defeated_the_old(seed):
    assert_controls_wrong(holdout_for(seed))


def test_the_new_controls_are_wrong_for_many_random_draws():
    for _ in range(3000):
        assert_controls_wrong(holdout_for(secrets.token_hex(32)))


def test_the_fixed_order_falls_back_to_the_last_members_only_when_the_first_are_drawn():
    _label, fixed = certifier.planted_selections(holdout_for(FIRST_K_DRAW))[1]
    assert fixed.selected == MEMBERS[-SIZE:]
    other = seed_where(lambda selected: selected != MEMBERS[:SIZE])
    _label, fixed = certifier.planted_selections(holdout_for(other))[1]
    assert fixed.selected == MEMBERS[:SIZE]


def test_controls_refuse_to_plant_when_no_wrong_record_exists(monkeypatch, capsys):
    assert_gate_fails(lambda: certifier.planted_selections(holdout_for(FIRST_K_DRAW, members=MEMBERS[:7], size=4)),
                      capsys, "twice the selection size")
    holdout = holdout_for(FIRST_K_DRAW)
    monkeypatch.setattr(certifier, "OTHER_SEEDS", (holdout.seed,))
    assert_gate_fails(lambda: certifier.planted_selections(holdout), capsys, "would prove nothing")


# ------------------------------------------------------------------ the gate itself, reproducibly

@pytest.mark.parametrize("seed", [FIRST_K_DRAW, OLD_OTHER_SEED_DRAW], ids=["first-k draw", "old other-seed draw"])
def test_gate_i_passes_when_the_store_draws_a_defeating_seed(monkeypatch, seed):
    """The CI failure, replayed through the real store: the store's seed is pinned to a draw that defeated the old
    controls. The ledger's events are numbered 1 to 10 in its fresh database, matching MEMBERS."""

    monkeypatch.setattr(model.secrets, "token_hex", lambda _nbytes: seed)
    result = certifier.gate_i_holdout_leakage()
    assert result["controls_rejected"] == 10


def test_gate_i_is_reproducible_across_draws():
    results = [certifier.gate_i_holdout_leakage() for _ in range(25)]
    assert all(result == results[0] for result in results)
    assert results[0]["controls_rejected"] == 10
    assert "selection from a fixed identifier order instead of the hash order rejected" in results[0]["controls"]
    assert "selection from another seed rejected" in results[0]["controls"]


# ------------------------------------------------------------------ the controls detect a broken check

@pytest.mark.parametrize("broken,message", [
    (lambda holdout: True, "accepted a selection from another seed"),
    (lambda holdout: holdout.selection_hash == selection_hash(holdout.selected), "accepted a selection from another seed"),
    (lambda holdout: set(holdout.selected) <= set(holdout.members) and len(holdout.selected) == holdout.size,
     "accepted a selection from another seed"),
    (lambda holdout: ordered_selection(holdout.seed, holdout.members, holdout.size) == holdout.selected
     or holdout.selected == tuple(sorted(holdout.members))[:holdout.size]
     or holdout.selected == tuple(sorted(holdout.members))[-holdout.size:],
     "accepted a selection from a fixed identifier order"),
    (lambda holdout: False, "a clean holdout did not reproduce"),
], ids=["accepts everything", "checks only the selection hash", "checks only membership and size",
        "also accepts a fixed order", "rejects everything"])
def test_gate_i_fails_when_the_reproduction_check_is_broken(monkeypatch, capsys, broken, message):
    """Each broken check must make the gate fail, for the stated reason. The store's seed is pinned to a draw that is
    neither the first nor the last members, so which control catches each break is fixed, not left to the draw."""

    monkeypatch.setattr(model.secrets, "token_hex", lambda _nbytes: ORDINARY_DRAW)
    monkeypatch.setattr(certifier, "record_reproduces", broken)
    assert_gate_fails(certifier.gate_i_holdout_leakage, capsys, message)
