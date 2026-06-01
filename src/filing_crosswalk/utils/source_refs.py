"""Source reference helpers."""

from __future__ import annotations

from pathlib import Path


def source_ref(source_path: str, paragraph_id: int) -> str:
    """Return a stable paragraph source reference."""

    name = Path(source_path).name or "input"
    return f"{name}#p{paragraph_id}"
