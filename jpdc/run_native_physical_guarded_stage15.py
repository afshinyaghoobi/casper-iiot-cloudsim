#!/usr/bin/env python3
"""Stage15 prespecified ten-arm single DEVELOPMENT seed85 physical experiment."""
import argparse,json,math
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_physical_guarded_freshness_stage15 import simulate as guarded_sim
from independent_physical_freshness_stage14 import simulate as unguarded_sim
from independent_network_probe_stage6 import simulate as original_sim

SEED=85
N=12000
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL","NEW_NETWORK_RESIDUAL_PROBE",
          "NEW_FRESHNESS_ACTIVE","NEW_FRESHNESS_GUARDED")
def run():
    cal=calibrate(SEED,80000,include_reference=True)
    assert cal["postburnin_service_ratio_count"]==70000
    rows=[]
    for scenario in SCENARIOS:
        for policy in POLICIES:
            r=guarded_sim(SEED,scenario,policy,cal,N)
            if policy in POLICIES[:3]:
                old=dict(r)
                old.pop("shadow_network_epoch")
                assert old==original_sim(SEED,scenario,policy,cal,N),(
                    "frozen Stage6 output changed",scenario,policy)
                print("JPDC_STAGE15_LEGACY_STAGE6_EXACT_PARITY_PASS",scenario,policy)
            elif policy=="NEW_FRESHNESS_ACTIVE":
                assert r==unguarded_sim(SEED,scenario,policy,cal,N),(
                    "original Stage14 algorithm was modified",scenario)
                print("JPDC_STAGE15_STAGE14_UNGUARDED_EXACT_PARITY_PASS",scenario)
            else:
                a=r["stage14_active"]
                assert a["causal_e2e_delivered"]==N
                assert a["probe_attempts"]<=a["normal_arrivals"]//100
                assert a["probe_opportunities"]==a["normal_arrivals"]//100
                assert a["probe_attempts"]+a["probe_skipped"]==a["probe_opportunities"]
                assert a["mission_unverified_decisions"]<=r["mission_tasks"]
                print("JPDC_STAGE15_GUARDED_CAUSAL_BUDGET_PASS",scenario)
            assert r["deployment_tasks"]==r["cpu_finish_events"]==r["e2e_feedback_events"]==N
            post=round(r["post_deadline_miss_rate"]*r["post_mission_tasks"])
            assert math.isclose(post/r["post_mission_tasks"],r["post_deadline_miss_rate"],abs_tol=1e-12)
            pre=r["mission_deadline_misses"]-post
            print("STAGE15_RESULT",scenario,policy,
                  "total_mission_misses",r["mission_deadline_misses"],
                  "pre_misses",pre,"post_misses",post,
                  "mean_wait_ms",r["mean_wait_ms"],
                  "mean_latency_ms",r["mean_latency_ms"],
                  "probes",r.get("stage14_active",{}).get("probe_attempts"))
            rows.append(r)
    assert len(rows)==10
    return dict(status="PASS",scientific_scope="one development seed85 no p-values",
                seed_index=SEED,task_policy_observations=120000,
                scenarios=list(SCENARIOS),policies=list(POLICIES),
                calibration={k:v for k,v in cal.items() if k!="reference_scores"},rows=rows)
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True)
    args=p.parse_args()
    data=run()
    path=Path(args.out)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE15_TEN_ARM_NATIVE_PHYSICAL_DEVELOPMENT_MATRIX_PASS")
