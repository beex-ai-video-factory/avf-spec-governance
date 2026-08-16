# FINAL PACKAGE HASH CANONICALIZATION
## AI Video Factory — Last Packaging Integrity Fix

Run as `/goal` in the SAME Gemini 3.7 Flash High remediation conversation.

Do not modify normative architecture or Council decisions.
Do not rerun C02R/C04R/C05R unless this packaging-only task discovers a semantic or governance defect.

The current targeted-patch log contains a Stage-D archive hash ordering defect:

1. a ZIP was built;
2. its digest was written into `FINAL_SPEC_MANIFEST.md`;
3. the ZIP was rebuilt, changing its byte stream;
4. a new digest was computed;
5. the external `DISTRIBUTABLE_ZIP_SHA256` file was updated without rebuilding a manifest that can truthfully describe that same archive.

A ZIP cannot normally contain its own exact byte-stream SHA-256 inside a file and remain the same ZIP after that file changes.

## Required canonical model

Use two distinct integrity concepts.

### A. Internal package content integrity
Inside `FINAL_FREEZE_V1_REMEDIATED/` and inside the distributable archive, record only:
- VERSION
- CONTENT_HASHES.json
- CONTENT_TREE_SHA256
- deterministic content hashing algorithm
- manifest of included files

These values may be embedded inside the archive because they hash normative content using explicitly documented exclusions.

### B. Distributable archive byte-stream integrity
The exact SHA-256 of the final ZIP MUST be stored OUTSIDE the ZIP as a sidecar:

`AVF_FINAL_FREEZE_v1.0.0_REMEDIATED.zip.sha256`

Do not attempt to embed the final ZIP's own SHA-256 inside the ZIP.

`FINAL_SPEC_MANIFEST.md` inside the archive must say:

`DISTRIBUTABLE_ZIP_SHA256 = EXTERNAL_SIDECAR`

and identify the expected sidecar filename, not a digest value.

An optional manifest OUTSIDE the ZIP may record the exact digest.

## Procedure

1. Finalize all files under:
   `review-session/FINAL_FREEZE_V1_REMEDIATED/`

2. Ensure `FINAL_SPEC_MANIFEST.md` contains:
   - content tree digest;
   - content hashing algorithm;
   - archive filename;
   - sidecar filename;
   - statement that archive byte-stream digest is external to avoid self-reference.

3. Remove any embedded `DISTRIBUTABLE_ZIP_SHA256` file from the directory that will be archived, unless it is explicitly a content-tree digest rather than archive digest.

4. Build `AVF_FINAL_FREEZE_v1.0.0_REMEDIATED.zip` exactly ONCE after final content is stable.

5. Do not alter or rebuild that ZIP afterward.

6. Compute:
   `shasum -a 256 AVF_FINAL_FREEZE_v1.0.0_REMEDIATED.zip`

7. Write exactly:
   `<sha256>  AVF_FINAL_FREEZE_v1.0.0_REMEDIATED.zip`
   to:
   `AVF_FINAL_FREEZE_v1.0.0_REMEDIATED.zip.sha256`

8. Independently verify:
   - recompute ZIP SHA-256;
   - compare with sidecar;
   - verify all internal content hashes;
   - verify CONTENT_TREE_SHA256.

9. Verify that extracting the ZIP does not claim an embedded archive digest different from the sidecar.

## Required final output

PACKAGE_HASH_CANONICALIZATION = PASS | FAIL
ZIP_BUILT_ONCE_AFTER_FINAL_CONTENT = YES | NO
EMBEDDED_SELF_REFERENTIAL_ZIP_DIGEST = NO | YES
CONTENT_TREE_HASH_VERIFIED = YES | NO
ZIP_SIDECAR_HASH_VERIFIED = YES | NO
ARCHIVE_FILENAME
SIDECAR_FILENAME
FINAL_DISTRIBUTABLE_ZIP_SHA256
NEXT_REQUIRED_ACTION = FINAL_EXTERNAL_CROSS_FAMILY_AUDIT | REMEDIATION_REQUIRED

STOP.
Do not begin implementation.
