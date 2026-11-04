#!/usr/bin/env python3
"""Recompute ranked mission choices from original unmodified E45 input snapshots.

Descriptive seed-level rank usage; NOT an independent simulator or efficacy claim.
"""
import argparse,csv,json,math
from collections import Counter
from pathlib import Path
from replay_casper_mission_decisions import replay, array, POLS, FIELDS

def analyze(path, expected_seed):
    data={p:{} for p in POLS}
    seeds=set()
    with open(path,encoding="utf-8") as f:
        for line in f:
            if not line.startswith("JPDC_POLICY_DECISION,"):continue
            values=next(csv.reader([line]))
            if len(values)!=len(FIELDS):raise ValueError("field count mismatch")
            r=dict(zip(FIELDS,values))
            if r["scenario"]!="S3_HIDDEN_NETWORK_50LOSS" or r["policy"] not in POLS or r["crit"]!="MISSION":
                raise ValueError("unexpected scientific identity")
            seed=int(r["seed"]);seeds.add(seed)
            tid=int(r["task"])
            if not 0<=tid<30000 or tid in data[r["policy"]]:raise ValueError("duplicate or bad task")
            pred=array(r["pred"]);alarm=array(r["alarms"],lambda x:{"true":True,"false":False}[x])
            sigma=array(r["sigma"]);q=array(r["qrank"])
            deadline=float(r["deadline"]);eta=float(r["eta"])
            if len(pred)!=21 or len(alarm)!=21 or len(sigma)!=21 or len(q)!=3:raise ValueError("array length")
            if not all(math.isfinite(x) for x in [*pred,*sigma,*q,deadline,eta]):raise ValueError("nonfinite")
            if min(pred)<0 or min(sigma)<=0 or min(q)<0 or deadline<=0 or not 1<=eta<=3:
                raise ValueError("nonphysical")
            expected=replay(pred,alarm,sigma,q,deadline,eta)
            if r["cert"] not in ("true","false"):raise ValueError("boolean")
            actual=(int(r["node"]),int(r["rank"]),r["cert"]=="true")
            if expected!=actual:raise ValueError(f"Java/Python decision mismatch {r['policy']} task{tid}")
            nodes=sorted((i for i in range(21) if not alarm[i]),key=lambda i:(pred[i],i))[:3]
            upper=[pred[n]+eta*q[k]*(3+.1*pred[n])*sigma[n] for k,n in enumerate(nodes)]
            if len(nodes)!=3:raise ValueError("fewer than 3 eligible; report separately if observed")
            data[r["policy"]][tid]={"rank":actual[1],"cert":actual[2],"upper":upper,
                                  "deadline":deadline,"q":q}
    if seeds!={4_202_202_600+expected_seed}:raise ValueError(f"seed mismatch {seeds}")
    if len(data[POLS[0]])<250 or set(data[POLS[0]])!=set(data[POLS[1]]):
        raise ValueError("mission cohort mismatch")
    results={"seed_index":expected_seed,"scientific_seed":next(iter(seeds)),"policies":{}}
    for p,rows in data.items():
        values=list(rows.values())
        gaps2=[r["upper"][1]-r["upper"][0] for r in values]
        gaps3=[r["upper"][2]-r["upper"][0] for r in values]
        ranks=Counter(v["rank"] for v in values)
        pats=Counter("".join("1" if u<=r["deadline"] else "0" for u in r["upper"]) for r in values)
        q_orders=Counter("".join("1" if r["q"][k]>=r["q"][0] else "0" for k in (1,2)) for r in values)
        results["policies"][p]={
            "mission_n":len(values),"post_mission_n":sum(t>=10000 for t in rows),
            "ranks":{str(k):ranks[k] for k in (1,2,3)},
            "certified":sum(v["cert"] for v in values),
            "rank2_rescues":sum(r["upper"][0]>r["deadline"]>=r["upper"][1] for r in values),
            "rank3_rescues":sum(r["upper"][0]>r["deadline"]>=r["upper"][2] for r in values),
            "rank2_bound_below_first":sum(g<-1e-10 for g in gaps2),
            "rank3_bound_below_first":sum(g<-1e-10 for g in gaps3),
            "min_gap_rank2_ms":min(gaps2),"min_gap_rank3_ms":min(gaps3),
            "feasible_patterns":dict(sorted(pats.items())),
            "q_relations":dict(sorted(q_orders.items()))
        }
    return results

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--log",required=True);p.add_argument("--out",required=True);p.add_argument("--seed-index",type=int,required=True)
    a=p.parse_args();r=analyze(a.log,a.seed_index)
    Path(a.out).write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(r,indent=2,sort_keys=True))
    print("JPDC_FROZEN_RANK_UTILIZATION_SCREEN_PASS")
