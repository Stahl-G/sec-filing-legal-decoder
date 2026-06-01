# Development Workflow

Use this workflow for first-time local setup.

```bash
git clone https://github.com/Stahl-G/sec-filing-legal-decoder.git
cd sec-filing-legal-decoder
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
pytest
```

The primary development workflow is `risk-cards`:

```bash
sec-filing-legal-decoder risk-cards examples/synthetic_sec_inline_xbrl.htm \
  --review-mode source-only \
  --issuer-profile general \
  --output-dir outputs/dev-smoke
```

Use `analyze` only for legacy paragraph-level debugging.

Do not place private filings, private issuer names, raw logs, credentials, or material non-public information in the repository. Keep user-specific test files under `local_filings/`, `private_filings/`, or another gitignored path.
