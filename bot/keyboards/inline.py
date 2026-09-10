from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def approval_keyboard(recommendation_id: int) -> InlineKeyboardMarkup:
    """Клавиатура подтверждения изменения ставки.

    Args:
        recommendation_id: ID рекомендации для callback-данных.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Да, применить",
                    callback_data=f"approve:{recommendation_id}",
                ),
                InlineKeyboardButton(
                    text="❌ Нет",
                    callback_data=f"reject:{recommendation_id}",
                ),
            ]
        ]
    )