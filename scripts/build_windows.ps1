# Build a portable Windows executable on a genuine Windows x64 host.
param([switch]$SkipTests)
$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')
Write-Host '== ML Universe / Windows x64 build ==' -ForegroundColor Cyan
if (!(Test-Path '.venv\Scripts\python.exe')) { py -3 -m venv .venv }
$python=(Resolve-Path '.venv\Scripts\python.exe').Path
& $python -m pip install --upgrade pip setuptools wheel
& $python -m pip install -r requirements-windows.txt
if (-not $SkipTests) {
    & $python -m pytest -q
    if ($LASTEXITCODE -ne 0) { throw 'Tests failed. Build canceled.' }
}
& $python -m PyInstaller --noconfirm --clean --onedir --windowed --name ML_Universe `
    --add-data 'ml_universe\static;ml_universe\static' `
    --collect-all sklearn --collect-all scipy --collect-all webview `
    --hidden-import sklearn.utils._cython_blas --hidden-import scipy.special._ufuncs `
    run.py
if ($LASTEXITCODE -ne 0) { throw 'PyInstaller failed.' }
$exe='dist\ML_Universe\ML_Universe.exe'
if (!(Test-Path $exe)) { throw 'ML_Universe.exe is missing.' }
Write-Host '== Checking packaged executable / local API ==' -ForegroundColor Cyan
$port=18765
$process=Start-Process -FilePath (Resolve-Path $exe).Path -ArgumentList @('--port',$port,'--no-open') -PassThru
try {
    $ok=$false
    for($i=0; $i -lt 35; $i++) {
        Start-Sleep -Seconds 1
        if($process.HasExited){ throw "Packaged process exited unexpectedly: $($process.ExitCode)" }
        try { $response=Invoke-RestMethod -Uri "http://127.0.0.1:$port/api/health" -TimeoutSec 2
              if($response.ok){$ok=$true;break} } catch {}
    }
    if(-not $ok){throw 'EXE health check timed out'}
    Write-Host 'OK: packaged EXE responds to the API.' -ForegroundColor Green
} finally { Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue }
$zip='dist\ML_Universe_Windows_x64.zip'
if(Test-Path $zip){Remove-Item $zip}
Compress-Archive -Path 'dist\ML_Universe' -DestinationPath $zip -CompressionLevel Optimal
Write-Host "Completed: $zip" -ForegroundColor Green
Write-Host 'Unzip the folder, then run ML_Universe\ML_Universe.exe (do not move EXE alone).'
