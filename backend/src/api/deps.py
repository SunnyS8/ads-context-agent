from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session import get_session
from src.services.campaign_service import CampaignService
from src.services.creative_service import CreativeService
from src.services.recommendation_service import RecommendationService
from src.services.stats_service import StatsService

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_campaign_service(
    session: SessionDep,
) -> CampaignService:
    """Фабрика сервиса кампаний."""
    return CampaignService(session)


async def get_stats_service(
    session: SessionDep,
) -> StatsService:
    """Фабрика сервиса статистики."""
    return StatsService(session)


async def get_recommendation_service(
    session: SessionDep,
) -> RecommendationService:
    """Фабрика сервиса рекомендаций."""
    return RecommendationService(session)


async def get_creative_service(
    session: SessionDep,
) -> CreativeService:
    """Фабрика сервиса креативов."""
    return CreativeService(session)