"""Read an existing finance or earnings analysis for overlay review."""

from __future__ import annotations

from pathlib import Path


def read_analysis(path: Path) -> str:
    """Read an existing analysis file as text."""

    if not path.exists():
        raise FileNotFoundError(f"Analysis file does not exist: {path}")
    return path.read_text(encoding="utf-8", errors="replace")
