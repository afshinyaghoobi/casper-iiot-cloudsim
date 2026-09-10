#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/target/core"
rm -rf "$OUT" && mkdir -p "$OUT"
find "$ROOT/src/main/java/org/casperiiot/e41/core" -name '*.java' -print0 | xargs -0 javac --release 17 -d "$OUT"
java -cp "$OUT" org.casperiiot.e41.core.CoreParitySmoke
