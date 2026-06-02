# Privacy And Sanitization

Do not commit private company material.

Never add:

- Real employer names.
- Internal company names.
- Internal transaction names.
- Private filings.
- Private legal, finance, audit, or management memos.
- Material non-public information.
- Credentials, tokens, raw logs, personal data, or local screenshots.
- Generated reports from user-specific private filings.

Use synthetic examples in skill files, references, examples, tests, evals, docs,
and sample outputs.

Acceptable synthetic names:

- Sample Foreign Issuer
- Sample Small FPI
- Sample De-SPAC Issuer
- Sample Manufacturing Issuer
- Sample Renewable Manufacturer
- Example Annual Report Issuer

Keep local inputs and outputs in gitignored folders such as `local_filings/`,
`private_filings/`, `private_outputs/`, or `outputs/`.

If testing user-provided private files, do not commit the inputs or generated
outputs.

Optional local sensitive-term scanning:

```bash
cp sensitive_terms.example.txt sensitive_terms.txt
python scripts/check_sensitive_terms.py
python skills/sec-filing-legal-decoder/scripts/validate_skill_structure.py
```
