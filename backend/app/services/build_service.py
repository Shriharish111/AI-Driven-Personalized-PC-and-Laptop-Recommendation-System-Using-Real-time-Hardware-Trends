BUDGET_SPLITS = {
    "gaming": {
        "gpu": 0.40,
        "cpu": 0.25,
        "ram": 0.10,
        "storage": 0.10,
        "psu": 0.07,
        "case": 0.05,
        "motherboard": 0.03,
    },
    "default": {
        "cpu": 0.30,
        "gpu": 0.30,
        "ram": 0.15,
        "storage": 0.15,
        "psu": 0.05,
        "case": 0.05,
    }
}

def pick_within_budget(items: list, max_price: int):
    affordable = [i for i in items if i["price_inr"] <= max_price]

    if not affordable:
        return None

    affordable = sorted(affordable, key=lambda x: x["price_inr"])

    chosen = affordable[-1]  # best within slice
    cheaper = affordable[-2] if len(affordable) > 1 else None

    if cheaper:
        chosen["cheaper_option"] = cheaper

    return chosen




def pick_middle(items: list):
    if not items:
        return None
    return items[len(items) // 2]


def pick_cheapest(items: list):
    if not items:
        return None
    return items[0]


def pick_expensive(items: list):
    if not items:
        return None
    return items[-1]


def assemble_build(components: dict, budget: int, use_case: str, strategy: str):
    split = BUDGET_SPLITS.get(use_case, BUDGET_SPLITS["default"])
    build = {}
    total_price = 0

    for part, ratio in split.items():
        allocated_budget = int(budget * ratio)

        selected = pick_within_budget(
            components.get(part, []),
            allocated_budget
        )

        if selected:
            build[part] = selected
            total_price += selected["price_inr"]

    build_data = {
    "strategy": strategy,
    "total_price": total_price,
    "components": build
    }

    # HARD BUDGET ENFORCEMENT (ONLY FOR BEST_VALUE)
    if strategy == "best_value":
        build_data = enforce_budget(build_data, budget)

    return build_data
def enforce_budget(build: dict, budget_max: int):
    """
    Ensure total price does not exceed budget by downgrading GPU first,
    then CPU if needed.
    """
    components = build["components"]
    total = build["total_price"]

    if total <= budget_max:
        return build

    # Try downgrading GPU
    gpu = components.get("gpu")
    if gpu:
        cheaper_gpu = gpu.get("cheaper_option")
        if cheaper_gpu:
            components["gpu"] = cheaper_gpu

    # Recalculate
    new_total = sum(
        part["price_inr"]
        for part in components.values()
        if part
    )

    build["total_price"] = new_total
    return build




def assemble_three_builds(components: dict, budget: int, use_case: str):
    return [
        assemble_build(components, budget, use_case, "best_value"),
        assemble_build(components, int(budget * 1.1), use_case, "best_performance"),
        assemble_build(components, int(budget * 1.2), use_case, "stretch"),
    ]


