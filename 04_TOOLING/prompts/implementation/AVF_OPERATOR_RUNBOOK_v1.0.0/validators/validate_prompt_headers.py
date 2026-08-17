#!/usr/bin/env python3
import os
import re
import sys

RUNBOOK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MANDATORY_HEADERS = [
    "PROMPT_ID",
    "PURPOSE",
    "CURRENT_PHASE",
    "RUN_FROM_WORKSPACE",
    "OPEN_REPOSITORY",
    "WORKING_DIRECTORY",
    "MODEL",
    "MODEL_FALLBACK",
    "ANTIGRAVITY_MODE",
    "NEW_OR_EXISTING_CONVERSATION",
    "EXPECTED_DURATION_CLASS",
    "PREREQUISITES",
    "READ_ONLY_INPUTS",
    "ALLOWED_WRITE_ROOT",
    "WRITEABLE_PATHS",
    "FORBIDDEN_WRITE_PATHS",
    "COMMAND_TO_RUN",
    "EXPECTED_ARTIFACTS",
    "PASS_CRITERIA",
    "FAIL_CRITERIA",
    "GIT_EXPECTATION",
    "HUMAN_ACTION_AFTER_PASS",
    "HUMAN_ACTION_AFTER_FAIL",
    "NEXT_PROMPT_IF_PASS",
    "NEXT_PROMPT_IF_FAIL"
]

def validate():
    print("[2/7] Running validate_prompt_headers.py...")
    failures = 0
    total_files = 0
    
    for root, dirs, files in os.walk(RUNBOOK_DIR):
        rel_root = os.path.relpath(root, RUNBOOK_DIR)
        if "validators" in root or any(part.startswith("_") for part in rel_root.split(os.sep)):
            continue
        for file in sorted(files):
            if file.endswith(".md"):
                rel_path = os.path.relpath(os.path.join(root, file), RUNBOOK_DIR)
                if "/" not in rel_path and rel_path != "RESUME_PROJECT.md":
                    continue
                # Skip non-prompt maintenance guide if present
                if rel_path.startswith("19_MAINTENANCE") and not file.startswith("MAINT_"):
                    continue
                    
                total_files += 1
                full_path = os.path.join(root, file)
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                missing = []
                for h in MANDATORY_HEADERS:
                    # Allow FORBIDDEN_PATHS as fallback for FORBIDDEN_WRITE_PATHS
                    if h == "FORBIDDEN_WRITE_PATHS":
                        if "**FORBIDDEN_WRITE_PATHS:**" not in content and "**FORBIDDEN_PATHS:**" not in content:
                            missing.append(h)
                    elif f"**{h}:**" not in content:
                        missing.append(h)
                        
                if missing:
                    print(f"FAIL: {rel_path} missing mandatory headers: {missing}")
                    failures += 1
                    
    if failures > 0:
        print(f"FAIL: {failures}/{total_files} prompt files failed header validation.")
        return False
        
    print(f"PASS: All {total_files} execution prompts contain all mandatory header fields (including ALLOWED_WRITE_ROOT and FORBIDDEN_WRITE_PATHS).")
    return True

if __name__ == "__main__":
    if not validate():
        sys.exit(1)

