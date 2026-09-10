import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = logging.getLogger(__name__)


def create_scheduler() -> AsyncIOScheduler:
    """Создает планировщик с задачами из расписания.

    Расписание MVP:
    - 08:00 загрузка статистики
    - 08:15 расчет KPI и поиск аномалий
    - 08:35 формирование рекомендаций
    - 09:00 отправка отчета (в разработке)
    """
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

    scheduler.add_job(
        sync_statistics_job,
        trigger="cron",
        hour=8,
        minute=0,
        id="sync_statistics",
        replace_existing=True,
    )
    scheduler.add_job(
        generate_recommendations_job,
        trigger="cron",
        hour=8,
        minute=35,
        id="generate_recommendations",
        replace_existing=True,
    )
    logger.info("Планировщик создан")
    return scheduler


async def sync_statistics_job() -> None:
    """Загружает статистику из всех платформ."""
    from src.database.session import async_session
    from src.services.stats_service import StatsService

    async with async_session() as session:
        service = StatsService(session)
        count = await service.sync_from_platforms()
        logger.info("Планировщик: загружено %d записей статистики", count)


async def generate_recommendations_job() -> None:
    """Генерирует рекомендации по текущей статистике."""
    from src.database.session import async_session
    from src.services.recommendation_service import RecommendationService

    async with async_session() as session:
        service = RecommendationService(session)
        count = await service.generate_recommendations()
        logger.info("Планировщик: создано %d рекомендаций", count)