Write-Host "Installing requirements..."
python -m pip install --upgrade pip
pip install -r requirements.txt
Write-Host "Setup complete. Run .\run_tests.ps1 to execute tests and generate coverage.txt"