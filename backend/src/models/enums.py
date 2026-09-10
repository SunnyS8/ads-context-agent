from enum import Enum

from sqlalchemy import Enum as SqlEnum


class RecommendationStatus(str, Enum):
    """Статусы рекомендаций."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    APPLIED = "applied"
    EXPIRED = "expired"


RecommendationStatusType = SqlEnum(
    RecommendationStatus, name="recommendation_status"
)