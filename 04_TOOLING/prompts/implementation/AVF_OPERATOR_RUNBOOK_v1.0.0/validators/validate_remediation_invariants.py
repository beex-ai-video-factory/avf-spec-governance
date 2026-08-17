#!/usr/bin/env python3
import os
import yaml
import sys
import re

RUNBOOK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(RUNBOOK_DIR))))
MANIFEST_PATH = os.path.join(RUNBOOK_DIR, "RUNBOOK_MANIFEST.yaml")

def validate():
    print("[7/7] Running validate_remediation_invariants.py...")
    failures = []
    
    # 1. Load manifest
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = yaml.safe_load(f)
    prompts_map = {p["id"]: p for p in manifest.get("prompts", [])}
    
    # 2. Verify MB-01: GATE-02 exact prerequisites
    gate_02 = prompts_map.get("GATE-02")
    if not gate_02:
        failures.append("GATE-02 entry missing from manifest")
    else:
        expected_g02 = ["R09-04", "R10-04", "R08-04", "GATE-01"]
        if gate_02.get("prerequisites") != expected_g02:
            failures.append(f"MB-01 Failed: GATE-02 prereqs {gate_02.get('prerequisites')} != {expected_g02}")
            
    # 3. Verify MB-02: GATE-03 exact prerequisites
    gate_03 = prompts_map.get("GATE-03")
    if not gate_03:
        failures.append("GATE-03 entry missing from manifest")
    else:
        expected_g03 = ["R12-04", "R11-04", "R05-04", "R04-04", "R03-04", "GATE-02"]
        if gate_03.get("prerequisites") != expected_g03:
            failures.append(f"MB-02 Failed: GATE-03 prereqs {gate_03.get('prerequisites')} != {expected_g03}")
            
    # 4. Verify all integration gates: manifest prereqs == prompt header prereqs
    all_gates = {
        "GATE-00": ["R07-04", "R02-04", "R14-04", "R01-04"],
        "GATE-01": ["R15-04", "R06-04", "GATE-00"],
        "GATE-02": ["R09-04", "R10-04", "R08-04", "GATE-01"],
        "GATE-03": ["R12-04", "R11-04", "R05-04", "R04-04", "R03-04", "GATE-02"],
        "GATE-04": ["R13-04", "GATE-03", "GATE-01"],
        "GATE-05": ["GATE-04"],
    }
    for gid, expected in all_gates.items():
        g_entry = prompts_map.get(gid)
        if not g_entry:
            failures.append(f"{gid} missing from manifest")
            continue
        if g_entry.get("prerequisites") != expected:
            failures.append(f"{gid} manifest prereqs mismatch: {g_entry.get('prerequisites')} != {expected}")
        g_file = os.path.join(RUNBOOK_DIR, g_entry["path"])
        with open(g_file, "r", encoding="utf-8") as gf:
            content = gf.read()
        m = re.search(r"\*\*PREREQUISITES:\*\*\s*(.+)", content)
        if not m:
            failures.append(f"{gid} prompt header missing PREREQUISITES")
        else:
            header_prereqs = [x.strip().replace("`", "") for x in m.group(1).split(",") if x.strip()]
            if header_prereqs != expected:
                failures.append(f"{gid} prompt header prereqs mismatch: {header_prereqs} != {expected}")
                
    # 5. Verify RESULT supports BLOCKED across root documents
    start_here = open(os.path.join(RUNBOOK_DIR, "START_HERE.md"), encoding="utf-8").read()
    op_rules = open(os.path.join(RUNBOOK_DIR, "OPERATOR_RULES.md"), encoding="utf-8").read()
    fail_tree = open(os.path.join(RUNBOOK_DIR, "FAILURE_DECISION_TREE.md"), encoding="utf-8").read()
    run_state_tpl = open(os.path.join(RUNBOOK_DIR, "RUN_STATE_TEMPLATE.yaml"), encoding="utf-8").read()
    
    if "BLOCKED" not in start_here:
        failures.append("START_HERE.md missing BLOCKED result definition")
    if "BLOCKED" not in op_rules:
        failures.append("OPERATOR_RULES.md missing BLOCKED result definition")
    if "BLOCKED" not in fail_tree:
        failures.append("FAILURE_DECISION_TREE.md missing BLOCKED result definition")
    if "BLOCKED" not in run_state_tpl:
        failures.append("RUN_STATE_TEMPLATE.yaml missing BLOCKED status support")
        
    # 6. Verify canonical human path is sequential (parallel_group: NONE for all manifest entries)
    non_none_parallel = [p["id"] for p in manifest.get("prompts", []) if p.get("parallel_group") != "NONE"]
    if non_none_parallel:
        failures.append(f"Non-NONE parallel_group found in prompts: {non_none_parallel}")
    master_seq = open(os.path.join(RUNBOOK_DIR, "MASTER_SEQUENCE.md"), encoding="utf-8").read()
    if "SAFE SEQUENTIAL OPERATOR MODE" not in master_seq:
        failures.append("MASTER_SEQUENCE.md does not establish SAFE SEQUENTIAL OPERATOR MODE")
        
    # 7. Verify all 99 prompts have ALLOWED_WRITE_ROOT and FORBIDDEN_WRITE_PATHS
    prompt_count = 0
    for root, dirs, files in os.walk(RUNBOOK_DIR):
        rel_root = os.path.relpath(root, RUNBOOK_DIR)
        if "validators" in root or any(part.startswith("_") for part in rel_root.split(os.sep)):
            continue
        for f in files:
            if f.endswith(".md"):
                rel_path = os.path.relpath(os.path.join(root, f), RUNBOOK_DIR)
                if "/" not in rel_path and rel_path != "RESUME_PROJECT.md":
                    continue
                if rel_path.startswith("19_MAINTENANCE") and not f.startswith("MAINT_"):
                    continue
                prompt_count += 1
                p_content = open(os.path.join(root, f), encoding="utf-8").read()
                if "**ALLOWED_WRITE_ROOT:**" not in p_content:
                    failures.append(f"{rel_path} missing ALLOWED_WRITE_ROOT header")
                if "**FORBIDDEN_WRITE_PATHS:**" not in p_content and "**FORBIDDEN_PATHS:**" not in p_content:
                    failures.append(f"{rel_path} missing FORBIDDEN_WRITE_PATHS header")
                    
    if prompt_count != 99:
        failures.append(f"Expected 99 execution prompts, scanned {prompt_count}")
        
    # 8. Verify post-v1.0.0 maintenance route exists
    maint_file = os.path.join(RUNBOOK_DIR, "19_MAINTENANCE", "MAINTENANCE_LIFECYCLE.md")
    if not os.path.exists(maint_file):
        failures.append("19_MAINTENANCE/MAINTENANCE_LIFECYCLE.md does not exist")
    else:
        m_content = open(maint_file, encoding="utf-8").read()
        for route_term in ["Hotfix", "Security Patch", "Contract Patch", "Implementation Bugfix", "Frozen Spec Defect", "Minor Feature Release", "Emergency Production Rollback"]:
            if route_term.lower() not in m_content.lower():
                failures.append(f"Maintenance guide missing section for: {route_term}")
                
    # 9. Verify no application implementation code was created in 05_IMPLEMENTATION/repos/
    impl_repos_dir = os.path.join(WORKSPACE_ROOT, "05_IMPLEMENTATION", "repos")
    if os.path.exists(impl_repos_dir):
        created_code_files = []
        for root, dirs, files in os.walk(impl_repos_dir):
            for f in files:
                if f.endswith((".ts", ".js", ".py", ".go", ".rs", ".java")):
                    created_code_files.append(os.path.join(root, f))
        if created_code_files:
            failures.append(f"Violated constraint: Application implementation files found: {created_code_files}")

    # Output report
    if failures:
        print(f"FAIL: {len(failures)} remediation invariant failures detected:")
        for fail in failures:
            print(f"  - {fail}")
        return False
        
    print("PASS: All remediation invariants verified:")
    print("  ✓ GATE-02 exact prerequisites (MB-01 resolved)")
    print("  ✓ GATE-03 exact prerequisites (MB-02 resolved)")
    print("  ✓ All 6 integration gate prerequisites 100% aligned across manifest & headers")
    print("  ✓ Formal RESULT: BLOCKED defined across documentation & state templates")
    print("  ✓ SAFE SEQUENTIAL OPERATOR MODE established as canonical golden path")
    print("  ✓ Explicit ALLOWED_WRITE_ROOT & FORBIDDEN_WRITE_PATHS present across all 99 prompts")
    print("  ✓ Post-v1.0.0 maintenance route fully documented (7 lifecycle routes)")
    print("  ✓ Zero application implementation code authored")
    return True

if __name__ == "__main__":
    if not validate():
        sys.exit(1)
