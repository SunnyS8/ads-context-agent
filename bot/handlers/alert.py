import httpx
import os
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api/v1")


@router.message(Command("alerts"))
async def cmd_alerts(message: Message) -> None:
    """Показывает последние рекомендации и аномалии."""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            res = await client.get(f"{BACKEND_URL}/recommendations")
            res.raise_for_status()
        recommendations = res.json()
    except httpx.HTTPError:
        await message.answer("Не удалось получить рекомендации.")
        return

    if not recommendations:
        await message.answer("Активных рекомендаций нет.")
        return

    lines = ["<b>Рекомендации:</b>\n"]
    for r in recommendations[:5]:
        lines.append(
            f"• Кампания #{r['campaign_id']}: {r['reason']} "
            f"(статус: {r['status']})"
        )
    await message.answer("\n".join(lines))