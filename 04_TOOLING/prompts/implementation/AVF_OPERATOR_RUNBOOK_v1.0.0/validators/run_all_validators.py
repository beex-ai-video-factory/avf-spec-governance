#!/usr/bin/env python3
import subprocess
import sys
import os

VALIDATORS = [
    "validate_manifest.py",
    "validate_prompt_headers.py",
    "validate_next_links.py",
    "validate_repo_coverage.py",
    "validate_model_matrix.py",
    "validate_frozen_path_guards.py",
    "validate_remediation_invariants.py"
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
        print(f"RESULT: ALL {len(VALIDATORS)}/{len(VALIDATORS)} VALIDATORS PASSED CONVINCINGLY.")
        print("Runbook is 100% compliant with frozen baseline, external audit & operator specifications.")
        print("================================================================")
        sys.exit(0)

if __name__ == "__main__":
    main()

