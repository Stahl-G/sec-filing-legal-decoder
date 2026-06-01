#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="${PYTHONPATH:-}:src"
if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN=python3
else
  PYTHON_BIN=python
fi

pytest
"${PYTHON_BIN}" evals/run_evals.py
"${PYTHON_BIN}" scripts/check_sensitive_terms.py
if command -v sec-filing-legal-decoder >/dev/null 2>&1; then
  sec-filing-legal-decoder --version
elif command -v python3 >/dev/null 2>&1; then
  "${PYTHON_BIN}" -m sec_filing_legal_decoder.cli --version
else
  "${PYTHON_BIN}" -m sec_filing_legal_decoder.cli --version
fi
scripts/run_smoke.sh
