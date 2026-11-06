#!/usr/bin/env python3
"""Stage27 preregistered native CPU and total nonnetwork signed residual trace."""
import argparse,json,math,statistics
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_physical_cpu_nonnetwork_trace_stage27 import simulate
from independent_network_probe_stage6 import simulate as frozen_stage6

SEED=90
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL")
N=12000

def pctl(a,q):
    vals=sorted(a)
    return vals[math.ceil(q*len(vals))-1]

def descript(rows,field):
    v=[r[field] for r in rows]
    return dict(mean_ms=statistics.mean(v),min_ms=min(v),max_ms=max(v),
                abs_p95_ms=pctl([abs(x) for x in v],.95),
                abs_p99_ms=pctl([abs(x) for x in v],.99))

def run():
    cal=calibrate(SEED,80000,include_reference=True)
    assert cal["postburnin_service_ratio_count"]==70000
    all_rows=[]
    for scenario in SCENARIOS:
        for policy in POLICIES:
            trace=[]
            result=simulate(SEED,scenario,policy,cal,N,queue_trace_hook=trace.append)
            baseline=dict(result)
            baseline.pop("shadow_network_epoch")
            assert baseline==frozen_stage6(SEED,scenario,policy,cal,N),(scenario,policy,"Stage6 output parity violated")
            assert len(trace)==N and sorted(x["task_index"] for x in trace)==list(range(N))
            for r in trace:
                assert r["queue_model_context"]=="native_python_strict_fcfs_vq_telemetry50ms"
                assert 0<=r["arrival_ms"]<=r["actual_start_ms"]<=r["delivered_cpu_finish_ms"]
                assert abs(r["actual_wait_ms"]-(r["actual_start_ms"]-r["arrival_ms"]))<1e-8
                assert abs(r["actual_cpu_ms"]-(r["delivered_cpu_finish_ms"]-r["actual_start_ms"]))<1e-8
                assert abs(r["actual_nonnetwork_ms"]-(r["actual_wait_ms"]+r["actual_cpu_ms"]))<1e-8
                assert abs(r["signed_cpu_residual_ms"]-(r["actual_cpu_ms"]-r["predicted_cpu_at_dispatch_ms"]))<1e-8
                assert abs(r["signed_nonnetwork_residual_ms"]-(r["signed_wait_residual_ms"]+r["signed_cpu_residual_ms"]))<1e-8
                assert abs(r["predicted_nonnetwork_at_dispatch_ms"]-(r["predicted_wait_at_dispatch_ms"]+r["predicted_cpu_at_dispatch_ms"]))<1e-8
                assert all(math.isfinite(r[k]) for k in ("actual_cpu_ms","signed_cpu_residual_ms","signed_nonnetwork_residual_ms"))
            stats=dict(seed_index=SEED,scenario=scenario,policy=policy,
                       task_policy_observations=N,stage6_exact_parity=True,
                       pre_10000=dict(n=10000,wait=descript([r for r in trace if r["task_index"]<10000],"signed_wait_residual_ms"),
                           cpu=descript([r for r in trace if r["task_index"]<10000],"signed_cpu_residual_ms"),
                           total_nonnetwork=descript([r for r in trace if r["task_index"]<10000],"signed_nonnetwork_residual_ms")),
                       post_10000=dict(n=2000,wait=descript([r for r in trace if r["task_index"]>=10000],"signed_wait_residual_ms"),
                           cpu=descript([r for r in trace if r["task_index"]>=10000],"signed_cpu_residual_ms"),
                           total_nonnetwork=descript([r for r in trace if r["task_index"]>=10000],"signed_nonnetwork_residual_ms")))
            print("STAGE27_CAUSAL_CPU_NONNETWORK_STATS",json.dumps(stats,sort_keys=True),flush=True)
            all_rows.append(dict(stats=stats,trace=sorted(trace,key=lambda x:x["task_index"])))
    return dict(status="PASS",scientific_seed=SEED,scientific_replicates=1,
                independent_cross_engine_parity=False,
                original_stage6_exact_parity=True,dependent_task_policy_observations=48000,
                rows=all_rows)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    a=p.parse_args();x=run();dest=Path(a.out);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(x,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n")
    print("JPDC_STAGE27_CAUSAL_CPU_PLUS_WAIT_SOURCE_TRACE_PASS",flush=True)
