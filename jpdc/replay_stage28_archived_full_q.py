#!/usr/bin/env python3
"""Stage28 read-only prequential full q replay from frozen Stage27, one used seed90.

No new physics. No claim of independent coverage or valid Stage24 queue bounds.
"""
import argparse,json,math
from collections import defaultdict
from pathlib import Path
from causal_nonnetwork_calibration_stage28 import CausalNonnetworkCalibrator

def replay(trace):
    c=CausalNonnetworkCalibrator()
    truth={}
    timeline=[]
    for r in trace:
        i=r["task_index"]
        assert i not in truth and 0<=i<12000
        truth[i]=r
        timeline.append((r["arrival_ms"],2,i))
        timeline.append((r["delivered_cpu_finish_ms"],0,i))
    assert len(truth)==12000
    timeline.sort()
    issued={}
    cohorts=defaultdict(lambda:dict(n=0,eligible=0,covered=0,low=0,high=0,max_exceed_ms=0.))
    def accumulate(key,usable,residual):
        v=cohorts[key];v["n"]+=1
        if usable is None:return
        v["eligible"]+=1
        if usable.lower_ms<=residual<=usable.upper_ms:v["covered"]+=1
        elif residual<usable.lower_ms:
            v["low"]+=1
            v["max_exceed_ms"]=max(v["max_exceed_ms"],usable.lower_ms-residual)
        else:
            v["high"]+=1
            v["max_exceed_ms"]=max(v["max_exceed_ms"],residual-usable.upper_ms)

    for clock,event,i in timeline:
        record=truth[i]
        if event==2:
            age=record["arrival_ms"]-record["last_queue_telemetry_ms"]
            z=c.query(clock,record["task_class"],age)
            assert z.descriptive_only and not z.certified
            assert z.context==record["queue_model_context"]
            issued[i]=z
            c.dispatch(i,record["node"],record["task_class"],clock,age,
                       record["predicted_wait_at_dispatch_ms"],
                       record["predicted_cpu_at_dispatch_ms"])
        else:
            assert i in issued
            pred=issued[i]
            observed=c.finish(i,record["node"],record["actual_start_ms"],clock)
            assert math.isclose(observed,record["signed_nonnetwork_residual_ms"],abs_tol=1e-8,rel_tol=0)
            assert math.isclose(observed,record["signed_wait_residual_ms"]+record["signed_cpu_residual_ms"],abs_tol=1e-8,rel_tol=0)
            # Offline only: no true residual was present at dispatch.
            valid=pred if pred.available else None
            band=pred.telemetry_band
            accumulate(("all","all"),valid,observed)
            accumulate(("phase","pre" if i<10000 else "post"),valid,observed)
            accumulate(("class",record["task_class"]),valid,observed)
            accumulate(("class_age",record["task_class"],band),valid,observed)
            accumulate(("phase_class","pre" if i<10000 else "post",record["task_class"]),valid,observed)
    assert len(issued)==c.dispatches==c.finishes==12000 and not c.pending
    c.invariant()
    items=[]
    for key,values in sorted(cohorts.items()):
        assert values["eligible"]==values["covered"]+values["low"]+values["high"]
        items.append(dict(group=list(key),**values,
                          abstained=values["n"]-values["eligible"],
                          empirical_inclusion=(values["covered"]/values["eligible"]
                                               if values["eligible"] else None)))
    return items

def main(source,dest):
    raw=json.loads(Path(source).read_text())
    assert raw["status"]=="PASS" and raw["scientific_seed"]==90
    assert len(raw["rows"])==4 and raw["dependent_task_policy_observations"]==48000
    out=[]
    for arm in raw["rows"]:
        stats=arm["stats"]
        assert len(arm["trace"])==12000 and stats["stage6_exact_parity"]
        summaries=replay(arm["trace"])
        overall=next(x for x in summaries if x["group"]==["all","all"])
        assert overall["n"]==12000
        rec=dict(scenario=stats["scenario"],policy=stats["policy"],overall=overall,subgroups=summaries)
        print("STAGE28_FULL_Q_PREQUENTIAL",json.dumps({k:v for k,v in rec.items() if k!="subgroups"},sort_keys=True),flush=True)
        for sub in summaries:
            if sub["group"][0] in ("phase","phase_class"):
                print("STAGE28_FULL_Q_PHASE_CONTEXT",json.dumps(dict(
                    scenario=stats["scenario"],policy=stats["policy"],**sub),sort_keys=True),flush=True)
        out.append(rec)
    result=dict(status="PASS",original_stage27_run=42269844289,scientific_seed=90,
                statistical_units=1,uses_only_archived_source_trace=True,
                guarantees="NONE: already-examined development source; nonexchangeable and not independent",
                note="Full CPU+WAIT nonnetwork q prequential descriptive inclusion; not Stage24 certified envelope",
                results=out)
    path=Path(dest);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE28_ORIGINAL_FROZEN_FULL_Q_PREQUENTIAL_REPLAY_PASS")

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--original",required=True);p.add_argument("--out",required=True)
    a=p.parse_args();main(a.original,a.out)
