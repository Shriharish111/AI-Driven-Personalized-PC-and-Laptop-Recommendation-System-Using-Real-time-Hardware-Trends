from bs4 import BeautifulSoup
from pathlib import Path
import json
import re
from datetime import date

BASE_DIR = Path(__file__).resolve().parents[3]

RAW_UPS_HTML = BASE_DIR / "backend" / "catalog" / "raw" / "ups_raw.html"
OUTPUT_JSON = BASE_DIR / "backend" / "catalog" / "processed" / "ups.json"


def clean_price(price_text: str) -> int:
    numbers = re.sub(r"[^\d]", "", price_text)
    return int(numbers) if numbers else 0


def extract_va(name: str) -> int:
    """
    Extract VA rating like 600VA, 1100VA, 1500VA
    """
    match = re.search(r"(\d+)\s*VA", name.upper())
    return int(match.group(1)) if match else 0


def parse_ups_html():
    soup = BeautifulSoup(RAW_UPS_HTML.read_text(encoding="utf-8"), "lxml")

    table = soup.find("table")
    rows = table.find_all("tr")[1:]  # skip header

    ups_list = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 3:
            continue

        raw_name = cols[0].get_text(strip=True)
        raw_price = cols[2].get_text(strip=True)

        ups = {
            "id": raw_name.lower().replace(" ", "_"),
            "name": raw_name,
            "category": "ups",
            "brand": raw_name.split()[0],
            "capacity_va": extract_va(raw_name),
            "price_inr": clean_price(raw_price),
            "source": "pcpricetracker",
            "last_updated": str(date.today())
        }

        ups_list.append(ups)

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(ups_list, indent=2), encoding="utf-8")

    print(f"Saved {len(ups_list)} UPS entries to {OUTPUT_JSON}")


if __name__ == "__main__":
    parse_ups_html()
