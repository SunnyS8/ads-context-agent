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
    scheduler.add_job(
        send_daily_report_job,
        trigger="cron",
        hour=9,
        minute=0,
        id="send_daily_report",
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


async def send_daily_report_job() -> None:
    """Формирует и отправляет ежедневный отчёт в Telegram.

    Собирает сводку за последние 7 дней и активные рекомендации,
    затем отправляет их в чат через Telegram Bot API.
    """
    from datetime import date, timedelta

    import httpx

    from src.config import settings
    from src.database.session import async_session, select
    from src.models import Campaign, Recommendation, RecommendationStatus, Statistic

    if not settings.telegram_bot_token or not settings.telegram_chat_id:
        logger.warning("Планировщик: не заданы TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID, отчёт пропущен")
        return

    date_from = date.today() - timedelta(days=7)
    async with async_session() as session:
        rows = (
            await session.execute(
                select(Statistic)
                .join(Campaign, Campaign.id == Statistic.campaign_id)
                .where(Statistic.date >= date_from)
            )
        ).scalars().all()

        recs = (
            await session.execute(
                select(Recommendation).where(
                    Recommendation.status == RecommendationStatus.PENDING
                )
            )
        ).scalars().all()

    total_impressions = sum(s.impressions for s in rows)
    total_clicks = sum(s.clicks for s in rows)
    total_spend = sum(s.spend for s in rows)
    total_conversions = sum(s.conversions for s in rows)

    ctr = total_clicks / total_impressions * 100 if total_impressions else 0
    cpc = total_spend / total_clicks if total_clicks else 0
    cpa = total_spend / total_conversions if total_conversions else 0

    lines = [
        "<b>Отчёт за 7 дней:</b>\n",
        f"Показы: {total_impressions:,.0f}",
        f"Клики: {total_clicks:,.0f}",
        f"Расход: {total_spend:,.0f} ₽",
        f"Конверсии: {total_conversions}",
        f"CTR: {ctr:.2f}%",
        f"CPC: {cpc:.0f} ₽",
        f"CPA: {cpa:.0f} ₽",
    ]

    if recs:
        lines.append("\n<b>Рекомендации:</b>")
        for r in recs[:5]:
            lines.append(f"• Кампания #{r.campaign_id}: {r.reason}")
    else:
        lines.append("\nРекомендаций пока нет.")

    text = "\n".join(lines)

    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.post(
            f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage",
            json={
                "chat_id": settings.telegram_chat_id,
                "text": text,
                "parse_mode": "HTML",
            },
        )
        if resp.status_code != 200:
            logger.warning("Планировщик: Telegram вернул %s: %s", resp.status_code, resp.text)
            return
    logger.info("Планировщик: ежедневный отчёт отправлен")