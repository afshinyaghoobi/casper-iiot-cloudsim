#!/usr/bin/env python3
"""Independent qRank, qGlobal, and health thresholds from real CloudSim score inputs.

The score events are Java-sourced physical outcomes. The qhat aggregation
and calibration-rank schedule are independent Python implementations.
"""
import argparse,csv,json,math
from pathlib import Path
from independent_workload_generator import calibration_mission_ranks,conformal_qhat

SCI_SEED=4202202640
RANK_ALPHA=(.006,.003,.001)
HEALTH_ALPHA=.01

def parse_array(value,cast=float):
    if not(value.startswith("[") and value.endswith("]")):raise ValueError("bad array brackets")
    values=[x.strip() for x in value[1:-1].split(";")]
    if len(values)!=3:raise ValueError("array length not 3")
    return [cast(v) for v in values]

def approx(a,b,name):
    if math.isinf(a) and math.isinf(b) and a>0 and b>0:return
    if not math.isfinite(a) or not math.isfinite(b) or not math.isclose(a,b,abs_tol=1e-10,rel_tol=0):
        raise ValueError(f"{name}: Java {a}, Python {b}")

def audit(log):
    mission_by_task=calibration_mission_ranks(SCI_SEED,80000,10000)
    mission={};service={};summary=None
    for line in Path(log).open(encoding="utf-8"):
        if not line.startswith(("JPDC_CAL_REAL_SERVICE,","JPDC_CAL_REAL_MISSION,","JPDC_CAL_REAL_SUMMARY,")):
            continue
        row=next(csv.reader([line]))
        tag=row[0]
        if tag=="JPDC_CAL_REAL_SERVICE":
            if len(row)!=6:raise ValueError("invalid service fields")
            _,seed,t,node,tier,value=row
            if int(seed)!=SCI_SEED:raise ValueError("service seed")
            t=int(t);node=int(node);tier=int(tier);ratio=float(value)
            expected_tier=0 if node<12 else 1 if node<18 else 2
            if t in service or not 10000<=t<80000 or not 0<=node<21 or tier!=expected_tier:
                raise ValueError("service identity/duplicate")
            if not math.isfinite(ratio) or ratio<=0:raise ValueError("nonphysical service ratio")
            service[t]=(node,tier,ratio)
        elif tag=="JPDC_CAL_REAL_MISSION":
            if len(row)!=6:raise ValueError("invalid mission fields")
            _,seed,t,rank,node,score=row
            if int(seed)!=SCI_SEED:raise ValueError("mission seed")
            t=int(t);rank=int(rank);node=int(node);score=float(score)
            if t in mission or t not in mission_by_task or rank!=mission_by_task[t] or not 0<=node<21:
                raise ValueError("mission rank/identity/duplicate mismatch")
            if not math.isfinite(score) or score<0:raise ValueError("invalid nonconformity score")
            mission[t]=(rank,node,score)
        elif tag=="JPDC_CAL_REAL_SUMMARY":
            if len(row)!=7 or summary is not None:raise ValueError("summary columns/duplicate")
            if int(row[1])!=SCI_SEED:raise ValueError("summary seed")
            summary=dict(q_rank=parse_array(row[2]),q_global=float(row[3]),
                         service_thresholds=parse_array(row[4]),
                         rank_counts=parse_array(row[5],int),tier_counts=parse_array(row[6],int))
    if len(service)!=70000 or set(service)!=set(range(10000,80000)):
        raise ValueError(f"service incomplete {len(service)}/70000")
    if set(mission)!=set(mission_by_task):
        raise ValueError(f"mission score coverage mismatch actual={len(mission)} expected={len(mission_by_task)}")
    for t,(_,node,_) in mission.items():
        if service[t][0]!=node:raise ValueError(f"mission service-node mismatch {t}")
    if summary is None:raise ValueError("missing calibration summary")
    rank_scores=[[v[2] for v in mission.values() if v[0]==rank] for rank in (1,2,3)]
    all_scores=[v[2] for v in mission.values()]
    tier_scores=[[v[2] for v in service.values() if v[1]==tier] for tier in range(3)]
    original_counts=[len(vals) for vals in rank_scores]
    tier_counts=[len(vals) for vals in tier_scores]
    if original_counts!=summary["rank_counts"] or tier_counts!=summary["tier_counts"]:
        raise ValueError("summary cohort count mismatch")
    computed_rank=[conformal_qhat(rank_scores[i],RANK_ALPHA[i]) for i in range(3)]
    computed_global=conformal_qhat(all_scores,.01)
    computed_tier=[conformal_qhat(s,.01) for s in tier_scores]
    for i,(a,b) in enumerate(zip(summary["q_rank"],computed_rank)):
        approx(a,b,f"qRank[{i+1}]")
    approx(summary["q_global"],computed_global,"qGlobal")
    for i,(a,b) in enumerate(zip(summary["service_thresholds"],computed_tier)):
        approx(a,b,f"serviceTierThreshold[{i}]")
    return {
        "scientific_seed":SCI_SEED,"calibration_tasks":80000,
        "post_burnin_service_ratios":len(service),"mission_scores":len(mission),
        "rank_counts":original_counts,"tier_counts":tier_counts,
        "independent_q_rank":computed_rank,"independent_q_global":computed_global,
        "independent_health_thresholds":computed_tier,
        "calibration_reference":"Java native CloudSim finished-task score and service inputs",
        "independent_component":"Python rank schedule and conformal qhat aggregation",
        "status":"PASS"
    }

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--log",required=True)
    p.add_argument("--out",required=True)
    args=p.parse_args()
    result=audit(args.log)
    Path(args.out).write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
    print("JPDC_REAL_CALIBRATION_INDEPENDENT_QHAT_PASS")
