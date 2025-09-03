import json, csv, pathlib

def load_data(path: str):
    p = pathlib.Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Data file not found: {path}")

    if p.suffix == ".json":
        return json.loads(p.read_text(encoding="utf-8"))

    if p.suffix == ".csv":
        with p.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return [row for row in reader]

    raise ValueError(f"Unsupported file format: {p.suffix}")
