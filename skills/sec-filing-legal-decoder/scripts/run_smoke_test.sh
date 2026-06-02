#!/usr/bin/env bash
set -euo pipefail

export PYTHONPATH="${PYTHONPATH:-}:src"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN=python3
else
  PYTHON_BIN=python
fi

if [[ -n "${VIRTUAL_ENV:-}" ]]; then
  "${PYTHON_BIN}" -m pip install -e ".[dev]"
else
  echo "No active virtual environment; using PYTHONPATH=src smoke-test fallback."
fi
"${PYTHON_BIN}" skills/sec-filing-legal-decoder/scripts/validate_skill_structure.py

if command -v sec-filing-legal-decoder >/dev/null 2>&1; then
  CLI=(sec-filing-legal-decoder)
else
  CLI=("${PYTHON_BIN}" -m sec_filing_legal_decoder.cli)
fi

"${CLI[@]}" risk-cards examples/synthetic_sec_inline_xbrl.htm \
  --review-mode source-only \
  --issuer-profile general \
  --output-dir outputs/skill-smoke-test

"${PYTHON_BIN}" skills/sec-filing-legal-decoder/scripts/validate_outputs.py outputs/skill-smoke-test
