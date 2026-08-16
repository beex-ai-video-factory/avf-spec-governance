import hashlib, json

def compute_idempotency_key(shot_version_id, prompt_version_id, provider_id, attempt_index, parameters):
    param_str = json.dumps(parameters, sort_keys=True)
    raw = f"{shot_version_id}:{prompt_version_id}:{provider_id}:{attempt_index}:{param_str}"
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()

def test_idempotency_determinism():
    k1 = compute_idempotency_key('sv-1', 'pv-1', 'google-flow', 1, {'ratio': '16:9'})
    k2 = compute_idempotency_key('sv-1', 'pv-1', 'google-flow', 1, {'ratio': '16:9'})
    assert k1 == k2, 'Idempotency keys must be deterministic!'
    
    # Next attempt produces distinct key
    k3 = compute_idempotency_key('sv-1', 'pv-1', 'google-flow', 2, {'ratio': '16:9'})
    assert k1 != k3, 'Subsequent attempts must produce distinct idempotency keys!'

if __name__ == '__main__':
    test_idempotency_determinism()
    print('test_06_idempotency_attempt_semantics PASSED')
