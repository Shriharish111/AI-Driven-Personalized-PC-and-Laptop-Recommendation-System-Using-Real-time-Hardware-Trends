from bs4 import BeautifulSoup
from pathlib import Path
import json
import re
from datetime import date

BASE_DIR = Path(__file__).resolve().parents[3]

RAW_CPU_HTML = BASE_DIR / "backend" / "catalog" / "raw" / "cpu_raw.html"
OUTPUT_JSON = BASE_DIR / "backend" / "catalog" / "processed" / "cpu.json"

def clean_price(price_text: str) -> int:
    return int(re.sub(r"[^\d]", "", price_text))

def normalize_cpu(raw_name: str) -> dict:
    name = raw_name.replace("Processor", "").strip()

    if "Intel" in name or "CORE" in name.upper():
        brand = "Intel"
    elif "Ryzen" in name or "AMD" in name.upper():
        brand = "AMD"
    else:
        brand = "Unknown"

    cpu_id = name.lower()
    cpu_id = re.sub(r"[^a-z0-9]+", "_", cpu_id).strip("_")

    return {
        "id": cpu_id,
        "name": name,
        "brand": brand
    }


def parse_cpu_html():
    html = RAW_CPU_HTML.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "lxml")

    table = soup.find("table", id="cpu-table")
    rows = table.tbody.find_all("tr")

    cpu_list = []

    for row in rows:
        name_td = row.find("td", class_="p-name")
        price_a = row.find("td", class_="p-view").find("a")

        if not name_td or not price_a:
            continue

        raw_name = name_td.get_text(strip=True)
        raw_price = price_a.get_text(strip=True)

        normalized = normalize_cpu(raw_name)

        cpu = {
            "id": normalized["id"],
            "name": normalized["name"],
            "category": "cpu",
            "brand": normalized["brand"],
            "price_inr": clean_price(raw_price),
            "source": "pcpricetracker",
            "last_updated": str(date.today())
        }

        cpu_list.append(cpu)

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(cpu_list, indent=2), encoding="utf-8")

    print(f"Saved {len(cpu_list)} CPUs to {OUTPUT_JSON}")


if __name__ == "__main__":
    parse_cpu_html()