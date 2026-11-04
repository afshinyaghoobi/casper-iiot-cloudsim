#!/usr/bin/env python3
"""Observe CASPER policy MISSION inputs and chosen decision, GENERATED E45 only.

No edit to frozen E42/E4.6, no changes to decision path.
"""
from pathlib import Path
p=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=p.read_text(encoding="utf-8")
anchor="""            if(j<0) j=argMin(pred,x->true);

            final double nominal=nominalServiceMs(t,nodes[j]);"""
replacement="""            if(j<0) j=argMin(pred,x->true);

            // Record ALL decision inputs for independent cross-language replay.
            // semicolon-separated arrays retain full Java double precision.
            if(scenario==Scenario.S3_HIDDEN_NETWORK_50LOSS &&
               t.crit()==Crit.MISSION &&
               (policy==Policy.CASPER_FULL || policy==Policy.CASPER_HEALTH_STATIC)){
                final double[] sigmaMultForDecision=new double[NODES];
                for(int p=0;p<NODES;p++) sigmaMultForDecision[p]=nodes[p].sigmaMult();
                System.out.printf(Locale.US,
                    "JPDC_POLICY_DECISION,%d,%s,%s,%d,%s,%.17g,%.17g,%d,%d,%b,%s,%s,%s,%s%n",
                    seed,scenario,policy,t.index(),t.crit(),t.deadlineMs(),eta,
                    j,chosenRank,certified,
                    Arrays.toString(pred).replace(",",";"),
                    Arrays.toString(alarmMask).replace(",",";"),
                    Arrays.toString(sigmaMultForDecision).replace(",",";"),
                    Arrays.toString(cal.qRank).replace(",",";"));
            }

            final double nominal=nominalServiceMs(t,nodes[j]);"""
if s.count(anchor)!=1 or "JPDC_POLICY_DECISION" in s:
    raise SystemExit("JPDC_POLICY_DECISION_PATCH_FAIL: exactly one original mapper anchor required")
p.write_text(s.replace(anchor,replacement),encoding="utf-8")
print("JPDC_POLICY_DECISION_INSTRUMENT_PASS")
