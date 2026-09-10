from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CampaignBase(BaseModel):
    """Базовые поля кампании."""

    platform: str = Field(default="elama", max_length=32)
    external_id: str = Field(..., max_length=128)
    name: str = Field(..., max_length=255)
    status: str = Field(default="active", max_length=32)
    daily_budget: float | None = None
    target_cpl: float | None = None


class CampaignCreate(CampaignBase):
    """Схема создания кампании."""


class CampaignUpdate(BaseModel):
    """Схема обновления кампании (все поля опциональны)."""

    name: str | None = Field(default=None, max_length=255)
    status: str | None = Field(default=None, max_length=32)
    daily_budget: float | None = None
    target_cpl: float | None = None


class CampaignRead(CampaignBase):
    """Схема чтения кампании."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)