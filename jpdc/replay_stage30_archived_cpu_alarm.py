#!/usr/bin/env python3
"""Stage30 fixed causal CPU change alarm on immutable Stage27 DEVELOPMENT seed90.

This is not a physical policy run, independent confirmation, calibrated false
alarm control, or an improvement to original Stage28 conditional coverage.
"""
import argparse,json,math
from collections import defaultdict
from pathlib import Path
from causal_cpu_shift_guard_stage30 import CausalCpuShiftGuard

def run_one(trace):
    truth={}
    events=[]
    for r in trace:
        i=r["task_index"]
        if i in truth:raise AssertionError("duplicate immutable task")
        truth[i]=r
        events.append((r["arrival_ms"],2,i))
        events.append((r["delivered_cpu_finish_ms"],0,i))
    assert len(truth)==12000
    events.sort()
    guard=CausalCpuShiftGuard()
    issued={}
    groups=defaultdict(lambda:dict(n=0,issued=0,sparse=0,revoked=0,covered=0,lower_miss=0,upper_miss=0,
                                   max_exceed_ms=0.))
    def update(group,pred,residual):
        x=groups[group]
        x["n"]+=1
        if pred.abstention_reason=="sparse":x["sparse"]+=1
        elif pred.abstention_reason=="cpu_shift_alarm":x["revoked"]+=1
        else:
            assert pred.issued and pred.original.available
            x["issued"]+=1
            lo,hi=pred.original.lower_ms,pred.original.upper_ms
            if lo<=residual<=hi:x["covered"]+=1
            elif residual<lo:
                x["lower_miss"]+=1
                x["max_exceed_ms"]=max(x["max_exceed_ms"],lo-residual)
            else:
                x["upper_miss"]+=1
                x["max_exceed_ms"]=max(x["max_exceed_ms"],residual-hi)
    for t,event,i in events:
        r=truth[i]
        if event==2:
            age=r["arrival_ms"]-r["last_queue_telemetry_ms"]
            pred=guard.query(t,r["task_class"],age)
            assert pred.original.context==r["queue_model_context"] and not pred.certified
            issued[i]=pred
            guard.dispatch(i,r["node"],r["task_class"],t,age,
                           r["predicted_wait_at_dispatch_ms"],r["predicted_cpu_at_dispatch_ms"])
        else:
            assert i in issued
            observed=guard.finish(i,r["node"],r["actual_start_ms"],t)
            assert math.isclose(observed,r["signed_nonnetwork_residual_ms"],abs_tol=1e-8,rel_tol=0)
            pred=issued[i]
            phase="post" if i>=10000 else "pre"
            update(("all",),pred,observed)
            update(("phase",phase),pred,observed)
            update(("phase_class",phase,r["task_class"]),pred,observed)
    assert len(issued)==guard.base.dispatches==guard.base.finishes==12000
    assert guard.base.pending=={}
    guard.invariant()
    output_groups={}
    for key,g in sorted(groups.items()):
        assert g["n"]==g["issued"]+g["sparse"]+g["revoked"]
        assert g["issued"]==g["covered"]+g["lower_miss"]+g["upper_miss"]
        output_groups["/".join(key)]={**g,
            "conditional_inclusion_only_issued":g["covered"]/g["issued"] if g["issued"] else None,
            "abstention_fraction":(g["sparse"]+g["revoked"])/g["n"]}
    first_shock_arrival=truth[10000]["arrival_ms"]
    first_post_finish=min(r["delivered_cpu_finish_ms"] for r in trace if r["task_index"]>=10000)
    alarm=guard.first_alarm_delivery_ms
    details=dict(
       alarm_count=guard.alarm_count,alarm_clock_ms=alarm,
       alarm_trigger_task_index=guard.first_alarm_task_index,
       alarm_evidence=list(guard.alarm_positive_evidence),
       postshock_first_task_arrival_ms=first_shock_arrival,
       postshock_first_cpu_finish_ms=first_post_finish,
       pre_shock_false_alarm=bool(alarm is not None and alarm<first_shock_arrival),
       first_alarm_delivery_lag_vs_postshock_arrival_ms=(alarm-first_shock_arrival if alarm is not None else None),
       alarm_after_first_postshock_cpu_finish=bool(alarm is not None and alarm>=first_post_finish),
       cpu_finish_labels=guard.finished_cpu_labels,
       abstention_sparse=guard.sparse_abstentions,
       abstention_revoked=guard.alarm_abstentions,
       issued=guard.issued)
    assert details["issued"]+details["abstention_sparse"]+details["abstention_revoked"]==12000
    return dict(alarm=details,groups=output_groups)

def main(source,dest):
    original=json.loads(Path(source).read_text())
    assert original["status"]=="PASS" and original["scientific_seed"]==90
    assert len(original["rows"])==4 and original["dependent_task_policy_observations"]==48000
    rows=[]
    for arm in original["rows"]:
        attr=arm["stats"]
        res=run_one(arm["trace"])
        summary={**dict(scenario=attr["scenario"],policy=attr["policy"]),**res}
        print("STAGE30_ARCHIVED_DEVELOPMENT_RESULT",json.dumps(
            dict(scenario=attr["scenario"],policy=attr["policy"],
                 alarm=res["alarm"],post=res["groups"]["phase/post"],
                 post_mission=res["groups"]["phase_class/post/MISSION"],
                 post_high=res["groups"]["phase_class/post/HIGH"]),sort_keys=True),flush=True)
        rows.append(summary)
    result=dict(status="PASS",original_stage27_artifact_run=42269844289,
                scientific_source_seeds=1,source_seed=90,
                no_new_physical_policy_simulation=True,
                nominal_coverage_guaranteed=False,
                caution="Alarm abstention is not correctness; conditional inclusion excludes revoked tasks and is not safety coverage",
                rows=rows)
    p=Path(dest);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print("JPDC_STAGE30_ARCHIVED_CPU_ALARM_DEVELOPMENT_REPLAY_PASS")

if __name__=="__main__":
    a=argparse.ArgumentParser()
    a.add_argument("--original",required=True);a.add_argument("--out",required=True)
    x=a.parse_args()
    main(x.original,x.out)
