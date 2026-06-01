# Contributing

Thanks for improving SEC Filing Legal Decoder.

## Development

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install ".[dev]"
pytest
python evals/run_evals.py
```

Keep v0.1 deterministic and rule-based. New model, EDGAR, MinerU API, DOCX, or
diff features should be added behind adapters so Markdown/TXT analysis continues
to work without external credentials.

## Safety

- Do not include confidential company documents.
- Use synthetic examples or clearly public filing excerpts only.
- Do not add legal, investment, accounting, or audit conclusions.
- Add tests when changing classification, triage, reports, or parser behavior.
