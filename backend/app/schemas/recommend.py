from typing import Optional
from pydantic import BaseModel, Field
from pydantic import model_validator



class RecommendationRequest(BaseModel):
    # Core user choices
    difficulty_level: str = Field(
        ..., description="beginner, intermediate, or expert"
    )
    device_type: str = Field(
        ..., description="pc or laptop"
    )
    use_case: str = Field(
        ..., description="gaming, editing, developing, ai_ml, etc"
    )

    # Budget constraints
    budget_min: float = Field(
        ..., ge=7000, description="Minimum budget (must be >= 7000)"
    )
    budget_max: float = Field(
        ..., description="Maximum budget"
    )

    

    # Optional preferences (used for intermediate/expert)
    preferred_brand: Optional[str] = None
    gpu_vram: Optional[int] = None          # in GB
    ram_size: Optional[int] = None          # in GB
    storage: Optional[str] = None           # e.g., 512GB SSD
    cpu_preference: Optional[str] = None
    motherboard_preference: Optional[str] = None
    psu_preference: Optional[str] = None

    @model_validator(mode="after")
    def validate_request_logic(self):
        # Budget range validation
        if self.budget_min > self.budget_max:
            raise ValueError("budget_min cannot be greater than budget_max")

        # Difficulty level validation
        allowed_difficulty = {"beginner", "intermediate", "expert"}
        if self.difficulty_level.lower() not in allowed_difficulty:
            raise ValueError(
                "difficulty_level must be beginner, intermediate, or expert"
            )

        # Device type validation
        allowed_devices = {"pc", "laptop"}
        if self.device_type.lower() not in allowed_devices:
            raise ValueError("device_type must be pc or laptop")

        return self

