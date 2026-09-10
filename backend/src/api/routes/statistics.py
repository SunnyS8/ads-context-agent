from datetime import date

from fastapi import APIRouter, Depends, Query

from src.api.deps import get_stats_service
from src.schemas.statistic import StatisticRead
from src.services.stats_service import StatsService

router = APIRouter()


@router.get("/statistics", response_model=list[StatisticRead])
async def get_statistics(
    campaign_id: int | None = Query(default=None),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    service: StatsService = Depends(get_stats_service),
) -> list[StatisticRead]:
    """Возвращает статистику по кампаниям за период."""
    return await service.get_statistics(
        campaign_id=campaign_id, date_from=date_from, date_to=date_to
    )


@router.post("/statistics/sync")
async def sync_statistics(
    service: StatsService = Depends(get_stats_service),
) -> dict:
    """Загружает статистику из всех подключенных платформ."""
    result = await service.sync_from_platforms()
    return {"status": "ok", "loaded": result}