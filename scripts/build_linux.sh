#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python -m pip install '.[build]'
python -m pytest -q
python -m PyInstaller --noconfirm --clean --onedir --name ML_Universe \
  --add-data 'ml_universe/static:ml_universe/static' --collect-all sklearn --collect-all scipy run.py
printf '\nLinux binary is in dist/ML_Universe/ (not Windows .exe).\n'
