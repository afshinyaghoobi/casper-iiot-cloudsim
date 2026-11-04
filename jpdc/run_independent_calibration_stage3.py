#!/usr/bin/env python3
"""Prespecified Stage3 native calibration matrix; independent physical outcomes."""
import argparse,json,math
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate,CAL_SIZE
SEEDS=(50,51)

def execute():
    results=[]
    for seed in SEEDS:
        result=calibrate(seed,CAL_SIZE)
        assert result["status"]=="PASS" and result["calibration_tasks"]==80000
        assert result["postburnin_service_ratio_count"]==70000
        assert result["mission_score_count"]==sum(result["rank_counts"])
        assert all(math.isfinite(x) and x>0 for x in [
            *result["q_rank"],result["q_global"],*result["tier_thresholds"]])
        assert sum(result["tier_counts"])==70000
        results.append(result)
        print("INDEPENDENT_CALIBRATION",seed,"rank_n",result["rank_counts"],
              "q_rank",result["q_rank"],"q_global",result["q_global"],
              "health_n",result["tier_counts"],
              "tier_thresholds",result["tier_thresholds"],
              "probes",result["actual_probes"])
    assert len(results)==2
    return {"status":"PASS","stage":"native independent 80k stochastic calibration",
            "scientific_claim":"conditional on strictly FIFO native Python physical engine, NOT CloudSim equivalence",
            "results":results}

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",required=True)
    args=parser.parse_args()
    report=execute()
    p=Path(args.out);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(report,sort_keys=True,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print("JPDC_NATIVE_PHYSICAL_CALIBRATION_STAGE3_PASS")
