import json
import pytest

from main import main_model, fallback_model, process_input, batch_process


def test_main_model_normal():
    data = "abcd"
    res = main_model(data)
    assert res == {"model": "main", "result": 4}


def test_fallback_model():
    res = fallback_model("anything")
    assert res == {"model": "fallback", "result": 0}


def test_process_input_main_path():
    rec = {"input": "hello"}
    res = process_input(rec)
    assert res["model"] == "main"
    assert res["result"] == len(rec["input"]) 


def test_process_input_corrupted_triggers_fallback():
    rec = {"input": "corrupted_data"}
    res = process_input(rec)
    assert res == {"model": "fallback", "result": 0}


def test_process_input_empty_string_triggers_fallback():
    rec = {"input": ""}
    res = process_input(rec)
    assert res == {"model": "fallback", "result": 0}


def test_process_input_missing_key_triggers_fallback():
    rec = {}
    res = process_input(rec)
    assert res == {"model": "fallback", "result": 0}


def test_batch_process(tmp_path):
    data = [{"input": "a"}, {"input": ""}, {"input": "corrupted_data"}, {}]
    p = tmp_path / "test.json"
    p.write_text(json.dumps(data))
    res = batch_process(str(p))
    assert res[0]["model"] == "main" and res[0]["result"] == 1
    for r in res[1:]:
        assert r == {"model": "fallback", "result": 0}
