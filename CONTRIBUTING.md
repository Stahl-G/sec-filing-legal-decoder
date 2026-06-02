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

Keep the project deterministic, rule-based, and source-only unless a release
explicitly introduces a new adapter boundary.

## Pull Requests

After the `0.4.2` bridge release, use pull requests by default:

```bash
git switch main
git pull --ff-only
git switch -c codex/short-change-name
pytest
python evals/run_evals.py
git push -u origin codex/short-change-name
gh pr create --base main --head codex/short-change-name
```

Direct pushes to `main` after `0.4.2` should be limited to explicit hotfix or
maintenance requests.

## Safety

- Do not include confidential company documents.
- Use synthetic examples or clearly public filing excerpts only.
- Do not add legal, investment, accounting, or audit conclusions.
- Add tests when changing classification, triage, reports, or parser behavior.
- Keep PR titles, descriptions, branch names, commits, screenshots, and sample
  outputs free of private filing names, internal company names, credentials, raw
  logs, or material non-public information.
