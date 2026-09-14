"""Q22 / H-7a: non-circular coverage of load-bearing certification values.

THE DEFECT THIS CLOSES. `test_certification_evidence_agreement.py` asserts
`_render(artifact) == stored_report`. That is `f(x) == stored f(x)`: it catches
a hand-edited report or a regenerated artifact, but it cannot catch any defect
INSIDE `_render`, because both sides of the comparison come from the same
function. Measured at `a62a2c8`, `_render` carries 44.9% of artifact leaf
values overall - 17.0% for Tier-0, 11.5% for `TRANSIT_V1` - so most of what an
artifact claims is defended by that circular comparison alone.

WHAT THIS GATE DOES INSTEAD. It reads the report TEXT and the artifact JSON
directly and asserts that every declared load-bearing value appears verbatim in
the report. `_render` is never called here, never imported here, and is never
modified by M1 (CEO execution control 11). A renderer that drops a field,
mislabels one, or truncates a float fails this gate and passes the old one.

THE DECLARATION IS INDEPENDENT OF THE RENDERER (CEO execution control 9). The
keys below are written from what a certification CLAIM consists of - the
verdict, the count of evidence, the extremal measure, the tolerance judged
against, the identity pin, the oracle's identity - not from inspecting what
`_render` happens to emit. `test_declaration_never_consults_the_renderer`
enforces that by reading this file's own source.
"""

import json
import pathlib
import re
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
CERTIFICATION = ROOT / "certification"
REPORTS = ROOT / "reports" / "certification"

# --------------------------------------------------------------- declaration

#: Exact key names whose value IS the claim.
LOAD_BEARING_KEYS = frozenset({
    "result",            # the verdict
    "adr",               # the decision entry the claim rests on
    "mismatches",        # disagreements found
    "comparisons",       # evidence volume
    "points",
    "cases",
    "anchors",
    "oracle_executed",   # whether an external oracle actually ran
    "package",           # which oracle
    "version",           # which version of it
    "modules_scanned",   # anti-fitting scan breadth
})

#: Key suffixes whose value is load-bearing whatever the surrounding block.
LOAD_BEARING_SUFFIXES = ("_sha256", "_error_arcsec", "_events")

#: Key prefixes, likewise.
LOAD_BEARING_PREFIXES = ("tolerance", "max_")

#: DECLARED SUPPORTING DETAIL, not load-bearing. Per-case values inside a list
#: (`profiles.*.cases[7].max_planet_error_arcsec`, the per-case dasha deltas)
#: support the aggregate rather than constituting the claim: the certification
#: asserts the AGGREGATE maximum and the AGGREGATE mismatch count, and those
#: aggregates are load-bearing and are checked. Stated as a judgement so it can
#: be disputed, not hidden as an implementation detail.
SUPPORTING_DETAIL = re.compile(r"\[\d+\]")

#: FROZEN RENDER GAPS - load-bearing values that are genuinely ABSENT from
#: their own human-readable report at `a62a2c8`. Each is a real defect in
#: `_render`'s coverage, NOT a defect in any calculation.
#:
#: They are frozen here rather than fixed because fixing them means changing
#: `_render`, which changes all 44 rendered evidence files and forces
#: regeneration across all 22 certifiers - the H-7b work the CEO placed OUT of
#: M1 scope. Freezing them means the set cannot grow silently: a new gap fails
#: `test_render_gap_set_has_not_grown`.
#:
#: The dominant pattern is that `_render` never emits the top-level `oracle`
#: block at all, so no report states WHICH external oracle or WHICH version
#: produced its comparison. This is reported to the CEO as an M1 finding.
DECLARED_RENDER_GAPS = frozenset({
    ("PANCHANGA_V1_certification.json", "oracle.package"),
    ("PANCHANGA_V1_certification.json", "oracle.version"),
    ("PARASHARI_DRISHTI_V1_certification.json", "oracle.package"),
    ("PARASHARI_DRISHTI_V1_certification.json", "oracle.version"),
    ("PARASHARI_YOGA_V1_certification.json", "rule.certifier_content_sha256"),
    ("PARASHARI_YOGA_V1_certification.json", "rule.production_content_sha256"),
    ("TRANSIT_V1_certification.json", "oracle.package"),
    ("TRANSIT_V1_certification.json", "oracle.version"),
    ("TRIKALAM_V1_certification.json", "gates.F_external_oracle.tolerance_rationale"),
    ("TRIKALAM_V1_certification.json", "oracle.package"),
    ("TRIKALAM_V1_certification.json", "oracle.version"),
    ("VARGA_D12_V1_certification.json", "oracle.package"),
    ("VARGA_D12_V1_certification.json", "oracle.version"),
    ("VARGA_D16_V1_certification.json", "gates.C_oracle.tolerance"),
    ("VARGA_D16_V1_certification.json", "oracle.tolerance"),
    ("VARGA_D20_V1_certification.json", "gates.C_oracle.tolerance"),
    ("VARGA_D20_V1_certification.json", "oracle.tolerance"),
    ("VARGA_D24_V1_certification.json", "oracle.package"),
    ("VARGA_D24_V1_certification.json", "oracle.version"),
    ("VARGA_D2_V1_certification.json", "oracle.package"),
    ("VARGA_D2_V1_certification.json", "oracle.version"),
    ("VARGA_D30_V1_certification.json", "oracle.package"),
    ("VARGA_D30_V1_certification.json", "oracle.version"),
    ("VARGA_D3_V1_certification.json", "oracle.package"),
    ("VARGA_D3_V1_certification.json", "oracle.version"),
    ("VARGA_D40_V1_certification.json", "gates.C_oracle.tolerance"),
    ("VARGA_D40_V1_certification.json", "oracle.tolerance"),
    ("VARGA_D45_V1_certification.json", "oracle.package"),
    ("VARGA_D45_V1_certification.json", "oracle.version"),
    ("VARGA_D4_V1_certification.json", "gates.C_oracle.tolerance"),
    ("VARGA_D4_V1_certification.json", "oracle.tolerance"),
    ("VARGA_D7_V1_certification.json", "oracle.package"),
    ("VARGA_D7_V1_certification.json", "oracle.version"),
    ("VIMSHOTTARI_V1_certification.json", "oracle.max_oracle_moon_delta_arcsec"),
    ("VIMSHOTTARI_V1_certification.json", "oracle.package"),
    ("VIMSHOTTARI_V1_certification.json", "oracle.version"),
    ("current_engine_certification.json", "profiles.kp_krishnamurti.max_ascendant_error_arcsec"),
    ("current_engine_certification.json", "profiles.kp_krishnamurti.max_cusp_error_arcsec"),
    ("current_engine_certification.json", "profiles.parashari_lahiri.max_planet_error_arcsec"),
})

#: Human labels a report may legitimately use instead of the raw JSON key. A
#: human-readable report should say "Decision entry: ADR-0011", not "adr":
#: attribution is what matters, not the machine field name. Declared here by
#: hand - like every other declaration in this file, it is written from what a
#: report OUGHT to say and is never derived from what `_render` emits.
FIELD_LABEL_ALIASES = {
    "adr": ("decision entry",),
    "modules_scanned": ("anti-fitting scan",),
    "tolerance_arcsec": ("tolerance",),
    "assets_verified": ("data assets verified",),
}

#: Guards against a discovery bug turning the whole gate into a no-op.
MINIMUM_ARTIFACTS = 20
MINIMUM_CHECKED_VALUES = 250


# ------------------------------------------------------------------ machinery

def _is_load_bearing(key: str) -> bool:
    return (
        key in LOAD_BEARING_KEYS
        or key.endswith(LOAD_BEARING_SUFFIXES)
        or key.startswith(LOAD_BEARING_PREFIXES)
    )


def _leaves(value, path=""):
    out = []
    if isinstance(value, dict):
        for key, item in value.items():
            out += _leaves(item, f"{path}.{key}" if path else key)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            out += _leaves(item, f"{path}[{index}]")
    else:
        out.append((path, value))
    return out


def load_bearing_values(artifact: dict):
    """Declared load-bearing (path, value) pairs. Never consults the renderer."""

    found = []
    for path, value in _leaves(artifact):
        if SUPPORTING_DETAIL.search(path):
            continue
        key = path.split(".")[-1]
        if not _is_load_bearing(key):
            continue
        if value is None or value == "":
            continue
        found.append((path, value))
    return found


def report_covers(report_text: str, path: str, value) -> bool:
    """Does the human-readable evidence state this value, ATTRIBUTED to its field?

    Naive substring containment is vacuous for short values: `mismatches = 0`
    is "present" in any report containing the digit 0 anywhere, including
    inside an unrelated count or a SHA-256. The renderer-mutation control
    (CEO execution control 10) caught exactly that hole in an earlier draft of
    this gate, so coverage now requires the field's own name and its value to
    appear on the SAME rendered line.

    That is still renderer-agnostic - it assumes only that a report states a
    field beside its value, not any particular formatting - and it is still
    non-circular, because the line is read from the stored report rather than
    produced by `_render`.
    """

    key = path.split(".")[-1]
    labels = [key.lower()] + [alias.lower() for alias in FIELD_LABEL_ALIASES.get(key, ())]
    needle = str(value)
    return any(
        needle in line and any(label in line.lower() for label in labels)
        for line in report_text.splitlines()
    )


def _pairs():
    found = []
    for artifact_path in sorted(CERTIFICATION.glob("*.json")):
        try:
            data = json.loads(artifact_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:  # pragma: no cover
            continue
        if not isinstance(data, dict) or not data.get("_slug"):
            continue
        report = REPORTS / f"{data['_slug']}.report.md"
        if not report.exists():  # pragma: no cover - the agreement gate owns this
            continue
        found.append((artifact_path.name, data, report.read_text(encoding="utf-8")))
    return found


def _actual_gaps():
    gaps = set()
    for name, data, text in _pairs():
        for path, value in load_bearing_values(data):
            if not report_covers(text, path, value):
                gaps.add((name, path))
    return gaps


# ---------------------------------------------------------------------- gates

def test_discovery_is_not_a_no_op():
    pairs = _pairs()
    assert len(pairs) >= MINIMUM_ARTIFACTS, (
        f"only {len(pairs)} artifact/report pairs discovered; discovery is broken"
    )
    total = sum(len(load_bearing_values(data)) for _, data, _ in pairs)
    assert total >= MINIMUM_CHECKED_VALUES, (
        f"only {total} load-bearing values declared across {len(pairs)} artifacts; "
        f"the declaration has collapsed and this gate would prove nothing"
    )


def test_every_load_bearing_value_is_stated_in_its_report():
    """The gate proper. Non-circular: `_render` is never called."""

    unexpected = []
    for name, data, text in _pairs():
        for path, value in load_bearing_values(data):
            if (name, path) in DECLARED_RENDER_GAPS:
                continue
            if not report_covers(text, path, value):
                unexpected.append(f"{name}:{path} = {str(value)[:60]}")
    assert not unexpected, (
        "load-bearing values absent from their human-readable report and not "
        "declared as a known render gap:\n  " + "\n  ".join(unexpected)
    )


def test_render_gap_set_has_not_grown():
    """The frozen gap list must match reality exactly, in both directions.

    Grown: a new load-bearing value stopped being rendered - a regression.
    Shrunk: a gap was closed, which means `_render` changed, which M1 forbids;
    the list must then be updated deliberately rather than drifting.
    """

    actual = _actual_gaps()
    newly_missing = sorted(actual - DECLARED_RENDER_GAPS)
    now_covered = sorted(DECLARED_RENDER_GAPS - actual)
    assert not newly_missing, f"NEW render gaps appeared: {newly_missing}"
    assert not now_covered, (
        f"declared render gaps are now covered: {now_covered}. If `_render` was "
        f"changed deliberately, update DECLARED_RENDER_GAPS in the same commit."
    )


def test_declaration_never_consults_the_renderer():
    """CEO execution control 9, enforced against this file's own source.

    The required-field set must be declared, not derived from `_render`.
    """

    import ast

    tree = ast.parse(pathlib.Path(__file__).read_text(encoding="utf-8"))

    # Prose may DISCUSS the renderer - this file's own docstring does, at
    # length. What must not exist is executable code that reaches it, so the
    # check walks the AST rather than grepping the text.
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
        elif isinstance(node, ast.Name):
            assert node.id != "_render", "this gate calls `_render`; independence lost"
        elif isinstance(node, ast.Attribute):
            assert node.attr != "_render", "this gate calls `_render`; independence lost"

    assert "certification_support" not in imported, (
        "this gate imports the module that produced the reports; the comparison "
        "would no longer be independent"
    )


# ----------------------------------------------------------- negative controls

@pytest.mark.parametrize(
    "damage, description",
    [
        (lambda t: t.replace("mismatches=0", "mismatches="), "value deleted from the report"),
        (lambda t: t.replace("**PASS**", "**FAIL**"), "verdict altered in the report"),
        (lambda t: re.sub(r"points=51429", "points=5142", t), "count truncated in the report"),
    ],
)
def test_negative_control_damaged_report_is_detected(damage, description):
    """The gate must FAIL when a report stops stating a load-bearing value.

    Operates on an in-memory copy of a real report. Nothing on disk is written,
    and the following test asserts that.
    """

    name = "VARGA_D2_V1_certification.json"
    data = json.loads((CERTIFICATION / name).read_text(encoding="utf-8"))
    text = (REPORTS / f"{data['_slug']}.report.md").read_text(encoding="utf-8")
    damaged = damage(text)
    assert damaged != text, f"control is inert: {description} changed nothing"

    still_covered = all(
        report_covers(damaged, path, value) for path, value in load_bearing_values(data)
    )
    assert not still_covered, (
        f"negative control FAILED: {description} left every load-bearing value "
        f"still findable, so this gate's PASS would mean nothing"
    )


def test_negative_controls_left_the_evidence_clean():
    for name, data, text in _pairs():
        assert text, f"{name}'s report vanished during the controls"
    assert not _actual_gaps() - DECLARED_RENDER_GAPS
