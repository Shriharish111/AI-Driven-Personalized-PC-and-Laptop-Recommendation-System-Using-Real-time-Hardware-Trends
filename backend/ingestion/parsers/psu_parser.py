from bs4 import BeautifulSoup
from pathlib import Path
import json
import re
from datetime import date

BASE_DIR = Path(__file__).resolve().parents[3]

RAW_PSU_HTML = BASE_DIR / "backend" / "catalog" / "raw" / "psu_raw.html"
OUTPUT_JSON = BASE_DIR / "backend" / "catalog" / "processed" / "psu.json"


def clean_price(price_text: str) -> int:
    numbers = re.sub(r"[^\d]", "", price_text)
    return int(numbers) if numbers else 0


def extract_wattage(name: str) -> int:
    match = re.search(r"(\d+)\s*W", name.upper())
    return int(match.group(1)) if match else 0


def extract_efficiency(name: str) -> str:
    name = name.upper()
    if "80+" in name:
        match = re.search(r"80\+\s*(BRONZE|SILVER|GOLD|PLATINUM)", name)
        if match:
            return f"80+ {match.group(1).capitalize()}"
        return "80+"
    return "Standard"


def parse_psu_html():
    soup = BeautifulSoup(RAW_PSU_HTML.read_text(encoding="utf-8"), "lxml")

    table = soup.find("table")
    rows = table.find_all("tr")[1:]  # skip header

    psu_list = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 3:
            continue

        raw_name = cols[0].get_text(strip=True)
        raw_price = cols[2].get_text(strip=True)

        psu = {
            "id": raw_name.lower().replace(" ", "_"),
            "name": raw_name,
            "category": "psu",
            "brand": raw_name.split()[0],
            "wattage": extract_wattage(raw_name),
            "efficiency": extract_efficiency(raw_name),
            "price_inr": clean_price(raw_price),
            "source": "pcpricetracker",
            "last_updated": str(date.today())
        }

        psu_list.append(psu)

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(psu_list, indent=2), encoding="utf-8")

    print(f"Saved {len(psu_list)} PSUs to {OUTPUT_JSON}")


if __name__ == "__main__":
    parse_psu_html()
