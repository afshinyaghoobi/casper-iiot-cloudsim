#!/usr/bin/env python3
"""Read-only original calibration finish-event quantile inputs, GENERATED E45 ONLY."""
from pathlib import Path
p=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=p.read_text(encoding="utf-8")
changes=[
('''                    serviceByTier[tier(m.node)].add(serviceMs/Math.max(m.nominalServiceMs,1e-12));''',
'''                    serviceByTier[tier(m.node)].add(serviceMs/Math.max(m.nominalServiceMs,1e-12));
                    System.out.printf(Locale.US,"JPDC_CAL_REAL_SERVICE,%d,%d,%d,%d,%.17g%n",
                        seed,m.task.index(),m.node,tier(m.node),serviceMs/Math.max(m.nominalServiceMs,1e-12));'''),
('''                        scoreByRank[m.rank-1].add(s);
                        allScores.add(s);''',
'''                        scoreByRank[m.rank-1].add(s);
                        allScores.add(s);
                        System.out.printf(Locale.US,"JPDC_CAL_REAL_MISSION,%d,%d,%d,%d,%.17g%n",
                            seed,m.task.index(),m.rank,m.node,s);'''),
('''        System.out.printf(Locale.US,
                "CALIBRATION rankN=%s''',
'''        System.out.printf(Locale.US,
            "JPDC_CAL_REAL_SUMMARY,%d,%s,%.17g,%s,%s,%s%n",
            seed,Arrays.toString(qRank).replace(",",";"),qGlobal,
            Arrays.toString(tierThr).replace(",",";"),
            Arrays.toString(rankN).replace(",",";"),
            Arrays.toString(tierN).replace(",",";"));
        System.out.printf(Locale.US,
                "CALIBRATION rankN=%s''')
]
for old,new in changes:
    if s.count(old)!=1:raise SystemExit("JPDC_CAL_REAL_INSTRUMENT_ANCHOR_FAIL "+old[:100])
    s=s.replace(old,new)
if s.count("JPDC_CAL_REAL_SERVICE")!=1 or s.count("JPDC_CAL_REAL_MISSION")!=1:
    raise SystemExit("calibration source replacement mismatch")
p.write_text(s,encoding="utf-8")
print("JPDC_REAL_CALIBRATION_EVENT_PATCH_PASS")
