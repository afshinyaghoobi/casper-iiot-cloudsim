package org.casperiiot.e41.cloudsim;

import org.cloudsimplus.brokers.DatacenterBrokerSimple;
import org.cloudsimplus.cloudlets.Cloudlet;
import org.cloudsimplus.cloudlets.CloudletSimple;
import org.cloudsimplus.core.CloudSimPlus;
import org.cloudsimplus.datacenters.DatacenterSimple;
import org.cloudsimplus.hosts.Host;
import org.cloudsimplus.hosts.HostSimple;
import org.cloudsimplus.resources.Pe;
import org.cloudsimplus.resources.PeSimple;
import org.cloudsimplus.utilizationmodels.UtilizationModelFull;
import org.cloudsimplus.vms.Vm;
import org.cloudsimplus.vms.VmSimple;
import org.casperiiot.e41.core.FrozenConfig;

import java.util.ArrayList;
import java.util.IdentityHashMap;
import java.util.List;
import java.util.Map;

/**
 * Runtime binding smoke for CloudSim Plus 8.5.7.
 * This deliberately tests framework construction/mapping/completion only.
 * Scientific parity is asserted by the dependency-free core smoke plus the frozen config manifest.
 */
public final class CloudSimPlusSmoke {
    public static void main(String[] args) {
        final var simulation = new CloudSimPlus();
        final List<Host> hosts = createHosts();
        new DatacenterSimple(simulation, hosts);
        final var broker = new DatacenterBrokerSimple(simulation);

        final List<Vm> vms = createVms();
        final List<Cloudlet> cloudlets = new ArrayList<>();
        final Map<Cloudlet,Vm> plan = new IdentityHashMap<>();
        final var utilization = new UtilizationModelFull();

        for (int i=0; i<42; i++) {
            Cloudlet c = new CloudletSimple(8_000 + 100L*i, 1, utilization);
            c.setSizes(1024);
            cloudlets.add(c);
            plan.put(c, vms.get(i % vms.size()));
        }

        broker.submitVmList(vms);
        broker.setVmMapper(c -> plan.getOrDefault(c, Vm.NULL));
        broker.submitCloudletList(cloudlets);
        simulation.start();

        final int finished = broker.getCloudletFinishedList().size();
        if (hosts.size() != FrozenConfig.TOTAL_NODES) throw new IllegalStateException("host topology mismatch");
        if (vms.size() != FrozenConfig.TOTAL_NODES) throw new IllegalStateException("vm topology mismatch");
        if (finished != cloudlets.size()) throw new IllegalStateException("not all smoke cloudlets completed: " + finished);

        System.out.printf("CLOUDSIM_RUNTIME_SMOKE PASS hosts=%d vms=%d cloudlets=%d finished=%d%n",
                hosts.size(), vms.size(), cloudlets.size(), finished);
    }

    private static List<Host> createHosts() {
        final List<Host> hosts = new ArrayList<>();
        for (int i=0; i<FrozenConfig.TOTAL_NODES; i++) {
            final long mips = i < 12 ? 4_000 : (i < 18 ? 12_000 : 40_000);
            final List<Pe> pes = List.of(new PeSimple(mips));
            hosts.add(new HostSimple(8_192, 10_000, 1_000_000, pes));
        }
        return hosts;
    }

    private static List<Vm> createVms() {
        final List<Vm> vms = new ArrayList<>();
        for (int i=0; i<FrozenConfig.TOTAL_NODES; i++) {
            final long mips = i < 12 ? 3_000 : (i < 18 ? 10_000 : 30_000);
            vms.add(new VmSimple(mips,1).setRam(2048).setBw(1000).setSize(10_000));
        }
        return vms;
    }
}
