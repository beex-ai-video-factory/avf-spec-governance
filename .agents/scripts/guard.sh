#!/usr/bin/env bash
# Pre-tool guard script for Antigravity agents
set -euo pipefail

TARGET_PATH="${1:-}"

if [[ -z "$TARGET_PATH" ]]; then
  exit 0
fi

# Protected path prefixes
PROTECTED_PREFIXES=(
  "01_FROZEN_RELEASE"
  "02_SOURCE_KITS_READONLY"
  "03_GOVERNANCE_EVIDENCE_READONLY"
  "90_ARCHIVE_READONLY"
  "./01_FROZEN_RELEASE"
  "./02_SOURCE_KITS_READONLY"
  "./03_GOVERNANCE_EVIDENCE_READONLY"
  "./90_ARCHIVE_READONLY"
)

for prefix in "${PROTECTED_PREFIXES[@]}"; do
  if [[ "$TARGET_PATH" == "$prefix"* ]]; then
    echo "[SECURITY ERROR] Mutation attempt blocked: Path '$TARGET_PATH' is permanently READ-ONLY." >&2
    echo "To propose changes to the frozen baseline, create a Change Request in 05_IMPLEMENTATION/change-requests/." >&2
    exit 1
  fi
done

exit 0
