import json
import os
import pytest
from main import process_input, batch_process


class LenError:
    def __len__(self):
        raise TypeError("len failed")


def test_main_model_with_string():
    rec = {"input": "hello"}
    res = process_input(rec)
    assert res["model"] == "main"
    assert res["result"] == len("hello")


def test_main_model_with_list():
    rec = {"input": [1, 2, 3, 4]}
    res = process_input(rec)
    assert res["model"] == "main"
    assert res["result"] == 4


def test_fallback_empty_string():
    rec = {"input": ""}
    res = process_input(rec)
    assert res["model"] == "fallback"
    assert res["result"] == 0


def test_fallback_missing_key():
    rec = {}
    res = process_input(rec)
    assert res["model"] == "fallback"
    assert res["result"] == 0


def test_fallback_corrupted_data():
    rec = {"input": "corrupted_data"}
    res = process_input(rec)
    assert res["model"] == "fallback"
    assert res["result"] == 0


def test_fallback_main_model_exception():
    rec = {"input": LenError()}
    res = process_input(rec)
    assert res["model"] == "fallback"
    assert res["result"] == 0


def test_fallback_none_input():
    rec = {"input": None}
    res = process_input(rec)
    assert res["model"] == "fallback"
    assert res["result"] == 0


def test_batch_process(tmp_path):
    data = [
        {"input": "normal_case"},
        {"input": "corrupted_data"},
        {"input": ""},
    ]
    p = tmp_path / "data.json"
    p.write_text(json.dumps(data))
    results = batch_process(str(p))
    assert isinstance(results, list)
    assert results[0]["model"] == "main"
    assert results[1]["model"] == "fallback"
    assert results[2]["model"] == "fallback"


def test_exec_main(tmp_path):
    # Create a sample_input.json file similar to default one
    data = [{"input": "abc"}, {"input": ""}]
    p = tmp_path / "sample_input.json"
    p.write_text(json.dumps(data))

    # Execute main.py using runpy.run_path with __name__ set to __main__ so coverage captures it
    import runpy
    from pathlib import Path
    cwd_root = Path(__file__).resolve().parents[1]
    # ensure we run the script from repo root so it finds the sample_input.json
    cwd_before = Path.cwd()
    try:
        Path.cwd()
        os.chdir(str(cwd_root))
        runpy.run_path(str(cwd_root / "main.py"), run_name="__main__")
    finally:
        os.chdir(str(cwd_before))


def test_int_input_fallback():
    rec = {"input": 123}
    res = process_input(rec)
    assert res["model"] == "fallback"
    assert res["result"] == 0


def test_batch_process_invalid_json(tmp_path):
    # invalid json content
    p = tmp_path / "bad.json"
    p.write_text("{ this is not: valid json }")
    with pytest.raises(Exception):
        batch_process(str(p))


def test_batch_process_non_list_json(tmp_path):
    # JSON is an object, not a list, which will trigger processing issues
    p = tmp_path / "obj.json"
    p.write_text(json.dumps({"input": "abc"}))
    with pytest.raises(Exception):
        batch_process(str(p))
