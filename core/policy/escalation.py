ESCALATE_INTENT_SCORE = 0.55


def should_escalate(
    intent_score: float, conflicts: bool, risk_flags: list[str]
) -> bool:
    if conflicts or risk_flags:
        return True
    return intent_score < ESCALATE_INTENT_SCORE
