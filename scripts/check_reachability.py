"""C4: production reachability against certification coverage (ADR-0099 s3 and s7, ADR-0107).

"In use" is decided here by an executed check, not by reading code. For every public
engine function and method it reports one status:

  IN_USE_COVERED        reachable from outside the verification surface, and either a
                        GATED member of a PASS artifact or called from one.
  IN_USE_UNCOVERED      reachable by a live path, and covered by no certification.
  DEAD_PATH_UNCOVERED   ADR-0099 s3's counting rule finds a call site outside the
                        surface, but every such caller is itself unreachable from any
                        entry point. It is in use by the literal rule, so it is reported
                        and tracked, never dropped.
  UNKNOWN               the only evidence is ambiguous: a method call on a value of
                        unknown type carrying this name. Neither use nor absence is
                        established, and this status says so.
  NOT_IN_USE            no call site outside the surface, no ambiguous evidence, no export.

Entry points: module-level code outside the surface, every function in a non-engine
module outside the surface, and names exported through ADR-0099 U2's surfaces.

Excluded from the universe, disclosed in the report: engine/main.py's route handlers
(they are callers and exports, not capabilities) and engine/tools/ (developer scaffolding,
not analytical). ADR-0108 s4 item 2, ratified.

An UNKNOWN method leaves that status through one of three kinds of evidence, never through
inspection alone: coverage_static resolves the receiver from the source; the method's class
is CONTAINED, so no value of it exists outside the surface for an unresolved call to land on;
or RECEIVER_EVIDENCE, a named caller whose unresolved use is still in the source, and a
committed test proving at runtime that the use reaches this method.

FAIL when: an uncovered in-use function is not tracked by an OPEN backlog finding; a
tracked finding is no longer uncovered; a source file cannot be parsed; receiver evidence
is stale or names no committed proof; or the committed report differs from this run.

The gate's PASS does NOT mean clause 2 of the JATAKA exit criterion is satisfied. The
report's `exit_clause_2` separates two different claims:

  no_confirmed_violations   no live-path or dead-path uncovered function was found.
  coverage_established      that, and no uncovered UNKNOWN method remains. Only this
                            supports `satisfied`: an unresolved method is neither
                            shown to be unused nor shown to be certified.

Exit 0 = PASS, 1 = FAIL. `--write` regenerates the committed report. `--backlog PATH` and
`--certification-dir PATH` let a negative control run the real enforcement path against a
planted backlog or a planted artifact set. `--exit-criterion` answers one question: exit 0
only if clause 2 is satisfied. That is clause 2 alone, and it is never JATAKA exit.
"""

from __future__ import annotations

import ast
import dataclasses
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import coverage_static  # noqa: E402

CERTIFICATION_DIR = ROOT / "certification"
BACKLOG = ROOT / "docs" / "CERTIFICATION_REMEDIATION_BACKLOG.json"
REPORT = ROOT / "reports" / "c4_reachability.json"

EXCLUDED_PREFIXES = {
    "engine.main.": "API route handlers: callers and exports, not capabilities",
    "engine.tools.": "developer scaffolding, not analytical",
}
FINDING_DISPOSITION = "OPEN_REACHABILITY_FINDING"
UNCOVERED = ("IN_USE_UNCOVERED", "DEAD_PATH_UNCOVERED")

_DASHA_PROOF = ("engine/tests/test_stage_b_coverage_gates.py::"
                "test_c4_dasha_period_properties_run_on_the_certified_path")

#: method -> the caller whose unresolved attribute use reaches it, with its committed proof.
RECEIVER_EVIDENCE = {
    "engine.models.dasha.DashaPeriod.lord": {
        "caller": "engine.dasha.vimshottari._subdivide", "proof": _DASHA_PROOF},
    "engine.models.dasha.DashaPeriod.duration_years": {
        "caller": "engine.dasha.vimshottari._subdivide", "proof": _DASHA_PROOF},
}

#: What a review found about each remaining UNKNOWN. A future one stays unresolved until it
#: has evidence, and reads NOT REVIEWED in the report until it is listed here. The nine reviewed
#: at ADR-0108 each now have evidence: see the C4 report and the Stage C record.
UNKNOWN_REVIEW: dict[str, str] = {}


def gated_members(certification_dir: Path) -> tuple[set[str], list[str]]:
    """GATED members of PASS artifacts. Anything else is not coverage."""

    members: set[str] = set()
    errors: list[str] = []
    for path in sorted(certification_dir.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"R5 {path.name} is not readable: {exc}")
            continue
        capabilities = payload.get("capabilities")
        if not isinstance(capabilities, list) or not payload.get("capability_schema"):
            continue  # Frozen evidence, whose `capabilities` is not this enumeration.
        verdict = payload.get("result") or (payload.get("summary") or {}).get("result")
        if verdict != "PASS":
            continue
        for capability in capabilities:
            for member in capability.get("members", []):
                if member.get("disposition") == "GATED":
                    members.add(member["callable"])
    return members, errors


def analyse(graph, members: set[str]) -> dict:
    """Pure analysis: the same graph and coverage always give the same report."""

    outside = {owner for owner, relative in graph.owners.items()
               if not coverage_static.in_verification_surface(relative)}
    roots: set[str] = set(graph.exports)
    for owner in outside:
        relative = graph.owners[owner]
        is_module = owner == coverage_static.module_name(relative)
        if is_module or not relative.startswith("engine/"):
            roots.add(owner)
    live = graph.closure(roots)
    covered = graph.closure(members)

    callers: dict[str, set[str]] = {}
    for owner, targets in graph.edges.items():
        if owner in outside:
            for target in targets:
                callers.setdefault(target, set()).add(owner)
    ambiguous: dict[str, set[str]] = {}
    for owner, names in graph.ambiguous.items():
        if owner in outside:
            for name in names:
                ambiguous.setdefault(name, set()).add(owner)

    # A contained class has no value outside the surface, so an unresolved `x.m` there cannot
    # land on its methods. Its direct callers still count, exactly as before.
    method_names = {dotted for names in graph.methods.values() for dotted in names
                    if not graph.contained(dotted.rsplit(".", 1)[0])}
    rows: dict[str, dict] = {}
    for name in sorted(graph.definitions):
        leaf = name.rsplit(".", 1)[-1]
        if leaf.startswith("_") or any(name.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
            continue
        direct = sorted(callers.get(name, set()))
        exported = sorted(graph.exports.get(name, set()))
        maybe = sorted(ambiguous.get(leaf, set())) if name in method_names else []
        if direct or exported:
            if name in covered:
                status = "IN_USE_COVERED"
            elif name in live or exported:
                status = "IN_USE_UNCOVERED"
            else:
                status = "DEAD_PATH_UNCOVERED"
        elif maybe:
            status = "UNKNOWN"
        else:
            status = "NOT_IN_USE"
        row = {"status": status, "covered": name in covered, "file": graph.definitions[name]}
        if direct:
            row["callers"] = direct[:5]
            row["caller_count"] = len(direct)
        if exported:
            row["exported_by"] = exported
        if status == "UNKNOWN":
            row["ambiguous_owner_count"] = len(maybe)
            row["ambiguous_owner_sample"] = maybe[:3]
        rows[name] = row

    summary: dict[str, int] = {}
    for row in rows.values():
        summary[row["status"]] = summary.get(row["status"], 0) + 1
    dynamic = {module: sorted(names) for module, names in sorted(graph.dynamic.items())
               if module.startswith("engine") and not module.startswith("engine.tests")}
    return {
        "schema": "ace-c4-reachability-v1",
        "authority": "ADR-0099 s3, s7; ADR-0107",
        "summary": dict(sorted(summary.items())),
        "universe_exclusions": EXCLUDED_PREFIXES,
        "dynamic_dispatch_in_engine_modules": dynamic,
        "rows": rows,
    }


def open_findings(backlog: dict | None) -> dict[str, dict]:
    return {entry["callable"]: entry for entry in (backlog or {}).get("entries", [])
            if isinstance(entry, dict) and entry.get("disposition") == FINDING_DISPOSITION
            and entry.get("status") == "OPEN" and "callable" in entry}


def evaluate(analysis: dict, findings: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    uncovered = {name for name, row in analysis["rows"].items() if row["status"] in UNCOVERED}
    for name in sorted(uncovered - set(findings)):
        row = analysis["rows"][name]
        errors.append(f"R1 {name} is {row['status']} (callers: {row.get('callers', row.get('exported_by'))}) "
                      f"and no OPEN backlog finding tracks it")
    for name in sorted(set(findings) - uncovered):
        status = analysis["rows"].get(name, {}).get("status", "absent")
        errors.append(f"R2 stale backlog finding: {name} is now {status}, not uncovered. Close the entry.")
    return errors


def exit_clause_2(analysis: dict) -> dict:
    """The exit criterion's second clause, stated without softening."""

    live = sorted(name for name, row in analysis["rows"].items() if row["status"] == "IN_USE_UNCOVERED")
    dead = sorted(name for name, row in analysis["rows"].items() if row["status"] == "DEAD_PATH_UNCOVERED")
    unknown = sorted(name for name, row in analysis["rows"].items() if row["status"] == "UNKNOWN")
    material = [name for name in unknown if not analysis["rows"][name]["covered"]]
    no_confirmed_violations = not live and not dead
    coverage_established = no_confirmed_violations and not material
    return {
        "no_confirmed_violations": no_confirmed_violations,
        "coverage_established": coverage_established,
        "satisfied": coverage_established,
        "live_path_uncovered": live,
        "dead_path_uncovered": dead,
        "material_unknown": material,
        "unknown_not_established_either_way": unknown,
    }


def exit_refusals(clause: dict) -> list[str]:
    """Why an exit PASS must be refused. Empty only if coverage is established."""

    refusals = [f"live-path uncovered: {name}" for name in clause["live_path_uncovered"]]
    refusals += [f"dead-path uncovered: {name}" for name in clause["dead_path_uncovered"]]
    refusals += [f"material UNKNOWN, neither shown unused nor shown certified: {name}"
                 for name in clause["material_unknown"]]
    return refusals


def apply_receiver_evidence(graph, evidence: dict, root: Path) -> tuple[object, list[str]]:
    """A copy of `graph` with each proven use as an edge, plus any evidence that fails."""

    errors: list[str] = []
    edges = {owner: set(targets) for owner, targets in graph.edges.items()}
    for method, item in evidence.items():
        caller, proof = item["caller"], item["proof"]
        leaf = method.rsplit(".", 1)[-1]
        if method not in graph.definitions:
            errors.append(f"R6 receiver evidence names {method}, which does not exist")
            continue
        if leaf not in graph.ambiguous.get(caller, set()):
            errors.append(f"R6 stale receiver evidence: {caller} no longer has an unresolved use of `{leaf}`")
            continue
        file_part, _, test_name = proof.partition("::")
        source = root / file_part
        names = set()
        if source.is_file():
            names = {node.name for node in ast.parse(source.read_text(encoding="utf-8-sig")).body
                     if isinstance(node, ast.FunctionDef)}
        if test_name not in names:
            errors.append(f"R6 receiver evidence for {method} names no committed proof: {proof}")
            continue
        edges.setdefault(caller, set()).add(method)
    return dataclasses.replace(graph, edges=edges), errors


def build_report(root: Path, certification_dir: Path, graph=None,
                 evidence: dict | None = None) -> tuple[dict, list[str], object]:
    evidence = RECEIVER_EVIDENCE if evidence is None else evidence
    graph = coverage_static.build_graph(root) if graph is None else graph
    members, errors = gated_members(certification_dir)
    errors.extend(f"R3 cannot parse {name}: {why}" for name, why in graph.unparsed.items())
    for member in sorted(members):
        if member not in graph.definitions and member not in graph.data:
            errors.append(f"R3 GATED member {member} does not exist in the source")
    resolved_graph, evidence_errors = apply_receiver_evidence(graph, evidence, root)
    errors.extend(evidence_errors)
    analysis = analyse(resolved_graph, members)
    for method, item in evidence.items():
        if method in analysis["rows"]:
            analysis["rows"][method]["receiver_evidence"] = item["proof"]
    analysis["exit_clause_2"] = exit_clause_2(analysis)
    analysis["unknown_review"] = {name: UNKNOWN_REVIEW.get(name, "NOT REVIEWED")
                                  for name in analysis["exit_clause_2"]["material_unknown"]}
    return analysis, errors, graph


def render(report: dict) -> str:
    return json.dumps(report, indent=1, sort_keys=True) + "\n"


def check(root: Path = ROOT, certification_dir: Path = CERTIFICATION_DIR, backlog_path: Path = BACKLOG,
          report_path: Path = REPORT, graph=None) -> tuple[list[str], dict]:
    report, errors, _graph = build_report(root, certification_dir, graph)
    try:
        backlog = json.loads(backlog_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return errors + [f"R5 the remediation backlog is not readable: {exc}"], report
    errors.extend(evaluate(report, open_findings(backlog)))
    try:
        committed = report_path.read_text(encoding="utf-8")
    except OSError as exc:
        return errors + [f"R4 the committed reachability report is not readable: {exc}"], report
    if committed != render(report):
        errors.append(f"R4 {report_path.name} differs from this run; regenerate it with --write and review the diff")
    return errors, report


def main(argv: list[str]) -> int:
    if "--write" in argv:
        report, errors, _graph = build_report(ROOT, CERTIFICATION_DIR)
        REPORT.write_text(render(report), encoding="utf-8", newline="\n")
        print(f"wrote {REPORT.relative_to(ROOT).as_posix()}: {report['summary']}")
        for error in errors:
            print(f"    {error}")
        return 1 if errors else 0
    backlog_path = Path(argv[argv.index("--backlog") + 1]) if "--backlog" in argv else BACKLOG
    certification_dir = (Path(argv[argv.index("--certification-dir") + 1]) if "--certification-dir" in argv
                         else CERTIFICATION_DIR)
    errors, report = check(certification_dir=certification_dir, backlog_path=backlog_path)
    clause = report["exit_clause_2"]
    print(f"reachability: {report['summary']}")
    print(f"no confirmed violations: {clause['no_confirmed_violations']} ({len(clause['live_path_uncovered'])} "
          f"live-path, {len(clause['dead_path_uncovered'])} dead-path uncovered)")
    print(f"coverage established: {clause['coverage_established']} ({len(clause['material_unknown'])} material "
          f"UNKNOWN of {len(clause['unknown_not_established_either_way'])})")
    print(f"exit clause 2 satisfied: {clause['satisfied']}")
    if "--exit-criterion" in argv:
        refusals = exit_refusals(clause)
        for refusal in refusals:
            print(f"    {refusal}")
        print("EXIT CRITERION: " + ("REFUSED" if refusals or errors
                                    else "clause 2 satisfied. Clause 2 alone: this is not JATAKA exit"))
        return 1 if refusals or errors else 0
    if errors:
        print(f"FAIL: reachability ({len(errors)} failures)")
        for error in errors:
            print(f"    {error}")
        return 1
    print("PASS: every uncovered in-use function is explicitly tracked; this is not a statement that none exist")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
