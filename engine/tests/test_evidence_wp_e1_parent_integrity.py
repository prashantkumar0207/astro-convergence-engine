"""WP-E1 HOLD correction (H0 s4; ADR-0114 AC5): shape B integrity.

Two defects these tests reproduce against the original WP-E1 code:
1. A derived (shape B) subject could carry zero charts.
2. The store accepted a parent link to an entity, or to a chart, that it does not hold, and a
   correction to a parent could silently remove the chart a child's link names.

Every record here is synthetic.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from engine.evidence.entity import (  # noqa: E402
    ChartCandidate, DataClass, EntityKind, EntityModelError, OriginCertainty, OriginMoment, ParentLink, Person,
    RecordProvenance, Shape,
)
from engine.evidence.identifiers import EntityId  # noqa: E402
from engine.evidence.store import EntityStore, StoreError  # noqa: E402

PROV = RecordProvenance(source="synthetic fixture", method="hand-written test data", schema_version="h0-v2")


def chart(label):
    return ChartCandidate(label=label, origin=OriginMoment(local_datetime="2000-01-01T12:00:00", timezone="UTC",
                                                           timezone_source="fixture", latitude=10.0, longitude=20.0,
                                                           precision="minute"),
                          origin_certainty=OriginCertainty.REPORTED, provenance=PROV)


def origin_subject(*labels):
    return Person(kind=EntityKind.PERSON, shape=Shape.ORIGIN, charts=tuple(chart(label) for label in labels),
                  applicable_domains=("jataka",), applicable_systems=("parashari",), provenance=PROV,
                  data_class=DataClass.SYNTHETIC)


def derived_subject(parent, parent_chart, charts=("varshaphal",)):
    return Person(kind=EntityKind.PERSON, shape=Shape.DERIVED, charts=tuple(chart(label) for label in charts),
                  applicable_domains=("varshaphal",), applicable_systems=("tajika",), provenance=PROV,
                  data_class=DataClass.SYNTHETIC,
                  parent=ParentLink(parent=parent, parent_chart=parent_chart, derivation="annual chart 2026"))


@pytest.fixture()
def store(tmp_path):
    with EntityStore(tmp_path / "entities.sqlite") as instance:
        yield instance


def test_a_derived_subject_needs_at_least_one_chart():
    with pytest.raises(EntityModelError):
        derived_subject(EntityId.from_number(1), "natal", charts=())


def test_a_valid_parent_link_persists_and_round_trips(store):
    parent = store.persist(origin_subject("natal"))
    child = derived_subject(parent, "natal")
    assert store.load(store.persist(child)) == child


def test_a_dangling_parent_entity_is_refused_and_takes_no_number(store):
    store.persist(origin_subject("natal"))
    before = store.issued_count()
    with pytest.raises(StoreError, match="parent"):
        store.persist(derived_subject(EntityId.from_number(99), "natal"))
    assert store.issued_count() == before


def test_a_dangling_parent_chart_is_refused_and_takes_no_number(store):
    parent = store.persist(origin_subject("natal"))
    before = store.issued_count()
    with pytest.raises(StoreError, match="chart"):
        store.persist(derived_subject(parent, "no-such-chart"))
    assert store.issued_count() == before


def test_a_correction_cannot_introduce_a_dangling_parent(store):
    parent = store.persist(origin_subject("natal"))
    child = store.persist(derived_subject(parent, "natal"))
    with pytest.raises(StoreError):
        store.append_revision(child, derived_subject(parent, "no-such-chart"), "planted bad correction")
    with pytest.raises(StoreError):
        store.append_revision(child, derived_subject(EntityId.from_number(99), "natal"), "planted bad correction")
    assert len(store.history(child)) == 1


def test_a_subject_cannot_derive_from_itself(store):
    first = store.persist(origin_subject("natal"))
    with pytest.raises(StoreError, match="itself"):
        store.append_revision(first, derived_subject(first, "natal"), "planted self-derivation")


def test_a_longer_derivation_cycle_is_refused(store):
    root = store.persist(origin_subject("natal"))
    middle = store.persist(derived_subject(root, "natal", charts=("annual",)))
    with pytest.raises(StoreError, match="itself"):
        store.append_revision(root, derived_subject(middle, "annual", charts=("natal",)), "planted cycle")


def test_a_parent_correction_cannot_silently_invalidate_a_child_link(store):
    parent = store.persist(origin_subject("natal", "rectified"))
    store.persist(derived_subject(parent, "natal"))
    with pytest.raises(StoreError, match="natal"):
        store.append_revision(parent, origin_subject("rectified"), "planted removal of a referenced chart")
    assert len(store.history(parent)) == 1
    # Keeping the referenced chart is a valid correction.
    assert store.append_revision(parent, origin_subject("natal", "rectified", "third"), "added a candidate") == 2
