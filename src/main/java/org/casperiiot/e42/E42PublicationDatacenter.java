package org.casperiiot.e42;

import org.cloudsimplus.core.CloudSimPlus;
import org.cloudsimplus.datacenters.DatacenterSimple;
import org.cloudsimplus.hosts.Host;

import java.util.List;

/**
 * E4.2 runtime-only correction for CloudSim Plus 8.5.7.
 *
 * DatacenterSimple.updateHostsProcessing() hard-codes an extra 0.01 seconds
 * on top of Simulation.getMinTimeBetweenEvents(). That floor delays short
 * Cloudlet completion events by about 10 ms and therefore contaminates the
 * selected-service parity audit and end-to-end latency measurements.
 *
 * This subclass preserves DatacenterSimple's host-processing logic and uses
 * exactly the simulation's configured minimum event spacing, without the
 * additional 10 ms padding. It changes no CASPER scientific parameter,
 * workload, policy, threshold, service model, or network model.
 */
final class E42PublicationDatacenter extends DatacenterSimple {
    E42PublicationDatacenter(final CloudSimPlus simulation, final List<? extends Host> hostList) {
        super(simulation, hostList);
    }

    @Override
    protected double updateHostsProcessing() {
        double nextSimulationDelay = Double.MAX_VALUE;
        for (final Host host : getHostList()) {
            final double delay = host.updateProcessing(getSimulation().clock());
            nextSimulationDelay = Math.min(delay, nextSimulationDelay);
        }

        final double minTimeBetweenEvents = getSimulation().getMinTimeBetweenEvents();
        return nextSimulationDelay == 0
                ? 0
                : Math.max(nextSimulationDelay, minTimeBetweenEvents);
    }
}
