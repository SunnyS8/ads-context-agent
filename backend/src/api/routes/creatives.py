from fastapi import APIRouter, Depends, HTTPException

from src.api.deps import get_creative_service
from src.schemas.creative import CreativeCreate, CreativeRead
from src.services.creative_service import CreativeService

router = APIRouter()


@router.post("/creatives/generate", response_model=CreativeRead)
async def generate_creative(
    payload: CreativeCreate,
    service: CreativeService = Depends(get_creative_service),
) -> CreativeRead:
    """Генерирует текст рекламного объявления через LLM."""
    try:
        return await service.generate(payload)
    except Exception as exc:
        raise HTTPException(
            status_code=502, detail=f"Ошибка генерации: {exc}"
        ) from exc