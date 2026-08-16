# Controversy Resolution Report: CONT-001 — Track A vs Track B Runtime Isolation Boundary

**CONTROVERSY_ID:** CONT-001  
**SOURCE_FINDINGS:** F-R13-001, F-R06-001, F-R02-004  
**COMPETING PARTIES:** Panel B (Runtime Isolationists) vs Panel A/C (Velocity & Simplicity)  
**STATUS:** RESOLVED via CP-005 Pure Hexagonal Port Isolation  

---

## Architectural Synthesis
The Council evaluated the competing proposals:
- **View A (Strict Subprocess / gRPC Isolation):** FlowKit runs strictly out-of-process.
- **View B (In-Process Module with Schema Boundary):** FlowKit imported as a TypeScript library inside `avf-flow-adapter`.

## Resolved Design Decision (CP-005)
The Council resolved this debate by adopting **Hexagonal Port Isolation (`FlowExecutionPort`)**:
1. `R08_GOOGLE_FLOW_ADAPTER` exposes a clean, provider-agnostic `FlowExecutionPort` contract.
2. Upstream workflow engine (R06) and Core State (R02) have zero knowledge of whether Track A or Track B is executing.
3. Track B (`avf-flowkit-bridge`) is packaged as an independent service communicating via gRPC/Unix socket, satisfying Panel B's dependency isolation requirements while presenting a standard provider interface.
4. Track A (`avf-browser-worker`) operates as an independent CDP worker.
