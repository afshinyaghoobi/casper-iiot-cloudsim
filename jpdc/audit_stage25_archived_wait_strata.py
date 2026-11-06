#!/usr/bin/env python3
"""Frozen Stage25 WAIT-only queue residual post hoc descriptive audit.

Original artifact only; no simulator runs or inferred coverage guarantees.
"""
import argparse,json,math,statistics
from collections import defaultdict
from pathlib import Path

def q(seq,p):
    s=sorted(seq)
    return s[math.ceil(len(s)*p)-1]

def stats(items):
    e=[x["signed_wait_residual_ms"] for x in items]
    ae=[abs(v) for v in e]
    return dict(n=len(items),mean_signed_ms=statistics.mean(e),
                min_signed_ms=min(e),max_signed_ms=max(e),
                p95_abs_ms=q(ae,.95),p99_abs_ms=q(ae,.99),
                fraction_abs_gt_2ms=sum(v>2 for v in ae)/len(ae),
                positive_fraction=sum(v>1e-9 for v in e)/len(e),
                negative_fraction=sum(v< -1e-9 for v in e)/len(e))

def main(src,dest):
    x=json.loads(Path(src).read_text())
    assert x["status"]=="PASS" and x["seed"]==89 and len(x["rows"])==4
    report=[]
    for arm in x["rows"]:
        original=arm["stats"]
        trace=arm["trace"]
        assert len(trace)==12000
        all_s=stats(trace)
        assert math.isclose(all_s["p95_abs_ms"],original["abs_wait_error_q95_ms"],abs_tol=1e-10)
        groups=defaultdict(list)
        for t in trace:
            age=t["arrival_ms"]-t["last_queue_telemetry_ms"]
            assert 0<=age<=50+1e-9
            agebin=("0_to_10ms" if age<10 else
                    "10_to_25ms" if age<25 else "25_to_50ms")
            groups["class_"+t["task_class"]].append(t)
            groups["telemetry_"+agebin].append(t)
            groups["period_"+("post_index10000" if t["task_index"]>=10000 else "pre_index10000")].append(t)
        summaries={k:stats(v) for k,v in sorted(groups.items())}
        assert sum(summaries[f"class_{name}"]["n"] for name in ("NORMAL","HIGH","MISSION"))==12000
        assert summaries["period_pre_index10000"]["n"]==10000
        assert summaries["period_post_index10000"]["n"]==2000
        report.append(dict(scenario=original["scenario"],policy=original["policy"],
                           overall=all_s,conditional_exploratory=summaries))
        for name in sorted(summaries):
            print("STAGE25_ARCHIVED_STRATUM",json.dumps(dict(
                scenario=original["scenario"],policy=original["policy"],
                stratum=name,**summaries[name]),sort_keys=True))
    out=dict(status="PASS",scientific_scope="single seed89, post hoc artifact-only exploratory strata; not independent or calibrated",
             rows=report,unchanged_source_run_id=42254782412)
    p=Path(dest);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(out,sort_keys=True,indent=2)+"\n")
    print("JPDC_STAGE25_ARCHIVED_STRATIFIED_WAIT_RESIDUAL_AUDIT_PASS")
if __name__=="__main__":
    a=argparse.ArgumentParser()
    a.add_argument("--original",required=True);a.add_argument("--out",required=True)
    p=a.parse_args();main(p.original,p.out)
