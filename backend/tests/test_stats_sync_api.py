"""Интеграционные тесты синхронизации статистики и генерации рекомендаций."""

MOCK_CAMPAIGNS = [
    {
        "platform": "mock",
        "external_id": "1001",
        "name": "Ремонт квартир — Поиск",
        "status": "active",
        "daily_budget": 3000.0,
        "target_cpl": 800.0,
    },
    {
        "platform": "mock",
        "external_id": "1002",
        "name": "Ремонт квартир — РСЯ",
        "status": "active",
        "daily_budget": 2000.0,
        "target_cpl": 1000.0,
    },
]


async def _seed_two_campaigns(client):
    for item in MOCK_CAMPAIGNS:
        resp = await client.post("/api/v1/campaigns", json=item)
        assert resp.status_code == 201


async def test_sync_loads_stats_once_and_is_idempotent(client):
    await _seed_two_campaigns(client)

    resp = await client.post("/api/v1/statistics/sync")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["loaded"] == 14  # 2 кампании * 7 дней

    resp = await client.get("/api/v1/statistics")
    assert len(resp.json()) == 14

    resp = await client.post("/api/v1/statistics/sync")
    assert resp.json()["loaded"] == 0  # идемпотентность

    resp = await client.get("/api/v1/statistics")
    assert len(resp.json()) == 14  # дубликатов нет


async def test_statistics_filtered_by_campaign(client):
    await _seed_two_campaigns(client)
    await client.post("/api/v1/statistics/sync")

    resp = await client.get("/api/v1/statistics", params={"campaign_id": 1})
    stats = resp.json()
    assert len(stats) == 7
    assert all(s["campaign_id"] == 1 for s in stats)


async def test_generate_recommendations_after_sync(client):
    await _seed_two_campaigns(client)
    await client.post("/api/v1/statistics/sync")

    resp = await client.post("/api/v1/recommendations/generate")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["generated"] >= 0

    resp = await client.get("/api/v1/recommendations")
    assert resp.status_code == 200
    for rec in resp.json():
        assert rec["campaign_id"] in (1, 2)
        assert rec["status"] in ("pending", "approved")