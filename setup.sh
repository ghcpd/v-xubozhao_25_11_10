#!/usr/bin/env bash
set -euo pipefail

echo "Creating virtual environment .venv..."
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Installed dependencies into .venv"
