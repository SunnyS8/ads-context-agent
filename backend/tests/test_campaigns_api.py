"""Интеграционные тесты CRUD кампаний через HTTP API."""


async def test_create_and_list_campaign(client):
    payload = {
        "platform": "mock",
        "external_id": "1001",
        "name": "Ремонт квартир — Поиск",
        "status": "active",
        "daily_budget": 3000.0,
        "target_cpl": 800.0,
    }
    resp = await client.post("/api/v1/campaigns", json=payload)
    assert resp.status_code == 201
    body = resp.json()
    assert body["id"] == 1
    assert body["external_id"] == "1001"
    assert body["status"] == "active"

    resp = await client.get("/api/v1/campaigns")
    assert resp.status_code == 200
    campaigns = resp.json()
    assert len(campaigns) == 1
    assert campaigns[0]["name"] == "Ремонт квартир — Поиск"


async def test_get_campaign_not_found(client):
    resp = await client.get("/api/v1/campaigns/999")
    assert resp.status_code == 404


async def test_update_campaign(client):
    resp = await client.post(
        "/api/v1/campaigns",
        json={
            "platform": "mock",
            "external_id": "2001",
            "name": "VK — Ремонт",
            "status": "active",
        },
    )
    campaign_id = resp.json()["id"]

    resp = await client.patch(
        f"/api/v1/campaigns/{campaign_id}",
        json={"status": "paused", "daily_budget": 1500.0},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "paused"
    assert body["daily_budget"] == 1500.0

    resp = await client.patch("/api/v1/campaigns/999", json={"status": "paused"})
    assert resp.status_code == 404