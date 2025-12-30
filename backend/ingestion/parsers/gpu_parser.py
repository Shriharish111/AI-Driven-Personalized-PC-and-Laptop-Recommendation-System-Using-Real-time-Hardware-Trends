from bs4 import BeautifulSoup
from pathlib import Path
import json
import re
from datetime import date

BASE_DIR = Path(__file__).resolve().parents[3]

RAW_GPU_HTML = BASE_DIR / "backend" / "catalog" / "raw" / "gpu_raw.html"
OUTPUT_JSON = BASE_DIR / "backend" / "catalog" / "processed" / "gpu.json"


def clean_price(price_text: str) -> int:
    numbers = re.sub(r"[^\d]", "", price_text)
    return int(numbers) if numbers else 0


def extract_vram(name: str) -> int:
    match = re.search(r"(\d+)\s*GB", name.upper())
    return int(match.group(1)) if match else 0


def normalize_gpu(raw_name: str) -> dict:
    name = raw_name.replace("Graphic Card", "").strip()

    if "RTX" in name:
        brand = "NVIDIA"
        chipset_match = re.search(r"RTX\s*\d{4}", name)
    elif "RX" in name:
        brand = "AMD"
        chipset_match = re.search(r"RX\s*\d{4}", name)
    else:
        brand = "Unknown"
        chipset_match = None

    chipset = chipset_match.group(0) if chipset_match else "Unknown"

    return {
        "name": name,
        "brand": brand,
        "chipset": chipset,
        "vram_gb": extract_vram(name)
    }


def parse_gpu_html():
    soup = BeautifulSoup(RAW_GPU_HTML.read_text(encoding="utf-8"), "lxml")

    table = soup.find("table")
    rows = table.find_all("tr")[1:]  # skip header

    gpu_list = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 3:
            continue

        raw_name = cols[0].get_text(strip=True)
        raw_price = cols[2].get_text(strip=True)

        normalized = normalize_gpu(raw_name)

        gpu = {
            "id": normalized["name"].lower().replace(" ", "_"),
            "name": normalized["name"],
            "category": "gpu",
            "brand": normalized["brand"],
            "chipset": normalized["chipset"],
            "vram_gb": normalized["vram_gb"],
            "price_inr": clean_price(raw_price),
            "source": "pcpricetracker",
            "last_updated": str(date.today())
        }

        gpu_list.append(gpu)

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(gpu_list, indent=2), encoding="utf-8")

    print(f"Saved {len(gpu_list)} GPUs to {OUTPUT_JSON}")


if __name__ == "__main__":
    parse_gpu_html()
