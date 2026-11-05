#!/usr/bin/env bash
# Install ML Universe in a local virtual environment and launch it in a browser.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
PYTHON="${PYTHON:-python3}"
if ! "$PYTHON" -c 'import sys; assert sys.version_info >= (3,11), "Python 3.11+ is required"'; then
  echo "Please install Python >=3.11 and python3-venv (Debian/Ubuntu)" >&2
  exit 1
fi
if [[ ! -x .venv/bin/python ]]; then
  "$PYTHON" -m venv .venv
fi
if ! .venv/bin/python -c 'import ml_universe, numpy, scipy, sklearn' 2>/dev/null; then
  .venv/bin/python -m pip install --upgrade pip
  .venv/bin/python -m pip install -e .
fi
exec .venv/bin/python -m ml_universe --browser "$@"
