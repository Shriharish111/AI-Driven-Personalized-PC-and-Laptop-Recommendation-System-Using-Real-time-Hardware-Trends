from bs4 import BeautifulSoup
from pathlib import Path
import json
import re
from datetime import date

BASE_DIR = Path(__file__).resolve().parents[3]

SSD_HTML = BASE_DIR / "backend" / "catalog" / "raw" / "ssd_raw.html"
HDD_HTML = BASE_DIR / "backend" / "catalog" / "raw" / "hdd_raw.html"
OUTPUT_JSON = BASE_DIR / "backend" / "catalog" / "processed" / "storage.json"


def clean_price(price_text: str) -> int:
    numbers = re.sub(r"[^\d]", "", price_text)
    return int(numbers) if numbers else 0


def extract_capacity(name: str) -> int:
    """
    Extract capacity in GB.
    Supports TB → converted to GB.
    """
    name = name.upper()

    tb_match = re.search(r"(\d+)\s*TB", name)
    if tb_match:
        return int(tb_match.group(1)) * 1000

    gb_match = re.search(r"(\d+)\s*GB", name)
    if gb_match:
        return int(gb_match.group(1))

    return 0


def extract_interface(name: str, storage_type: str) -> str:
    name = name.upper()

    if storage_type == "SSD":
        if "NVME" in name or "M.2" in name:
            return "NVMe"
        return "SATA"

    return "SATA"


def parse_storage_html(html_path: Path, storage_type: str) -> list:
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "lxml")

    table = soup.find("table")
    rows = table.find_all("tr")[1:]  # skip header

    items = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 3:
            continue

        raw_name = cols[0].get_text(strip=True)
        raw_price = cols[2].get_text(strip=True)

        item = {
            "id": raw_name.lower().replace(" ", "_"),
            "name": raw_name,
            "category": "storage",
            "brand": raw_name.split()[0],
            "type": storage_type,
            "capacity_gb": extract_capacity(raw_name),
            "interface": extract_interface(raw_name, storage_type),
            "price_inr": clean_price(raw_price),
            "source": "pcpricetracker",
            "last_updated": str(date.today())
        }

        items.append(item)

    return items


def parse_storage():
    storage_items = []

    storage_items.extend(parse_storage_html(SSD_HTML, "SSD"))
    storage_items.extend(parse_storage_html(HDD_HTML, "HDD"))

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(storage_items, indent=2), encoding="utf-8")

    print(f"Saved {len(storage_items)} storage devices to {OUTPUT_JSON}")


if __name__ == "__main__":
    parse_storage()
