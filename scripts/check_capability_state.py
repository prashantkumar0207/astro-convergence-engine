"""Capability-state consistency gate (ADR-0093; designed by the 2026-09-05 reconciliation audit).

The defect this gate exists to catch
------------------------------------
`docs/ENGINE_STATUS.md` declares itself "CURRENT - regenerate on every certified
change". On 2026-09-05 it was found to be four weeks stale and, worse,
affirmatively FALSE in two places: it denied yogas while `PARASHARI_YOGA_V1` held
a PASS artifact, and denied KP significators while `KP_SIGNIFICATOR_V1` held one.
`docs/VARGA_CERTIFICATION_ROADMAP.md` listed D24, D40 and D45 as "not certified
and not implemented" while all three were production-registered.

No gate could detect any of it. `check_artifact_drift.py` compares each evidence
file to ITS OWN COMMITTED VERSION, so a file that is never regenerated passes
forever; its PASS means "unchanged", never "true". That is the same lesson as
audit finding B-03 (stored artifacts are history, not proof) and DP-032's own
Finding 2 (a value that is reported but never enforced is not enforcement).

So this gate compares documented claims against LIVE state, computed now:

  * `engine.astrology.CERTIFIED_PRODUCTION_VARGAS` - registry membership. ADR-0010
    ratified this constant as "the single source of truth for sanctioned registry
    state", so the gate takes it as authority rather than inventing one.
  * the runner-regenerated `certification/*.json` `result` fields - certification
    evidence.
  * `certification_support.CERTIFIER_SOURCES` / `VALIDATOR_SOURCES` - the source
    registries.

What it deliberately does NOT do
--------------------------------
It parses ONLY the explicitly delimited machine-readable block in the target
document. It does no free-text interpretation of prose. Prose that mentions a
division in a historical sentence ("D45 was the first production capability") is
legitimate and must not fail a gate; a regex sweeping whole documents would fire
on it. The cost of that choice is stated honestly: **prose drift is not detected**,
only the block is. Keeping prose consistent with the block remains manual.

FROZEN historical evidence is excluded from the live sources (`FROZEN_EVIDENCE`).
`ADR-0092` classifies `certification/ENGINE_CAPABILITY_INVENTORY.json` as frozen
dated historical evidence and explicitly forbids its use as a live-state
authority. Reading it here would reintroduce exactly the 2026-08-11 snapshot the
audit found divergent in eleven capability statuses.

Exit 0 = PASS, 1 = FAIL. Accepts an optional target path so the negative controls
can run the real enforcement path against a mutated copy.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

DEFAULT_TARGET = ROOT / "docs" / "ENGINE_STATUS.md"

BEGIN = "<!-- CAPABILITY-BLOCK:BEGIN"
END = "<!-- CAPABILITY-BLOCK:END -->"

_BLOCK = re.compile(
    re.escape(BEGIN) + r"[^\n]*-->\s*```json\s*(?P<json>.*?)```\s*" + re.escape(END),
    re.DOTALL,
)

# Dated evidence, never a live source. ADR-0092 decides this for the capability
# inventory specifically; the other three share its shape (a date, a source
# commit or environment, and no runner that regenerates them).
FROZEN_EVIDENCE = frozenset({
    "ENGINE_CAPABILITY_INVENTORY.json",   # ADR-0092, DP-034 Option 2
    "ORACLE_ENVIRONMENT.json",
    "G6_REMOTE_CI_VALIDATION.json",
    "CURRENT_ENGINE_LOCK.json",
})

# A non-claim token is refutable only if we know which artifact would refute it.
# Tokens absent from this map (e.g. "horary", "numerology") are unrefutable by
# this gate and pass; that limitation is real and is stated rather than hidden.
NON_CLAIM_ARTIFACTS = {
    "yogas": "PARASHARI_YOGA_V1",
    "kp_significators": "KP_SIGNIFICATOR_V1",
    "panchanga": "PANCHANGA_V1",
    "rise_set": "RISE_SET_V1",
    "trikalam": "TRIKALAM_V1",
    "transits": "TRANSIT_V1",
    "vimshottari": "VIMSHOTTARI_V1",
    "graha_drishti": "PARASHARI_DRISHTI_V1",
    "kp_chains": "KP_CHAIN_V1",
    "planet_strength": "PLANET_STRENGTH_V1",  # no such artifact: the claim stands
}


def live_registered_divisions() -> set[int]:
    from engine.astrology import CERTIFIED_PRODUCTION_VARGAS

    return {division for division, _school in CERTIFIED_PRODUCTION_VARGAS}


def live_pass_artifacts(certification_dir: Path | None = None) -> dict[str, str]:
    """Capability stem -> result, for every artifact that is NOT frozen evidence."""

    directory = certification_dir or (ROOT / "certification")
    results: dict[str, str] = {}
    for path in sorted(directory.glob("*.json")):
        if path.name in FROZEN_EVIDENCE:
            continue
        try:
            payload = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        result = payload.get("result")
        if isinstance(result, str):
            results[path.name.replace("_certification.json", "")] = result
    return results


def live_source_counts() -> dict[str, int]:
    from scripts.certification_support import CERTIFIER_SOURCES, VALIDATOR_SOURCES

    return {
        "certifier_sources": len(CERTIFIER_SOURCES),
        "validator_sources": len(VALIDATOR_SOURCES),
    }


def extract_block(text: str) -> tuple[dict | None, list[str]]:
    match = _BLOCK.search(text)
    if match is None:
        return None, [
            "no CAPABILITY-BLOCK found. A gate that passes when the block it "
            "checks has been deleted is not a gate."
        ]
    try:
        block = json.loads(match.group("json"))
    except json.JSONDecodeError as exc:
        return None, [f"CAPABILITY-BLOCK is not valid JSON: {exc}"]
    if not isinstance(block, dict):
        return None, ["CAPABILITY-BLOCK must be a JSON object"]
    return block, []


def check(
    text: str,
    registered: set[int] | None = None,
    artifacts: dict[str, str] | None = None,
    counts: dict[str, int] | None = None,
) -> list[str]:
    """Return every failure. Empty list means PASS.

    The live sources are injectable so the committed controls can drive known
    states through the real comparison logic, rather than reimplementing it.
    """

    block, errors = extract_block(text)
    if block is None:
        return errors

    registered = live_registered_divisions() if registered is None else registered
    artifacts = live_pass_artifacts() if artifacts is None else artifacts
    counts = live_source_counts() if counts is None else counts

    passing = {name for name, result in artifacts.items() if result == "PASS"}
    claimed_production = set(block.get("production_registered_vargas", []))
    claimed_unregistered = set(block.get("certified_not_registered_vargas", []))
    claimed_not_certified = set(block.get("not_certified_vargas", []))
    claimed_capabilities = set(block.get("certified_capabilities", []))

    # F1: registered in production, missing from the document.
    for division in sorted(registered - claimed_production):
        errors.append(
            f"F1 D{division} is in CERTIFIED_PRODUCTION_VARGAS but missing from "
            f"production_registered_vargas"
        )

    # F2: claimed as registered, not actually registered.
    for division in sorted(claimed_production - registered):
        errors.append(
            f"F2 D{division} is claimed as production-registered but is NOT in "
            f"CERTIFIED_PRODUCTION_VARGAS"
        )

    # F3: a non-claim contradicted by a PASS artifact.
    for token in block.get("non_claims", []):
        artifact = NON_CLAIM_ARTIFACTS.get(token)
        if artifact and artifact in passing:
            errors.append(
                f"F3 non-claim {token!r} is contradicted by {artifact}, which holds "
                f"a PASS certification artifact"
            )

    # F4: listed as not certified, but holding a PASS artifact.
    for division in sorted(claimed_not_certified):
        artifact = f"VARGA_D{division}_V1"
        if artifact in passing:
            errors.append(
                f"F4 D{division} is listed as not certified but {artifact} holds a "
                f"PASS certification artifact"
            )

    # F5: stated source-registry counts disagreeing with live values. The test
    # count is deliberately NOT carried in the block: the only faithful check is
    # a full suite run, which belongs in the test gate, not a documentation gate.
    for key, live in sorted(counts.items()):
        stated = block.get("counts", {}).get(key)
        if stated is not None and stated != live:
            errors.append(f"F5 counts.{key} states {stated}; live value is {live}")

    # Completeness: a PASS artifact accounted for nowhere. Without this, a
    # document could pass by simply omitting a capability.
    accounted = set(claimed_capabilities)
    for division in claimed_production | claimed_unregistered:
        accounted.add(f"VARGA_D{division}_V1")
    for name in sorted(passing - accounted):
        errors.append(
            f"F6 {name} holds a PASS artifact but is claimed nowhere in the block"
        )

    # A claimed capability with no PASS artifact behind it.
    for name in sorted(claimed_capabilities):
        if name not in passing:
            errors.append(
                f"F7 {name} is claimed as certified but has no PASS certification artifact"
            )

    # The certified-but-not-registered distinction, both halves enforced.
    for division in sorted(claimed_unregistered):
        artifact = f"VARGA_D{division}_V1"
        if artifact not in passing:
            errors.append(
                f"F8 D{division} is claimed certified-not-registered but {artifact} "
                f"holds no PASS artifact"
            )
        if division in registered:
            errors.append(
                f"F8 D{division} is claimed NOT production-registered but IS in "
                f"CERTIFIED_PRODUCTION_VARGAS"
            )

    return errors


def main(argv: list[str]) -> int:
    target = Path(argv[1]) if len(argv) > 1 else DEFAULT_TARGET
    if not target.is_file():
        print(f"FAIL: capability-state target not found: {target}")
        return 1

    errors = check(target.read_text())
    if errors:
        print(f"FAIL: documented capability state disagrees with live state ({target})")
        for error in errors:
            print(f"    {error}")
        print()
        print("The live sources are authoritative: CERTIFIED_PRODUCTION_VARGAS,")
        print("the regenerated certification artifacts, and the source registries.")
        print("Correct the document, not this gate.")
        return 1

    print(f"PASS: documented capability state matches live state ({target.name})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
