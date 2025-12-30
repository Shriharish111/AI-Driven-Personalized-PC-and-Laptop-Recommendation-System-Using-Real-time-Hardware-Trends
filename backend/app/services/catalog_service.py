from app.services.catalog_loader import load_catalog


def get_pc_component_candidates(budget_max: int) -> dict:
    """
    Load and filter catalog components under the given budget.
    Pure catalog logic. No other dependencies.
    """
    catalog = load_catalog()

    filtered = {}
    for part, items in catalog.items():
        filtered[part] = [
            item for item in items
            if item.get("price_inr", 0) <= budget_max
        ]

    return filtered
