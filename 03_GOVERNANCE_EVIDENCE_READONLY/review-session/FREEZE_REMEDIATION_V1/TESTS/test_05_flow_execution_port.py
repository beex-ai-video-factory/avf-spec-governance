import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from schema_validator import SchemaValidator, ValidationError

def test_all_10_command_types_validate():
    cmd_path = os.path.join(os.path.dirname(__file__), '../REVISED_SPEC_CANDIDATE/02_contracts/browser-command.schema.json')
    res_path = os.path.join(os.path.dirname(__file__), '../REVISED_SPEC_CANDIDATE/02_contracts/flow-execution-result.schema.json')
    with open(cmd_path) as f: cmd_schema = json.load(f)
    with open(res_path) as f: res_schema = json.load(f)
    
    val_cmd = SchemaValidator(cmd_schema)
    val_res = SchemaValidator(res_schema)
    
    commands = [
        ('ENSURE_SESSION', {'account_alias': 'primary_test', 'headless': True}),
        ('OPEN_FLOW', {'flow_url': 'https://flow.google.com/test'}),
        ('CREATE_OR_SELECT_PROJECT', {'project_name': 'Project Alpha'}),
        ('ATTACH_ASSETS', {'assets': [{'asset_id': '11111111-1111-4111-8111-111111111111', 'storage_uri': 's3://bucket/ref.png', 'mime_type': 'image/png', 'role': 'CHARACTER'}]}),
        ('SET_GENERATION_OPTIONS', {'aspect_ratio': '16:9', 'resolution': '1080p', 'duration_seconds': 5}),
        ('SUBMIT_PROMPT', {'prompt_text': 'Cyberpunk scene', 'idempotency_key': 'a'*32, 'attempt_index': 1}),
        ('READ_GENERATION_STATE', {'provider_job_id': 'flow-123'}),
        ('DOWNLOAD_OUTPUT', {'provider_job_id': 'flow-123', 'destination_storage_uri': 's3://bucket/out.mp4'}),
        ('CAPTURE_DIAGNOSTIC', {'destination_diagnostic_uri': 's3://bucket/diag.zip'}),
        ('CANCEL', {'provider_job_id': 'flow-123', 'reason': 'User abort'})
    ]
    
    for cmd_type, params in commands:
        cmd_instance = {
            'command_id': '11111111-1111-4111-8111-111111111111',
            'session_id': 'sess-001',
            'timestamp_utc': '2026-08-15T12:00:00Z',
            'command_type': cmd_type,
            'params': params
        }
        val_cmd.validate(cmd_instance)
        
        res_instance = {
            'command_id': '11111111-1111-4111-8111-111111111111',
            'session_id': 'sess-001',
            'command_type': cmd_type,
            'status': 'SUCCESS',
            'timestamp_utc': '2026-08-15T12:00:01Z',
            'duration_ms': 500,
            'result': {'ack': True}
        }
        val_res.validate(res_instance)

if __name__ == '__main__':
    test_all_10_command_types_validate()
    print('test_05_flow_execution_port PASSED')
