"""Parser negative controls MP-1 to MP-10 (R1 s5.4.3): a mutant-kill matrix.

Each mutant is an exact-once source replacement applied to the text of gitstatus.py and
loaded as a separate module. The designated detector (from test_gitstatus.py) is run
against the mutant and must FAIL; the same detector must PASS against the unmutated
module. A surviving mutant fails this test. The withdrawn `.strip()` control is not used:
it is equivalent on every well-formed porcelain v2 -z output.
"""

import sys
import types
from pathlib import Path

import pytest

HARNESS_DIR = Path(__file__).resolve().parents[1]
TESTS_DIR = Path(__file__).resolve().parent
for entry in (str(HARNESS_DIR), str(TESTS_DIR)):
    if entry not in sys.path:
        sys.path.insert(0, entry)

import gitstatus  # noqa: E402
import test_gitstatus as detectors  # noqa: E402

SOURCE_PATH = HARNESS_DIR / "gitstatus.py"

#: (id, category, old snippet, new snippet, designated detector, accepted failure types)
MUTANTS = [
    ("MP-1", "field misparsed: path taken without maxsplit",
     '    path = parts[8]\n',
     '    path = token.split(b" ")[8]\n',
     "T7b", ("AssertionError",)),
    ("MP-2", "field omitted: short type-1 record accepted leniently",
     '    if len(parts) != 9:\n'
     '        raise StatusParseError(f"ordinary record has {len(parts)} fields, expected 9: {token!r}")\n',
     '    if len(parts) != 9:\n'
     '        return Record("1", _decode(parts[-1]), parts[1].decode("ascii"), None, ())\n',
     "T11", ("AssertionError",)),
    ("MP-3", "field omitted: rename original-path token not consumed",
     '            step = 2\n',
     '            step = 1\n',
     "T6", ("AssertionError", "StatusParseError")),
    ("MP-3b", "record discarded: type-2 records dropped",
     '            records.append(_parse_rename(token, orig))\n',
     '            pass\n',
     "T6", ("AssertionError",)),
    ("MP-4", "prefix acceptance: allow-list entry used as a prefix",
     '    return record.kind == "1" and record.xy == ".M" and record.path in allow_list\n',
     '    return record.kind == "1" and record.xy == ".M" and any(record.path.startswith(entry) for entry in allow_list)\n',
     "T15", ("AssertionError",)),
    ("MP-4b", "directory-prefix acceptance (the WP-N1 rule)",
     '    return record.kind == "1" and record.xy == ".M" and record.path in allow_list\n',
     '    return record.kind == "1" and record.xy == ".M" and record.path.startswith(("certification/", "reports/"))\n',
     "T16", ("AssertionError",)),
    ("MP-5", "XY ignored: any change on an allow-listed path accepted",
     '    return record.kind == "1" and record.xy == ".M" and record.path in allow_list\n',
     '    return record.kind == "1" and record.path in allow_list\n',
     "T5", ("AssertionError",)),
    ("MP-6", "untracked records silently discarded",
     '            records.append(_parse_untracked(token))\n',
     '            pass\n',
     "T3", ("AssertionError",)),
    ("MP-7", "ignored records silently discarded",
     '            records.append(_parse_ignored(token))\n',
     '            pass\n',
     "T12", ("AssertionError",)),
    ("MP-7b", "ignored-baseline comparison inverted",
     '            if record.path not in pre:\n',
     '            if record.path in pre:\n',
     "T12", ("AssertionError",)),
    ("MP-8", "unexpected record type tolerated",
     '            raise StatusParseError(f"unrecognised status record type: {token[:32]!r}")\n',
     '            pass\n',
     "T14", ("AssertionError",)),
    ("MP-9", "truncated output tolerated",
     '    if not raw.endswith(b"\\0"):\n'
     '        raise StatusParseError("status output is not NUL-terminated (truncated)")\n',
     '    if not raw.endswith(b"\\0"):\n'
     '        raw = raw + b"\\0"\n',
     "T13", ("AssertionError",)),
    ("MP-10", "git failure tolerated as empty output",
     '    if done.returncode != 0:\n'
     '        raise GitStatusError(f"git status exited',
     '    if False:\n'
     '        raise GitStatusError(f"git status exited',
     "T17", ("AssertionError",)),
]


def load_mutant(mutant_id, old, new):
    source = SOURCE_PATH.read_text(encoding="utf-8")
    occurrences = source.count(old)
    if occurrences != 1:
        raise RuntimeError(f"{mutant_id}: mutation site occurs {occurrences} times, expected 1")
    mutated = source.replace(old, new, 1)
    if mutated == source:
        raise RuntimeError(f"{mutant_id}: mutation changed nothing")
    name = "gitstatus_mutant_" + mutant_id.replace("-", "_").lower()
    module = types.ModuleType(name)
    module.__file__ = str(SOURCE_PATH) + f" [{mutant_id}]"
    sys.modules[name] = module
    exec(compile(mutated, module.__file__, "exec", dont_inherit=True), module.__dict__)
    return module


@pytest.mark.parametrize("mutant", MUTANTS, ids=[m[0] for m in MUTANTS])
def test_mutant_is_killed_by_designated_detector(mutant):
    mutant_id, category, old, new, detector_name, accepted = mutant
    detector = detectors.DETECTORS[detector_name]

    detector(gitstatus)  # pristine control: the unmutated module must pass

    module = load_mutant(mutant_id, old, new)
    try:
        detector(module)
    except Exception as exc:  # noqa: BLE001 - the detector failing is the expected result
        kill = type(exc).__name__
    else:
        pytest.fail(f"{mutant_id} SURVIVED ({category}): detector {detector_name} passed")
    assert kill in accepted, f"{mutant_id} failed for an unexpected reason: {kill}"


def test_every_ceo_named_category_is_covered():
    categories = " ".join(m[1] for m in MUTANTS)
    for needle in ("misparsed", "omitted", "prefix", "untracked", "ignored", "unexpected",
                   "truncated", "git failure"):
        assert needle in categories


def test_mutant_sites_are_exact_once():
    source = SOURCE_PATH.read_text(encoding="utf-8")
    for mutant_id, _category, old, new, _detector, _accepted in MUTANTS:
        assert source.count(old) == 1, mutant_id
        assert old != new, mutant_id


def test_withdrawn_strip_control_is_equivalent_on_well_formed_output():
    """Documents why `.strip()` is not a meaningful negative control (RD-C2)."""

    from test_gitstatus import MOD, RENAME
    for raw in (MOD(b"certification/A.json"), RENAME, b"? x\0", b"! y\0", b""):
        assert raw.strip() == raw
