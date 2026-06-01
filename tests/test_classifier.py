from filing_crosswalk.classifiers import classify_section


def test_classifies_material_weakness_first():
    text = "Management identified a material weakness in internal control over financial reporting."
    assert classify_section(text) == "internal_control"


def test_classifies_related_party():
    text = "The company purchased services from a related-party affiliate controlled by a director."
    assert classify_section(text) == "related_party_transaction"


def test_classifies_generic_boilerplate():
    text = (
        "The company may from time to time face uncertain conditions that could "
        "impact operations and financial results depending on market circumstances."
    )
    assert classify_section(text) == "generic_boilerplate"
