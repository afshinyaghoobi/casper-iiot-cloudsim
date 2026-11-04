import java.util.Locale;
import org.casperiiot.e41.core.E17DualMemory;
import org.casperiiot.e41.core.NodeHealthDetector;
import org.casperiiot.e41.core.VirtualQueueEstimator;

/** Read-only deterministic reference harness on frozen scientific state classes. */
public final class CASPERStateReferenceHarness {
    public static void main(String[] args) {
        final double[] reference = new double[300];
        for(int i=0;i<reference.length;i++){
            reference[i]=0.50+((i*37)%101)/100.0;
        }
        final E17DualMemory memory = new E17DualMemory(reference);
        for(int t=0;t<=600;t++){
            System.out.printf(Locale.US,"STATE_E17,%d,%.17g,%b,%d,%.17g%n",
                t,memory.etaBeforeOutcome(),memory.alarmEver(),
                memory.transitionAge(),memory.referenceQ95());
            if(t==600)break;
            final double score=t<150 ? 0.65+((t*17)%23)/100.0
                : t<330 ? 2.50+((t*29)%31)/100.0
                : 0.80+((t*13)%19)/100.0;
            memory.observe(score);
        }

        final NodeHealthDetector[] health={
            new NodeHealthDetector(1.10),new NodeHealthDetector(1.40)};
        for(int t=0;t<180;t++){
            for(int node=0;node<health.length;node++){
                final double ratio=0.80+((t*11+node*7)%17)/10.0;
                final boolean alarm=health[node].observe(ratio*10.0,10.0);
                System.out.printf(Locale.US,"STATE_HEALTH,%d,%d,%b%n",node,t,alarm);
            }
        }

        final VirtualQueueEstimator queue=new VirtualQueueEstimator(3);
        for(int t=0;t<180;t++){
            final double now=2.5*t;
            if(t%20==0){
                final double[] telemetry=new double[3];
                for(int j=0;j<3;j++)telemetry[j]=now+5.0*(j+1);
                queue.resetFromTelemetry(telemetry);
            }
            final double[] backlog=new double[3];
            for(int j=0;j<3;j++)backlog[j]=queue.predictedBacklogMs(j,now);
            final int node=(t*7)%3;
            queue.onDispatch(node,now,2+(t%11)*0.25);
            System.out.printf(Locale.US,
                "STATE_QUEUE,%d,%.17g,%.17g,%.17g,%.17g,%.17g,%.17g,%.17g%n",
                t,now,backlog[0],backlog[1],backlog[2],
                queue.predictedNextFreeMs(0),queue.predictedNextFreeMs(1),
                queue.predictedNextFreeMs(2));
        }
        System.out.println("STATE_REFERENCE_COMPLETE");
    }
}
