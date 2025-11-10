import json
import os
import tempfile

import pytest

from main import main_model, fallback_model, process_input, batch_process


def test_main_model_normal():
    data = "abc"
    out = main_model(data)
    assert out["model"] == "main"
    assert out["result"] == len(data)


def test_fallback_model_returns_zero_for_invalid_input():
    out = fallback_model(None)
    assert out["model"] == "fallback"
    assert out["result"] == 0


def test_process_input_main_path():
    record = {"input": "hello"}
    out = process_input(record)
    assert out["model"] == "main"
    assert out["result"] == len("hello")


def test_process_input_empty_input_fallback():
    record = {"input": ""}  # falsy
    out = process_input(record)
    assert out["model"] == "fallback"
    assert out["result"] == 0


def test_process_input_missing_input_key_fallback():
    record = {}  # no input key
    out = process_input(record)
    assert out["model"] == "fallback"
    assert out["result"] == 0


def test_process_input_corrupted_data_triggers_fallback():
    record = {"input": "corrupted_data"}
    out = process_input(record)
    assert out["model"] == "fallback"


def test_batch_process_reads_file(tmp_path):
    sample = [
        {"input": "ok"},
        {"input": ""},
        {"input": "corrupted_data"},
        {},
    ]
    file_path = tmp_path / "input.json"
    file_path.write_text(json.dumps(sample), encoding="utf-8")

    out = batch_process(str(file_path))
    # Check that we processed all records
    assert isinstance(out, list)
    assert len(out) == 4
    # First record should be main model
    assert out[0]["model"] == "main"
    # Next three should be fallback paths
    assert out[1]["model"] == "fallback"
    assert out[2]["model"] == "fallback"
    assert out[3]["model"] == "fallback"


def test_main_module_executes_and_prints_json(capsys):
    # Execute the module within this process so coverage captures the __main__ block
    import runpy

    runpy.run_module("main", run_name="__main__")
    captured = capsys.readouterr()
    out = json.loads(captured.out)
    assert isinstance(out, list)
    assert len(out) == 3
    assert out[0]["model"] == "main"
