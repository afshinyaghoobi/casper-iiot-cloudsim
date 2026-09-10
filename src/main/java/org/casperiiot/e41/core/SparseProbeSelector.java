package org.casperiiot.e41.core;

/** Frozen E3.11 target rule: least-recently-observed healthy node that is point-deadline-plausible. */
public final class SparseProbeSelector {
    private SparseProbeSelector() {}

    public static int choose(double[] predictedLatencyMs, double deadlineMs, boolean[] alarmed, long[] lastObservedOrdinal) {
        int best=-1;
        long oldest=Long.MAX_VALUE;
        double bestLatency=Double.POSITIVE_INFINITY;
        for(int j=0;j<predictedLatencyMs.length;j++) {
            if(alarmed[j] || predictedLatencyMs[j] > deadlineMs) continue;
            long ageKey = lastObservedOrdinal[j] < 0 ? Long.MIN_VALUE : lastObservedOrdinal[j];
            if(best<0 || ageKey < oldest || (ageKey==oldest && predictedLatencyMs[j]<bestLatency)) {
                best=j; oldest=ageKey; bestLatency=predictedLatencyMs[j];
            }
        }
        return best;
    }
}
