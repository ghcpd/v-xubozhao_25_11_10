$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
Push-Location 'e:\Bug Bash\11_10\GPT-5-mini'
python -m coverage run --source=. -m pytest -q -p no:pytest_flask
python -m coverage report -m > coverage.txt
python -m pytest -q -p no:pytest_flask | Tee-Object -FilePath test_log.txt
Pop-Location
