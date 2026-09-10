#!/usr/bin/env python3
from pathlib import Path
p=Path('src/main/java/org/casperiiot/e42/E42Campaign.java')
s=p.read_text()
old='new CloudSimPlus(0.0001)'
new='new CloudSimPlus(0.000001)'
n=s.count(old)
if n!=2: raise SystemExit(f'PATCH REFUSED: expected 2 current precision constructors, found {n}')
s=s.replace(old,new)
p.write_text(s)
print('E42_PRECISION_REFINE_PATCH PASS minTimeBetweenEvents=0.000001s (0.001ms)')
print('Purpose: satisfy prelocked <=2ms numerical service-parity gate before publication results.')
print('Scientific CASPER parameters changed: NO')
