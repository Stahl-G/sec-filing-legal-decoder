# SEC Filing Legal Decoder

Use this skill when a user wants to review legal-heavy SEC filing language,
especially in `10-K`, `10-Q`, `20-F`, `40-F`, annual report, or amendment
documents.

## What To Do

1. Prefer the EDGAR main `.htm/.html` filing document when available.
2. Use `sec-filing-legal-decoder analyze` to generate Markdown and JSON reports.
3. Use `sec-filing-legal-decoder memo` when the user wants a management-ready
   triage memo.
4. Focus on legal proceedings, risk factors, regulatory compliance, internal
   controls, debt covenants, related-party transactions, guarantees,
   commitments, dilution, and material contracts.
5. Summarize outputs as risk notes, reading decisions, and escalation questions.

## Guardrails

- Do not provide legal advice, investment advice, accounting advice, audit
  advice, or disclosure conclusions.
- Treat outputs as triage aids requiring qualified professional review.
- Do not use PDF as the primary source when an EDGAR `.htm/.html` main filing is
  available.
- Do not include confidential company documents, credentials, raw logs, or
  material non-public information in this repository.

## First Command

```bash
sec-filing-legal-decoder analyze examples/synthetic_sec_inline_xbrl.htm \
  --out outputs/html-report.md \
  --json outputs/html-report.json
```
