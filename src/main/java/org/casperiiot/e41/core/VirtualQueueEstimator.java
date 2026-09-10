package org.casperiiot.e41.core;

import java.util.Arrays;

public final class VirtualQueueEstimator {
    private final double[] nextFreeMs;

    public VirtualQueueEstimator(int nodes) {
        this.nextFreeMs = new double[nodes];
    }

    public void resetFromTelemetry(double[] trueNextFreeSnapshotMs) {
        if (trueNextFreeSnapshotMs.length != nextFreeMs.length) throw new IllegalArgumentException("size");
        System.arraycopy(trueNextFreeSnapshotMs, 0, nextFreeMs, 0, nextFreeMs.length);
    }

    public double predictedBacklogMs(int node, double nowMs) {
        return Math.max(0.0, nextFreeMs[node] - nowMs);
    }

    /** Pre-outcome update using only the service duration predicted by the dispatcher. */
    public void onDispatch(int node, double nowMs, double predictedServiceMs) {
        nextFreeMs[node] = Math.max(nextFreeMs[node], nowMs) + predictedServiceMs;
    }

    public double predictedNextFreeMs(int node) { return nextFreeMs[node]; }
    public double[] snapshot() { return Arrays.copyOf(nextFreeMs, nextFreeMs.length); }
}
