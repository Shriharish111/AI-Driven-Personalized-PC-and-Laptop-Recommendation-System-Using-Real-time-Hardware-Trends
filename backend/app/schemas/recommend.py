from pydantic import BaseModel, Field
from typing import Optional


class RecommendationRequest(BaseModel):
    # Core flow (required for everyone)
    difficulty: str = Field(..., description="beginner | intermediate | expert")
    category: str = Field(..., description="pc | laptop (pc active)")
    use_case: str = Field(..., description="gaming | editing | developing | aiml")
    budget_min: int = Field(..., ge=0)
    budget_max: int = Field(..., ge=0)

    # Optional preferences (used only for intermediate & expert)
    preferred_cpu: Optional[str] = None
    preferred_gpu: Optional[str] = None
    preferred_ram_gb: Optional[int] = None
    preferred_storage_gb: Optional[int] = None
