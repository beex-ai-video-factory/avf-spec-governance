#!/usr/bin/env bash
set -euo pipefail

WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
REPOS_DIR="$WORKSPACE_ROOT/05_IMPLEMENTATION/repos"

echo "=== Verifying 15 Polyrepos Git Initialization & Artifacts ==="

REPOS=(
  "R01_contracts"
  "R02_core_state"
  "R03_creative"
  "R04_assets_continuity"
  "R05_prompt_compiler"
  "R06_workflow"
  "R07_provider_sdk"
  "R08_google_flow_adapter"
  "R09_browser_worker"
  "R10_flowkit_bridge"
  "R11_qc"
  "R12_media"
  "R13_operator_console"
  "R14_platform_observability"
  "R15_integration_harness"
)

PASSED=0
FAILED=0

for repo in "${REPOS[@]}"; do
  repo_path="$REPOS_DIR/$repo"
  
  if [[ ! -d "$repo_path/.git" ]]; then
    echo "FAIL: $repo is missing .git"
    FAILED=$((FAILED + 1))
    continue
  fi
  
  if [[ ! -f "$repo_path/.gitignore" ]]; then
    echo "FAIL: $repo is missing .gitignore"
    FAILED=$((FAILED + 1))
    continue
  fi
  
  if [[ ! -f "$repo_path/README.md" ]]; then
    echo "FAIL: $repo is missing README.md"
    FAILED=$((FAILED + 1))
    continue
  fi
  
  branch=$(cd "$repo_path" && git rev-parse --abbrev-ref HEAD)
  if [[ "$branch" != "main" ]]; then
    echo "FAIL: $repo branch is '$branch', expected 'main'"
    FAILED=$((FAILED + 1))
    continue
  fi
  
  commit_count=$(cd "$repo_path" && git rev-list --count HEAD)
  if [[ "$commit_count" -lt 1 ]]; then
    echo "FAIL: $repo has no commits"
    FAILED=$((FAILED + 1))
    continue
  fi
  
  sha=$(cd "$repo_path" && git rev-parse HEAD)
  echo "OK: $repo [branch=$branch, commits=$commit_count, sha=${sha:0:8}]"
  PASSED=$((PASSED + 1))
done

echo ""
echo "Verification Summary: PASSED=$PASSED, FAILED=$FAILED (Total: ${#REPOS[@]})"

if [[ "$FAILED" -gt 0 ]]; then
  exit 1
fi
