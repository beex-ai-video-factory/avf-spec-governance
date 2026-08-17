#!/usr/bin/env python3
"""
AI Video Factory v1.0.0 — Comprehensive Human Operator Runbook Generator
Generates the complete, production-grade 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/ pack.
"""

import os
import sys
import yaml
import json

BASE_DIR = "/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW"
RUNBOOK_DIR = os.path.join(BASE_DIR, "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0")

# Ensure target directories exist
SUBDIRS = [
    "00_CHECKPOINTS",
    "01_REPO_PROVISIONING",
    "02_R01_CONTRACTS",
    "03_R02_CORE_STATE",
    "04_R07_PROVIDER_SDK",
    "05_R06_WORKFLOW",
    "06_R15_INTEGRATION_HARNESS",
    "07_R08_GOOGLE_FLOW_ADAPTER",
    "08_R10_FLOWKIT_BRIDGE",
    "09_R09_BROWSER_WORKER",
    "10_R03_CREATIVE",
    "11_R04_ASSETS_CONTINUITY",
    "12_R05_PROMPT_COMPILER",
    "13_R11_QC",
    "14_R12_MEDIA",
    "15_R14_OBSERVABILITY",
    "16_R13_OPERATOR_CONSOLE",
    "17_INTEGRATION_GATES",
    "18_RELEASE",
    "99_RECOVERY",
    "validators"
]

for d in SUBDIRS:
    os.makedirs(os.path.join(RUNBOOK_DIR, d), exist_ok=True)

print("Created all target directories.")
