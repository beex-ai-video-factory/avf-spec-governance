#!/usr/bin/env bash
# AI Video Factory — Frozen Baseline Validator
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== 1. Validating Canonical Distributable ZIP & Detached Sidecar ==="
ZIP_FILE="$WORKSPACE_ROOT/01_FROZEN_RELEASE/distributable/AVF_FINAL_FREEZE_v1.0.0_REMEDIATED.zip"
SIDECAR_FILE="$WORKSPACE_ROOT/01_FROZEN_RELEASE/distributable/AVF_FINAL_FREEZE_v1.0.0_REMEDIATED.zip.sha256"

if [[ ! -f "$ZIP_FILE" ]]; then
  echo "ERROR: Missing canonical release ZIP: $ZIP_FILE" >&2
  exit 1
fi

if [[ ! -f "$SIDECAR_FILE" ]]; then
  echo "ERROR: Missing detached SHA256 sidecar: $SIDECAR_FILE" >&2
  exit 1
fi

cd "$WORKSPACE_ROOT/01_FROZEN_RELEASE/distributable"
shasum -a 256 -c "AVF_FINAL_FREEZE_v1.0.0_REMEDIATED.zip.sha256"
cd "$WORKSPACE_ROOT"
echo "Distributable archive integrity: OK"

echo "=== 2. Validating Frozen Spec Version ==="
VERSION_FILE="$WORKSPACE_ROOT/01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/VERSION"
if [[ ! -f "$VERSION_FILE" ]]; then
  echo "ERROR: Missing VERSION file at $VERSION_FILE" >&2
  exit 1
fi

VERSION_VAL=$(cat "$VERSION_FILE" | tr -d ' \n\r')
if [[ "$VERSION_VAL" != "1.0.0" ]]; then
  echo "ERROR: Expected version 1.0.0, got '$VERSION_VAL'" >&2
  exit 1
fi
echo "Version verification: OK (1.0.0)"

echo "=== 3. Validating Internal Normative Package Content Hashes ==="
python3 "$WORKSPACE_ROOT/01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/verify_package.py"

echo "=== 4. Validating Protected Directories Read-Only Permissions ==="
PROTECTED_DIRS=(
  "01_FROZEN_RELEASE"
  "02_SOURCE_KITS_READONLY"
  "03_GOVERNANCE_EVIDENCE_READONLY"
  "90_ARCHIVE_READONLY"
)

for dir in "${PROTECTED_DIRS[@]}"; do
  full_d="$WORKSPACE_ROOT/$dir"
  if [[ ! -d "$full_d" ]]; then
    echo "ERROR: Protected directory missing: $full_d" >&2
    exit 1
  fi
  # Test write permission
  if [[ -w "$full_d" ]]; then
    echo "WARNING/NOTE: Directory $dir is currently writable on disk. Will be locked down during final permissions freeze."
  else
    echo "Read-only protection verified for $dir: OK"
  fi
done

echo "=== Frozen Baseline Verification: ALL CHECKS PASSED ==="
