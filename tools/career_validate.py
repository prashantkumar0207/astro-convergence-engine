#!/usr/bin/env python3
"""Career batch validator - executable subset of CAREER_VALIDATION_CHECKLIST.md.
Runs against knowledge/hlkg/domains/career/career.questions.json (+ schema).
Exit 0 = all executable checks pass; nonzero = findings printed. Skips are failures."""
import json, re, sys, unicodedata, collections
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
REC = ROOT/"knowledge/hlkg/domains/career/career.questions.json"
SCH = ROOT/"schemas/question.schema.json"

def norm(s):
    s = unicodedata.normalize("NFKC", s).lower()
    s = re.sub(r"\s+"," ",s).strip()
    return re.sub(r"[?!.।]+$","",s).strip()

def main():
    findings=[]
    F=lambda cid,msg: findings.append(f"[{cid}] {msg}")
    recs=json.loads(REC.read_text()); S=json.loads(SCH.read_text())
    # B1 schema
    try:
        from jsonschema import Draft202012Validator
        v=Draft202012Validator(S)
        for r in recs:
            for e in v.iter_errors(r): F("VC-B1", f"{r.get('question_id')}: {e.message[:100]}")
    except ImportError:
        F("VC-B1","jsonschema not installed - MANDATORY dependency, fail not skip")
    SEG=r"[a-z0-9](?:[a-z0-9_]{0,28}[a-z0-9])?"
    ids=set(); slugs=set(); labels={}
    for r in recs:
        qid=r["question_id"]
        if qid in ids: F("VC-A1",f"dup id {qid}")
        ids.add(qid)
        if not re.fullmatch(rf"{SEG}\.{SEG}\.{SEG}", r["slug"]): F("VC-A2",f"slug {r['slug']}")
        if not r["slug"].startswith("career."): F("VC-A3",f"domain segment {r['slug']}")
        if r["slug"] in slugs: F("VC-A4",f"dup slug {r['slug']}")
        slugs.add(r["slug"])
        n=norm(r["canonical_label"])
        if n in labels: F("VC-A5",f"normalised label collision {qid} vs {labels[n]}")
        labels[n]=qid
        # C class-parameter conformance
        pnames={p["name"]:p for p in r.get("parameters",[])}
        if "subject" not in pnames or not pnames["subject"]["required"]: F("VC-D1",f"{qid} missing required subject")
        cls=r["question_class"]
        if cls=="OCCURRENCE" and not (pnames.get("horizon",{}).get("required")): F("VC-C2",f"{qid} OCCURRENCE without required horizon")
        if cls=="SELECTION" and not (pnames.get("option_set",{}).get("required")): F("VC-C3",f"{qid} SELECTION without required option_set")
        if cls=="TIMING" and "horizon" in pnames and pnames["horizon"]["required"]: F("VC-C4",f"{qid} TIMING horizon must be optional")
        for p in r.get("parameters",[]):
            if p["kind"] not in {"horizon","subject","option_set","count_threshold","locale_of_answer"}: F("VC-D2",f"{qid} unregistered kind {p['kind']}")
    # E aliases per-locale uniqueness + vs labels
    seen={}
    for r in recs:
        for a in r.get("aliases",[]):
            k=(a["locale"],norm(a["text"]))
            if k in seen and seen[k]!=r["question_id"]: F("VC-E1",f"alias collision {k} {seen[k]} vs {r['question_id']}")
            seen[k]=r["question_id"]
            if re.search(r"\b(19|20)\d\d\b", a["text"]): F("VC-E3",f"parameter value in alias: {a['text']}")
    for n,qid in labels.items():
        if ("en",n) in seen and seen[("en",n)]!=qid: F("VC-E2",f"alias equals label of {qid}")
    # F relationships
    RTYPES={"REFINES","PRECEDES","DEPENDS_ON","EXCLUDES","RELATES_TO","SUPERSEDED_BY"}
    edges=[]; pairtypes=collections.defaultdict(set)
    for r in recs:
        for e in r.get("relationships",[]):
            if e["type"] not in RTYPES: F("VC-F1",f"{r['question_id']} type {e['type']}")
            if e["target"] not in ids: F("VC-F2",f"{r['question_id']} target {e['target']} not in batch (cross-batch targets need registry check)")
            if e["target"]==r["question_id"]: F("VC-F3",f"self-edge {r['question_id']}")
            if e["type"]=="RELATES_TO" and len(e.get("rationale",""))<10: F("VC-F4",f"{r['question_id']} RELATES_TO without rationale")
            if e["type"]=="SUPERSEDED_BY" and r["lifecycle_state"] not in ("DEPRECATED","RETIRED"): F("VC-F5",f"{r['question_id']} SUPERSEDED_BY on {r['lifecycle_state']}")
            edges.append((e["type"],r["question_id"],e["target"]))
            pairtypes[frozenset((r["question_id"],e["target"]))].add(e["type"])
    if len(edges)!=len(set(edges)): F("VC-F6","duplicate edge triple")
    for k,ts in pairtypes.items():
        if {"DEPENDS_ON","PRECEDES"}<=ts: F("VC-F7",f"double-typed pair {sorted(k)}")
    for typ in ("REFINES","PRECEDES","DEPENDS_ON"):
        g=collections.defaultdict(list)
        for t,s,d in edges:
            if t==typ: g[s].append(d)
        st={}
        def dfs(n):
            st[n]=1
            for m in g[n]:
                if st.get(m)==1: F("VC-F8",f"cycle {typ} at {m}")
                elif st.get(m) is None: dfs(m)
            st[n]=2
        for n in list(g):
            if st.get(n) is None: dfs(n)
    # I lifecycle-gated
    for r in recs:
        if r["lifecycle_state"]=="CANONICAL":
            for f_ in ("definition","owner","review_status"):
                if not r.get(f_): F("VC-I2",f"{r['question_id']} CANONICAL missing {f_}")
        if not r.get("history"): F("VC-I4",f"{r['question_id']} empty history")
        if r["modified_at"]<r["created_at"]: F("VC-I5",f"{r['question_id']} timestamps")
        ra=r.get("reserved_annotations")
        if ra and any(v is not None for v in ra.values()): F("VC-I6",f"{r['question_id']} reserved field populated")
    print(f"records: {len(recs)} | executable findings: {len(findings)}")
    for f_ in findings[:40]: print(" ", f_)
    return 1 if findings else 0

if __name__=="__main__":
    sys.exit(main())
