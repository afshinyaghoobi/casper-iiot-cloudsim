#!/usr/bin/env python3
"""Produce paper's A2 CSV and vector SVG from verified old original + posthoc audit JSON.
No new source simulations, no altered data, no subjective selected-case exclusion.
"""
import argparse,csv,json,html
from pathlib import Path
def draw(rows,out):
    width=1300
    left=235
    x0=left
    chartw=920
    top=105
    rowh=29
    bottom=65
    height=top+rowh*len(rows)+bottom
    vmax=max(max(r["max_abs_wait_discrepancy_ms"],r["oracle_max"]) for r in rows)
    vmax=(int(vmax/50)+1)*50
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="24-case native waiting versus requested FIFO and posthoc service FIFO comparison">',
       '<rect width="100%" height="100%" fill="white"/>',
       '<text x="26" y="31" font-family="Arial,sans-serif" font-size="19" font-weight="bold" fill="#172b4d">A2 native waiting discrepancy versus two FIFO references</text>',
       '<text x="26" y="55" font-family="Arial,sans-serif" font-size="13" fill="#38465b">24 synthetic fixed conditions; maximum absolute wait residual per 12-job case (ms)</text>',
       '<rect x="260" y="70" width="15" height="10" fill="#3168a6"/><text x="283" y="80" font-family="Arial" font-size="12">Requested-service FIFO (preregistered)</text>',
       '<rect x="685" y="70" width="15" height="10" fill="#d98b39"/><text x="708" y="80" font-family="Arial" font-size="12">Hindsight native-service FIFO (posthoc)</text>']
    for tick in range(0,vmax+1,50):
        x=x0+chartw*tick/vmax
        parts.append(f'<line x1="{x:.2f}" x2="{x:.2f}" y1="{top-4}" y2="{top+rowh*len(rows)}" stroke="#e3e8ec" stroke-width="1"/>')
        parts.append(f'<text x="{x:.2f}" y="{top-11}" font-family="Arial" font-size="11" fill="#697586" text-anchor="middle">{tick}</text>')
    for i,row in enumerate(rows):
        y=top+i*rowh
        name=html.escape(row["case"])
        req=row["max_abs_wait_discrepancy_ms"]
        oracle=row["oracle_max"]
        parts.append(f'<text x="{left-12}" y="{y+17}" font-family="Arial" font-size="11.5" text-anchor="end" fill="#263648">{name}</text>')
        parts.append(f'<rect x="{x0}" y="{y+4}" width="{chartw*req/vmax:.2f}" height="9" fill="#3168a6"/>')
        parts.append(f'<rect x="{x0}" y="{y+15}" width="{chartw*oracle/vmax:.2f}" height="9" fill="#d98b39"/>')
        if i%4==3:parts.append(f'<line x1="18" y1="{y+rowh}" x2="{width-45}" y2="{y+rowh}" stroke="#e3e8ec" stroke-width="1"/>')
    parts.append(f'<text x="{left}" y="{height-28}" font-family="Arial" font-size="12" fill="#38465b">Blue = main prespecified comparison; orange = descriptive after-completion service sensitivity, not a causal attribution.</text>')
    parts.append('</svg>')
    Path(out).write_text("\n".join(parts)+"\n")
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--primary",required=True);p.add_argument("--oracle",required=True)
    p.add_argument("--csv",required=True);p.add_argument("--svg",required=True)
    a=p.parse_args()
    primary=json.loads(Path(a.primary).read_text())
    oracle=json.loads(Path(a.oracle).read_text())
    first=primary["results"]; second={x["case"]:x for x in oracle["results"]}
    assert primary["native_cases"]==oracle["cases"]==24
    assert set(x["case"] for x in first)==set(second)
    rows=[]
    for x in sorted(first,key=lambda z:z["case"]):
        other=second[x["case"]]
        if abs(other["max_abs_wait_requested_ms"]-x["max_abs_wait_discrepancy_ms"])>1e-6:raise ValueError("primary and hindsight input mismatch")
        if x["native_reference_deadline_disagreements_25ms"]!=other["deadline25_disagree_requested"]:raise ValueError("deadline25 differs")
        if x["native_reference_deadline_disagreements_50ms"]!=other["deadline50_disagree_requested"]:raise ValueError("deadline50 differs")
        rows.append({"case":x["case"],"family":x["family"],"pes":x["pes"],"gap_sec":x["event_gap_sec"],
                     "max_abs_wait_discrepancy_ms":x["max_abs_wait_discrepancy_ms"],
                     "oracle_max":other["max_abs_wait_native_service_oracle_ms"],
                     "native_reference_deadline_disagreements_25ms":x["native_reference_deadline_disagreements_25ms"],
                     "oracle_deadline_disagreements_25ms":other["deadline25_disagree_oracle"],
                     "native_reference_deadline_disagreements_50ms":x["native_reference_deadline_disagreements_50ms"],
                     "oracle_deadline_disagreements_50ms":other["deadline50_disagree_oracle"]})
    with Path(a.csv).open("w",newline="") as fh:
        writer=csv.DictWriter(fh,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    draw(rows,a.svg)
    print(json.dumps({"cases":len(rows),"max_req":max(r["max_abs_wait_discrepancy_ms"] for r in rows),
         "max_oracle":max(r["oracle_max"] for r in rows),
         "d25req":sum(r["native_reference_deadline_disagreements_25ms"] for r in rows),
         "d25oracle":sum(r["oracle_deadline_disagreements_25ms"] for r in rows),
         "d50req":sum(r["native_reference_deadline_disagreements_50ms"] for r in rows),
         "d50oracle":sum(r["oracle_deadline_disagreements_50ms"] for r in rows)},sort_keys=True))
if __name__=="__main__":main()
