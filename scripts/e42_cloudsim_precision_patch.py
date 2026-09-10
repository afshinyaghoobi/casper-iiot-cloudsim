#!/usr/bin/env python3
from pathlib import Path
p=Path('src/main/java/org/casperiiot/e42/E42Campaign.java')
s=p.read_text()
changes=[
 ('final CloudSimPlus sim = new CloudSimPlus();','final CloudSimPlus sim = new CloudSimPlus(0.0001);'),
 ('final CloudSimPlus sim=new CloudSimPlus();','final CloudSimPlus sim=new CloudSimPlus(0.0001);')
]
for old,new in changes:
    n=s.count(old)
    if n!=1: raise SystemExit(f'PATCH REFUSED: expected one occurrence of {old!r}, found {n}')
    s=s.replace(old,new)
if s.count('new CloudSimPlus(0.0001)')!=2:
    raise SystemExit('PATCH REFUSED: precision constructor count mismatch')
p.write_text(s)
print('E42_CLOUDSIM_PRECISION_PATCH PASS minTimeBetweenEvents=0.0001s (0.1ms)')
print('Scientific CASPER parameters changed: NO')
