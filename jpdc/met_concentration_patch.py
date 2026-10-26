from pathlib import Path
p=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=p.read_text()
needle="final Acc acc=new Acc();"
assert s.count(needle)==1
s=s.replace(needle,needle+"""
        final long[] metDispatchCounts=new long[NODES];
""")
needle="final double nominal=nominalServiceMs(t,nodes[j]);"
assert s.count(needle)==1
s=s.replace(needle,"""if(policy==Policy.ONLINE_MET_ADAPTED && t.index()>=CHANGE_TASK) metDispatchCounts[j]++;
            """+needle)
needle="return summarize(seed,n,scenario,policy,acc,affected);"
assert s.count(needle)==1
s=s.replace(needle,"""if(policy==Policy.ONLINE_MET_ADAPTED) {
            final long totalDispatched=java.util.Arrays.stream(metDispatchCounts).sum();
            final long maxNodeDispatch=java.util.Arrays.stream(metDispatchCounts).max().orElse(0);
            final long usedNodes=java.util.Arrays.stream(metDispatchCounts).filter(v->v>0).count();
            System.out.printf(java.util.Locale.US,"MET_CONCENTRATION scenario=%s seed=%d total=%d usedNodes=%d maxNodeTasks=%d maxNodeShare=%.9f%n",
                scenario.name(),seed,totalDispatched,usedNodes,maxNodeDispatch,totalDispatched==0?0:maxNodeDispatch/(double)totalDispatched);
        }
        """+needle)
p.write_text(s)
print("MET_CONCENTRATION_INSTRUMENT_PASS")
