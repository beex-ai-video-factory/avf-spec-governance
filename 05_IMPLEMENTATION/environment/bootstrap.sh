#!/usr/bin/env bash
# AI Video Factory — Environment Bootstrap Script
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== AI Video Factory: Bootstrapping Implementation Workspace ==="
echo "Workspace Root: $WORKSPACE_ROOT"

# 1. Ensure .env exists
if [[ ! -f "$SCRIPT_DIR/.env" ]]; then
  echo "--> Copying .env.example to .env..."
  cp "$SCRIPT_DIR/.env.example" "$SCRIPT_DIR/.env"
else
  echo "--> .env file already exists. Preserving existing configuration."
fi

# 2. Ensure temp directory exists
mkdir -p "$WORKSPACE_ROOT/99_TEMP" "$SCRIPT_DIR/tmp_data"

# 3. Run Doctor to verify readiness
echo "--> Running environment diagnostics..."
bash "$SCRIPT_DIR/doctor.sh"

echo "=== Environment Bootstrap Completed Successfully ==="
