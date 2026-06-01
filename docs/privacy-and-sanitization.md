# Privacy And Sanitization

This repository must not contain private company material.

Do not commit:

- Internal company documents.
- Private filings.
- Material non-public information.
- Real employer-specific examples.
- Internal transaction names or private legal/finance questions.
- Credentials, tokens, raw logs, or personal data.
- Generated reports from user-specific private filings.

Use synthetic examples only in docs, examples, tests, evals, issue templates, screenshots, and committed sample outputs.

Acceptable synthetic names include:

- Sample Foreign Issuer
- Sample Small FPI
- Sample Solar Manufacturer
- Synthetic De-SPAC Issuer
- Under-Covered Manufacturing Issuer
- Example Renewable Manufacturer

Public SEC filings may be used for local testing only when the filing is clearly public and already filed. Do not commit large downloaded filings or generated reports unless they are intentionally synthetic and reviewed.

## Local Private Testing

Use gitignored folders:

```text
local_filings/
private_filings/
private_outputs/
outputs/
```

## Sensitive-Term Scanner

Create a local `sensitive_terms.txt` file for private names or phrases that must not enter commits. This file is gitignored.

```bash
cp sensitive_terms.example.txt sensitive_terms.txt
python scripts/check_sensitive_terms.py
```

The scanner is intentionally local. Do not add private company names to source code, tests, docs, examples, or committed config.
