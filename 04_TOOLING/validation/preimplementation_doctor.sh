#!/usr/bin/env bash
# AI Video Factory — Pre-Implementation Master Doctor & Gate Validator
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "================================================================="
echo "   AI Video Factory — Pre-Implementation Master Doctor Suite   "
echo "================================================================="
echo "Workspace: $WORKSPACE_ROOT"
echo ""

echo "--- STEP 1: Verifying Workspace Layout & Cleanup Hygiene ---"
bash "$SCRIPT_DIR/verify_workspace_layout.sh"
echo ""

echo "--- STEP 2: Verifying Frozen Baseline Integrity & Sidecars ---"
bash "$SCRIPT_DIR/verify_frozen_baseline.sh"
echo ""

echo "--- STEP 3: Verifying Zero Frozen Mutation Drift ---"
bash "$SCRIPT_DIR/verify_no_frozen_mutation.sh"
echo ""

echo "--- STEP 4: Verifying Agent Rules, Skills & Hooks ---"
bash "$SCRIPT_DIR/verify_agent_customizations.sh"
echo ""

echo "--- STEP 5: Verifying Development Environment Doctor ---"
bash "$WORKSPACE_ROOT/05_IMPLEMENTATION/environment/doctor.sh"
echo ""

echo "================================================================="
echo "   PRE-IMPLEMENTATION STATUS: READY_FOR_IMPLEMENTATION (PASS)   "
echo "================================================================="
