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
import org.cloudsimplus.schedulers.MipsShare;
import org.cloudsimplus.utilizationmodels.UtilizationModelFull;
import org.cloudsimplus.vms.Vm;
import org.cloudsimplus.vms.VmSimple;

import java.util.*;
import java.util.stream.Collectors;

/** Stage49: predeclared fixed CloudSimPlus 8.5.7 clock-sensitivity micro experiment.
 * Original E42/E4.6 and Stage19/20 source are immutable.
 * All outputs are PASSIVE observations, never scheduler interference.
 */
public final class Stage49ClockSensitivity {
    private static final long MIPS = 1_000_000_000L;
    private static final double BASE_SECONDS=1.0;
    private static final double[] SERVICE_MS={8.099623,4.730689,9.120283};
    private static final double[] ARRIVE_MS={0.0,5.318920,8.0997406};
    private static final double[] MIN_EVENTS_SEC={0.000001,0.005,0.02};
    private static final String[] NAMES={"MICRO_1US","MICRO_5MS","MICRO_20MS"};

    private static String ids(final List<CloudletExecution> list) {
        return list.stream().map(e->Long.toString(e.getId())).collect(Collectors.joining(";"));
    }
    private static final class PassiveScheduler extends CloudletSchedulerSpaceShared {
        private final CloudSimPlus sim;
        private final String name;
        private final List<String> events;
        PassiveScheduler(CloudSimPlus sim,String name,List<String> events) {
            this.sim=sim;this.name=name;this.events=events;
        }
        private void submitLog(String moment,CloudletExecution job) {
            events.add(String.format(Locale.US,"STAGE49_SUBMIT,%s,%s,%.12f,%d,%s,%s",
                name,moment,sim.clock()*1000.0,job.getId(),
                ids(getCloudletExecList()),ids(getCloudletWaitingList())));
        }
        @Override
        protected double cloudletSubmitInternal(CloudletExecution job,double transfer) {
            submitLog("BEFORE",job);
            double r=super.cloudletSubmitInternal(job,transfer);
            submitLog("AFTER",job);
            return r;
        }
        @Override
        public double updateProcessing(double now,MipsShare share) {
            events.add(String.format(Locale.US,"STAGE49_UPDATE,%s,BEFORE,%.12f,%s,%s",
                name,now*1000.0,ids(getCloudletExecList()),ids(getCloudletWaitingList())));
            double next=super.updateProcessing(now,share);
            events.add(String.format(Locale.US,"STAGE49_UPDATE,%s,AFTER,%.12f,%s,%s",
                name,now*1000.0,ids(getCloudletExecList()),ids(getCloudletWaitingList())));
            return next;
        }
    }
    private static Cloudlet newCloudlet(double serviceMs,double arrivalMs) {
        long length=Math.max(1L,Math.round(serviceMs/1000.0*MIPS));
        Cloudlet c=new CloudletSimple(length,1);
        c.setSubmissionDelay(BASE_SECONDS+arrivalMs/1000.0);
        c.setUtilizationModelCpu(new UtilizationModelFull());
        return c;
    }
    private static void runCase(String name,double eventSec) {
        CloudSimPlus sim=new CloudSimPlus(eventSec);
        List<String> events=new ArrayList<>();
        PassiveScheduler scheduler=new PassiveScheduler(sim,name,events);
        HostSimple host=new HostSimple(16384,100_000,100_000,
            List.of(new PeSimple(MIPS+1_000_000)));
        new DatacenterSimple(sim,List.of(host));
        Vm vm=new VmSimple(MIPS,1).setRam(4096).setBw(10_000).setSize(100_000)
            .setCloudletScheduler(scheduler);
        DatacenterBrokerSimple broker=new DatacenterBrokerSimple(sim);
        broker.submitVmList(List.of(vm));
        List<Cloudlet> jobs=new ArrayList<>();
        for(int i=0;i<3;i++) {
            final int idx=i;
            Cloudlet c=newCloudlet(SERVICE_MS[i],ARRIVE_MS[i]);
            c.addOnFinishListener(info-> {
                Cloudlet done=info.getCloudlet();
                events.add(String.format(Locale.US,
                    "STAGE49_FINISH,%s,%d,%d,%.12f,%.12f,%.12f,%.12f",
                    name,idx,done.getId(),sim.clock()*1000.0,
                    done.getStartWaitTime()*1000.0,
                    done.getTotalExecutionTime()*1000.0,
                    SERVICE_MS[idx]));
            });
            jobs.add(c);
        }
        broker.submitCloudletList(jobs);
        sim.start();
        if(broker.getCloudletFinishedList().size()!=3)
            throw new AssertionError("three real CloudSimPlus jobs did not finish");
        System.out.printf(Locale.US,"STAGE49_CASE,%s,minEventSec=%.9f,expectedDataCenterFloorMs=%.9f%n",
            name,eventSec,1000.0*(eventSec+.01));
        for(String e:events)System.out.println(e);
        for(int i=0;i<3;i++) {
            Cloudlet c=jobs.get(i);
            System.out.printf(Locale.US,
                "STAGE49_OUTCOME,%s,%d,%d,%.12f,%.12f,%.12f,%.12f%n",
                name,i,c.getId(),c.getStartWaitTime()*1000.0,
                c.getTotalExecutionTime()*1000.0,ARRIVE_MS[i],SERVICE_MS[i]);
        }
        System.out.printf(Locale.US,"STAGE49_CASE_DONE,%s,submissions=%d,finishes=%d%n",
            name,events.stream().filter(z->z.startsWith("STAGE49_SUBMIT,"+name+",BEFORE,")).count(),
            events.stream().filter(z->z.startsWith("STAGE49_FINISH,"+name+",")).count());
    }
    public static void main(String[] args) {
        for(int i=0;i<NAMES.length;i++)runCase(NAMES[i],MIN_EVENTS_SEC[i]);
        System.out.println("JPDC_STAGE49_REAL_CLOUDSIM_857_THREE_CLOCK_CASES_COMPLETE");
    }
}
