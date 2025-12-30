from typing import Dict, Optional

from app.core.rag import retrieve_relevant_parts
from app.core.gemini import generate_text
from app.services.catalog_service import get_pc_component_candidates


def apply_difficulty_rules(
    difficulty: str,
    components: Dict[str, list],
    preferences: Optional[Dict[str, str]]
) -> Dict[str, list]:
    """
    Modify component candidates based on user difficulty level.
    """

    if difficulty == "beginner":
        # Beginner: system decides everything
        return components

    if difficulty == "intermediate":
        # Intermediate: soft constraints on major components
        if preferences:
            for part in ["cpu", "gpu", "ram", "storage"]:
                if part in preferences and part in components:
                    filtered = [
                        c for c in components[part]
                        if preferences[part].lower() in c.get("name", "").lower()
                    ]
                    if filtered:
                        components[part] = filtered
        return components

    if difficulty == "expert":
        # Expert: strict constraints
        if preferences:
            for part, value in preferences.items():
                if part in components:
                    components[part] = [
                        c for c in components[part]
                        if value.lower() in c.get("name", "").lower()
                    ]
        return components

    return components


def generate_pc_recommendation(
    difficulty: str,
    user_intent: str,
    budget_min: int,
    budget_max: int,
    preferences: Optional[Dict[str, str]] = None
) -> Dict:
    """
    Generate PC recommendation context and explanation.
    NOTE: This service does NOT assemble builds.
    """

    # 1. Load catalog under budget
    components = get_pc_component_candidates(budget_max=budget_max)

    # 2. Apply difficulty rules
    components = apply_difficulty_rules(
        difficulty=difficulty,
        components=components,
        preferences=preferences
    )

    # 3. Retrieve RAG knowledge (safe)
    try:
        retrieved_parts = retrieve_relevant_parts(user_intent, top_k=5)
    except Exception:
        retrieved_parts = []

    context_block = "\n".join(f"- {part}" for part in retrieved_parts)

    # 4. Generate explanation (safe Gemini)
    prompt = f"""
You are a PC hardware expert.

Use the following hardware knowledge to explain the recommendation.

HARDWARE KNOWLEDGE:
{context_block}

USER REQUIREMENT:
{user_intent}

TASK:
Explain why the recommended build fits the requirement.
Mention trade-offs and expected performance.
"""

    try:
        explanation = generate_text(prompt)
    except Exception:
        explanation = (
            "This recommendation is generated based on your budget, "
            "use case, and current hardware suitability."
        )

    return {
        "filtered_components": components,
        "rag_context": retrieved_parts,
        "explanation": explanation
    }
