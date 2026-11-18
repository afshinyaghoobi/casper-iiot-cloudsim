package org.casperiiot.jpdc;

import java.util.*;
import java.util.stream.Collectors;

import org.cloudsimplus.brokers.DatacenterBrokerSimple;
import org.cloudsimplus.cloudlets.Cloudlet;
import org.cloudsimplus.cloudlets.CloudletExecution;
import org.cloudsimplus.cloudlets.CloudletSimple;
import org.cloudsimplus.core.CloudSimPlus;
import org.cloudsimplus.datacenters.DatacenterSimple;
import org.cloudsimplus.hosts.HostSimple;
import org.cloudsimplus.resources.Pe;
import org.cloudsimplus.resources.PeSimple;
import org.cloudsimplus.schedulers.cloudlet.CloudletSchedulerSpaceShared;
import org.cloudsimplus.utilizationmodels.UtilizationModelFull;
import org.cloudsimplus.vms.VmSimple;

/**
 * FROZEN A2 prospective synthetic 24-condition native semantics experiment.
 * See jpdc/JPDC_A2_BOUNDED_GENERALIZATION_PREREG_2026-11-17.md.
 * No CASPER algorithm changes and no claim of independent real workload.
 */
public final class NativeA3TimeOriginDiagnostic {
    private static final long MIPS=1_000_000_000L;
    private static final double BASE_SEC=1.0;
    private static final double[] SERVICE={8,13,5,19,7,11,17,6,14,9,16,10};
    private static final double[][] JITTER={
        {0,0,0,0,0,0,0,0,0,0,0,0},
        {0,0.4,0.8,0,0.4,0.8,0,0.4,0.8,0,0.4,0.8},
        {0.8,0.4,0,0.8,0.4,0,0.8,0.4,0,0.8,0.4,0}
    };
    private static String ids(List<CloudletExecution> items) {
        return items.stream().map(j->Long.toString(j.getId())).collect(Collectors.joining(";"));
    }
    private static final class Passive extends CloudletSchedulerSpaceShared {
        private final CloudSimPlus sim;
        private final String name;
        private final List<String> events;
        Passive(CloudSimPlus sim,String name,List<String> events){
            this.sim=sim;this.name=name;this.events=events;
        }
        @Override
        protected double cloudletSubmitInternal(CloudletExecution job,double transfer){
            events.add(String.format(Locale.US,"A2_SUBMIT,%s,BEFORE,%.12f,%d,%s,%s",
                name,sim.clock()*1000,job.getId(),ids(getCloudletExecList()),ids(getCloudletWaitingList())));
            double ret=super.cloudletSubmitInternal(job,transfer);
            events.add(String.format(Locale.US,"A2_SUBMIT,%s,AFTER,%.12f,%d,%s,%s",
                name,sim.clock()*1000,job.getId(),ids(getCloudletExecList()),ids(getCloudletWaitingList())));
            return ret;
        }
    }
    private static void execute(String family,int seed,double eventGap,int pes){
        String name=String.format(Locale.US,"%s_S%d_%s_P%d",family,seed,eventGap<0.001?"1US":"5MS",pes);
        CloudSimPlus sim=new CloudSimPlus(eventGap);
        List<String> events=new ArrayList<>();
        Passive scheduler=new Passive(sim,name,events);
        List<Pe> hostPes=new ArrayList<>();
        for(int i=0;i<pes;i++)hostPes.add(new PeSimple(MIPS+1_000_000));
        HostSimple host=new HostSimple(16384,100_000,100_000,hostPes);
        new DatacenterSimple(sim,List.of(host));
        VmSimple vm=new VmSimple(MIPS,pes);
        vm.setRam(4096).setBw(10_000).setSize(100_000).setCloudletScheduler(scheduler);
        DatacenterBrokerSimple broker=new DatacenterBrokerSimple(sim);
        broker.submitVmList(List.of(vm));
        List<Cloudlet> jobs=new ArrayList<>();
        for(int i=0;i<SERVICE.length;i++){
            final int index=i;
            double arrival=(family.equals("STAGGERED")?3*i:12*(i/3))+JITTER[seed][i];
            Cloudlet c=new CloudletSimple(Math.round(SERVICE[i]/1000.0*MIPS),1);
            c.setSubmissionDelay(BASE_SEC+arrival/1000.0);
            c.setUtilizationModelCpu(new UtilizationModelFull());
            c.addOnFinishListener(info->{
                Cloudlet done=info.getCloudlet();
                events.add(String.format(Locale.US,
                    "A2_FINISH,%s,%d,%d,%.12f,%.12f,%.12f,%.12f,%.12f",
                    name,index,done.getId(),sim.clock()*1000.0,
                    done.getStartWaitTime()*1000.0,done.getTotalExecutionTime()*1000.0,
                    arrival,SERVICE[index]));
            });
            c.addOnFinishListener(info->{
                Cloudlet done=info.getCloudlet();
                events.add(String.format(Locale.US,
                    "A3_CLOCK,%s,%d,%.12f,%.12f,%.12f,%.12f",
                    name,index,done.getDcArrivalTime()*1000.0,
                    done.getStartTime()*1000.0,done.getStartWaitTime()*1000.0,
                    sim.clock()*1000.0));
            });
            jobs.add(c);
        }
        broker.submitCloudletList(jobs);
        sim.start();
        int completed=broker.getCloudletFinishedList().size();
        System.out.printf(Locale.US,"A2_CASE,%s,%s,%d,%.9f,%d%n",name,family,seed,eventGap,pes);
        for(String e:events)System.out.println(e);
        System.out.printf(Locale.US,"A2_DONE,%s,%d%n",name,completed);
        if(completed!=12)throw new AssertionError("Incomplete native A2 case "+name);
    }
    public static void main(String[] args){
        for(String family:new String[]{"STAGGERED","BURSTY"})
            for(int seed=0;seed<3;seed++)
                for(double gap:new double[]{0.000001,0.005})
                    for(int pes:new int[]{1,2})
                        execute(family,seed,gap,pes);
        System.out.println("JPDC_A2_NATIVE_24_CASES_COMPLETE");
    }
}
