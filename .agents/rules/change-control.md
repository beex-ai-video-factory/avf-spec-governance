# RULE: Change Control & Ambiguity Classification
# Trigger: Always On

## Objective
Establish a formal mechanism for classifying ambiguities, recording technical decisions, and managing frozen baseline defects during implementation.

## Mandatory Directives
1. **Classify Every Ambiguity Before Proceeding:** When encountering an unspecified scenario, the implementing agent must categorize the issue into one of three classifications:
   - **Classification A: Implementation Detail:** If the frozen architecture/ADRs are intentionally silent and multiple reasonable designs exist, create an **Implementation Decision Record (IDR)** in `05_IMPLEMENTATION/decisions/` documenting the rationale and trade-offs. IDRs may NOT contradict any frozen ADR or contract.
   - **Classification B: Frozen Architecture / Contract Defect:** If the frozen specification contains a logical contradiction, missing required field, or broken contract, create a formal **Change Request (CR)** in `05_IMPLEMENTATION/change-requests/` and **HALT** implementation on the affected component until human triage/approval.
   - **Classification C: Empirical Provider Unknown:** If an external behavior (e.g., Google Flow UI layout, undocumented header) cannot be deduced, implement a targeted benchmark/spike under `04_TOOLING/bootstrap/` or a mock adapter with configurable parameters.
2. **Never Silently Rewrite:** Agents are strictly forbidden from modifying specifications, schema files, or contracts in-place without a documented CR or IDR.
