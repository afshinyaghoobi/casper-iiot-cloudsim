#!/usr/bin/env python3
"""Second A2 validator: independent raw CSV pass, not importing the primary auditor."""
import argparse,csv,json,math
from pathlib import Path
S=(8.,13.,5.,19.,7.,11.,17.,6.,14.,9.,16.,10.)
def check(native,primary):
    allrows={}
    case_headers=set()
    cases_done=set()
    end_count=0
    for line in Path(native).read_text().splitlines():
        if line=="JPDC_A2_NATIVE_24_CASES_COMPLETE":
            end_count+=1;continue
        if not line.startswith("A2_"):continue
        p=next(csv.reader([line]))
        if p[0]=="A2_CASE":
            name=p[1];case_headers.add(name)
        elif p[0]=="A2_DONE":
            if int(p[2])!=12:raise AssertionError("missing jobs")
            cases_done.add(p[1])
        elif p[0]=="A2_SUBMIT" and p[2]=="AFTER":
            allrows.setdefault(p[1],{"submit":[],"finish":{}})["submit"].append((int(p[4]),float(p[3])))
        elif p[0]=="A2_FINISH":
            allrows.setdefault(p[1],{"submit":[],"finish":{}})["finish"][int(p[2])]=tuple(float(x) for x in p[4:])
    report=json.loads(Path(primary).read_text())
    if end_count!=1 or set(allrows)!=case_headers or cases_done!=case_headers or len(allrows)!=24:
        raise AssertionError("case count mismatch")
    if report["native_cases"]!=24 or report["finished_cloudlets"]!=288:raise AssertionError("primary misleading count")
    primaryrows={x["case"]:x for x in report["results"]}
    if set(primaryrows)!=set(allrows):raise AssertionError("unmatched matrix")
    maxdiff=0
    total_elig=0
    for name,raw in allrows.items():
        reported=primaryrows[name]
        c=int(name.rsplit("_P",1)[1])
        records=raw["submit"]
        if len(records)!=12 or set(j for j,_ in records)!=set(range(12)):
            raise AssertionError("bad job list")
        if len(raw["finish"])!=12:raise AssertionError("missing finish")
        # Explicit independent FIFO computation: server_end is next time each server frees.
        server_end=[records[0][1] for _ in range(c)]
        wait_errors=[]
        miss={25:[0,0],50:[0,0]}
        for job,t in records:
            server=sorted(enumerate(server_end),key=lambda item:(item[1],item[0]))[0][0]
            start=t if server_end[server]<t else server_end[server]
            server_end[server]=start+S[job]
            rec=raw["finish"][job]
            native_finish,native_wait,native_exec=rec[:3]
            wait_errors.append(native_wait-(start-t))
            for margin in (25,50):
                native_bad=native_finish>t+margin+1e-8
                reference_bad=server_end[server]>t+margin+1e-8
                miss[margin][0]+=native_bad
                miss[margin][1]+=native_bad!=reference_bad
        max_gap=max(abs(x) for x in wait_errors)
        if abs(max_gap-reported["max_abs_wait_discrepancy_ms"])>1e-6:
            raise AssertionError("primary worst wait disagrees")
        if abs(sum(abs(x) for x in wait_errors)/12-reported["mean_abs_wait_discrepancy_ms"])>1e-6:
            raise AssertionError("primary mean wait disagrees")
        for margin in (25,50):
            if miss[margin] != [reported[f"native_missed_arrival_plus_{margin}ms"],reported[f"native_reference_deadline_disagreements_{margin}ms"]]:
                raise AssertionError("deadline mismatch")
        maxdiff=max(maxdiff,max_gap)
        total_elig+=len(records)
    return {"status":"PASS","cases":len(allrows),"cloudlets":total_elig,
            "max_abs_wait_delta_across_case_ms":round(maxdiff,9),
            "primary_audit_confirmed":True,"native_synthetic_only":True}
def main():
    p=argparse.ArgumentParser();p.add_argument("--native",required=True);p.add_argument("--primary",required=True);p.add_argument("--out",required=True)
    a=p.parse_args()
    report=check(a.native,a.primary)
    Path(a.out).write_text(json.dumps(report,sort_keys=True,indent=2)+"\n")
    print("JPDC_A2_INDEPENDENT_AUDIT",json.dumps(report,sort_keys=True))
if __name__=="__main__":main()
