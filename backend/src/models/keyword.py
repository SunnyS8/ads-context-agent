from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base, TimestampMixin


class Keyword(Base, TimestampMixin):
    """Ключевая фраза кампании."""

    __tablename__ = "keywords"

    id: Mapped[int] = mapped_column(primary_key=True)
    campaign_id: Mapped[int] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE")
    )
    keyword: Mapped[str] = mapped_column(String(255))
    bid: Mapped[float | None] = mapped_column(nullable=True)

    campaign = relationship("Campaign", back_populates="keywords")


class KeywordStatistic(Base):
    """Статистика по ключевой фразе за день."""

    __tablename__ = "keyword_statistics"

    id: Mapped[int] = mapped_column(primary_key=True)
    keyword_id: Mapped[int] = mapped_column(
        ForeignKey("keywords.id", ondelete="CASCADE")
    )
    date: Mapped[str] = mapped_column(String(10))
    impressions: Mapped[int] = mapped_column(default=0)
    clicks: Mapped[int] = mapped_column(default=0)
    spend: Mapped[float] = mapped_column(default=0.0)