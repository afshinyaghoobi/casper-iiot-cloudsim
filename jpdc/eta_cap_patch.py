#!/usr/bin/env python3
"""Exploratory sensitivity of adaptive envelope upper cap. E4.6 remains frozen."""
import sys
from pathlib import Path
eta=int(sys.argv[1])
assert eta in (1,2,3)
p=Path('src/main/java/org/casperiiot/e45/E45Campaign.java')
s=p.read_text()
old='final double eta=policy.adaptive?e17.etaBeforeOutcome():1.0;'
new=f'final double eta=policy.adaptive?Math.min({float(eta):.1f},e17.etaBeforeOutcome()):1.0;'
assert s.count(old)==1
p.write_text(s.replace(old,new))
print(f'ETA_CAP_PATCH_PASS value={eta}, only deployment cap changed')
