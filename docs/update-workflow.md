# Update Workflow

Do not delete and re-clone the repository for routine updates. Update the existing checkout.

## Normal Update

```bash
cd sec-filing-legal-decoder
git status
git pull --ff-only
python -m pip install -e ".[dev]"
pytest
```

## If Local Files Changed

```bash
git status
git stash push -u -m "local-wip-before-update"
git pull --ff-only
python -m pip install -e ".[dev]"
pytest
git stash pop
```

Resolve any stash conflicts manually, then rerun tests.

## If Using Branches

```bash
git fetch origin
git switch main
git pull --ff-only
git switch -c feature/v0.4-source-only-review
```

Keep private filings and generated private reports in gitignored directories such as `local_filings/`, `private_filings/`, and `private_outputs/`.
