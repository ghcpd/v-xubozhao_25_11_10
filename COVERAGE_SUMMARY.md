# Coverage Summary

All tests pass and coverage is 100% for the code base as of this run.

Previously untested fallback branches that are now covered:
- Empty input path in `process_input` (ValueError -> fallback)
- Corrupted data path in `process_input` (RuntimeError -> fallback)
- Missing `input` key in `process_input` (fallback)
- None input in `process_input` (fallback)
- Main model exception (TypeError raised by len on unsupported objects) handled by `process_input` fallback
- Integer input leading to `main_model` exception -> fallback
- Batch processing reading valid list and handling record-level fallback
- Execution of the script's `__main__` block via `runpy` execution

Notes:
- `batch_process` will raise exceptions on invalid JSON or when the JSON content is not a list. Tests assert that these error paths raise exceptions.
- The test suite includes a test that intentionally tests `main_model` failing due to len() raising an exception to ensure fallback is invoked.

How to run tests and generate coverage:
1. `python -m pip install -r requirements.txt`
2. `python -m coverage run -m pytest -q`
3. `python -m coverage report -m` or use the helper scripts `run_tests.sh` (POSIX) or `run_all.ps1` (PowerShell)

Files of note:
- `tests/test_main.py` - comprehensive tests as described above
- `coverage.txt` - coverage output generated via coverage
