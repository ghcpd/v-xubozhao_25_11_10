#!/usr/bin/env bash
set -euo pipefail

if [ -d ".venv" ]; then
  # Linux/macOS venv activation
  source .venv/bin/activate || true
fi

echo "Running tests with coverage..."
coverage run -m pytest -q
coverage report -m > coverage.txt
coverage html -d coverage_html || true

echo "Coverage report generated at coverage.txt and coverage_html/index.html"
echo "--- Coverage summary ---"
cat coverage.txt
