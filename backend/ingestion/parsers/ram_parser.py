from bs4 import BeautifulSoup
from pathlib import Path
import json
import re
from datetime import date

BASE_DIR = Path(__file__).resolve().parents[3]

RAW_RAM_HTML = BASE_DIR / "backend" / "catalog" / "raw" / "ram_raw.html"
OUTPUT_JSON = BASE_DIR / "backend" / "catalog" / "processed" / "ram.json"


def clean_price(price_text: str) -> int:
    numbers = re.sub(r"[^\d]", "", price_text)
    return int(numbers) if numbers else 0


def extract_capacity(name: str) -> int:
    """
    Extract RAM capacity in GB.
    Supports single or kit sizes like 16GB, 8GB, 32GB.
    """
    match = re.search(r"(\d+)\s*GB", name.upper())
    return int(match.group(1)) if match else 0


def extract_ddr_type(name: str) -> str:
    name = name.upper()
    if "DDR5" in name:
        return "DDR5"
    if "DDR4" in name:
        return "DDR4"
    return "Unknown"


def parse_ram_html():
    soup = BeautifulSoup(RAW_RAM_HTML.read_text(encoding="utf-8"), "lxml")

    table = soup.find("table")
    rows = table.find_all("tr")[1:]  # skip header

    ram_list = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 3:
            continue

        raw_name = cols[0].get_text(strip=True)
        raw_price = cols[2].get_text(strip=True)

        ram = {
            "id": raw_name.lower().replace(" ", "_"),
            "name": raw_name,
            "category": "ram",
            "brand": raw_name.split()[0],
            "capacity_gb": extract_capacity(raw_name),
            "ddr_type": extract_ddr_type(raw_name),
            "price_inr": clean_price(raw_price),
            "source": "pcpricetracker",
            "last_updated": str(date.today())
        }

        ram_list.append(ram)

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(ram_list, indent=2), encoding="utf-8")

    print(f"Saved {len(ram_list)} RAM entries to {OUTPUT_JSON}")


if __name__ == "__main__":
    parse_ram_html()
