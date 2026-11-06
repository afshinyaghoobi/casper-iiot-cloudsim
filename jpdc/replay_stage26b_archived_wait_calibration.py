#!/usr/bin/env python3
"""Stage26b archived Stage25 WAIT-only causal chronological prequential replay.

This does not rerun a physical model; score coverage is exploratory, single seed89.
"""
import argparse,json,math
from collections import defaultdict
from pathlib import Path
from causal_wait_calibration_stage26 import CausalWaitCalibrator

def replay(trace):
    c=CausalWaitCalibrator()
    events=[]
    truth={}
    for t in trace:
        i=t["task_index"]
        assert i not in truth
        assert t["queue_model_context"]=="native_python_strict_fcfs_vq_telemetry50ms"
        truth[i]=t
        # Same-time CPU completions before new arrivals, as source event loop.
        events.append((t["arrival_ms"],2,i))
        events.append((t["delivered_cpu_finish_ms"],0,i))
    events.sort()
    issued={}
    coverage=defaultdict(lambda:dict(count=0,available=0,covered=0,low_miss=0,high_miss=0,
                                     max_miss_ms=0.,no_samples=0))
    for clock,kind,i in events:
        t=truth[i]
        age=t["arrival_ms"]-t["last_queue_telemetry_ms"]
        key=(t["task_class"],c.band(age))
        if kind==2:
            assert i not in issued
            forecast=c.query(clock,t["task_class"],age)
            assert forecast.descriptive_only and not forecast.certified
            assert forecast.context==t["queue_model_context"]
            # Opaque issue-time value never mutated after CPU completion.
            issued[i]=forecast
            c.dispatch(i,t["node"],t["task_class"],clock,age,
                       t["predicted_wait_at_dispatch_ms"])
            coverage[key]["count"]+=1
            if forecast.available:
                coverage[key]["available"]+=1
            else:
                coverage[key]["no_samples"]+=1
        else:
            assert i in issued
            f=issued[i]
            residual=c.finish(i,t["node"],t["actual_start_ms"],
                              clock,t["actual_wait_ms"])
            assert math.isclose(residual,t["signed_wait_residual_ms"],rel_tol=0,abs_tol=1e-8)
            if f.available:
                if f.lower_ms<=residual<=f.upper_ms:
                    coverage[key]["covered"]+=1
                else:
                    if residual<f.lower_ms:
                        coverage[key]["low_miss"]+=1
                        v=f.lower_ms-residual
                    else:
                        coverage[key]["high_miss"]+=1
                        v=residual-f.upper_ms
                    coverage[key]["max_miss_ms"]=max(coverage[key]["max_miss_ms"],v)
    assert len(issued)==12000 and c.delivered==c.dispatched==12000 and not c.pending
    c.invariant()
    arr=[]
    for key in sorted(coverage):
        s=coverage[key]
        assert s["count"]==s["available"]+s["no_samples"]
        assert s["available"]==s["covered"]+s["low_miss"]+s["high_miss"]
        arr.append(dict(task_class=key[0],telemetry_age_band=key[1],**s,
                        prequential_inclusion_rate=s["covered"]/s["available"] if s["available"] else None))
    assert sum(a["count"] for a in arr)==12000
    return arr

def main(source,output):
    x=json.loads(Path(source).read_text())
    assert x["status"]=="PASS" and x["seed"]==89 and len(x["rows"])==4
    outs=[]
    for arm in x["rows"]:
        attrs=arm["stats"]
        assert len(arm["trace"])==12000
        arr=replay(arm["trace"])
        total_available=sum(s["available"] for s in arr)
        total_covered=sum(s["covered"] for s in arr)
        row=dict(scenario=attrs["scenario"],policy=attrs["policy"],
                 observations=12000,interval_available_decisions=total_available,
                 abstentions=12000-total_available,
                 prequential_inclusion_rate=(total_covered/total_available if total_available else None),
                 strata=arr)
        print("STAGE26B_REPLAY_RESULT",json.dumps({
            k:v for k,v in row.items() if k!="strata"},sort_keys=True))
        for b in arr:
            print("STAGE26B_CONTEXT",json.dumps(dict(scenario=attrs["scenario"],
                policy=attrs["policy"],**b),sort_keys=True))
        outs.append(row)
    output_data=dict(status="PASS",scientific_status="posthoc archived one-seed development replay, no independent coverage guarantee",
                     original_artifact_run=42254782412,all_results_descriptive_only=True,
                     seed_index=89,rows=outs)
    dst=Path(output);dst.parent.mkdir(parents=True,exist_ok=True)
    dst.write_text(json.dumps(output_data,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE26B_ARCHIVED_CAUSAL_WAIT_REPLAY_PASS")

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--original",required=True);p.add_argument("--out",required=True)
    a=p.parse_args();main(a.original,a.out)
