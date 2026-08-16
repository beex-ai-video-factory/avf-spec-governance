#!/usr/bin/env bash
# AI Video Factory — Agent Customizations Validator
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== Checking Antigravity Rules in .agents/rules ==="
REQUIRED_RULES=(
  "frozen-baseline-guardian.md"
  "contract-first.md"
  "repo-boundary-enforcer.md"
  "test-gates.md"
  "change-control.md"
)

for r in "${REQUIRED_RULES[@]}"; do
  rf="$WORKSPACE_ROOT/.agents/rules/$r"
  if [[ ! -f "$rf" ]]; then
    echo "ERROR: Missing rule: $r" >&2
    exit 1
  fi
  echo "Rule $r: OK"
done
echo "All 5 required rules installed: OK"

echo "=== Checking Antigravity Skills in .agents/skills ==="
REQUIRED_SKILLS=(
  "avf-baseline-reader"
  "avf-contract-first"
  "avf-repo-boundaries"
  "avf-temporal-durability"
  "avf-provider-adapter"
  "avf-flow-execution-port"
  "avf-browser-worker-safety"
  "avf-qc-media"
  "avf-observability-security"
  "avf-implementation-done"
)

python3 -c '
import os, sys

workspace = "'"$WORKSPACE_ROOT"'"
skills = [
  "avf-baseline-reader",
  "avf-contract-first",
  "avf-repo-boundaries",
  "avf-temporal-durability",
  "avf-provider-adapter",
  "avf-flow-execution-port",
  "avf-browser-worker-safety",
  "avf-qc-media",
  "avf-observability-security",
  "avf-implementation-done"
]

for s in skills:
    sk_path = os.path.join(workspace, ".agents/skills", s, "SKILL.md")
    if not os.path.exists(sk_path):
        print(f"ERROR: Missing SKILL.md for {s}", file=sys.stderr)
        sys.exit(1)
    with open(sk_path, encoding="utf-8") as f:
        content = f.read()
    if not (content.startswith("---") and "name:" in content and "description:" in content):
        print(f"ERROR: SKILL.md for {s} missing valid YAML frontmatter", file=sys.stderr)
        sys.exit(1)
    print(f"Skill {s}: OK (valid YAML frontmatter)")

print(f"All {len(skills)} required skills validated: OK")
'

echo "=== Checking Antigravity Hooks in .agents/hooks.json ==="
HOOKS_FILE="$WORKSPACE_ROOT/.agents/hooks.json"
if [[ ! -f "$HOOKS_FILE" ]]; then
  echo "ERROR: Missing .agents/hooks.json" >&2
  exit 1
fi

python3 -c '
import json, sys
with open("'"$HOOKS_FILE"'") as f:
    data = json.load(f)
assert "hooks" in data, "hooks key missing"
assert "pre_tool_execution" in data["hooks"], "pre_tool_execution missing"
print(".agents/hooks.json: OK (valid JSON structure)")
'

echo "=== Agent Customizations Verification: ALL CHECKS PASSED ==="
