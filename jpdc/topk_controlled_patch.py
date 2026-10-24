#!/usr/bin/env python3
"""Controlled K sensitivity: change ONLY deployment top-K; rank calibration stays frozen."""
import sys
from pathlib import Path
k=int(sys.argv[1])
assert k in (1,3)
p=Path('src/main/java/org/casperiiot/e45/E45Campaign.java')
s=p.read_text()
old='final int[] family=topK(pred,eligible,3);'
assert s.count(old)==1
s=s.replace(old,f'final int[] family=topK(pred,eligible,{k});')
p.write_text(s)
print('JPDC_TOPK_PATCH_PASS K='+str(k)+' CALIBRATION_UNCHANGED')
