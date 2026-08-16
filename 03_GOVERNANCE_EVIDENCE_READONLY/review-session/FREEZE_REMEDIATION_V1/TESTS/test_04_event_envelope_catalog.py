import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from schema_validator import SchemaValidator, ValidationError

def test_event_envelope():
    path = os.path.join(os.path.dirname(__file__), '../REVISED_SPEC_CANDIDATE/02_contracts/event-envelope.schema.json')
    with open(path, 'r') as f:
        schema = json.load(f)
    val = SchemaValidator(schema)
    
    sample_event = {
        'event_id': '11111111-1111-4111-8111-111111111111',
        'event_type': 'avf.generation.job_completed',
        'aggregate_id': '22222222-2222-4222-8222-222222222222',
        'aggregate_version': 2,
        'timestamp_utc': '2026-08-15T12:05:00Z',
        'correlation_id': '33333333-3333-4333-8333-333333333333',
        'trace_id': '4bf92f3577b34da6a3ce929d0e0e4736',
        'span_id': '00f067aa0ba902b7',
        'workflow_run_id': 'wf-run-987654',
        'schema_version': '1.0.0',
        'payload': {
            'job_id': '22222222-2222-4222-8222-222222222222',
            'take_id': '44444444-4444-4444-8444-444444444444',
            'status': 'COMPLETED'
        }
    }
    val.validate(sample_event)

def test_event_catalog_naming_regex():
    catalog_event_types = [
        'avf.project.created',
        'avf.project.updated',
        'avf.shot.version_created',
        'avf.prompt.version_created',
        'avf.generation.job_queued',
        'avf.generation.job_reserved',
        'avf.generation.job_submitted',
        'avf.generation.job_progress',
        'avf.generation.job_completed',
        'avf.generation.job_failed',
        'avf.generation.job_cancelled',
        'avf.generation.job_reconciled',
        'avf.take.registered',
        'avf.qc.completed',
        'avf.media.quarantined'
    ]
    pattern = re.compile(r'^avf\.[a-z0-9_-]+(\.[a-z0-9_-]+)+$')
    for event_type in catalog_event_types:
        assert pattern.match(event_type), f'Event type {event_type} failed regex match!'

if __name__ == '__main__':
    test_event_envelope()
    test_event_catalog_naming_regex()
    print('test_04_event_envelope_catalog PASSED')
