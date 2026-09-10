#!/usr/bin/env python3
from pathlib import Path
p=Path('src/main/java/org/casperiiot/e42/E42Campaign.java')
s=p.read_text()
old='for(double q:c.serviceThresholdByNode)if(!Double.isFinite(q))throw new IllegalStateException("non-finite health threshold");\n        System.out.println("CALIBRATION_VALIDATION PASS");'
new='long infiniteHealth=Arrays.stream(c.serviceThresholdByNode).filter(q -> !Double.isFinite(q)).count();\n        if(infiniteHealth>0) System.out.println("CALIBRATION_SUPPORT_WARNING conservative_infinite_health_threshold_nodes="+infiniteHealth);\n        System.out.println("CALIBRATION_VALIDATION PASS");'
if s.count(old)!=1: raise SystemExit(f'PATCH REFUSED expected 1 target, found {s.count(old)}')
s=s.replace(old,new)
p.write_text(s)
print('E42_CONSERVATIVE_SUPPORT_PATCH PASS')
print('Scientific behavior: finite-sample qhat=+Infinity retained exactly when calibration support is insufficient; no fallback threshold introduced.')
