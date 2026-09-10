from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class StatisticBase(BaseModel):
    """Базовые поля статистики."""

    campaign_id: int
    date: date
    impressions: int = Field(default=0, ge=0)
    clicks: int = Field(default=0, ge=0)
    spend: float = Field(default=0.0, ge=0)
    conversions: int = Field(default=0, ge=0)
    revenue: float = Field(default=0.0, ge=0)


class StatisticRead(StatisticBase):
    """Статистика для чтения."""

    id: int

    model_config = ConfigDict(from_attributes=True)