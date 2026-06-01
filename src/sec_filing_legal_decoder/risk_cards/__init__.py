"""Risk-card generation for v0.4 source-only legal-to-finance workflows."""

from .risk_domain_classifier import classify_risk_domains


def generate_risk_card_report(document, review_mode="source-only", issuer_profile="general"):
    """Generate a risk-card report without eager imports that create routing cycles."""

    from .card_generator import generate_risk_card_report as _generate_risk_card_report

    return _generate_risk_card_report(
        document,
        review_mode=review_mode,
        issuer_profile=issuer_profile,
    )


__all__ = ["classify_risk_domains", "generate_risk_card_report"]
