#!/usr/bin/env python3
"""Audits exact A1 six-case passive wait-promotion source hook trace.

Requires separate byte-for-byte control equivalence in CI. This script alone
does NOT demonstrate a library defect, physical CPU start or causal effect.
"""
import argparse,csv,json,collections
from pathlib import Path
def split_ids(s):
    return set() if not s else set(s.split(";"))
def audit(path):
    cases=collections.defaultdict(lambda:{"calls":[],"paired":[],"submissions":[],"updates":[]})
    for line in path.read_text().splitlines():
        if not line.startswith("ARRIVALTRACE_"):continue
        row=next(csv.reader([line]));kind=row[0]
        if kind not in ("ARRIVALTRACE_PROMOTION","ARRIVALTRACE_SUBMIT","ARRIVALTRACE_UPDATE"):continue
        name=row[1];assert name in (
         "EARLY4_1US","EARLY4_5MS","ORIGINAL_1US","ORIGINAL_5MS","LATE10_1US","LATE10_5MS")
        g=cases[name]
        if kind=="ARRIVALTRACE_PROMOTION":
            if row[2]=="BEFORE":
                g["calls"].append(row)
            else:
                assert row[2]=="AFTER" and g["calls"]
                before=g["calls"].pop()
                assert before[2]=="BEFORE" and before[3]==row[3]
                bx,bw=split_ids(before[4]),split_ids(before[5])
                ax,aw=split_ids(row[4]),split_ids(row[5])
                g["paired"].append({"clock_ms":float(row[3]),"exec_before":sorted(bx),
                  "wait_before":sorted(bw),"exec_after":sorted(ax),
                  "wait_after":sorted(aw),
                  "promoted_ids":sorted((bw-aw)&ax),
                  "exec_added_ids":sorted(ax-bx),
                  "wait_removed_ids":sorted(bw-aw)})
        elif kind=="ARRIVALTRACE_SUBMIT":
            g["submissions"].append(row)
        elif kind=="ARRIVALTRACE_UPDATE":
            g["updates"].append(row)
    assert len(cases)==6
    for name,g in cases.items():
        assert not g["calls"]
        assert len([x for x in g["submissions"] if x[2]=="BEFORE"])==3
        assert len([x for x in g["submissions"] if x[2]=="AFTER"])==3
        assert len(g["paired"])>=0
    result={
      "status":"PASS_SOURCE_VERIFIED_PASSIVE_PROMOTION_TRACE",
      "cases":6,
      "promotion_hook_invocations":sum(len(g["paired"]) for g in cases.values()),
      "promotion_with_observed_wait_to_exec":sum(bool(x["promoted_ids"]) for g in cases.values() for x in g["paired"]),
      "observed_promoted_cloudlet_ids_by_case":{name:[{"clock_ms":q["clock_ms"],"ids":q["promoted_ids"]} for q in v["paired"] if q["promoted_ids"]] for name,v in sorted(cases.items())},
      "promotion_call_counts_by_case":{name:len(v["paired"]) for name,v in sorted(cases.items())},
      "interpretation":"Method-hook before-after list observations, not physical CPU starts or proof of error.",
      "instrumentation_byte_equal_control_must_be_verified_separately":True,
      "observational_only":True,
      "original_30k_crossruntime_parity":"FAIL",
      "stage65_safety":"FAIL"}
    return result
if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--trace",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    a=ap.parse_args()
    res=audit(a.trace)
    a.out.write_text(json.dumps(res,sort_keys=True,indent=2)+"\n")
    print(json.dumps(res,sort_keys=True,indent=2))
