#!/usr/bin/env python3
"""Audit native Cloudlet datacenter arrival and start timing; never alter prior fidelity result."""
import argparse,csv,json,math,tempfile
from pathlib import Path
from audit_native_start_forensic import audit as prior_audit

TARGET={10898,10899,10900,10901,10902}
POLICIES=("CASPER_FULL","CASPER_HEALTH_STATIC")

def audit(path):
    samples={p:{} for p in POLICIES}
    stripped=[]
    with open(path,encoding="utf-8") as file:
        for line in file:
            if not line.startswith("JPDC_FORENSIC_FINISH_DC,"):
                stripped.append(line)
                continue
            r=next(csv.reader([line]))
            if len(r)!=15:raise ValueError("wrong datacenter forensic field count")
            _,seed,scenario,policy,tid,node,workload,derived,native,dc,end,wait,service,observed,cid=r
            if scenario!="S3_HIDDEN_NETWORK_50LOSS" or policy not in POLICIES:
                raise ValueError("forensic record identity mismatch")
            tid=int(tid)
            if tid not in TARGET or tid in samples[policy]:raise ValueError("unexpected / duplicate task")
            times=list(map(float,(workload,derived,native,dc,end,wait,service,observed)))
            if not all(map(math.isfinite,times)):raise ValueError("nonfinite time")
            samples[policy][tid]={"task":tid,"node":int(node),
              "workload_arrival_ms":float(workload),"derived_start_ms":float(derived),
              "native_start_ms":float(native),"datacenter_arrival_ms":float(dc),
              "callback_clock_ms":float(end),"wait_ms":float(wait),
              "start_minus_dc_minus_wait_ms":float(native)-float(dc)-float(wait)}
            # Remove dc extra field and restore pre-existing native-finish format
            old=["JPDC_FORENSIC_FINISH_NATIVE",*r[1:9],*r[10:]]
            assert len(old)==14
            stripped.append(",".join(old)+"\n")
    if any(set(samples[p])!=TARGET for p in POLICIES):raise ValueError("missing datacenter forensic observations")
    with tempfile.TemporaryDirectory() as temp:
        oldpath=Path(temp)/"compatible_native.log"
        oldpath.write_text("".join(stripped),encoding="utf-8")
        previous=prior_audit(oldpath)
    result={"analysis":"diagnostic only; preserves original FCFS fidelity FAIL",
            "source_native_audit":{p:{"native_start_order":e["native_start_order"],"mapper_order":e["mapper_order"]}
                                   for p,e in previous["policies"].items()},
            "policies":{}}
    for p in POLICIES:
        rows=samples[p]
        order=lambda key:sorted(rows,key=lambda t:(rows[t][key],t))
        result["policies"][p]={
            "workload_arrival_order":order("workload_arrival_ms"),
            "datacenter_arrival_order":order("datacenter_arrival_ms"),
            "native_start_order":order("native_start_ms"),
            "max_abs_start_minus_dc_minus_wait_ms":max(abs(rows[t]["start_minus_dc_minus_wait_ms"]) for t in rows),
            "observations":{str(t):rows[t] for t in sorted(rows)}}
    return result

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--log",required=True);p.add_argument("--out",required=True)
    a=p.parse_args()
    r=audit(a.log)
    Path(a.out).write_text(json.dumps(r,indent=2)+"\n",encoding="utf-8")
    for pol,v in r["policies"].items():
        print(pol,"workload",v["workload_arrival_order"],
              "datacenter",v["datacenter_arrival_order"],
              "native_start",v["native_start_order"])
        for t in ("10900","10901"):
            print(pol,t,json.dumps(v["observations"][t]))
    print("JPDC_DATACENTER_ARRIVAL_FORENSIC_AUDIT_PASS")
