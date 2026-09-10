from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base, TimestampMixin


class Campaign(Base, TimestampMixin):
    """Рекламная кампания."""

    __tablename__ = "campaigns"

    id: Mapped[int] = mapped_column(primary_key=True)
    platform: Mapped[str] = mapped_column(String(32))
    external_id: Mapped[str] = mapped_column(String(128), unique=True)
    name: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(32), default="active")
    daily_budget: Mapped[float | None] = mapped_column(Float, nullable=True)
    target_cpl: Mapped[float | None] = mapped_column(Float, nullable=True)

    statistics = relationship("Statistic", back_populates="campaign")
    recommendations = relationship(
        "Recommendation", back_populates="campaign"
    )
    keywords = relationship("Keyword", back_populates="campaign")