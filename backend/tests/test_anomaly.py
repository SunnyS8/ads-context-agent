from datetime import date

from src.models.statistic import Statistic
from src.services.anomaly_service import AnomalyService


def make_stats(
    days: int = 7,
    clicks_per_day: int = 10,
    spend_per_day: float = 1200.0,
    conversions_per_day: int = 1,
) -> list[Statistic]:
    """Собирает тестовую дневную статистику."""
    stats = []
    for i in range(days):
        stats.append(
            Statistic(
                campaign_id=1,
                date=date(2026, 3, 1 + i),
                impressions=1000,
                clicks=clicks_per_day,
                spend=spend_per_day,
                conversions=conversions_per_day,
                revenue=0.0,
            )
        )
    return stats


def test_insufficient_data_anomaly():
    service = AnomalyService()
    stats = make_stats(clicks_per_day=3)  # 21 клик за 7 дней
    anomalies = service.analyze(stats, target_cpl=1500.0)
    kinds = {a.kind for a in anomalies}
    assert "insufficient_data" in kinds


def test_no_conversions_anomaly():
    service = AnomalyService()
    stats = make_stats(conversions_per_day=0)  # 70 кликов, 0 конверсий
    anomalies = service.analyze(stats, target_cpl=1500.0)
    kinds = {a.kind for a in anomalies}
    assert "no_conversions" in kinds


def test_cpa_high_anomaly():
    service = AnomalyService()
    # 40 кликов за 4 дня, CPA = 2600 ₽ при целевом 1500 ₽ (+73%)
    stats = make_stats(
        days=4, clicks_per_day=10, spend_per_day=2600.0, conversions_per_day=1
    )
    anomalies = service.analyze(stats, target_cpl=1500.0)
    kinds = {a.kind for a in anomalies}
    assert "cpa_high" in kinds
    assert "no_conversions" not in kinds


def test_no_anomaly_for_good_campaign():
    service = AnomalyService()
    # spend 1500/день, 1 конверсия/день → CPA = 1500 ₽ = целевой KPI
    stats = make_stats(
        days=7, clicks_per_day=10, spend_per_day=1500.0, conversions_per_day=1
    )
    anomalies = service.analyze(stats, target_cpl=1500.0)
    assert anomalies == []