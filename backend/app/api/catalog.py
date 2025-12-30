from fastapi import APIRouter, Query, HTTPException
from pathlib import Path
import json

router = APIRouter(prefix="/available-components", tags=["Catalog"])

BASE_DIR = Path(__file__).resolve().parents[3]
CATALOG_DIR = BASE_DIR / "backend" / "catalog" / "processed"

CATEGORY_FILE_MAP = {
    "cpu": "cpu.json",
    "gpu": "gpu.json",
    "ram": "ram.json",
    "storage": "storage.json",
    "motherboard": "motherboard.json",
    "cooler": "cooler.json",
    "psu": "psu.json",
    "case": "case.json",
    "ups": "ups.json",
}


def load_category_data(category: str):
    if category not in CATEGORY_FILE_MAP:
        raise HTTPException(status_code=400, detail="Invalid category")

    file_path = CATALOG_DIR / CATEGORY_FILE_MAP[category]

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Catalog data not found")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


@router.get("/")
def get_available_components(
    category: str = Query(..., description="Component category"),
    min_price: int | None = Query(None, ge=0),
    max_price: int | None = Query(None, ge=0),
):
    data = load_category_data(category)

    if min_price is not None:
        data = [item for item in data if item["price_inr"] >= min_price]

    if max_price is not None:
        data = [item for item in data if item["price_inr"] <= max_price]

    return {
        "category": category,
        "count": len(data),
        "items": data,
    }
