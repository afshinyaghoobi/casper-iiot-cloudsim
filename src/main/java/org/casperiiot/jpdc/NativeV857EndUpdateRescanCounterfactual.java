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

/** Eligibility callback trace: preregistered reuse of six old inputs with new passive eligibility observations.
 * Original E42/E4.6 and Stage19/20 source are immutable.
 * All outputs are PASSIVE observations, never scheduler interference.
 */
public final class NativeV857EndUpdateRescanCounterfactual {
    private static final long MIPS = 1_000_000_000L;
    private static final double BASE_SECONDS=1.0;
    private static final double[] SERVICE_MS={8.099623,4.730689,9.120283};
    private static final double[] ARRIVE_MS={0.0,5.318920,8.0997406};
    private static final double[] MIN_EVENTS_SEC={0.000001,0.005};
    private static final double[] SHIFTS_MS={-4.0,0.0,10.0};
    private static final String[] SHIFT_LABELS={"EARLY4","ORIGINAL","LATE10"};

    private static String ids(final List<CloudletExecution> list) {
        return list.stream().map(e->Long.toString(e.getId())).collect(Collectors.joining(";"));
    }
    private static final class PassiveScheduler extends CloudletSchedulerSpaceShared {
        private final CloudSimPlus sim;
        private final String name;
        private final List<String> events;
        private final boolean treat;
        PassiveScheduler(CloudSimPlus sim,String name,List<String> events,boolean treat) {
            this.sim=sim;this.name=name;this.events=events;this.treat=treat;
        }
        private void submitLog(String moment,CloudletExecution job) {
            events.add(String.format(Locale.US,"ARRIVALTRACE_SUBMIT,%s,%s,%.12f,%d,%s,%s",
                name,moment,sim.clock()*1000.0,job.getId(),
                ids(getCloudletExecList()),ids(getCloudletWaitingList())));
        }
        @Override
        protected boolean canExecuteCloudletInternal(CloudletExecution job) {
            final String beforeExec=ids(getCloudletExecList());
            final String beforeWait=ids(getCloudletWaitingList());
            final boolean eligible=super.canExecuteCloudletInternal(job);
            events.add(String.format(Locale.US,
                "ARRIVALTRACE_ELIGIBILITY,%s,%.12f,%d,%s,%s,%s",
                name,sim.clock()*1000.0,job.getId(),
                Boolean.toString(eligible),beforeExec,beforeWait));
            return eligible;
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
            events.add(String.format(Locale.US,"ARRIVALTRACE_UPDATE,%s,BEFORE,%.12f,%s,%s",
                name,now*1000.0,ids(getCloudletExecList()),ids(getCloudletWaitingList())));
            double next=super.updateProcessing(now,share);
            events.add(String.format(Locale.US,"ARRIVALTRACE_UPDATE,%s,AFTER,%.12f,%s,%s",
                name,now*1000.0,ids(getCloudletExecList()),ids(getCloudletWaitingList())));
            // ONE predeclared intervention package, after super.updateProcessing returns.
            // Underlying library is unchanged; no list mutations except the library
            // method itself, called via its passive traced wrapper.
            if(treat && getCloudletExecList().isEmpty() && !getCloudletWaitingList().isEmpty()) {
                final String beforeExec=ids(getCloudletExecList());
                final String beforeWait=ids(getCloudletWaitingList());
                double extra=moveNextCloudletsFromWaitingToExecList(now);
                double chosen=(extra>0 && (next<=0 || extra<next))?extra:next;
                events.add(String.format(Locale.US,
                    "SIMPAT_INTERVENTION,%s,%.12f,%s,%s,%s,%s,%.12f,%.12f,%.12f",
                    name,now*1000.0,beforeExec,beforeWait,
                    ids(getCloudletExecList()),ids(getCloudletWaitingList()),
                    next,extra,chosen));
                return chosen;
            }
            return next;
        }
        @Override
        protected double moveNextCloudletsFromWaitingToExecList(final double currentTime) {
            events.add(String.format(Locale.US,
                "ARRIVALTRACE_PROMOTION,%s,BEFORE,%.12f,%s,%s",
                name,currentTime*1000.0,
                ids(getCloudletExecList()),ids(getCloudletWaitingList())));
            double result=super.moveNextCloudletsFromWaitingToExecList(currentTime);
            events.add(String.format(Locale.US,
                "ARRIVALTRACE_PROMOTION,%s,AFTER,%.12f,%s,%s",
                name,currentTime*1000.0,
                ids(getCloudletExecList()),ids(getCloudletWaitingList())));
            return result;
        }
    }
    private static Cloudlet newCloudlet(double serviceMs,double arrivalMs) {
        long length=Math.max(1L,Math.round(serviceMs/1000.0*MIPS));
        Cloudlet c=new CloudletSimple(length,1);
        c.setSubmissionDelay(BASE_SECONDS+arrivalMs/1000.0);
        c.setUtilizationModelCpu(new UtilizationModelFull());
        return c;
    }
    private static void runCase(String name,double eventSec,double shiftMs,boolean treat) {
        CloudSimPlus sim=new CloudSimPlus(eventSec);
        List<String> events=new ArrayList<>();
        PassiveScheduler scheduler=new PassiveScheduler(sim,name,events,treat);
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
            Cloudlet c=newCloudlet(SERVICE_MS[i],ARRIVE_MS[i]+(i==2?shiftMs:0.0));
            c.addOnFinishListener(info-> {
                Cloudlet done=info.getCloudlet();
                events.add(String.format(Locale.US,
                    "ARRIVALTRACE_FINISH,%s,%d,%d,%.12f,%.12f,%.12f,%.12f",
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
        System.out.printf(Locale.US,"ARRIVALTRACE_CASE,%s,minEventSec=%.9f,expectedDataCenterFloorMs=%.9f%n",
            name,eventSec,1000.0*(eventSec+.01));
        for(String e:events)System.out.println(e);
        for(int i=0;i<3;i++) {
            Cloudlet c=jobs.get(i);
            System.out.printf(Locale.US,
                "ARRIVALTRACE_OUTCOME,%s,%d,%d,%.12f,%.12f,%.12f,%.12f%n",
                name,i,c.getId(),c.getStartWaitTime()*1000.0,
                c.getTotalExecutionTime()*1000.0,ARRIVE_MS[i]+(i==2?shiftMs:0.0),SERVICE_MS[i]);
        }
        System.out.printf(Locale.US,"ARRIVALTRACE_CASE_DONE,%s,submissions=%d,finishes=%d%n",
            name,events.stream().filter(z->z.startsWith("ARRIVALTRACE_SUBMIT,"+name+",BEFORE,")).count(),
            events.stream().filter(z->z.startsWith("ARRIVALTRACE_FINISH,"+name+",")).count());
    }
    public static void main(String[] args) {
        if(args.length!=1 || !(args[0].equals("CONTROL")||args[0].equals("TREATMENT")))
            throw new IllegalArgumentException("Specify CONTROL or TREATMENT");
        boolean treat=args[0].equals("TREATMENT");
        for(int shift=0;shift<SHIFTS_MS.length;shift++)for(int k=0;k<MIN_EVENTS_SEC.length;k++) {
            String name=String.format(Locale.US,"%s_%s",SHIFT_LABELS[shift],(k==0?"1US":"5MS"));
            runCase(name,MIN_EVENTS_SEC[k],SHIFTS_MS[shift],treat);
        }
        System.out.println("JPDC_ARRIVALTRACE_NATIVE_SIX_CASES_COMPLETE");
    }
}
