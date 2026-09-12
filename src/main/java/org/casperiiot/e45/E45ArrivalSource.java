package org.casperiiot.e45;

import org.cloudsimplus.core.CloudSimEntity;
import org.cloudsimplus.core.CloudSimPlus;
import org.cloudsimplus.core.events.SimEvent;

import java.util.Arrays;
import java.util.function.IntConsumer;

/**
 * E4.5 runtime-only simulation entity that emits Cloudlet arrivals at the
 * already-generated frozen publication timestamps.
 *
 * This is the publication-scale form of the event-scheduled arrival mechanism
 * validated in E4.4. It changes no workload distribution, arrival timestamp,
 * service time, policy logic, threshold, seed, deadline, or publication gate.
 */
final class E45ArrivalSource extends CloudSimEntity {
    private static final int ARRIVAL_EVENT = 90_001;

    private final double[] arrivalSec;
    private final IntConsumer submitTask;

    E45ArrivalSource(
            final CloudSimPlus simulation,
            final double[] arrivalSec,
            final IntConsumer submitTask) {
        super(simulation);
        this.arrivalSec = Arrays.copyOf(arrivalSec, arrivalSec.length);
        this.submitTask = submitTask;
        validateArrivals(this.arrivalSec);
        setName("E45ArrivalSource");
    }

    @Override
    protected void startInternal() {
        if (arrivalSec.length > 0) {
            schedule(arrivalSec[0], ARRIVAL_EVENT, 0);
        }
    }

    @Override
    public void processEvent(final SimEvent evt) {
        if (evt.getTag() != ARRIVAL_EVENT || !(evt.getData() instanceof Integer task)) {
            throw new IllegalStateException("Unexpected E4.5 arrival event: " + evt.getTag());
        }

        submitTask.accept(task);

        final int next = task + 1;
        if (next < arrivalSec.length) {
            final double delay = arrivalSec[next] - arrivalSec[task];
            schedule(delay, ARRIVAL_EVENT, next);
        } else {
            shutdown();
        }
    }

    private static void validateArrivals(final double[] arrivals) {
        double previous = 0.0;
        for (int i = 0; i < arrivals.length; i++) {
            final double t = arrivals[i];
            if (!Double.isFinite(t) || t < 0.0 || (i > 0 && t < previous)) {
                throw new IllegalArgumentException("Invalid E4.5 arrival timestamp at task " + i + ": " + t);
            }
            previous = t;
        }
    }
}
