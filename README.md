# OSWE-Prime: Test Suite & Coverage

This repository contains a small Python service that switches between a main model and a fallback model depending on input. This change adds a test suite and helper scripts to run coverage and test cases.

How to run (recommended):

POSIX (bash):
```bash
./setup.sh
./run_tests.sh
```

Windows (PowerShell):
```powershell
./run_all.ps1
```

Alternatively, use the standard Python commands:
```bash
python -m pip install -r requirements.txt
python -m coverage run -m pytest -q
python -m coverage report -m
```

What was added:
- `tests/test_main.py` - tests for normal behavior, fallback logic, and edge cases
- `requirements.txt` - pytest and coverage
- `setup.sh`, `run_tests.sh`, `run_all.ps1`, `run_all.sh` - setup and test runner scripts
- `COVERAGE_SUMMARY.md` - human readable summary of new coverage and branches tested

Next steps (optional):
- Add CI (GitHub Actions) to run tests and upload coverage reports
- Add tests for large inputs and performance

Contact: ask for any extra enhancement or test cases you'd like added.
