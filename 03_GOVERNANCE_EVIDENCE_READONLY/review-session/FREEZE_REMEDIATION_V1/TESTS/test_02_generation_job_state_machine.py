VALID_TRANSITIONS = {
    'QUEUED': ['RESERVED', 'CANCELLED', 'FAILED'],
    'RESERVED': ['RUNNING', 'CANCELLED', 'FAILED'],
    'RUNNING': ['COMPLETED', 'FAILED', 'CANCELLED', 'RECONCILED'],
    'COMPLETED': [],
    'FAILED': [],
    'CANCELLED': [],
    'RECONCILED': []
}

STAGE_TO_STATUS = {
    'WAITING_FOR_ASSETS': 'QUEUED',
    'PROMPT_READY': 'QUEUED',
    'BUDGET_RESERVED': 'RESERVED',
    'SUBMITTING': 'RUNNING',
    'SUBMITTED': 'RUNNING',
    'GENERATING': 'RUNNING',
    'DOWNLOADING': 'RUNNING',
    'DOWNLOADED': 'RUNNING',
    'QC_RUNNING': 'RUNNING',
    'APPROVED': 'COMPLETED',
    'EXECUTION_FAILED': 'FAILED',
    'QC_REJECTED': 'FAILED',
    'TIMEOUT': 'FAILED',
    'ABORTED_BY_USER': 'CANCELLED',
    'ABORTED_BY_SYSTEM': 'CANCELLED',
    'RECONCILED_SUCCESS': 'RECONCILED',
    'RECONCILED_TERMINAL': 'RECONCILED'
}

def validate_transition(current_status, next_status):
    if next_status not in VALID_TRANSITIONS.get(current_status, []):
        raise ValueError(f'Invalid state transition: {current_status} -> {next_status}')
    return True

def test_valid_transitions():
    assert validate_transition('QUEUED', 'RESERVED')
    assert validate_transition('RESERVED', 'RUNNING')
    assert validate_transition('RUNNING', 'COMPLETED')
    assert validate_transition('RUNNING', 'RECONCILED')

def test_invalid_transitions_rejected():
    try:
        validate_transition('QUEUED', 'COMPLETED')
        assert False, 'Should have failed'
    except ValueError:
        pass
    try:
        validate_transition('COMPLETED', 'RUNNING')
        assert False, 'Should have failed'
    except ValueError:
        pass

def test_stage_mapping_integrity():
    for stage, status in STAGE_TO_STATUS.items():
        assert status in VALID_TRANSITIONS

if __name__ == '__main__':
    test_valid_transitions()
    test_invalid_transitions_rejected()
    test_stage_mapping_integrity()
    print('test_02_generation_job_state_machine PASSED')
