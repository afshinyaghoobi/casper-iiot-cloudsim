#!/usr/bin/env python3
"""Stage65 original-source n8 holdout audit with prereg safety and exact sign tests."""
import argparse,json,math
from pathlib import Path
SEEDS=tuple(range(1811,1819))
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL","PARTIAL_MINIMAX_FULL_FALLBACK")

def exact_two_sided_sign(deltas):
    nonzero=[d for d in deltas if d!=0]
    n=len(nonzero)
    if n==0:return dict(nonzero_n=0,favorable=0,adverse=0,p=1.0)
    favor=sum(d<0 for d in nonzero)
    adverse=n-favor
    tail=sum(math.comb(n,k) for k in range(min(favor,adverse)+1))
    return dict(nonzero_n=n,favorable=favor,adverse=adverse,
                p=min(1.0,2.0*tail/(2**n)))

def audit(sources):
    assert set(sources)==set(SEEDS)
    indexed={}
    for seed in SEEDS:
        obj=sources[seed]
        assert obj["status"]=="PASS" and obj["source_seed"]==seed
        assert obj["source_task_observations"]==72000 and len(obj["rows"])==6
        for r in obj["rows"]:
            key=(seed,r["scenario"],r["policy"])
            assert key not in indexed and r["seed"]==seed
            assert r["scenario"] in SCENARIOS and r["policy"] in POLICIES
            assert 0<=r["post_mission_deadline_misses"]<=r["post_mission_n"]
            assert 0<=r["all_mission_deadline_misses"]
            if r["policy"]==POLICIES[-1]:
                assert r["candidate"]["full_original_fallback"]
                assert r["candidate"]["source_causal_feedback_only"]
                assert not r["candidate"]["historical_sample_max_calibrated"]
            else:assert r["candidate"] is None
            indexed[key]=r
    assert len(indexed)==len(SEEDS)*len(SCENARIOS)*len(POLICIES)
    cells=[]
    stats={}
    all_safe=True
    scenario_wins={}
    all_wins=0
    for sc in SCENARIOS:
        deltas=[]
        win_count=0
        for seed in SEEDS:
            g=indexed[(seed,sc,"PRED_GREEDY")]
            full=indexed[(seed,sc,"CASPER_FULL")]
            part=indexed[(seed,sc,"PARTIAL_MINIMAX_FULL_FALLBACK")]
            assert g["post_mission_n"]==full["post_mission_n"]==part["post_mission_n"]
            post_delta=part["post_mission_deadline_misses"]-full["post_mission_deadline_misses"]
            total_delta=part["all_mission_deadline_misses"]-full["all_mission_deadline_misses"]
            deltas.append(post_delta)
            win_count+=int(post_delta<0)
            all_wins+=int(post_delta<0)
            if post_delta>0 or total_delta>0:all_safe=False
            cells.append(dict(seed=seed,scenario=sc,
                 post_mission_n=full["post_mission_n"],
                 greedy_post_misses=g["post_mission_deadline_misses"],
                 full_post_misses=full["post_mission_deadline_misses"],
                 partial_post_misses=part["post_mission_deadline_misses"],
                 partial_minus_full_post=post_delta,
                 full_all_mission_misses=full["all_mission_deadline_misses"],
                 partial_all_mission_misses=part["all_mission_deadline_misses"],
                 partial_minus_full_all=total_delta,
                 candidate_live_actual_switches=part["candidate"]["actual_mission_switches_vs_instantaneous_full"],
                 candidate_live_postshock_switches=part["candidate"]["postshock_actual_switches_vs_instantaneous_full"],
                 candidate_mission_ready=part["candidate"]["mission_ready"],
                 candidate_mission_fallback=part["candidate"]["mission_fallback"]))
        scenario_wins[sc]=win_count
        stats[sc]=dict(paired_seed_deltas=deltas,mean_delta_misses_per_source=sum(deltas)/len(deltas),
                        exact_paired_sign=exact_two_sided_sign(deltas),
                        strict_source_wins=win_count)
    safety_and_benefit=all_safe and all_wins>=4 and all(v>=1 for v in scenario_wins.values())
    return dict(status="PASS",technical_validation="PASS",
       original_source_n=8,dependent_policy_task_observations=576000,
       no_harm_both_scopes_all_16_cells=all_safe,
       postshock_strict_source_wins=all_wins,
       benefit_per_scenario=scenario_wins,
       prereg_acceptance_gate="PASS" if safety_and_benefit else "FAIL",
       statistical_superiority_at_p_005_per_scenario=all(
           stats[sc]["exact_paired_sign"]["p"]<.05 for sc in SCENARIOS),
       published_uncertainty_calibration=False,
       Java_SpaceShared_parity_remaining_failed=True,
       scenarios=stats,cells=cells)

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--source-dir",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    sources={}
    for seed in SEEDS:
        folder=Path(a.source_dir)/f"jpdc-stage65-frozen-holdout-seed-{seed}"
        assert (folder/"source.json").read_bytes()==(folder/"repeat.json").read_bytes()
        assert (folder/"source.log").read_bytes()==(folder/"repeat.log").read_bytes()
        sources[seed]=json.loads((folder/"source.json").read_text())
    result=audit(sources)
    target=Path(a.out);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n")
    for case in result["cells"]:
        print("JPDC_STAGE65_HOLDOUT_CELL",json.dumps(case,sort_keys=True))
    print("JPDC_STAGE65_ORIGINAL_HOLDOUT_AUDIT_PASS")
