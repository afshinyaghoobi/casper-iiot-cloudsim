import re,glob,csv,json
from pathlib import Path
logs=list(Path("s4_audit_archive").rglob("seed_*.log"))
assert len(logs)==30, f"expected 30 logs; got {len(logs)}"
pattern=re.compile(r"JPDC_S4_AUDIT seed=(\d+) mission=(\d+) high=(\d+) normal=(\d+) postMissionAffected=(\d+) lateMissionAffected=(\d+) lateMissionTotal=(\d+)")
rows=[]
for file in logs:
 matches=pattern.findall(file.read_text())
 assert len(matches)==1,(str(file),len(matches))
 vals=list(map(int,matches[0]))
 rows.append(dict(zip(["seed","mission","high","normal","postMissionAffected","lateMissionAffected","lateMissionTotal"],vals)))
assert sorted(r["seed"] for r in rows)==list(range(4202202600,4202202630))
assert all(r["lateMissionTotal"]==250 and 0<=r["lateMissionAffected"]<=r["postMissionAffected"]<=r["mission"] for r in rows)
rows.sort(key=lambda r:r["seed"])
totals={key:sum(r[key] for r in rows) for key in rows[0] if key!="seed"}
totals["seeds_with_late_exposure"]=sum(r["lateMissionAffected"]>0 for r in rows)
with open("s4_audit_summary.csv","w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
Path("s4_audit_summary.json").write_text(json.dumps(totals,indent=2))
print("S4_30SEED_AUDIT_PASS",json.dumps(totals))
