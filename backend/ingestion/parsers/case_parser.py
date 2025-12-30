from bs4 import BeautifulSoup
from pathlib import Path
import json
import re
from datetime import date

BASE_DIR = Path(__file__).resolve().parents[3]

RAW_CASE_HTML = BASE_DIR / "backend" / "catalog" / "raw" / "case_raw.html"
OUTPUT_JSON = BASE_DIR / "backend" / "catalog" / "processed" / "case.json"


def clean_price(price_text: str) -> int:
    numbers = re.sub(r"[^\d]", "", price_text)
    return int(numbers) if numbers else 0


def extract_form_factor(name: str) -> str:
    name = name.upper()
    if "MINI ITX" in name or "ITX" in name:
        return "Mini-ITX"
    if "MICRO ATX" in name or "M-ATX" in name:
        return "Micro-ATX"
    return "ATX"  # default / most common


def parse_case_html():
    soup = BeautifulSoup(RAW_CASE_HTML.read_text(encoding="utf-8"), "lxml")

    table = soup.find("table")
    rows = table.find_all("tr")[1:]  # skip header

    case_list = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 3:
            continue

        raw_name = cols[0].get_text(strip=True)
        raw_price = cols[2].get_text(strip=True)

        case = {
            "id": raw_name.lower().replace(" ", "_"),
            "name": raw_name,
            "category": "case",
            "brand": raw_name.split()[0],
            "form_factor": extract_form_factor(raw_name),
            "price_inr": clean_price(raw_price),
            "source": "pcpricetracker",
            "last_updated": str(date.today())
        }

        case_list.append(case)

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(case_list, indent=2), encoding="utf-8")

    print(f"Saved {len(case_list)} cases to {OUTPUT_JSON}")


if __name__ == "__main__":
    parse_case_html()
