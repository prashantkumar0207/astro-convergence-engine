"""C3: the scope-coverage gate (ADR-0099 s4 and s7, ADR-0101 s2-s5, ADR-0102, ADR-0107).

Evaluated from each artifact's own declarations, never by parsing `scope` prose:

  S1  a scope-bearing artifact enumerates its capabilities under stable identifiers;
  S2  every capability has members, each with a valid path, kind and disposition;
  S3  every gate declares an `exercises` array (an empty one must state why);
  S4  `exercises` names only capabilities the artifact enumerates;
  S5  a capability in no gate's `exercises` and not in `scope_not_gated` is a SCOPE
      OVERCLAIM. It fails unless an OPEN backlog entry tracks that exact capability;
  S6  a member's disposition must agree with the gates: naming a parent capability
      never verifies a member, and a GATED member needs a gate that lists its capability;
  S7  a member's path must exist in the source;
  S8  each `scope_not_gated` item needs a real member or capability and a reason;
  S9  ADR-0099 s5 / C5: an inherited claim must name its delegate and a committed test;
  S10 independent evidence: a static reading of the certifier and its validator must
      support each GATED member's `exercised_by`. A declaration is not an observation
      (ADR-0101 s3), so this is checked by a separate method. It supports a declaration,
      and cannot prove a gate's assertions are strong.

The gate reads the 22 scope-bearing artifacts named by ADR-0102 s2, plus SUPPORT_PATHS_V1,
which ADR-0108 s4 item 5's certification route added later, and EVIDENCE_FOUNDATIONS_V1, the
structural EVIDENCE certification ADR-0115 s4 added. The four frozen artifacts carry
no such content; their dispositions live in the backlog.

Exit 0 = PASS, 1 = FAIL. Paths are injectable so the negative controls can run the
real enforcement path against planted copies.
"""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import coverage_static  # noqa: E402

CERTIFICATION_DIR = ROOT / "certification"
BACKLOG = ROOT / "docs" / "CERTIFICATION_REMEDIATION_BACKLOG.json"

SCOPE_BEARING_ARTIFACTS = (
    "EVIDENCE_FOUNDATIONS_V1_certification.json",
    "current_engine_certification.json", "KP_CHAIN_V1_certification.json",
    "KP_SIGNIFICATOR_V1_certification.json", "PANCHANGA_V1_certification.json",
    "PARASHARI_DRISHTI_V1_certification.json", "PARASHARI_YOGA_V1_certification.json",
    "RISE_SET_V1_certification.json", "SIGN_CONVENTION_V1_certification.json",
    "SUPPORT_PATHS_V1_certification.json",
    "TRANSIT_V1_certification.json", "TRIKALAM_V1_certification.json",
    "VARGA_D2_V1_certification.json", "VARGA_D3_V1_certification.json",
    "VARGA_D4_V1_certification.json", "VARGA_D7_V1_certification.json",
    "VARGA_D12_V1_certification.json", "VARGA_D16_V1_certification.json",
    "VARGA_D20_V1_certification.json", "VARGA_D24_V1_certification.json",
    "VARGA_D30_V1_certification.json", "VARGA_D40_V1_certification.json",
    "VARGA_D45_V1_certification.json", "VIMSHOTTARI_V1_certification.json",
)

#: Certifier for each artifact, for the S10 static reading.
CERTIFIERS = {
    "current_engine_certification.json": "certify_current_engine.py",
    "KP_CHAIN_V1_certification.json": "certify_kp_chain.py",
    "KP_SIGNIFICATOR_V1_certification.json": "certify_kp_significator.py",
    "PANCHANGA_V1_certification.json": "certify_panchanga.py",
    "PARASHARI_DRISHTI_V1_certification.json": "certify_parashari_drishti.py",
    "PARASHARI_YOGA_V1_certification.json": "certify_parashari_yoga.py",
    "RISE_SET_V1_certification.json": "certify_rise_set.py",
    "SIGN_CONVENTION_V1_certification.json": "certify_sign_convention.py",
    "SUPPORT_PATHS_V1_certification.json": "certify_support_paths.py",
    "EVIDENCE_FOUNDATIONS_V1_certification.json": "certify_evidence_foundations.py",
    "TRANSIT_V1_certification.json": "certify_transits.py",
    "TRIKALAM_V1_certification.json": "certify_trikalam.py",
    "VIMSHOTTARI_V1_certification.json": "certify_vimshottari.py",
    **{f"VARGA_D{n}_V1_certification.json": f"certify_d{n}.py" for n in (2, 3, 4, 7, 12, 16, 20, 24, 30, 40, 45)},
}

CAPABILITY_ID = re.compile(r"^[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*$")
MEMBER_PATH = re.compile(r"^engine(\.[A-Za-z_][A-Za-z0-9_]*)+$")
GATED = "GATED"
SCOPE_NOT_GATED = "SCOPE_NOT_GATED"
OPEN_SCOPE_OVERCLAIM = "OPEN_SCOPE_OVERCLAIM"
INHERITED = "INHERITED_NEUTRALITY_PROVEN"
DISPOSITIONS = (GATED, SCOPE_NOT_GATED, OPEN_SCOPE_OVERCLAIM, INHERITED)


def _gate_blocks(artifact_name: str, payload: dict) -> tuple[dict, list[str]]:
    """gate name -> (exercises, note), wherever the artifact records them."""

    errors, gates = [], {}
    raw = payload.get("gates")
    if not isinstance(raw, dict) or not raw:
        return {}, [f"S3 {artifact_name} has no gates"]
    scalar = payload.get("scalar_gate_exercises", {})
    for name, block in raw.items():
        record = block if isinstance(block, dict) else scalar.get(name)
        if not isinstance(record, dict) or not isinstance(record.get("exercises"), list):
            errors.append(f"S3 {artifact_name} gate {name} declares no `exercises` array")
            continue
        gates[name] = (record["exercises"], record.get("exercises_note"))
    return gates, errors


def open_overclaim_entries(backlog: dict | None) -> dict[str, dict]:
    """OPEN overclaim entries in the backlog, keyed by entry id."""

    entries = (backlog or {}).get("entries", [])
    return {entry["id"]: entry for entry in entries
            if isinstance(entry, dict) and entry.get("status") == "OPEN"
            and entry.get("disposition") == OPEN_SCOPE_OVERCLAIM and "id" in entry}


def check_artifact(artifact_name: str, payload: dict, overclaims: dict[str, dict],
                   graph, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    capabilities = payload.get("capabilities")
    if not isinstance(capabilities, list) or not capabilities:
        return [f"S1 {artifact_name} enumerates no capabilities; ADR-0101 s5 item 4: not compliant"]

    gates, gate_errors = _gate_blocks(artifact_name, payload)
    errors.extend(gate_errors)

    known_ids: set[str] = set()
    for capability in capabilities:
        identifier = capability.get("id") if isinstance(capability, dict) else None
        if not isinstance(identifier, str) or not CAPABILITY_ID.match(identifier):
            errors.append(f"S1 {artifact_name}: invalid capability identifier {identifier!r}")
            continue
        if identifier in known_ids:
            errors.append(f"S1 {artifact_name}: duplicate capability identifier {identifier}")
        known_ids.add(identifier)

    exercised_by_gate: dict[str, set[str]] = {}
    for gate, (exercises, note) in gates.items():
        if not exercises and not (isinstance(note, str) and note.strip()):
            errors.append(f"S3 {artifact_name} gate {gate} has an empty `exercises` with no stated reason")
        for identifier in exercises:
            if identifier not in known_ids:
                errors.append(f"S4 {artifact_name} gate {gate} exercises unknown capability {identifier!r}")
            exercised_by_gate.setdefault(identifier, set()).add(gate)

    not_gated = payload.get("scope_not_gated")
    if not isinstance(not_gated, list):
        errors.append(f"S8 {artifact_name} has no `scope_not_gated` array")
        not_gated = []
    not_gated_ids = {}
    for item in not_gated:
        if not isinstance(item, dict) or not str(item.get("reason", "")).strip() or not item.get("id"):
            errors.append(f"S8 {artifact_name}: a scope_not_gated item lacks an id or a reason: {item!r}")
            continue
        not_gated_ids[item["id"]] = item

    all_members: set[str] = set()
    for capability in capabilities:
        if not isinstance(capability, dict) or capability.get("id") not in known_ids:
            continue
        identifier = capability["id"]
        members = capability.get("members")
        if not isinstance(members, list) or not members:
            errors.append(f"S2 {artifact_name}: capability {identifier} has no members")
            continue
        for member in members:
            errors.extend(_check_member(artifact_name, identifier, member, gates, exercised_by_gate,
                                        not_gated_ids, overclaims, graph, root))
            if isinstance(member, dict):
                all_members.add(member.get("callable"))
        member_gates = {gate for member in members if isinstance(member, dict)
                        for gate in member.get("exercised_by", [])}
        # S6: a gate may not list a capability unless it claims one of its members.
        for gate in sorted(exercised_by_gate.get(identifier, set()) - member_gates):
            errors.append(f"S6 {artifact_name} gate {gate} names capability {identifier} but exercises none of "
                          f"its members; naming a parent does not verify a member")
        # S5, ADR-0101 s5 item 3.
        if identifier not in exercised_by_gate and identifier not in not_gated_ids:
            tracked = all(isinstance(member, dict) and member.get("disposition") in (
                OPEN_SCOPE_OVERCLAIM, SCOPE_NOT_GATED) for member in members)
            if not tracked or not any(member.get("disposition") == OPEN_SCOPE_OVERCLAIM for member in members):
                errors.append(f"S5 SCOPE OVERCLAIM: {artifact_name} capability {identifier} is exercised by no "
                              f"gate, is not in scope_not_gated, and no OPEN backlog entry tracks it")

    for identifier in not_gated_ids:
        if identifier not in known_ids and identifier not in all_members:
            errors.append(f"S8 {artifact_name}: scope_not_gated names {identifier}, which is not enumerated")
    return errors


def _check_member(artifact_name, capability_id, member, gates, exercised_by_gate, not_gated_ids,
                  overclaims, graph, root) -> list[str]:
    errors: list[str] = []
    where = f"{artifact_name} {capability_id}"
    if not isinstance(member, dict):
        return [f"S2 {where}: a member is not an object"]
    path = member.get("callable")
    kind = member.get("kind")
    disposition = member.get("disposition")
    exercised_by = member.get("exercised_by")
    if not isinstance(path, str) or not MEMBER_PATH.match(path):
        errors.append(f"S2 {where}: invalid member path {path!r}")
        return errors
    if kind not in ("callable", "data"):
        errors.append(f"S2 {where} {path}: invalid kind {kind!r}")
    if disposition not in DISPOSITIONS:
        errors.append(f"S2 {where} {path}: invalid disposition {disposition!r}")
    if not isinstance(exercised_by, list):
        errors.append(f"S2 {where} {path}: `exercised_by` is not an array")
        exercised_by = []

    # S7: the member must exist in the source, as the kind it claims.
    if graph is not None:
        table = graph.data if kind == "data" else graph.definitions
        if path not in table:
            errors.append(f"S7 {where}: member {path} does not exist in the source as {kind}")

    if disposition == GATED:
        if not exercised_by:
            errors.append(f"S6 {where} {path}: GATED, but no gate exercises it")
    elif exercised_by:
        errors.append(f"S6 {where} {path}: {disposition}, yet it lists exercising gates")
    for gate in exercised_by:
        if gate not in gates:
            errors.append(f"S6 {where} {path}: exercised_by names unknown gate {gate}")
        elif capability_id not in gates[gate][0]:
            errors.append(f"S6 {where} {path}: gate {gate} does not list {capability_id} in `exercises`")
    if disposition == SCOPE_NOT_GATED and path not in not_gated_ids:
        errors.append(f"S8 {where} {path}: SCOPE_NOT_GATED, but absent from `scope_not_gated`")
    if disposition == OPEN_SCOPE_OVERCLAIM:
        entry = overclaims.get(member.get("backlog_entry"))
        if entry is None:
            errors.append(f"S5 SCOPE OVERCLAIM: {where} {path} names backlog entry "
                          f"{member.get('backlog_entry')!r}, which is not an OPEN overclaim entry")
        elif entry.get("artifact") != artifact_name or entry.get("capability") != capability_id:
            errors.append(f"S5 {where} {path}: backlog entry {entry['id']} tracks a different capability")
        if capability_id in exercised_by_gate:
            errors.append(f"S6 {where} {path}: open overclaim, yet a gate lists its capability")
    if disposition == INHERITED:
        errors.extend(_check_inherited(where, path, member, root))
    return errors


def _check_inherited(where, path, member, root) -> list[str]:
    """S9, ADR-0099 s5: inspection is not enough. A committed test must exist."""

    errors = []
    if not member.get("delegate"):
        errors.append(f"S9 {where} {path}: inherited certification names no delegate")
    reference = str(member.get("neutrality_test", ""))
    file_part, _, test_name = reference.partition("::")
    source = root / file_part if file_part else None
    if source is None or not source.is_file() or not test_name:
        return errors + [f"S9 {where} {path}: inherited certification names no committed neutrality test "
                         f"(`path::test`), got {reference!r}"]
    tree = ast.parse(source.read_text(encoding="utf-8-sig"))
    if test_name not in {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}:
        errors.append(f"S9 {where} {path}: {reference} does not exist")
    return errors


def _local_functions(tree: ast.Module) -> dict[str, ast.FunctionDef]:
    return {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}


def _gate_functions(tree: ast.Module, gate_names) -> dict[str, str]:
    """gate name -> the certifier function that runs it."""

    functions = _local_functions(tree)
    mapping: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            for key, value in zip(node.keys, node.values):
                if (isinstance(key, ast.Constant) and key.value in gate_names and isinstance(value, ast.Call)
                        and isinstance(value.func, ast.Name) and value.func.id in functions):
                    mapping[key.value] = value.func.id
    for gate in gate_names:
        if gate in mapping:
            continue
        prefix = f"gate_{gate.split('_')[0].lower()}_"
        candidates = [name for name in functions if name.startswith(prefix)]
        mapping[gate] = candidates[0] if len(candidates) == 1 else "main"
    return mapping


def _reach_of(function_name, tree, certifier_module, graph, root) -> set[str]:
    """Static reach of one gate: its helpers, any validator it runs, and onward."""

    functions = _local_functions(tree)
    seen, stack, reached, validators = set(), [function_name], set(), set()
    while stack:
        current = stack.pop()
        if current in seen or current not in functions:
            continue
        seen.add(current)
        for node in ast.walk(functions[current]):
            if isinstance(node, ast.Name) and node.id in functions:
                stack.append(node.id)
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                match = re.fullmatch(r"(validate_\w+)\.py", node.value)
                if match:
                    validators.add(match.group(1))
        reached |= graph.edges.get(f"{certifier_module}.{current}", set())
    # A module-level constant naming a validator (e.g. a VALIDATOR path).
    for validator in validators:
        reached |= graph.edges.get(validator, set())
        for owner, targets in graph.edges.items():
            if owner.startswith(f"{validator}."):
                reached |= targets
    return graph.closure(reached)


def check_independent_evidence(artifact_name: str, payload: dict, graph, root: Path = ROOT) -> list[str]:
    """S10: does a static reading of the certifier support each GATED member's gates?"""

    certifier = CERTIFIERS.get(artifact_name)
    if certifier is None:
        return [f"S10 {artifact_name}: no certifier is known for the static reading"]
    path = root / "scripts" / certifier
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    module = coverage_static.module_name(f"scripts/{certifier}")
    gate_names = list(payload.get("gates", {}))
    functions = _gate_functions(tree, gate_names)
    reach_by_function: dict[str, set[str]] = {}
    errors: list[str] = []
    for capability in payload.get("capabilities", []):
        for member in capability.get("members", []):
            if member.get("disposition") != GATED:
                continue
            for gate in member.get("exercised_by", []):
                function = functions.get(gate, "main")
                if function not in reach_by_function:
                    reach_by_function[function] = _reach_of(function, tree, module, graph, root)
                if member["callable"] not in reach_by_function[function]:
                    errors.append(f"S10 {artifact_name} gate {gate} declares {member['callable']}, but a static "
                                  f"reading of {certifier}:{function} does not reach it")
    return errors


def load_backlog(path: Path) -> tuple[dict | None, list[str]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except (OSError, json.JSONDecodeError) as exc:
        return None, [f"S5 the remediation backlog is not readable at {path}: {exc}"]


def check(certification_dir: Path = CERTIFICATION_DIR, backlog_path: Path = BACKLOG, root: Path = ROOT,
          graph=None) -> tuple[list[str], dict]:
    """Every failure, plus counts for the report. Empty failures means PASS."""

    graph = coverage_static.build_graph(root) if graph is None else graph
    errors = [f"S7 cannot parse {name}: {why}" for name, why in graph.unparsed.items()]
    backlog, backlog_errors = load_backlog(backlog_path)
    errors.extend(backlog_errors)
    overclaims = open_overclaim_entries(backlog)
    counts = {"artifacts": 0, "capabilities": 0, "members": 0, "gates": 0, "open_overclaims": 0,
              "scope_not_gated": 0, "inherited_claims": 0}
    for name in SCOPE_BEARING_ARTIFACTS:
        path = certification_dir / name
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"S1 {name} is not readable: {exc}")
            continue
        errors.extend(check_artifact(name, payload, overclaims, graph, root))
        errors.extend(check_independent_evidence(name, payload, graph, root))
        counts["artifacts"] += 1
        counts["gates"] += len(payload.get("gates") or {})
        counts["scope_not_gated"] += len(payload.get("scope_not_gated") or [])
        for capability in payload.get("capabilities") or []:
            counts["capabilities"] += 1
            for member in capability.get("members", []):
                counts["members"] += 1
                counts["open_overclaims"] += member.get("disposition") == OPEN_SCOPE_OVERCLAIM
                counts["inherited_claims"] += member.get("disposition") == INHERITED
    return errors, counts


def main(argv: list[str]) -> int:
    certification_dir = Path(argv[1]) if len(argv) > 1 else CERTIFICATION_DIR
    backlog_path = Path(argv[2]) if len(argv) > 2 else BACKLOG
    errors, counts = check(certification_dir, backlog_path)
    if errors:
        print(f"FAIL: scope coverage ({len(errors)} failures)")
        for error in errors:
            print(f"    {error}")
        return 1
    print(f"PASS: scope coverage: {counts['artifacts']} artifacts, {counts['capabilities']} capabilities, "
          f"{counts['members']} members, {counts['gates']} gates; {counts['open_overclaims']} open tracked "
          f"overclaims, {counts['scope_not_gated']} scope_not_gated, {counts['inherited_claims']} inherited claims")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
