#!/usr/bin/env python3
"""Synthetic Stage50 trace parser contract test; does NOT validate CloudSim physics."""
from audit_stage50_queue_transitions import audit, NAMES, EVENT_GAPS, SERVICE, ARRIVE

def fixture():
    rows=[]
    for case,gap in zip(NAMES,EVENT_GAPS):
        rows.append(f"STAGE50_CASE,{case},minEventSec={gap:.9f},expectedDataCenterFloorMs={(gap+.01)*1000:.9f}")
        for idx in range(3):
            # Deliberately separate submissions and execution snapshots; this tests
            # matching by cloudlet ID, clock units and deterministic state transitions.
            t=1000.0+25.0*idx
            running=""  # state before source submission
            rows.append(f"STAGE50_SUBMIT,{case},BEFORE,{t:.12f},{idx},{running},")
            rows.append(f"STAGE50_SUBMIT,{case},AFTER,{t:.12f},{idx},{idx},")
            rows.append(f"STAGE50_UPDATE,{case},BEFORE,{t+1:.12f},{idx},")
            rows.append(f"STAGE50_UPDATE,{case},AFTER,{t+9:.12f},,")
            rows.append(f"STAGE50_FINISH,{case},{idx},{idx},{t+9:.12f},0.000000000000,{SERVICE[idx]:.12f},{SERVICE[idx]:.12f}")
            rows.append(f"STAGE50_OUTCOME,{case},{idx},{idx},0.000000000000,{SERVICE[idx]:.12f},{ARRIVE[idx]:.12f},{SERVICE[idx]:.12f}")
        rows.append(f"STAGE50_CASE_DONE,{case},submissions=3,finishes=3")
    rows.append("JPDC_STAGE50_REAL_CLOUDSIM_857_THREE_CLOCK_TRANSITIONS_COMPLETE")
    return rows

def main():
    lines=fixture()
    report=audit(lines)
    assert report["status"]=="PASS"
    assert len(report["cases"])==3
    assert all(len(x["rows"])==3 for x in report["cases"])
    assert all(len(x["transitions"])>=3 for x in report["cases"])
    # The auditor must reject truncated and malformed source logs.
    duplicate_submit_after = list(lines)
    after_record = next(x for x in lines if x.startswith("STAGE50_SUBMIT,MICRO_1US,AFTER,"))
    duplicate_submit_after.insert(duplicate_submit_after.index(after_record) + 1, after_record)
    invalid_phase = [x.replace("STAGE50_SUBMIT,MICRO_5MS,AFTER,", "STAGE50_SUBMIT,MICRO_5MS,UNKNOWN,") if x.startswith("STAGE50_SUBMIT,MICRO_5MS,AFTER,") else x for x in lines]
    invalid_queue_id = [x.replace(",0,", ",-99,") if x.startswith("STAGE50_UPDATE,MICRO_1US,BEFORE,") else x for x in lines]
    for mutated in (lines[:-1], duplicate_submit_after, invalid_phase, invalid_queue_id,
                    [z for z in lines if not z.startswith("STAGE50_FINISH,MICRO_5MS,1,")],
                    [z.replace("STAGE50_SUBMIT,MICRO_20MS,BEFORE,", "STAGE50_SUBMIT,MICRO_20MS,BEFORE,-")
                     if z.startswith("STAGE50_SUBMIT,MICRO_20MS,BEFORE,") else z for z in lines]):
        try:
            audit(mutated)
        except (AssertionError,ValueError):
            continue
        raise AssertionError("Stage50 audit unexpectedly accepted invalid fixture")
    print("JPDC_STAGE50_SYNTHETIC_PARSER_CONTRACT_PASS")

if __name__=="__main__":
    main()
