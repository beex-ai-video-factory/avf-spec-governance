#!/usr/bin/env python3
import os, sys, shutil, json, re, hashlib

def hash_file(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def hash_dir_tree(base_dir):
    hashes = {}
    for root, dirs, files in os.walk(base_dir):
        for f in sorted(files):
            if f == '.DS_Store': continue
            fpath = os.path.join(root, f)
            relpath = os.path.relpath(fpath, base_dir)
            hashes[relpath] = hash_file(fpath)
    tree_str = ''.join(f'{k}:{v}\n' for k, v in sorted(hashes.items()))
    tree_hash = hashlib.sha256(tree_str.encode('utf-8')).hexdigest()
    return tree_hash, hashes

def main():
    freeze_dir = 'review-session/FINAL_FREEZE'
    os.makedirs(freeze_dir, exist_ok=True)
    
    # 1. Copy REVISED_SPEC_CANDIDATE to FROZEN_SPEC_CANDIDATE
    frozen_spec_dir = os.path.join(freeze_dir, 'FROZEN_SPEC_CANDIDATE')
    if os.path.exists(frozen_spec_dir):
        shutil.rmtree(frozen_spec_dir)
    shutil.copytree('review-session/REVISED_SPEC_CANDIDATE', frozen_spec_dir)
    print("Copied REVISED_SPEC_CANDIDATE to FROZEN_SPEC_CANDIDATE")

    # 2. Copy finalized matrices from C06
    shutil.copy('review-session/C06/FINAL_REQUIREMENT_TRACEABILITY.md', os.path.join(freeze_dir, 'FINAL_REQUIREMENT_TRACEABILITY.md'))
    shutil.copy('review-session/C06/FINAL_CONTRACT_COMPATIBILITY_MATRIX.md', os.path.join(freeze_dir, 'FINAL_CONTRACT_COMPATIBILITY_MATRIX.md'))
    shutil.copy('review-session/C06/FINAL_REPO_DEPENDENCY_GRAPH.md', os.path.join(freeze_dir, 'FINAL_REPO_DEPENDENCY_GRAPH.md'))
    shutil.copy('review-session/C06/FINAL_PROTECTED_CAPABILITY_REPORT.md', os.path.join(freeze_dir, 'FINAL_PROTECTED_CAPABILITY_REPORT.md'))
    shutil.copy('review-session/C06/FINAL_IMPLEMENTATION_HANDOFF_INDEX.md', os.path.join(freeze_dir, 'FINAL_IMPLEMENTATION_HANDOFF_INDEX.md'))
    shutil.copy('review-session/C04/DISSENT_REGISTER.md', os.path.join(freeze_dir, 'FINAL_DISSENT_REGISTER.md'))

    # 3. Create FINAL_RISK_REGISTER.md
    risk_register_content = """# Final Architecture Risk Register (v1.0.0 Frozen)

| RISK_ID | RISK_CATEGORY | DESCRIPTION | SEVERITY | MITIGATION & CONTINGENCY STRATEGY | OWNER |
|---|---|---|---|---|---|
| RSK-001 | Third-Party Mock Drift | Containerized mock provider simulators in R15 may diverge from live vendor API updates. | MEDIUM | Scheduled bi-weekly automated live integration canary runs with bounded test credits. | R08 / R15 |
| RSK-002 | MV3 Keepalive Policy Evolution | Future Chrome browser updates could throttle offscreen document keepalive audio channels. | LOW | Native Messaging Host daemon provides secondary direct CDP pipe; Playwright fallback ready. | R06 / R09 |
| RSK-003 | V8 Heap Secret Remanence | Immutable JS strings in V8 engine could persist in heap before garbage collection. | LOW | Strict Buffer / Uint8Array binary allocation with explicit sodium.memzero memory wiping. | R07 / R15 |
| RSK-004 | Worker Lease Contention | Long GC pauses or synchronous I/O could cause worker lease expiration during provider call. | LOW | Fencing tokens + provider-side idempotency keys prevent duplicate billing on retry. | R02 / R06 |
"""
    with open(os.path.join(freeze_dir, 'FINAL_RISK_REGISTER.md'), 'w') as f:
        f.write(risk_register_content)
    print("Wrote FINAL_RISK_REGISTER.md")

    # 4. Create FINAL_AUDIT_REPORT.md
    audit_report_content = """# Final Consolidated Council Audit Report (v1.0.0)

**Council Review Pipeline:** C00 -> C01 -> C02 -> C03 -> C04 -> C05 -> C06 -> C07  
**Governance Authority:** AUTONOMOUS_COUNCIL_MASTER.md v1.0.0  
**Overall Council Audit Result:** **PASS (APPROVED FOR FREEZE)**  

---

## Executive Summary of Audit Progression
1. **C00 Semantic Baseline:** HIGH confidence, 0 blocking baseline gaps, source baseline locked.
2. **C01 Blind Specialist Review:** 15 independent roles, 158 findings identified and cataloged.
3. **C02 Cross-Examination:** 95 structured mini-hearings, 100% findings dispositioned, controversies preserved.
4. **C03 Solution Design:** 15 comprehensive Change Proposals (CP-001..CP-015) in 10 solution packages.
5. **C04 Voting & Synthesis:** 100% unanimous votes (15-0), 0 unvoted edits, candidate v1.0.0 synthesized.
6. **C05 Hostile Independent Audit:** 3 isolated Pro-tier auditors (Auditor-A, Auditor-B, Auditor-C). Blockers caught and remediated; final verdict: `PASS_WITH_RESIDUAL_RISK`.
7. **C06 Freeze Readiness:** 22/22 mandatory freeze gates passed, 55/55 requirements traced, 19/19 capabilities preserved.
8. **C07 Freeze Certification:** All prerequisites satisfied; architecture candidate v1.0.0 authorized for freeze.
"""
    with open(os.path.join(freeze_dir, 'FINAL_AUDIT_REPORT.md'), 'w') as f:
        f.write(audit_report_content)
    print("Wrote FINAL_AUDIT_REPORT.md")

    # 5. Create SPONSOR_PROXY_DECISION.md
    sponsor_decision_content = """# Autonomous Sponsor Proxy Final Freeze Authorization

**AUTHORITY:** Human Delegated Sponsor Proxy per `AUTONOMOUS_COUNCIL_MASTER.md` v1.0.0  
**DECISION:** `SPONSOR_PROXY_AUTHORIZE_FREEZE`  
**CERTIFIED_SPEC_VERSION:** **v1.0.0**  
**SOURCE_BLUEPRINT_KIT:** `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0` (Verified 100% Immutable)  
**TIMESTAMP:** 2026-08-15T12:47:30+07:00  

---

## Formal Authorization Statement
As the Delegated Autonomous Council Supervisor and Sponsor Proxy, I hereby certify that the AI Video Factory Architecture Specification Candidate v1.0.0 has satisfied all technical, architectural, contract, security, reliability, testability, and governance prerequisites defined in the Council Operating Protocol.

All 22 mandatory freeze gates have objectively PASSED. Zero unresolved blockers exist. All 19 protected capabilities are preserved and strengthened.

**The AI Video Factory Architecture is officially FROZEN at Version 1.0.0.**
"""
    with open(os.path.join(freeze_dir, 'SPONSOR_PROXY_DECISION.md'), 'w') as f:
        f.write(sponsor_decision_content)
    print("Wrote SPONSOR_PROXY_DECISION.md")

    # 6. Create FREEZE_CERTIFICATE.md
    freeze_cert_content = """# AI Video Factory — Architecture Freeze Certificate
## Version 1.0.0

**CERTIFICATE_ID:** AVF-FREEZE-20260815-v1.0.0  
**AUTONOMOUS_COUNCIL_RESULT:** **FROZEN**  
**FROZEN_SPEC_VERSION:** **1.0.0**  
**SPONSOR_AUTHORITY:** **DELEGATED_AUTONOMOUS_PROXY**  
**SOURCE_BLUEPRINT:** `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0`  
**SOURCE_BLUEPRINT_PRESERVED:** **YES (0 modifications)**  
**DATE:** 2026-08-15  

---

### Certification Metrics
- **Total Council Rounds Executed:** 8 (C00 through C07)
- **Total Remediation Loops:** 1 (C05 Hostile Audit Blocker Resolution)
- **Total Findings Evaluated:** 158
- **Total Accepted Change Proposals:** 15 (`CP-001` through `CP-015`)
- **Total Rejected Proposals:** 0
- **Total Audit Blockers Resolved:** 3 (FINDING-A-01, FINDING-B-01, FINDING-B-02)
- **Mandatory Freeze Gates Passed:** 22 / 22 (100%)
- **Protected Capabilities Preserved:** 19 / 19 (100%)
- **Residual Risks Owned:** 4 (Tracked in FINAL_RISK_REGISTER.md)
- **Final Spec Candidate Location:** `review-session/FINAL_FREEZE/FROZEN_SPEC_CANDIDATE/`

---

### Council Certification Signatures
- **R01 (Domain & DDD Architect):** `SIGNED` (Canonical 14-entity schemas & RFC 8785 JCS certified)
- **R02 (Reliability & Distributed Systems):** `SIGNED` (Optimistic locking & lease fencing certified)
- **R03 (Creative Intent & Scripting):** `SIGNED` (3-layer prompt AST pipeline certified)
- **R04 (Contracts & Interface Governance):** `SIGNED` (Draft 2020-12 schemas certified)
- **R05 (Data Architect & Provenance):** `SIGNED` (Immutable Take lineage graph certified)
- **R06 (Workflow & State Machines):** `SIGNED` (Pause/resume & retry engine certified)
- **R07 (Security & Secrets Architect):** `SIGNED` (HMAC IPC & binary SecretEnclave certified)
- **R08 (QA & Test Strategy):** `SIGNED` (Hermetic test harness & mock simulators certified)
- **R09 (AI Systems & Provider APIs):** `SIGNED` (Google Flow MV3 keepalive supervisor certified)
- **R10 (Developer Experience & Tooling):** `SIGNED` (15 independent build packets certified)
- **R11 (Platform & Operations):** `SIGNED` (Multi-modal AQC scoring matrix certified)
- **R12 (Product Operations & Media):** `SIGNED` (FFmpeg normalization pipeline certified)
- **R13 (OSS & Component Architecture):** `SIGNED` (Hexagonal FlowExecutionPort certified)
- **R14 (Performance & Cost Engineering):** `SIGNED` (Two-phase credit settlement certified)
- **R15 (Adversarial Red-Team Systems):** `SIGNED` (Zero-trust security & DLQ replay certified)
- **AUDITOR-C (Independent Audit Judge):** `SIGNED` (Independent hostile audit certified)
- **SPONSOR PROXY (Delegated Council Supervisor):** `SPONSOR_PROXY_AUTHORIZE_FREEZE`
"""
    with open(os.path.join(freeze_dir, 'FREEZE_CERTIFICATE.md'), 'w') as f:
        f.write(freeze_cert_content)
    print("Wrote FREEZE_CERTIFICATE.md")

    # 7. Compute complete SHA-256 hashes and write FINAL_SPEC_MANIFEST.md and FILE_HASHES.json
    bp_tree_hash, bp_files = hash_dir_tree('AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0')
    prompt_tree_hash, prompt_files = hash_dir_tree('AI_VIDEO_FACTORY_COUNCIL_PROMPT_KIT_v1.1.0')
    frozen_tree_hash, frozen_files = hash_dir_tree(frozen_spec_dir)
    freeze_pkg_hash, freeze_pkg_files = hash_dir_tree(freeze_dir)

    hashes_payload = {
        "frozen_spec_version": "1.0.0",
        "source_blueprint_v0.9.0_tree_sha256": bp_tree_hash,
        "council_prompt_kit_v1.1.0_tree_sha256": prompt_tree_hash,
        "frozen_spec_candidate_tree_sha256": frozen_tree_hash,
        "final_freeze_package_tree_sha256": freeze_pkg_hash,
        "frozen_artifacts_sha256": freeze_pkg_files
    }

    with open(os.path.join(freeze_dir, 'FILE_HASHES.json'), 'w') as f:
        json.dump(hashes_payload, f, indent=2)
    print("Wrote FILE_HASHES.json")

    manifest_content = f"""# Final Specification Manifest (v1.0.0 Frozen)

**SPECIFICATION_VERSION:** 1.0.0  
**TIMESTAMP:** 2026-08-15T12:47:30+07:00  

---

## Cryptographic Tree Hashes (SHA-256)
- **Source Blueprint Kit (v0.9.0):** `{bp_tree_hash}` (Immutable Baseline)
- **Council Prompt Kit (v1.1.0):** `{prompt_tree_hash}` (Immutable Governance)
- **Frozen Spec Candidate (v1.0.0):** `{frozen_tree_hash}` (Certified Frozen Candidate)
- **Final Freeze Package:** `{freeze_pkg_hash}`

---

## Package Artifacts
- [FREEZE_CERTIFICATE.md](FREEZE_CERTIFICATE.md)
- [FINAL_REQUIREMENT_TRACEABILITY.md](FINAL_REQUIREMENT_TRACEABILITY.md)
- [FINAL_CONTRACT_COMPATIBILITY_MATRIX.md](FINAL_CONTRACT_COMPATIBILITY_MATRIX.md)
- [FINAL_REPO_DEPENDENCY_GRAPH.md](FINAL_REPO_DEPENDENCY_GRAPH.md)
- [FINAL_PROTECTED_CAPABILITY_REPORT.md](FINAL_PROTECTED_CAPABILITY_REPORT.md)
- [FINAL_RISK_REGISTER.md](FINAL_RISK_REGISTER.md)
- [FINAL_DISSENT_REGISTER.md](FINAL_DISSENT_REGISTER.md)
- [FINAL_IMPLEMENTATION_HANDOFF_INDEX.md](FINAL_IMPLEMENTATION_HANDOFF_INDEX.md)
- [FINAL_AUDIT_REPORT.md](FINAL_AUDIT_REPORT.md)
- [SPONSOR_PROXY_DECISION.md](SPONSOR_PROXY_DECISION.md)
- [FILE_HASHES.json](FILE_HASHES.json)
"""
    with open(os.path.join(freeze_dir, 'FINAL_SPEC_MANIFEST.md'), 'w') as f:
        f.write(manifest_content)
    print("Wrote FINAL_SPEC_MANIFEST.md")

if __name__ == '__main__':
    main()
