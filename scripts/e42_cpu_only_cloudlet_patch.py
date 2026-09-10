#!/usr/bin/env python3
from pathlib import Path

p = Path('src/main/java/org/casperiiot/e42/E42Campaign.java')
s = p.read_text()

old_import = 'import org.cloudsimplus.utilizationmodels.UtilizationModelFull;\n'
new_import = old_import + 'import org.cloudsimplus.utilizationmodels.UtilizationModelDynamic;\n'
if 'UtilizationModelDynamic;' not in s:
    if old_import not in s:
        raise SystemExit('expected UtilizationModelFull import not found')
    s = s.replace(old_import, new_import, 1)

old_ctor = 'new CloudletSimple(Math.max(1,Math.round(t.work()*12)),1,new UtilizationModelFull())'
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

p.write_text(s)
print('E42_CPU_ONLY_CLOUDLET_PATCH PASS')
print('scientific parameters unchanged; CloudSim RAM/BW internal demand removed')
