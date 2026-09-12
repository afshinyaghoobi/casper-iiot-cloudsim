package org.casperiiot.e45;

import org.cloudsimplus.core.CloudSimPlus;
import org.cloudsimplus.datacenters.DatacenterSimple;
import org.cloudsimplus.hosts.Host;

import java.util.List;

/**
 * E4.5 carries forward the E4.2 runtime-only CloudSim Plus processing-delay
 * correction unchanged in behavior. No CASPER scientific parameter, workload,
 * policy, threshold, service model, network model, seed, or gate is changed.
 */
final class E45PublicationDatacenter extends DatacenterSimple {
    E45PublicationDatacenter(final CloudSimPlus simulation, final List<? extends Host> hostList) {
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
