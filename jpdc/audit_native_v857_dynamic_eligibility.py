#!/usr/bin/env python3
"""Independent v8.5.7 dynamic eligibility + submit state auditor; no primary parser import."""
import argparse
import csv
import json
import math
from pathlib import Path

CASES = ["EARLY4_1US","EARLY4_5MS","ORIGINAL_1US","ORIGINAL_5MS","LATE10_1US","LATE10_5MS"]
BYPASS = {"ORIGINAL_5MS","LATE10_5MS"}

def ids(raw):
    values=[] if not raw else [int(z) for z in raw.split(";")]
    if len(values)!=len(set(values)) or set(values)-{0,1,2}:
        raise ValueError("invalid cloudlet list IDs")
    return values

def parse(lines):
    d={k:{"submit_before":[],"submit_after":[],"eligibility":[],"finished":set(),"complete":0} for k in CASES}
    current=None
    for line in lines:
        if not line.startswith("ARRIVALTRACE_"):continue
        row=next(csv.reader([line]))
        tag=row[0]
        if tag=="ARRIVALTRACE_CASE":
            current=row[1]
            if current not in d:raise ValueError("unexpected case")
        elif tag=="ARRIVALTRACE_CASE_DONE":
            if row[1] not in d or row[2:]!=["submissions=3","finishes=3"]:raise ValueError("incomplete case")
            d[row[1]]["complete"]+=1
        elif tag=="ARRIVALTRACE_SUBMIT":
            if len(row)!=7 or row[1] not in d:raise ValueError("bad submit")
            phase=row[2]
            if phase not in ("BEFORE","AFTER"):raise ValueError("bad phase")
            data={"time":float(row[3]),"job":int(row[4]),"exec":ids(row[5]),"wait":ids(row[6])}
            d[row[1]]["submit_before" if phase=="BEFORE" else "submit_after"].append(data)
        elif tag=="ARRIVALTRACE_ELIGIBILITY":
            if len(row)!=7 or row[1] not in d or row[4] not in ("true","false"):raise ValueError("bad eligibility callback")
            data={"time":float(row[2]),"job":int(row[3]),"eligible":row[4]=="true",
                  "exec":ids(row[5]),"wait":ids(row[6])}
            d[row[1]]["eligibility"].append(data)
        elif tag=="ARRIVALTRACE_FINISH":
            if len(row)!=8 or row[1] not in d:raise ValueError("bad finish")
            d[row[1]]["finished"].add(int(row[2]))
    out=[]
    for k,x in d.items():
        if x["complete"]!=1 or x["finished"]!={0,1,2}:raise ValueError("not all jobs completed")
        before=x["submit_before"];after=x["submit_after"]
        if len(before)!=3 or len(after)!=3 or any(a["job"]!=b["job"] or abs(a["time"]-b["time"])>1e-7 for a,b in zip(before,after)):
            raise ValueError("submit callback mismatch")
        expected_order=[0,2,1] if k.startswith("EARLY4") else [0,1,2]
        order=[e["job"] for e in before]
        if order!=expected_order:raise ValueError("unexpected actual submit order")
        eligible=x["eligibility"]
        if not eligible:raise ValueError("no dynamic eligibility callbacks observed")
        if not all(math.isfinite(e["time"]) for e in before+after+eligible):raise ValueError("nonfinite timestamp")
        for i in range(3):
            # Eligibility callbacks are counted but not assumed to be invoked for every submitted job.
            if set(before[i]["exec"])&set(before[i]["wait"]) or set(after[i]["exec"])&set(after[i]["wait"]):
                raise ValueError("overlapping native lists")
        bypass=[]
        accepted=set()
        for b,a in zip(before,after):
            # Only accepted earlier cloudlets count as older WAIT.
            if b["job"]!=a["job"]:raise ValueError("submission changed identity")
            old_wait=set(b["wait"])&accepted
            if a["job"] in a["exec"] and old_wait&set(a["wait"]):
                bypass.append(a["job"])
            accepted.add(a["job"])
        if bool(bypass)!=(k in BYPASS):raise ValueError("unexpected bypass case")
        submitted_target=[e for e in eligible if e["job"]==2]
        out.append({"case":k,"submit_order":order,"eligibility_callback_count":len(eligible),
                    "job2_eligibility_values":[e["eligible"] for e in submitted_target],
                    "job2_eligibility_saw_older_wait":any(1 in e["wait"] for e in submitted_target),
                    "direct_submit_bypass":bool(bypass)})
    return {"status":"PASS","actual_native_cases":6,"native_cloudlets_finished":18,
            "eligibility_callbacks_dynamically_observed":sum(x["eligibility_callback_count"] for x in out),
            "bypass_cases":[x["case"] for x in out if x["direct_submit_bypass"]],
            "publisher_version":"8.5.7","stage65_safety":"FAIL",
            "original_30k_java_python_parity":"FAIL","cases":out}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--trace",required=True);p.add_argument("--out",required=True)
    a=p.parse_args()
    report=parse(Path(a.trace).read_text().splitlines())
    Path(a.out).write_text(json.dumps(report,sort_keys=True,indent=2)+"\n")
    print("JPDC_NATIVE_DYNAMIC_ELIGIBILITY_AUDIT",json.dumps({k:v for k,v in report.items() if k!="cases"},sort_keys=True))
if __name__=="__main__":main()
