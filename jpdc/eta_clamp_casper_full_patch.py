#!/usr/bin/env python3
"""Generated-E45-only causal ablation: clamp eta for CASPER_FULL at dispatch.

Apply after tools/e45_generate.py, to a separate worktree/output run.
Do not modify frozen E42 or E4.6. Keep all policies and outcome feedback.
"""
from pathlib import Path
p=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=p.read_text()
old="            final double eta=policy.adaptive?e17.etaBeforeOutcome():1.0;"
new=("            // JPDC exploratory intervention: preserve outcome feedback and all\n"
     "            // components except effective dispatch-time eta for CASPER_FULL.\n"
     "            final double eta=policy==Policy.CASPER_FULL?1.0:\n"
     "                    (policy.adaptive?e17.etaBeforeOutcome():1.0);")
if s.count(old)!=1 or "JPDC exploratory intervention" in s:
    raise SystemExit("ETA_CLAMP_FAIL: unexpected E45 source or already patched")
s=s.replace(old,new)
p.write_text(s)
print("ETA_CLAMP_CASPER_FULL_PASS")
