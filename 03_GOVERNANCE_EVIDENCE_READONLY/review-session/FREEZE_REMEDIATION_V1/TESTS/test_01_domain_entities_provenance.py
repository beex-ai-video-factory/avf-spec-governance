import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from schema_validator import SchemaValidator, ValidationError

def load_schema():
    path = os.path.join(os.path.dirname(__file__), '../REVISED_SPEC_CANDIDATE/02_contracts/domain-entities.schema.json')
    with open(path, 'r') as f:
        return json.load(f)

def test_shot_version_creative_intent():
    schema = load_schema()
    val = SchemaValidator(schema)
    shot_version_def = schema.get('$defs', schema.get('definitions', {}))['ShotVersion']
    
    valid_shot_version = {
        'shot_version_id': '11111111-1111-4111-8111-111111111111',
        'shot_id': '22222222-2222-4222-8222-222222222222',
        'version_number': 1,
        'duration_ms': 5000,
        'action_description': 'A cinematic camera dolly forward revealing a futuristic cityscape at sunset.',
        'camera_motion': 'DOLLY_IN',
        'environment_settings': 'Cyberpunk sunset, neon reflections',
        'character_refs': ['33333333-3333-4333-8333-333333333333'],
        'style_refs': ['44444444-4444-4444-8444-444444444444'],
        'asset_refs': [],
        'constraints': ['No lens flare on main character face'],
        'continuity_refs': [],
        'created_at': '2026-08-15T12:00:00Z'
    }
    val.validate(valid_shot_version, shot_version_def)

def test_prompt_version_linkage():
    schema = load_schema()
    val = SchemaValidator(schema)
    prompt_def = schema.get('$defs', schema.get('definitions', {}))['PromptVersion']
    
    valid_prompt = {
        'prompt_version_id': '55555555-5555-4555-8555-555555555555',
        'shot_id': '22222222-2222-4222-8222-222222222222',
        'shot_version_id': '11111111-1111-4111-8111-111111111111',
        'version_number': 1,
        'target_provider': 'google-flow-veo2',
        'positive_prompt': 'Cinematic 8k footage of neon city sunset',
        'negative_prompt': 'blurry, distorted',
        'parameters': {'aspect_ratio': '16:9'},
        'ast_snapshot': {'root': 'scene_01'},
        'created_at': '2026-08-15T12:00:00Z'
    }
    val.validate(valid_prompt, prompt_def)

def test_generation_job_provenance():
    schema = load_schema()
    val = SchemaValidator(schema)
    job_def = schema.get('$defs', schema.get('definitions', {}))['GenerationJob']
    
    valid_job = {
        'job_id': '66666666-6666-4666-8666-666666666666',
        'project_id': '77777777-7777-4777-8777-777777777777',
        'shot_id': '22222222-2222-4222-8222-222222222222',
        'shot_version_id': '11111111-1111-4111-8111-111111111111',
        'prompt_version_id': '55555555-5555-4555-8555-555555555555',
        'provider_id': 'google-flow',
        'idempotency_key': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
        'status': 'RUNNING',
        'execution_stage': 'GENERATING',
        'attempt_index': 1,
        'max_attempts': 3,
        'provider_job_id': 'veo-job-987654',
        'flow_track': 'TRACK_A_EXTENSION',
        'lease_token': '88888888-8888-4888-8888-888888888888',
        'lease_expires_at': '2026-08-15T13:30:00Z',
        'estimated_cost_credits': 10.0,
        'actual_cost_credits': 0.0,
        'requested_at': '2026-08-15T12:00:00Z',
        'submitted_at': '2026-08-15T12:01:00Z',
        'entity_version': 1
    }
    val.validate(valid_job, job_def)

def test_invalid_uuid_rejected():
    schema = load_schema()
    val = SchemaValidator(schema)
    uuid_def = schema.get('$defs', schema.get('definitions', {}))['UUID']
    try:
        val.validate('not-a-valid-uuid-format-12345', uuid_def)
        assert False, 'Should have raised ValidationError'
    except ValidationError:
        pass

if __name__ == '__main__':
    test_shot_version_creative_intent()
    test_prompt_version_linkage()
    test_generation_job_provenance()
    test_invalid_uuid_rejected()
    print('test_01_domain_entities_provenance PASSED')
