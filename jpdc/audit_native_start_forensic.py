#!/usr/bin/env python3
"""Check the native CloudSim start forensic file, no assumptions about native vs derived equality."""
import argparse,csv,json,math
from collections import defaultdict
from pathlib import Path
TASKS=set(range(10898,10903))
POLICIES=("CASPER_FULL","CASPER_HEALTH_STATIC")
S="S3_HIDDEN_NETWORK_50LOSS"

def audit(path):
    arrivals=defaultdict(list)
    mapped=defaultdict(dict)
    finished=defaultdict(dict)
    with open(path,encoding="utf-8") as f:
        for line in f:
            if not line.startswith(("JPDC_FORENSIC_ARRIVAL,","JPDC_FORENSIC_MAPPER,","JPDC_FORENSIC_FINISH_NATIVE,")):continue
            r=next(csv.reader([line]))
            if r[0]=="JPDC_FORENSIC_ARRIVAL":
                if len(r)!=4:raise ValueError("arrival arity")
                tid=int(r[1]);arrivals[tid].append((float(r[2]),float(r[3])))
                continue
            if r[0]=="JPDC_FORENSIC_MAPPER":
                if len(r)!=10:raise ValueError("mapper arity")
                _,seed,scenario,policy,tid,node,arr,clock,cl,vm=r
                if scenario!=S or policy not in POLICIES:raise ValueError("mapper identity")
                tid=int(tid)
                if tid in mapped[policy]:raise ValueError("duplicate mapper")
                mapped[policy][tid]=dict(seed=seed,node=int(node),arrival=float(arr),
                                          mapper=float(clock),cloudlet_id=int(cl),vm_id=int(vm))
            else:
                if len(r)!=14:raise ValueError(f"native finish arity {len(r)}")
                _,seed,scenario,policy,tid,node,arr,derived,native,end,wait,service,actual,cl=r
                if scenario!=S or policy not in POLICIES:raise ValueError("finish identity")
                tid=int(tid)
                if tid in finished[policy]:raise ValueError("duplicate finish")
                finished[policy][tid]=dict(seed=seed,node=int(node),arrival=float(arr),
                    derived_start_ms=float(derived),native_start_ms=float(native),
                    callback_clock_ms=float(end),wait_ms=float(wait),service_ms=float(service),
                    observed_latency_ms=float(actual),cloudlet_id=int(cl))
    if set(arrivals)!=TASKS or any(len(arrivals[t])!=9 for t in TASKS):
        raise ValueError("source arrival count mismatch (1 calibration + 8 deployment)")
    result={}
    for policy in POLICIES:
        if set(mapped[policy])!=TASKS or set(finished[policy])!=TASKS:
            raise ValueError("incomplete target set")
        for t in TASKS:
            m,o=mapped[policy][t],finished[policy][t]
            if m["seed"]!=o["seed"] or m["node"]!=o["node"] or m["cloudlet_id"]!=o["cloudlet_id"]:
                raise ValueError("cloudlet identity drift")
            if abs(m["arrival"]-o["arrival"])>1e-8:raise ValueError("workload arrival mismatch")
            if len([a for a,c in arrivals[t] if abs(a-m["arrival"])<1e-8 and abs(c-a)<1e-8])!=8:
                raise ValueError("unmatched deployment source event clocks")
            if abs(o["derived_start_ms"]-(o["arrival"]+o["wait_ms"]))>2e-8:
                raise ValueError("derived start arithmetic mismatch")
            if not all(math.isfinite(x) for x in (m["mapper"],o["native_start_ms"],
                    o["derived_start_ms"],o["callback_clock_ms"],o["wait_ms"],o["service_ms"])):
                raise ValueError("invalid times")
        order=lambda rows,field:sorted(TASKS,key=lambda t:(rows[t][field],t))
        result[policy]=dict(
            mapper_order=order(mapped[policy],"mapper"),
            native_start_order=order(finished[policy],"native_start_ms"),
            derived_start_order=order(finished[policy],"derived_start_ms"),
            per_task={str(t):{**mapped[policy][t],**finished[policy][t],
                "native_minus_derived_ms":finished[policy][t]["native_start_ms"]-finished[policy][t]["derived_start_ms"]}
                for t in sorted(TASKS)})
    return dict(source="actual run; native Cloudlet.getStartTime vs independently labeled derived start",
                arrivals={str(k):v for k,v in arrivals.items()},policies=result)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--log",required=True);p.add_argument("--out",required=True)
    args=p.parse_args()
    r=audit(args.log)
    Path(args.out).write_text(json.dumps(r,indent=2)+"\n",encoding="utf-8")
    for policy,entry in r["policies"].items():
        print(policy,"mapper",entry["mapper_order"],"native",entry["native_start_order"],
              "derived",entry["derived_start_order"])
        for task in ("10900","10901"):
            d=entry["per_task"][task]
            print(policy,task,"native_ms",d["native_start_ms"],"derived_ms",d["derived_start_ms"],
                  "native_minus_derived_ms",d["native_minus_derived_ms"])
    print("JPDC_NATIVE_START_FORENSIC_AUDIT_PASS")
