#!/usr/bin/env python3
"""Generate E4.5 from the exact frozen E4.2 campaign source.

Only runtime arrival/submission semantics and stage labels are changed.  The
script fails closed if the frozen E4.2 blob is not exactly the pre-registered
blob or if any expected transformation site changes count.
"""

from __future__ import annotations

import difflib
import hashlib
from pathlib import Path

SOURCE = Path("src/main/java/org/casperiiot/e42/E42Campaign.java")
OUTPUT = Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
DIFF = Path("e45_generated.diff")
MANIFEST = Path("e45_generation_manifest.txt")
EXPECTED_GIT_BLOB = "34256ca7bff46f911cf20e8b94278fbd09175746"


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def replace_exact(text: str, old: str, new: str, count: int, label: str) -> str:
    actual = text.count(old)
    if actual != count:
        raise SystemExit(f"E45_GENERATOR FAIL {label}: expected {count} sites, found {actual}")
    return text.replace(old, new)


def main() -> None:
    raw = SOURCE.read_bytes()
    source_blob = git_blob_sha(raw)
    if source_blob != EXPECTED_GIT_BLOB:
        raise SystemExit(
            f"E45_GENERATOR FAIL frozen E4.2 source blob {source_blob} != {EXPECTED_GIT_BLOB}"
        )

    original = raw.decode("utf-8")
    src = original

    src = replace_exact(src, "package org.casperiiot.e42;", "package org.casperiiot.e45;", 1, "package")
    src = replace_exact(src, "public final class E42Campaign", "public final class E45Campaign", 1, "class")
    src = replace_exact(src, "E4.2 publication-scale CloudSim Plus campaign.",
                        "E4.5 online-dispatch publication campaign generated from frozen E4.2 science.",
                        1, "stage-doc")
    src = replace_exact(src, "new E42PublicationDatacenter(sim,hosts);",
                        "new E45PublicationDatacenter(sim,hosts);", 1, "datacenter")
    src = replace_exact(src, '"e42_seed_"', '"e45_seed_"', 1, "default-output")
    src = replace_exact(src, '"E42 seed=%d scientificSeed=%d cal=%d deploy=%d%n"',
                        '"E45 seed=%d scientificSeed=%d cal=%d deploy=%d%n"', 1, "stage-log")
    src = replace_exact(src, '"E42_SEED_COMPLETE seed="', '"E45_SEED_COMPLETE seed="', 1, "seed-complete")

    # Keep the broker alive across the idle interval before the first true arrival.
    src = replace_exact(
        src,
        "        final DatacenterBrokerSimple broker = new DatacenterBrokerSimple(sim);\n",
        "        final DatacenterBrokerSimple broker = new DatacenterBrokerSimple(sim);\n"
        "        broker.setShutdownWhenIdle(false);\n",
        1,
        "calibration-broker-lifetime",
    )
    src = replace_exact(
        src,
        "        final DatacenterBrokerSimple broker=new DatacenterBrokerSimple(sim);\n",
        "        final DatacenterBrokerSimple broker=new DatacenterBrokerSimple(sim);\n"
        "        broker.setShutdownWhenIdle(false);\n",
        1,
        "deployment-broker-lifetime",
    )

    # Cloudlets are still generated from the identical frozen Task list, but the
    # old pre-submission delay is removed because the arrival entity submits the
    # object only when its already-generated absolute timestamp is reached.
    src = replace_exact(
        src,
        "            c.setSubmissionDelay(t.arrivalMs()/1000.0);\n",
        "",
        2,
        "remove-pre-submission-delay",
    )

    # Enforce that every mapper invocation occurs on/after the frozen Task arrival.
    src = replace_exact(
        src,
        "            final Task t=spec.get(cl);\n",
        "            final Task t=spec.get(cl);\n"
        "            requireRuntimeArrival(sim,t);\n",
        2,
        "runtime-arrival-assertion",
    )

    # Replace the two bulk pre-start submissions (calibration + deployment) with
    # true CloudSim future-event submissions at the exact frozen timestamps.
    arrival_block = (
        "        new E45ArrivalSource(\n"
        "                sim,\n"
        "                tasks.stream().mapToDouble(t -> t.arrivalMs()/1000.0).toArray(),\n"
        "                i -> broker.submitCloudlet(cloudlets.get(i)));\n"
    )
    src = replace_exact(
        src,
        "        broker.submitCloudletList(cloudlets);\n",
        arrival_block,
        2,
        "event-scheduled-submission",
    )

    helper_anchor = "    private static Map<String,String> parseArgs(String[] args){\n"
    helper = (
        "    private static void requireRuntimeArrival(CloudSimPlus sim,Task t){\n"
        "        final double clockMs=sim.clock()*1000.0;\n"
        "        if(clockMs+1e-6<t.arrivalMs())\n"
        "            throw new IllegalStateException(\"E4.5 mapper ran before arrival task=\"+t.index()+\" clockMs=\"+clockMs+\" arrivalMs=\"+t.arrivalMs());\n"
        "    }\n\n"
    )
    src = replace_exact(src, helper_anchor, helper + helper_anchor, 1, "runtime-helper")

    seed_line = '        System.out.println("E45_SEED_COMPLETE seed="+seedIndex+" rows="+(scenarios.size()*Policy.values().length));\n'
    src = replace_exact(
        src,
        seed_line,
        '        System.out.println("E45_ONLINE_DISPATCH_RUNTIME PASS");\n' + seed_line,
        1,
        "runtime-pass-marker",
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(src, encoding="utf-8")

    diff = "".join(
        difflib.unified_diff(
            original.splitlines(keepends=True),
            src.splitlines(keepends=True),
            fromfile="E42Campaign.java@frozen",
            tofile="E45Campaign.java@generated",
        )
    )
    DIFF.write_text(diff, encoding="utf-8")

    generated_sha256 = hashlib.sha256(src.encode()).hexdigest()
    MANIFEST.write_text(
        f"source_git_blob={source_blob}\n"
        f"generated_sha256={generated_sha256}\n"
        "runtime_transform=true_event_scheduled_arrivals\n"
        "scientific_retuning=false\n",
        encoding="utf-8",
    )
    print(f"E45_GENERATOR PASS source_blob={source_blob} generated_sha256={generated_sha256}")


if __name__ == "__main__":
    main()
