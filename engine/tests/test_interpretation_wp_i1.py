"""WP-I1 (ADR-0133, PROPOSED): house-lord placement, closed condition evaluation, synthetic rule application and
deterministic explanation. Synthetic charts only."""

import dataclasses
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from engine.astronomy.profile import KP_KRISHNAMURTI, PARASHARI_LAHIRI
from engine.calculations.calculations import calculate
from engine.evidence import rule_registry
from engine.evidence.entity import DataClass
from engine.evidence.evidence_identifiers import RuleId
from engine.interpretation import application, conditions, explanation
from engine.models.birth_data import BirthData
from engine.parashari import house_lord

BIRTH = BirthData(1983, 6, 8, 11, 30, 0.0, 13.0827, 80.2707, "UTC")
PROVENANCE = calculate(BIRTH, profile=PARASHARI_LAHIRI).snapshot.provenance
GRAHAS = house_lord.PLACED_GRAHAS
ONE, THREE, KP_RULE, NADI_RULE = (RuleId.from_number(number) for number in (1, 3, 2, 4))


def _chart(ascendant, label="a synthetic chart", **placed):
    longitudes = {graha: 75.0 for graha in GRAHAS}
    longitudes.update(placed)
    snapshot = SimpleNamespace(provenance=PROVENANCE, houses=SimpleNamespace(ascendant=ascendant),
                               sidereal_planets={graha: SimpleNamespace(longitude=longitudes[graha]) for graha in GRAHAS})
    return application.SyntheticChart(house_lord.house_lords_from_snapshot(snapshot), DataClass.SYNTHETIC, label)


FIRING = _chart(5.0, Saturn=285.0, Sun=280.0, Moon=95.0)
QUIET = _chart(5.0, Saturn=10.0, Sun=130.0, Moon=65.0)
SPLIT = _chart(35.0, Moon=135.0)


# --------------------------------------------------------------- PARASHARI_HOUSE_LORD_V1

def test_house_signs_and_lords_follow_whole_sign_counting_from_the_lagna():
    assert [house_lord.house_sign(house, 11) for house in (1, 2, 3, 12)] == [11, 12, 1, 10]
    assert [house_lord.house_lord(house, 1) for house in range(1, 13)] == [
        "Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]


def test_a_real_kernel_chart_gives_every_lord_its_own_whole_sign_house():
    chart = house_lord.house_lords(BIRTH)
    assert chart.ascendant_sign == 8 and len(chart.lordships) == 12 and len(chart.placements) == 9
    for item in chart.lordships:
        assert item.lord_house == chart.placement(item.lord).house
        assert item.lord_sign == chart.placement(item.lord).sign


def test_house_lordship_refuses_another_profile_and_an_unprovenanced_snapshot():
    with pytest.raises(house_lord.HouseLordProfileError):
        house_lord.house_lords_from_snapshot(calculate(BIRTH, profile=KP_KRISHNAMURTI).snapshot)
    with pytest.raises(house_lord.HouseLordProfileError):
        house_lord.house_lords_from_snapshot(SimpleNamespace(provenance=None))
    real = calculate(BIRTH, profile=PARASHARI_LAHIRI).snapshot
    renamed = SimpleNamespace(provenance=dataclasses.replace(real.provenance, profile_name=KP_KRISHNAMURTI.name),
                              houses=real.houses, sidereal_planets=real.sidereal_planets)
    with pytest.raises(house_lord.HouseLordProfileError, match="requires the parashari_lahiri profile"):
        house_lord.house_lords_from_snapshot(renamed)


# --------------------------------------------------------------- conditions

def test_each_evaluated_kind_records_its_facts_and_its_answer():
    chart = FIRING.chart
    lord = conditions.evaluate(rule_registry.Condition("house_lord_in_house", (("house", 10), ("lord_of", 10))), chart)
    assert lord.holds and dict(lord.facts) == {"house_sign": 10, "lord": "Saturn", "lord_house": 10}
    moon = conditions.evaluate(rule_registry.Condition("planet_in_sign", (("planet", "Moon"), ("sign", 5))), chart)
    assert not moon.holds and moon.facts == (("planet_sign", 4),)


def test_an_unevaluated_kind_and_a_non_chart_are_refused():
    kp = rule_registry.Condition("cusp_sublord_signifies", (("cusp", 10), ("houses", (2, 6, 10))))
    with pytest.raises(conditions.ConditionError, match="is not evaluated here"):
        conditions.evaluate(kp, FIRING.chart)
    with pytest.raises(conditions.ConditionError, match="certified PARASHARI_HOUSE_LORD_V1 chart"):
        conditions.evaluate(rule_registry.Condition("planet_in_sign", (("planet", "Moon"), ("sign", 4))), object())


# --------------------------------------------------------------- application

def test_a_rule_fires_only_when_its_condition_and_activation_conditions_hold():
    assert [r.fired for r in application.apply_rule(FIRING, ONE, 1).records] == [True]
    assert [r.fired for r in application.apply_rule(QUIET, ONE, 1).records] == [False]
    partial = _chart(5.0, Saturn=285.0, Sun=10.0)
    assert [r.fired for r in application.apply_rule(partial, ONE, 2).records] == [False]
    assert [r.fired for r in application.apply_rule(FIRING, ONE, 2).records] == [True]


def test_every_variant_is_applied_kept_and_its_disagreement_stated():
    applied = application.apply_rule(SPLIT, THREE, 1)
    assert [(r.variant, r.fired, r.declared_polarity) for r in applied.records] == [
        ("reading-a", True, "positive"), ("reading-b", False, "negative")]
    assert applied.variants_disagree
    assert explanation.render_application(applied)[-1].startswith("The variants disagree in polarity")


@pytest.mark.parametrize("number", range(5, 11))
def test_every_genuine_rule_is_refused(number):
    with pytest.raises(application.ApplicationError, match="not published by the evidence-pinned registry"):
        application.apply_rule(FIRING, RuleId.from_number(number), 1)


def test_other_schools_and_undeclared_charts_are_refused():
    for rule, school in ((KP_RULE, "kp"), (NADI_RULE, "nakshatra_nadi")):
        with pytest.raises(application.ApplicationError, match=f"belongs to the {school} school"):
            application.apply_rule(FIRING, rule, 1)
    with pytest.raises(application.ApplicationError, match="only a chart declared synthetic"):
        application.SyntheticChart(FIRING.chart, "real", "a person")
    with pytest.raises(application.ApplicationError, match="only to a SyntheticChart"):
        application.apply_rule(FIRING.chart, ONE, 1)


def test_application_is_deterministic_and_every_record_is_hashed():
    first, second = (application.apply_rule(FIRING, THREE, 1) for _ in range(2))
    assert [application.canonical(r) for r in first.records] == [application.canonical(r) for r in second.records]
    for record in first.records:
        assert record.record_sha256 == application.record_hash(record)


def test_a_record_carries_no_prediction_field():
    names = tuple(field.name for field in dataclasses.fields(application.ApplicationRecord))
    assert names == application.RECORD_FIELDS
    assert not set(names) & set(application.FORBIDDEN_FIELDS)


# --------------------------------------------------------------- explanation

def test_an_explanation_comes_from_the_record_and_the_pinned_registry():
    record = application.apply_rule(FIRING, ONE, 1).records[0]
    lines = explanation.render(record)
    assert rule_registry.pinned().lookup(ONE, 1, "base").statement in lines[1]
    assert "the rule fired" in lines[-3] and lines[-1] == explanation.NON_CLAIM_TEXT


def test_a_tampered_record_or_text_is_refused():
    record = application.apply_rule(FIRING, ONE, 1).records[0]
    with pytest.raises(application.ApplicationError, match="does not match its content hash"):
        explanation.render(dataclasses.replace(record, chart_label="a real person"))
    draft = dataclasses.replace(record, fired=False, record_sha256="")
    with pytest.raises(application.ApplicationError, match="outcome does not follow"):
        explanation.render(dataclasses.replace(draft, record_sha256=application.record_hash(draft)))
    with pytest.raises(application.ApplicationError, match="exactly its schema's fields"):
        explanation.render("Saturn in the tenth gives fame.")


def test_gate_y_passes_with_its_refusals_and_controls():
    root = Path(__file__).resolve().parents[2]
    sys.path[:0] = [str(root), str(root / "scripts")]
    import certify_evidence_foundations

    result = certify_evidence_foundations.gate_y_rule_application()
    assert (result["refusals_verified"], result["legitimate_reads_preserved"], result["controls_rejected"]) == (39, 8, 12)
