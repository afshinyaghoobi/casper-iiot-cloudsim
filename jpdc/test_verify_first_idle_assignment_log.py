#!/usr/bin/env python3
"""Regression tests for fail-closed node-assignment logs. No CloudSim runs."""
from verify_first_idle_assignment_log import audit, SCENARIOS, POLICIES

def main():
    counts=", ".join(["30000"]+["0"]*23)
    lines=[f"JPDC_NODE_ASSIGNMENTS scenario={s} policy={p} seed=4202202600 counts=[{counts}]"
        for s in sorted(SCENARIOS) for p in sorted(POLICIES)]
    assert len(audit("\n".join(lines)))==45
    bad_cases={
        "malformed extra record":lines+["JPDC_NODE_ASSIGNMENTS unexpected format"],
        "malformed count":lines[:-1]+[lines[-1].split(" counts=")[0]+" counts=[1]"],
        "duplicate":lines+[lines[0]],
        "incomplete grid":lines[:-1],
    }
    for label,example in bad_cases.items():
        try: audit("\n".join(example))
        except ValueError: pass
        else: raise AssertionError(f"accepted {label}")
    print("FIRST_IDLE_ASSIGNMENT_VALIDATOR_REGRESSION_PASS 1 valid + 4 invalid cases")

if __name__=="__main__": main()
