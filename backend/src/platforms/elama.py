import logging
from datetime import date

import httpx

from src.config import settings
from src.platforms.base import (
    PlatformAdapter,
    PlatformCampaign,
    PlatformStats,
)

logger = logging.getLogger(__name__)


class ElamaAdapter(PlatformAdapter):
    """Адаптер eLama API — основной прослой для Яндекс.Директ.

    Args:
        token: API-токен eLama.
        base_url: Базовый URL API eLama.
    """

    def __init__(
        self,
        token: str | None = None,
        base_url: str | None = None,
    ) -> None:
        self._token = token or settings.elama_api_token
        self._base_url = base_url or settings.elama_base_url

    @property
    def platform_name(self) -> str:
        return "elama"

    async def get_campaigns(self) -> list[PlatformCampaign]:
        """Возвращает список кампаний Яндекс.Директ через eLama."""
        # TODO: реализовать запрос eLama /v1/direct/campaigns
        raise NotImplementedError("Метод пока не реализован")

    async def get_statistics(
        self,
        date_from: date,
        date_to: date,
    ) -> list[PlatformStats]:
        """Возвращает агрегированную статистику через eLama."""
        # TODO: реализовать Aggregated Reports eLama
        raise NotImplementedError("Метод пока не реализован")

    async def get_bid(self, campaign_external_id: str) -> float:
        """Возвращает текущую ставку кампании."""
        # TODO: реализовать запрос текущей ставки
        raise NotImplementedError("Метод пока не реализован")

    async def set_bid(self, campaign_external_id: str, new_bid: float) -> bool:
        """Изменяет ставку кампании."""
        # TODO: реализовать изменение ставки через eLama
        raise NotImplementedError("Метод пока не реализован")

    async def pause_campaign(self, campaign_external_id: str) -> bool:
        """Приостанавливает кампанию."""
        # TODO: реализовать паузу кампании
        raise NotImplementedError("Метод пока не реализован")

    async def resume_campaign(self, campaign_external_id: str) -> bool:
        """Возобновляет кампанию."""
        # TODO: реализовать возобновление кампании
        raise NotImplementedError("Метод пока не реализован")