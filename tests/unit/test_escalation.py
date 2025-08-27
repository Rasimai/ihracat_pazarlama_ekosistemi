from core.policy.escalation import should_escalate


def test_escalate_on_conflict():
    assert should_escalate(0.9, conflicts=True, risk_flags=[])


def test_score_threshold():
    assert should_escalate(0.40, conflicts=False, risk_flags=[])
    assert not should_escalate(0.80, conflicts=False, risk_flags=[])
