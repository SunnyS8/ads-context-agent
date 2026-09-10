from enum import Enum

from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base, TimestampMixin
from src.models.enums import RecommendationStatus, RecommendationStatusType


class Recommendation(Base, TimestampMixin):
    """Рекомендация по оптимизации кампании."""

    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(primary_key=True)
    campaign_id: Mapped[int] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE")
    )
    action: Mapped[str] = mapped_column(String(64))
    old_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    new_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    reason: Mapped[str] = mapped_column(Text)
    status: Mapped[RecommendationStatus] = mapped_column(
        RecommendationStatusType,
        default=RecommendationStatus.PENDING,
    )

    campaign = relationship("Campaign", back_populates="recommendations")