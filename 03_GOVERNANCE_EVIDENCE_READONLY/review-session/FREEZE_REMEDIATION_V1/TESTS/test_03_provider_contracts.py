import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from schema_validator import SchemaValidator, ValidationError

def test_provider_request_schema():
    path = os.path.join(os.path.dirname(__file__), '../REVISED_SPEC_CANDIDATE/02_contracts/provider-request.schema.json')
    with open(path, 'r') as f:
        schema = json.load(f)
    val = SchemaValidator(schema)
    
    valid_request = {
        'request_id': '11111111-1111-4111-8111-111111111111',
        'job_id': '22222222-2222-4222-8222-222222222222',
        'prompt_version_id': '33333333-3333-4333-8333-333333333333',
        'provider_id': 'google-flow',
        'positive_prompt': 'A breathtaking drone shot of mountains at dawn.',
        'negative_prompt': 'low quality, artifacts',
        'aspect_ratio': '16:9',
        'duration_seconds': 5,
        'idempotency_key': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
        'attempt_index': 1,
        'timestamp_utc': '2026-08-15T12:00:00Z'
    }
    val.validate(valid_request)

def test_provider_result_success_and_error():
    path = os.path.join(os.path.dirname(__file__), '../REVISED_SPEC_CANDIDATE/02_contracts/provider-result.schema.json')
    with open(path, 'r') as f:
        schema = json.load(f)
    val = SchemaValidator(schema)
    
    success_result = {
        'request_id': '11111111-1111-4111-8111-111111111111',
        'job_id': '22222222-2222-4222-8222-222222222222',
        'provider_id': 'google-flow',
        'provider_job_id': 'flow-987654',
        'status': 'SUCCESS',
        'generation_status': 'SUCCEEDED',
        'progress_percent': 100.0,
        'output_uri': 's3://avf-renders/project-1/take-1.mp4',
        'output_metadata': {
            'mime_type': 'video/mp4',
            'byte_size': 15728640,
            'checksum_sha256': 'a' * 64,
            'duration_ms': 5000
        },
        'cost_credits_used': 8.5,
        'timestamp_utc': '2026-08-15T12:05:00Z'
    }
    val.validate(success_result)
    
    error_result = {
        'request_id': '11111111-1111-4111-8111-111111111111',
        'job_id': '22222222-2222-4222-8222-222222222222',
        'provider_id': 'google-flow',
        'status': 'FAILED',
        'generation_status': 'FAILED',
        'error': {
            'code': 'SECURITY_CHALLENGE',
            'message': 'Google Flow presented a CAPTCHA challenge.',
            'retry_category': 'POLICY_BLOCKED',
            'suggested_backoff_ms': 0
        },
        'timestamp_utc': '2026-08-15T12:01:00Z'
    }
    val.validate(error_result)

if __name__ == '__main__':
    test_provider_request_schema()
    test_provider_result_success_and_error()
    print('test_03_provider_contracts PASSED')
