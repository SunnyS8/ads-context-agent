from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base, TimestampMixin


class Ad(Base, TimestampMixin):
    """Объявление внутри группы."""

    __tablename__ = "ads"

    id: Mapped[int] = mapped_column(primary_key=True)
    ad_group_id: Mapped[int] = mapped_column(
        ForeignKey("ad_groups.id", ondelete="CASCADE")
    )
    external_id: Mapped[str] = mapped_column(String(128), unique=True)
    title: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(String(512))

    ad_group = relationship("AdGroup", back_populates="ads")