package org.casperiiot.e44;

import org.cloudsimplus.core.CloudSimEntity;
import org.cloudsimplus.core.CloudSimPlus;
import org.cloudsimplus.core.events.SimEvent;

import java.util.function.IntConsumer;

/**
 * Parity-only simulation entity that emits deterministic Cloudlet-arrival events.
 *
 * The entity exists solely to put each arrival on CloudSim's future-event queue.
 * It does not change workload parameters, service times, policy logic, detector
 * thresholds, seeds, or any frozen E4.2 scientific configuration.
 */
final class E44ArrivalSource extends CloudSimEntity {
    private static final int ARRIVAL_EVENT = 90_001;

    private final int tasks;
    private final double firstArrivalSec;
    private final double interarrivalSec;
    private final IntConsumer submitTask;

    E44ArrivalSource(
            final CloudSimPlus simulation,
            final int tasks,
            final double firstArrivalSec,
            final double interarrivalSec,
            final IntConsumer submitTask) {
        super(simulation);
        this.tasks = tasks;
        this.firstArrivalSec = firstArrivalSec;
        this.interarrivalSec = interarrivalSec;
        this.submitTask = submitTask;
        setName("E44ArrivalSource");
    }

    @Override
    protected void startInternal() {
        if (tasks > 0) {
            schedule(firstArrivalSec, ARRIVAL_EVENT, 0);
        }
    }

    @Override
    public void processEvent(final SimEvent evt) {
        if (evt.getTag() != ARRIVAL_EVENT || !(evt.getData() instanceof Integer task)) {
            throw new IllegalStateException("Unexpected E4.4 arrival event: " + evt.getTag());
        }

        submitTask.accept(task);

        final int next = task + 1;
        if (next < tasks) {
            schedule(interarrivalSec, ARRIVAL_EVENT, next);
        } else {
            shutdown();
        }
    }
}
