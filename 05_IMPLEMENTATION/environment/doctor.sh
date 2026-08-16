#!/usr/bin/env bash
# AI Video Factory — Environment Doctor & System Health Checker
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "========================================================"
echo "    AI Video Factory — Development Environment Doctor   "
echo "========================================================"

FAILURES=0
WARNINGS=0

check_cmd() {
  local name="$1"
  local cmd="$2"
  local min_ver="${3:-}"
  printf "%-30s ... " "$name"
  if command -v "$cmd" >/dev/null 2>&1; then
    local ver
    ver=$("$cmd" --version 2>&1 | head -n 1)
    echo "[OK] ($ver)"
  else
    echo "[MISSING]"
    ((FAILURES++))
  fi
}

check_cmd_optional() {
  local name="$1"
  local cmd="$2"
  printf "%-30s ... " "$name (optional)"
  if command -v "$cmd" >/dev/null 2>&1; then
    local ver
    ver=$("$cmd" --version 2>&1 | head -n 1)
    echo "[OK] ($ver)"
  else
    echo "[NOT INSTALLED] (optional)"
    ((WARNINGS++))
  fi
}

# 1. OS & Hardware Info
echo ""
echo "--- 1. Operating System & Architecture ---"
echo "OS: $(uname -s) $(uname -r)"
echo "Arch: $(uname -m)"

# 2. Required Runtimes
echo ""
echo "--- 2. Core Runtimes & Tooling ---"
check_cmd "Node.js" "node"
check_cmd "npm" "npm"
check_cmd "Python 3" "python3"
check_cmd "Git" "git"
check_cmd_optional "Docker" "docker"
check_cmd_optional "Docker Compose" "docker compose"
check_cmd_optional "FFmpeg" "ffmpeg"
check_cmd_optional "FFprobe" "ffprobe"
check_cmd_optional "Temporal CLI" "temporal"

# 3. Frozen Baseline Integrity
echo ""
echo "--- 3. Frozen Baseline Integrity Verification ---"
printf "%-30s ... " "Baseline Spec Package"
if [[ -f "$WORKSPACE_ROOT/01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/verify_package.py" ]]; then
  if python3 "$WORKSPACE_ROOT/01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/verify_package.py" >/dev/null 2>&1; then
    echo "[OK] (60/60 files verified, tree hash match)"
  else
    echo "[FAILED: HASH MISMATCH]"
    ((FAILURES++))
  fi
else
  echo "[FAILED: VERIFY SCRIPT MISSING]"
  ((FAILURES++))
fi

printf "%-30s ... " "Release ZIP & Sidecar"
if [[ -f "$WORKSPACE_ROOT/01_FROZEN_RELEASE/distributable/AVF_FINAL_FREEZE_v1.0.0_REMEDIATED.zip.sha256" ]]; then
  cd "$WORKSPACE_ROOT/01_FROZEN_RELEASE/distributable"
  if shasum -a 256 -c "AVF_FINAL_FREEZE_v1.0.0_REMEDIATED.zip.sha256" >/dev/null 2>&1; then
    echo "[OK] (SHA-256 sidecar verified)"
  else
    echo "[FAILED: ZIP CHECKSUM MISMATCH]"
    ((FAILURES++))
  fi
  cd "$WORKSPACE_ROOT"
else
  echo "[FAILED: SIDECAR MISSING]"
  ((FAILURES++))
fi

# 4. Port Availability Check
echo ""
echo "--- 4. Port Availability Diagnostics ---"
check_port() {
  local port="$1"
  local service="$2"
  printf "%-30s (Port %s) ... " "$service" "$port"
  if lsof -Pi :"$port" -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "[OCCUPIED / RUNNING]"
  else
    echo "[AVAILABLE]"
  fi
}

check_port 5432 "PostgreSQL (R02)"
check_port 7233 "Temporal Server (R06)"
check_port 8088 "Temporal UI (R06)"
check_port 8090 "FakeVideoProvider (R07/R15)"
check_port 9000 "MinIO API (Storage)"
check_port 9001 "MinIO Console (Storage)"
check_port 4318 "OTel Collector (R14)"

# Summary
echo ""
echo "========================================================"
if [[ $FAILURES -eq 0 ]]; then
  echo "DOCTOR VERDICT: PASS (Environment is ready for implementation)"
  exit 0
else
  echo "DOCTOR VERDICT: FAIL ($FAILURES critical failure(s) detected)"
  exit 1
fi
