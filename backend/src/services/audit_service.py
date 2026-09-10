from sqlalchemy.ext.asyncio import AsyncSession

from src.models import AuditLog


class AuditService:
    """Запись всех действий агента в журнал."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def log(
        self,
        action: str,
        payload: dict,
        user: str | None = None,
        platform: str = "unknown",
        campaign_external_id: str | None = None,
        result: str | None = None,
    ) -> None:
        """Записывает действие в audit_log.

        Args:
            action: Название действия (например, set_bid).
            payload: Данные действия (старое/новое значение, причина).
            user: Пользователь, инициировавший действие.
            platform: Платформа (elama, vk_ads).
            campaign_external_id: Внешний ID кампании.
            result: Результат (значение или ошибка).
        """
        record = AuditLog(
            user=user,
            action=action,
            payload=payload,
            platform=platform,
            campaign_external_id=campaign_external_id,
            result=result,
        )
        self._session.add(record)
        await self._session.commit()