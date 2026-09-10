from datetime import datetime

from sqlalchemy import String, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base, TimestampMixin


class Creative(Base, TimestampMixin):
    """Сгенерированный креатив (тексты объявлений)."""

    __tablename__ = "creatives"

    id: Mapped[int] = mapped_column(primary_key=True)
    platform: Mapped[str] = mapped_column(String(32), default="elama")
    title: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(Text)
    hint: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source: Mapped[str] = mapped_column(String(32), default="ai")
    status: Mapped[str] = mapped_column(String(32), default="draft")
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))