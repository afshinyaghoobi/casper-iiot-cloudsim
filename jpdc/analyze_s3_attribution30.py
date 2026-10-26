#!/usr/bin/env python3
"""Aggregate passive S3 family-wise network-shock attribution for 30 paired seeds."""
import csv,glob,json,re
from pathlib import Path
root=Path("s3_attribution30_analysis")
logs=sorted(root.glob("input/**/seed_*.log"))
assert len(logs)==30,f"Need 30 logs, found {len(logs)}"
pat=re.compile(r"^S3_AUDIT seed=(\d+) postMission=(\d+) familyAffected=(\d+) familyMiss=(\d+) affectedMiss=(\d+) candidates=(\d+) affectedCandidates=(\d+)$",re.M)
rows=[]
for f in logs:
    m=pat.findall(f.read_text())
    assert len(m)==1,(f,m)
    seed,post,affected,miss,affected_miss,candidates,affected_candidates=map(int,m[0])
    assert int(f.stem.split("_")[-1])+4202202600==seed
    assert 0<=affected_miss<=miss<=post and affected<=post
    assert 0<=affected_candidates<=candidates
    assert affected_miss<=affected
    assert candidates==post*3,(seed,candidates,post)
    rows.append(dict(seed=seed,postMission=post,familyAffected=affected,familyMiss=miss,affectedMiss=affected_miss,candidates=candidates,affectedCandidates=affected_candidates))
assert {r["seed"] for r in rows}==set(range(4202202600,4202202630))
totals={k:sum(r[k] for r in rows) for k in rows[0] if k!="seed"}
summary=dict(status="PASS",seed_count=30,totals=totals,miss_attribution_share=(totals["affectedMiss"]/totals["familyMiss"] if totals["familyMiss"] else None),post_shock_family_miss_rate=totals["familyMiss"]/totals["postMission"],notes=["These counts are across all post-shock missions, not the late-window FWC metric","AffectedMiss means at least one violated candidate bound belongs to a network-affected node; this is association, not proof of unique cause"],seed_rows=rows)
root.mkdir(exist_ok=True)
(root/"s3_attribution30.json").write_text(json.dumps(summary,indent=2))
with (root/"s3_attribution30.csv").open("w",newline="") as h:
    w=csv.DictWriter(h,fieldnames=list(rows[0]))
    w.writeheader();w.writerows(rows)
print("S3_ATTRIBUTION30_PASS seeds=30",json.dumps(totals,sort_keys=True),"share",summary["miss_attribution_share"])
