#!/usr/bin/env python3
"""
AI Video Factory v1.0.0 — GitHub Polyrepo Provisioning Verification Suite
PROMPT_ID: PROV-03
Verifies remotes, branch tracking, and protection rulesets for all 15 polyrepos + governance repo.
"""

import json
import os
import subprocess
import sys

ORGANIZATION = "beex-ai-video-factory"
BASE_DIR = "/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW"

ALL_REPOS = [
    {
        "repo_id": "GOV",
        "dir": ".",
        "gh_name": "avf-spec-governance",
    },
    {
        "repo_id": "R01",
        "dir": "05_IMPLEMENTATION/repos/R01_contracts",
        "gh_name": "avf-contracts",
    },
    {
        "repo_id": "R02",
        "dir": "05_IMPLEMENTATION/repos/R02_core_state",
        "gh_name": "avf-core-state",
    },
    {
        "repo_id": "R03",
        "dir": "05_IMPLEMENTATION/repos/R03_creative",
        "gh_name": "avf-creative",
    },
    {
        "repo_id": "R04",
        "dir": "05_IMPLEMENTATION/repos/R04_assets_continuity",
        "gh_name": "avf-assets-continuity",
    },
    {
        "repo_id": "R05",
        "dir": "05_IMPLEMENTATION/repos/R05_prompt_compiler",
        "gh_name": "avf-prompt-compiler",
    },
    {
        "repo_id": "R06",
        "dir": "05_IMPLEMENTATION/repos/R06_workflow",
        "gh_name": "avf-workflow",
    },
    {
        "repo_id": "R07",
        "dir": "05_IMPLEMENTATION/repos/R07_provider_sdk",
        "gh_name": "avf-provider-sdk",
    },
    {
        "repo_id": "R08",
        "dir": "05_IMPLEMENTATION/repos/R08_google_flow_adapter",
        "gh_name": "avf-google-flow-adapter",
    },
    {
        "repo_id": "R09",
        "dir": "05_IMPLEMENTATION/repos/R09_browser_worker",
        "gh_name": "avf-browser-worker",
    },
    {
        "repo_id": "R10",
        "dir": "05_IMPLEMENTATION/repos/R10_flowkit_bridge",
        "gh_name": "avf-flowkit-bridge",
    },
    {
        "repo_id": "R11",
        "dir": "05_IMPLEMENTATION/repos/R11_qc",
        "gh_name": "avf-qc",
    },
    {
        "repo_id": "R12",
        "dir": "05_IMPLEMENTATION/repos/R12_media",
        "gh_name": "avf-media",
    },
    {
        "repo_id": "R13",
        "dir": "05_IMPLEMENTATION/repos/R13_operator_console",
        "gh_name": "avf-operator-console",
    },
    {
        "repo_id": "R14",
        "dir": "05_IMPLEMENTATION/repos/R14_platform_observability",
        "gh_name": "avf-observability",
    },
    {
        "repo_id": "R15",
        "dir": "05_IMPLEMENTATION/repos/R15_integration_harness",
        "gh_name": "avf-integration-harness",
    },
]

def run_cmd(cmd, cwd=None):
    proc = subprocess.run(
        cmd,
        cwd=cwd or BASE_DIR,
        text=True,
        capture_output=True
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()

def verify():
    print("=" * 70)
    print("AI VIDEO FACTORY — GITHUB PROVISIONING VERIFICATION")
    print("=" * 70)

    passed_count = 0
    total_count = len(ALL_REPOS)

    for item in ALL_REPOS:
        repo_id = item["repo_id"]
        rel_dir = item["dir"]
        gh_name = item["gh_name"]
        repo_full_name = f"{ORGANIZATION}/{gh_name}"
        full_path = os.path.join(BASE_DIR, rel_dir)

        print(f"\n[{repo_id}] Verifying {gh_name} ({rel_dir})...")

        # 1. Check local git remote
        code, remotes_out, _ = run_cmd(["git", "remote", "-v"], cwd=full_path)
        if f"git@github.com:{repo_full_name}.git" not in remotes_out and f"https://github.com/{repo_full_name}.git" not in remotes_out:
            print(f"  ❌ FAILED: origin remote mismatch: {remotes_out}")
            continue

        # 2. Check local tracking branch
        code, branch_out, _ = run_cmd(["git", "branch", "-vv"], cwd=full_path)
        if "[origin/main" not in branch_out:
            print(f"  ❌ FAILED: main is not tracking origin/main: {branch_out}")
            continue

        # 3. Check GitHub remote repo
        code, view_out, _ = run_cmd(["gh", "repo", "view", repo_full_name, "--json", "name,isPrivate,defaultBranchRef"])
        if code != 0:
            print(f"  ❌ FAILED: gh repo view failed for {repo_full_name}")
            continue

        # 4. Check GitHub ruleset / branch protection
        code, rulesets_out, _ = run_cmd(["gh", "api", f"/repos/{repo_full_name}/rulesets"])
        if code != 0 or "main-protection" not in rulesets_out:
            print(f"  ❌ FAILED: branch protection ruleset not found on {repo_full_name}")
            continue

        print(f"  ✓ Local remote: OK")
        print(f"  ✓ Upstream tracking: [origin/main] OK")
        print(f"  ✓ GitHub repo: {repo_full_name} OK")
        print(f"  ✓ Branch protection ruleset: ACTIVE OK")
        passed_count += 1

    print("\n" + "=" * 70)
    print(f"VERIFICATION RESULT: {passed_count}/{total_count} PASSED")
    print("=" * 70)

    if passed_count == total_count:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    verify()
