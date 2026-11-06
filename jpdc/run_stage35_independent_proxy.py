#!/usr/bin/env python3
"""Stage35 prespecified independent science seeds, frozen Stage34 proxy rule."""
import argparse,json
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_physical_cpu_nonnetwork_trace_stage27 import simulate
from independent_network_probe_stage6 import simulate as frozen_stage6
from replay_stage34_archived_high_mission_proxy import one as proxy
from replay_stage32_archived_recovery import one as exact_own

SEEDS=(513,514,515,516)
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL")
N=12000

def run(seed):
    if seed not in SEEDS:raise ValueError("not preregistered")
    cal=calibrate(seed,80000,include_reference=True)
    assert cal["postburnin_service_ratio_count"]==70000
    entries=[]
    for scenario in SCENARIOS:
        for policy in POLICIES:
            trace=[]
            physical=simulate(seed,scenario,policy,cal,N,queue_trace_hook=trace.append)
            parity=dict(physical);parity.pop("shadow_network_epoch")
            assert parity==frozen_stage6(seed,scenario,policy,cal,N),(seed,scenario,policy,"frozen Stage6 original parity")
            assert len(trace)==N and sorted(t["task_index"] for t in trace)==list(range(N))
            old=exact_own(trace)
            new=proxy(trace)
            assert old["alarm_trigger_clock_ms"]==new["alarm_trigger_clock_ms"]
            assert new["original_issued"]==old["original_issued"]
            assert new["sparse_abstentions"]==old["sparse_abstentions"]
            assert new["proxy_issued"]==new["recovered_issued"]-old["recovered_issued"]
            assert new["rebuild_abstentions"]==old["rebuild_abstentions"]-new["proxy_issued"]
            for cls in ("NORMAL","HIGH"):
                key="phase_class/post/"+cls
                assert old["groups"][key]=={k:v for k,v in new["groups"][key].items() if k not in ("proxy_issued","proxy_covered","proxy_missed","proxy_inclusion")}
            oldm=old["groups"]["phase_class/post/MISSION"]
            mission=new["groups"]["phase_class/post/MISSION"]
            assert mission["n"]==oldm["n"]
            assert mission["proxy_issued"]==mission["proxy_covered"]+mission["proxy_missed"]
            assert mission["recovered_issued"]==oldm["recovered_issued"]+mission["proxy_issued"]
            assert mission["original_issued"]==oldm["original_issued"]
            s2=scenario==SCENARIOS[0]
            enough=mission["proxy_issued"]>=10
            passes={
                "S2_post_MISSION_at_least_50pct_issued":mission["available_fraction"]>=.5 if s2 else None,
                "S2_at_least10_proxy_and_at_least90pct_proxy_inclusion":(
                    enough and mission["proxy_inclusion"]>=.90) if s2 else None,
                "S3_no_cpu_alarm_and_no_proxy":(
                    new["alarm_trigger_clock_ms"] is None and mission["proxy_issued"]==0) if not s2 else None,
                "S3_post_MISSION_at_least90pct_issued":(
                    mission["available_fraction"]>=.9) if not s2 else None}
            record=dict(seed=seed,scenario=scenario,policy=policy,
                        source_stage6_exact_json_parity=True,
                        alarm_clock_ms=new["alarm_trigger_clock_ms"],
                        original_strict_post_mission=oldm,
                        proxy_post_mission=mission,
                        proxy_post_normal=new["groups"]["phase_class/post/NORMAL"],
                        proxy_post_high=new["groups"]["phase_class/post/HIGH"],
                        proxy_post_all=new["groups"]["phase/post"],
                        total_proxy_issued=new["proxy_issued"],
                        preregistered_operational_gates=passes)
            entries.append(record)
            print("JPDC_STAGE35_SEED_PROXY_RESULT",json.dumps(record,sort_keys=True),flush=True)
    assert len(entries)==4
    return dict(status="PASS",scientific_seed=seed,independent_units=1,
                task_policy_observations=48000,all_original_policy_parity=True,
                policy_rule_frozen_from_stage34=True,certified_intervals=False,rows=entries)
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--seed",type=int,required=True);p.add_argument("--out",required=True)
    a=p.parse_args()
    results=run(a.seed)
    dest=Path(a.out);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(results,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE35_ONE_INDEPENDENT_SOURCE_SEED_COMPLETE_PASS",a.seed)
