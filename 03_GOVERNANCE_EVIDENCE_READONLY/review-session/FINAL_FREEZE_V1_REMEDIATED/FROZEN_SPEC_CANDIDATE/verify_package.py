#!/usr/bin/env python3
import os, sys, hashlib, json

def verify():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    hash_file = os.path.join(base_dir, 'CONTENT_HASHES.json')
    if not os.path.exists(hash_file):
        print('ERROR: CONTENT_HASHES.json not found')
        sys.exit(1)
    with open(hash_file) as f:
        expected_hashes = json.load(f)
    
    tree_lines = []
    failed = False
    for rel_p, exp_sha in sorted(expected_hashes.items()):
        fp = os.path.join(base_dir, rel_p)
        if not os.path.exists(fp):
            print(f'MISSING: {rel_p}')
            failed = True
            continue
        h = hashlib.sha256()
        with open(fp, 'rb') as fh:
            while chunk := fh.read(65536):
                h.update(chunk)
        act_sha = h.hexdigest()
        if act_sha != exp_sha:
            print(f'MISMATCH: {rel_p} (expected {exp_sha}, got {act_sha})')
            failed = True
        tree_lines.append(rel_p + '\t' + act_sha)
    
    if failed:
        print('VERIFICATION FAILED')
        sys.exit(1)
    
    tree_blob = '\n'.join(tree_lines) + '\n'
    computed_tree = hashlib.sha256(tree_blob.encode('utf-8')).hexdigest()
    print(f'Verifying AVF Specification Package at: {base_dir}')
    print(f'Computed CONTENT_TREE_SHA256: {computed_tree}')
    print(f'Total Normative Content Files Hashed: {len(expected_hashes)}')
    print('Package verification: OK')

if __name__ == '__main__':
    verify()
