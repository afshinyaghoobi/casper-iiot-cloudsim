#!/usr/bin/env python3
"""Sharp integer bounds on S3 misses in affected/unaffected candidate strata.
Input: CSV artifact of GitHub Actions run 40517387076.
"""
import argparse,csv,hashlib,json
from pathlib import Path
def analyze(path):
    raw=path.read_bytes()
    expected="78fd57691aa3fabd7a3d84fddac28903c66b173f7165def809b7ec374685321c"
    assert hashlib.sha256(raw).hexdigest()==expected, "wrong reference CSV"
    rows=list(csv.DictReader(raw.decode().splitlines()))
    assert len(rows)==90
    d={}
    for r in rows:
        s,w=int(r['seed']),int(r['window'])
        n,a,m=[int(r[k]) for k in ('count','affected','misses')]
        assert 0<=a<=n and 0<=m<=n and (s,w) not in d
        d[s,w]=(n,a,m)
    assert set(d)=={(4202202600+s,w) for s in range(30) for w in range(3)}
    out={'source_run':40517387076,'sha256':expected,'windows':{},'zero_affected_nonzero_miss':[]}
    for (s,w),(n,a,m) in sorted(d.items()):
        if a==0 and m>0: out['zero_affected_nonzero_miss'].append({'seed':s,'window':w,'misses':m})
    for w in range(3):
        row=[v for (s,k),v in d.items() if k==w]
        N=sum(n for n,a,m in row);A=sum(a for n,a,m in row);M=sum(m for n,a,m in row);U=N-A
        lo=sum(max(0,m-(n-a)) for n,a,m in row);hi=sum(min(a,m) for n,a,m in row)
        out['windows'][str(w)]={'n':N,'affected':A,'unaffected':U,'misses':M,'affected_misses_bounds':[lo,hi],'unaffected_misses_bounds':[M-hi,M-lo],'affected_rate_bounds':[lo/A,hi/A],'unaffected_rate_bounds':[(M-hi)/U,(M-lo)/U]}
    return out
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('csv',type=Path);p.add_argument('--out',type=Path);a=p.parse_args()
    res=analyze(a.csv);content=json.dumps(res,indent=2,sort_keys=True)+'\n'
    if a.out:a.out.write_text(content)
    print(content)
