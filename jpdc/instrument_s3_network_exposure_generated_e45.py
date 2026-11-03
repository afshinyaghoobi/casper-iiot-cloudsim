#!/usr/bin/env python3
"""Instrument generated E45 only: affected nodes + realized per-MISSION network exposure."""
from pathlib import Path
p=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=p.read_text()
anchor="        final boolean[] affected=affectedMask(seed,scenario);"
extra='''        if(policy==Policy.CASPER_FULL && scenario==Scenario.S3_HIDDEN_NETWORK_50LOSS){
            for(int aj=0;aj<NODES;aj++)
                System.out.printf(Locale.US,"JPDC_SHOCK_MASK,%d,%s,%s,%d,%b%n",
                        seed,scenario,policy,aj,affected[aj]);
        }'''
if s.count(anchor)!=1:raise SystemExit("MASK_INSTRUMENT_FAIL")
s=s.replace(anchor,anchor+"\n"+extra)
anchor2="            final double actualNet=nominalNetworkMs(t,nodes[j])*netMult;"
extra2='''            if(policy==Policy.CASPER_FULL && scenario==Scenario.S3_HIDDEN_NETWORK_50LOSS &&
               t.crit()==Crit.MISSION){
                System.out.printf(Locale.US,
                    "JPDC_NETWORK_EXPOSURE,%d,%s,%s,%d,%d,%b,%.9f,%.9f,%.9f,%.9f%n",
                    seed,scenario,policy,t.index(),j,affected[j],
                    nominalNetworkMs(t,nodes[j]),actualNet,netMult,pred[j]);
            }'''
if s.count(anchor2)!=1:raise SystemExit("NETWORK_INSTRUMENT_FAIL")
s=s.replace(anchor2,anchor2+"\n"+extra2)
p.write_text(s)
print("JPDC_NETWORK_EXPOSURE_INSTRUMENT_PASS")
