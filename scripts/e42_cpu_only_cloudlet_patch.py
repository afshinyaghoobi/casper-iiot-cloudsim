#!/usr/bin/env python3
from pathlib import Path

p = Path('src/main/java/org/casperiiot/e42/E42Campaign.java')
s = p.read_text()

# Preserve the already-applied CPU-only Cloudlet semantics. Keep this patch
# idempotent so it can safely be re-run on the current E4.2 source.
old_import = 'import org.cloudsimplus.utilizationmodels.UtilizationModelFull;\n'
new_import = old_import + 'import org.cloudsimplus.utilizationmodels.UtilizationModelDynamic;\n'
if 'UtilizationModelDynamic;' not in s:
    if old_import not in s:
        raise SystemExit('expected UtilizationModelFull import not found')
    s = s.replace(old_import, new_import, 1)

old_ctor = 'new CloudletSimple(Math.max(1,Math.round(t.work()*12)),1,new UtilizationModelFull())'
if old_ctor in s:
    count = s.count(old_ctor)
    if count != 2:
        raise SystemExit(f'expected exactly 2 campaign cloudlet constructors, found {count}')
    s = s.replace(old_ctor, 'cpuOnlyCloudlet(Math.max(1,Math.round(t.work()*12)))')

anchor = '    private static List<Vm> createInfrastructure(CloudSimPlus sim,NodeParams[] nodes){\n'
helper = '''    /**\n     * E4.2 CloudSim compute-only cloudlet. CPU demand is simulated by CloudSim;\n     * end-to-end network latency is modeled explicitly by the frozen algebraic\n     * endpoint model, and RAM contention is outside the frozen E3.12 model.\n     * Therefore RAM/BW utilization inside CloudSim is intentionally zero to\n     * prevent unintended CloudSim VMem/BW oversubscription delays.\n     */\n    private static Cloudlet cpuOnlyCloudlet(long length){\n        final Cloudlet c = new CloudletSimple(length,1);\n        c.setUtilizationModelCpu(new UtilizationModelFull());\n        c.setUtilizationModelRam(new UtilizationModelDynamic(0.0));\n        c.setUtilizationModelBw(new UtilizationModelDynamic(0.0));\n        return c;\n    }\n\n'''
if 'private static Cloudlet cpuOnlyCloudlet' not in s:
    if anchor not in s:
        raise SystemExit('createInfrastructure anchor not found')
    s = s.replace(anchor, helper + anchor, 1)

# Runtime-parity audit correction: CloudSim Plus 8.5.x exposes the Cloudlet's
# actual CPU execution duration as getTotalExecutionTime().  finishTime-startTime
# is a lifecycle wall-clock interval and can include scheduler/event timing that
# is not CPU service.  E4.2 service-health, latency, and parity accounting must
# therefore use the framework's CPU execution-time metric.
old_service = 'final double serviceMs=(cl.getFinishTime()-cl.getStartTime())*1000.0;'
new_service = 'final double serviceMs=cl.getTotalExecutionTime()*1000.0;'
count = s.count(old_service)
if count not in (0, 2):
    raise SystemExit(f'expected 0 or 2 lifecycle service-time expressions, found {count}')
if count == 2:
    s = s.replace(old_service, new_service)
if s.count(new_service) != 2:
    raise SystemExit(f'expected exactly 2 CloudSim CPU execution-time expressions, found {s.count(new_service)}')

p.write_text(s)
print('E42_RUNTIME_SERVICE_PARITY_AUDIT_PATCH PASS')
print('scientific parameters unchanged; service timing now uses CloudSim total CPU execution time')
