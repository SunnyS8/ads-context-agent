from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date


@dataclass
class PlatformCampaign:
    """Кампания рекламной платформы."""

    external_id: str
    name: str
    status: str
    daily_budget: float | None = None


@dataclass
class PlatformStats:
    """Статистика кампании за период."""

    campaign_external_id: str
    date: date
    impressions: int
    clicks: int
    spend: float
    conversions: int
    revenue: float


class PlatformAdapter(ABC):
    """Абстрактный интерфейс рекламной платформы."""

    @property
    @abstractmethod
    def platform_name(self) -> str:
        """Имя платформы (elama, vk_ads, mock)."""

    @abstractmethod
    async def get_campaigns(self) -> list[PlatformCampaign]:
        """Возвращает список кампаний."""

    @abstractmethod
    async def get_statistics(
        self,
        date_from: date,
        date_to: date,
    ) -> list[PlatformStats]:
        """Возвращает статистику по всем кампаниям за период."""

    @abstractmethod
    async def get_bid(self, campaign_external_id: str) -> float:
        """Возвращает текущую ставку кампании."""

    @abstractmethod
    async def set_bid(self, campaign_external_id: str, new_bid: float) -> bool:
        """Изменяет ставку кампании."""

    @abstractmethod
    async def pause_campaign(self, campaign_external_id: str) -> bool:
        """Приостанавливает кампанию."""

    @abstractmethod
    async def resume_campaign(self, campaign_external_id: str) -> bool:
        """Возобновляет кампанию."""