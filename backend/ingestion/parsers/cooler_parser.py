from bs4 import BeautifulSoup
from pathlib import Path
import json
import re
from datetime import date

BASE_DIR = Path(__file__).resolve().parents[3]

RAW_COOLER_HTML = BASE_DIR / "backend" / "catalog" / "raw" / "cooler_raw.html"
OUTPUT_JSON = BASE_DIR / "backend" / "catalog" / "processed" / "cooler.json"


def clean_price(price_text: str) -> int:
    numbers = re.sub(r"[^\d]", "", price_text)
    return int(numbers) if numbers else 0


def extract_cooler_type(name: str) -> str:
    name = name.upper()
    if "LIQUID" in name or "AIO" in name:
        return "Liquid"
    return "Air"


def parse_cooler_html():
    soup = BeautifulSoup(RAW_COOLER_HTML.read_text(encoding="utf-8"), "lxml")

    table = soup.find("table")
    rows = table.find_all("tr")[1:]  # skip header

    coolers = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 3:
            continue

        raw_name = cols[0].get_text(strip=True)
        raw_price = cols[2].get_text(strip=True)

        cooler = {
            "id": raw_name.lower().replace(" ", "_"),
            "name": raw_name,
            "category": "cooler",
            "brand": raw_name.split()[0],
            "type": extract_cooler_type(raw_name),
            "price_inr": clean_price(raw_price),
            "source": "pcpricetracker",
            "last_updated": str(date.today())
        }

        coolers.append(cooler)

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(coolers, indent=2), encoding="utf-8")

    print(f"Saved {len(coolers)} coolers to {OUTPUT_JSON}")


if __name__ == "__main__":
    parse_cooler_html()
