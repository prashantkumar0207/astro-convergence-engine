"""WP-E5 acceptance tests (ADR-0120 s6) and the RUL issuance safeguards (ADR-0121). Every rule here is synthetic."""

from __future__ import annotations

import ast
import dataclasses
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import author_rule_registry as author  # noqa: E402
import check_rule_registry as issuance_gate  # noqa: E402
from engine.evidence import rule_registry as registry  # noqa: E402
from engine.evidence.evidence import ProducingSystem, RuleSpec  # noqa: E402
from engine.evidence.evidence_identifiers import RuleId  # noqa: E402
from engine.evidence.evidence_store import EvidenceStore  # noqa: E402
from engine.evidence.store import StoreError  # noqa: E402

PINNED = registry.pinned()
FIRST = PINNED.by_key("synthetic.parashari.tenth-lord-in-tenth")
KP = PINNED.by_key("synthetic.kp.tenth-cusp-sublord")
VARIANTS = PINNED.by_key("synthetic.parashari.moon-in-fourth")
RECORD = {**registry.content_record(PINNED.lookup(FIRST, 1, "base")),
          "content_hash": PINNED.lookup(FIRST, 1, "base").content_hash}
REGISTRY_MODULE = ROOT / "engine" / "evidence" / "rule_registry.py"


def _write(path, data):
    path.write_bytes((json.dumps(data, sort_keys=True, indent=1) + "\n").encode("ascii"))


def _rehash(record, **changes):
    record.update(changes)
    record["content_hash"] = hashlib.sha256(registry.canonical(
        {key: value for key, value in record.items() if key != "content_hash"})).hexdigest()
    return record


@pytest.fixture()
def copy(tmp_path):
    def make(name="registry"):
        target = tmp_path / name
        shutil.copytree(registry.DATA_DIR, target)
        return target
    return make


@pytest.fixture()
def store(tmp_path):
    instance = EvidenceStore(tmp_path / "evidence.sqlite")
    yield instance
    instance.close()


# ------------------------------------------------------------------ AC1 to AC4 the rule record

@pytest.mark.parametrize("field", registry.RECORD_FIELDS)
def test_ac1_every_field_is_required(field):
    with pytest.raises(registry.RegistryError, match="refused"):
        registry.rule_from_record({key: value for key, value in RECORD.items() if key != field})


@pytest.mark.parametrize("change,message", [
    ({"school": "inferred"}, "unknown value"),
    ({"statement": " "}, "statement"),
    ({"citation": {"source": "", "locator": "x"}}, "citation source"),
    ({"condition": {"kind": "planet_in_house", "parameters": {"planet": "Moon"}}}, "takes exactly"),
    ({"condition": {"kind": "planet_in_house", "parameters": {"planet": "Pluto", "house": 4}}}, "must name one of"),
    ({"condition": {"kind": "code", "parameters": {}}}, "not in the declared schema"),
    ({"condition": "lambda chart: True"}, "only its schema's fields"),
    ({"activation_conditions": "none"}, "lists"),
    ({"effect": ""}, "effect"),
    ({"polarity": "maybe"}, "unknown value"),
    ({"known_variants": ["other"]}, "known variants"),
    ({"declared_strength": " "}, "declared_strength"),
])
def test_ac1_a_malformed_field_is_refused(change, message):
    with pytest.raises(registry.RegistryError, match=message):
        registry.rule_from_record(_rehash(dict(RECORD), **change))


def test_ac1_the_statement_and_the_condition_are_separate_and_the_condition_is_data():
    rule = PINNED.lookup(FIRST, 1, "base")
    assert isinstance(rule.statement, str) and isinstance(rule.condition, registry.Condition)
    assert all(not callable(value) for _name, value in rule.condition.parameters)
    assert set(registry.CONDITION_SCHEMA) >= {item.condition.kind for item in PINNED.rules()}


def test_ac2_versions_share_their_rul_number_and_the_school_never_changes():
    assert PINNED.versions(FIRST) == (1, 2)
    first, second = PINNED.lookup(FIRST, 1, "base"), PINNED.lookup(FIRST, 2, "base")
    assert first.rule == second.rule and first.school is second.school and first.content_hash != second.content_hash


def test_ac3_the_four_certification_claims_are_separate():
    fields = [field.name for field in dataclasses.fields(registry.CertificationLevel)]
    assert fields == ["transcription_fidelity", "source_attribution", "applicability_conditions",
                      "measured_performance"]
    states = list(registry.ClaimState)
    level = registry.CertificationLevel(states[2], states[0], states[1], None)
    assert (level.transcription_fidelity, level.source_attribution, level.applicability_conditions) == \
        (states[2], states[0], states[1])
    with pytest.raises(registry.RegistryError, match="measured performance"):
        registry.CertificationLevel(states[0], states[0], states[0], "0.7")


def test_ac4_variants_are_named_explicit_and_both_kept():
    assert PINNED.variants(VARIANTS, 1) == ("reading-a", "reading-b")
    a, b = PINNED.lookup(VARIANTS, 1, "reading-a"), PINNED.lookup(VARIANTS, 1, "reading-b")
    assert a.polarity is not b.polarity and a.known_variants == b.known_variants
    for missing in ("default", "", None):
        with pytest.raises(registry.RegistryError):
            PINNED.lookup(VARIANTS, 1, missing)


# ------------------------------------------------------------------ AC5, AC6 the pinned snapshot

def test_ac5_the_pinned_snapshot_verifies_and_the_pin_is_in_code():
    manifest = json.loads((registry.DATA_DIR / registry.MANIFEST_NAME).read_bytes())
    raw = (registry.DATA_DIR / manifest["snapshot"]).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == manifest["sha256"] == registry.PINNED_SNAPSHOT_SHA256
    assert PINNED.snapshot_sha256 == registry.PINNED_SNAPSHOT_SHA256


@pytest.mark.parametrize("case,message", [
    ("changed byte", "do not match the pinned hash"),
    ("changed pin", "differs from the pinned hash"),
    ("missing snapshot", "cannot be read"),
    ("missing manifest", "cannot be read"),
    ("schema violation", "only its schema's fields"),
])
def test_ac5_each_violation_fails_closed(copy, case, message):
    target = copy()
    pin = registry.PINNED_SNAPSHOT_SHA256
    if case == "changed byte":
        raw = (target / "snapshot.json").read_bytes()
        (target / "snapshot.json").write_bytes(raw.replace(b"Synthetic fixture", b"Planted fixture", 1))
    elif case == "changed pin":
        pin = "0" * 64
    elif case == "missing snapshot":
        (target / "snapshot.json").unlink()
    elif case == "missing manifest":
        (target / registry.MANIFEST_NAME).unlink()
    else:
        data = json.loads((target / "snapshot.json").read_bytes())
        data["extra"] = 1
        _write(target / "snapshot.json", data)
        pin = hashlib.sha256((target / "snapshot.json").read_bytes()).hexdigest()
        manifest = json.loads((target / registry.MANIFEST_NAME).read_bytes())
        _write(target / registry.MANIFEST_NAME, dict(manifest, sha256=pin))
    with pytest.raises(registry.RegistryError, match=message):
        registry.load_registry(target, pin)


def test_ac6_the_registry_reads_no_path_outside_its_pinned_snapshot():
    tree = ast.parse(REGISTRY_MODULE.read_text(encoding="utf-8"))
    imported = {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names} | \
        {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}
    assert not [name for name in imported if name.startswith("engine.knowledge")]
    assert registry.DATA_DIR == REGISTRY_MODULE.parent / "rule_registry_data"
    opens = [ast.unparse(node) for node in ast.walk(tree) if isinstance(node, ast.Call)
             and isinstance(node.func, ast.Name) and node.func.id == "open"]
    assert opens == []  # every read goes through the directory the loader is given


# ------------------------------------------------------------------ AC7, AC8 refusals and evidence binding

def test_ac7_unregistered_rules_and_versions_are_refused():
    for rule, version, variant in ((RuleId.from_number(9999), 1, "base"), (FIRST, 3, "base"), (FIRST, 1, "other")):
        with pytest.raises(registry.RegistryError, match="is not registered"):
            PINNED.lookup(rule, version, variant)
    with pytest.raises(registry.RegistryError):
        PINNED.by_key("synthetic.never-authored")


def test_ac8_the_store_admits_only_the_published_rule_exactly(store):
    good = PINNED.rule_version(FIRST, 1, "base")
    assert store.register_rule(good) == good
    for change, message in (({"school": ProducingSystem.KP}, "school differs"),
                            ({"content_hash": "e" * 64}, "content hash differs"),
                            ({"knowledge_snapshot_hash": "f" * 64}, "snapshot hash differs"),
                            ({"declared_strength": "planted"}, "declared strength differs"),
                            ({"variant": "reading-a"}, "is not registered")):
        with pytest.raises(StoreError, match=message):
            store.register_rule(dataclasses.replace(good, spec=dataclasses.replace(good.spec, **change)))
    assert [rule.spec.knowledge_snapshot_hash for rule in store.rule_versions(FIRST)] == [PINNED.snapshot_sha256]


# ------------------------------------------------------------------ ADR-0121 the RUL issuance safeguards

def test_adr0121_the_store_issues_no_rul_and_accepts_no_free_standing_spec(store):
    with pytest.raises(StoreError, match="issues EVD only"):
        store.issued_count("RUL")
    spec = RuleSpec(school=ProducingSystem.PARASHARI, content_hash="a" * 64, knowledge_snapshot_hash="b" * 64,
                    declared_strength="x", variant="base", provenance=PINNED.rule_version(FIRST, 1, "base").spec.provenance,
                    data_class=PINNED.rule_version(FIRST, 1, "base").spec.data_class)
    with pytest.raises(StoreError, match="registry's RuleVersion"):
        store.register_rule(spec)
    assert not hasattr(store, "register_rule_version")


def test_adr0121_duplicate_registration_unissued_numbers_and_rebinding_are_refused(store):
    good = PINNED.rule_version(FIRST, 1, "base")
    store.register_rule(good)
    with pytest.raises(StoreError, match="already registered"):
        store.register_rule(good)
    with pytest.raises(StoreError, match="is not registered"):
        store.register_rule(dataclasses.replace(good, rule=RuleId.from_number(9999)))
    with pytest.raises(StoreError, match="is not registered"):
        store.register_rule(dataclasses.replace(good, version=7))
    rebound = dataclasses.replace(PINNED.rule_version(KP, 1, "base"), rule=FIRST)
    with pytest.raises(StoreError, match="differs"):
        store.register_rule(rebound)


@pytest.mark.parametrize("label", ["duplicate issuance", "reuse", "rebinding"])
def test_adr0121_the_history_refuses_duplicate_issuance_reuse_and_rebinding(copy, label):
    target = copy()
    history = json.loads((target / registry.HISTORY_NAME).read_bytes())
    if label == "duplicate issuance":
        history["allocations"].append(dict(history["allocations"][0], number=len(history["allocations"]) + 1))
        message = "issued twice"
    elif label == "reuse":
        history["allocations"][1]["number"] = 1
        message = "issued once, in order"
    else:
        history["allocations"][2]["key"] = "synthetic.planted"
        message = "rebinds it"
    _write(target / registry.HISTORY_NAME, history)
    with pytest.raises(registry.RegistryError, match=message):
        registry.load_registry(target, registry.PINNED_SNAPSHOT_SHA256)


def test_adr0121_a_snapshot_never_allocates(copy):
    target = copy()
    data = json.loads((target / "snapshot.json").read_bytes())
    _rehash(data["rules"][0], rule=777)
    _write(target / "snapshot.json", data)
    pin = hashlib.sha256((target / "snapshot.json").read_bytes()).hexdigest()
    manifest = json.loads((target / registry.MANIFEST_NAME).read_bytes())
    _write(target / registry.MANIFEST_NAME, dict(manifest, sha256=pin))
    with pytest.raises(registry.RegistryError, match="never issued by the authoring process"):
        registry.load_registry(target, pin)


def test_adr0121_the_authoring_process_allocates_append_only(copy):
    target = copy()
    source = json.loads((target / "source.json").read_bytes())
    new_rule = json.loads(json.dumps(source["rules"][1]))
    new_rule["key"] = "synthetic.kp.planted-new-rule"
    source["rules"].append(new_rule)
    _write(target / "source.json", source)
    before = json.loads((target / registry.HISTORY_NAME).read_bytes())["allocations"]
    history, _snapshot, _manifest = author.build(target)
    after = json.loads(history)["allocations"]
    assert after[:len(before)] == before and after[-1] == {"number": len(before) + 1,
                                                           "key": "synthetic.kp.planted-new-rule", "school": "kp"}
    source["rules"] = source["rules"][:-1]
    _write(target / "source.json", source)
    (target / registry.HISTORY_NAME).write_bytes(history)
    with pytest.raises(SystemExit, match="never authored"):
        author.build(target)


def test_adr0121_the_committed_registry_is_exactly_the_authoring_output():
    assert issuance_gate.check_load(registry.DATA_DIR, registry.PINNED_SNAPSHOT_SHA256) == []
    assert issuance_gate.check_authored(registry.DATA_DIR) == []


def test_adr0121_the_gate_refuses_a_rewritten_or_withdrawn_version_against_the_base(copy):
    history = json.loads((registry.DATA_DIR / registry.HISTORY_NAME).read_bytes())
    snapshot = json.loads((registry.DATA_DIR / "snapshot.json").read_bytes())
    rewritten = json.loads(json.dumps(snapshot))
    rewritten["rules"][0]["content_hash"] = "0" * 64
    assert any("was rewritten" in error for error in issuance_gate.check_against(history, rewritten,
                                                                                registry.DATA_DIR))
    shorter = dict(history, allocations=history["allocations"] + [{"number": 99, "key": "k", "school": "kp"}])
    assert any("dropped, reused or rebound" in error for error in issuance_gate.check_against(shorter, snapshot,
                                                                                            registry.DATA_DIR))
    assert issuance_gate.check_against(history, snapshot, registry.DATA_DIR) == []


def test_adr0121_the_negative_controls_script_catches_every_planted_violation():
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / "rule_registry_negative_controls.py")],
                            capture_output=True, text=True)
    assert result.returncode == 0 and "8 planted violations" in result.stdout, result.stdout


# ------------------------------------------------------------------ AC9 to AC13

def test_ac9_no_llm_client_free_text_path_or_dynamic_evaluation():
    tree = ast.parse(REGISTRY_MODULE.read_text(encoding="utf-8"))
    imported = {alias.name.split(".")[0] for node in ast.walk(tree) if isinstance(node, ast.Import)
                for alias in node.names} | \
        {node.module.split(".")[0] for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}
    assert not imported & {"openai", "anthropic", "requests", "urllib"}
    calls = {node.func.id for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)}
    assert not calls & {"eval", "exec", "compile", "__import__"}
    with pytest.raises(registry.RegistryError, match="refused"):
        registry.rule_from_record({**RECORD, "generated_text": "a rule an LLM wrote"})


def test_ac10_every_rule_is_cited():
    assert all(item.citation.source and item.citation.locator for item in PINNED.rules())


def test_ac11_every_rule_is_synthetic_and_unmarked_rules_are_refused():
    assert all(item.synthetic for item in PINNED.rules())
    with pytest.raises(registry.RegistryError, match="synthetic rules only"):
        registry.rule_from_record(_rehash(dict(RECORD), synthetic=False))


def test_ac12_nothing_is_applied_and_no_calculation_is_imported():
    tree = ast.parse(REGISTRY_MODULE.read_text(encoding="utf-8"))
    imported = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}
    assert not [name for name in imported if name.startswith(("engine.astronomy", "engine.astrology", "engine.dasha",
                                                             "engine.transits", "engine.kp", "engine.parashari"))]
    public = [name for name in dir(registry.RuleRegistry) if not name.startswith("_")]
    assert not [name for name in public if any(word in name for word in ("apply", "evaluate", "match", "fire"))]


def test_ac13_no_certified_rule_table_is_touched():
    changed = subprocess.run(["git", "-C", str(ROOT), "diff", "--name-only", "origin/main", "--",
                              "engine/astrology", "engine/astronomy", "engine/knowledge/data"],
                             capture_output=True, text=True)
    assert changed.returncode != 0 or changed.stdout.strip() == ""


def _evidence_world(store):
    """A synthetic entity in `store`, the published RUL-1 v1 base rule registered, and an item builder naming a rule
    reference of the caller's choosing."""

    from engine.evidence.entity import (ChartCandidate, DataClass, EntityKind, OriginCertainty, OriginMoment, Person,
                                        RecordProvenance, Shape)
    from engine.evidence.evidence import (CONFIDENCE_COMPONENTS, CalculatedInput, ChartContext, ChartReference,
                                          Confidence, Domain, EvidenceItem, Lineage, Polarity, RuleReference,
                                          TimingContext, TimingKind)
    from engine.models.provenance import Provenance

    prov = RecordProvenance(source="synthetic fixture", method="hand-written test data", schema_version="h5-v1")
    chart = ChartCandidate(label="natal", origin=OriginMoment(local_datetime="2000-01-01T12:00:00", timezone="UTC",
                                                              timezone_source="fixture", latitude=10.0, longitude=20.0,
                                                              precision="minute"),
                           origin_certainty=OriginCertainty.REPORTED, provenance=prov)
    entity = store.entities.persist(Person(kind=EntityKind.PERSON, shape=Shape.ORIGIN, charts=(chart,),
                                           applicable_domains=("career",), applicable_systems=("parashari",),
                                           provenance=prov, data_class=DataClass.SYNTHETIC))
    good = PINNED.rule_version(FIRST, 1, "base")
    store.register_rule(good)
    calc = Provenance(profile_name="parashari_lahiri", ayanamsa_mode=1, frame="sidereal", house_system="W",
                      node_policy="mean", ephemeris_mode="swieph")

    def item(variant, rule=FIRST, version=1):
        return EvidenceItem(
            entity=entity, domain=Domain.JATAKA, question=None, producing_system=ProducingSystem.PARASHARI,
            rule=RuleReference(rule=rule, version=version, variant=variant),
            declared_strength=good.spec.declared_strength, measured_reliability=None,
            lineage=Lineage(inputs=(CalculatedInput(fact="Moon longitude", provenance=calc),), inputs_complete=True,
                            derivations_complete=True),
            chart=ChartReference(entity_revision=1, chart_label="natal"),
            chart_context=ChartContext(varga="D1", planets=("Moon",), houses=(10,), signs=(4,), significators=()),
            timing=TimingContext(kind=TimingKind.DASHA, label="synthetic", start="2010-01-01", end="2011-01-01"),
            polarity=Polarity.POSITIVE, confidence=Confidence(**{name: None for name in CONFIDENCE_COMPONENTS}),
            historical_performance=None, derived_from=(), recomputes=None, provenance=prov,
            data_class=DataClass.SYNTHETIC)
    return good, item


def _plant_row(store, key, rule_version):
    """A row written straight into the table, bypassing register_rule: what a forged or corrupted store holds."""

    from engine.evidence.evidence_store import rule_to_record

    store._db.execute("INSERT INTO registered_rule_versions (rule_id, version, variant, payload) VALUES (?, ?, ?, ?)",
                      (*key, json.dumps(rule_to_record(rule_version))))


def test_ac8_new_evidence_names_only_a_rule_of_the_pinned_snapshot_in_force(store):
    """A rule version recorded under another snapshot stays historical: new evidence cannot name it (AC8)."""

    good, item = _evidence_world(store)
    stale = dataclasses.replace(good, spec=dataclasses.replace(good.spec, variant="stale",
                                                               knowledge_snapshot_hash="f" * 64))
    _plant_row(store, (FIRST.value, 1, "stale"), stale)
    assert store.persist(item("base")).number == 1
    with pytest.raises(StoreError, match="another snapshot"):
        store.persist(item("stale"))


UNISSUED = RuleId.from_number(999999)


def _forged_rows(good):
    """Rows the pinned registry does not publish, each carrying the pinned snapshot hash (CEO HOLD on PR #56,
    item 1): the reference the evidence names, the row's key, its payload, and the refusal expected."""

    def spec(**changes):
        return dataclasses.replace(good, spec=dataclasses.replace(good.spec, **changes))

    second = PINNED.rule_version(FIRST, 2, "base")
    return {
        "a forged variant": ((FIRST, 1, "forged"), (FIRST.value, 1, "forged"), spec(variant="forged"),
                             "not published by the pinned registry"),
        "an unissued RUL identity": ((UNISSUED, 1, "base"), (UNISSUED.value, 1, "base"),
                                     dataclasses.replace(good, rule=UNISSUED), "not published by the pinned registry"),
        "a payload naming another published identity than its key": (
            (FIRST, 2, "base"), (FIRST.value, 2, "base"), good, "differs from the pinned registry's publication"),
        "a published identity with forged content": (
            (FIRST, 2, "base"), (FIRST.value, 2, "base"),
            dataclasses.replace(second, spec=dataclasses.replace(second.spec, content_hash="e" * 64)),
            "differs from the pinned registry's publication"),
        "a published identity with forged declared strength": (
            (FIRST, 2, "base"), (FIRST.value, 2, "base"),
            dataclasses.replace(second, spec=dataclasses.replace(second.spec, declared_strength="planted")),
            "differs from the pinned registry's publication"),
    }


@pytest.mark.parametrize("case", ["a forged variant", "an unissued RUL identity",
                                  "a payload naming another published identity than its key",
                                  "a published identity with forged content",
                                  "a published identity with forged declared strength"])
def test_ac7_ac8_persist_refuses_a_recorded_row_the_pinned_registry_does_not_publish(store, case):
    """A row carrying the pinned snapshot hash is still refused unless it is exactly the published rule under the
    identity the evidence names. The refusal takes no EVD number, and every recorded row stays in place."""

    good, item = _evidence_world(store)
    reference, key, row, reason = _forged_rows(good)[case]
    assert row.spec.knowledge_snapshot_hash == PINNED.snapshot_sha256
    _plant_row(store, key, row)
    with pytest.raises(StoreError, match=reason):
        store.persist(item(reference[2], rule=reference[0], version=reference[1]))
    assert store.issued_count("EVD") == 0 and store.evidence_ids() == []
    assert store.persist(item("base")).number == 1
    assert row in store.rule_versions(reference[0])


def test_ac8_historical_snapshot_records_are_preserved_beside_the_published_rule(store):
    """The exact-publication check refuses new evidence only: a row from another snapshot stays readable, keeps its
    AC8 refusal, and evidence already persisted against the published rule still loads."""

    good, item = _evidence_world(store)
    stale = dataclasses.replace(good, spec=dataclasses.replace(good.spec, variant="stale",
                                                               knowledge_snapshot_hash="f" * 64))
    _plant_row(store, (FIRST.value, 1, "stale"), stale)
    first = store.persist(item("base"))
    assert store.rule_versions(FIRST) == [good, stale]
    with pytest.raises(StoreError, match="another snapshot"):
        store.persist(item("stale"))
    assert store.load(first) == item("base") and store.evidence_ids() == [first]
