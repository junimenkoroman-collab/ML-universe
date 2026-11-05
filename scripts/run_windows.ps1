$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')
if (!(Test-Path '.venv\Scripts\python.exe')) { py -3 -m venv .venv }
$python=(Resolve-Path '.venv\Scripts\python.exe').Path
& $python -m pip install -e '.[desktop]'
& $python -m ml_universe
