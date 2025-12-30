import json
from pathlib import Path


def load_catalog() -> dict:
    BASE_DIR = Path(__file__).resolve().parents[3]
    catalog_dir = BASE_DIR / "backend" / "catalog" / "processed"

    catalog = {}

    for file in catalog_dir.glob("*.json"):
        part = file.stem
        with open(file, "r", encoding="utf-8") as f:
            catalog[part] = json.load(f)

    return catalog
