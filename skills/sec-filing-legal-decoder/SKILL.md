---
name: sec-filing-legal-decoder
description: This skill should be used when the user asks to "review a 10-K", "review a 20-F", "analyze SEC filing legal risks", "decode legal-heavy annual report language", "generate legal risk cards", "explain filing legal risks for finance readers", "review related-party transactions", "review going concern language", "check internal control weaknesses", "review legal proceedings", "analyze warrants or earnout dilution", "review debt covenants", "generate escalation questions", "create a Chinese legal-to-finance review", or perform source-only legal risk review of 10-K, 10-Q, 20-F, 40-F, 6-K, annual reports, and amendment documents.
version: 0.4.2
---

# SEC Filing Legal Decoder

## Purpose

Use this skill to run `sec-filing-legal-decoder`, a Python CLI and agent-readable
workflow for source-only legal-to-finance review of SEC filings. The core output
is an integrated `legal-risk-review.md` plus evidence-backed legal risk cards,
escalation questions, management follow-up, evidence audit, and JSON.

Keep the Python CLI as the execution layer. Treat this skill as the agent
entrypoint that teaches when to use the project, which source file to prefer,
which command to run, which outputs to read, and which professional boundaries
to preserve.

## When To Use

Use for legal-heavy `10-K`, `10-Q`, `20-F`, `40-F`, `6-K`, annual report, and
amendment review. Typical requests include SEC filing legal-risk review,
going-concern language, internal control weakness, legal proceedings,
related-party transactions, debt covenants, guarantees, commitments, warrants,
earnout dilution, disclosure consistency, cybersecurity governance, material
contracts, and Chinese bilingual legal-to-finance review.

Do not use as a generic financial statement reader. Use it when the question is
whether filing language is boilerplate, finance-relevant, needs escalation, or
requires Legal / Finance / Auditor / IR / Board follow-up.

## Default Workflow

Prefer the risk-card workflow:

```bash
sec-filing-legal-decoder risk-cards input.htm \
  --review-mode source-only \
  --issuer-profile general \
  --output-dir outputs/sample-risk-review
```

If the installed CLI does not support `--review-mode` or `--issuer-profile`,
fall back to:

```bash
sec-filing-legal-decoder risk-cards input.htm \
  --output-dir outputs/sample-risk-review
```

Use issuer profiles only when the filing context supports them:

- `general`
- `small-issuer`
- `foreign-private-issuer`
- `spac-de-spac`
- `manufacturing`
- `solar-manufacturing`

## Source Priority

Prefer sources in this order:

1. Official SEC EDGAR `.htm` / `.html` main filing.
2. SEC `.txt` submission package only when the main HTML must be extracted.
3. Company investor relations HTML if EDGAR HTML is unavailable.
4. PDF only when HTML is unavailable.
5. MinerU / OCR fallback only for PDF-only or non-EDGAR documents.

Do not prefer PDF when EDGAR HTML is available. Read
`references/source-priority.md` for details.

## Primary Commands

English source-only review:

```bash
sec-filing-legal-decoder risk-cards input.htm \
  --review-mode source-only \
  --issuer-profile general \
  --output-dir outputs/sample-risk-review
```

Chinese bilingual review:

```bash
sec-filing-legal-decoder risk-cards input.htm \
  --review-mode source-only \
  --issuer-profile general \
  --lang zh-CN \
  --output-dir outputs/sample-risk-review-zh
```

Review an existing finance analysis against filing risk cards:

```bash
sec-filing-legal-decoder review-overlay input.htm \
  --analysis existing-analysis.md \
  --output-dir outputs/sample-overlay
```

Use `analyze` only for legacy paragraph-level debugging.

## Output Reading Order

Read outputs in this order:

1. `legal-risk-review.md`
2. `legal-risk-cards.md`
3. `escalation-questions.md`
4. `management-follow-up.md`
5. `evidence-audit.md`
6. `legal-risk-cards.json`

Read `references/output-contract.md` before summarizing outputs for a user.

## Chinese Bilingual Output

Use `--lang zh-CN` when the user wants Chinese explanation. Write Chinese
explanation first, preserve key English legal / accounting / SEC terms, and keep
source excerpts in the original filing language. Avoid Chinese legal
over-translation that implies non-US legal concepts when the source is SEC / US
reporting language.

Read `references/zh-cn-legal-style.md` for style rules and term examples.

## Source-Only Review

Keep review source-only. Use only the filing text and built-in legal risk
grammar. Do not add media coverage, law-firm memos, analyst reports, external
public legal review, market data, databases, web search, or user-specific
internal knowledge unless a future workflow explicitly supports enrichment and
the user asks for it.

Read `references/source-only-review.md` for rationale and boundaries.

## Privacy Guardrails

Do not commit private filings, internal company names, employer-specific
examples, internal transaction names, raw logs, credentials, personal data, or
material non-public information. Keep user-specific inputs and generated outputs
in gitignored local folders.

Use synthetic issuer names in prompts, examples, tests, docs, and sample
outputs. Read `references/privacy-and-sanitization.md` before creating or
committing skill files.

## Professional-Boundary Guardrails

Do not provide legal advice, investment advice, accounting advice, audit advice,
disclosure conclusions, or professional opinions. Treat all outputs as triage
aids requiring qualified professional review.

Do not overstate speculative, conditional, forward-looking, boilerplate, or
uncertain disclosure as confirmed events. Do not infer wrongdoing, liability,
breach, fraud, illegality, default, or regulatory violation unless the filing
explicitly supports that statement.

## Additional Resources

- `references/source-priority.md`: source selection and MinerU fallback.
- `references/risk-taxonomy.md`: risk domains, signals, and typical owners.
- `references/output-contract.md`: output files, reading contract, and v0.5 placeholders.
- `references/source-only-review.md`: source-only boundaries.
- `references/privacy-and-sanitization.md`: repository privacy rules.
- `references/zh-cn-legal-style.md`: Chinese bilingual style rules.
- `references/update-workflow.md`: update without recloning.
- `examples/prompt-basic-risk-cards.md`: basic agent prompt.
- `examples/prompt-zh-cn-risk-review.md`: Chinese bilingual agent prompt.
- `examples/prompt-review-overlay.md`: overlay prompt.
- `examples/prompt-small-issuer-source-only.md`: small issuer prompt.

## Smoke Test

Run the skill smoke test from the repository root:

```bash
bash skills/sec-filing-legal-decoder/scripts/run_smoke_test.sh
```

For structure-only validation:

```bash
python skills/sec-filing-legal-decoder/scripts/validate_skill_structure.py
```
