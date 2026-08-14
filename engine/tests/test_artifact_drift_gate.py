"""Certification artifact drift gate, with its negative controls.

The CI step that was meant to enforce ADR-0018's "regenerated artifacts differ
in the `date` field ONLY" claim ran `git diff` with no `--exit-code`, so it
printed differences into the log and the job went green regardless. A changed
comparison count, a changed maximum error, a widened tolerance or a removed
case would all have passed. `scripts/check_artifact_drift.py` enforces the
claim; these tests prove it can fail, and that it does not fire on the fields
that are legitimately volatile.

The comparison functions are exercised directly rather than through git, so the
controls are deterministic and independent of the working tree's commit state.
"""

import copy
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import check_artifact_drift as gate  # noqa: E402

BASELINE = {
    "schema": "current_engine_certification_v1",
    "adr": "ADR-0005",
    "date": "2026-08-13",
    "tolerance_arcsec": 0.5,
    "preconditions": {"data_assets": {"assets_verified": 3}},
    "run": {
        "source_revision": "a" * 40,
        "working_tree_dirty": False,
        "executed_utc": "2026-08-13T08:00:00Z",
        "engine_version": "0.3.0",
    },
    "profiles": {
        "parashari_lahiri": {
            "cases": [
                {"id": "H1", "swetest_cmd": "<bundled>/swetest -edir<repo-root> -b1.1.2000"},
                {"id": "H2", "swetest_cmd": "<bundled>/swetest -edir<repo-root> -b2.1.2000"},
            ]
        }
    },
    "summary": {
        "total_planet_comparisons": 264,
        "max_planet_error_arcsec": 0.00017942695649253437,
        "moshier_fallback_events": 0,
        "failures": [],
        "result": "PASS",
    },
}


def _drift(mutate):
    regenerated = copy.deepcopy(BASELINE)
    mutate(regenerated)
    return gate._differences(gate._prune(BASELINE), gate._prune(regenerated))


def test_identical_artifacts_show_no_drift():
    assert _drift(lambda d: None) == []


# --------------------------------------------------------------------------
# Volatile fields must NOT trip the gate.
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "mutate, description",
    [
        (lambda d: d.__setitem__("date", "1999-01-01"), "date"),
        (lambda d: d["run"].__setitem__("executed_utc", "1999-01-01T00:00:00Z"), "run.executed_utc"),
        (lambda d: d["run"].__setitem__("source_revision", "b" * 40), "run.source_revision"),
        (lambda d: d["run"].__setitem__("working_tree_dirty", True), "run.working_tree_dirty"),
    ],
)
def test_volatile_fields_are_ignored(mutate, description):
    assert _drift(mutate) == [], f"{description} should be permitted to differ"


def test_the_volatile_list_is_exactly_what_is_documented():
    """A silently widened volatile list would gut this gate."""

    assert gate.VOLATILE == (
        "date",
        "run.executed_utc",
        "run.source_revision",
        "run.working_tree_dirty",
    )


# --------------------------------------------------------------------------
# Negative controls. Every one of these MUST be detected.
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "mutate, description",
    [
        (lambda d: d["summary"].__setitem__("max_planet_error_arcsec", 0.4), "numerical maximum raised"),
        (lambda d: d["summary"].__setitem__("max_planet_error_arcsec", 0.0), "numerical maximum lowered"),
        (lambda d: d.__setitem__("tolerance_arcsec", 5.0), "tolerance widened"),
        (lambda d: d["summary"].__setitem__("total_planet_comparisons", 1), "comparison count reduced"),
        (lambda d: d["summary"].__setitem__("result", "FAIL"), "verdict flipped"),
        (lambda d: d["summary"].__setitem__("moshier_fallback_events", 3), "fallback count changed"),
        (lambda d: d["summary"].__setitem__("failures", ["something"]), "failures appeared"),
        (lambda d: d["profiles"]["parashari_lahiri"]["cases"].pop(), "a holdout case removed"),
        (
            lambda d: d["profiles"]["parashari_lahiri"]["cases"][0].__setitem__("id", "H99"),
            "a holdout case identity changed",
        ),
        (
            lambda d: d["profiles"]["parashari_lahiri"]["cases"][0].__setitem__(
                "swetest_cmd", "/tmp/swetest_abc/swetest -edir/home/someone/ace -b1.1.2000"
            ),
            "swetest_cmd regressed to absolute paths (Q15)",
        ),
        (
            lambda d: d["preconditions"]["data_assets"].__setitem__("assets_verified", 0),
            "ephemeris verification count dropped",
        ),
        (lambda d: d.__setitem__("adr", "ADR-9999"), "decision entry reattributed"),
        (lambda d: d["run"].__setitem__("engine_version", "0.4.0"), "engine version changed"),
    ],
)
def test_negative_control_drift_is_detected(mutate, description):
    found = _drift(mutate)
    assert found, f"drift NOT detected: {description}; the gate cannot fail"


def test_added_and_removed_keys_are_detected():
    assert _drift(lambda d: d.__setitem__("something_new", 1))
    assert _drift(lambda d: d.pop("tolerance_arcsec"))


def test_prune_does_not_mutate_its_input():
    before = copy.deepcopy(BASELINE)
    gate._prune(BASELINE)
    assert BASELINE == before


def test_swetest_cmd_is_not_volatile():
    """Q15 made it deterministic precisely so it could be held to this gate."""

    assert not any(entry.endswith("swetest_cmd") for entry in gate.VOLATILE)


# --------------------------------------------------------------------------
# Rendered evidence: reports and console transcripts (added after an audit
# found `reports/certification/` was diffed by CI and enforced by nothing).
# --------------------------------------------------------------------------

REPORT = """\
# certification - HUMAN-READABLE REPORT

- Decision entry: ADR-0005
- Date: 2026-08-13
- Result: **PASS**

## Run metadata

- source_revision: aaaa
- working_tree_dirty: False
- executed_utc: 2026-08-13T08:00:00Z
- engine_version: 0.3.0

## Summary

- **max_planet_error_arcsec**: 0.00017942695649253437
- **result**: PASS
"""


def _text_drift(mutate):
    return gate._normalise_text(REPORT) != gate._normalise_text(mutate(REPORT))


@pytest.mark.parametrize(
    "replacement, description",
    [
        (("- Date: 2026-08-13", "- Date: 1999-01-01"), "date line"),
        (("- source_revision: aaaa", "- source_revision: bbbb"), "source revision line"),
        (("- working_tree_dirty: False", "- working_tree_dirty: True"), "dirty flag line"),
        (
            ("- executed_utc: 2026-08-13T08:00:00Z", "- executed_utc: 1999-01-01T00:00:00Z"),
            "timestamp line",
        ),
    ],
)
def test_volatile_report_lines_are_ignored(replacement, description):
    old, new = replacement
    assert not _text_drift(lambda t: t.replace(old, new)), f"{description} should be volatile"


@pytest.mark.parametrize(
    "replacement, description",
    [
        (("- **result**: PASS", "- **result**: FAIL"), "verdict flipped"),
        (("- Result: **PASS**", "- Result: **FAIL**"), "headline verdict flipped"),
        (
            ("0.00017942695649253437", "0.4"),
            "numerical maximum altered",
        ),
        (("- Decision entry: ADR-0005", "- Decision entry: ADR-9999"), "entry reattributed"),
        (("- engine_version: 0.3.0", "- engine_version: 0.4.0"), "engine version changed"),
    ],
)
def test_negative_control_report_drift_is_detected(replacement, description):
    old, new = replacement
    assert _text_drift(lambda t: t.replace(old, new)), (
        f"report drift NOT detected: {description}; the gate cannot fail on rendered evidence"
    )


def test_negative_control_a_removed_report_line_is_detected():
    assert _text_drift(lambda t: t.replace("- **result**: PASS\n", ""))


def test_the_volatile_line_prefixes_are_exactly_what_is_documented():
    assert gate.VOLATILE_LINE_PREFIXES == (
        "- Date:",
        "- source_revision:",
        "- working_tree_dirty:",
        "- executed_utc:",
    )


def test_rendered_evidence_is_actually_in_scope():
    """The audit finding: reports were diffed by CI and enforced by nothing."""

    tracked = gate.tracked_evidence()
    assert any(name.endswith(".report.md") for name in tracked), "no report in scope"
    assert any(name.endswith(".console.txt") for name in tracked), "no transcript in scope"
    assert any(name.endswith(".json") for name in tracked), "no artifact in scope"
    assert len(tracked) >= 30, f"only {len(tracked)} evidence files discovered"
