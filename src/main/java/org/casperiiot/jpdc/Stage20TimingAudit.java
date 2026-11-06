package org.casperiiot.jpdc;

import org.cloudsimplus.brokers.DatacenterBrokerSimple;
import org.cloudsimplus.cloudlets.Cloudlet;
import org.cloudsimplus.cloudlets.CloudletExecution;
import org.cloudsimplus.cloudlets.CloudletSimple;
import org.cloudsimplus.core.CloudSimPlus;
import org.cloudsimplus.datacenters.DatacenterSimple;
import org.cloudsimplus.hosts.HostSimple;
import org.cloudsimplus.resources.PeSimple;
import org.cloudsimplus.schedulers.cloudlet.CloudletSchedulerSpaceShared;
import org.cloudsimplus.utilizationmodels.UtilizationModelFull;
import org.cloudsimplus.vms.Vm;
import org.cloudsimplus.vms.VmSimple;

import java.util.*;
import java.util.stream.Collectors;

/**
 * Stage20 PASSIVE event timing audit on the frozen Stage19 microfixtures.
 * No CASPER/E42 changes, no out-of-band manipulation of waiting queues.
 * Exact two cases preregistered; no case selection after outcomes.
 */
public final class Stage20TimingAudit {
    private static final long MIPS = 1_000_000_000L;
    private static final double BASE_SECONDS = 1.0;
    private static final double FINISH_FIRST_MS = 8.099623;
    private static final double SECOND_ARRIVE_MS = 5.318920;
    private static final double THIRD_ARRIVE_NEAR_MS = 8.0997406;
    private static final double THIRD_ARRIVE_LATE_MS = 10.0;
    private static final double[] SERVICE_MS = {8.099623,4.730689,9.120283};

    private static final class PassiveScheduler extends CloudletSchedulerSpaceShared {
        private final CloudSimPlus sim;
        private final String label;
        private final List<String> records;
        PassiveScheduler(final CloudSimPlus simulation, final String caseName,final List<String> out) {
            sim=simulation;label=caseName;records=out;
        }
        private static String ids(final List<CloudletExecution> tasks){
            return tasks.stream().map(c -> Long.toString(c.getId())).collect(Collectors.joining(";"));
        }
        private void snapshot(final String stage, final CloudletExecution cle){
            records.add(String.format(Locale.US,
                "STAGE20_SUBMIT,%s,%s,%.12f,%d,%s,%s",
                label,stage,sim.clock()*1000.0,cle.getId(),
                ids(getCloudletExecList()),ids(getCloudletWaitingList())));
        }
        @Override
        public double updateProcessing(final double currentTime,
                                       final org.cloudsimplus.schedulers.MipsShare share){
            records.add(String.format(Locale.US,
                "STAGE20_UPDATE,%s,BEFORE,%.12f,%s,%s",
                label,currentTime*1000.0,ids(getCloudletExecList()),ids(getCloudletWaitingList())));
            final double next=super.updateProcessing(currentTime,share);
            records.add(String.format(Locale.US,
                "STAGE20_UPDATE,%s,AFTER,%.12f,%s,%s",
                label,currentTime*1000.0,ids(getCloudletExecList()),ids(getCloudletWaitingList())));
            return next;
        }
        @Override
        protected double cloudletSubmitInternal(final CloudletExecution cle,final double transfer){
            snapshot("BEFORE",cle);
            final double r=super.cloudletSubmitInternal(cle,transfer);
            snapshot("AFTER",cle);
            return r;
        }
    }

    private static Cloudlet newCloudlet(final double durationMs,final double arrivalMs) {
        final long length=Math.max(1L,Math.round(durationMs/1000.0*MIPS));
        Cloudlet c=new CloudletSimple(length,1);
        c.setSubmissionDelay(BASE_SECONDS+arrivalMs/1000.0);
        c.setUtilizationModelCpu(new UtilizationModelFull());
        return c;
    }

    private static void runCase(final String name,final double lastArrivalMs) {
        final CloudSimPlus sim=new CloudSimPlus(0.000001);
        final List<String> log=new ArrayList<>();
        final PassiveScheduler scheduler=new PassiveScheduler(sim,name,log);
        final HostSimple host=new HostSimple(16384,100_000,100_000,
                List.of(new PeSimple(MIPS+1_000_000)));
        new DatacenterSimple(sim,List.of(host));
        final Vm vm=new VmSimple(MIPS,1)
            .setRam(4096).setBw(10_000).setSize(100_000)
            .setCloudletScheduler(scheduler);
        final DatacenterBrokerSimple broker=new DatacenterBrokerSimple(sim);
        broker.submitVmList(List.of(vm));
        final List<Cloudlet> jobs=List.of(
            newCloudlet(SERVICE_MS[0],0.0),
            newCloudlet(SERVICE_MS[1],SECOND_ARRIVE_MS),
            newCloudlet(SERVICE_MS[2],lastArrivalMs));
        for (int ordinal=0;ordinal<jobs.size();ordinal++){
            final int index=ordinal;
            jobs.get(index).addOnFinishListener(info -> {
                final Cloudlet c=info.getCloudlet();
                log.add(String.format(Locale.US,
                    "STAGE20_FINISH,%s,%d,%d,%.12f,%.12f,%.12f,%.12f",
                    name,index,c.getId(),sim.clock()*1000.0,
                    c.getStartWaitTime()*1000.0,
                    c.getTotalExecutionTime()*1000.0,
                    SERVICE_MS[index]));
            });
        }
        broker.submitCloudletList(jobs);
        sim.start();
        final List<Cloudlet> finished=broker.getCloudletFinishedList();
        if(finished.size()!=3)throw new AssertionError("not all three microfixture jobs completed");
        for(final String line:log)System.out.println(line);
        for(int i=0;i<jobs.size();i++){
            Cloudlet c=jobs.get(i);
            System.out.printf(Locale.US,"STAGE20_OUTCOME,%s,%d,%d,%.12f,%.12f%n",
                name,i,c.getId(),c.getStartWaitTime()*1000.0,c.getTotalExecutionTime()*1000.0);
        }
        System.out.printf(Locale.US,"STAGE20_CASE_DONE,%s,submissions=%d,finished=%d%n",
            name,log.stream().filter(x->x.contains(",BEFORE,")).count(),finished.size());
    }

    public static void main(String[] args) {
        runCase("NEAR_ORIGINAL_EVENT_GAP",THIRD_ARRIVE_NEAR_MS);
        runCase("LATE_AFTER_COMPLETION_CONTROL",THIRD_ARRIVE_LATE_MS);
        System.out.println("JPDC_STAGE20_ORIGINAL_FIXTURES_NATIVE_TIMING_CALLBACKS_EXECUTED");
    }
}
