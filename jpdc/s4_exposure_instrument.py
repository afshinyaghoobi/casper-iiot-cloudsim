#!/usr/bin/env python3
"""Instrument S3/S4 network candidate exposure without modifying scientific summaries."""
from pathlib import Path
p=Path('src/main/java/org/casperiiot/e45/E45Campaign.java')
s=p.read_text()
old='final Acc acc=new Acc();'
assert s.count(old)==1
s=s.replace(old,old+'''
        final long[] jpdcExposure={0,0,0,0}; // selected_affected, selected_post, affected_candidates, candidates_post
        final double[] jpdcNetworkExtra={0.0};
''')
old='final int k=family[p];'
assert s.count(old)==1
s=s.replace(old,old+'''
                        if(t.index()>=CHANGE_TASK) {
                            jpdcExposure[3]++;
                            if(affected[k]) jpdcExposure[2]++;
                        }
''')
old='final double actualNet=nominalNetworkMs(t,nodes[j])*netMult;'
assert s.count(old)==1
s=s.replace(old,old+'''
            if(t.index()>=CHANGE_TASK) {
                jpdcExposure[1]++;
                if(affected[j]) {
                    jpdcExposure[0]++;
                    jpdcNetworkExtra[0]+=actualNet-nominalNetworkMs(t,nodes[j]);
                }
            }
''')
old='return summarize(seed,n,scenario,policy,acc,affected);'
assert s.count(old)==1
s=s.replace(old,'''if(policy==Policy.CASPER_FULL && (scenario==Scenario.S3_HIDDEN_NETWORK_50LOSS || scenario==Scenario.S4_COMPOUND))
            System.out.printf(java.util.Locale.US,"NETWORK_EXPOSURE scenario=%s seed=%d selectedAffected=%d selectedPost=%d affectedCandidates=%d totalCandidates=%d totalNetworkExtraMs=%.9f%n",
                  scenario.name(),seed,jpdcExposure[0],jpdcExposure[1],jpdcExposure[2],jpdcExposure[3],jpdcNetworkExtra[0]);
        '''+old)
p.write_text(s)
print('NETWORK_EXPOSURE_INSTRUMENTATION_PASS')
