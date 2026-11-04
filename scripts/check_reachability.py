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
not analytical). Both exclusions await ratification with ADR-0108.

FAIL when: an uncovered in-use function is not tracked by an OPEN backlog finding; a
tracked finding is no longer uncovered; a source file cannot be parsed; or the
committed report differs from this run. PASS does NOT mean clause 2 of the JATAKA exit
criterion is satisfied: the report's `exit_clause_2` field states that separately.

Exit 0 = PASS, 1 = FAIL. `--write` regenerates the committed report. `--backlog PATH`
lets a negative control run the real enforcement path against a planted backlog.
"""

from __future__ import annotations

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

    method_names = {dotted for names in graph.methods.values() for dotted in names}
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
    return {
        "satisfied": not live and not dead,
        "live_path_uncovered": live,
        "dead_path_uncovered": dead,
        "unknown_not_established_either_way": unknown,
    }


def build_report(root: Path, certification_dir: Path, graph=None) -> tuple[dict, list[str], object]:
    graph = coverage_static.build_graph(root) if graph is None else graph
    members, errors = gated_members(certification_dir)
    errors.extend(f"R3 cannot parse {name}: {why}" for name, why in graph.unparsed.items())
    for member in sorted(members):
        if member not in graph.definitions and member not in graph.data:
            errors.append(f"R3 GATED member {member} does not exist in the source")
    analysis = analyse(graph, members)
    analysis["exit_clause_2"] = exit_clause_2(analysis)
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
    errors, report = check(backlog_path=backlog_path)
    clause = report["exit_clause_2"]
    print(f"reachability: {report['summary']}")
    print(f"exit clause 2 satisfied: {clause['satisfied']} ({len(clause['live_path_uncovered'])} live-path, "
          f"{len(clause['dead_path_uncovered'])} dead-path uncovered; "
          f"{len(clause['unknown_not_established_either_way'])} unknown)")
    if errors:
        print(f"FAIL: reachability ({len(errors)} failures)")
        for error in errors:
            print(f"    {error}")
        return 1
    print("PASS: every uncovered in-use function is explicitly tracked; this is not a statement that none exist")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
