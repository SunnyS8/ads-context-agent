import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import select

from src.database.session import async_session
from src.models import Campaign

MOCK_CAMPAIGNS = [
    dict(
        platform="mock",
        external_id="1001",
        name="Ремонт квартир — Поиск",
        status="active",
        daily_budget=3000.0,
        target_cpl=800.0,
    ),
    dict(
        platform="mock",
        external_id="1002",
        name="Ремонт квартир — РСЯ",
        status="active",
        daily_budget=2000.0,
        target_cpl=1000.0,
    ),
    dict(
        platform="mock",
        external_id="2001",
        name="VK — Ремонт",
        status="paused",
        daily_budget=1500.0,
        target_cpl=900.0,
    ),
]


async def seed() -> None:
    async with async_session() as session:
        existing = await session.execute(
            select(Campaign.external_id).where(Campaign.platform == "mock")
        )
        existing_ids = set(existing.scalars().all())
        created = 0
        for item in MOCK_CAMPAIGNS:
            if item["external_id"] in existing_ids:
                print(f"skip {item['external_id']} (уже есть)")
                continue
            session.add(Campaign(**item))
            created += 1
        await session.commit()
        print(f"Создано кампаний: {created}")


if __name__ == "__main__":
    asyncio.run(seed())