#!/usr/bin/env python3
import os
import yaml
import sys

RUNBOOK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(RUNBOOK_DIR, "RUNBOOK_MANIFEST.yaml")

FROZEN_PREFIXES = [
    "01_FROZEN_RELEASE",
    "02_SOURCE_KITS_READONLY",
    "03_GOVERNANCE_EVIDENCE_READONLY",
    "90_ARCHIVE_READONLY"
]

def validate():
    print("[6/7] Running validate_frozen_path_guards.py...")
    with open(MANIFEST_PATH, "r") as f:
        data = yaml.safe_load(f)
        
    prompts = data.get("prompts", [])
    failures = 0
    
    for p in prompts:
        writes = p.get("writes_to", [])
        forbidden = p.get("forbidden_writes", [])
        
        for w in writes:
            for frz in FROZEN_PREFIXES:
                if w.startswith(frz):
                    print(f"FAIL: Prompt {p['id']} declares writable access to frozen path: {w}")
                    failures += 1
                    
        for frz in FROZEN_PREFIXES:
            guarded = any(f.startswith(frz) for f in forbidden)
            if not guarded:
                print(f"FAIL: Prompt {p['id']} does not explicitly forbid writes to {frz}")
                failures += 1
                
    if failures > 0:
        print(f"FAIL: Frozen path guard check failed with {failures} violations.")
        return False
        
    print("PASS: Zero frozen-write permissions found. Absolute baseline protection confirmed across all prompts.")
    return True

if __name__ == "__main__":
    if not validate():
        sys.exit(1)
