from fastapi import APIRouter
from app.schemas.recommend import RecommendationRequest
from app.core.rag import retrieve_relevant_parts
from app.services.catalog_service import get_pc_component_candidates
from app.services.build_service import assemble_three_builds
from app.core.gemini import explain_build
from app.services.recommender import apply_difficulty_rules


router = APIRouter(prefix="/recommend", tags=["Recommendation"])

def build_user_intent(request) -> str:
    """
    Convert structured user input into a clean natural language intent
    for RAG and LLM reasoning.
    """

    difficulty = request.difficulty.capitalize()
    category = request.category.upper()
    use_case = request.use_case.replace("_", " ")

    intent = (
        f"{difficulty} user wants a {use_case} {category} "
        f"with a budget between {request.budget_min} and {request.budget_max} INR."
    )

    return intent

@router.post("/")
def recommend(request: RecommendationRequest):
    try:
        # 1. Build user intent (for RAG + explanation)
        user_intent = build_user_intent(request)

        # 2. Retrieve RAG context (safe)
        try:
            rag_context = retrieve_relevant_parts(user_intent)
        except Exception:
            rag_context = []

        # 3. Load catalog under budget
        catalog_candidates = get_pc_component_candidates(
            budget_max=request.budget_max
        )

        # 4. Apply difficulty rules (Polish 2)
        catalog_candidates = apply_difficulty_rules(
            difficulty=request.difficulty,
            components=catalog_candidates,
            preferences=request.preferences
        )

        # 5. Assemble builds (budget-aware)
        builds = assemble_three_builds(
            catalog_candidates,
            budget=request.budget_max,
            use_case=request.use_case
        )

        # 6. Explain builds (safe Gemini)
        for b in builds:
            try:
                b["explanation"] = explain_build(
                    b, request.use_case
                )
            except Exception:
                b["explanation"] = (
                    "This build is recommended based on your budget "
                    "and selected use case."
                )

        return {
            "status": "success",
            "builds": builds
        }

    except Exception as e:
        return {
            "status": "error",
            "message": "Unable to generate recommendation at this time."
        }
