#!/usr/bin/env python3
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
    print("[5/7] Running validate_model_matrix.py...")
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
