"""INTERPRETATION prerequisites, Stage 1 (ADR-0130): the publication-only registry mechanism (R1-R9) and the fail-closed
explanation boundary (L1-L8). No genuine source rule is published: genuine rules here come from a test source on test
snapshots, and quote nothing. Every record is synthetic."""

from __future__ import annotations

import ast
import dataclasses
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "engine" / "tests"))

import certify_evidence_foundations as certifier  # noqa: E402
import check_rule_registry  # noqa: E402
from test_evidence_wp_e4 import World  # noqa: E402

from engine.evidence import explanation_boundary as boundary  # noqa: E402
from engine.evidence import rule_registry  # noqa: E402
from engine.evidence.evidence import Polarity  # noqa: E402
from engine.evidence.evidence_identifiers import EvidenceId  # noqa: E402
from engine.evidence.evidence_store import EvidenceStore, item_to_record  # noqa: E402
from engine.evidence.store import StoreError  # noqa: E402

PINNED = rule_registry.pinned()
BOUNDARY_MODULE = ROOT / "engine" / "evidence" / "explanation_boundary.py"


def load(tmp_path, name="sourced", change=None, history_change=None):
    directory, digest = certifier.sourced_copy(tmp_path, name, change, history_change)
    return rule_registry.load_registry(directory, digest)


def genuine(registry):
    return registry.lookup(registry.by_key(certifier.GENUINE_KEY), 1, "base")


# ------------------------------------------------------------------ R: the publication-only registry mechanism

def test_r8_the_pinned_snapshot_and_its_pin_are_unchanged():
    assert PINNED.snapshot_sha256 == "ea8d185ff0786e1c2d68b8010b45b9721367e8e55efca49a4c1a4b8402643d0d"
    assert PINNED.sources() == () and PINNED.verifications() == () and all(item.synthetic for item in PINNED.rules())


def test_r1_a_genuine_rule_from_an_authorized_source_is_published_for_citation(tmp_path):
    rule = genuine(load(tmp_path))
    assert rule.synthetic is False and rule.citation.source == certifier.TEST_SOURCE["id"]
    assert rule.citation.locator == certifier.TEST_LOCATOR


@pytest.mark.parametrize("change,reason", [
    (lambda d: certifier._rehash(certifier._genuine(d), citation={"source": "SRC-OTHER", "locator": certifier.TEST_LOCATOR}),
     "synthetic rules only"),
    (lambda d: d["sources"][0].update(school="kp"), "synthetic rules only"),
], ids=["an unlisted source", "a source of another school"])
def test_r1_a_genuine_rule_from_any_other_source_is_refused(tmp_path, change, reason):
    with pytest.raises(rule_registry.RegistryError, match=reason):
        load(tmp_path, change=change)


def test_r1_a_non_synthetic_record_read_without_sources_is_refused(tmp_path):
    rule = genuine(load(tmp_path))
    with pytest.raises(rule_registry.RegistryError, match="synthetic rules only"):
        rule_registry.rule_from_record({**rule_registry.content_record(rule), "content_hash": rule.content_hash})


@pytest.mark.parametrize("locator", ["BPHS 24.109", "chapter 24", "verse 109, page 325", "chapter 24, verse 109",
                                     "chapter 0, verse 109, page 325", "chapter 24, verse 109, page 325 (approx.)"])
def test_r2_an_imprecise_locator_is_refused(tmp_path, locator):
    change = lambda d: certifier._rehash(certifier._genuine(d), citation={"source": certifier.TEST_SOURCE["id"],
                                                                          "locator": locator})
    with pytest.raises(rule_registry.RegistryError, match="names chapter, verse and page"):
        load(tmp_path, change=change)


@pytest.mark.parametrize("locator", ["chapter 24, verse 109, page 325", "chapter 24, verses 109-110, pages 325-326"])
def test_r2_a_precise_locator_is_accepted(tmp_path, locator):
    change = lambda d: certifier._rehash(certifier._genuine(d), citation={"source": certifier.TEST_SOURCE["id"],
                                                                          "locator": locator})
    assert genuine(load(tmp_path, change=change)).citation.locator == locator


def test_r3_an_independently_checked_claim_needs_a_matching_verification(tmp_path):
    with pytest.raises(rule_registry.RegistryError, match="no independent verification"):
        load(tmp_path, "unverified", change=certifier._claim_checked)
    with pytest.raises(rule_registry.RegistryError, match="does not match the published statement"):
        load(tmp_path, "mismatch", change=lambda d: (certifier._claim_checked(d), d["verifications"].append(
            certifier._verification(d, transcription_sha256="1" * 64))))
    verified = load(tmp_path, "verified", change=lambda d: (certifier._claim_checked(d), d["verifications"].append(
        certifier._verification(d))))
    assert len(verified.verifications()) == 1


def test_r3_the_transcription_digest_normalises_only_what_is_declared():
    assert rule_registry.statement_digest("a  b\n c") == rule_registry.statement_digest("a b c")
    assert rule_registry.statement_digest("a b c") != rule_registry.statement_digest("a b d")


def test_r4_a_verification_reviews_every_aspect(tmp_path):
    with pytest.raises(rule_registry.RegistryError, match="reviews exactly"):
        load(tmp_path, change=lambda d: (certifier._claim_checked(d), d["verifications"].append(
            certifier._verification(d, reviewed=["statement", "locator"]))))
    assert rule_registry.VERIFIED_ASPECTS == ("statement", "locator", "condition", "domain", "polarity")


@pytest.mark.parametrize("change,reason", [
    (lambda d: d["verifications"].append({**certifier._verification(d), "rule": 1, "version": 1, "variant": "base"}),
     "one published genuine rule"),
    (lambda d: d["sources"].append(dict(certifier.TEST_SOURCE)), "listed once"),
    (lambda d: d["sources"][0].update(witness_sha256="unpinned"), "pins its witness"),
    (lambda d: d["sources"][0].pop("rights_basis"), "only its schema's fields"),
    (lambda d: d.update(schema=rule_registry.SNAPSHOT_SCHEMA), "not a rule snapshot of this schema"),
    (lambda d: d.update(extra=1), "only its schema's fields"),
], ids=["a verification of a synthetic rule", "a source listed twice", "an unpinned witness", "no rights basis",
        "the plain schema name", "an undeclared field"])
def test_r1_r3_a_malformed_sourced_snapshot_fails_closed(tmp_path, change, reason):
    with pytest.raises(rule_registry.RegistryError, match=reason):
        load(tmp_path, change=change)


def test_r5_variants_stay_explicit_for_genuine_rules(tmp_path):
    registry = load(tmp_path)
    assert registry.variants(registry.by_key(certifier.GENUINE_KEY), 1) == ("base",)
    with pytest.raises(rule_registry.RegistryError, match="explicit variant"):
        registry.lookup(registry.by_key(certifier.GENUINE_KEY), 1, None)


def test_r6_a_genuine_rule_uses_an_issued_number_and_earlier_publications_are_unchanged(tmp_path):
    with pytest.raises(rule_registry.RegistryError, match="never issued"):
        load(tmp_path, "unissued", history_change=lambda history: history["allocations"].pop())
    directory, _digest = certifier.sourced_copy(tmp_path, "g3")
    previous = (json.loads((rule_registry.DATA_DIR / rule_registry.HISTORY_NAME).read_bytes()),
                json.loads((rule_registry.DATA_DIR / "snapshot.json").read_bytes()))
    assert check_rule_registry.check_against(*previous, directory) == []


def test_r7_no_measured_performance_and_strength_as_stated(tmp_path):
    rule = genuine(load(tmp_path))
    assert rule.certification.measured_performance is None and rule.declared_strength == "not stated"


def test_r9_a_genuine_rule_is_never_projected_or_registered(tmp_path, monkeypatch):
    registry = load(tmp_path)
    rule = genuine(registry)
    with pytest.raises(rule_registry.RegistryError, match="never projected into evidence"):
        registry.rule_version(rule.rule, 1, "base")
    monkeypatch.setattr(rule_registry, "pinned", lambda: registry)
    with EvidenceStore(tmp_path / "evidence.sqlite") as store:
        with pytest.raises(StoreError, match="never projected into evidence"):
            store.register_rule(certifier._genuine_projection(registry))


def test_r9_registry_lookups_for_citation_still_work(tmp_path):
    registry = load(tmp_path)
    assert genuine(registry).statement and certifier.GENUINE_KEY in {item.key for item in registry.rules()}


# ------------------------------------------------------------------ L: the explanation boundary

@pytest.fixture()
def items(tmp_path):
    world = World(tmp_path / "evidence.sqlite")
    first = world.store.persist(world.item(facts=("Sun longitude", "Moon longitude")))
    second = world.store.persist(world.item(facts=("Mars longitude",)))
    yield world.store, first, second
    world.store.close()


def candidate(scope, segments):
    return {"schema": boundary.EXPLANATION_SCHEMA, "scope": [value.value for value in scope], "segments": segments}


def test_l1_every_kind_renders_only_from_trusted_data(items):
    store, first, second = items
    item = store.load(first)
    lines = boundary.render(candidate((first, second), [
        {"kind": "rule_statement", "evidence": first.value}, {"kind": "rule_citation", "evidence": first.value},
        {"kind": "chart_fact", "evidence": first.value, "field": "houses"},
        {"kind": "calculated_input", "evidence": first.value, "index": 1},
        {"kind": "timing", "evidence": second.value}, {"kind": "polarity", "evidence": second.value},
        {"kind": "uncertainty", "evidence": first.value, "field": "rule_confidence"},
        {"kind": "no_answer"}]), store, PINNED)
    published = PINNED.lookup(item.rule.rule, item.rule.version, item.rule.variant)
    assert published.statement in lines[0] and published.citation.source in lines[1]
    assert "Moon longitude" in lines[3] and item.timing.label in lines[4] and "absent" in lines[6]
    assert lines[7] == boundary.ABSTENTION_TEXT


# The words each reason a candidate could once select would have asserted about the evidence or the question.
FORMER_REASON_CLAIMS = {"no_evidence": "no recorded evidence", "incomplete_lineage": "incomplete",
                        "conflicting_evidence": "conflict", "outside_scope": "outside the scope"}


def test_l6_a_no_answer_segment_renders_a_neutral_abstention_that_asserts_nothing(items):
    store, first, _second = items
    assert boundary.render(candidate((first,), [{"kind": "no_answer"}]), store, PINNED) == (boundary.ABSTENTION_TEXT,)
    assert not any(claim in boundary.ABSTENTION_TEXT.lower() for claim in FORMER_REASON_CLAIMS.values())
    assert boundary.SEGMENT_KEYS[boundary.SegmentKind.NO_ANSWER] == ("kind",)


@pytest.mark.parametrize("reason", sorted(FORMER_REASON_CLAIMS))
def test_l6_a_candidate_selected_reason_is_refused_over_valid_non_conflicting_evidence(items, reason):
    """The CEO's example: a valid, non-conflicting item must never yield the statement that evidence conflicts."""

    store, first, _second = items
    # The item passes every read check, is not recorded as contradictory, and no relationship is recorded at all.
    assert store.load(first).polarity is not Polarity.CONTRADICTORY and store.relationships() == []
    with pytest.raises(boundary.BoundaryError, match="carries exactly"):
        boundary.render(candidate((first,), [{"kind": "polarity", "evidence": first.value},
                                             {"kind": "no_answer", "reason": reason}]), store, PINNED)


@pytest.mark.parametrize("label,make,reason", [
    ("plain text", lambda f, s: "a new rule about Saturn", "carries exactly"),
    ("a free-text field", lambda f, s: {**candidate((f,), [{"kind": "polarity", "evidence": f.value}]), "text": "x"},
     "carries exactly"),
    ("a segment made of text", lambda f, s: candidate((f,), ["the tenth lord gives fame"]), "names its kind"),
    ("an undeclared kind", lambda f, s: candidate((f,), [{"kind": "rule_application", "evidence": f.value}]),
     "undeclared segment kind"),
    ("a stated rule", lambda f, s: candidate((f,), [{"kind": "rule_statement", "evidence": f.value, "statement": "x"}]),
     "carries exactly"),
    ("a named rule", lambda f, s: candidate((f,), [{"kind": "rule_citation", "evidence": f.value, "rule": "RUL-000002"}]),
     "carries exactly"),
    ("a stated polarity", lambda f, s: candidate((f,), [{"kind": "polarity", "evidence": f.value, "value": "negative"}]),
     "carries exactly"),
    ("an overridden value", lambda f, s: candidate((f,), [
        {"kind": "calculated_input", "evidence": f.value, "index": 0, "value": "Moon 12 Aries"}]), "carries exactly"),
    ("an undeclared chart field", lambda f, s: candidate((f,), [
        {"kind": "chart_fact", "evidence": f.value, "field": "effect"}]), "names one of"),
    ("a score", lambda f, s: candidate((f,), [{"kind": "uncertainty", "evidence": f.value, "field": "score"}]),
     "names one of"),
    ("a boolean index", lambda f, s: candidate((f,), [{"kind": "calculated_input", "evidence": f.value, "index": True}]),
     "by its index"),
    ("a reason in its own words", lambda f, s: candidate((f,), [{"kind": "no_answer", "reason": "unclear"}]),
     "carries exactly"),
    ("a malformed identifier", lambda f, s: candidate((f,), [{"kind": "polarity", "evidence": "first"}]),
     "not an EVD identifier"),
    ("evidence outside the scope", lambda f, s: candidate((f,), [{"kind": "polarity", "evidence": s.value}]),
     "not in the explanation's scope"),
    ("an input not recorded", lambda f, s: candidate((f,), [{"kind": "calculated_input", "evidence": f.value, "index": 9}]),
     "records no calculated input"),
    ("an empty scope", lambda f, s: candidate((), [{"kind": "no_answer"}]),
     "names the evidence in its scope"),
    ("another schema", lambda f, s: {**candidate((f,), [{"kind": "polarity", "evidence": f.value}]), "schema": "v0"},
     "this schema"),
])
def test_l2_to_l6_a_candidate_not_made_of_references_is_refused(items, label, make, reason):
    store, first, second = items
    with pytest.raises(boundary.BoundaryError, match=reason):
        boundary.render(make(first, second), store, PINNED)


def test_l4_an_item_failing_the_evidence_read_checks_is_refused(items):
    store, first, _second = items
    store._db.execute("INSERT INTO evidence_items (evidence_id, entity_id, recomputes, payload) VALUES (?, ?, NULL, ?)",
                      ("EVD-0000000900", "ENT-00000001", "{}"))
    with pytest.raises(boundary.BoundaryError, match="fails the evidence read checks"):
        boundary.render(candidate((first,), [{"kind": "polarity", "evidence": first.value}]) | {
            "scope": ["EVD-0000000900"], "segments": [{"kind": "polarity", "evidence": "EVD-0000000900"}]}, store, PINNED)


def test_l4_an_intact_row_whose_recorded_graph_is_missing_is_refused(items):
    """The row itself reads cleanly; only the store's full read, with its graph accounting, refuses it."""

    store, first, _second = items
    planted = EvidenceId.from_number(900)
    item = store.load(first)
    store._db.execute("INSERT INTO evidence_items (evidence_id, entity_id, recomputes, payload) VALUES (?, ?, NULL, ?)",
                      (planted.value, item.entity.value, json.dumps(item_to_record(planted, item))))
    assert store._stored_item(planted) == item
    with pytest.raises(boundary.BoundaryError, match="fails the evidence read checks"):
        boundary.render(candidate((planted,), [{"kind": "polarity", "evidence": planted.value}]), store, PINNED)


def test_l5_a_rule_the_pinned_registry_does_not_publish_is_refused(items):
    store, first, _second = items
    item = store.load(first)
    without = rule_registry.RuleRegistry(tuple(rule for rule in PINNED.rules() if rule.rule != item.rule.rule),
                                         PINNED.snapshot_sha256)
    with pytest.raises(boundary.BoundaryError, match="is not registered"):
        boundary.render(candidate((first,), [{"kind": "rule_statement", "evidence": first.value}]), store, without)


def test_l7_the_renderer_never_echoes_a_candidate_even_with_the_parse_weakened(items, monkeypatch):
    store, first, _second = items
    monkeypatch.setattr(boundary, "_exact", lambda name, data, keys: data)
    lines = boundary.render({**candidate((first,), [{"kind": "rule_statement", "evidence": first.value,
                                                      "statement": "PLANTED"}]), "text": "PLANTED"}, store, PINNED)
    assert not any("PLANTED" in line for line in lines)


def test_l8_the_contract_has_no_free_text_field_and_no_llm_or_network_path():
    tree = ast.parse(BOUNDARY_MODULE.read_text(encoding="utf-8"))
    imported = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module} | \
        {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
    assert not {name.split(".")[0] for name in imported} & {"openai", "anthropic", "requests", "urllib", "http",
                                                              "socket", "httpx"}
    assert [field.name for field in dataclasses.fields(boundary.Explanation)] == ["scope", "segments"]
    assert [field.name for field in dataclasses.fields(boundary.Segment)] == ["kind", "evidence", "field", "index"]
    assert set(boundary.SEGMENT_KEYS[kind] for kind in boundary.SegmentKind) and all(
        "text" not in keys and "statement" not in keys for keys in boundary.SEGMENT_KEYS.values())


# ------------------------------------------------------------------ the real gates fail on weakened checks

def _project_genuine(self, rule, version, variant):
    item = self.lookup(rule, version, variant)
    return rule_registry.RuleVersion(rule=item.rule, version=item.version, spec=rule_registry.RuleSpec(
        school=item.school, content_hash=item.content_hash, knowledge_snapshot_hash=self.snapshot_sha256,
        declared_strength=item.declared_strength, variant=item.variant,
        provenance=rule_registry.RecordProvenance(source="the pinned rule registry", method="published snapshot",
                                                  schema_version=rule_registry.SNAPSHOT_SCHEMA),
        data_class=rule_registry.DataClass.SYNTHETIC))


@pytest.mark.parametrize("name,weakened", [
    ("RuleRegistry.rule_version", _project_genuine),
    ("_require_authorized", lambda data, sources: None),
    ("_require_verified", lambda rules, verifications: None),
], ids=["a projection admitting genuine rules", "no source check", "no verification check"])
def test_the_real_gate_v_fails_when_a_publication_check_is_weakened(monkeypatch, name, weakened):
    owner, attribute = (rule_registry.RuleRegistry, "rule_version") if "." in name else (rule_registry, name)
    monkeypatch.setattr(owner, attribute, weakened)
    with pytest.raises((SystemExit, StoreError, rule_registry.RegistryError)):
        certifier.gate_v_genuine_rule_publication()


_STRICT_EXACT = boundary._exact


def _admit_without_scope(explanation, store, registry):
    named = tuple(explanation.scope) + tuple(item.evidence for item in explanation.segments if item.evidence is not None)
    return {evidence_id: store.load(evidence_id) for evidence_id in named}


@pytest.mark.parametrize("name,weakened", [
    ("_exact", lambda name, data, keys: data if isinstance(data, dict) and set(keys) <= set(data) else
     _STRICT_EXACT(name, data, keys)),
    ("admit", _admit_without_scope),
    ("_published", lambda item, registry: PINNED.lookup(item.rule.rule, item.rule.version, item.rule.variant)),
    ("_exact", lambda name, data, keys: _STRICT_EXACT(name, {key: value for key, value in data.items() if key != "reason"}
                                                      if name == "a no_answer segment" else data, keys)),
], ids=["extra keys admitted", "no scope check", "a registry other than the one given",
        "a candidate-selected reason admitted"])
def test_the_real_gate_w_fails_when_a_boundary_check_is_weakened(monkeypatch, capsys, name, weakened):
    """Each weakening still renders; the gate itself must find the candidate it did not refuse."""

    monkeypatch.setattr(boundary, name, weakened)
    with pytest.raises(SystemExit):
        certifier.gate_w_explanation_boundary()
    assert "CERTIFICATION FAIL: not refused:" in capsys.readouterr().out


def test_the_real_gate_w_fails_when_a_no_answer_segment_asserts_a_reason(monkeypatch, capsys):
    """The defect the CEO found, reinstated in the renderer: an abstention that says the evidence conflicts."""

    strict = boundary.render_segment
    monkeypatch.setattr(boundary, "render_segment", lambda segment, item, registry: (
        "The recorded evidence conflicts, so no single answer is given." if segment.kind is boundary.SegmentKind.NO_ANSWER
        else strict(segment, item, registry)))
    with pytest.raises(SystemExit):
        certifier.gate_w_explanation_boundary()
    assert "CERTIFICATION FAIL: a rendered sentence does not come from the evidence" in capsys.readouterr().out


def test_the_real_gates_v_and_w_pass_on_the_real_code():
    v, w = certifier.gate_v_genuine_rule_publication(), certifier.gate_w_explanation_boundary()
    assert v["refusals_verified"] >= 25 and v["controls_rejected"] >= 3
    assert w["refusals_verified"] >= 25 and w["controls_rejected"] >= 5
