"""SUPPORT_PATHS_V1 CERTIFICATION RUNNER (ADR-0099 s3, ADR-0108 s4 item 5).

Regenerates certification/SUPPORT_PATHS_V1_certification.json FROM SCRATCH on every
run; the stored JSON is never accepted as proof.

ADR-0108 s4 item 5 leaves a dead-path uncovered function three ways out: an owner
ruling, removal of its dead caller, or certification. These functions stay in use by
ADR-0099 s3's literal counting rule, and this runner certifies them. It exempts nothing
and it adds no production capability.

Gates, each against a reference that is not the code under test:
  A  equal_house_from_ascendant against exact rational arithmetic and literal cases.
  B  map_planet against exact rational arithmetic.
  C  to_utc against offset subtraction, and against literal UTC instants for named zones.
  D  the knowledge access path against the data files read independently.
  E  natural_relationship against PyJHora's published naisargika tables.
  F  rashi_chart's neutrality over the gated build_chart, on real snapshots.
  G  every comparator above rejects planted wrong functions. A gate that cannot fail
     is not evidence.

Exit 0 = PASS, 3 = FAIL.
"""

import dataclasses
import hashlib
import importlib.metadata
import json
import math
import sys
from datetime import date, datetime, timedelta, timezone
from fractions import Fraction
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

sys.path.insert(0, str(ROOT / "scripts"))
import certification_support as support  # noqa: E402

from engine.astrology.chart_builder import build_chart  # noqa: E402
from engine.astrology.dignity import Relationship, natural_relationship  # noqa: E402
from engine.astrology.house import equal_house_from_ascendant, whole_sign_house  # noqa: E402
from engine.astrology.planet_mapper import map_planet  # noqa: E402
from engine.astrology.rashi_chart import rashi_chart  # noqa: E402
from engine.astronomy.profile import KP_KRISHNAMURTI, PARASHARI_LAHIRI  # noqa: E402
from engine.calculations.calculations import calculate  # noqa: E402
from engine.core.timezone_engine import to_utc  # noqa: E402
from engine.knowledge.loader import KnowledgeLoader  # noqa: E402
from engine.knowledge.registry import KnowledgeRegistry  # noqa: E402
from engine.knowledge.repository import KnowledgeRepository  # noqa: E402
from engine.knowledge.validator import SchemaValidator  # noqa: E402
from engine.models.birth_data import BirthData  # noqa: E402
from engine.evidence.entity import (  # noqa: E402
    ChartCandidate, DataClass, EntityKind, EntityLink, EventEntity, GeographicEntity, Organisation,
    OriginCertainty, OriginMoment, Person, Question, RecordProvenance, Shape, rectification_permitted,
)
from engine.evidence.identifiers import EntityId, IdentifierError  # noqa: E402
from engine.evidence.store import EntityStore, StoreError, subject_from_record, subject_to_record  # noqa: E402

#: Set by gate_e_natural_relationship() itself. PyJHora is required only by Gate E.
PYJHORA_VERSION = None

DATA_DIR = ROOT / "engine" / "knowledge" / "data"
DATASETS = ("planets", "signs", "houses", "dignities", "natural_relationships", "nakshatras")

#: Exact in binary, so the rational reference and the float code see the same values.
GRID_STEP = 3.75
GRID = tuple(index * GRID_STEP + offset for index in range(96) for offset in (0.0, 0.125))

#: (longitude, ascendant, house), derived by hand from the convention in
#: engine/astrology/longitude_utils.py: a value within 1e-10 below a boundary is in the next division.
EQUAL_HOUSE_LITERALS = (
    (15.0, 15.0, 1), (45.0, 15.0, 2), (345.0, 15.0, 12), (95.0, 100.0, 12), (15.0, 345.0, 2),
    (360.0, 0.0, 1), (735.0, 0.0, 1), (-15.0, 0.0, 12), (-1e-16, 0.0, 1),
    (30.0, 0.0, 2), (29.999999, 0.0, 1), (29.99999999995, 0.0, 2), (329.999999, 0.0, 11),
)

OFFSET_INSTANTS = (
    datetime(1900, 3, 1, 12, 0), datetime(2000, 1, 1, 0, 0),
    datetime(2024, 2, 29, 23, 59, 59, 500000), datetime(2038, 1, 19, 3, 14, 7),
)
#: (zone, local wall clock, the UTC instant it denotes), from the published zone rules.
NAMED_ZONE_LITERALS = (
    ("Asia/Kolkata", datetime(2024, 1, 15, 12, 0), datetime(2024, 1, 15, 6, 30)),
    ("Asia/Kathmandu", datetime(2024, 1, 15, 12, 0), datetime(2024, 1, 15, 6, 15)),
    ("America/New_York", datetime(2024, 1, 15, 12, 0), datetime(2024, 1, 15, 17, 0)),
    ("America/New_York", datetime(2024, 7, 15, 12, 0), datetime(2024, 7, 15, 16, 0)),
    ("Europe/London", datetime(2024, 1, 15, 12, 0), datetime(2024, 1, 15, 12, 0)),
    ("Europe/London", datetime(2024, 7, 15, 12, 0), datetime(2024, 7, 15, 11, 0)),
    ("Australia/Sydney", datetime(2024, 1, 15, 12, 0), datetime(2024, 1, 15, 1, 0)),
    ("Australia/Sydney", datetime(2024, 7, 15, 12, 0), datetime(2024, 7, 15, 2, 0)),
)

GRAHAS = ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn")

#: Synthetic instants chosen for spread, not drawn from any certification holdout.
D1_CASES = (
    (1950, 6, 15, 4, 30, 0.0, 28.6, 77.2), (1975, 1, 1, 0, 0, 0.0, -33.9, 151.2),
    (1988, 11, 23, 18, 45, 30.0, 51.5, -0.1), (2000, 3, 20, 7, 35, 0.0, 0.0, 0.0),
    (2012, 8, 9, 12, 0, 0.0, 40.7, -74.0), (2024, 2, 29, 23, 59, 59.0, 19.1, 72.9),
)


def fail(message):
    print("SUPPORT_PATHS CERTIFICATION FAIL:", message)
    sys.exit(3)


def _exact_sign(longitude) -> int:
    return math.floor((Fraction(longitude) % 360) / 30) + 1


def equal_house_mismatches(function) -> int:
    mismatches = 0
    for longitude in GRID:
        for ascendant in GRID:
            exact = math.floor(((Fraction(longitude) - Fraction(ascendant)) % 360) / 30) + 1
            mismatches += function(longitude, ascendant) != exact
    for longitude, ascendant, house in EQUAL_HOUSE_LITERALS:
        mismatches += function(longitude, ascendant) != house
    return mismatches


def gate_a_equal_house():
    mismatches = equal_house_mismatches(equal_house_from_ascendant)
    if mismatches:
        fail(f"equal_house_from_ascendant: {mismatches} mismatches")
    return {"classification": "mathematical_correctness", "grid_comparisons": len(GRID) ** 2,
            "literal_cases": len(EQUAL_HOUSE_LITERALS), "mismatches": 0}


def map_planet_mismatches(function) -> int:
    mismatches = 0
    for longitude in GRID:
        for ascendant in GRID[::4]:
            sign = _exact_sign(longitude)
            expected = {
                "longitude": longitude,
                "sign": sign,
                "degree": float(Fraction(longitude) % 30),
                "house": (sign - _exact_sign(ascendant)) % 12 + 1,
            }
            mismatches += function(longitude=longitude, ascendant=ascendant) != expected
    return mismatches


def gate_b_map_planet():
    mismatches = map_planet_mismatches(map_planet)
    if mismatches:
        fail(f"map_planet: {mismatches} mismatches")
    return {"classification": "mathematical_correctness", "grid_comparisons": len(GRID) * len(GRID[::4]),
            "mismatches": 0}


def to_utc_mismatches(function) -> int:
    mismatches = 0
    for minutes in range(-12 * 60, 14 * 60 + 1, 15):
        offset = timedelta(minutes=minutes)
        for naive in OFFSET_INSTANTS:
            converted = function(naive.replace(tzinfo=timezone(offset)))
            expected = (naive - offset).replace(tzinfo=timezone.utc)
            mismatches += converted != expected or converted.utcoffset() != timedelta(0)
    for zone, local, instant in NAMED_ZONE_LITERALS:
        converted = function(local.replace(tzinfo=ZoneInfo(zone)))
        mismatches += converted.replace(tzinfo=None) != instant or converted.utcoffset() != timedelta(0)
    return mismatches


def gate_c_to_utc():
    mismatches = to_utc_mismatches(to_utc)
    if mismatches:
        fail(f"to_utc: {mismatches} mismatches")
    for bad, expected_error in ((datetime(2024, 1, 1, 12, 0), ValueError), ("2024-01-01", TypeError)):
        try:
            to_utc(bad)
            fail(f"to_utc accepted {bad!r}")
        except expected_error:
            pass
    return {"classification": "mathematical_correctness",
            "offsets_checked": len(range(-12 * 60, 14 * 60 + 1, 15)), "instants_per_offset": len(OFFSET_INSTANTS),
            "named_zone_literals": len(NAMED_ZONE_LITERALS), "refusals_verified": 2, "mismatches": 0}


def _reference(dataset):
    return json.loads((DATA_DIR / f"{dataset}.json").read_bytes())


def knowledge_mismatches(read) -> int:
    """`read` gets a dataset name and returns what the access path under test returned."""

    return sum(read(dataset) != _reference(dataset) for dataset in DATASETS)


def _registry_read(dataset):
    KnowledgeRegistry.clear()
    return KnowledgeRegistry.get(dataset)


def gate_d_knowledge_access():
    paths = {
        "KnowledgeLoader.load": lambda name: KnowledgeLoader.load(DATA_DIR / f"{name}.json"),
        "KnowledgeRepository.load_json": lambda name: KnowledgeRepository.load_json(f"{name}.json"),
        "SchemaValidator.load_json": lambda name: SchemaValidator.load_json(DATA_DIR / f"{name}.json"),
        "KnowledgeRegistry.get": _registry_read,
    }
    accessors = {"planets": KnowledgeRepository.planets, "signs": KnowledgeRepository.signs,
                 "houses": KnowledgeRepository.houses, "dignities": KnowledgeRepository.dignities,
                 "natural_relationships": KnowledgeRepository.natural_relationships,
                 "nakshatras": KnowledgeRepository.nakshatras}
    if set(accessors) != set(DATASETS):
        fail("the accessor table does not match the data sets")
    paths["KnowledgeRepository accessors"] = lambda name: accessors[name]()
    for label, read in paths.items():
        mismatches = knowledge_mismatches(read)
        if mismatches:
            fail(f"{label}: {mismatches} data sets differ from the file")
    for loader in (KnowledgeLoader.load, SchemaValidator.load_json):
        try:
            loader(DATA_DIR / "absent.json")
            fail(f"{loader.__qualname__} read an absent file")
        except FileNotFoundError:
            pass
    KnowledgeRegistry.clear()
    first = KnowledgeRegistry.get("planets")
    if KnowledgeRegistry.get("planets") is not first:
        fail("KnowledgeRegistry.get did not serve from its cache")
    KnowledgeRegistry.clear()
    if KnowledgeRegistry.get("planets") is first:
        fail("KnowledgeRegistry.clear did not clear")
    KnowledgeRegistry.clear()
    try:
        KnowledgeRegistry.get("absent_dataset")
        fail("KnowledgeRegistry.get served an absent data set")
    except AttributeError:
        pass
    return {
        "classification": "access_path_fidelity",
        "access_paths": sorted(paths),
        "data_sets": list(DATASETS),
        "data_sha256": {name: hashlib.sha256((DATA_DIR / f"{name}.json").read_bytes()).hexdigest()
                        for name in DATASETS},
        "mismatches": 0,
    }


def relationship_mismatches(function, friends, neutrals, enemies) -> int:
    """Compare every ordered pair with oracle tables indexed Sun=0 ... Saturn=6."""

    mismatches = 0
    for source_index, source in enumerate(GRAHAS):
        groups = ((friends[source_index], Relationship.FRIEND), (neutrals[source_index], Relationship.NEUTRAL),
                  (enemies[source_index], Relationship.ENEMY))
        for target_index, target in enumerate(GRAHAS):
            if target_index == source_index:
                continue
            expected = [kind for members, kind in groups if target_index in members]
            if len(expected) != 1:
                fail(f"the oracle does not classify {target} relative to {source} exactly once")
            mismatches += function(source, target) != expected[0]
    return mismatches


def _oracle_tables():
    global PYJHORA_VERSION
    from jhora import const as jhora_const

    PYJHORA_VERSION = importlib.metadata.version("PyJHora")
    return jhora_const._friendly_planets, jhora_const._neutral_planets, jhora_const._enemy_planets


def gate_e_natural_relationship():
    friends, neutrals, enemies = _oracle_tables()
    mismatches = relationship_mismatches(natural_relationship, friends, neutrals, enemies)
    if mismatches:
        fail(f"natural_relationship: {mismatches} pairs differ from the oracle")
    return {"classification": "external_oracle_agreement",
            "ordered_pairs_compared": len(GRAHAS) * (len(GRAHAS) - 1), "mismatches": 0,
            "reference": f"PyJHora {PYJHORA_VERSION} jhora.const._friendly_planets, _neutral_planets, _enemy_planets"}


def _snapshots():
    for year, month, day, hour, minute, second, latitude, longitude in D1_CASES:
        birth = BirthData(year, month, day, hour, minute, second, latitude, longitude, "UTC")
        for profile in (PARASHARI_LAHIRI, KP_KRISHNAMURTI):
            yield calculate(birth, profile=profile).snapshot


def rashi_mismatches(function) -> int:
    return sum(function(snapshot) != build_chart(snapshot) for snapshot in _snapshots())


def gate_f_rashi_chart():
    mismatches = rashi_mismatches(rashi_chart)
    if mismatches:
        fail(f"rashi_chart differs from build_chart on {mismatches} snapshots")
    return {"classification": "wrapper_neutrality", "snapshots_compared": len(D1_CASES) * 2, "mismatches": 0,
            "delegate": "engine.astrology.chart_builder.build_chart"}


def gate_g_negative_controls():
    """Every comparator must reject a wrong function, or its gate above proves nothing."""

    def off_by_one_sign(longitude, ascendant):
        return dict(map_planet(longitude=longitude, ascendant=ascendant),
                    sign=_exact_sign(longitude) - 1)

    def equal_house_in_map(longitude, ascendant):
        return dict(map_planet(longitude=longitude, ascendant=ascendant),
                    house=equal_house_from_ascendant(longitude, ascendant))

    def tampered(dataset):
        value = _reference(dataset)
        value["schema_version"] = "tampered"
        return value

    def symmetrised(source, target):
        if {source, target} == {"Mercury", "Moon"}:
            return Relationship.FRIEND
        return natural_relationship(source, target)

    friends, neutrals, enemies = _oracle_tables()
    controls = {
        "equal_house: the whole-sign rule": equal_house_mismatches(whole_sign_house),
        "equal_house: one house too far": equal_house_mismatches(
            lambda longitude, ascendant: equal_house_from_ascendant(longitude, ascendant) % 12 + 1),
        "map_planet: a zero-based sign": map_planet_mismatches(off_by_one_sign),
        "map_planet: equal houses": map_planet_mismatches(equal_house_in_map),
        "to_utc: the wall clock relabelled as UTC": to_utc_mismatches(
            lambda value: value.replace(tzinfo=timezone.utc)),
        "to_utc: the aware value returned unconverted": to_utc_mismatches(lambda value: value),
        "knowledge: a tampered value": knowledge_mismatches(tampered),
        "knowledge: the wrong data set": knowledge_mismatches(lambda _dataset: _reference("planets")),
        "natural_relationship: the Mercury-Moon asymmetry removed":
            relationship_mismatches(symmetrised, friends, neutrals, enemies),
        # engine/astrology/rashi_chart.py's own recorded defect: it once returned the snapshot unchanged.
        "rashi_chart: the snapshot returned unchanged": rashi_mismatches(lambda snapshot: snapshot),
    }
    for control, rejected in controls.items():
        if not rejected:
            fail(f"negative control not rejected: {control}")
    return {"classification": "negative_control", "controls_rejected": len(controls),
            "rejections_by_control": controls}


def _synthetic_subjects():
    """One synthetic subject of each of the five kinds. No real person, place or organisation."""

    provenance = RecordProvenance(source="synthetic certifier fixture", method="constructed", schema_version="h0-v2")

    def chart(label, certainty):
        return ChartCandidate(label=label, origin=OriginMoment(local_datetime="2000-01-01T12:00:00", timezone="UTC",
                                                               timezone_source="fixture", latitude=10.0,
                                                               longitude=20.0, precision="minute"),
                              origin_certainty=certainty, provenance=provenance)

    common = {"applicable_domains": ("synthetic",), "applicable_systems": ("parashari",), "provenance": provenance,
              "data_class": DataClass.SYNTHETIC}
    two_charts = (chart("documented", OriginCertainty.DOCUMENTED), chart("reported", OriginCertainty.REPORTED))
    return [
        Person(kind=EntityKind.PERSON, shape=Shape.ORIGIN, charts=two_charts, **common),
        Organisation(kind=EntityKind.ORGANISATION, shape=Shape.ORIGIN, charts=two_charts, **common),
        GeographicEntity(kind=EntityKind.GEOGRAPHIC, shape=Shape.ORIGIN, charts=two_charts, **common),
        EventEntity(kind=EntityKind.EVENT, shape=Shape.ORIGIN, charts=two_charts, **common),
        Question(kind=EntityKind.QUESTION, shape=Shape.QUERY, charts=(chart("asked", OriginCertainty.DOCUMENTED),),
                 **common),
    ]


def gate_h_entity_foundations():
    """Structural integrity of the H0 model, the append-only store and the ENT issuer (ADR-0114 s3)."""

    import tempfile

    subjects = _synthetic_subjects()
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "entities.sqlite"
        store = EntityStore(path)
        issued = [store.persist(subject) for subject in subjects]
        if [entity.number for entity in issued] != list(range(1, len(subjects) + 1)):
            fail("ENT numbers are not issued 1..n")
        if [str(entity) for entity in issued] != [str(EntityId.from_number(n)) for n in range(1, len(subjects) + 1)]:
            fail("issued identifiers do not match the family's format")
        if EntityId.from_number(len(subjects)).number != len(subjects):
            fail("an identifier's number does not round-trip")
        for entity, subject in zip(issued, subjects):
            if store.load(entity) != subject:
                fail(f"{entity} did not round-trip")
            if subject_from_record(subject_to_record(subject)) != subject:
                fail(f"{entity} record did not round-trip")
        revision = store.append_revision(issued[0], subjects[0], "certifier correction")
        history = store.history(issued[0])
        if revision != 2 or [number for number, _subject, _reason in history] != [1, 2]:
            fail("a correction did not append a revision")
        link = EntityLink(source=issued[0], relation="LEADS", target=issued[1], provenance=subjects[0].provenance)
        store.add_link(link)
        if store.links() != [link] or store.entity_ids() != issued:
            fail("links or entity listing did not round-trip")
        store.close()
        reopened = EntityStore(path)
        durable = reopened.issued_count() == len(subjects) and reopened.persist(subjects[1]).number == len(subjects) + 1
        reopened.close()
        if not durable:
            fail("the issuer is not durable across reopening")
    if rectification_permitted(subjects[0], "documented") or not rectification_permitted(subjects[0], "reported"):
        fail("a documented origin must not be rectified; a reported one may be")
    if rectification_permitted(subjects[4], "asked"):
        fail("a query moment must not be rectified")
    return {"classification": "structural_integrity", "kinds": len(subjects), "round_trips": len(subjects),
            "competing_charts_held": 2, "revisions_checked": 2, "links_checked": 1, "mismatches": 0}


def gate_i_entity_store_refusals():
    """Each refusal the WP-E1 contract requires, triggered for real (ADR-0114 s3 AC2, AC3, AC8 to AC10)."""

    import sqlite3
    import tempfile

    subjects = _synthetic_subjects()
    refused = {}
    with tempfile.TemporaryDirectory() as folder:
        store = EntityStore(Path(folder) / "entities.sqlite")
        first = store.persist(subjects[0])
        second = store.persist(subjects[1])
        store.add_link(EntityLink(source=first, relation="LEADS", target=second, provenance=subjects[0].provenance))
        for label, sql in (("update a revision", "UPDATE entity_revisions SET reason = 'x'"),
                           ("delete a revision", "DELETE FROM entity_revisions"),
                           ("update a link", "UPDATE entity_links SET payload = '{}'"),
                           ("delete a link", "DELETE FROM entity_links"),
                           ("lower the issuer", "UPDATE issuer SET last_number = 0"),
                           ("delete the issuer", "DELETE FROM issuer")):
            try:
                store._db.execute(sql)
                fail(f"the store allowed: {label}")
            except sqlite3.DatabaseError:
                refused[label] = True
        record = subject_to_record(subjects[0])
        for key in ("interpretation", "score", "weight", "confidence"):
            planted = {"schema": record["schema"], "subject": dict(record["subject"], **{key: 1})}
            try:
                subject_from_record(planted)
                fail(f"the store accepted analytical content: {key}")
            except StoreError:
                refused[f"analytical key {key}"] = True
        try:
            subject_from_record({"schema": record["schema"], "subject": dict(record["subject"], data_class="real")})
            fail("the store accepted non-synthetic data")
        except ValueError:
            refused["non-synthetic data"] = True
        try:
            store.append_revision(first, subjects[4], "a kind change")
            fail("a correction changed an entity's kind")
        except StoreError:
            refused["kind change"] = True
        # Assembled at run time and labelled descriptively, so no identifier literal enters the evidence.
        family = "ENT" + "-"
        for label, bad in (("seven digits", family + "0" * 6 + "1"), ("lower-case family", family.lower() + "0" * 7 + "1"),
                           ("number zero", family + "0" * 8)):
            try:
                EntityId(bad)
                fail(f"accepted an invalid identifier: {label}")
            except IdentifierError:
                refused[f"identifier: {label}"] = True
        before = store.issued_count()
        try:
            store.persist("not a subject")
            fail("persisted a non-subject")
        except StoreError:
            refused["non-subject"] = True
        if store.issued_count() != before:
            fail("a failed persistence consumed an ENT number")
        store.close()
    return {"classification": "negative_control", "refusals_verified": len(refused), "refused": sorted(refused)}


def main():
    tee = support.start_transcript()
    preconditions = support.preflight()
    gates = {
        "A_equal_house_closed_form": gate_a_equal_house(),
        "B_map_planet_closed_form": gate_b_map_planet(),
        "C_to_utc_reference": gate_c_to_utc(),
        "D_knowledge_access_fidelity": gate_d_knowledge_access(),
        "E_natural_relationship_oracle": gate_e_natural_relationship(),
        "F_rashi_chart_neutrality": gate_f_rashi_chart(),
        "G_negative_controls": gate_g_negative_controls(),
        "H_entity_foundations": gate_h_entity_foundations(),
        "I_entity_store_refusals": gate_i_entity_store_refusals(),
    }
    report = {
        "schema": "support_paths_v1_certification",
        "adr": "ADR-0108 s4 item 5",
        "date": str(date.today()),
        "scope": ("Support functions certified under ADR-0108 s4 item 5, each only as far as its gate's "
                  "classification: mathematical correctness of equal-house arithmetic, the planet mapper and "
                  "timezone conversion; external-oracle agreement of the naisargika relationship lookup; "
                  "access-path fidelity of the knowledge loaders, not of the data they return; "
                  "rashi_chart's neutrality over build_chart; and the structural integrity of the EVIDENCE "
                  "entity foundations (ADR-0114 WP-E1): the H0 entity model, the append-only store and the "
                  "ENT issuer."),
        "reference": {
            "equal_house_and_map_planet": "exact rational arithmetic and hand-derived literal cases",
            "to_utc": "offset subtraction and literal UTC instants",
            "knowledge_access": "the data files read independently of the code under test",
            "natural_relationship": f"PyJHora {PYJHORA_VERSION}, compared at run time",
            "rashi_chart": "build_chart, a GATED member of SIGN_CONVENTION_V1",
        },
        "gates": gates,
        "explicit_non_claims": [
            "declares no production analytical input: ADR-0099 s2's D1 and D2 are untouched",
            "certifies no dead caller: house_from_longitude, map_chart, build_all_charts, "
            "calculate_from_datetime and KnowledgeResolver.resolve stay uncertified",
            "Gate D proves that the access path returns the file. It does not prove the classical correctness "
            "of the planets, signs, houses, nakshatras or dignities data",
            "Gate F proves rashi_chart equals build_chart. It adds nothing to what is certified about D1 charts",
            "Gate C does not validate the timezone database against a second source beyond its literal cases",
            "a GATED member is not thereby in use: KnowledgeRegistry.clear is gated here and is NOT_IN_USE under C4",
            "Gates H and I certify structure only: the entity model, store and issuer make no analytical claim, and "
            "carry no score, weight or confidence; every record they use is synthetic",
            "the EVIDENCE entity foundations are not a production analytical input and are not served by any API",
            "KnowledgeLoader.load, load_json and dignities are also reached through PARASHARI_YOGA_V1, so this "
            "artifact is not their only coverage",
        ],
        "environment": {"python": sys.version.split()[0]},
        "preconditions": preconditions,
        "result": "PASS",
    }
    out = support.emit(report, "SUPPORT_PATHS_V1_certification.json", "support_paths", tee)
    print("=" * 60)
    print("SUPPORT_PATHS_V1 CERTIFICATION")
    print("=" * 60)
    for name, block in report["gates"].items():
        print(f"{name}: {block.get('mismatches', block.get('controls_rejected'))}")
    print("archived:", out.relative_to(ROOT).as_posix())
    print("RESULT  : PASS")


if __name__ == "__main__":
    main()
