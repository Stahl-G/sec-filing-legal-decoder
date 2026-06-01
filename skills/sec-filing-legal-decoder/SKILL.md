# SEC Filing Legal Decoder

Use this skill when a user wants to review legal-heavy SEC filing language,
especially in `10-K`, `10-Q`, `20-F`, `40-F`, annual report, or amendment
documents.

## What To Do

1. Prefer the EDGAR main `.htm/.html` filing document when available.
2. Use `sec-filing-legal-decoder risk-cards` for the preferred v0.3.0 workflow:
   an integrated `legal-risk-review.md` plus issue-level legal risk cards.
3. Use `sec-filing-legal-decoder review-overlay` when the user has an existing
   finance or earnings analysis and wants legal/governance/disclosure gaps.
4. Use `sec-filing-legal-decoder analyze` only when the user specifically wants
   legacy paragraph-level review output.
5. Use `sec-filing-legal-decoder memo` when the user wants a management-ready
   triage memo.
6. Use `--obsidian-dir` with `risk-cards` when the user wants linked Obsidian
   risk-card notes.
7. Focus on legal proceedings, risk factors, regulatory compliance, internal
   controls, debt covenants, related-party transactions, guarantees,
   commitments, dilution, tax, cybersecurity governance, disclosure consistency,
   and material contracts.
8. Read `legal-risk-review.md` first, then use `legal-risk-cards.md` and
   `evidence-audit.md` as appendices for card and source-evidence details.
9. Summarize outputs as issuer-specific legal risk themes, escalation questions,
   management follow-up, and what-not-to-overstate cautions.
10. Use `--lang zh-CN --term-style bilingual` when the user wants Chinese
    explanation with key English filing/legal terms preserved. Source excerpts
    remain in the original filing language.

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
sec-filing-legal-decoder risk-cards examples/synthetic_sec_inline_xbrl.htm \
  --output-dir outputs/sample-risk-cards
```

For Chinese bilingual output:

```bash
sec-filing-legal-decoder risk-cards examples/synthetic_sec_inline_xbrl.htm \
  --output-dir outputs/sample-risk-cards-zh \
  --lang zh-CN \
  --term-style bilingual
```

## Obsidian Export

The normal `risk-cards --output-dir` Markdown is already Obsidian-friendly.
Use `--obsidian-dir` when the user wants linked risk-card notes inside an
Obsidian folder.

```bash
sec-filing-legal-decoder risk-cards input.htm \
  --output-dir outputs/company-risk-cards \
  --obsidian-dir ~/Documents/ObsidianVault/SEC\ Filings/COMPANY/2025\ 10-K \
  --company "Company Name" \
  --ticker TICKER \
  --form 10-K \
  --year 2025
```
