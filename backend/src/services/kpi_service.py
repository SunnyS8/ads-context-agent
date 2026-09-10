from datetime import date
from dataclasses import dataclass

from src.platforms.base import PlatformStats


def calculate_ctr(impressions: int, clicks: int) -> float:
    """Рассчитывает CTR (%)."""
    if impressions == 0:
        return 0.0
    return clicks / impressions * 100


def calculate_cpc(spend: float, clicks: int) -> float:
    """Рассчитывает стоимость клика (CPC)."""
    if clicks == 0:
        return 0.0
    return spend / clicks


def calculate_cpa(spend: float, conversions: int) -> float:
    """Рассчитывает стоимость цели/конверсии (CPA)."""
    if conversions == 0:
        return 0.0
    return spend / conversions


def calculate_cpl(spend: float, leads: int) -> float:
    """Рассчитывает стоимость лида (CPL)."""
    if leads == 0:
        return 0.0
    return spend / leads


def calculate_drr(spend: float, revenue: float) -> float:
    """Рассчитывает долю рекламных расходов (ДРР, %)."""
    if revenue == 0:
        return 0.0
    return spend / revenue * 100


def calculate_roas(revenue: float, spend: float) -> float:
    """Рассчитывает возврат на рекламные расходы (ROAS)."""
    if spend == 0:
        return 0.0
    return revenue / spend


@dataclass
class KpiMetrics:
    """Набор показателей кампании за период."""

    impressions: int = 0
    clicks: int = 0
    spend: float = 0.0
    conversions: int = 0
    revenue: float = 0.0

    @property
    def ctr(self) -> float:
        return calculate_ctr(self.impressions, self.clicks)

    @property
    def cpc(self) -> float:
        return calculate_cpc(self.spend, self.clicks)

    @property
    def cpa(self) -> float:
        return calculate_cpa(self.spend, self.conversions)

    @property
    def cpl(self) -> float:
        return calculate_cpl(self.spend, self.conversions)

    @property
    def drr(self) -> float:
        return calculate_drr(self.spend, self.revenue)

    @property
    def roas(self) -> float:
        return calculate_roas(self.revenue, self.spend)


def summarize_stats(stats: list[PlatformStats]) -> KpiMetrics:
    """Сворачивает дневную статистику в агрегированные KPI.

    Args:
        stats: Дневная статистика кампании (PlatformStats или ORM Statistic).

    Returns:
        KpiMetrics с суммарными показателями за период.
    """
    metrics = KpiMetrics()
    for item in stats:
        metrics.impressions += item.impressions
        metrics.clicks += item.clicks
        metrics.spend += item.spend
        metrics.conversions += item.conversions
        metrics.revenue += item.revenue
    return metrics