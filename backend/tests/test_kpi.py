from datetime import date

import pytest

from src.platforms.mock import MockAdsProvider
from src.services.kpi_service import (
    calculate_cpa,
    calculate_cpc,
    calculate_ctr,
    calculate_drr,
    calculate_roas,
    summarize_stats,
)


def test_calculate_ctr():
    assert calculate_ctr(1000, 100) == pytest.approx(10.0)


def test_calculate_ctr_zero_impressions():
    assert calculate_ctr(0, 0) == 0.0


def test_calculate_cpc():
    assert calculate_cpc(1000, 10) == pytest.approx(100.0)


def test_calculate_cpc_zero_clicks():
    assert calculate_cpc(1000, 0) == 0.0


def test_calculate_cpa():
    assert calculate_cpa(3000, 2) == pytest.approx(1500.0)


def test_calculate_cpa_zero_conversions():
    assert calculate_cpa(3000, 0) == 0.0


def test_calculate_drr():
    assert calculate_drr(3000, 10000) == pytest.approx(30.0)


def test_calculate_drr_zero_revenue():
    assert calculate_drr(3000, 0) == 0.0


def test_calculate_roas():
    assert calculate_roas(10000, 1000) == pytest.approx(10.0)


@pytest.mark.asyncio
async def test_mock_get_campaigns():
    provider = MockAdsProvider()
    campaigns = await provider.get_campaigns()
    assert len(campaigns) == 3
    assert campaigns[0].name == "Ремонт квартир — Поиск"


@pytest.mark.asyncio
async def test_mock_get_statistics():
    provider = MockAdsProvider()
    stats = await provider.get_statistics(
        date_from=date(2026, 1, 1), date_to=date(2026, 1, 3)
    )
    assert len(stats) == 6  # 2 кампании x 3 дня


def test_summarize_stats():
    provider = MockAdsProvider().__class__
    stats = []
    from src.platforms.base import PlatformStats

    stats.append(
        PlatformStats(
            campaign_external_id="1",
            date=date(2026, 1, 1),
            impressions=1000,
            clicks=100,
            spend=1500.0,
            conversions=1,
            revenue=3000.0,
        )
    )
    stats.append(
        PlatformStats(
            campaign_external_id="1",
            date=date(2026, 1, 2),
            impressions=2000,
            clicks=200,
            spend=3000.0,
            conversions=1,
            revenue=6000.0,
        )
    )
    metrics = summarize_stats(stats)
    assert metrics.impressions == 3000
    assert metrics.clicks == 300
    assert metrics.spend == 4500.0
    assert metrics.cpa == pytest.approx(2250.0)