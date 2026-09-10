from datetime import date, timedelta

from src.platforms.base import (
    PlatformAdapter,
    PlatformCampaign,
    PlatformStats,
)


class MockAdsProvider(PlatformAdapter):
    """Mock-адаптер для тестов и разработки без реальных API.

    Возвращает заранее подготовленные данные. Чтение работает,
    изменение ставок всегда возвращает True (но не делает ничего).
    """

    def __init__(self, campaigns: list[PlatformCampaign] | None = None) -> None:
        self._campaigns = campaigns or [
            PlatformCampaign(
                external_id="1001",
                name="Ремонт квартир — Поиск",
                status="active",
                daily_budget=3000,
            ),
            PlatformCampaign(
                external_id="1002",
                name="Ремонт квартир — РСЯ",
                status="active",
                daily_budget=2000,
            ),
            PlatformCampaign(
                external_id="2001",
                name="VK — Ремонт",
                status="paused",
                daily_budget=1500,
            ),
        ]

    @property
    def platform_name(self) -> str:
        return "mock"

    async def get_campaigns(self) -> list[PlatformCampaign]:
        """Возвращает тестовый список кампаний."""
        return list(self._campaigns)

    async def get_statistics(
        self,
        date_from: date,
        date_to: date,
    ) -> list[PlatformStats]:
        """Возвращает тестовую статистику за каждый день периода."""
        stats: list[PlatformStats] = []
        days = (date_to - date_from).days + 1
        for campaign in self._campaigns[:2]:
            for offset in range(days):
                day = date_from + timedelta(days=offset)
                impressions = 500 + offset * 10
                clicks = max(1, impressions // 50)
                conversions = 1 if offset % 3 == 0 else 0
                stats.append(
                    PlatformStats(
                        campaign_external_id=campaign.external_id,
                        date=day,
                        impressions=impressions,
                        clicks=clicks,
                        spend=clicks * 120.0,
                        conversions=conversions,
                        revenue=conversions * 2000.0,
                    )
                )
        return stats

    async def get_bid(self, campaign_external_id: str) -> float:
        """Возвращает фиксированную тестовую ставку 120 ₽."""
        return 120.0

    async def set_bid(self, campaign_external_id: str, new_bid: float) -> bool:
        """Заглушка — не изменяет ничего, всегда успех."""
        return True

    async def pause_campaign(self, campaign_external_id: str) -> bool:
        """Заглушка — не изменяет ничего, всегда успех."""
        return True

    async def resume_campaign(self, campaign_external_id: str) -> bool:
        """Заглушка — не изменяет ничего, всегда успех."""
        return True