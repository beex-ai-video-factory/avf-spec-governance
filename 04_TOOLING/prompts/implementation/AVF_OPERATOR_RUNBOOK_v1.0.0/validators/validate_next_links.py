#!/usr/bin/env python3
import os
import yaml
import sys

RUNBOOK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(RUNBOOK_DIR, "RUNBOOK_MANIFEST.yaml")

def validate():
    print("[3/7] Running validate_next_links.py...")
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        
    prompts = data.get("prompts", [])
    valid_paths = set(p["path"] for p in prompts)
    valid_ids = set(p["id"] for p in prompts)
    
    failures = 0
    for p in prompts:
        pass_link = p["pass_next"]
        fail_link = p["fail_next"]
        
        is_dynamic_or_dispatch = pass_link.startswith("Dynamic") or pass_link.startswith("Deterministic")
        if pass_link != "TERMINAL_COMPLETE" and not is_dynamic_or_dispatch:
            clean_pass = pass_link.replace("04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/", "")
            if clean_pass not in valid_paths and pass_link not in valid_ids:
                print(f"FAIL: Prompt {p['id']} has unresolved pass_next link: {pass_link}")
                failures += 1
                
        is_fail_dispatch = fail_link.startswith("Dynamic") or fail_link.startswith("Deterministic")
        if fail_link != "TERMINAL_COMPLETE" and not is_fail_dispatch:
            clean_fail = fail_link.replace("04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/", "")
            if clean_fail not in valid_paths and fail_link not in valid_ids:
                print(f"FAIL: Prompt {p['id']} has unresolved fail_next link: {fail_link}")
                failures += 1
                
    if failures > 0:
        print(f"FAIL: {failures} dangling next links found.")
        return False
        
    print(f"PASS: Zero dangling links across all {len(prompts)} prompts. Graph resolves completely.")
    return True

if __name__ == "__main__":
    if not validate():
        sys.exit(1)

