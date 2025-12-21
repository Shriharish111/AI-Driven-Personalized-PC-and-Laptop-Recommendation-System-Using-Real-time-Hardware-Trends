from fastapi import APIRouter
from app.schemas.recommend import RecommendationRequest
from app.services.recommender import generate_pc_recommendation


router = APIRouter(prefix="/recommend", tags=["Recommendation"])

def build_user_intent(request) -> str:
    """
    Convert structured user input into a natural language intent string.
    """
    budget_part = f"with a budget between {int(request.budget_min)} and {int(request.budget_max)}"

    intent = (
        f"{request.difficulty_level.capitalize()} "
        f"{request.use_case} "
        f"{request.device_type.upper()} "
        f"{budget_part}"
    )

    return intent

@router.post("/")
def recommend(request: RecommendationRequest):
    """
    Full recommendation endpoint using RAG + Gemini.
    """
    user_intent = build_user_intent(request)

    recommendation = generate_pc_recommendation(user_intent)

    return {
        "status": "success",
        "recommendation": recommendation
    }


