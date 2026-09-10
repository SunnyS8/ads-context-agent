from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Campaign, Recommendation, RecommendationStatus, Statistic
from src.config import settings
from src.services.anomaly_service import AnomalyService
from src.services.kpi_service import summarize_stats


class RecommendationService:
    """Сервис формирования рекомендаций по оптимизации."""

    MAX_BID_CHANGE_PERCENT = 15
    MAX_BID = 250.0

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._anomaly_service = AnomalyService()

    async def list_recommendations(self) -> list[Recommendation]:
        """Возвращает активные рекомендации."""
        stmt = (
            select(Recommendation)
            .where(
                Recommendation.status.in_(
                    [RecommendationStatus.PENDING, RecommendationStatus.APPROVED]
                )
            )
            .order_by(Recommendation.id.desc())
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def generate_recommendations(self) -> int:
        """Генерирует рекомендации по текущей статистике всех кампаний.

        Returns:
            Количество созданных рекомендаций.
        """
        campaigns = await self._session.execute(select(Campaign))
        created = 0
        for campaign in campaigns.scalars().all():
            stats = await self._session.execute(
                select(Statistic).where(
                    Statistic.campaign_id == campaign.id
                )
            )
            daily_stats = list(stats.scalars().all())
            if not daily_stats:
                continue

            metrics = summarize_stats(daily_stats)
            target_cpl = campaign.target_cpl or 1500.0
            anomalies = self._anomaly_service.analyze(
                daily_stats, target_cpl, campaign.daily_budget
            )

            for anomaly in anomalies:
                if not self._to_recommendation(anomaly.kind, metrics, target_cpl):
                    continue
                old_bid = 120.0  # TODO: получить реальную ставку через адаптер
                new_bid, action = self._suggest_bid_change(
                    anomaly.kind, anomaly.severity, old_bid
                )
                chapter = {
                    "action": action,
                    "old_value": old_bid,
                    "new_value": new_bid,
                    "reason": anomaly.message,
                }
                if anomaly.kind == "insufficient_data":
                    chapter = {
                        "action": "monitor",
                        "old_value": None,
                        "new_value": None,
                        "reason": anomaly.message,
                    }
                if anomaly.kind == "no_conversions":
                    chapter = {
                        "action": "pause_for_review",
                        "old_value": None,
                        "new_value": None,
                        "reason": anomaly.message,
                    }

                self._session.add(
                    Recommendation(
                        campaign_id=campaign.id,
                        **chapter,
                        status=RecommendationStatus.PENDING,
                    )
                )
                created += 1

        await self._session.commit()
        return created

    def _to_recommendation(
        self, kind: str, metrics: object, target_cpl: float
    ) -> bool:
        """Определяет, требует ли аномалия рекомендации."""
        if kind == "budget_exceeded":
            return False  # бюджет не меняем автоматически
        if kind == "insufficient_data":
            return True
        if kind == "no_conversions":
            return metrics.clicks >= self._anomaly_service.MIN_CLICKS_THRESHOLD
        return True

    def _suggest_bid_change(
        self, kind: str, severity: str, old_bid: float
    ) -> tuple[float, str]:
        """Предлагает новое значение ставки и действие.

        Returns:
            Кортеж (new_bid, action).
        """
        if kind == "cpa_high" or severity == "critical":
            change = old_bid * self.MAX_BID_CHANGE_PERCENT / 100
            new_bid = max(1.0, old_bid - change)
            return round(new_bid, 2), "decrease_bid"
        if kind == "cpa_low":
            change = old_bid * 10 / 100
            new_bid = min(self.MAX_BID, old_bid + change)
            return round(new_bid, 2), "increase_bid"
        return old_bid, "monitor"