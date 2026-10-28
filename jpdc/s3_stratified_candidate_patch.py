#!/usr/bin/env python3
"""Add affected-status-stratified counters to a GENERATED E45 Java campaign.

Must be executed after tools/e45_generate.py and jpdc/s3_all_candidate_patch.py.
Never changes committed source or the frozen E4.6 tag.
"""
from pathlib import Path
p=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=p.read_text()
needle="        final double[][] s3all=new double[3][8];"
assert s.count(needle)==1
s=s.replace(needle,"        final long[][][] s3strata=new long[3][2][2]; // window,affected(0/1),count/miss\n"+needle)
needle='                            s3all[window][0]++;'
assert s.count(needle)==1
s=s.replace(needle,'''                            final int stratum=affected[node]?1:0;
                            s3strata[window][stratum][0]++;
                            if(actualAudit[ix]>upper[ix])s3strata[window][stratum][1]++;
'''+needle)
needle='                double[] x=s3all[win];'
assert s.count(needle)==1
s=s.replace(needle,'''                System.out.printf(java.util.Locale.US,
                    "S3_STRATA seed=%d window=%d unaffectedN=%d unaffectedMiss=%d affectedN=%d affectedMiss=%d%n",
                    seed,win,s3strata[win][0][0],s3strata[win][0][1],s3strata[win][1][0],s3strata[win][1][1]);
'''+needle)
p.write_text(s)
print("S3_STRATA_PATCH_PASS")
