package org.casperiiot.e44;

import org.cloudsimplus.core.CloudSimPlus;
import org.cloudsimplus.datacenters.DatacenterSimple;
import org.cloudsimplus.hosts.Host;

import java.util.List;

/** Parity-only copy of the E4.2 CloudSim 8.5.7 processing-delay correction. */
final class E44ParityDatacenter extends DatacenterSimple {
    E44ParityDatacenter(final CloudSimPlus simulation, final List<? extends Host> hostList) {
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
        return nextSimulationDelay == 0 ? 0 : Math.max(nextSimulationDelay, minTimeBetweenEvents);
    }
}
