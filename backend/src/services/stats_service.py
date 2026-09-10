import logging
from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Campaign, Statistic
from src.platforms.base import PlatformAdapter, PlatformStats
from src.platforms.mock import MockAdsProvider

logger = logging.getLogger(__name__)


class StatsService:
    """Сервис загрузки и хранения статистики."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._adapter: PlatformAdapter = MockAdsProvider()

    async def get_statistics(
        self,
        campaign_id: int | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> list[Statistic]:
        """Возвращает статистику из БД с фильтрами."""
        stmt = select(Statistic).order_by(Statistic.date)
        if campaign_id is not None:
            stmt = stmt.where(Statistic.campaign_id == campaign_id)
        if date_from is not None:
            stmt = stmt.where(Statistic.date >= date_from)
        if date_to is not None:
            stmt = stmt.where(Statistic.date <= date_to)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def sync_from_platforms(self) -> int:
        """Загружает статистику из платформы и сохраняет без дубликатов.

        Returns:
            Количество загруженных записей.
        """
        today = date.today()
        stats: list[PlatformStats] = await self._adapter.get_statistics(
            date_from=today - timedelta(days=6),
            date_to=today,
        )

        campaigns = await self._session.execute(select(Campaign))
        campaign_map = {
            c.external_id: c
            for c in campaigns.scalars().all()
            if c.platform == self._adapter.platform_name
        }

        existing = await self._session.execute(select(Statistic))
        existing_keys = {
            (s.campaign_id, s.date) for s in existing.scalars().all()
        }

        loaded = 0
        for item in stats:
            campaign = campaign_map.get(item.campaign_external_id)
            if campaign is None:
                continue
            key = (campaign.id, item.date)
            if key in existing_keys:
                continue
            self._session.add(
                Statistic(
                    campaign_id=campaign.id,
                    date=item.date,
                    impressions=item.impressions,
                    clicks=item.clicks,
                    spend=item.spend,
                    conversions=item.conversions,
                    revenue=item.revenue,
                )
            )
            existing_keys.add(key)
            loaded += 1

        await self._session.commit()
        logger.info("Загружено записей статистики: %s", loaded)
        return loaded