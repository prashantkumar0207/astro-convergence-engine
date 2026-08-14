# Decision-paper identifier-family gate (ADR-0040).
from __future__ import annotations
import re, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "decisions" / "README.md"
DP_RE = re.compile(r"(?<![A-Za-z0-9_])DP-(\d{3})(?!\d)")
def tracked_files():
    out = subprocess.run(["git","ls-files"], cwd=ROOT, capture_output=True, text=True, check=True)
    return [x for x in out.stdout.splitlines() if x]
def registered_ids(text):
    return re.findall(r"^\|\s*(DP-\d{3})\s*\|", text, re.MULTILINE)
def main():
    try: index = INDEX.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"FAIL: cannot read decision-paper index: {exc}"); return 2
    ids = registered_ids(index)
    dup = sorted({x for x in ids if ids.count(x) > 1})
    if dup:
        print(f"FAIL: duplicate DP allocations: {dup}"); return 1
    registered = set(ids); hits = []
    for rel in tracked_files():
        p = ROOT / rel
        try: text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError): continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for m in DP_RE.finditer(line):
                if m.group(0) not in registered:
                    hits.append(f"{rel}:{lineno}: {m.group(0)}")
    if hits:
        print("FAIL: unregistered decision-paper identifiers:")
        for hit in hits: print("  ", hit)
        return 1
    print(f"PASS: {len(registered)} registered DP identifiers; no unregistered tokens.")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
