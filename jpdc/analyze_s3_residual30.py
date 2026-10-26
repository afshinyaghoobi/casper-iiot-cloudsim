#!/usr/bin/env python3
"""Aggregate audited S3 candidate failures across the exact thirty frozen seed indices."""
import re,json,csv
from pathlib import Path
root=Path("residual30_analysis")
files=sorted(root.glob("input/**/seed_*.log"))
assert len(files)==30,len(files)
keys=("seed","missingCandidates","affectedMissCandidates","allCandidates","netIncrementSum","queueResidualSum","serviceResidualSum","etaSum","excessAboveUpperSum","absQueueResidualSum","absServiceResidualSum")
regex=re.compile(r"^S3_DECOMP " + " ".join(k+r"=([-+\d.eE]+)" for k in keys)+r"$",re.M)
records=[]
for f in files:
    m=regex.findall(f.read_text())
    assert len(m)==1,(f,m)
    row={k:(int(v) if k in ("seed","missingCandidates","affectedMissCandidates","allCandidates") else float(v)) for k,v in zip(keys,m[0])}
    assert row["seed"]==4202202600+int(f.stem.split("_")[-1])
    assert row["affectedMissCandidates"]<=row["missingCandidates"]<=row["allCandidates"]
    assert row["absQueueResidualSum"]+1e-5>=abs(row["queueResidualSum"])
    assert row["absServiceResidualSum"]+1e-5>=abs(row["serviceResidualSum"])
    records.append(row)
assert {r["seed"] for r in records}==set(range(4202202600,4202202630))
totals={k:sum(r[k] for r in records) for k in keys if k!="seed"}
report=dict(status="PASS",n_seeds=30,totals=totals,means_per_failing_candidate={k:totals[k]/totals["missingCandidates"] for k in keys if k not in ("seed","missingCandidates","affectedMissCandidates","allCandidates")},caveat="Conditioned on candidate interval misses. Signed and absolute residual components describe these selected failures, not causal contributions or all dispatched tasks.",records=records)
root.mkdir(exist_ok=True)
(root/"s3_residual30.json").write_text(json.dumps(report,indent=2))
with (root/"s3_residual30.csv").open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=keys)
    w.writeheader();w.writerows(records)
print("S3_RESIDUAL30_PASS",json.dumps(totals,sort_keys=True))
