#!/usr/bin/env bash
# AI Video Factory — Workspace Layout Validator
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== Checking Required Top-Level Directories ==="
REQUIRED_DIRS=(
  "00_PROJECT_ADMIN"
  "01_FROZEN_RELEASE"
  "02_SOURCE_KITS_READONLY"
  "03_GOVERNANCE_EVIDENCE_READONLY"
  "04_TOOLING"
  "05_IMPLEMENTATION"
  "90_ARCHIVE_READONLY"
  "99_TEMP"
  ".agents"
)

for d in "${REQUIRED_DIRS[@]}"; do
  if [[ ! -d "$WORKSPACE_ROOT/$d" ]]; then
    echo "ERROR: Missing required directory: $d" >&2
    exit 1
  fi
  echo "Directory $d: OK"
done

echo "=== Checking Root Control Files ==="
REQUIRED_ROOT_FILES=(
  "PROJECT.md"
  "BASELINE.lock.json"
  ".gitignore"
  ".editorconfig"
)

for f in "${REQUIRED_ROOT_FILES[@]}"; do
  if [[ ! -f "$WORKSPACE_ROOT/$f" ]]; then
    echo "ERROR: Missing required root control file: $f" >&2
    exit 1
  fi
  echo "Root file $f: OK"
done

echo "=== Checking Canonical Release Uniqueness ==="
CANONICAL_ZIPS=$(find "$WORKSPACE_ROOT/01_FROZEN_RELEASE/distributable" -name "*.zip" | wc -l | tr -d ' ')
if [[ "$CANONICAL_ZIPS" -ne 1 ]]; then
  echo "ERROR: Expected exactly 1 canonical release ZIP, found $CANONICAL_ZIPS" >&2
  exit 1
fi
echo "Canonical release copies: Exactly 1 (OK)"

echo "=== Checking Absence of Loose Historical Prompts at Root ==="
LOOSE_PROMPTS=(
  "AUTONOMOUS_COUNCIL_MASTER.md"
  "AUTONOMOUS_FREEZE_REMEDIATION_MASTER.md"
  "FINAL_FREEZE_FORENSIC_AUDIT.md"
  "FINAL_PACKAGE_HASH_CANONICALIZATION.md"
  "FINAL_REMEDIATED_CROSS_FAMILY_AUDIT.md"
  "FINAL_TARGETED_GOVERNANCE_PATCH.md"
  "PRE_IMPLEMENTATION_WORKSPACE_FREEZE_AND_NORMALIZE.md"
)

for p in "${LOOSE_PROMPTS[@]}"; do
  if [[ -f "$WORKSPACE_ROOT/$p" ]]; then
    echo "ERROR: Loose prompt '$p' found at root. Must be moved to 04_TOOLING/prompts/historical/" >&2
    exit 1
  fi
done
echo "Root cleanliness: OK (No loose historical prompts)"

echo "=== Checking 15 Repositories Registered in 05_IMPLEMENTATION/repos ==="
for i in {1..15}; do
  prefix=$(printf "R%02d_" "$i")
  matching=$(find "$WORKSPACE_ROOT/05_IMPLEMENTATION/repos" -maxdepth 1 -type d -name "${prefix}*" | wc -l | tr -d ' ')
  if [[ "$matching" -lt 1 ]]; then
    echo "ERROR: Missing repository placeholder for $prefix" >&2
    exit 1
  fi
done
echo "All 15 implementation repository placeholders registered: OK"

echo "=== Workspace Layout Verification: ALL CHECKS PASSED ==="
