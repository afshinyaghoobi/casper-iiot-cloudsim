#!/usr/bin/env python3
"""Read-only Stage17 original artifact diagnosis; no new physical evaluations."""
import json,sys,math
from pathlib import Path
root=Path(sys.argv[1])
found=list(root.rglob("ablation.json"))
results={}
for f in found:
    x=json.loads(f.read_text())
    assert x["status"]=="PASS" and len(x["rows"])==8
    k=x["seed_index"]
    assert k not in results and k in (86,87)
    results[k]=x
assert sorted(results)==[86,87],("all preregistered development seeds required",sorted(results))
for seed in (86,87):
    rows={(x["scenario"],x["policy"]):x for x in results[seed]["rows"]}
    for scenario in ("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS"):
        base=rows[(scenario,"NEW_FRESHNESS_GUARDED")]
        no=rows[(scenario,"NEW_FRESHNESS_NO_ACTIVE_PROBE")]
        assert base["mission_tasks"]==no["mission_tasks"]
        a=base["stage17_stats"];b=no["stage17_stats"]
        assert sum(a["stage17_selected_node_counts"])==12000
        assert sum(b["stage17_selected_node_counts"])==12000
        assert b["probe_attempts"]==0
        if a["probe_attempts"]>a["probe_opportunities"]:raise AssertionError("budget exceeded")
        # Herfindahl fraction of all selections: descriptive concentration, not causality.
        hhi=lambda c: sum((v/sum(c))**2 for v in c)
        item=dict(seed=seed,scenario=scenario,
            full_misses=rows[(scenario,"CASPER_FULL")]["total_misses"],
            guarded_misses=base["total_misses"],
            no_probe_misses=no["total_misses"],
            no_probe_minus_guarded_misses=no["total_misses"]-base["total_misses"],
            no_probe_minus_guarded_pre_misses=no["pre_misses"]-base["pre_misses"],
            no_probe_minus_guarded_post_misses=no["post_misses"]-base["post_misses"],
            guarded_mean_wait=base["mean_wait_ms"],no_probe_mean_wait=no["mean_wait_ms"],
            guarded_mean_latency=base["mean_latency_ms"],no_probe_mean_latency=no["mean_latency_ms"],
            guarded_probe_attempts=a["probe_attempts"],
            guarded_probe_changed_choices=a["probe_changed_choices"],
            no_probe_attempts=b["probe_attempts"],
            guarded_node_selection_hhi=hhi(a["stage17_selected_node_counts"]),
            no_probe_node_selection_hhi=hhi(b["stage17_selected_node_counts"]))
        print("STAGE17_ARCHIVED_ABLATION_DIAGNOSIS",json.dumps(item,sort_keys=True))
print("JPDC_STAGE17_IMMUTABLE_TWO_SEED_ABLATION_AUDIT_PASS")
