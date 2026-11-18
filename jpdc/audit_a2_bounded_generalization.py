#!/usr/bin/env python3
"""Audit prospective actual native A2 24-case cloudlet results against FIFO m-server reference."""
import argparse
import csv
import json
import math
from pathlib import Path

SERVICE=[8,13,5,19,7,11,17,6,14,9,16,10]
EXPECTED={f"{family}_S{seed}_{gap}_P{pes}" for family in ("STAGGERED","BURSTY")
          for seed in range(3) for gap in ("1US","5MS") for pes in (1,2)}
JITTER=[[0]*12,[0,.4,.8]*4,[.8,.4,0]*4]
def parse(path):
    data={k:{"header":[],"done":[],"before":[],"after":[],"finish":{}} for k in EXPECTED}
    trailer=0
    for line in Path(path).read_text().splitlines():
        if line=="JPDC_A2_NATIVE_24_CASES_COMPLETE":
            trailer+=1;continue
        if not line.startswith("A2_"):continue
        r=next(csv.reader([line]));tag=r[0]
        if len(r)<2 or r[1] not in data:raise ValueError("unknown case")
        d=data[r[1]]
        if tag=="A2_CASE":
            if len(r)!=6:raise ValueError("bad case")
            d["header"].append(r)
        elif tag=="A2_DONE":
            if len(r)!=3 or r[2]!="12":raise ValueError("incomplete case")
            d["done"].append(r)
        elif tag=="A2_SUBMIT":
            if len(r)!=7 or r[2] not in ("BEFORE","AFTER"):raise ValueError("bad submit")
            job=int(r[4]);when=float(r[3])
            if job not in range(12) or not math.isfinite(when):raise ValueError("bad job/time")
            x={"id":job,"when":when,"exec":r[5],"wait":r[6]}
            d["before" if r[2]=="BEFORE" else "after"].append(x)
        elif tag=="A2_FINISH":
            if len(r)!=9:raise ValueError("bad finish")
            idx=int(r[2]);native=int(r[3]);values=[float(z) for z in r[4:]]
            if idx not in range(12) or native!=idx or idx in d["finish"] or not all(map(math.isfinite,values)):
                raise ValueError("invalid finish")
            d["finish"][idx]=values
        else:raise ValueError("unexpected native event")
    if trailer!=1:raise ValueError("no successful complete trailer")
    return data

def audit(data):
    results=[]
    for case in sorted(EXPECTED):
        d=data[case]
        if len(d["header"])!=1 or len(d["done"])!=1 or len(d["before"])!=12 or len(d["after"])!=12 or set(d["finish"])!=set(range(12)):
            raise ValueError("case conservation "+case)
        _,header_case,family,seedstr,gapstr,pestr=d["header"][0]
        if header_case != case: raise ValueError("header case key mismatch")
        seed=int(seedstr);gap=float(gapstr);pes=int(pestr)
        if (family,seed,gap,pes)!=(case.split("_")[0],int(case.split("_")[1][1:]),.000001 if "1US" in case else .005,int(case.split("_")[-1][1:])):
            raise ValueError("header factors differ from case key")
        order=[]
        for b,a in zip(d["before"],d["after"]):
            if b["id"]!=a["id"] or abs(b["when"]-a["when"])>1e-7:
                raise ValueError("bad paired submit callbacks")
            order.append(a["id"])
        if set(order)!=set(range(12)):raise ValueError("duplicate submit IDs")
        # Actual observed native SUBMIT AFTER order is the FIFO tie-breaker.
        free=[d["after"][0]["when"]]*pes
        errors=[];deadline25=deadline50=disagree25=disagree50=0
        for entry in d["after"]:
            job=entry["id"];arrival=entry["when"]
            index=min(range(pes),key=lambda j:(free[j],j))
            refstart=max(arrival,free[index]);refwait=refstart-arrival
            reffinish=refstart+SERVICE[job];free[index]=reffinish
            finish,wait,actual_service,nominal_arr,requested_service=d["finish"][job]
            expected_arr=(3*job if family=="STAGGERED" else 12*(job//3))+JITTER[seed][job]
            if abs(requested_service-SERVICE[job])>1e-7 or abs(nominal_arr-expected_arr)>1e-7:
                raise ValueError("source values changed")
            if wait < -1e-7 or actual_service < -1e-7 or finish < arrival -1e-7:
                raise ValueError("unphysical basic accounting")
            if abs((finish-arrival)-(wait+actual_service))>1e-5:
                raise ValueError("native finish != wait + reported service")
            errors.append(wait-refwait)
            for margin in (25,50):
                n=finish>arrival+margin+1e-8
                q=reffinish>arrival+margin+1e-8
                if margin==25:
                    deadline25+=int(n);disagree25+=int(n!=q)
                else:
                    deadline50+=int(n);disagree50+=int(n!=q)
        results.append({"case":case,"family":family,"variant":seed,"event_gap_sec":gap,"pes":pes,
                        "actual_submit_order":order,"finished":12,
                        "max_abs_wait_discrepancy_ms":round(max(map(abs,errors)),9),
                        "mean_abs_wait_discrepancy_ms":round(sum(map(abs,errors))/12,9),
                        "mean_signed_wait_discrepancy_ms":round(sum(errors)/12,9),
                        "native_missed_arrival_plus_25ms":deadline25,"native_missed_arrival_plus_50ms":deadline50,
                        "native_reference_deadline_disagreements_25ms":disagree25,
                        "native_reference_deadline_disagreements_50ms":disagree50})
    return {"status":"PASS","native_cases":24,"finished_cloudlets":288,
            "real_world_workload":False,"crossruntime_parity_original":"FAIL","stage65_safety_original":"FAIL",
            "results":results}
def main():
    p=argparse.ArgumentParser();p.add_argument("--native",required=True);p.add_argument("--out",required=True)
    a=p.parse_args()
    report=audit(parse(a.native))
    Path(a.out).write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print("JPDC_A2_AUDIT",json.dumps({k:v for k,v in report.items() if k!="results"},sort_keys=True))
if __name__=="__main__":main()
