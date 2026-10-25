import re,csv,json,math
from pathlib import Path
root=Path("window_analysis")
files=list(root.glob("input/**/seed_*.log"))
assert len(files)==30, f"expected 30 log files, found {len(files)}"
rx=re.compile(r"JPDC_WINDOW scenario=S4_COMPOUND seed=(\d+) size=(250|500|1000|2000|POST) lateDvr=([0-9.]+) lateFwc=([0-9.]+)")
rows=[]
for file in files:
    found=rx.findall(file.read_text())
    assert len(found)==5,(str(file),len(found))
    for seed,w,dvr,fwc in found:
        rows.append(dict(seed=int(seed),window=w,dvr=float(dvr),fwc=float(fwc)))
assert sorted(set(x["seed"] for x in rows))==list(range(4202202600,4202202630))
for seed in range(4202202600,4202202630):
    assert {r["window"] for r in rows if r["seed"]==seed}=={"250","500","1000","2000","POST"}
summary=[]
for window in ("250","500","1000","2000","POST"):
    z=[r for r in rows if r["window"]==window]
    summary.append(dict(window=window,seed_count=len(z),mean_dvr=sum(x["dvr"] for x in z)/len(z),mean_fwc=sum(x["fwc"] for x in z)/len(z)))
by={(r["seed"],r["window"]):r for r in rows}
d=[by[s,"POST"]["fwc"]-by[s,"250"]["fwc"] for s in range(4202202600,4202202630)]
result={"seed_count":30,"rows":len(rows),"summary":summary,"paired_post_minus_250_fwc_mean":sum(d)/len(d),"seeds_lower_post_fwc":sum(x<0 for x in d),"seeds_higher_post_fwc":sum(x>0 for x in d),"seeds_equal":sum(x==0 for x in d)}
with (root/"s4_window30.csv").open("w",newline="") as f:
    writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
(root/"s4_window30_summary.json").write_text(json.dumps(result,indent=2))
print("WINDOW30_PASS",json.dumps(result))
