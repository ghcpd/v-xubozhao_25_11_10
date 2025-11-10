#!/usr/bin/env pwsh
Set-StrictMode -Version Latest
if (Test-Path -Path .venv) {
    Write-Output "Activating venv and running tests..."
}
else {
    python -m venv .venv
}
python -m pip install -r requirements.txt
python -m coverage run -m pytest -q
python -m coverage report -m | Out-File -FilePath coverage.txt -Encoding utf8
Write-Output "Coverage written to coverage.txt"
