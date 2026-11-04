#!/usr/bin/env python3
"""One-seed descriptive independent rank-upper-bound audit of original Actions trace.

Usage: python3 jpdc/audit_original_rank_dominance.py --log instrumented.log --out result.json
Do not treat 3090 task records as independent scientific replications.
"""
import argparse,csv,json,math
from collections import Counter
from pathlib import Path

POLICIES=("CASPER_FULL","CASPER_HEALTH_STATIC")

def arr(s,cast=float):
    if not (s.startswith("[") and s.endswith("]")):raise ValueError("malformed Java array")
    return [cast(x.strip()) for x in s[1:-1].split(";")]

def audit(path):
    seen={p:{} for p in POLICIES}
    with open(path,encoding="utf-8") as f:
        for line in f:
            if not line.startswith("JPDC_POLICY_DECISION,"):continue
            r=next(csv.reader([line]))
            if len(r)!=15:raise ValueError("wrong number of fields")
            tag,seed,scenario,policy,task,crit,deadline,eta,node,rank,cert,pred,alarms,sigma,qranks=r
            if scenario!="S3_HIDDEN_NETWORK_50LOSS" or policy not in POLICIES or crit!="MISSION":
                raise ValueError("invalid record identity")
            task=int(task)
            if task in seen[policy]:raise ValueError("duplicate mission task")
            pred=arr(pred);alarms=arr(alarms,lambda v:{"true":True,"false":False}[v])
            sigma=arr(sigma);qranks=arr(qranks)
            deadline=float(deadline);eta=float(eta)
            if len(pred)!=21 or len(alarms)!=21 or len(sigma)!=21 or len(qranks)!=3:
                raise ValueError("invalid candidate count")
            if not all(math.isfinite(x) for x in [*pred,*sigma,*qranks,deadline,eta]):
                raise ValueError("nonfinite input")
            if min(pred)<0 or min(sigma)<=0 or min(qranks)<0 or deadline<=0 or not 1<=eta<=3:
                raise ValueError("nonphysical input")
            family=sorted((j for j in range(21) if not alarms[j]),key=lambda j:(pred[j],j))[:3]
            if len(family)!=3:raise ValueError("not three eligible candidates")
            upper=[pred[j]+eta*qranks[k]*(3+.1*pred[j])*sigma[j] for k,j in enumerate(family)]
            first_ok=upper[0]<=deadline
            safe=next((i for i,u in enumerate(upper) if u<=deadline),None)
            expected=(family[safe if safe is not None else 0],safe+1 if safe is not None else 1,safe is not None)
            if cert not in ("true","false"):raise ValueError("malformed certificate")
            if (int(node),int(rank),cert=="true")!=expected:
                raise ValueError(f"decision parity mismatch {policy} {task}")
            seen[policy][task]=dict(seed=seed,bounds=upper,deadline=deadline,cert=cert=="true")
    if len(seen[POLICIES[0]])!=1545 or set(seen[POLICIES[0]])!=set(seen[POLICIES[1]]):
        raise ValueError("original exact 1545 mission task cohort mismatch")
    if len({v["seed"] for rows in seen.values() for v in rows.values()})!=1:
        raise ValueError("mixed seeds")
    answer={"scope":"single-seed rank bound mechanism, descriptive only",
            "source_run_id":41779874971,"source_artifact_id":13298343053,"policies":{}}
    for policy,rows in seen.items():
        gap2=[x["bounds"][1]-x["bounds"][0] for x in rows.values()]
        gap3=[x["bounds"][2]-x["bounds"][0] for x in rows.values()]
        patterns=Counter("".join("1" if u<=x["deadline"] else "0" for u in x["bounds"]) for x in rows.values())
        answer["policies"][policy]=dict(
            mission_tasks=len(rows),certificates=sum(x["cert"] for x in rows.values()),
            rank2_better_upper_count=sum(v<0 for v in gap2),
            rank3_better_upper_count=sum(v<0 for v in gap3),
            rank2_rescues=sum(x["bounds"][0]>x["deadline"]>=x["bounds"][1] for x in rows.values()),
            rank3_rescues=sum(x["bounds"][0]>x["deadline"]>=x["bounds"][2] for x in rows.values()),
            rank2_minus_rank1_min_ms=min(gap2),rank2_minus_rank1_max_ms=max(gap2),
            rank3_minus_rank1_min_ms=min(gap3),rank3_minus_rank1_max_ms=max(gap3),
            feasible_patterns=dict(sorted(patterns.items())))
    return answer

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--log",required=True);p.add_argument("--out",required=True)
    q=p.parse_args();result=audit(q.log)
    Path(q.out).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,sort_keys=True))
    print("JPDC_ORIGINAL_RANK_BOUND_AUDIT_PASS")
