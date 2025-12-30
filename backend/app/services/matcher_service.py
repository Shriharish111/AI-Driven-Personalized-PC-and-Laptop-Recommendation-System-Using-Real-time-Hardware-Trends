"""
Matcher service

This module reduces catalog candidates using simple,
explainable rule-based logic.
"""


def match_candidates_with_rag(catalog: dict, rag_context: list) -> dict:
    """
    Reduce catalog candidates using simple, safe rules.
    """

    reduced = {}

    # CPU: remove entry-level CPUs
    reduced["cpu"] = [
        cpu for cpu in catalog.get("cpu", [])
        if not any(low in cpu["name"].lower()
                   for low in ["i3", "ryzen 3", "athlon", "pentium"])
    ]

    # GPU: remove very low-end GPUs
    reduced["gpu"] = [
        gpu for gpu in catalog.get("gpu", [])
        if not any(low in gpu["name"].upper()
                   for low in ["GT 710", "GT 730", "GT 1030"])
    ]

    # RAM: prefer 16GB or more
    reduced["ram"] = [
        ram for ram in catalog.get("ram", [])
        if ram.get("capacity_gb", 0) >= 16
    ]

    # Storage: keep only SSDs
    reduced["storage"] = [
        s for s in catalog.get("storage", [])
        if s.get("type", "").upper() == "SSD"
    ]

    return reduced
