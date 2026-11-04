#!/usr/bin/env python3
"""Reconcile actual SpaceShared before/after cloudletSubmit snapshots.

Nine episode blocks expected: one calibration and eight E45 deployment policies.
The original registered 5-ms max-wait fidelity FAILURE remains unchanged.
"""
import argparse,csv,json
from collections import defaultdict
from pathlib import Path

POLICIES=["CALIBRATION","CLOUD_ONLY","EDGE_FIRST","PRED_GREEDY","GLOBAL_CP",
          "RANKED_CP_STATIC","CASPER_ADAPT_NO_HEALTH","CASPER_HEALTH_STATIC","CASPER_FULL"]
TARGET=set(range(10898,10903))
def parse(log):
    stages=[]
    snapshots=[]
    with open(log,encoding="utf-8") as f:
        for line in f:
            if line.startswith("JPDC_SCHEDULER_SUBMIT,"):
                r=next(csv.reader([line]))
                if len(r)!=8:raise ValueError(f"unexpected scheduler snapshot arity: {len(r)}")
                _,phase,clock,vm,cloudlet,transfer,running,waiting=r
                if phase not in ("BEFORE","AFTER") or int(cloudlet) not in TARGET:
                    raise ValueError("incorrect scheduler snapshot")
                snapshots.append(dict(phase=phase,clock_ms=float(clock),vm=int(vm),
                    id=int(cloudlet),file_transfer_ms=float(transfer),
                    running=running,waiting=waiting))
            elif line.startswith("JPDC_FORENSIC_MAPPER,"):
                r=next(csv.reader([line]))
                if len(r)!=10:raise ValueError("mapper field count")
                if r[3] in ("CASPER_FULL","CASPER_HEALTH_STATIC"):
                    stages.append(dict(policy=r[3],id=int(r[4]),node=int(r[5]),clock=float(r[7])))
    before=[s for s in snapshots if s["phase"]=="BEFORE"]
    after=[s for s in snapshots if s["phase"]=="AFTER"]
    if len(before)!=9*len(TARGET) or len(after)!=9*len(TARGET):
        raise ValueError(f"expected 9x5 pre/post snapshots, got {len(before)}/{len(after)}")
    episodes=[]
    for i,policy in enumerate(POLICIES):
        b=before[i*5:(i+1)*5]
        a=after[i*5:(i+1)*5]
        if {x["id"] for x in b}!=TARGET or {x["id"] for x in a}!=TARGET:
            raise ValueError(f"incomplete episode {policy}")
        if set(x["id"] for x in b)!=set(x["id"] for x in a):
            raise ValueError("pre/post identity mismatch")
        for k in TARGET:
            before_row=next(x for x in b if x["id"]==k)
            after_row=next(x for x in a if x["id"]==k)
            if before_row["vm"]!=after_row["vm"] or abs(before_row["clock_ms"]-after_row["clock_ms"])>1e-8:
                raise ValueError("mutated event clock during scheduler call")
        episodes.append(dict(episode=i,policy=policy,
            submission_order=[x["id"] for x in b],
            node14_pair=[{k:v for k,v in x.items()} for x in b+a if x["id"] in (10900,10901)]))
    for p in ("CASPER_HEALTH_STATIC","CASPER_FULL"):
        selected=[x for x in stages if x["policy"]==p]
        if {x["id"] for x in selected}!=TARGET:raise ValueError(f"missing mapper {p}")
        episode=next(x for x in episodes if x["policy"]==p)
        assert len(episode["node14_pair"])==4
    return dict(scope="scheduler call order, not proof of internal VM event causation",
                original_fcfs_fidelity="FAIL max 9.1214 ms >5 ms",
                episode_count=len(episodes),snapshots=len(snapshots),episodes=episodes)
if __name__=="__main__":
    a=argparse.ArgumentParser();a.add_argument("--log",required=True);a.add_argument("--out",required=True)
    q=a.parse_args();r=parse(q.log)
    Path(q.out).write_text(json.dumps(r,indent=2)+"\n",encoding="utf-8")
    for x in r["episodes"]:
        if x["policy"] in ("CASPER_FULL","CASPER_HEALTH_STATIC"):
            print(x["policy"],"scheduler_submit_order",x["submission_order"],
                "target_node14_snapshots",json.dumps(x["node14_pair"]))
    print("JPDC_SCHEDULER_SUBMISSION_FORENSIC_AUDIT_PASS")
