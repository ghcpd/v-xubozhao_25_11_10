#!/usr/bin/env bash
set -euo pipefail

# Run pytest with coverage and output a coverage.txt report
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 coverage run -m pytest -q
coverage report -m > coverage.txt
echo "Coverage report saved to coverage.txt"
echo "---- Summary ----"
coverage report -m