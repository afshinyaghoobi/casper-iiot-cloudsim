#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if ! command -v mvn >/dev/null 2>&1; then
  echo "BLOCKED_ENVIRONMENT: Maven is not installed; CloudSim Plus dependency cannot be resolved/runtime-tested here." >&2
  exit 3
fi
cd "$ROOT"
mvn -q -DskipTests compile exec:java -Dexec.mainClass=org.casperiiot.e41.cloudsim.CloudSimPlusSmoke
