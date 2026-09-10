import logging
from datetime import date

from src.config import settings
from src.platforms.base import (
    PlatformAdapter,
    PlatformCampaign,
    PlatformStats,
)

logger = logging.getLogger(__name__)


class VKAdsAdapter(PlatformAdapter):
    """Адаптер VK Ads (TARGETING) API.

    Args:
        access_token: Токен доступа VK Ads.
        app_id: ID приложения VK.
    """

    def __init__(
        self,
        access_token: str | None = None,
        app_id: str | None = None,
    ) -> None:
        self._access_token = access_token or settings.vk_ads_token
        self._app_id = app_id or settings.vk_ads_app_id

    @property
    def platform_name(self) -> str:
        return "vk_ads"

    async def get_campaigns(self) -> list[PlatformCampaign]:
        """Возвращает список кампаний VK Ads."""
        # TODO: реализовать ads.getCampaigns
        raise NotImplementedError("Метод пока не реализован")

    async def get_statistics(
        self,
        date_from: date,
        date_to: date,
    ) -> list[PlatformStats]:
        """Возвращает статистику VK Ads за период."""
        # TODO: реализовать ads.getStatistics
        raise NotImplementedError("Метод пока не реализован")

    async def get_bid(self, campaign_external_id: str) -> float:
        """Возвращает текущую ставку кампании VK Ads."""
        # TODO: реализовать ads.getCampaigns (Cpc)
        raise NotImplementedError("Метод пока не реализован")

    async def set_bid(self, campaign_external_id: str, new_bid: float) -> bool:
        """Изменяет ставку кампании VK Ads."""
        # TODO: реализовать ads.updateCampaigns
        raise NotImplementedError("Метод пока не реализован")

    async def pause_campaign(self, campaign_external_id: str) -> bool:
        """Приостанавливает кампанию VK Ads."""
        # TODO: реализовать ads.updateCampaigns (status=pause)
        raise NotImplementedError("Метод пока не реализован")

    async def resume_campaign(self, campaign_external_id: str) -> bool:
        """Возобновляет кампанию VK Ads."""
        # TODO: реализовать ads.updateCampaigns (status=resume)
        raise NotImplementedError("Метод пока не реализован")