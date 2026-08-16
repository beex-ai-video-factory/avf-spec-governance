# RULE: Frozen Baseline Guardian
# Trigger: Always On

## Objective
Preserve the absolute immutability of the frozen AI Video Factory v1.0.0 specification baseline and all historical audit evidence.

## Mandatory Directives
1. **Read-Only Baseline:** You may read from `01_FROZEN_RELEASE/`, `02_SOURCE_KITS_READONLY/`, `03_GOVERNANCE_EVIDENCE_READONLY/`, and `90_ARCHIVE_READONLY/`, but you must **NEVER** edit, delete, overwrite, or move files within these directories.
2. **Defect Handling via Change Requests:** If you discover a bug, contradiction, or gap in the frozen baseline during implementation, do **NOT** edit the frozen specification. Instead, create a formal **Change Request (CR)** in `05_IMPLEMENTATION/change-requests/` using the approved template and halt affected implementation paths.
3. **No Baseline Contamination:** Do not write modified spec files, generated schemas, or implementation artifacts back into `01_FROZEN_RELEASE/` or any other protected directory.
4. **All Writable Work in 05_IMPLEMENTATION:** All implementation code, configuration, tests, decision records, and temporary builds must live strictly within `05_IMPLEMENTATION/` (or `04_TOOLING/` for developer scripts).
