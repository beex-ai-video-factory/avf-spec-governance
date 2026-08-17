#!/usr/bin/env python3
import os
import yaml
import sys
import re

RUNBOOK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(RUNBOOK_DIR, "RUNBOOK_MANIFEST.yaml")

EXPECTED_GATE_PREREQS = {
    "GATE-00": ["R07-04", "R02-04", "R14-04", "R01-04"],
    "GATE-01": ["R15-04", "R06-04", "GATE-00"],
    "GATE-02": ["R09-04", "R10-04", "R08-04", "GATE-01"],
    "GATE-03": ["R12-04", "R11-04", "R05-04", "R04-04", "R03-04", "GATE-02"],
    "GATE-04": ["R13-04", "GATE-03", "GATE-01"],
    "GATE-05": ["GATE-04"],
}

def validate():
    print("[1/7] Running validate_manifest.py...")
    if not os.path.exists(MANIFEST_PATH):
        print(f"FAIL: Manifest not found at {MANIFEST_PATH}")
        return False
        
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        
    prompts = data.get("prompts", [])
    if len(prompts) == 0:
        print("FAIL: Zero prompts found in manifest.")
        return False
        
    ids = set()
    required_keys = ["id", "path", "phase", "repo", "purpose", "model", "model_fallback", "mode", "conversation_type", "pass_next", "fail_next", "writes_to", "forbidden_writes"]
    
    for p in prompts:
        for k in required_keys:
            if k not in p or p[k] is None:
                print(f"FAIL: Prompt {p.get('id')} missing required key '{k}'")
                return False
                
        if p["id"] in ids:
            print(f"FAIL: Duplicate prompt ID detected: {p['id']}")
            return False
        ids.add(p["id"])
        
        file_path = os.path.join(RUNBOOK_DIR, p["path"])
        if not os.path.exists(file_path):
            print(f"FAIL: Referenced file does not exist: {p['path']}")
            return False
            
        # Check gate prerequisites alignment
        pid = p["id"]
        if pid in EXPECTED_GATE_PREREQS:
            expected = EXPECTED_GATE_PREREQS[pid]
            manifest_prereqs = p.get("prerequisites", [])
            if manifest_prereqs != expected:
                print(f"FAIL: {pid} manifest prerequisites mismatch. Expected {expected}, got {manifest_prereqs}")
                return False
                
            # Verify match with prompt file header
            with open(file_path, "r", encoding="utf-8") as pf:
                header_text = pf.read()
            m = re.search(r"\*\*PREREQUISITES:\*\*\s*(.+)", header_text)
            if not m:
                print(f"FAIL: {pid} prompt file missing PREREQUISITES header")
                return False
            raw_header_prereqs = [x.strip().replace("`", "") for x in m.group(1).split(",") if x.strip() and x.strip() != "None"]
            if raw_header_prereqs != expected:
                print(f"FAIL: {pid} prompt header prerequisites mismatch. Expected {expected}, got {raw_header_prereqs}")
                return False

    print(f"PASS: Manifest is valid with {len(prompts)} uniquely identified prompts and all gate prerequisites 100% aligned.")
    return True

if __name__ == "__main__":
    if not validate():
        sys.exit(1)

