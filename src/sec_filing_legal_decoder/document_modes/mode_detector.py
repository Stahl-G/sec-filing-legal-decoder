"""Detect high-level filing mode before risk-card routing."""

from __future__ import annotations

import re
from pathlib import Path

from sec_filing_legal_decoder.schemas import ParsedDocument


FORM_PATTERNS: tuple[tuple[str, str], ...] = (
    ("6-K", r"\bform\s+6-k\b|\b6-k\b"),
    ("10-K", r"\bform\s+10-k\b|\b10-k\b"),
    ("10-Q", r"\bform\s+10-q\b|\b10-q\b"),
    ("20-F", r"\bform\s+20-f\b|\b20-f\b"),
    ("40-F", r"\bform\s+40-f\b|\b40-f\b"),
)


def detect_document_mode(document: ParsedDocument) -> tuple[str, str]:
    """Return ``(form_type, mode)`` for a parsed filing.

    The detector is intentionally conservative. It only labels an earnings
    release 6-K when the text resembles an exhibit results announcement.
    """

    title = document.title or ""
    filename = Path(document.source_path).name
    sample = " ".join(document.content.split()[:2500])
    text = f"{title} {filename} {sample}".lower()
    form_type = _detect_form_type(text)

    if form_type == "20-F":
        return form_type, "annual_report_20f"
    if form_type == "40-F":
        return form_type, "annual_report_40f"
    if form_type == "10-K":
        return form_type, "annual_report_10k"
    if form_type == "10-Q":
        return form_type, "quarterly_10q"
    if form_type == "6-K":
        if _looks_like_earnings_release(text):
            return form_type, "earnings_release_6k"
        return form_type, "foreign_issuer_6k"
    return "unknown", "unknown"


def _detect_form_type(text: str) -> str:
    primary = _first_form_heading(text)
    if primary != "unknown":
        return primary
    for form_type, pattern in FORM_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            return form_type
    return "unknown"


def _first_form_heading(text: str) -> str:
    candidates: list[tuple[int, str]] = []
    for form_type in ["6-K", "10-K", "10-Q", "20-F", "40-F"]:
        form_pattern = re.escape(form_type).replace(r"\-", r"[-\s]?")
        for pattern in (rf"\bform\s+{form_pattern}\b", rf"\b{form_pattern}\b"):
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                candidates.append((match.start(), form_type))
                break
    if not candidates:
        return "unknown"
    return sorted(candidates)[0][1]


def _looks_like_earnings_release(text: str) -> bool:
    exhibit_signal = re.search(r"\bexhibit\s+99\.?1\b", text) is not None
    result_signal = re.search(
        r"\b(reports?|announces?)\b.{0,80}\b(results?|quarter|fiscal|earnings)\b",
        text,
    ) is not None
    press_release_signal = "press release" in text and (
        "quarter" in text or "financial results" in text
    )
    return bool((exhibit_signal and result_signal) or press_release_signal)
