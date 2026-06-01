"""Rule-based classification and triage."""

from .boilerplate_material_triage import TriageResult, triage_paragraph
from .legal_section_classifier import classify_section

__all__ = ["TriageResult", "classify_section", "triage_paragraph"]
