#!/usr/bin/env python3
"""
AI Video Factory v1.0.0 — GitHub Polyrepo Provisioning Automation Script
PROMPT_ID: PROV-03
Configures GitHub remotes and branch protection rulesets for all AVF repositories.
"""

import json
import os
import subprocess
import sys

ORGANIZATION = "beex-ai-video-factory"
BASE_DIR = "/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW"

REPOS = [
    {
        "repo_id": "R01",
        "dir": "05_IMPLEMENTATION/repos/R01_contracts",
        "gh_name": "avf-contracts",
        "description": "AVF v1.0.0 R01: Contracts & Typed Schemas (Layer 0)",
    },
    {
        "repo_id": "R02",
        "dir": "05_IMPLEMENTATION/repos/R02_core_state",
        "gh_name": "avf-core-state",
        "description": "AVF v1.0.0 R02: Core State & Persistence Engine (Layer 1)",
    },
    {
        "repo_id": "R03",
        "dir": "05_IMPLEMENTATION/repos/R03_creative",
        "gh_name": "avf-creative",
        "description": "AVF v1.0.0 R03: Creative & Script Generation Engine (Layer 2)",
    },
    {
        "repo_id": "R04",
        "dir": "05_IMPLEMENTATION/repos/R04_assets_continuity",
        "gh_name": "avf-assets-continuity",
        "description": "AVF v1.0.0 R04: Assets & Character Continuity Service (Layer 2)",
    },
    {
        "repo_id": "R05",
        "dir": "05_IMPLEMENTATION/repos/R05_prompt_compiler",
        "gh_name": "avf-prompt-compiler",
        "description": "AVF v1.0.0 R05: Provider-Aware Prompt Compiler (Layer 2)",
    },
    {
        "repo_id": "R06",
        "dir": "05_IMPLEMENTATION/repos/R06_workflow",
        "gh_name": "avf-workflow",
        "description": "AVF v1.0.0 R06: Temporal Workflow Orchestrator (Layer 5)",
    },
    {
        "repo_id": "R07",
        "dir": "05_IMPLEMENTATION/repos/R07_provider_sdk",
        "gh_name": "avf-provider-sdk",
        "description": "AVF v1.0.0 R07: Provider Neutral SDK & FakeProvider (Layer 3)",
    },
    {
        "repo_id": "R08",
        "dir": "05_IMPLEMENTATION/repos/R08_google_flow_adapter",
        "gh_name": "avf-google-flow-adapter",
        "description": "AVF v1.0.0 R08: Google Flow Provider Adapter (Layer 3)",
    },
    {
        "repo_id": "R09",
        "dir": "05_IMPLEMENTATION/repos/R09_browser_worker",
        "gh_name": "avf-browser-worker",
        "description": "AVF v1.0.0 R09: Track A Browser Automation Worker (Layer 4)",
    },
    {
        "repo_id": "R10",
        "dir": "05_IMPLEMENTATION/repos/R10_flowkit_bridge",
        "gh_name": "avf-flowkit-bridge",
        "description": "AVF v1.0.0 R10: Track B Direct FlowKit Bridge (Layer 4)",
    },
    {
        "repo_id": "R11",
        "dir": "05_IMPLEMENTATION/repos/R11_qc",
        "gh_name": "avf-qc",
        "description": "AVF v1.0.0 R11: Quality Control & Validation Service (Layer 2)",
    },
    {
        "repo_id": "R12",
        "dir": "05_IMPLEMENTATION/repos/R12_media",
        "gh_name": "avf-media",
        "description": "AVF v1.0.0 R12: Media Processing & Assembly Service (Layer 2)",
    },
    {
        "repo_id": "R13",
        "dir": "05_IMPLEMENTATION/repos/R13_operator_console",
        "gh_name": "avf-operator-console",
        "description": "AVF v1.0.0 R13: Human-in-the-Loop Operator Console (Layer 5)",
    },
    {
        "repo_id": "R14",
        "dir": "05_IMPLEMENTATION/repos/R14_platform_observability",
        "gh_name": "avf-observability",
        "description": "AVF v1.0.0 R14: Observability, Telemetry & Security (Cross-Cutting)",
    },
    {
        "repo_id": "R15",
        "dir": "05_IMPLEMENTATION/repos/R15_integration_harness",
        "gh_name": "avf-integration-harness",
        "description": "AVF v1.0.0 R15: End-to-End Integration & Scenario Test Harness (Cross-Cutting)",
    },
]

RULESET_PAYLOAD = {
    "name": "main-protection",
    "target": "branch",
    "enforcement": "active",
    "conditions": {
        "ref_name": {
            "include": ["~DEFAULT_BRANCH"],
            "exclude": []
        }
    },
    "rules": [
        {
            "type": "deletion"
        },
        {
            "type": "non_fast_forward"
        },
        {
            "type": "pull_request",
            "parameters": {
                "required_approving_review_count": 0,
                "dismiss_stale_reviews_on_push": False,
                "require_code_owner_review": False,
                "require_last_push_approval": False,
                "required_review_thread_resolution": True
            }
        }
    ]
}

def run_cmd(cmd, cwd=None, input_data=None):
    proc = subprocess.run(
        cmd,
        cwd=cwd or BASE_DIR,
        input=input_data,
        text=True,
        capture_output=True
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()

def repo_exists(repo_full_name):
    code, out, err = run_cmd(["gh", "repo", "view", repo_full_name])
    return code == 0

def create_remote_repo(repo_full_name, description):
    print(f"Creating GitHub repository {repo_full_name}...")
    code, out, err = run_cmd([
        "gh", "repo", "create", repo_full_name,
        "--public",
        "--description", description
    ])
    if code != 0:
        print(f"Error creating {repo_full_name}: {err}")
        return False
    return True

def configure_local_remote_and_push(repo_dir, repo_full_name):
    full_path = os.path.join(BASE_DIR, repo_dir)
    remote_url = f"git@github.com:{repo_full_name}.git"
    
    # Check existing remotes
    code, out, _ = run_cmd(["git", "remote", "-v"], cwd=full_path)
    if "origin" in out:
        run_cmd(["git", "remote", "set-url", "origin", remote_url], cwd=full_path)
    else:
        run_cmd(["git", "remote", "add", "origin", remote_url], cwd=full_path)
    
    # Push to origin main
    print(f"Pushing main branch for {repo_dir} to {remote_url}...")
    code, out, err = run_cmd(["git", "push", "-u", "origin", "main"], cwd=full_path)
    if code != 0:
        print(f"Error pushing to {remote_url}: {err}")
        return False
    return True

def apply_ruleset(repo_full_name):
    print(f"Applying branch protection ruleset to {repo_full_name}...")
    # Check if ruleset already exists
    code, out, err = run_cmd(["gh", "api", f"/repos/{repo_full_name}/rulesets"])
    if code == 0 and out:
        try:
            existing_rulesets = json.loads(out)
            for r in existing_rulesets:
                if r.get("name") == "main-protection":
                    print(f"Ruleset already exists on {repo_full_name} (ID: {r.get('id')}).")
                    return True
        except Exception:
            pass

    payload_str = json.dumps(RULESET_PAYLOAD)
    code, out, err = run_cmd(
        ["gh", "api", "--method", "POST", f"/repos/{repo_full_name}/rulesets", "--input", "-"],
        input_data=payload_str
    )
    if code != 0:
        print(f"Error creating ruleset on {repo_full_name}: {err}")
        return False
    return True

def main():
    print("=" * 60)
    print("AI Video Factory — GitHub Polyrepo Provisioning Automation")
    print("=" * 60)
    
    success_count = 0
    total_repos = len(REPOS)

    for item in REPOS:
        repo_id = item["repo_id"]
        repo_dir = item["dir"]
        gh_name = item["gh_name"]
        description = item["description"]
        repo_full_name = f"{ORGANIZATION}/{gh_name}"

        print(f"\n--- [{repo_id}] {gh_name} ({repo_dir}) ---")

        # 1. Ensure remote repo exists
        if not repo_exists(repo_full_name):
            created = create_remote_repo(repo_full_name, description)
            if not created:
                print(f"FAILED to create remote repository {repo_full_name}")
                sys.exit(1)
        else:
            print(f"Remote repository {repo_full_name} already exists.")

        # 2. Configure local git remote & push
        pushed = configure_local_remote_and_push(repo_dir, repo_full_name)
        if not pushed:
            print(f"FAILED to push local repository {repo_dir} to {repo_full_name}")
            sys.exit(1)

        # 3. Apply branch protection ruleset
        ruleset_ok = apply_ruleset(repo_full_name)
        if not ruleset_ok:
            print(f"FAILED to apply ruleset on {repo_full_name}")
            sys.exit(1)

        success_count += 1
        print(f"SUCCESS: {repo_id} ({gh_name}) fully provisioned and protected.")

    print("\n" + "=" * 60)
    print(f"PROVISIONING COMPLETE: {success_count}/{total_repos} repositories successfully provisioned and protected.")
    print("=" * 60)

if __name__ == "__main__":
    main()
