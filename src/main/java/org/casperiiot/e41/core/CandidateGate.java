package org.casperiiot.e41.core;

import java.util.Arrays;

public final class CandidateGate {
    private CandidateGate() {}

    /** Return up to k lowest predicted-latency healthy nodes. */
    public static int[] topKHealthy(double[] predictedLatency, boolean[] alarmed, int k) {
        return java.util.stream.IntStream.range(0, predictedLatency.length)
            .filter(i -> !alarmed[i])
            .boxed()
            .sorted((a,b) -> Double.compare(predictedLatency[a], predictedLatency[b]))
            .limit(k)
            .mapToInt(Integer::intValue)
            .toArray();
    }

    public static int firstSafe(int[] family, double[] upperBoundByNode, double deadlineMs) {
        for (int node : family) if (upperBoundByNode[node] <= deadlineMs) return node;
        return -1;
    }
}
