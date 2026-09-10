# E4.1 Scope and Validity

E4.1 is an implementation-port/parity stage. It does **not** add or tune any CASPER-IIoT algorithmic parameter.

The frozen E3.12 architecture is represented in dependency-free Java core classes and in a CloudSim Plus binding/smoke source tree. The core is compiled with `javac --release 17` and exercised independently of any simulator library. The CloudSim-specific source pins `org.cloudsimplus:cloudsimplus:8.5.7` in Maven.

## What has been executed

The dependency-free Java core parity smoke has been executed in this environment. It checks topology, criticality/rank risk parameters, finite-sample conformal quantiles, one-sided scores, the dispatcher-side virtual queue update/reset semantics, node-health alarm logic, health gating, sparse-probe budget/selection, E1.7 detector/memory/eta constraints, and the frozen E3.12 scenario constants.

## What has not been executed

The actual CloudSim Plus runtime smoke has **not** been executed because this runtime has no Maven executable, no local CloudSim Plus 8.5.7 JAR, and outbound dependency retrieval is unavailable. A direct dependency download was attempted and failed. Therefore no result in E4.1 may be described as a CloudSim Plus simulation result.

The CloudSim runtime source is ready in `CloudSimPlusSmoke.java`; it creates 21 hosts and 21 VMs, submits mapped Cloudlets, starts `CloudSimPlus`, and asserts that all submitted Cloudlets finish. It must be run in an environment where Maven can resolve CloudSim Plus 8.5.7 before E4.2 is authorized.

## Publication gate

E4.2 (30-seed publication campaign) remains **NO-GO** until the actual CloudSim runtime smoke compiles and passes. This is an environment blocker, not an algorithmic failure.
