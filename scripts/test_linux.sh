#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
PY="${PYTHON:-python3}"
if [[ -x .venv/bin/python ]]; then PY=.venv/bin/python; fi
if ! "$PY" -c 'import pytest' 2>/dev/null; then
  if [[ "$PY" == *.venv/bin/python ]]; then "$PY" -m pip install -e '.[test]';
  else echo 'pytest is missing. Run ./scripts/run_linux.sh first or install pytest' >&2; exit 1; fi
fi
"$PY" -m pytest -q
if command -v node >/dev/null 2>&1; then node --check ml_universe/static/app.js; fi
