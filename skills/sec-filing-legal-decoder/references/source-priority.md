# Source Priority

Prefer the official SEC EDGAR main `.htm` / `.html` filing. For modern annual
and quarterly reports, this is usually Inline XBRL HTML: readable in a browser
and parseable by HTML tooling.

## Priority Order

1. Official SEC EDGAR `.htm` / `.html` main filing.
2. SEC `.txt` submission package when the main HTML must be extracted.
3. Company investor relations HTML if EDGAR HTML is unavailable.
4. PDF only when HTML is unavailable.
5. MinerU / OCR fallback only for PDF-only or non-EDGAR documents.

Do not prefer PDF when EDGAR HTML is available.

## MinerU

MinerU is optional. Use it only for PDF, Office, image, or non-EDGAR documents
that cannot be parsed as EDGAR HTML, Markdown, or TXT.

Do not upload confidential documents to external parsers unless the user
explicitly approves and the document is safe to process.

## Agent Rule

When the user provides several formats, pick EDGAR HTML first. If only a PDF is
available, state that PDF is a fallback and may have table, line-break, header,
footer, and OCR issues.
