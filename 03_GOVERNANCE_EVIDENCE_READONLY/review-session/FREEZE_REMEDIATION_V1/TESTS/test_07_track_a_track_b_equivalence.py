import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from schema_validator import SchemaValidator, ValidationError

class FakeTrackABrowserWorker:
    def execute(self, command):
        return {
            'command_id': command['command_id'],
            'session_id': command['session_id'],
            'command_type': command['command_type'],
            'status': 'SUCCESS',
            'timestamp_utc': '2026-08-15T12:00:01Z',
            'duration_ms': 350,
            'result': {'track': 'TRACK_A_EXTENSION', 'provider_job_id': 'flow-ext-100', 'state': 'SUBMITTED'}
        }

class FakeTrackBFlowKitBridge:
    def execute(self, command):
        return {
            'command_id': command['command_id'],
            'session_id': command['session_id'],
            'command_type': command['command_type'],
            'status': 'SUCCESS',
            'timestamp_utc': '2026-08-15T12:00:01Z',
            'duration_ms': 120,
            'result': {'track': 'TRACK_B_FLOWKIT', 'provider_job_id': 'flow-fk-200', 'state': 'SUBMITTED'}
        }

def test_port_equivalence():
    res_path = os.path.join(os.path.dirname(__file__), '../REVISED_SPEC_CANDIDATE/02_contracts/flow-execution-result.schema.json')
    with open(res_path) as f:
        res_schema = json.load(f)
    val = SchemaValidator(res_schema)
    
    command = {
        'command_id': '11111111-1111-4111-8111-111111111111',
        'session_id': 'sess-shared',
        'timestamp_utc': '2026-08-15T12:00:00Z',
        'command_type': 'SUBMIT_PROMPT',
        'params': {
            'prompt_text': 'Equivalence test prompt',
            'idempotency_key': 'a'*32,
            'attempt_index': 1
        }
    }
    
    worker_a = FakeTrackABrowserWorker()
    worker_b = FakeTrackBFlowKitBridge()
    
    res_a = worker_a.execute(command)
    res_b = worker_b.execute(command)
    
    val.validate(res_a)
    val.validate(res_b)
    
    assert res_a['status'] == 'SUCCESS'
    assert res_b['status'] == 'SUCCESS'
    assert res_a['command_type'] == res_b['command_type'] == 'SUBMIT_PROMPT'

if __name__ == '__main__':
    test_port_equivalence()
    print('test_07_track_a_track_b_equivalence PASSED')
