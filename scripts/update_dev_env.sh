#!/usr/bin/env bash
set -euo pipefail

git status
git pull --ff-only
python -m pip install -e ".[dev]"
pytest
