#!/usr/bin/env python3
"""Observe actual CloudletSchedulerSpaceShared submissions, generated E45 only.

Fail-closed unique patch. Deliberately does NOT modify E42/E4.6.
"""
from pathlib import Path
p=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=p.read_text(encoding="utf-8")
target="new CloudletSchedulerSpaceShared()"
anchor="    public static void main(String[] args) throws Exception {"
if s.count(target)!=1 or s.count(anchor)!=1 or "JPDC_SCHEDULER_SUBMIT" in s:
    raise SystemExit("JPDC_SCHEDULER_PROBE_ANCHOR_FAIL")
extension="""    // JPDC diagnostic-only wrapper: preserve the original SpaceShared logic.
    private static final class JPDCForensicQueueScheduler extends CloudletSchedulerSpaceShared {
        private final CloudSimPlus simulation;
        JPDCForensicQueueScheduler(final CloudSimPlus simulation){this.simulation=simulation;}
        private void snapshot(final String phase, final Cloudlet cloudlet, final double transfer){
            if(cloudlet.getId()<10898 || cloudlet.getId()>10902)return;
            final long[] running=getCloudletExecList().stream().mapToLong(x->x.getId()).toArray();
            final long[] waiting=getCloudletWaitingList().stream().mapToLong(x->x.getId()).toArray();
            System.out.printf(Locale.US,
                "JPDC_SCHEDULER_SUBMIT,%s,%.12f,%d,%d,%.12f,%s,%s%n",
                phase,simulation.clock()*1000.0,getVm().getId(),cloudlet.getId(),
                transfer*1000.0,Arrays.toString(running).replace(",",";"),
                Arrays.toString(waiting).replace(",",";"));
        }
        @Override
        public double cloudletSubmit(final Cloudlet cloudlet, final double fileTransferTime){
            snapshot("BEFORE",cloudlet,fileTransferTime);
            final double result=super.cloudletSubmit(cloudlet,fileTransferTime);
            snapshot("AFTER",cloudlet,fileTransferTime);
            return result;
        }
    }

"""
s=s.replace(target,"new JPDCForensicQueueScheduler(sim)").replace(anchor,extension+anchor)
p.write_text(s,encoding="utf-8")
print("JPDC_SCHEDULER_SUBMISSION_PROBE_PATCH_PASS")
