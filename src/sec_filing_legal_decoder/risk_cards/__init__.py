"""Risk-card generation for v0.3 legal-to-finance workflows."""

from .risk_domain_classifier import classify_risk_domains


def generate_risk_card_report(document):
    """Generate a risk-card report without eager imports that create routing cycles."""

    from .card_generator import generate_risk_card_report as _generate_risk_card_report

    return _generate_risk_card_report(document)


__all__ = ["classify_risk_domains", "generate_risk_card_report"]
