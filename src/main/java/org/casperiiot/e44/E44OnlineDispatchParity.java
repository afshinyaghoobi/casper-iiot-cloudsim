package org.casperiiot.e44;

import org.cloudsimplus.brokers.DatacenterBrokerSimple;
import org.cloudsimplus.cloudlets.Cloudlet;
import org.cloudsimplus.cloudlets.CloudletSimple;
import org.cloudsimplus.core.CloudSimPlus;
import org.cloudsimplus.hosts.Host;
import org.cloudsimplus.hosts.HostSimple;
import org.cloudsimplus.resources.Pe;
import org.cloudsimplus.resources.PeSimple;
import org.cloudsimplus.schedulers.cloudlet.CloudletSchedulerSpaceShared;
import org.cloudsimplus.utilizationmodels.UtilizationModelFull;
import org.cloudsimplus.vms.Vm;
import org.cloudsimplus.vms.VmSimple;
import org.casperiiot.e41.core.E17DualMemory;
import org.casperiiot.e41.core.FrozenConfig;
import org.casperiiot.e41.core.NodeHealthDetector;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Locale;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * E4.4 deterministic runtime-ordering harness.
 *
 * This is not a scientific campaign. It validates only that Cloudlets submitted
 * at runtime are mapped after earlier completion callbacks have had a chance to
 * update the frozen health/E1.7 state used by later dispatches.
 */
public final class E44OnlineDispatchParity {
    private static final int TASKS = 80;
    private static final double FIRST_ARRIVAL_SEC = 0.20;
    private static final double INTERARRIVAL_SEC = 0.05;
    private static final double NOMINAL_SERVICE_MS = 10.0;
    private static final double ACTUAL_SERVICE_MS = 20.0;
    private static final long MIPS = 10_000L;
    private static final double TIME_EPS = 1e-9;

    private E44OnlineDispatchParity() {}

    public static void main(String[] args) {
        final CloudSimPlus sim = new CloudSimPlus(0.000001);

        /*
         * Runtime-fixture correction only: the parity harness submits two
         * single-PE VMs. A single physical PE makes the fallback VM permanently
         * unschedulable under the default space-shared VM scheduler. Two
         * identical PEs make both VMs allocatable without changing VM MIPS,
         * service times, workload, policy, thresholds, seeds, or frozen E4.2
         * scientific configuration.
         */
        final List<Pe> pes = List.of(new PeSimple(50_000), new PeSimple(50_000));
        final List<Host> hosts = List.of(new HostSimple(16_384, 100_000, 10_000_000, pes));
        new E44ParityDatacenter(sim, hosts);

        final DatacenterBrokerSimple broker = new DatacenterBrokerSimple(sim);
        broker.setShutdownWhenIdle(false);

        final Vm primary = new VmSimple(MIPS, 1)
                .setRam(4096).setBw(10_000).setSize(100_000)
                .setCloudletScheduler(new CloudletSchedulerSpaceShared());
        final Vm fallback = new VmSimple(MIPS, 1)
                .setRam(4096).setBw(10_000).setSize(100_000)
                .setCloudletScheduler(new CloudletSchedulerSpaceShared());
        final List<Vm> vms = List.of(primary, fallback);

        /* Synthetic fixture threshold only; FrozenConfig itself is untouched. */
        final NodeHealthDetector health = new NodeHealthDetector(
                1.05, FrozenConfig.HEALTH_WINDOW, FrozenConfig.HEALTH_EXCEEDANCES);
        final double[] reference = new double[FrozenConfig.E17_SLOW_WINDOW];
        Arrays.fill(reference, 1.0);
        final E17DualMemory e17 = new E17DualMemory(reference);

        final AtomicInteger submitted = new AtomicInteger();
        final AtomicInteger finished = new AtomicInteger();
        final AtomicInteger firstHealthVisibleDispatch = new AtomicInteger(-1);
        final AtomicInteger firstE17AlarmVisibleDispatch = new AtomicInteger(-1);
        final AtomicInteger firstEtaAboveOneVisibleDispatch = new AtomicInteger(-1);
        final List<Integer> mapperOrder = new ArrayList<>();
        final List<Integer> finishOrder = new ArrayList<>();
        final List<Double> etaAtDispatch = new ArrayList<>();
        final double[] mapperTime = new double[TASKS];
        Arrays.fill(mapperTime, Double.NaN);

        broker.setVmMapper(cloudlet -> {
            final int idx = (int) cloudlet.getId();
            final boolean alarm = health.isAlarmed();
            final boolean e17Alarm = e17.alarmEver();
            final double eta = e17.etaBeforeOutcome();
            mapperOrder.add(idx);
            mapperTime[idx] = sim.clock();
            etaAtDispatch.add(eta);
            if (alarm && firstHealthVisibleDispatch.get() < 0) firstHealthVisibleDispatch.set(idx);
            if (e17Alarm && firstE17AlarmVisibleDispatch.get() < 0) firstE17AlarmVisibleDispatch.set(idx);
            if (eta > 1.0 + 1e-12 && firstEtaAboveOneVisibleDispatch.get() < 0) firstEtaAboveOneVisibleDispatch.set(idx);
            return alarm ? fallback : primary;
        });

        broker.submitVmList(vms);

        /*
         * True simulation-native arrivals. The E44ArrivalSource places each
         * arrival directly on CloudSim's future-event queue. This removes the
         * need to use Datacenter.schedulingInterval as a clock generator, so
         * Cloudlet-processing updates retain their exact runtime completion
         * events while each later dispatch can observe earlier feedback.
         */
        new E44ArrivalSource(sim, TASKS, FIRST_ARRIVAL_SEC, INTERARRIVAL_SEC, i -> {
            final long length = Math.max(1L, Math.round(MIPS * ACTUAL_SERVICE_MS / 1000.0));
            final Cloudlet c = new CloudletSimple(length, 1)
                    .setUtilizationModelCpu(new UtilizationModelFull());
            c.setId(i);
            c.addOnFinishListener(evt -> {
                final Cloudlet done = evt.getCloudlet();
                final int task = (int) done.getId();
                finishOrder.add(task);
                final double serviceMs = done.getTotalExecutionTime() * 1000.0;
                health.observe(serviceMs, NOMINAL_SERVICE_MS);
                e17.observe(2.0);
                finished.incrementAndGet();
            });
            broker.submitCloudlet(c);
            submitted.incrementAndGet();
        });

        /*
         * Do not impose a wall on simulation time here. The parity gate is that
         * every deterministically scheduled runtime event drains to completion.
         * A fixed terminateAt horizon can cut off valid deferred processing
         * events and create a false all_cloudlets_finish failure.
         */
        sim.start();

        final boolean allFinished = finished.get() == TASKS
                && broker.getCloudletFinishedList().size() == TASKS;

        boolean mapperAtOrAfterArrival = submitted.get() == TASKS && mapperOrder.size() == TASKS;
        for (int i = 0; i < TASKS && mapperAtOrAfterArrival; i++) {
            final double arrival = FIRST_ARRIVAL_SEC + i * INTERARRIVAL_SEC;
            mapperAtOrAfterArrival = !Double.isNaN(mapperTime[i])
                    && mapperTime[i] + TIME_EPS >= arrival;
        }

        final boolean healthVisible = firstHealthVisibleDispatch.get() >= 0;
        final boolean e17Visible = firstE17AlarmVisibleDispatch.get() >= 0;
        final boolean etaVisible = firstEtaAboveOneVisibleDispatch.get() >= 0;
        final boolean feedbackPrecedesLaterDispatch = healthVisible
                && finishOrder.stream().anyMatch(x -> x < firstHealthVisibleDispatch.get());
        final boolean fallbackUsedAfterAlarm = healthVisible
                && broker.getCloudletFinishedList().stream()
                .anyMatch(c -> c.getVm() == fallback && c.getId() >= firstHealthVisibleDispatch.get());

        System.out.printf(Locale.US,
                "E44_PARITY healthVisibleAt=%d e17VisibleAt=%d etaVisibleAt=%d submitted=%d mapped=%d finished=%d etaMax=%.6f%n",
                firstHealthVisibleDispatch.get(), firstE17AlarmVisibleDispatch.get(),
                firstEtaAboveOneVisibleDispatch.get(), submitted.get(), mapperOrder.size(), finished.get(),
                etaAtDispatch.stream().mapToDouble(Double::doubleValue).max().orElse(1.0));

        require(mapperAtOrAfterArrival, "mapper_runs_at_or_after_each_cloudlet_arrival");
        require(allFinished, "all_cloudlets_finish");
        require(feedbackPrecedesLaterDispatch, "completion_callback_can_precede_later_dispatch");
        require(healthVisible, "health_alarm_becomes_visible_to_later_dispatch");
        require(e17Visible, "e17_alarm_becomes_visible_to_later_dispatch");
        require(etaVisible, "eta_above_one_becomes_visible_to_later_dispatch");
        require(fallbackUsedAfterAlarm, "health_state_changes_later_vm_mapping");

        System.out.println("E44_ONLINE_DISPATCH_PARITY PASS");
    }

    private static void require(boolean condition, String name) {
        if (!condition) throw new IllegalStateException("E44 gate failed: " + name);
        System.out.println("E44_GATE PASS " + name);
    }
}
