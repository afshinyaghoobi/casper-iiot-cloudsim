#!/usr/bin/env python3
"""Generated E45 only: scale CASPER_FULL conformal q at candidate scoring (not calibration data)."""
import argparse
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--scale",type=float,required=True);args=p.parse_args()
if args.scale not in (0.9,1.1):raise SystemExit("Only predeclared q scales 0.9 or 1.1 allowed")
src=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=src.read_text()
old="upper[p]=pred[k]+eta*q*sigma;"
new=f"upper[p]=pred[k]+eta*q*sigma*(policy==Policy.CASPER_FULL?{args.scale:.1f}:1.0);"
if s.count(old)!=1:raise SystemExit("Q_SCALE_PATCH_FAIL unexpected generated E45 source")
src.write_text(s.replace(old,new))
print("Q_SCALE_PATCH_PASS",args.scale)
