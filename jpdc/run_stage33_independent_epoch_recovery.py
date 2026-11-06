#!/usr/bin/env python3
"""Stage33 frozen post-alarm epoch recovery on preregistered independent seeds."""
import argparse,json
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_physical_cpu_nonnetwork_trace_stage27 import simulate
from independent_network_probe_stage6 import simulate as frozen_stage6
from replay_stage32_archived_recovery import one as recovered
from replay_stage30_archived_cpu_alarm import run_one as permanent

SEEDS=(509,510,511,512)
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL")
N=12000

def run(seed):
    if seed not in SEEDS:raise ValueError("unregistered independent seed")
    calibration=calibrate(seed,80000,include_reference=True)
    assert calibration["postburnin_service_ratio_count"]==70000
    results=[]
    for scenario in SCENARIOS:
        for policy in POLICIES:
            trace=[]
            out=simulate(seed,scenario,policy,calibration,N,queue_trace_hook=trace.append)
            original=dict(out);original.pop("shadow_network_epoch")
            assert original==frozen_stage6(seed,scenario,policy,calibration,N),(seed,scenario,policy,"Stage6 original parity failed")
            assert len(trace)==N and sorted(r["task_index"] for r in trace)==list(range(N))
            r=recovered(trace)
            baseline=permanent(trace)
            assert r["alarm_trigger_clock_ms"]==baseline["alarm"]["alarm_clock_ms"]
            assert r["original_issued"]==baseline["groups"]["all"]["issued"]
            assert r["sparse_abstentions"]==baseline["groups"]["all"]["sparse"]
            assert r["recovered_issued"]+r["rebuild_abstentions"]==baseline["groups"]["all"]["revoked"]
            post=r["groups"]["phase/post"]
            mission=r["groups"]["phase_class/post/MISSION"]
            high=r["groups"]["phase_class/post/HIGH"]
            assert post["n"]==2000 and 0<mission["n"]<2000 and high["n"]>0
            for x in (post,mission,high):
                assert x["n"]==x["original_issued"]+x["recovered_issued"]+x["sparse_abstained"]+x["post_alarm_rebuild_abstained"]
            s2=scenario==SCENARIOS[0]
            check=dict(
                S2_post_MISSION_issued_at_least_half=(mission["available_fraction"]>=.50) if s2 else None,
                S2_post_HIGH_issued_at_least_half=(high["available_fraction"]>=.50) if s2 else None,
                S3_zero_CPU_alarms=(r["alarm_trigger_clock_ms"] is None) if not s2 else None,
                S3_MISSION_issued_at_least_90pct=(mission["available_fraction"]>=.90) if not s2 else None)
            row=dict(seed=seed,scenario=scenario,policy=policy,original_stage6_exact_parity=True,
                alarm_clock_ms=r["alarm_trigger_clock_ms"],
                first_recovery_by_context=r["first_recovery_by_context"],
                original_issued=r["original_issued"],recovered_issued=r["recovered_issued"],
                sparse_abstentions=r["sparse_abstentions"],rebuild_abstentions=r["rebuild_abstentions"],
                post=post,post_high=high,post_mission=mission,
                permanent_revoke_post=baseline["groups"]["phase/post"]["revoked"],
                frozen_operational_gates=check)
            results.append(row)
            print("JPDC_STAGE33_INDEPENDENT_RECOVERY_SEED_RESULT",json.dumps(row,sort_keys=True),flush=True)
    assert len(results)==4
    return dict(status="PASS",seed=seed,independent_scientific_units=1,
                task_policy_evaluations=48000,all_four_original_stage6_parity=True,
                source_only_recovery_observer_not_scheduler=True,
                interval_guarantee=False,rows=results)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--seed",type=int,required=True)
    p.add_argument("--out",required=True);a=p.parse_args()
    result=run(a.seed)
    dst=Path(a.out);dst.parent.mkdir(parents=True,exist_ok=True)
    dst.write_text(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE33_FROZEN_SOURCE_SEED_COMPLETE_PASS",a.seed,flush=True)
