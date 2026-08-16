# Research Report: RES-001 — RFC 8785 JSON Canonicalization Scheme (JCS)

**REQUEST_ID:** RES-001  
**SOURCE_FINDING:** F-R01-006  
**ASSIGNED_OWNERS:** R01 (Domain & DDD) & R05 (Data & Provenance)  
**STATUS:** RESOLVED (Incorporated into CP-011)  

---

## Executive Summary
This research investigates cross-language deterministic JSON serialization for cryptographic state hashing across TypeScript (Node.js), Python 3.11+, and Go 1.22+. 

Standard JSON stringification across different runtime platforms introduces subtle formatting divergences (whitespace, float representation, Unicode escaping, and dictionary key ordering). 

## Evaluation Results
1. **RFC 8785 (JSON Canonicalization Scheme - JCS)** guarantees identical byte-level serialization across all conforming implementations.
2. Verified libraries:
   - **TypeScript / Node.js:** `canonicalize` (v2.0.0)
   - **Python:** `canonicaljson` (v2.0.0)
   - **Go:** `github.com/gowebpki/jcs` (v1.0.1)
3. Conformance verification proved identical SHA-256 digests across all three languages for complex nested domain entities including arrays, floating point numbers, and UTF-8 strings.

## Council Recommendation
Formally adopt RFC 8785 JCS as the canonical serialization standard in CP-011. Incorporate cross-language hash conformance tests into R15 Integration Harness.
