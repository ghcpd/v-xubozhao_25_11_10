import pytest
import json
import tempfile
import os
from pathlib import Path
from main import main_model, fallback_model, process_input, batch_process


class TestMainModel:
    """Tests for main_model function."""
    
    def test_main_model_with_valid_string(self):
        """Test main_model returns correct result with valid string input."""
        result = main_model("hello")
        assert result == {"model": "main", "result": 5}
        assert result["model"] == "main"
        assert result["result"] == 5
    
    def test_main_model_with_empty_string(self):
        """Test main_model with empty string."""
        result = main_model("")
        assert result == {"model": "main", "result": 0}
        assert result["result"] == 0
    
    def test_main_model_with_long_string(self):
        """Test main_model with longer string."""
        long_input = "a" * 100
        result = main_model(long_input)
        assert result["result"] == 100
        assert result["model"] == "main"


class TestFallbackModel:
    """Tests for fallback_model function."""
    
    def test_fallback_model_always_returns_zero(self):
        """Test fallback_model always returns result=0 regardless of input."""
        result = fallback_model("any_input")
        assert result == {"model": "fallback", "result": 0}
        assert result["result"] == 0
    
    def test_fallback_model_with_empty_input(self):
        """Test fallback_model with empty input."""
        result = fallback_model("")
        assert result["model"] == "fallback"
        assert result["result"] == 0
    
    def test_fallback_model_with_none(self):
        """Test fallback_model with None input."""
        result = fallback_model(None)
        assert result == {"model": "fallback", "result": 0}


class TestProcessInput:
    """Tests for process_input function - the critical function with fallback paths."""
    
    # NORMAL PATH TESTS
    def test_process_input_normal_case(self):
        """Test normal path: valid input processes with main model."""
        record = {"input": "normal_case"}
        result = process_input(record)
        assert result["model"] == "main"
        assert result["result"] == 11  # len("normal_case") == 11
    
    def test_process_input_with_valid_data(self):
        """Test normal path with different valid input."""
        record = {"input": "test"}
        result = process_input(record)
        assert result["model"] == "main"
        assert result["result"] == 4
    
    # FALLBACK PATH TESTS - Empty Input
    def test_process_input_empty_string_fallback(self):
        """FALLBACK: Test empty input triggers fallback path."""
        record = {"input": ""}
        result = process_input(record)
        assert result["model"] == "fallback"
        assert result["result"] == 0
    
    def test_process_input_missing_input_key_fallback(self):
        """FALLBACK: Test missing 'input' key triggers fallback path."""
        record = {}
        result = process_input(record)
        assert result["model"] == "fallback"
        assert result["result"] == 0
    
    def test_process_input_none_value_fallback(self):
        """FALLBACK: Test None as input value triggers fallback path."""
        record = {"input": None}
        result = process_input(record)
        assert result["model"] == "fallback"
        assert result["result"] == 0
    
    # FALLBACK PATH TESTS - Exception Handling
    def test_process_input_corrupted_data_fallback(self):
        """FALLBACK: Test corrupted_data triggers RuntimeException fallback."""
        record = {"input": "corrupted_data"}
        result = process_input(record)
        assert result["model"] == "fallback"
        assert result["result"] == 0
    
    def test_process_input_exception_handling(self):
        """FALLBACK: Test that exceptions trigger fallback model."""
        # The corrupted_data case raises RuntimeError
        record = {"input": "corrupted_data"}
        result = process_input(record)
        assert result["model"] == "fallback"
    
    # EDGE CASES
    def test_process_input_with_numeric_string(self):
        """Test numeric string input."""
        record = {"input": "12345"}
        result = process_input(record)
        assert result["model"] == "main"
        assert result["result"] == 5
    
    def test_process_input_with_special_characters(self):
        """Test input with special characters."""
        record = {"input": "!@#$%"}
        result = process_input(record)
        assert result["model"] == "main"
        assert result["result"] == 5
    
    def test_process_input_with_whitespace_only(self):
        """Test whitespace-only input is treated as valid (non-empty)."""
        record = {"input": "   "}
        result = process_input(record)
        # Since "   " is not empty (len > 0), it should use main model
        assert result["model"] == "main"
        assert result["result"] == 3
    
    def test_process_input_record_with_extra_fields(self):
        """Test record with extra fields doesn't break processing."""
        record = {"input": "data", "extra": "field", "another": 123}
        result = process_input(record)
        assert result["model"] == "main"
        assert result["result"] == 4
    
    def test_process_input_false_value_fallback(self):
        """FALLBACK: Test False value is treated as falsy, triggers fallback."""
        record = {"input": False}
        result = process_input(record)
        # False is falsy, so .get("input") evaluates to False
        assert result["model"] == "fallback"
    
    def test_process_input_zero_value_fallback(self):
        """FALLBACK: Test 0 is treated as falsy, triggers fallback."""
        record = {"input": 0}
        result = process_input(record)
        # 0 is falsy, so .get("input") evaluates to 0 (falsy)
        assert result["model"] == "fallback"


class TestBatchProcess:
    """Tests for batch_process function."""
    
    def test_batch_process_multiple_records(self):
        """Test batch processing with multiple records."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            test_data = [
                {"input": "hello"},
                {"input": "world"},
                {"input": "corrupted_data"}
            ]
            json.dump(test_data, f)
            temp_file = f.name
        
        try:
            results = batch_process(temp_file)
            assert len(results) == 3
            assert results[0]["model"] == "main"
            assert results[1]["model"] == "main"
            assert results[2]["model"] == "fallback"
        finally:
            os.unlink(temp_file)
    
    def test_batch_process_with_mixed_inputs(self):
        """Test batch processing with mixed valid and invalid inputs."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            test_data = [
                {"input": "valid"},
                {"input": ""},
                {"input": "corrupted_data"},
                {"input": "another_valid"}
            ]
            json.dump(test_data, f)
            temp_file = f.name
        
        try:
            results = batch_process(temp_file)
            assert len(results) == 4
            assert results[0]["model"] == "main"
            assert results[1]["model"] == "fallback"
            assert results[2]["model"] == "fallback"
            assert results[3]["model"] == "main"
        finally:
            os.unlink(temp_file)
    
    def test_batch_process_empty_array(self):
        """Test batch processing with empty input file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump([], f)
            temp_file = f.name
        
        try:
            results = batch_process(temp_file)
            assert results == []
        finally:
            os.unlink(temp_file)
    
    def test_batch_process_file_not_found(self):
        """Test batch process raises error for missing file."""
        with pytest.raises(FileNotFoundError):
            batch_process("nonexistent_file.json")
    
    def test_batch_process_invalid_json(self):
        """Test batch process raises error for invalid JSON."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("invalid json content {]")
            temp_file = f.name
        
        try:
            with pytest.raises(json.JSONDecodeError):
                batch_process(temp_file)
        finally:
            os.unlink(temp_file)


class TestCoverageSummary:
    """Integration tests to verify all critical paths are covered."""
    
    def test_main_path_coverage(self):
        """Verify main model execution path is covered."""
        assert process_input({"input": "test"})["model"] == "main"
    
    def test_fallback_empty_input_coverage(self):
        """Verify fallback path for empty input is covered."""
        assert process_input({"input": ""})["model"] == "fallback"
    
    def test_fallback_exception_coverage(self):
        """Verify fallback path for exceptions is covered."""
        assert process_input({"input": "corrupted_data"})["model"] == "fallback"
    
    def test_fallback_missing_input_coverage(self):
        """Verify fallback path for missing input is covered."""
        assert process_input({})["model"] == "fallback"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=main", "--cov-report=html", "--cov-report=term-missing"])
