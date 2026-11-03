#!/usr/bin/env python3
"""Strictly alter generated E45 S3 affected-mask only, for fixed six node indices."""
import argparse
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument("--nodes",required=True,help="6 comma separated 0..20 node indices")
a=p.parse_args()
try: nodes=[int(x) for x in a.nodes.split(",")]
except ValueError as e:raise SystemExit(str(e))
if len(nodes)!=6 or len(set(nodes))!=6 or any(x<0 or x>=21 for x in nodes):
    raise SystemExit("MASK_OVERRIDE_FAIL expected six distinct nodes 0..20")
file=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=file.read_text()
anchor="        for(int k=0;k<6;k++)m[a.get(k)]=true;"
statement='''        // Diagnostic-only S3 affected-mask intervention, applied to all policies.
        if(s==Scenario.S3_HIDDEN_NETWORK_50LOSS){
            for(int j:new int[]{'''+",".join(map(str,nodes))+'''})m[j]=true;
            return m;
        }
'''
if s.count(anchor)!=1:raise SystemExit("MASK_OVERRIDE_FAIL unexpected frozen-source-generated site")
file.write_text(s.replace(anchor,statement+anchor))
print("JPDC_S3_FIXED_MASK_PATCH_PASS",nodes)
