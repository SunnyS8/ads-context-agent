from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Campaign, Statistic
from src.schemas.campaign import CampaignCreate, CampaignUpdate


class CampaignService:
    """Сервис управления кампаниями."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_campaigns(self) -> list[Campaign]:
        """Возвращает все кампании."""
        result = await self._session.execute(
            select(Campaign).order_by(Campaign.id)
        )
        return list(result.scalars().all())

    async def get_campaign(self, campaign_id: int) -> Campaign | None:
        """Возвращает кампанию по id."""
        return await self._session.get(Campaign, campaign_id)

    async def create_campaign(self, payload: CampaignCreate) -> Campaign:
        """Создает кампанию."""
        campaign = Campaign(**payload.model_dump())
        self._session.add(campaign)
        await self._session.commit()
        await self._session.refresh(campaign)
        return campaign

    async def update_campaign(
        self, campaign_id: int, payload: CampaignUpdate
    ) -> Campaign | None:
        """Обновляет кампанию, если она существует."""
        campaign = await self._session.get(Campaign, campaign_id)
        if campaign is None:
            return None
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(campaign, field, value)
        await self._session.commit()
        await self._session.refresh(campaign)
        return campaign

    async def delete_campaign(self, campaign_id: int) -> bool:
        """Удаляет кампанию."""
        campaign = await self._session.get(Campaign, campaign_id)
        if campaign is None:
            return False
        await self._session.delete(campaign)
        await self._session.commit()
        return True