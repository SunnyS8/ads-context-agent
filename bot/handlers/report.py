import httpx
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

BACKEND_URL = "http://localhost:8000/api/v1"


@router.message(Command("report"))
async def cmd_report(message: Message) -> None:
    """Формирует отчет по статистике за последние 7 дней."""
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            res = await client.get(f"{BACKEND_URL}/statistics")
            res.raise_for_status()
            statistics = res.json()
    except httpx.HTTPError:
        await message.answer("Не удалось получить статистику.")
        return

    if not statistics:
        await message.answer("Статистики пока нет.")
        return

    total = {
        "impressions": sum(s["impressions"] for s in statistics),
        "clicks": sum(s["clicks"] for s in statistics),
        "spend": sum(s["spend"] for s in statistics),
        "conversions": sum(s["conversions"] for s in statistics),
    }
    ctr = (
        total["clicks"] / total["impressions"] * 100
        if total["impressions"]
        else 0
    )
    cpc = total["spend"] / total["clicks"] if total["clicks"] else 0
    cpa = (
        total["spend"] / total["conversions"]
        if total["conversions"]
        else 0
    )

    await message.answer(
        "<b>Отчет за 7 дней:</b>\n"
        f"Показы: {total['impressions']:,.0f}\n"
        f"Клики: {total['clicks']:,.0f}\n"
        f"Расход: {total['spend']:,.0f} ₽\n"
        f"Конверсии: {total['conversions']}\n"
        f"CTR: {ctr:.2f}%\n"
        f"CPC: {cpc:.0f} ₽\n"
        f"CPA: {cpa:.0f} ₽"
    )