from datetime import date

from sqlalchemy import Date, Integer, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class Statistic(Base):
    """Статистика кампании за день."""

    __tablename__ = "statistics"
    __table_args__ = (
        UniqueConstraint(
            "campaign_id", "date", name="uq_campaign_date"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    campaign_id: Mapped[int] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE")
    )
    date: Mapped[date] = mapped_column(Date)

    impressions: Mapped[int] = mapped_column(Integer, default=0)
    clicks: Mapped[int] = mapped_column(Integer, default=0)
    spend: Mapped[float] = mapped_column(Float, default=0.0)
    conversions: Mapped[int] = mapped_column(Integer, default=0)
    revenue: Mapped[float] = mapped_column(Float, default=0.0)

    campaign = relationship("Campaign", back_populates="statistics")