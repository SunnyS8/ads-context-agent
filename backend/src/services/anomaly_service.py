from dataclasses import dataclass

from src.services.kpi_service import KpiMetrics, summarize_stats
from src.models.statistic import Statistic


@dataclass
class Anomaly:
    """Обнаруженная аномалия в статистике."""

    kind: str
    severity: str
    message: str


class AnomalyService:
    """Поиск аномалий в статистике кампаний."""

    MIN_CLICKS_THRESHOLD = 30
    SPEND_BUDGET_MULTIPLIER = 2.0

    def analyze(
        self,
        stats: list[Statistic],
        target_cpl: float,
        daily_budget: float | None = None,
    ) -> list[Anomaly]:
        """Анализирует статистику и возвращает список аномалий.

        Args:
            stats: Дневная статистика кампании.
            target_cpl: Целевая стоимость заявки.
            daily_budget: Дневной бюджет (для контроля расхода).

        Returns:
            Список обнаруженных аномалий.
        """
        if not stats:
            return []

        metrics = summarize_stats(stats)
        anomalies: list[Anomaly] = []

        if metrics.clicks < self.MIN_CLICKS_THRESHOLD:
            anomalies.append(
                Anomaly(
                    kind="insufficient_data",
                    severity="warning",
                    message=(
                        f"Мало данных: {metrics.clicks} кликов "
                        f"(минимум {self.MIN_CLICKS_THRESHOLD})"
                    ),
                )
            )

        if target_cpl > 0 and metrics.cpa == 0 and metrics.clicks >= self.MIN_CLICKS_THRESHOLD:
            anomalies.append(
                Anomaly(
                    kind="no_conversions",
                    severity="critical",
                    message=(
                        f"Нет конверсий при расходе "
                        f"{metrics.spend:.0f} ₽ (целевой CPL {target_cpl:.0f} ₽)"
                    ),
                )
            )

        if target_cpl > 0 and metrics.cpa > 0:
            deviation = (metrics.cpa - target_cpl) / target_cpl
            if deviation > 0.30:
                anomalies.append(
                    Anomaly(
                        kind="cpa_high",
                        severity="warning",
                        message=(
                            f"CPA {metrics.cpa:.0f} ₽ выше целевого "
                            f"{target_cpl:.0f} ₽ на {deviation * 100:.0f}%"
                        ),
                    )
                )
            elif deviation < -0.20:
                anomalies.append(
                    Anomaly(
                        kind="cpa_low",
                        severity="info",
                        message=(
                            f"CPA {metrics.cpa:.0f} ₽ ниже целевого "
                            f"{target_cpl:.0f} ₽ на {-deviation * 100:.0f}%"
                        ),
                    )
                )

        if daily_budget and metrics.spend > daily_budget * len(stats):
            anomalies.append(
                Anomaly(
                    kind="budget_exceeded",
                    severity="warning",
                    message=(
                        f"Расход {metrics.spend:.0f} ₽ превышает бюджет "
                        f"{daily_budget * len(stats):.0f} ₽ за период"
                    ),
                )
            )

        return anomalies