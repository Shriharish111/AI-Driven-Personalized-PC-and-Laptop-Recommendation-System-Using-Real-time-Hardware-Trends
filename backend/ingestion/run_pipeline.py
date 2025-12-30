"""
Catalog ingestion pipeline.

Runs all parsers to convert raw HTML files
into processed JSON catalog files.

Usage:
    python ingestion/run_pipeline.py
"""

from parsers.cpu_parser import parse_cpu_html
from parsers.gpu_parser import parse_gpu_html
from parsers.ram_parser import parse_ram_html
from parsers.motherboard_parser import parse_motherboard_html
from parsers.storage_parser import parse_storage
from parsers.cooler_parser import parse_cooler_html
from parsers.psu_parser import parse_psu_html
from parsers.case_parser import parse_case_html
from parsers.ups_parser import parse_ups_html


def run_pipeline():
    print("Starting catalog ingestion pipeline...\n")

    parse_cpu_html()
    parse_gpu_html()
    parse_ram_html()
    parse_motherboard_html()
    parse_storage()
    parse_cooler_html()
    parse_psu_html()
    parse_case_html()
    parse_ups_html()

    print("\nCatalog ingestion pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()
