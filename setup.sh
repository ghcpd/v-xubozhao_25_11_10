#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade pip
pip install -r requirements.txt
echo "Setup complete. To run tests: ./run_tests.sh"