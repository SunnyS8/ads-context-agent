import json

from src.config import settings

_PROMPT_TEMPLATE = """Ты эксперт по контекстной рекламе Директ и VK Ads.
Сгенерируй текст рекламного объявления.

Бренд: {brand}
Продукт: {product}
Целевая аудитория: {audience}
Оффер (УТП): {offer}
Тон коммуникации: {tone}

Формат ответа строго JSON:
{{"title": "заголовок до 56 символов",
 "body": "текст объявления до 81 символа",
 "hint": "быстрые ссылки/уточнения, если нужно"}}
"""


async def generate_creative_text(
    brand: str,
    product: str,
    audience: str = "",
    offer: str = "",
    tone: str = "informative",
) -> dict:
    """Генерирует текст объявления через OpenAI API.

    Args:
        brand: Название бренда.
        product: Что рекламируем.
        audience: Целевая аудитория.
        offer: Оффер/УТП.
        tone: Тон коммуникации.

    Returns:
        Словарь с ключами title, body, hint.

    Raises:
        RuntimeError: если API недоступен или ответ невалиден.
    """
    prompt = _PROMPT_TEMPLATE.format(
        brand=brand,
        product=product,
        audience=audience or "широкая аудитория",
        offer=offer or "обратитесь за консультацией",
        tone=tone,
    )

    try:
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=settings.openai_api_key)
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
        )
    except Exception as exc:
        raise RuntimeError(f"OpenAI API недоступен: {exc}") from exc

    content = response.choices[0].message.content or ""
    try:
        return json.loads(content)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "Модель вернула невалидный JSON для креатива"
        ) from exc