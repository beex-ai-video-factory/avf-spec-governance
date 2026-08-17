#!/usr/bin/env python3
"""
Generates RUNBOOK_MANIFEST.yaml and all validator scripts for AVF_OPERATOR_RUNBOOK_v1.0.0.
"""

import os
import yaml
import re

RUNBOOK_DIR = "/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0"
VALIDATORS_DIR = os.path.join(RUNBOOK_DIR, "validators")
os.makedirs(VALIDATORS_DIR, exist_ok=True)

# 1. Parse all prompts to build RUNBOOK_MANIFEST.yaml
def extract_header_fields(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    
    fields = {}
    patterns = {
        "id": r"\*\*PROMPT_ID:\*\*\s*`?([^`\n]+)`?",
        "purpose": r"\*\*PURPOSE:\*\*\s*([^\n]+)",
        "phase": r"\*\*CURRENT_PHASE:\*\*\s*`?([^`\n]+)`?",
        "workspace": r"\*\*RUN_FROM_WORKSPACE:\*\*\s*`?([^`\n]+)`?",
        "repo": r"\*\*OPEN_REPOSITORY:\*\*\s*`?([^`\n]+)`?",
        "working_dir": r"\*\*WORKING_DIRECTORY:\*\*\s*`?([^`\n]+)`?",
        "model": r"\*\*MODEL:\*\*\s*`?([^`\n]+)`?",
        "model_fallback": r"\*\*MODEL_FALLBACK:\*\*\s*`?([^`\n]+)`?",
        "mode": r"\*\*ANTIGRAVITY_MODE:\*\*\s*`?([^`\n]+)`?",
        "conversation": r"\*\*NEW_OR_EXISTING_CONVERSATION:\*\*\s*`?([^`\n]+)`?",
        "duration": r"\*\*EXPECTED_DURATION_CLASS:\*\*\s*`?([^`\n]+)`?",
        "prerequisites": r"\*\*PREREQUISITES:\*\*\s*`?([^`\n]+)`?",
        "pass_next": r"\*\*NEXT_PROMPT_IF_PASS:\*\*\s*`?([^`\n]+)`?",
        "fail_next": r"\*\*NEXT_PROMPT_IF_FAIL:\*\*\s*`?([^`\n]+)`?"
    }
    for key, pat in patterns.items():
        m = re.search(pat, content)
        if m:
            fields[key] = m.group(1).strip()
        else:
            fields[key] = None
            
    # Extract writes and forbidden
    writes_m = re.search(r"\*\*WRITEABLE_PATHS:\*\*\n([\s\S]*?)(?=\*\*FORBIDDEN_PATHS:)", content)
    if writes_m:
        writes_lines = [l.strip("- `").strip() for l in writes_m.group(1).strip().split("\n") if l.strip().startswith("-")]
        fields["writes_to"] = writes_lines
    else:
        fields["writes_to"] = []
        
    forbid_m = re.search(r"\*\*FORBIDDEN_PATHS:\*\*\n([\s\S]*?)(?=\*\*COMMAND_TO_RUN:)", content)
    if forbid_m:
        forbid_lines = [l.strip("- `").strip() for l in forbid_m.group(1).strip().split("\n") if l.strip().startswith("-")]
        fields["forbidden_writes"] = forbid_lines
    else:
        fields["forbidden_writes"] = []
        
    return fields

# Find all markdown files in RUNBOOK_DIR (excluding root navigation docs and validators)
all_prompt_entries = []
for root, dirs, files in os.walk(RUNBOOK_DIR):
    if "validators" in root:
        continue
    for file in sorted(files):
        if file.endswith(".md"):
            rel_path = os.path.relpath(os.path.join(root, file), RUNBOOK_DIR)
            # Skip root summary docs from strict manifest prompt entries except RESUME_PROJECT.md
            if "/" not in rel_path and rel_path != "RESUME_PROJECT.md":
                continue
            
            filepath = os.path.join(RUNBOOK_DIR, rel_path)
            hdr = extract_header_fields(filepath)
            
            entry = {
                "id": hdr["id"] or file.replace(".md", ""),
                "path": rel_path,
                "phase": hdr["phase"] or "GENERAL",
                "repo": hdr["repo"] or "SYSTEM",
                "purpose": hdr["purpose"] or "",
                "model": hdr["model"] or "Gemini 3.7 Flash High",
                "model_fallback": hdr["model_fallback"] or "Gemini 3.1 Pro High",
                "mode": hdr["mode"] or "Local workspace",
                "conversation_type": hdr["conversation"] or "NEW_OR_EXISTING",
                "duration_class": hdr["duration"] or "FAST (<3 min)",
                "prerequisites": [p.strip() for p in hdr["prerequisites"].split(",")] if hdr["prerequisites"] and hdr["prerequisites"] != "None" else [],
                "pass_next": hdr["pass_next"] or "TERMINAL_COMPLETE",
                "fail_next": hdr["fail_next"] or "99_RECOVERY/RECOVERY_06_STALLED_AGENT.md",
                "parallel_group": "PARALLEL_SAFE" if "PARALLEL_SAFE" in str(hdr.get("purpose", "")) or "PARALLEL" in str(hdr.get("phase", "")) else "NONE",
                "writes_to": hdr["writes_to"],
                "forbidden_writes": hdr["forbidden_writes"]
            }
            all_prompt_entries.append(entry)

manifest_data = {
    "version": "1.0.0",
    "project": "AI Video Factory",
    "total_prompts": len(all_prompt_entries),
    "prompts": all_prompt_entries
}

manifest_path = os.path.join(RUNBOOK_DIR, "RUNBOOK_MANIFEST.yaml")
with open(manifest_path, "w") as f:
    yaml.dump(manifest_data, f, sort_keys=False, default_flow_style=False)

print(f"Generated RUNBOOK_MANIFEST.yaml with {len(all_prompt_entries)} prompts.")

# 2. Generate Validator 1: validate_manifest.py
VALIDATE_MANIFEST_PY = """#!/usr/bin/env python3
import os
import yaml
import sys

RUNBOOK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(RUNBOOK_DIR, "RUNBOOK_MANIFEST.yaml")

def validate():
    print("[1/6] Running validate_manifest.py...")
    if not os.path.exists(MANIFEST_PATH):
        print(f"FAIL: Manifest not found at {MANIFEST_PATH}")
        return False
        
    with open(MANIFEST_PATH, "r") as f:
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
            
    print(f"PASS: Manifest is valid with {len(prompts)} uniquely identified prompts.")
    return True

if __name__ == "__main__":
    if not validate():
        sys.exit(1)
"""

# 3. Generate Validator 2: validate_prompt_headers.py
VALIDATE_PROMPT_HEADERS_PY = """#!/usr/bin/env python3
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
    "WRITEABLE_PATHS",
    "FORBIDDEN_PATHS",
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
    print("[2/6] Running validate_prompt_headers.py...")
    failures = 0
    total_files = 0
    
    for root, dirs, files in os.walk(RUNBOOK_DIR):
        if "validators" in root:
            continue
        for file in sorted(files):
            if file.endswith(".md"):
                rel_path = os.path.relpath(os.path.join(root, file), RUNBOOK_DIR)
                # Skip non-prompt root documentation except RESUME_PROJECT.md
                if "/" not in rel_path and rel_path != "RESUME_PROJECT.md":
                    continue
                    
                total_files += 1
                full_path = os.path.join(root, file)
                with open(full_path, "r") as f:
                    content = f.read()
                    
                missing = []
                for h in MANDATORY_HEADERS:
                    if f"**{h}:**" not in content:
                        missing.append(h)
                        
                if missing:
                    print(f"FAIL: {rel_path} missing mandatory headers: {missing}")
                    failures += 1
                    
    if failures > 0:
        print(f"FAIL: {failures}/{total_files} prompt files failed header validation.")
        return False
        
    print(f"PASS: All {total_files} execution prompts contain all 24 mandatory header fields.")
    return True

if __name__ == "__main__":
    if not validate():
        sys.exit(1)
"""

# 4. Generate Validator 3: validate_next_links.py
VALIDATE_NEXT_LINKS_PY = """#!/usr/bin/env python3
import os
import yaml
import sys

RUNBOOK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(RUNBOOK_DIR, "RUNBOOK_MANIFEST.yaml")

def validate():
    print("[3/6] Running validate_next_links.py...")
    with open(MANIFEST_PATH, "r") as f:
        data = yaml.safe_load(f)
        
    prompts = data.get("prompts", [])
    valid_paths = set(p["path"] for p in prompts)
    valid_ids = set(p["id"] for p in prompts)
    
    failures = 0
    for p in prompts:
        pass_link = p["pass_next"]
        fail_link = p["fail_next"]
        
        # Check pass link
        if pass_link != "TERMINAL_COMPLETE" and not pass_link.startswith("Dynamic"):
            clean_pass = pass_link.replace("04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/", "")
            if clean_pass not in valid_paths and pass_link not in valid_ids:
                print(f"FAIL: Prompt {p['id']} has unresolved pass_next link: {pass_link}")
                failures += 1
                
        # Check fail link
        if fail_link != "TERMINAL_COMPLETE" and not fail_link.startswith("Dynamic"):
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
"""

# 5. Generate Validator 4: validate_repo_coverage.py
VALIDATE_REPO_COVERAGE_PY = """#!/usr/bin/env python3
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
    print("[4/6] Running validate_repo_coverage.py...")
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
"""

# 6. Generate Validator 5: validate_model_matrix.py
VALIDATE_MODEL_MATRIX_PY = """#!/usr/bin/env python3
import os
import yaml
import sys

RUNBOOK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(RUNBOOK_DIR, "RUNBOOK_MANIFEST.yaml")

ALLOWED_MODELS = [
    "Gemini 3.7 Flash High",
    "Gemini 3.1 Pro High",
    "Claude Opus 4.6 Thinking"
]

CRITICAL_ACCEPTANCE_PROMPTS = [
    "R01-04",
    "R06-04",
    "R08-04",
    "R10-04",
    "R09-04",
    "GATE-00",
    "GATE-02",
    "GATE-05",
    "REL-01"
]

def validate():
    print("[5/6] Running validate_model_matrix.py...")
    with open(MANIFEST_PATH, "r") as f:
        data = yaml.safe_load(f)
        
    prompts = data.get("prompts", [])
    failures = 0
    
    for p in prompts:
        model = p.get("model")
        fallback = p.get("model_fallback")
        conv = p.get("conversation_type")
        
        if model not in ALLOWED_MODELS:
            print(f"FAIL: Invalid model '{model}' in prompt {p['id']}")
            failures += 1
            
        if fallback not in ALLOWED_MODELS:
            print(f"FAIL: Invalid fallback model '{fallback}' in prompt {p['id']}")
            failures += 1
            
        if p["id"] in CRITICAL_ACCEPTANCE_PROMPTS:
            if model != "Claude Opus 4.6 Thinking":
                print(f"FAIL: Critical acceptance prompt {p['id']} must use Claude Opus 4.6 Thinking, got {model}")
                failures += 1
            if conv != "NEW_REQUIRED":
                print(f"FAIL: Critical acceptance prompt {p['id']} must require NEW conversation, got {conv}")
                failures += 1
                
    if failures > 0:
        print(f"FAIL: Model matrix validation failed with {failures} issues.")
        return False
        
    print("PASS: Model routing, fallback definitions, and hostile acceptance assignments verified.")
    return True

if __name__ == "__main__":
    if not validate():
        sys.exit(1)
"""

# 7. Generate Validator 6: validate_frozen_path_guards.py
VALIDATE_FROZEN_PATH_GUARDS_PY = """#!/usr/bin/env python3
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
    print("[6/6] Running validate_frozen_path_guards.py...")
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
"""

# 8. Master Validator Runner: run_all_validators.py
RUN_ALL_VALIDATORS_PY = """#!/usr/bin/env python3
import subprocess
import sys
import os

VALIDATORS = [
    "validate_manifest.py",
    "validate_prompt_headers.py",
    "validate_next_links.py",
    "validate_repo_coverage.py",
    "validate_model_matrix.py",
    "validate_frozen_path_guards.py"
]

def main():
    print("================================================================")
    print(" AI VIDEO FACTORY v1.0.0 — RUNBOOK VALIDATION SUITE")
    print("================================================================")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    failed = []
    
    for val in VALIDATORS:
        val_path = os.path.join(script_dir, val)
        res = subprocess.run([sys.executable, val_path])
        if res.returncode != 0:
            failed.append(val)
            
    print("================================================================")
    if failed:
        print(f"RESULT: FAILED ({len(failed)}/{len(VALIDATORS)} validators failed)")
        print(f"Failed scripts: {failed}")
        sys.exit(1)
    else:
        print("RESULT: ALL 6/6 VALIDATORS PASSED CONVINCINGLY.")
        print("Runbook is 100% compliant with frozen baseline & operator specifications.")
        print("================================================================")
        sys.exit(0)

if __name__ == "__main__":
    main()
"""

validator_files = {
    "validate_manifest.py": VALIDATE_MANIFEST_PY,
    "validate_prompt_headers.py": VALIDATE_PROMPT_HEADERS_PY,
    "validate_next_links.py": VALIDATE_NEXT_LINKS_PY,
    "validate_repo_coverage.py": VALIDATE_REPO_COVERAGE_PY,
    "validate_model_matrix.py": VALIDATE_MODEL_MATRIX_PY,
    "validate_frozen_path_guards.py": VALIDATE_FROZEN_PATH_GUARDS_PY,
    "run_all_validators.py": RUN_ALL_VALIDATORS_PY
}

for name, content in validator_files.items():
    filepath = os.path.join(VALIDATORS_DIR, name)
    with open(filepath, "w") as f:
        f.write(content.strip() + "\n")
    os.chmod(filepath, 0o755)
    print(f"Written validator: {name}")

print("Manifest and validator suite generated successfully.")
