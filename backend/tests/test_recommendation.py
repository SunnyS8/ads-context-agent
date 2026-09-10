import pytest

from src.models import RecommendationStatus
from src.services.kpi_service import summarize_stats
from src.services.recommendation_service import RecommendationService


class FakeSession:
    """Заглушка сессии — не используется реально, только для конструктора."""

    def __init__(self):
        pass


def test_suggest_bid_change_decrease():
    service = RecommendationService(FakeSession())  # type: ignore
    new_bid, action = service._suggest_bid_change("cpa_high", "warning", 120.0)
    assert action == "decrease_bid"
    assert new_bid == pytest.approx(102.0)  # -15%


def test_suggest_bid_change_increase_capped():
    service = RecommendationService(FakeSession())  # type: ignore
    new_bid, action = service._suggest_bid_change("cpa_low", "info", 240.0)
    assert action == "increase_bid"
    assert new_bid == pytest.approx(250.0)  # не выше MAX_BID


def test_to_recommendation_insufficient_data():
    service = RecommendationService(FakeSession())  # type: ignore
    stats = []
    metrics = summarize_stats(stats)
    assert service._to_recommendation("insufficient_data", metrics, 1500.0)