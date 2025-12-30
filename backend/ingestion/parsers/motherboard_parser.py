from bs4 import BeautifulSoup
from pathlib import Path
import json
import re
from datetime import date

BASE_DIR = Path(__file__).resolve().parents[3]

RAW_MB_HTML = BASE_DIR / "backend" / "catalog" / "raw" / "motherboard_raw.html"
OUTPUT_JSON = BASE_DIR / "backend" / "catalog" / "processed" / "motherboard.json"


def clean_price(price_text: str) -> int:
    numbers = re.sub(r"[^\d]", "", price_text)
    return int(numbers) if numbers else 0


def extract_form_factor(name: str) -> str:
    name = name.upper()
    if "ITX" in name:
        return "Mini-ITX"
    if "M-ATX" in name or "MICRO ATX" in name:
        return "Micro-ATX"
    return "ATX"


def extract_socket(name: str) -> str:
    name = name.upper()
    if "LGA1700" in name:
        return "LGA1700"
    if "AM4" in name:
        return "AM4"
    if "AM5" in name:
        return "AM5"
    return "Unknown"


def parse_motherboard_html():
    soup = BeautifulSoup(RAW_MB_HTML.read_text(encoding="utf-8"), "lxml")

    table = soup.find("table")
    rows = table.find_all("tr")[1:]  # skip header

    boards = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 3:
            continue

        raw_name = cols[0].get_text(strip=True)
        raw_price = cols[2].get_text(strip=True)

        board = {
            "id": raw_name.lower().replace(" ", "_"),
            "name": raw_name,
            "category": "motherboard",
            "brand": raw_name.split()[0],
            "socket": extract_socket(raw_name),
            "form_factor": extract_form_factor(raw_name),
            "price_inr": clean_price(raw_price),
            "source": "pcpricetracker",
            "last_updated": str(date.today())
        }

        boards.append(board)

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(boards, indent=2), encoding="utf-8")

    print(f"Saved {len(boards)} motherboards to {OUTPUT_JSON}")


if __name__ == "__main__":
    parse_motherboard_html()
