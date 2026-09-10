from dataclasses import dataclass

from src.services.kpi_service import KpiMetrics


@dataclass
class AnalysisInsight:
    """Наблюдение по кампании для отчета."""

    campaign_name: str
    message: str
    severity: str


class InsightAnalyzer:
    """Построение текстовых инсайтов на базе KPI.

    Работает без LLM: формулирует выводы по правилам,
    чтобы не тратить токены на простые расчеты.
    """

    def analyze_campaign(self, campaign_name: str, metrics: KpiMetrics) -> list[AnalysisInsight]:
        """Формирует инсайты по одной кампании.

        Args:
            campaign_name: Имя кампании.
            metrics: Агрегированные KPI кампании.

        Returns:
            Список наблюдений.
        """
        insights: list[AnalysisInsight] = []
        if metrics.clicks == 0:
            insights.append(
                AnalysisInsight(
                    campaign_name,
                    "Нет кликов за период анализа",
                    "warning",
                )
            )
        if 0 < metrics.clicks < 30:
            insights.append(
                AnalysisInsight(
                    campaign_name,
                    f"Мало данных: {metrics.clicks} кликов",
                    "warning",
                )
            )
        if metrics.cpa > 0 and metrics.cpa > 1500:
            insights.append(
                AnalysisInsight(
                    campaign_name,
                    f"CPA ниже эффективности: {metrics.cpa:.0f} ₽",
                    "danger",
                )
            )
        return insights