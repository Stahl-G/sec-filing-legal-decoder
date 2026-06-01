# SEC Filing Legal Decoder

Use this skill when a user wants to review legal-heavy SEC filing language,
especially in `10-K`, `10-Q`, `20-F`, `40-F`, annual report, or amendment
documents.

## What To Do

1. Prefer the EDGAR main `.htm/.html` filing document when available.
2. Use `sec-filing-legal-decoder analyze` to generate Obsidian-friendly Markdown and JSON reports.
3. Use `sec-filing-legal-decoder memo` when the user wants a management-ready
   triage memo.
4. Use `--obsidian-vault` and `--obsidian-folder` when the user wants a linked
   Obsidian reading workspace.
5. Focus on legal proceedings, risk factors, regulatory compliance, internal
   controls, debt covenants, related-party transactions, guarantees,
   commitments, dilution, and material contracts.
6. Summarize outputs as risk notes, reading decisions, and escalation questions.

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

## Obsidian Export

The normal `--out report.md` output is already Obsidian-friendly Markdown.
Use the vault options only when the user wants a linked note set inside an
Obsidian vault.

```bash
sec-filing-legal-decoder analyze input.htm \
  --obsidian-vault ~/Documents/ObsidianVault \
  --obsidian-folder "SEC Filings/COMPANY/2025 10-K" \
  --company "Company Name" \
  --ticker TICKER \
  --form 10-K \
  --year 2025
```
