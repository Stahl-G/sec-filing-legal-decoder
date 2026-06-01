from sec_filing_legal_decoder.classifiers import triage_paragraph


def test_generic_boilerplate_skips_or_skims():
    result = triage_paragraph(
        "The company may from time to time face claims that could adversely affect results.",
        "legal_proceedings",
    )
    assert result.boilerplate_or_material == "likely_boilerplate"
    assert result.reading_decision == "SKIM"


def test_actual_subpoena_escalates():
    result = triage_paragraph(
        "The company received a subpoena from the SEC and has accrued a liability of $4.2 million.",
        "legal_proceedings",
    )
    assert result.boilerplate_or_material == "potentially_material"
    assert result.reading_decision == "ESCALATE"
    assert "received_notice" in result.signals


def test_material_weakness_escalates():
    result = triage_paragraph(
        "Management concluded controls were ineffective due to a material weakness.",
        "internal_control",
    )
    assert result.reading_decision == "ESCALATE"
