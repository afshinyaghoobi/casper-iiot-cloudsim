#!/usr/bin/env python3
"""Regression test for the seed29 task-trace CSV contract (synthetic data only)."""
import csv
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_seed29_task_trace import analyze, POLICIES, SCENARIO, SEED

N = 10250
with tempfile.TemporaryDirectory() as td:
    dispatch = Path(td) / "dispatch.csv"
    outcome = Path(td) / "outcome.csv"
    with dispatch.open("w", newline="") as da, outcome.open("w", newline="") as ou:
        dw, ow = csv.writer(da), csv.writer(ou)
        for policy in POLICIES:
            for task in range(N):
                mission = task >= 10000
                is_full = policy == POLICIES[0]
                # The two policies disagree on node and deadline outcome for one task.
                node = 1 if (is_full and task == 10249) else 0
                missed = is_full and task == 10249
                certified = not (is_full and task == 10248)
                covered = not (is_full and task == 10247)
                dw.writerow(["JPDC_TASK_DISPATCH", SEED, SCENARIO, policy,
                             task, node, 1.5 if is_full else 1.0, 5.0, 10.0,
                             str(certified).lower(), 4.0 if is_full else 2.0,
                             str(covered).lower()])
                ow.writerow(["JPDC_TASK_OUTCOME", SEED, SCENARIO, policy,
                             task, node, 10.0 if missed else 5.0, 10.0,
                             str(missed).lower(), str(mission).lower()])
    result = analyze(dispatch, outcome, N)
    assert result["different_node_count"] == 1
    # Exactly one late task changes node, so the other 249 share a node.
    assert result["late_paired_latency_by_node"]["late_same_node"]["count"] == 249
    assert result["late_paired_latency_by_node"]["late_different_node"]["count"] == 1
    assert result["late_paired_latency_by_node"]["late_different_node"]["full_slower_count"] == 0
    assert result["late_paired_latency_by_node"]["late_different_node"]["near_equal_latency_count"] == 1
    assert result["late_mission_disagreements"] == 1
    assert abs(result["late_dvr_delta_full_minus_static"] - 0.004) < 1e-12
    assert result["certification_overlap"]["full_only"]["count"] == 0
    assert result["certification_overlap"]["static_only"]["count"] == 1
    assert result["certification_by_policy"][POLICIES[0]]["certified"] == 249
    assert abs(result["late_fwc"][POLICIES[0]] - 249 / 250) < 1e-12
    assert result["late_fwc"][POLICIES[1]] == 1.0
    assert result["late_mapper_us_mean"][POLICIES[0]] == 4.0
    assert result["late_mapper_us_mean"][POLICIES[1]] == 2.0
    # Simulate a true miss whose 9-decimal CSV latency rounds to the deadline.
    # The logged miss flag remains authoritative at the rounding boundary.
    assert result["late_mission_disagreements"] == 1
    # A false "no miss" flag must not be accepted when the rounded latency exceeds deadline.
    bad_outcome = Path(td) / "bad_outcome.csv"
    with outcome.open(newline="") as source, bad_outcome.open("w", newline="") as dest:
        rdr, wtr = csv.reader(source), csv.writer(dest)
        changed = False
        for row in rdr:
            if not changed and row[3] == POLICIES[0] and int(row[4]) == 10249:
                row[6], row[8] = "10.000000001", "false"
                changed = True
            wtr.writerow(row)
    assert changed
    try:
        analyze(dispatch, bad_outcome, N)
    except ValueError as exc:
        assert "dispatch/outcome mismatch" in str(exc), str(exc)
    else:
        raise AssertionError("false no-miss accepted above deadline")
    # Reject a trace with an incorrect coverage boolean rather than silently accepting it.
    broken = Path(td) / "broken.csv"
    rows = dispatch.read_text().splitlines()
    rows[0] = rows[0].rsplit(",", 1)[0] + ",maybe"
    broken.write_text("\n".join(rows) + "\n")
    try:
        analyze(broken, outcome, N)
    except ValueError as exc:
        assert "coverage flag" in str(exc), str(exc)
    else:
        raise AssertionError("invalid coverage flag accepted")
print("SEED29_TRACE_CONTRACT_PASS")
