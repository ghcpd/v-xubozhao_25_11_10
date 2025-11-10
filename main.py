import json

def main_model(data):
    return {"model": "main", "result": len(data)}

def fallback_model(data):
    return {"model": "fallback", "result": 0}

def process_input(record):
    try:
        if not record.get("input"):
            raise ValueError("Empty input")
        if record.get("input") == "corrupted_data":
            raise RuntimeError("Main model failed")
        return main_model(record["input"])
    except Exception:
        return fallback_model(record.get("input", ""))

def batch_process(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [process_input(rec) for rec in data]

if __name__ == "__main__":
    results = batch_process("sample_input.json")
    print(json.dumps(results, indent=2))
