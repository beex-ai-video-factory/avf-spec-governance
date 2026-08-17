#!/usr/bin/env python3
import os
import sys

RUNBOOK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REQUIRED_REPOS = [
    ("R01", "02_R01_CONTRACTS", "R01_contracts"),
    ("R14", "15_R14_OBSERVABILITY", "R14_platform_observability"),
    ("R02", "03_R02_CORE_STATE", "R02_core_state"),
    ("R07", "04_R07_PROVIDER_SDK", "R07_provider_sdk"),
    ("R06", "05_R06_WORKFLOW", "R06_workflow"),
    ("R15", "06_R15_INTEGRATION_HARNESS", "R15_integration_harness"),
    ("R08", "07_R08_GOOGLE_FLOW_ADAPTER", "R08_google_flow_adapter"),
    ("R10", "08_R10_FLOWKIT_BRIDGE", "R10_flowkit_bridge"),
    ("R09", "09_R09_BROWSER_WORKER", "R09_browser_worker"),
    ("R03", "10_R03_CREATIVE", "R03_creative"),
    ("R04", "11_R04_ASSETS_CONTINUITY", "R04_assets_continuity"),
    ("R05", "12_R05_PROMPT_COMPILER", "R05_prompt_compiler"),
    ("R11", "13_R11_QC", "R11_qc"),
    ("R12", "14_R12_MEDIA", "R12_media"),
    ("R13", "16_R13_OPERATOR_CONSOLE", "R13_operator_console"),
]

PROMPT_SUFFIXES = [
    "01_PLAN.md",
    "02_IMPLEMENT.md",
    "03_TEST_AND_REVIEW.md",
    "04_ACCEPT_RELEASE.md",
    "RECOVERY.md"
]

def validate():
    print("[4/7] Running validate_repo_coverage.py...")
    failures = 0
    
    for r_id, r_dir, r_name in REQUIRED_REPOS:
        target_dir = os.path.join(RUNBOOK_DIR, r_dir)
        if not os.path.exists(target_dir):
            print(f"FAIL: Missing directory for {r_id} at {r_dir}")
            failures += 1
            continue
            
        for s in PROMPT_SUFFIXES:
            fname = f"{r_id}_{s}"
            fpath = os.path.join(target_dir, fname)
            if not os.path.exists(fpath):
                print(f"FAIL: Missing prompt {fname} in {r_dir}")
                failures += 1
                
    if failures > 0:
        print(f"FAIL: Repository coverage check failed with {failures} missing files.")
        return False
        
    print(f"PASS: 15/15 repositories fully covered with 5-prompt standard suites (75/75 prompts).")
    return True

if __name__ == "__main__":
    if not validate():
        sys.exit(1)
