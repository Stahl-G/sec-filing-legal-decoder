#!/usr/bin/env python3
"""Validate a risk-card output directory."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_FILES = [
    "legal-risk-review.md",
    "legal-risk-cards.md",
    "legal-risk-cards.json",
    "evidence-audit.md",
    "escalation-questions.md",
    "management-follow-up.md",
]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate sec-filing-legal-decoder output files.")
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args(argv)

    failures: list[str] = []
    if not args.output_dir.exists() or not args.output_dir.is_dir():
        failures.append(f"output directory does not exist: {args.output_dir}")
    for name in REQUIRED_FILES:
        path = args.output_dir / name
        if not path.exists():
            failures.append(f"missing {name}")
        elif path.stat().st_size == 0:
            failures.append(f"empty {name}")

    json_path = args.output_dir / "legal-risk-cards.json"
    if json_path.exists():
        try:
            payload = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"invalid legal-risk-cards.json: {exc}")
        else:
            for key in ["review_mode", "external_enrichment", "issuer_profile", "risk_cards"]:
                if key not in payload:
                    failures.append(f"legal-risk-cards.json missing {key}")

    if failures:
        print("Output validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Output validation passed: {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
