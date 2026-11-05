#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
PY="${PYTHON:-python3}"
if [[ -x .venv/bin/python ]]; then PY=.venv/bin/python; fi
"$PY" -m pytest -q
if command -v node >/dev/null 2>&1; then node --check ml_universe/static/app.js; fi
