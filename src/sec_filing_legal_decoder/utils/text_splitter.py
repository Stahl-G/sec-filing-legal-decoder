"""Paragraph splitting helpers for pre-parsed filing text."""

from __future__ import annotations

import re


def split_paragraphs(content: str) -> list[str]:
    """Split Markdown or plain text into analysis-ready paragraphs."""

    normalized = content.replace("\r\n", "\n").replace("\r", "\n")
    blocks = re.split(r"\n\s*\n+", normalized)
    paragraphs: list[str] = []
    for block in blocks:
        cleaned = _clean_block(block)
        if len(cleaned.split()) >= 8:
            paragraphs.append(cleaned)
    return paragraphs


def _clean_block(block: str) -> str:
    lines = []
    for line in block.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        stripped = re.sub(r"^#{1,6}\s+", "", stripped)
        stripped = re.sub(r"^[-*]\s+", "", stripped)
        lines.append(stripped)
    return " ".join(lines).strip()
