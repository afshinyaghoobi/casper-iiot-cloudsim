#!/usr/bin/env python3
"""Generate E4.6 aggregation from the exact frozen E4.2 aggregation source.

Only stage labels and output/input file prefixes are changed. Statistical tests,
bootstrap settings, policies, scenarios, and all prelocked publication gates are
left byte-for-byte identical apart from those labels.
"""

from __future__ import annotations

import difflib
import hashlib
from pathlib import Path

SOURCE = Path("scripts/e42_aggregate.py")
OUTPUT = Path("scripts/e46_aggregate.py")
DIFF = Path("e46_aggregate_generated.diff")
MANIFEST = Path("e46_aggregate_generation_manifest.txt")
EXPECTED_GIT_BLOB = "29c2d6649ee13a872f294721553b9394552886bf"


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def main() -> None:
    raw = SOURCE.read_bytes()
    source_blob = git_blob_sha(raw)
    if source_blob != EXPECTED_GIT_BLOB:
        raise SystemExit(
            f"E46_AGGREGATE_GENERATOR FAIL frozen E4.2 aggregate blob {source_blob} != {EXPECTED_GIT_BLOB}"
        )

    original = raw.decode("utf-8")
    if "E4.2" not in original or "e42_" not in original or "E42_" not in original:
        raise SystemExit("E46_AGGREGATE_GENERATOR FAIL expected E4.2 stage labels missing")

    generated = original.replace("E4.2", "E4.6").replace("e42_", "e46_").replace("E42_", "E46_")

    # Fail closed if a frozen E4.2 stage/file label survived the label-only transform.
    for forbidden in ("E4.2", "e42_", "E42_"):
        if forbidden in generated:
            raise SystemExit(f"E46_AGGREGATE_GENERATOR FAIL surviving label {forbidden}")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(generated, encoding="utf-8")

    diff = "".join(
        difflib.unified_diff(
            original.splitlines(keepends=True),
            generated.splitlines(keepends=True),
            fromfile="e42_aggregate.py@frozen",
            tofile="e46_aggregate.py@generated",
        )
    )
    DIFF.write_text(diff, encoding="utf-8")

    generated_sha256 = hashlib.sha256(generated.encode()).hexdigest()
    MANIFEST.write_text(
        f"source_git_blob={source_blob}\n"
        f"generated_sha256={generated_sha256}\n"
        "transform=stage_and_file_labels_only\n"
        "statistical_logic_changed=false\n"
        "publication_gates_changed=false\n"
        "scientific_retuning=false\n",
        encoding="utf-8",
    )
    print(
        f"E46_AGGREGATE_GENERATOR PASS source_blob={source_blob} generated_sha256={generated_sha256}"
    )


if __name__ == "__main__":
    main()
