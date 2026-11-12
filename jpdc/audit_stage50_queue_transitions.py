#!/usr/bin/env python3
"""Stage50 prospective passive CloudSimPlus SpaceShared state-transition audit."""
import argparse
import json
import math
from pathlib import Path

NAMES = ("MICRO_1US", "MICRO_5MS", "MICRO_20MS")
SERVICE = (8.099623, 4.730689, 9.120283)
ARRIVE = (0.0, 5.318920, 8.0997406)
EVENT_GAPS = (0.000001, 0.005, 0.02)
TOL = 1e-6


def finite_nonnegative(x):
    v = float(x)
    assert math.isfinite(v) and v >= 0, x
    return v


def ids(raw):
    return [int(x) for x in raw.split(";") if x]


def audit(lines):
    assert "JPDC_STAGE50_REAL_CLOUDSIM_857_THREE_CLOCK_TRANSITIONS_COMPLETE" in lines
    output = []
    for case_index, name in enumerate(NAMES):
        events = []
        submissions = {}
        outcomes = {}
        finishes = {}
        header = None
        done = None
        for seq, line in enumerate(lines):
            if not line.startswith("STAGE50_"):
                continue
            p = line.split(",")
            if len(p) < 2 or p[1] != name:
                continue
            if p[0] == "STAGE50_CASE":
                assert header is None
                header = dict(x.split("=", 1) for x in p[2:])
            elif p[0] == "STAGE50_CASE_DONE":
                assert done is None
                done = dict(x.split("=", 1) for x in p[2:])
            elif p[0] == "STAGE50_SUBMIT":
                assert len(p) == 7, (name, line)
                _, _, phase, clock, task_id, running, waiting = p
                task_id = int(task_id)
                event = dict(seq=seq, kind="SUBMIT_" + phase,
                             clock_ms=finite_nonnegative(clock), submitted=task_id,
                             exec_ids=ids(running), wait_ids=ids(waiting))
                events.append(event)
                if phase == "BEFORE":
                    assert task_id not in submissions
                    submissions[task_id] = event["clock_ms"]
            elif p[0] == "STAGE50_UPDATE":
                assert len(p) == 6, (name, line)
                _, _, phase, clock, running, waiting = p
                events.append(dict(seq=seq, kind="UPDATE_" + phase,
                                   clock_ms=finite_nonnegative(clock),
                                   exec_ids=ids(running), wait_ids=ids(waiting)))
            elif p[0] == "STAGE50_OUTCOME":
                assert len(p) == 8, (name, line)
                _, _, index, task_id, native_wait, native_exec, arrive, service = p
                index = int(index)
                assert index not in outcomes
                outcomes[index] = dict(id=int(task_id),
                                       native_wait_ms=finite_nonnegative(native_wait),
                                       native_execution_ms=finite_nonnegative(native_exec),
                                       arrival_offset_ms=finite_nonnegative(arrive),
                                       requested_service_ms=finite_nonnegative(service))
            elif p[0] == "STAGE50_FINISH":
                assert len(p) == 8, (name, line)
                _, _, index, task_id, clock, wait, execution, service = p
                index = int(index)
                assert index not in finishes
                finishes[index] = dict(id=int(task_id),
                                       callback_ms=finite_nonnegative(clock),
                                       native_wait_ms=finite_nonnegative(wait),
                                       native_execution_ms=finite_nonnegative(execution),
                                       requested_service_ms=finite_nonnegative(service))
        assert header is not None and done is not None
        assert math.isclose(float(header["minEventSec"]), EVENT_GAPS[case_index],
                            abs_tol=1e-10)
        assert int(done["submissions"]) == int(done["finishes"]) == 3
        assert len(submissions) == len(outcomes) == len(finishes) == 3
        all_ids = {v["id"] for v in outcomes.values()}
        assert len(all_ids) == 3 and set(submissions) == all_ids
        assert set(outcomes) == set(finishes) == {0, 1, 2}
        for ev in events:
            assert set(ev["exec_ids"]).issubset(all_ids)
            assert set(ev["wait_ids"]).issubset(all_ids)
            assert not (set(ev["exec_ids"]) & set(ev["wait_ids"]))
            assert len(ev["exec_ids"]) <= 1, (name, ev)
        states = {task_id: [] for task_id in all_ids}
        transitions = []
        current = {task_id: "ABSENT" for task_id in all_ids}
        for ev in events:
            for task_id in sorted(all_ids):
                state = ("EXEC" if task_id in ev["exec_ids"] else
                         "WAIT" if task_id in ev["wait_ids"] else "ABSENT")
                if state != current[task_id]:
                    transitions.append(dict(task_id=task_id, from_state=current[task_id],
                                            to_state=state, seq=ev["seq"],
                                            observed_at_ms=ev["clock_ms"],
                                            event=ev["kind"]))
                if state != "ABSENT":
                    states[task_id].append(dict(state=state, clock_ms=ev["clock_ms"],
                                                seq=ev["seq"], event=ev["kind"]))
                current[task_id] = state
        predicted_finish = 0.0
        ideal_wait = {}
        for submitted, task_id in sorted((v, k) for k, v in submissions.items()):
            idx = next(i for i, v in outcomes.items() if v["id"] == task_id)
            ideal_start = max(predicted_finish, submitted)
            ideal_wait[task_id] = ideal_start - submitted
            predicted_finish = ideal_start + SERVICE[idx]
        rows = []
        for idx in range(3):
            o, f = outcomes[idx], finishes[idx]
            task_id = o["id"]
            assert task_id == f["id"]
            assert abs(o["native_wait_ms"] - f["native_wait_ms"]) <= TOL
            assert abs(o["native_execution_ms"] - f["native_execution_ms"]) <= TOL
            assert abs(o["requested_service_ms"] - SERVICE[idx]) <= TOL
            assert abs(o["arrival_offset_ms"] - ARRIVE[idx]) <= TOL
            observed_exec = [x["clock_ms"] for x in states[task_id] if x["state"] == "EXEC"]
            observed_wait = [x["clock_ms"] for x in states[task_id] if x["state"] == "WAIT"]
            assert observed_exec, ("no EXEC observation", name, task_id)
            first_exec = observed_exec[0]
            assert first_exec + TOL >= submissions[task_id]
            rows.append(dict(task_index=idx, cloudlet_id=task_id,
                             observed_submit_ms=submissions[task_id],
                             first_wait_list_observation_ms=observed_wait[0] if observed_wait else None,
                             first_exec_list_observation_ms=first_exec,
                             last_exec_list_observation_ms=observed_exec[-1],
                             finish_callback_ms=f["callback_ms"],
                             reported_native_wait_ms=o["native_wait_ms"],
                             reported_native_execution_ms=o["native_execution_ms"],
                             ideal_strict_fcfs_wait_ms=ideal_wait[task_id],
                             exec_observed_minus_submit_ms=first_exec - submissions[task_id],
                             reported_wait_minus_exec_observation_ms=(
                                 o["native_wait_ms"] - (first_exec - submissions[task_id]))))
        output.append(dict(case=name, event_gap_s=EVENT_GAPS[case_index],
                           rows=rows, transitions=transitions,
                           transition_wait_to_exec=sum(
                               x["from_state"] == "WAIT" and x["to_state"] == "EXEC"
                               for x in transitions),
                           transition_exec_to_wait=sum(
                               x["from_state"] == "EXEC" and x["to_state"] == "WAIT"
                               for x in transitions),
                           note="EXEC list snapshots are not exact CPU-start events."))
    return dict(status="PASS", original_30k_cross_engine_parity="UNRESOLVED_FAIL",
                claim_of_native_strict_fcfs_equivalence=False, cases=output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    data = audit(Path(args.input).read_text().splitlines())
    dest = Path(args.out)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(data, indent=2, sort_keys=True, allow_nan=False) + "\n")
    print("JPDC_STAGE50_NATIVE_QUEUE_TRANSITION_AUDIT_PASS")
