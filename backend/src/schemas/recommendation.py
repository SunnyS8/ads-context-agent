from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class RecommendationBase(BaseModel):
    """Базовые поля рекомендации."""

    campaign_id: int
    action: str = Field(..., max_length=64)
    old_value: float | None = None
    new_value: float | None = None
    reason: str
    status: Literal[
        "pending", "approved", "rejected", "applied", "expired"
    ] = "pending"


class RecommendationRead(RecommendationBase):
    """Рекомендация для чтения."""

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)