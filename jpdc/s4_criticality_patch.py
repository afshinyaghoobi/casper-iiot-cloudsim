from pathlib import Path
p=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=p.read_text()
needle="final Acc acc=new Acc();"
assert s.count(needle)==1
s=s.replace(needle,needle+"""
        final java.util.Set<Integer> auditAffectedMission=new java.util.HashSet<>();
        final long[] auditAffectedCrit={0,0,0};
""")
needle="final double actualNet=nominalNetworkMs(t,nodes[j])*netMult;"
assert s.count(needle)==1
s=s.replace(needle,needle+"""
            if(t.index()>=CHANGE_TASK && affected[j]) {
                switch(t.crit()) {
                    case MISSION -> {auditAffectedCrit[0]++; auditAffectedMission.add(t.index());}
                    case HIGH -> auditAffectedCrit[1]++;
                    case NORMAL -> auditAffectedCrit[2]++;
                }
            }
""")
needle="return summarize(seed,n,scenario,policy,acc,affected);"
assert s.count(needle)==1
s=s.replace(needle,"""
        if(policy==Policy.CASPER_FULL && scenario==Scenario.S4_COMPOUND) {
            final java.util.List<MissionRec> missions=acc.mission.stream().sorted(java.util.Comparator.comparingInt(MissionRec::taskIndex)).toList();
            final java.util.List<MissionRec> post=missions.stream().filter(MissionRec::post).toList();
            final java.util.List<MissionRec> late=post.size()<=LATE_MISSION?post:post.subList(post.size()-LATE_MISSION,post.size());
            final long postAffected=post.stream().filter(x->auditAffectedMission.contains(x.taskIndex())).count();
            final long lateAffected=late.stream().filter(x->auditAffectedMission.contains(x.taskIndex())).count();
            System.out.printf(java.util.Locale.US,"JPDC_S4_AUDIT seed=%d mission=%d high=%d normal=%d postMissionAffected=%d lateMissionAffected=%d lateMissionTotal=%d%n",seed,auditAffectedCrit[0],auditAffectedCrit[1],auditAffectedCrit[2],postAffected,lateAffected,late.size());
        }
        """+needle)
p.write_text(s)
print("S4_DIAGNOSTIC_PATCH_PASS")
