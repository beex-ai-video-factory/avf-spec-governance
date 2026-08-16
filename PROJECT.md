# AI VIDEO FACTORY

**CURRENT PHASE:**  
`IMPLEMENTATION`

**FROZEN BASELINE:**  
`v1.0.0 — VERIFIED_IMPLEMENTATION_BASELINE`

**READ-ONLY:**  
- `01_FROZEN_RELEASE`
- `02_SOURCE_KITS_READONLY`
- `03_GOVERNANCE_EVIDENCE_READONLY`
- `90_ARCHIVE_READONLY`

**WRITABLE:**  
- `05_IMPLEMENTATION`
- `04_TOOLING`
- `00_PROJECT_ADMIN`
- `99_TEMP`
- `.agents`

**RULE:**  
Never edit frozen baseline.  
Spec defects become Change Requests.

**IMPLEMENTATION START GATE:**  
`R01 Contracts` (JSON Schemas, TypeScript types, validation test fixtures).

---

## 1. Quick Navigation & Essential Links

- **Baseline Lockfile:** [BASELINE.lock.json](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/BASELINE.lock.json)
- **Implementation Baseline:** [05_IMPLEMENTATION/IMPLEMENTATION_BASELINE.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/IMPLEMENTATION_BASELINE.md)
- **Repository Registry (R01–R15):** [05_IMPLEMENTATION/repo-registry.yaml](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/repo-registry.yaml)
- **Dependency Gates:** [05_IMPLEMENTATION/dependency-gates.yaml](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/dependency-gates.yaml)
- **Development Environment:** [05_IMPLEMENTATION/environment/](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/environment/)
- **Change Request Process:** [05_IMPLEMENTATION/change-requests/README.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/change-requests/README.md)
- **Implementation Decisions:** [05_IMPLEMENTATION/decisions/README.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/decisions/README.md)
- **R01 Pre-Implementation Hardening:** [05_IMPLEMENTATION/R01_PREIMPLEMENTATION_HARDENING.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/R01_PREIMPLEMENTATION_HARDENING.md)
- **Pre-Implementation Certificate:** [00_PROJECT_ADMIN/PREIMPLEMENTATION_CERTIFICATE.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/00_PROJECT_ADMIN/PREIMPLEMENTATION_CERTIFICATE.md)
- **Workspace Normalization Map:** [00_PROJECT_ADMIN/WORKSPACE_MAP.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/00_PROJECT_ADMIN/WORKSPACE_MAP.md)

---

## 2. Directory Architecture

```text
AVF_SPEC_REVIEW/
├── PROJECT.md                                # Mandatory first-read entrypoint
├── BASELINE.lock.json                        # Cryptographic baseline lockfile
├── .gitignore                                # Git ignore policy
├── .editorconfig                             # Formatting standards
├── .agents/                                  # Agent rules, skills, hooks
│   ├── rules/                                # 5 mandatory guardian rules
│   ├── skills/                               # 10 specialized AVF skills
│   ├── hooks.json                            # Pre/post tool safety hooks
│   └── scripts/                              # Guard scripts
├── 00_PROJECT_ADMIN/                         # Governance certificates, cleanup inventories
├── 01_FROZEN_RELEASE/                        # [READ-ONLY] Authoritative v1.0.0 release & sidecar
├── 02_SOURCE_KITS_READONLY/                  # [READ-ONLY] Input specification & council kits
├── 03_GOVERNANCE_EVIDENCE_READONLY/          # [READ-ONLY] Historical review session & forensic audits
├── 04_TOOLING/                               # Developer validation scripts & generators
├── 05_IMPLEMENTATION/                        # [WRITABLE] Implementation workspace for R01-R15
│   ├── repos/                                # 15 modular polyrepo targets
│   ├── environment/                          # Docker compose, env, doctor
│   ├── change-requests/                      # Formal spec defect tickets
│   └── decisions/                            # Implementation Decision Records (IDRs)
├── 90_ARCHIVE_READONLY/                      # [READ-ONLY] Superseded release archives
└── 99_TEMP/                                  # Temporary developer scratch space
```

---

## 3. Getting Started for Implementation Agents

1. Execute the pre-implementation doctor to confirm integrity:
   ```bash
   04_TOOLING/validation/preimplementation_doctor.sh
   ```
2. Review the R01 Contracts blueprint and hardening register:
   - [01_FROZEN_RELEASE/v1.0.0/03_repo_blueprints/R01_CONTRACTS.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R01_CONTRACTS.md)
   - [05_IMPLEMENTATION/R01_PREIMPLEMENTATION_HARDENING.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/R01_PREIMPLEMENTATION_HARDENING.md)
3. Implement R01 Contracts in `05_IMPLEMENTATION/repos/R01_contracts/`.
