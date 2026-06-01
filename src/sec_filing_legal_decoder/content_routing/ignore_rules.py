"""Rules for filing admin text that should not produce risk cards."""

from __future__ import annotations

import re


ADMIN_PATTERNS: tuple[str, ...] = (
    r"^table of contents$",
    r"^index to .*financial statements?$",
    r"^exhibit index$",
    r"^signatures?$",
    r"^cover page$",
    r"pursuant to the requirements of the securities exchange act",
    r"the registrant has duly caused this report to be signed",
    r"securities registered pursuant to section",
    r"indicate by check mark",
    r"commission file number",
    r"large accelerated filer",
    r"transition report pursuant to",
    r"exact name of registrant as specified",
    r"address of principal executive offices",
    r"table of contents item\s+\d",
)


def is_filing_admin(text: str) -> bool:
    """Return True when a paragraph is filing admin chrome."""

    lowered = " ".join(text.lower().split())
    if len(lowered.split()) <= 14 and re.search(r"^(item\s+\d+|part\s+[ivx]+)\b", lowered):
        return True
    return any(re.search(pattern, lowered, flags=re.IGNORECASE) for pattern in ADMIN_PATTERNS)
