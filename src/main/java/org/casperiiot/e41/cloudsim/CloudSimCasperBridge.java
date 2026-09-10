package org.casperiiot.e41.cloudsim;

import org.casperiiot.e41.core.CandidateGate;
import org.casperiiot.e41.core.Conformal;
import org.casperiiot.e41.core.NodeHealthDetector;
import org.casperiiot.e41.core.VirtualQueueEstimator;

/** Framework-facing adapter for the frozen CASPER core. */
public final class CloudSimCasperBridge {
    private final VirtualQueueEstimator virtualQueue;
    private final NodeHealthDetector[] health;

    public CloudSimCasperBridge(int nodeCount, double[] serviceRatioThresholdByNode) {
        virtualQueue = new VirtualQueueEstimator(nodeCount);
        health = new NodeHealthDetector[nodeCount];
        for (int j=0;j<nodeCount;j++) health[j] = new NodeHealthDetector(serviceRatioThresholdByNode[j]);
    }
    public void onTelemetry(double[] trueNextFreeMs) { virtualQueue.resetFromTelemetry(trueNextFreeMs); }
    public void onDispatch(int node, double nowMs, double predictedServiceMs) { virtualQueue.onDispatch(node, nowMs, predictedServiceMs); }
    public void onFinishedExecution(int node, double actualServiceMs, double nominalPredictedServiceMs) { health[node].observe(actualServiceMs, nominalPredictedServiceMs); }
    public boolean[] alarmMask() {
        boolean[] a = new boolean[health.length];
        for (int j=0;j<a.length;j++) a[j]=health[j].isAlarmed();
        return a;
    }
    public int[] eligibleTop3(double[] predictedLatencyMs) { return CandidateGate.topKHealthy(predictedLatencyMs, alarmMask(), 3); }
    public double predictedQueueMs(int node, double nowMs) { return virtualQueue.predictedBacklogMs(node, nowMs); }
    public double upperBound(double predictedLatencyMs, double sigmaMs, double q, double eta) { return Conformal.upper(predictedLatencyMs, sigmaMs, q, eta); }
}
