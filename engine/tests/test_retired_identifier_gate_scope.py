"""Scope of the retired-identifier gate's supersession exemption (ADR-0014).

ADR-0014 D2 authorises supersession traceability in exactly three syntactic
positions, and its D1 fixes a replacement map division by division. The gate's
exemption regex originally accepted `[^"]+` and `\\S+` for the value, which meant
ANY token passed in the authorised position: an invented identifier family, or a
retired identifier belonging to a different division. That is the same defect
class ADR-0004 retired, surviving inside the gate written to prevent it.

These tests pin the corrected scope. They exercise the gate's own functions, so
they run in the default gate rather than only as a manual demonstration.
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import check_retired_identifiers as gate  # noqa: E402

D3 = "scripts/certify_d3.py"
D12 = "certification/VARGA_D12_V1_certification.json"
UNSCOPED = "scripts/certify_current_engine.py"


def _prose(identifier: str) -> str:
    return f"- Supersedes provisional identifier: {identifier}"


def _json(identifier: str) -> str:
    return f'  "supersedes_provisional_id": "{identifier}",'


def test_the_division_map_is_derived_from_the_retired_list():
    """One source of truth. A hand-written second copy would drift."""

    assert gate._VARGA_BY_DIVISION == {
        2: "ADR-VARGA-D2-001",
        3: "ADR-VARGA-D3-001",
        7: "ADR-VARGA-D7-001",
        12: "ADR-VARGA-D12-001",
        30: "ADR-VARGA-D30-001",
    }
    for identifier in gate._VARGA_BY_DIVISION.values():
        assert identifier in gate.RETIRED


@pytest.mark.parametrize(
    "path, expected",
    [
        ("scripts/certify_d3.py", "ADR-VARGA-D3-001"),
        ("scripts/certify_d30.py", "ADR-VARGA-D30-001"),
        ("certification/VARGA_D7_V1_certification.json", "ADR-VARGA-D7-001"),
        ("engine/tests/test_varga_d12_certification.py", "ADR-VARGA-D12-001"),
        ("reports/certification/varga_d2.report.md", "ADR-VARGA-D2-001"),
        ("scripts/certify_current_engine.py", None),
        ("docs/DECISION_LOG.md", None),
    ],
)
def test_division_is_read_off_the_path(path, expected):
    assert gate.authorised_supersession(path) == expected


# --------------------------------------------------------------------------
# The authorised case must still pass, or the gate is unusable.
# --------------------------------------------------------------------------


@pytest.mark.parametrize("render", [_prose, _json])
def test_the_correct_identifier_in_the_authorised_position_is_exempt(render):
    line = render("ADR-VARGA-D3-001")
    assert gate.scrub_supersession(D3, line).strip().strip(",") in ("", '"',)
    assert "ADR-VARGA-D3-001" not in gate.scrub_supersession(D3, line)


@pytest.mark.parametrize("render", [_prose, _json])
def test_an_unscoped_file_may_claim_any_retired_identifier(render):
    """Pre-existing behaviour, preserved deliberately and reported as such."""

    line = render("ADR-KP-001")
    assert "ADR-KP-001" not in gate.scrub_supersession(UNSCOPED, line)


# --------------------------------------------------------------------------
# Negative controls: the hole the audit found must stay closed.
# --------------------------------------------------------------------------


@pytest.mark.parametrize("render", [_prose, _json])
@pytest.mark.parametrize(
    "identifier, description",
    [
        ("ADR-VARGA-D12-001", "wrong division: D12 claimed in a D3 file"),
        ("ADR-KP-001", "wrong layer: KP claimed in a D3 file"),
        ("ADR-DASHA-001", "wrong layer: dasha claimed in a D3 file"),
    ],
)
def test_negative_control_wrong_identifier_for_the_division_is_not_exempt(
    render, identifier, description
):
    line = render(identifier)
    scrubbed = gate.scrub_supersession(D3, line)
    assert identifier in scrubbed, f"{description} was wrongly exempted"


@pytest.mark.parametrize("render", [_prose, _json])
def test_negative_control_an_invented_family_is_not_exempt(render):
    invented = "ADR-" + "MADE" + "-UP-777"
    line = render(invented)
    assert invented in gate.scrub_supersession(D3, line), (
        "an invented identifier family was exempted in the authorised position"
    )
    assert invented in gate.scrub_supersession(UNSCOPED, line), (
        "an invented identifier family was exempted in an unscoped file"
    )


def test_negative_control_a_retired_identifier_outside_the_position_is_not_exempt():
    line = "# see ADR-VARGA-D3-001 for background"
    assert "ADR-VARGA-D3-001" in gate.scrub_supersession(D3, line)


def test_the_real_tree_still_passes_both_patterns():
    a_hits, b_hits = gate.scan()
    assert a_hits == [], a_hits
    assert b_hits == [], b_hits


def test_every_real_supersession_claim_matches_its_own_division():
    """The corrected rule, applied to the repository as it stands."""

    import json

    for artifact in sorted((ROOT / "certification").glob("VARGA_D*_V1_certification.json")):
        data = json.loads(artifact.read_text())
        claimed = data.get("supersedes_provisional_id")
        expected = gate.authorised_supersession(f"certification/{artifact.name}")
        assert claimed == expected, (
            f"{artifact.name} claims {claimed}, but its division authorises {expected}"
        )
