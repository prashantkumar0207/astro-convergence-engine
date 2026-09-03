"""Scope of the retired-identifier gate's supersession exemption (ADR-0014).

ADR-0014 D2 authorises supersession traceability in exactly three syntactic
positions, and its D1 fixes a replacement map division by division. The gate's
exemption regex originally accepted `[^"]+` and `\\S+` for the value, which meant
ANY token passed in the authorised position: an invented identifier family, or a
retired identifier belonging to a different division. That is the same defect
class ADR-0004 retired, surviving inside the gate written to prevent it.

These tests pin the corrected scope.

NOT ONE RETIRED IDENTIFIER IS WRITTEN AS A LITERAL IN THIS FILE. Every one is
assembled at run time from `gate.RETIRED`, the single source of truth. The first
version of this module spelled them out, which made it a real violation inside a
tracked file, turned the identifier gate and the whole default gate red, and was
caught only after it was committed. `.github/workflows/ci.yml` had already
recorded that exact lesson for its own probe; the lesson was applied to the YAML
and not to this file. It is applied here now.
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import check_retired_identifiers as gate  # noqa: E402

D3_FILE = "scripts/certify_d3.py"
D12_FILE = "certification/VARGA_D12_V1_certification.json"
UNSCOPED_FILE = "scripts/certify_current_engine.py"
UNMAPPED_FILE = "scripts/certify_d9.py"


def retired_for(division: int) -> str:
    """The retired varga identifier for a division, from the gate's own table."""

    return gate._VARGA_BY_DIVISION[division]


def retired_named(fragment: str) -> str:
    """The one retired identifier containing `fragment`, from `gate.RETIRED`."""

    matches = [name for name in gate.RETIRED if fragment in name]
    assert len(matches) == 1, f"{fragment} matched {matches}"
    return matches[0]


def invented() -> str:
    """An identifier of a family that has never existed, assembled at run time."""

    return "ADR-" + "NEVER" + "-ISSUED-777"


def _prose(identifier: str) -> str:
    return f"- Supersedes provisional identifier: {identifier}"


def _json(identifier: str) -> str:
    return f'  "supersedes_provisional_id": "{identifier}",'


RENDERERS = [_prose, _json]


def test_this_module_contains_no_retired_identifier_literal():
    """The defect this file was rewritten to remove. Self-enforcing."""

    text = Path(__file__).read_text()
    for name in gate.RETIRED:
        assert name not in text, (
            f"{name} is spelled out in this test module, which makes it a real "
            "violation in a tracked file and turns the gate red on itself"
        )


def test_the_division_map_is_derived_from_the_retired_list():
    assert sorted(gate._VARGA_BY_DIVISION) == [2, 3, 7, 12, 30]
    for identifier in gate._VARGA_BY_DIVISION.values():
        assert identifier in gate.RETIRED


@pytest.mark.parametrize(
    "path, division",
    [
        ("scripts/certify_d3.py", 3),
        ("scripts/certify_d30.py", 30),
        ("certification/VARGA_D7_V1_certification.json", 7),
        ("engine/tests/test_varga_d12_certification.py", 12),
        ("reports/certification/varga_d2.report.md", 2),
    ],
)
def test_division_is_read_off_the_path(path, division):
    assert gate.authorised_supersession(path) == retired_for(division)


@pytest.mark.parametrize("path", ["scripts/certify_current_engine.py", "docs/DECISION_LOG.md"])
def test_a_path_with_no_division_token_is_unscoped(path):
    assert gate.authorised_supersession(path) is gate.ANY_RETIRED


def test_a_path_with_an_UNMAPPED_division_authorises_nothing():
    """D9 and D10 are certified vargas with no provisional identifier.

    The first form of this fix returned the same permissive sentinel for "no
    division in the path" and "division present but not in the map", so a D9 or
    D10 file could have claimed to supersede any retired identifier at all.
    Fail closed instead.
    """

    assert gate.authorised_supersession("scripts/certify_d9.py") is gate.NOTHING_AUTHORISED
    assert gate.authorised_supersession("certification/VARGA_D10_V1.json") is gate.NOTHING_AUTHORISED


# --------------------------------------------------------------------------
# The authorised case must still pass, or the gate is unusable.
# --------------------------------------------------------------------------


@pytest.mark.parametrize("render", RENDERERS)
def test_the_correct_identifier_in_the_authorised_position_is_exempt(render):
    identifier = retired_for(3)
    assert identifier not in gate.scrub_supersession(D3_FILE, render(identifier))


@pytest.mark.parametrize("render", RENDERERS)
def test_an_unscoped_file_may_claim_any_retired_identifier(render):
    identifier = retired_named("KP")
    assert identifier not in gate.scrub_supersession(UNSCOPED_FILE, render(identifier))


# --------------------------------------------------------------------------
# Negative controls.
# --------------------------------------------------------------------------


@pytest.mark.parametrize("render", RENDERERS)
@pytest.mark.parametrize("division", [12, 30, 2])
def test_negative_control_wrong_division_is_not_exempt(render, division):
    identifier = retired_for(division)
    assert identifier in gate.scrub_supersession(D3_FILE, render(identifier))


@pytest.mark.parametrize("render", RENDERERS)
@pytest.mark.parametrize("fragment", ["KP", "DASHA", "TRANSIT"])
def test_negative_control_wrong_layer_is_not_exempt(render, fragment):
    identifier = retired_named(fragment)
    assert identifier in gate.scrub_supersession(D3_FILE, render(identifier))


@pytest.mark.parametrize("render", RENDERERS)
def test_negative_control_an_invented_family_is_not_exempt(render):
    token = invented()
    assert token in gate.scrub_supersession(D3_FILE, render(token))
    assert token in gate.scrub_supersession(UNSCOPED_FILE, render(token))


@pytest.mark.parametrize("render", RENDERERS)
def test_negative_control_an_unmapped_division_exempts_nothing(render):
    identifier = retired_for(30)
    assert identifier in gate.scrub_supersession(UNMAPPED_FILE, render(identifier))


def test_negative_control_a_retired_identifier_outside_the_position_is_not_exempt():
    identifier = retired_for(3)
    assert identifier in gate.scrub_supersession(D3_FILE, f"# see {identifier} for background")


@pytest.mark.parametrize(
    "prefix",
    ["xyz", "not_a_", "fake"],
)
def test_negative_control_the_key_must_stand_alone(prefix):
    """`xyzsupersedes_provisional_id` must not inherit the exemption."""

    identifier = retired_for(3)
    line = f'  "{prefix}supersedes_provisional_id": "{identifier}",'
    assert identifier in gate.scrub_supersession(D3_FILE, line), (
        "a look-alike key inherited the supersession exemption"
    )


# --------------------------------------------------------------------------
# The repository as it stands.
# --------------------------------------------------------------------------


def test_the_real_tree_still_passes_both_patterns():
    a_hits, b_hits = gate.scan()
    assert a_hits == [], a_hits
    assert b_hits == [], b_hits


def test_every_real_supersession_claim_matches_its_own_division():
    import json

    checked = 0
    for artifact in sorted((ROOT / "certification").glob("VARGA_D*_V1_certification.json")):
        data = json.loads(artifact.read_text())
        claimed = data.get("supersedes_provisional_id")
        expected = gate.authorised_supersession(f"certification/{artifact.name}")
        assert claimed == expected, (
            f"{artifact.name} claims {claimed}, but its division authorises {expected}"
        )
        checked += 1
    assert checked == 8, f"expected 8 varga artifacts, checked {checked}"
