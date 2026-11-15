#!/usr/bin/env python3
"""Stage63 original chosen-node time-ordered snapshot audit only; n=2 DEV."""
import argparse,json
from pathlib import Path
SEEDS=(1611,1612)
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL")
FIELDS=("mission","cpu_eligible","net_eligible","joint_eligible",
    "cpu_hit","cpu_violation","net_hit","net_violation","joint_both_hit",
    "joint_both_violation","joint_total_excess_hit","joint_total_excess_violation")

def summarize(original):
    assert set(original)==set(SEEDS)
    rows={}
    for seed in SEEDS:
        a=original[seed]
        assert a["status"]=="PASS" and a["source_seed"]==seed
        assert a["no_route_changes"] and a["original_source_parity"]
        assert a["source_task_observations"]==48000
        assert len(a["rows"])==4
        for item in a["rows"]:
            key=(seed,item["scenario"],item["policy"])
            assert key not in rows and item["seed"]==seed
            assert item["scenario"] in SCENARIOS and item["policy"] in POLICIES
            sh=item["shadow"]
            assert sh["stage63_no_counterfactual_unselected_nodes"] is True
            assert sh["stage63_no_coverage_calibration_claim"] is True
            assert sh["CPU_completion_deliveries"]==sh["E2E_delivered_feedback"]==12000
            assert sh["original_source_task_count"]==12000
            assert sh["stage63_chosen_node_temporal_coverage"]["ALL_MISSION"]["mission"]==sh["mission_arrivals"]
            assert sh["stage63_chosen_node_temporal_coverage"]["POST_MISSION"]["mission"]==sh["post_mission_arrivals"]
            for phase in ("ALL_MISSION","POST_MISSION"):
                c=sh["stage63_chosen_node_temporal_coverage"][phase]
                assert 0<=c["joint_eligible"]<=min(c["cpu_eligible"],c["net_eligible"])<=c["mission"]
                assert c["cpu_hit"]+c["cpu_violation"]==c["cpu_eligible"]
                assert c["net_hit"]+c["net_violation"]==c["net_eligible"]
                assert c["joint_both_hit"]+c["joint_both_violation"]==c["joint_eligible"]
                assert c["joint_total_excess_hit"]+c["joint_total_excess_violation"]==c["joint_eligible"]
            rows[key]=sh
    assert len(rows)==8
    group=[]
    for sc in SCENARIOS:
        for p in POLICIES:
            samples=[rows[(seed,sc,p)] for seed in SEEDS]
            summaries={}
            for phase in ("ALL_MISSION","POST_MISSION"):
                counts={k:sum(sh["stage63_chosen_node_temporal_coverage"][phase][k] for sh in samples)
                    for k in FIELDS}
                assert counts["joint_eligible"]<=counts["mission"]
                counts["joint_component_hit_fraction"]=counts["joint_both_hit"]/counts["joint_eligible"] if counts["joint_eligible"] else None
                counts["joint_total_excess_hit_fraction"]=counts["joint_total_excess_hit"]/counts["joint_eligible"] if counts["joint_eligible"] else None
                counts["chosen_node_joint_eligible_fraction"]=counts["joint_eligible"]/counts["mission"]
                counts["max_cpu_overrun_ms"]=max(sh["stage63_chosen_node_temporal_coverage"][phase]["max_cpu_overrun_ms"] for sh in samples)
                counts["max_net_overrun_ms"]=max(sh["stage63_chosen_node_temporal_coverage"][phase]["max_net_overrun_ms"] for sh in samples)
                summaries[phase]=counts
            per_seed=[]
            for seed,sh in zip(SEEDS,samples):
                post=sh["stage63_chosen_node_temporal_coverage"]["POST_MISSION"]
                joint=post["joint_eligible"]
                hit=post["joint_both_hit"]
                verdict="INSUFFICIENT_EVIDENCE" if joint<30 else "MEETS_90pct_DESCRIPTIVE_TARGET" if hit/joint>=.90 else "INADEQUATE_HISTORICAL_SAMPLE_MAX"
                per_seed.append(dict(seed=seed,post_mission=post["mission"],
                    joint_eligible=joint,joint_both_hit=hit,
                    joint_component_hit_fraction=hit/joint if joint else None,
                    prereg_postshock_gate=verdict,
                    post_cpu_violation=post["cpu_violation"],
                    post_network_violation=post["net_violation"]))
            group.append(dict(scenario=sc,policy=p,phases=summaries,
                              per_seed=per_seed))
    verdicts=[v["prereg_postshock_gate"] for x in group for v in x["per_seed"]]
    overall=("INADEQUATE" if "INADEQUATE_HISTORICAL_SAMPLE_MAX" in verdicts
             else "INSUFFICIENT_EVIDENCE" if "INSUFFICIENT_EVIDENCE" in verdicts
             else "DESCRIPTIVE_TARGET_MET_NOT_CALIBRATED")
    return dict(status="PASS",original_stage6_parity=True,
        software_audit="PASS",preregistered_temporal_coverage_target=overall,
        scientific_source_seed_n=2,new_policy_efficacy_holdout_n=0,
        original_stage61_all_node_feasibility_fail_preserved=True,
        counterfactual_unchosen_node_coverage="NOT_OBSERVABLE",
        future_true_world_coverage_certified=False,rows=group)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source-dir",required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args()
    sources={}
    root=Path(a.source_dir)
    for seed in SEEDS:
        path=root/f"jpdc-stage63-chosen-node-source-{seed}"
        assert (path/"source.json").read_bytes()==(path/"repeat.json").read_bytes()
        assert (path/"source.log").read_bytes()==(path/"repeat.log").read_bytes()
        sources[seed]=json.loads((path/"source.json").read_text())
    r=summarize(sources)
    out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(r,sort_keys=True,indent=2,allow_nan=False)+"\n")
    for x in r["rows"]:
        print("JPDC_STAGE63_CHOSEN_NODE_OBSERVATIONAL_COVERAGE",json.dumps(x,sort_keys=True))
    print("JPDC_STAGE63_ORIGINAL_COHORT_AUDIT_PASS")
