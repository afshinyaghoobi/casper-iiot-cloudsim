#!/usr/bin/env python3
"""Stage25 registered seed89 frozen two-scenario/two-policy queue WAIT audit."""
import argparse,json,math,statistics
from collections import Counter
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_physical_queue_trace_stage25 import simulate
from independent_network_probe_stage6 import simulate as frozen_stage6

SEED=89
N=12000
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL")

def percentile(values,q):
    a=sorted(values)
    return a[math.ceil(len(a)*q)-1]

def run():
    cal=calibrate(SEED,80000,include_reference=True)
    assert cal["postburnin_service_ratio_count"]==70000
    rows=[]
    for scenario in SCENARIOS:
        for policy in POLICIES:
            trace=[]
            actual=simulate(SEED,scenario,policy,cal,N,queue_trace_hook=trace.append)
            original=frozen_stage6(SEED,scenario,policy,cal,N)
            reference=dict(actual);reference.pop("shadow_network_epoch")
            assert reference==original,(scenario,policy,"source policy mutated")
            assert len(trace)==N
            indices=[t["task_index"] for t in trace]
            assert sorted(indices)==list(range(N))
            error=[]
            abs_error=[]
            telemetry_ages=[]
            types=Counter()
            post_errors=[]
            for t in trace:
                assert t["queue_model_context"]=="native_python_strict_fcfs_vq_telemetry50ms"
                assert t["arrival_ms"]<=t["actual_start_ms"]<=t["delivered_cpu_finish_ms"]
                assert t["predicted_wait_at_dispatch_ms"]>=0
                assert math.isclose(t["actual_wait_ms"],t["actual_start_ms"]-t["arrival_ms"],abs_tol=1e-8)
                assert math.isclose(t["signed_wait_residual_ms"],t["actual_wait_ms"]-t["predicted_wait_at_dispatch_ms"],abs_tol=1e-8)
                assert all(math.isfinite(t[k]) for k in
                    ("arrival_ms","actual_start_ms","delivered_cpu_finish_ms",
                     "actual_wait_ms","predicted_wait_at_dispatch_ms","signed_wait_residual_ms"))
                assert t["last_queue_telemetry_ms"] is not None and t["last_queue_telemetry_ms"]<=t["arrival_ms"]
                telemetry_ages.append(t["arrival_ms"]-t["last_queue_telemetry_ms"])
                error.append(t["signed_wait_residual_ms"])
                abs_error.append(abs(t["signed_wait_residual_ms"]))
                types[t["task_class"]]+=1
                if t["task_index"]>=10000:post_errors.append(t["signed_wait_residual_ms"])
            stats=dict(scenario=scenario,policy=policy,scientific_seed=SEED,
                records=N,task_class_counts=dict(types),source_stage6_parity=True,
                signed_wait_error_min_ms=min(error),signed_wait_error_max_ms=max(error),
                signed_wait_error_mean_ms=statistics.mean(error),
                signed_wait_error_median_ms=statistics.median(error),
                abs_wait_error_q90_ms=percentile(abs_error,.90),
                abs_wait_error_q95_ms=percentile(abs_error,.95),
                abs_wait_error_q99_ms=percentile(abs_error,.99),
                abs_wait_error_over_2ms_count=sum(v>2. for v in abs_error),
                postshock_signed_wait_error_mean_ms=statistics.mean(post_errors),
                telemetry_age_mean_ms=statistics.mean(telemetry_ages),
                telemetry_age_max_ms=max(telemetry_ages))
            print("STAGE25_QUEUE_WAIT_DESCRIPTIVE",json.dumps(stats,sort_keys=True),flush=True)
            rows.append(dict(stats=stats,trace=sorted(trace,key=lambda t:t["task_index"])))
    assert len(rows)==4
    return dict(status="PASS",seed=SEED,science="ONE source development seed; descriptive WAIT-only residuals NOT queue prediction bounds",
                original_stage6_policy_parity=True,rows=rows,dependent_task_policy_records=48000)
if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--out",required=True)
    args=parser.parse_args()
    data=run()
    output=Path(args.out);output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(data,sort_keys=True,allow_nan=False,separators=(",",":"))+"\n")
    print("JPDC_STAGE25_FROZEN_QUEUE_WAIT_TRACE_COMPLETE_PASS",flush=True)
