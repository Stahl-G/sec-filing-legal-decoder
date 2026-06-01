from sec_filing_legal_decoder.crosswalk.escalation_questions import generate_escalation_questions


def test_legal_proceedings_questions_include_core_roles():
    questions = generate_escalation_questions(
        "legal_proceedings", "ESCALATE", ["received_notice", "named_regulator"]
    )
    assert "Ask Legal" in questions
    assert "Ask Finance" in questions
    assert "Ask Auditor" in questions
    assert "Ask Management / Board" in questions
