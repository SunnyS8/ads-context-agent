from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.models import Creative
from src.schemas.creative import CreativeCreate
from src.ai.text_generator import generate_creative_text


class CreativeService:
    """Сервис генерации креативов."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def generate(self, payload: CreativeCreate) -> Creative:
        """Генерирует текст объявления через LLM и сохраняет его."""
        result = await generate_creative_text(
            brand=payload.brand,
            product=payload.product,
            audience=payload.audience,
            offer=payload.offer,
            tone=payload.tone,
        )

        creative = Creative(
            platform=payload.platform,
            title=result["title"],
            body=result["body"],
            hint=result.get("hint"),
            source="ai",
            status="draft",
            generated_at=datetime.now(timezone.utc),
        )
        self._session.add(creative)
        await self._session.commit()
        await self._session.refresh(creative)
        return creative