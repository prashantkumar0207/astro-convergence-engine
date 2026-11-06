"""M-05 (G1 audit; ADR-0111): transit events and views carry complete provenance.

The defect: TransitEvent carried a bare profile_name, and TransitView validated the natal
provenance and then dropped it. These tests require each event's provenance to equal what a real
snapshot under the same profile carries, and require the view to keep the natal provenance. They
also check that the comparisons reject an event or view whose provenance is wrong.
"""

from __future__ import annotations

import dataclasses
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from engine.astronomy.profile import KP_KRISHNAMURTI, PARASHARI_LAHIRI  # noqa: E402
from engine.calculations.calculations import calculate  # noqa: E402
from engine.models.birth_data import BirthData  # noqa: E402
from engine.models.transit_event import TransitEvent  # noqa: E402
from engine.transits.crossing import find_crossings  # noqa: E402
from engine.transits.events import natal_conjunctions, returns, sign_ingresses  # noqa: E402
from engine.transits.view import TransitView, transit_view  # noqa: E402

BIRTH = BirthData(1990, 1, 15, 6, 0, 0.0, 25.6, 85.1333, "Asia/Kolkata")
JD_START, JD_END = 2451545.0, 2451545.0 + 40.0
PROFILES = (PARASHARI_LAHIRI, KP_KRISHNAMURTI)


def snapshot_provenance(profile):
    """The provenance a real snapshot under ``profile`` carries: the independent reference."""

    return calculate(BIRTH, profile=profile).snapshot.provenance


def event_provenance_is_complete(event: TransitEvent, profile) -> bool:
    return (event.provenance is not None and event.provenance == snapshot_provenance(profile)
            and event.provenance.profile_name == event.profile_name)


def view_provenance_is_complete(view: TransitView, natal_snapshot, profile) -> bool:
    return (view.natal_provenance is not None and view.natal_provenance == natal_snapshot.provenance
            and view.provenance == snapshot_provenance(profile))


def _events(profile):
    natal = calculate(BIRTH, profile=profile).snapshot
    moon = natal.sidereal_planets["Moon"].longitude
    found = list(find_crossings("Moon", 123.4, JD_START, JD_END, profile))
    found += sign_ingresses("Moon", JD_START, JD_END, profile)
    found += returns("Moon", moon, JD_START, JD_END, profile)
    # natal_conjunctions returns (label, event) pairs.
    found += [event for _label, event in natal_conjunctions(
        "Sun", {"Ascendant": natal.houses.ascendant}, JD_START, JD_START + 400, profile)]
    return found


@pytest.mark.parametrize("profile", PROFILES, ids=lambda p: p.name)
def test_every_event_carries_its_profiles_full_provenance(profile):
    events = _events(profile)
    assert len(events) > 5 and {event.kind for event in events} >= {"crossing", "sign_ingress", "return"}
    assert all(event_provenance_is_complete(event, profile) for event in events)


@pytest.mark.parametrize("profile", PROFILES, ids=lambda p: p.name)
def test_the_view_keeps_the_natal_provenance_it_validates(profile):
    natal = calculate(BIRTH, profile=profile).snapshot
    view = transit_view(natal, JD_START, 25.6, 85.1333, profile)
    assert view_provenance_is_complete(view, natal, profile)


def test_the_provenance_field_is_required_on_events():
    """Complete by construction: an event cannot be built without it."""

    with pytest.raises(TypeError):
        TransitEvent(body="Moon", target_longitude=0.0, julian_day=JD_START, direction=1,
                     residual_arcsec=0.0, kind="crossing", profile_name=PARASHARI_LAHIRI.name)


def test_the_event_check_rejects_wrong_provenance():
    event = _events(PARASHARI_LAHIRI)[0]
    assert event_provenance_is_complete(event, PARASHARI_LAHIRI)
    foreign = dataclasses.replace(event, provenance=snapshot_provenance(KP_KRISHNAMURTI))
    assert not event_provenance_is_complete(foreign, PARASHARI_LAHIRI)
    assert not event_provenance_is_complete(dataclasses.replace(event, provenance=None), PARASHARI_LAHIRI)
    relabelled = dataclasses.replace(event, profile_name=KP_KRISHNAMURTI.name)
    assert not event_provenance_is_complete(relabelled, PARASHARI_LAHIRI)


def test_the_view_check_rejects_a_foreign_or_missing_natal_provenance():
    natal = calculate(BIRTH, profile=PARASHARI_LAHIRI).snapshot
    view = transit_view(natal, JD_START, 25.6, 85.1333, PARASHARI_LAHIRI)
    other = calculate(BIRTH, profile=KP_KRISHNAMURTI).snapshot
    assert not view_provenance_is_complete(dataclasses.replace(view, natal_provenance=other.provenance), natal,
                                           PARASHARI_LAHIRI)
    assert not view_provenance_is_complete(dataclasses.replace(view, natal_provenance=None), natal, PARASHARI_LAHIRI)


def test_the_three_transit_overclaims_stay_open():
    backlog = json.loads((ROOT / "docs" / "CERTIFICATION_REMEDIATION_BACKLOG.json").read_text(encoding="utf-8"))
    entries = {entry["id"]: entry for entry in backlog["entries"]}
    for name in ("OVERCLAIM-TRANSIT-RETURNS", "OVERCLAIM-TRANSIT-NATAL-CONJUNCTIONS", "OVERCLAIM-TRANSIT-NATAL-VIEW"):
        assert entries[name]["status"] == "OPEN" and entries[name]["disposition"] == "OPEN_SCOPE_OVERCLAIM"
