# Update Workflow

Update without deleting or recloning:

```bash
git status
git pull --ff-only
python -m pip install -e ".[dev]"
pytest
```

If local changes exist:

```bash
git stash push -u -m "local-wip-before-update"
git pull --ff-only
python -m pip install -e ".[dev]"
pytest
git stash pop
```

If conflicts appear after `git stash pop`, resolve them locally, rerun tests,
and avoid committing private filings or generated private outputs.
