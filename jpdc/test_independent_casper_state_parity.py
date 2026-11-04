#!/usr/bin/env python3
"""Independent Python cross-language comparison with frozen Java state harness."""
import argparse,csv,math
from pathlib import Path
from independent_casper_state import DualMemory, NodeHealth, VirtualQueue

def close(a,b,label):
    if not math.isfinite(float(a)) or not math.isclose(float(a),float(b),rel_tol=0,abs_tol=1e-10):
        raise ValueError(f"{label}: expected {b} got {a}")

def validate(path):
    with open(path,encoding="utf-8") as f:
        lines=[row for row in csv.reader(f) if row and (row[0] in ("STATE_E17","STATE_HEALTH","STATE_QUEUE"))]
    expected_counts={"STATE_E17":601,"STATE_HEALTH":360,"STATE_QUEUE":180}
    counts={k:0 for k in expected_counts}
    reference=[0.50+((i*37)%101)/100 for i in range(300)]
    m=DualMemory(reference)
    h=[NodeHealth(1.10),NodeHealth(1.40)]
    q=VirtualQueue(3)
    stage={"STATE_E17":0,"STATE_HEALTH":1,"STATE_QUEUE":2}
    last=-1
    for r in lines:
        name=r[0]
        if name not in stage:raise ValueError("unknown state reference type")
        if stage[name]<last:raise ValueError("stage order changed")
        last=stage[name]
        idx=counts[name]
        if name=="STATE_E17":
            if len(r)!=6 or int(r[1])!=idx:raise ValueError("E17 sequence/cardinality")
            close(r[2],m.eta_before_outcome(),"eta at t="+str(idx))
            if r[3] != str(m.alarm_ever).lower():raise ValueError(f"E17 alarm {idx}")
            if int(r[4]) != m.transition_age:raise ValueError(f"E17 transition age {idx}")
            close(r[5],m.reference_q95,"reference Q95")
            if idx<600:
                score=(.65+((idx*17)%23)/100 if idx<150
                       else 2.50+((idx*29)%31)/100 if idx<330
                       else .80+((idx*13)%19)/100)
                m.observe(score)
        elif name=="STATE_HEALTH":
            if len(r)!=4:raise ValueError("health columns")
            t=idx//2;node=idx%2
            if int(r[1])!=node or int(r[2])!=t:raise ValueError("health order")
            ratio=.80+((t*11+node*7)%17)/10
            alarm=h[node].observe(ratio*10,10)
            if r[3]!=str(alarm).lower():raise ValueError(f"health mismatch node{node} t{t}")
        else:
            if len(r)!=9:raise ValueError("queue columns")
            t=idx
            if int(r[1])!=t:raise ValueError("queue order")
            now=t*2.5
            close(r[2],now,"queue now")
            if t%20==0:q.reset_from_telemetry([now+5*(j+1) for j in range(3)])
            before=[q.predicted_backlog(j,now) for j in range(3)]
            for j in range(3):close(r[3+j],before[j],f"queue backlog t{t} node{j}")
            node=(t*7)%3
            q.on_dispatch(node,now,2+(t%11)*.25)
            for j in range(3):close(r[6+j],q.next_free[j],f"queue free t{t} node{j}")
        counts[name]+=1
    if counts!=expected_counts:
        raise ValueError(f"incomplete records: {counts}")
    with open(path,encoding="utf-8") as f:
        if sum(line.strip()=="STATE_REFERENCE_COMPLETE" for line in f)!=1:
            raise ValueError("missing or duplicate Java harness completion")
    if not m.alarm_ever or m.transition_age<200:raise ValueError("E17 synthetic shift coverage missing")
    if not all(x.alarmed for x in h):raise ValueError("health alarm never triggered")
    return counts

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--java-output",required=True)
    a=p.parse_args();result=validate(Path(a.java_output))
    print("PASS E17: ",result["STATE_E17"],"recorded states including detector+fast/slow+transition")
    print("PASS HEALTH:",result["STATE_HEALTH"],"observations across two alarm thresholds")
    print("PASS QUEUE:",result["STATE_QUEUE"],"telemetry resets + pre/post dispatch")
    print("JPDC_INDEPENDENT_CASPER_STATE_PARITY_PASS")
