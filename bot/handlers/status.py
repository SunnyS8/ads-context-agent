import httpx
import os
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api/v1")


@router.message(Command("status"))
async def cmd_status(message: Message) -> None:
    """Показывает сводку по кампаниям."""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            res = await client.get(f"{BACKEND_URL}/campaigns")
            res.raise_for_status()
            campaigns = res.json()
    except httpx.HTTPError:
        await message.answer("Не удалось получить данные. Бэкенд недоступен.")
        return

    if not campaigns:
        await message.answer("Кампаний пока нет.")
        return

    lines = ["<b>Статус кампаний:</b>\n"]
    for c in campaigns:
        status_text = {
            "active": "🟢 активна",
            "paused": "⏸ на паузе",
            "archived": "🗄 архив",
        }.get(c["status"], c["status"])
        budget = c["daily_budget"] or 0
        lines.append(f"• {c['name']} — {status_text} (бюджет {budget:,.0f} ₽)")

    await message.answer("\n".join(lines))