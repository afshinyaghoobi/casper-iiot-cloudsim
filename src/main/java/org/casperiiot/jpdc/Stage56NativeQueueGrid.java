package org.casperiiot.jpdc;

import org.cloudsimplus.brokers.DatacenterBrokerSimple;
import org.cloudsimplus.cloudlets.Cloudlet;
import org.cloudsimplus.cloudlets.CloudletExecution;
import org.cloudsimplus.cloudlets.CloudletSimple;
import org.cloudsimplus.core.CloudSimPlus;
import org.cloudsimplus.datacenters.DatacenterSimple;
import org.cloudsimplus.hosts.HostSimple;
import org.cloudsimplus.resources.PeSimple;
import org.cloudsimplus.schedulers.MipsShare;
import org.cloudsimplus.schedulers.cloudlet.CloudletSchedulerSpaceShared;
import org.cloudsimplus.utilizationmodels.UtilizationModelFull;
import org.cloudsimplus.vms.Vm;
import org.cloudsimplus.vms.VmSimple;
import java.util.*;
import java.util.stream.Collectors;

/** Stage56 preregistered cross-runtime queue timing study.
 * Observation only: does not modify CASPER E42/E4.6 or CloudSim scheduler.
 */
public final class Stage56NativeQueueGrid {
    private static final long MIPS=1_000_000_000L;
    private static final double BASE_S=1.0;
    private static final double[] SVC={8.099623,4.730689,9.120283,6.4,11.3,4.5,7.2,12.7,3.6,10.2,5.1,8.8};
    private static final double[][] ARR={
        {0,75,150,225,300,375,450,525,600,675,750,825},
        {0,.2,.4,.6,.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2},
        {0,5.318920,8.0997406,25,25.5,30,50,55.4,55.6,75,80,84}
    };
    private static final String[] PROFILES={"ISOLATED","BURST","WAVES"};
    private static final double[] GAPS={.000001,.005,.02};

    private static String ids(List<CloudletExecution> list) {
        return list.stream().map(x->Long.toString(x.getId())).collect(Collectors.joining(";"));
    }
    private static final class PassiveScheduler extends CloudletSchedulerSpaceShared {
        private final CloudSimPlus sim;
        private final String caseName;
        private final List<String> logs;
        PassiveScheduler(CloudSimPlus sim,String caseName,List<String> logs){
            this.sim=sim;this.caseName=caseName;this.logs=logs;
        }
        private void record(String phase,CloudletExecution c) {
            logs.add(String.format(Locale.US,
                "STAGE56_SUBMIT,%s,%s,%.12f,%d,%s,%s",
                caseName,phase,sim.clock()*1000.0,c.getId(),
                ids(getCloudletExecList()),ids(getCloudletWaitingList())));
        }
        @Override protected double cloudletSubmitInternal(CloudletExecution job,double transfer){
            record("BEFORE",job);
            double next=super.cloudletSubmitInternal(job,transfer);
            record("AFTER",job);
            return next;
        }
        @Override public double updateProcessing(double now,MipsShare share){
            logs.add(String.format(Locale.US,
                "STAGE56_UPDATE,%s,BEFORE,%.12f,%s,%s",caseName,now*1000.,
                ids(getCloudletExecList()),ids(getCloudletWaitingList())));
            double next=super.updateProcessing(now,share);
            logs.add(String.format(Locale.US,
                "STAGE56_UPDATE,%s,AFTER,%.12f,%s,%s",caseName,now*1000.,
                ids(getCloudletExecList()),ids(getCloudletWaitingList())));
            return next;
        }
    }
    private static void one(int profile,int gapIndex){
        final String caseName=PROFILES[profile]+"_"+gapIndex;
        CloudSimPlus sim=new CloudSimPlus(GAPS[gapIndex]);
        List<String> logs=new ArrayList<>();
        PassiveScheduler sched=new PassiveScheduler(sim,caseName,logs);
        HostSimple host=new HostSimple(16384,100000,100000,
            List.of(new PeSimple(MIPS+1_000_000)));
        new DatacenterSimple(sim,List.of(host));
        Vm vm=new VmSimple(MIPS,1).setRam(4096).setBw(10000).setSize(100000)
                .setCloudletScheduler(sched);
        DatacenterBrokerSimple broker=new DatacenterBrokerSimple(sim);
        broker.submitVmList(List.of(vm));
        List<Cloudlet> jobs=new ArrayList<>();
        for(int i=0;i<SVC.length;i++){
            final int ix=i;
            long length=Math.max(1L,Math.round(SVC[i]*MIPS/1000.0));
            Cloudlet c=new CloudletSimple(length,1);
            c.setSubmissionDelay(BASE_S+ARR[profile][i]/1000.0);
            c.setUtilizationModelCpu(new UtilizationModelFull());
            c.addOnFinishListener(info->{
                Cloudlet done=info.getCloudlet();
                logs.add(String.format(Locale.US,"STAGE56_FINISH,%s,%d,%d,%.12f",
                    caseName,ix,done.getId(),sim.clock()*1000.0));
            });
            jobs.add(c);
        }
        broker.submitCloudletList(jobs);
        sim.start();
        if(broker.getCloudletFinishedList().size()!=SVC.length)
            throw new AssertionError("Stage56 missing finished real cloudlets");
        System.out.printf(Locale.US,"STAGE56_CASE,%s,%s,%.9f,%d%n",caseName,
            PROFILES[profile],GAPS[gapIndex],SVC.length);
        for(String x:logs)System.out.println(x);
        for(int i=0;i<SVC.length;i++){
            Cloudlet c=jobs.get(i);
            System.out.printf(Locale.US,
              "STAGE56_OUTCOME,%s,%d,%d,%.12f,%.12f,%.12f,%.12f%n",
              caseName,i,c.getId(),c.getStartWaitTime()*1000.0,
              c.getTotalExecutionTime()*1000.0,ARR[profile][i],SVC[i]);
        }
        System.out.printf(Locale.US,"STAGE56_END,%s,%d,%d,%d%n",caseName,
            logs.stream().filter(x->x.startsWith("STAGE56_SUBMIT,"+caseName+",BEFORE,")).count(),
            logs.stream().filter(x->x.startsWith("STAGE56_SUBMIT,"+caseName+",AFTER,")).count(),
            logs.stream().filter(x->x.startsWith("STAGE56_FINISH,"+caseName+",")).count());
    }
    public static void main(String[] args){
        for(int profile=0;profile<PROFILES.length;profile++)
            for(int gap=0;gap<GAPS.length;gap++)one(profile,gap);
        System.out.println("JPDC_STAGE56_NATIVE_GRID_COMPLETE");
    }
}
