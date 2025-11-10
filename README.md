# Test coverage for main.py

This project includes unit tests to cover both normal and fallback code paths for a simple model routing service in `main.py`.

How to run locally (PowerShell):

1. Install requirements:

   ./setup.ps1

2. Run tests and generate coverage report:

   ./run_tests.ps1

How to run locally (bash):

1. Install requirements:

   ./setup.sh

2. Run tests and generate coverage report:

   ./run_tests.sh

Generated files:
- `coverage.txt`: coverage report showing line coverage for `main.py` and tests
- `tests/test_main.py`: pytest unit tests that cover main and fallback paths

What was covered:
- `main_model` success path
- `fallback_model`
- `process_input` fallback for empty / missing input
- `process_input` fallback for the "corrupted_data" special-case
- `batch_process` file-based processing
- The `__main__` path invoked by the script

This setup should be reproducible in a single command per platform (PowerShell or bash) as shown above.