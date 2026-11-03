"""Parser and classification tests T1-T18 (R1 s5.4.1).

Each check is written as a `detector_*` function taking the module under test, so the
mutant-kill matrix (test_gitstatus_mutants.py) can run the identical check against a
source-mutated copy of gitstatus.py. Detectors raise AssertionError on failure.
"""

import os
import subprocess
import sys
from pathlib import Path

HARNESS_DIR = Path(__file__).resolve().parents[1]
if str(HARNESS_DIR) not in sys.path:
    sys.path.insert(0, str(HARNESS_DIR))

import gitstatus  # noqa: E402

H = b"a" * 40
Z = b"0" * 40
AL = frozenset({"certification/A.json", "reports/a.md"})


def F1(xy, mode_head, mode_index, mode_worktree, oid_head, oid_index, path):
    return (b"1 " + xy + b" N... " + mode_head + b" " + mode_index + b" " + mode_worktree
            + b" " + oid_head + b" " + oid_index + b" " + path + b"\0")


def MOD(path):
    return F1(b".M", b"100644", b"100644", b"100644", H, H, path)


RENAME = b"2 R. N... 100644 100644 100644 " + H + b" " + H + b" R100 certification/B.json\0engine/x.py\0"


def verdict(gs, raw, allow=AL, pre=frozenset()):
    return gs.classify(gs.parse_records(gs.split_records(raw)), allow, pre)


def expect_raises(exc_types, fn):
    try:
        fn()
    except exc_types:
        return
    raise AssertionError(f"expected {exc_types} to be raised")


# ---------------------------------------------------------------- detectors

def detector_T1(gs):
    records = gs.parse_records(gs.split_records(MOD(b"certification/A.json")))
    assert len(records) == 1
    assert (records[0].kind, records[0].xy, records[0].path) == ("1", ".M", "certification/A.json")
    v = verdict(gs, MOD(b"certification/A.json"))
    assert v.clean and v.allowed == ("certification/A.json",) and v.outside == ()


def detector_T2(gs):
    v = verdict(gs, MOD(b"engine/x.py"))
    assert not v.clean and v.outside == ("1 .M engine/x.py",)


def detector_T3(gs):
    v = verdict(gs, b"? reports/new.md\0")
    assert not v.clean and v.outside == ("? reports/new.md",)


def detector_T4(gs):
    v = verdict(gs, F1(b"A.", b"000000", b"100644", b"100644", Z, H, b"certification/A.json"))
    assert not v.clean and v.allowed == ()


def detector_T5(gs):
    v = verdict(gs, F1(b".D", b"100644", b"100644", b"000000", H, H, b"reports/a.md"))
    assert not v.clean and v.allowed == ()


def detector_T6(gs):
    records = gs.parse_records(gs.split_records(RENAME))
    assert len(records) == 1, records
    record = records[0]
    assert (record.kind, record.xy, record.path, record.orig_path) == (
        "2", "R.", "certification/B.json", "engine/x.py")
    assert record.fields[-1] == "R100"
    v = verdict(gs, RENAME, allow=AL | {"certification/B.json"})
    assert not v.clean and v.allowed == ()


def detector_T7(gs):
    records = gs.parse_records(gs.split_records(MOD(b"reports/a b.md")))
    assert records[0].path == "reports/a b.md"
    assert not verdict(gs, MOD(b"reports/a b.md")).clean


def detector_T7b(gs):
    records = gs.parse_records(gs.split_records(MOD(b"certification/A.json old")))
    assert records[0].path == "certification/A.json old"
    v = verdict(gs, MOD(b"certification/A.json old"))
    assert not v.clean and v.allowed == ()


def detector_T8(gs):
    raw_path = b'r/a\nb\t"c\\d\xff.md'
    records = gs.parse_records(gs.split_records(MOD(raw_path)))
    assert records[0].path == os.fsdecode(raw_path)
    assert os.fsencode(records[0].path) == raw_path
    assert not verdict(gs, MOD(raw_path)).clean


def detector_T9(gs):
    assert gs.split_records(b"") == []
    v = verdict(gs, b"")
    assert v.clean and v.allowed == () and v.outside == () and v.ignored_new == ()


def detector_T11(gs):
    expect_raises(gs.StatusParseError, lambda: verdict(gs, b"1 .M certification/A.json\0"))


def detector_T12(gs):
    path = b"engine/__pycache__/m.cpython-311.pyc"
    v = verdict(gs, b"! " + path + b"\0")
    assert not v.clean and v.ignored_new == (path.decode(),)


def detector_T12b(gs):
    path = "engine/__pycache__/m.cpython-311.pyc"
    v = verdict(gs, b"! " + path.encode() + b"\0", pre=frozenset({path}))
    assert v.clean and v.ignored_new == ()


def detector_T13(gs):
    expect_raises(gs.StatusParseError, lambda: verdict(gs, MOD(b"certification/A.json")[:-1]))


def detector_T14(gs):
    expect_raises(gs.StatusParseError, lambda: verdict(gs, b"# branch.head main\0"))
    expect_raises(gs.StatusParseError, lambda: verdict(gs, b"x foo\0"))


def detector_T15(gs):
    v = verdict(gs, MOD(b"certification/A.json.bak"))
    assert not v.clean and v.allowed == ()


def detector_T16(gs):
    v = verdict(gs, MOD(b"certification/B.json"))
    assert not v.clean and v.allowed == ()


def detector_T17(gs):
    def fake_git(argv, capture_output=True):
        return subprocess.CompletedProcess(argv, 128, b"", b"fatal: not a git repository")

    expect_raises(gs.GitStatusError,
                  lambda: gs.status_verdict("/nonexistent", AL, runner=fake_git))


def detector_T18(gs):
    raw = b"2 R. N... 100644 100644 100644 " + H + b" " + H + b" R100 certification/B.json\0"
    expect_raises(gs.StatusParseError, lambda: verdict(gs, raw))


DETECTORS = {name[len("detector_"):]: fn for name, fn in globals().items()
             if name.startswith("detector_")}


# ---------------------------------------------------------------- tests

def test_T1():
    detector_T1(gitstatus)


def test_T2():
    detector_T2(gitstatus)


def test_T3():
    detector_T3(gitstatus)


def test_T4():
    detector_T4(gitstatus)


def test_T5():
    detector_T5(gitstatus)


def test_T6():
    detector_T6(gitstatus)


def test_T7():
    detector_T7(gitstatus)


def test_T7b():
    detector_T7b(gitstatus)


def test_T8():
    detector_T8(gitstatus)


def test_T9():
    detector_T9(gitstatus)


def test_T10_old_parser_characterization():
    """The archived WP-N1 parser (wpn1_harness.py L188 `.stdout.strip()` followed by
    L310-L312 `l[3:].startswith(...)`), transcribed, reproduces the defect: the first v1
    record loses its leading status column and is misclassified as outside."""

    v1_output = " M certification/A.json\n M reports/a.md\n"
    status = v1_output.strip()                                   # archived L188
    outside = [line for line in status.splitlines()               # archived L310-L312
               if not line[3:].startswith(("certification/", "reports/"))]
    assert outside == ["M certification/A.json"]
    # The new parser classifies the equivalent v2 -z output correctly.
    v = verdict(gitstatus, MOD(b"certification/A.json") + MOD(b"reports/a.md"))
    assert v.clean and v.allowed == ("certification/A.json", "reports/a.md")


def test_T11():
    detector_T11(gitstatus)


def test_T12():
    detector_T12(gitstatus)


def test_T12b():
    detector_T12b(gitstatus)


def test_T13():
    detector_T13(gitstatus)


def test_T14():
    detector_T14(gitstatus)


def test_T15():
    detector_T15(gitstatus)


def test_T16():
    detector_T16(gitstatus)


def test_T17():
    detector_T17(gitstatus)


def test_T18():
    detector_T18(gitstatus)


def test_field_validators_reject_malformed_fields():
    bad = [
        F1(b".Z", b"100644", b"100644", b"100644", H, H, b"x"),        # XY
        F1(b".M", b"100644", b"100644", b"10064", H, H, b"x"),         # mode length
        F1(b".M", b"100644", b"100644", b"100649", H, H, b"x"),        # non-octal mode
        F1(b".M", b"100644", b"100644", b"100644", b"a" * 39, H, b"x"),  # object name
        b"1 .M X... 100644 100644 100644 " + H + b" " + H + b" x\0",   # submodule state
        b"2 R. N... 100644 100644 100644 " + H + b" " + H + b" Q100 b\0a\0",  # score
        b"? \0",                                                      # empty path
        b"1 .M N... 100644 100644 100644 " + H + b" " + H + b" a\0\0",  # empty inner token
    ]
    for raw in bad:
        expect_raises(gitstatus.StatusParseError, lambda raw=raw: verdict(gitstatus, raw))


def test_unmerged_record_is_parsed_and_outside():
    raw = (b"u UU N... 100644 100644 100644 100644 " + H + b" " + H + b" " + H
           + b" certification/A.json\0")
    records = gitstatus.parse_records(gitstatus.split_records(raw))
    assert records[0].kind == "u" and records[0].path == "certification/A.json"
    assert not verdict(gitstatus, raw).clean


def test_sha256_object_names_are_accepted():
    raw = F1(b".M", b"100644", b"100644", b"100644", b"b" * 64, b"c" * 64, b"certification/A.json")
    assert verdict(gitstatus, raw).clean


def test_git_version_meets_minimum():
    assert gitstatus.git_version() >= gitstatus.MIN_GIT_VERSION


def test_detector_registry_covers_every_specified_detector():
    expected = {"T1", "T2", "T3", "T4", "T5", "T6", "T7", "T7b", "T8", "T9", "T11", "T12",
                "T12b", "T13", "T14", "T15", "T16", "T17", "T18"}
    assert set(DETECTORS) == expected
