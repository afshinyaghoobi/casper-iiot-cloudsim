#!/usr/bin/env python3
"""Stage56 parser rejection checks on actual native log, no synthetic outcomes."""
import argparse
from pathlib import Path
from audit_stage56_java_python_queue_grid import audit

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--input",required=True)
    a=p.parse_args()
    lines=Path(a.input).read_text().splitlines()
    assert audit(lines)["status"] in ("PASS","AUDIT_PASS_WITH_UNFINISHED_TASKS")
    variants=[
        [x for x in lines if x!="JPDC_STAGE56_NATIVE_GRID_COMPLETE"],
        [x for x in lines if not x.startswith("STAGE56_END,ISOLATED_0,")],
        [x for x in lines if not x.startswith("STAGE56_SUBMIT,WAVES_2,BEFORE,")],
        [x.replace("STAGE56_SUBMIT,BURST_1,AFTER,","STAGE56_SUBMIT,BURST_1,INVALID,")
         if x.startswith("STAGE56_SUBMIT,BURST_1,AFTER,") else x for x in lines],
    ]
    for mutated in variants:
        try:audit(mutated)
        except (AssertionError,ValueError):
            continue
        raise AssertionError("Stage56 parser accepted incomplete or corrupted real trace")
    print("JPDC_STAGE56_REAL_LOG_NEGATIVE_CONTRACT_PASS")
