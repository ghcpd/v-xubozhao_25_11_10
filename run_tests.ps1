Write-Host "Running pytest and coverage..."
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = "1"
python -m coverage run -m pytest -q
python -m coverage report -m > coverage.txt
Write-Host "Coverage report saved to coverage.txt"
python -m coverage report -m