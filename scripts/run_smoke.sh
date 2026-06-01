#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="${PYTHONPATH:-}:src"

if command -v sec-filing-legal-decoder >/dev/null 2>&1; then
  CLI=(sec-filing-legal-decoder)
elif command -v python3 >/dev/null 2>&1; then
  CLI=(python3 -m sec_filing_legal_decoder.cli)
else
  CLI=(python -m sec_filing_legal_decoder.cli)
fi

"${CLI[@]}" risk-cards examples/synthetic_sec_inline_xbrl.htm \
  --review-mode source-only \
  --issuer-profile general \
  --output-dir outputs/smoke-risk-cards

"${CLI[@]}" risk-cards examples/synthetic_sec_inline_xbrl.htm \
  --review-mode source-only \
  --issuer-profile general \
  --lang zh-CN \
  --output-dir outputs/smoke-risk-cards-zh

test -f outputs/smoke-risk-cards/legal-risk-review.md
test -f outputs/smoke-risk-cards/legal-risk-cards.md
test -f outputs/smoke-risk-cards/legal-risk-cards.json
test -f outputs/smoke-risk-cards-zh/legal-risk-review.md
