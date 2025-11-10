#!/usr/bin/env bash
# Run tests with coverage and output coverage report to coverage.txt and test_log.txt
# Use python -m to ensure the correct modules are executed on Windows
python -m coverage run -m pytest -q -p no:pytest_flask
python -m coverage report -m > coverage.txt
python -m pytest -q -p no:pytest_flask | tee test_log.txt
