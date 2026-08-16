#!/usr/bin/env bash
# AI Video Factory — Frozen Mutation & Drift Detector
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== Verifying Protected Tree Hashes Against BASELINE.lock.json ==="

LOCK_FILE="$WORKSPACE_ROOT/BASELINE.lock.json"
if [[ ! -f "$LOCK_FILE" ]]; then
  echo "ERROR: BASELINE.lock.json not found at $LOCK_FILE" >&2
  exit 1
fi

python3 -c '
import os, sys, json, hashlib

workspace = "'"$WORKSPACE_ROOT"'"
with open(os.path.join(workspace, "BASELINE.lock.json")) as f:
    lock = json.load(f)

expected_tree_sha = lock["content_tree_sha256"]
expected_zip_sha = lock["final_zip_sha256"]

# 1. Verify content tree hash
hash_file = os.path.join(workspace, "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/CONTENT_HASHES.json")
if not os.path.exists(hash_file):
    print("ERROR: CONTENT_HASHES.json not found", file=sys.stderr)
    sys.exit(1)

with open(hash_file) as f:
    expected_file_hashes = json.load(f)

base_dir = os.path.join(workspace, "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE")
tree_lines = []
for rel_p, exp_sha in sorted(expected_file_hashes.items()):
    fp = os.path.join(base_dir, rel_p)
    if not os.path.exists(fp):
        print(f"MUTATION DRIFT: Missing file {rel_p}", file=sys.stderr)
        sys.exit(1)
    with open(fp, "rb") as fh:
        act_sha = hashlib.sha256(fh.read()).hexdigest()
    if act_sha != exp_sha:
        print(f"MUTATION DRIFT: File {rel_p} hash changed! Expected {exp_sha}, got {act_sha}", file=sys.stderr)
        sys.exit(1)
    tree_lines.append(rel_p + "\t" + act_sha)

computed_tree_sha = hashlib.sha256(("\n".join(tree_lines) + "\n").encode("utf-8")).hexdigest()
if computed_tree_sha != expected_tree_sha:
    print(f"MUTATION DRIFT: Content tree SHA mismatch! Expected {expected_tree_sha}, computed {computed_tree_sha}", file=sys.stderr)
    sys.exit(1)

# 2. Verify distributable zip sha
zip_path = os.path.join(workspace, "01_FROZEN_RELEASE/distributable/AVF_FINAL_FREEZE_v1.0.0_REMEDIATED.zip")
with open(zip_path, "rb") as fz:
    act_zip_sha = hashlib.sha256(fz.read()).hexdigest()

if act_zip_sha != expected_zip_sha:
    print(f"MUTATION DRIFT: Distributable ZIP hash changed! Expected {expected_zip_sha}, got {act_zip_sha}", file=sys.stderr)
    sys.exit(1)

print(f"CONTENT_TREE_SHA256: {computed_tree_sha} (MATCH)")
print(f"RELEASE_ZIP_SHA256:  {act_zip_sha} (MATCH)")
print("Frozen drift: 0 (ZERO DRIFT)")
'

echo "=== No Frozen Mutation Verification: OK ==="
