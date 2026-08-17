#!/usr/bin/env bash
set -euo pipefail

WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
REPOS_DIR="$WORKSPACE_ROOT/05_IMPLEMENTATION/repos"

echo "=== Initializing Git Repositories in 05_IMPLEMENTATION/repos ==="

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

for repo in "${REPOS[@]}"; do
  repo_path="$REPOS_DIR/$repo"
  cd "$repo_path"
  
  # Remove .gitkeep if exists
  rm -f .gitkeep
  
  # Init git repo with default branch main
  if [[ ! -d .git ]]; then
    git init -b main
  else
    git checkout -B main
  fi
  
  git config user.name "minhson226" || true
  git config user.email "minhson226@gmail.com" || true
  
  git add .
  git commit -m "chore: initialize polyrepo scaffold" || true
  
  sha=$(git rev-parse HEAD)
  echo "REPO_INIT_RESULT: $repo | main | $sha"
done

echo "=== ALL 15 REPOSITORIES INITIALIZED SUCCESSFULLY ==="
