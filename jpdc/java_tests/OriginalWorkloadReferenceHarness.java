import java.lang.reflect.*;
import java.util.*;

/** Invoke original frozen E42 Java generators via read-only reflection. */
public final class OriginalWorkloadReferenceHarness {
    private static Object accessor(Object record, String name) throws Exception {
        Method m=record.getClass().getDeclaredMethod(name);
        m.setAccessible(true);
        return m.invoke(record);
    }
    @SuppressWarnings({"unchecked","rawtypes"})
    public static void main(String[] args) throws Exception {
        long seed=4202202640L;
        int n=30000;
        Class<?> owner=Class.forName("org.casperiiot.e42.E42Campaign");
        Method makeNodes=owner.getDeclaredMethod("makeNodes",long.class);
        makeNodes.setAccessible(true);
        Object[] nodes=(Object[])makeNodes.invoke(null,seed);
        if(nodes.length!=21)throw new IllegalStateException("node count");
        for(int j=0;j<nodes.length;j++){
            Object node=nodes[j];
            System.out.printf(Locale.US,"JPDC_NODE,%d,%.17g,%.17g,%.17g,%.17g,%d%n",
                j,(double)accessor(node,"cap"),(double)accessor(node,"bwMbps"),
                (double)accessor(node,"rttMs"),(double)accessor(node,"sigmaMult"),
                (long)accessor(node,"vmMips"));
        }
        Class<?> scenario=Class.forName("org.casperiiot.e42.E42Campaign$Scenario");
        Method makeTasks=owner.getDeclaredMethod("makeTasks",long.class,int.class,scenario);
        makeTasks.setAccessible(true);
        String[] scenarios={"S0_STATIONARY","S1_LAMBDA_X2","S2_HIDDEN_COMPUTE_40LOSS",
                            "S3_HIDDEN_NETWORK_50LOSS","S4_COMPOUND"};
        for(String scenarioName:scenarios){
            Object arg=Enum.valueOf((Class<? extends Enum>)scenario,scenarioName);
            List<?> tasks=(List<?>)makeTasks.invoke(null,seed ^ 0xD3F10A77L,n,arg);
            if(tasks.size()!=n)throw new IllegalStateException("task count");
            for(Object t:tasks){
                System.out.printf(Locale.US,
                    "JPDC_TASK,%s,%d,%s,%.17g,%.17g,%.17g,%.17g,%.17g%n",
                    scenarioName,(int)accessor(t,"index"),accessor(t,"crit"),
                    (double)accessor(t,"deadlineMs"),(double)accessor(t,"work"),
                    (double)accessor(t,"inputMb"),(double)accessor(t,"outputMb"),
                    (double)accessor(t,"arrivalMs"));
            }
        }
        System.out.println("JPDC_WORKLOAD_REFERENCE_COMPLETE");
    }
}
