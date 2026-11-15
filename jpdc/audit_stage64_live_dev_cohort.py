#!/usr/bin/env python3
"""Stage64 all-or-nothing paired original DEV source cohort audit; no p-values."""
import argparse,json
from pathlib import Path
SEEDS=(1711,1712)
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
PARTIAL="PARTIAL_MINIMAX_FULL_FALLBACK"
POLICIES=("PRED_GREEDY","CASPER_FULL",PARTIAL)

def audit(sources):
    assert set(sources)==set(SEEDS)
    records={}
    for seed in SEEDS:
        obj=sources[seed]
        assert obj["status"]=="PASS" and obj["source_seed"]==seed
        assert obj["source_task_observations"]==72000
        assert len(obj["rows"])==6
        for row in obj["rows"]:
            key=(seed,row["scenario"],row["policy"])
            assert row["seed"]==seed and key not in records
            assert row["scenario"] in SCENARIOS and row["policy"] in POLICIES
            assert 0<=row["post_mission_deadline_misses"]<=row["post_mission_n"]
            if row["policy"]==PARTIAL:
                diag=row["candidate"]
                assert diag is not None and diag["policy"]==PARTIAL
                assert diag["source_causal_feedback_only"]
                assert diag["full_original_fallback"]
                assert diag["mission_attempts"]==diag["mission_ready"]+diag["mission_fallback"]
                assert not diag["historical_sample_max_calibrated"]
                assert diag["postshock_mission_misses"]==row["post_mission_deadline_misses"]
            else:
                assert row["candidate"] is None
            records[key]=row
    assert len(records)==12
    cells=[]
    strict_improvement=False
    safety_pass=True
    differences_pass=True
    for sc in SCENARIOS:
        for seed in SEEDS:
            a=records[(seed,sc,PARTIAL)]
            f=records[(seed,sc,"CASPER_FULL")]
            g=records[(seed,sc,"PRED_GREEDY")]
            assert a["post_mission_n"]==f["post_mission_n"]==g["post_mission_n"]
            delta=a["post_mission_deadline_misses"]-f["post_mission_deadline_misses"]
            switch=a["candidate"]["actual_mission_switches_vs_instantaneous_full"]
            if delta>0:safety_pass=False
            if delta<0:strict_improvement=True
            if switch<1:differences_pass=False
            cells.append(dict(seed=seed,scenario=sc,
                post_mission_n=a["post_mission_n"],
                pred_greedy_post_misses=g["post_mission_deadline_misses"],
                original_full_post_misses=f["post_mission_deadline_misses"],
                live_partial_post_misses=a["post_mission_deadline_misses"],
                partial_minus_full_misses=delta,
                full_trajectory_mission_switches=switch,
                postshock_mission_switches=a["candidate"]["postshock_actual_switches_vs_instantaneous_full"],
                mission_ready=a["candidate"]["mission_ready"],
                mission_fallback=a["candidate"]["mission_fallback"],
                mean_latency_ms=a["mean_latency_ms"],
                mean_wait_ms=a["mean_wait_ms"]))
    gate=safety_pass and strict_improvement and differences_pass
    return dict(status="PASS",source_technical_audit="PASS",
         prereg_dev_no_harm_per_seed=safety_pass,
         prereg_dev_some_strict_improvement=strict_improvement,
         prereg_dev_distinct_actual_routes_each_cell=differences_pass,
         prereg_candidate_advance_gate="PASS" if gate else "FAIL",
         scientific_independent_DEV_source_n=2,
         independent_untouched_holdout_n=0,
         dependent_policy_task_observations=144000,
         calibrated_uncertainty_coverage=False,
         original_java_python_queue_parity_still_failed=True,
         cells=cells)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source-dir",required=True)
    p.add_argument("--out",required=True)
    args=p.parse_args()
    sources={}
    for seed in SEEDS:
        folder=Path(args.source_dir)/f"jpdc-stage64-live-partial-dev-seed-{seed}"
        assert (folder/"source.json").read_bytes()==(folder/"repeat.json").read_bytes()
        assert (folder/"source.log").read_bytes()==(folder/"repeat.log").read_bytes()
        sources[seed]=json.loads((folder/"source.json").read_text())
    outcome=audit(sources)
    d=Path(args.out);d.parent.mkdir(parents=True,exist_ok=True)
    d.write_text(json.dumps(outcome,sort_keys=True,indent=2,allow_nan=False)+"\n")
    for cell in outcome["cells"]:
        print("JPDC_STAGE64_PAIRED_DEV_CELL",json.dumps(cell,sort_keys=True))
    print("JPDC_STAGE64_ORIGINAL_SOURCE_COHORT_AUDIT_PASS")
