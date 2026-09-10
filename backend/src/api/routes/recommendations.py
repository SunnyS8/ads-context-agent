from fastapi import APIRouter, Depends

from src.api.deps import get_recommendation_service
from src.schemas.recommendation import RecommendationRead
from src.services.recommendation_service import RecommendationService

router = APIRouter()


@router.get("/recommendations", response_model=list[RecommendationRead])
async def list_recommendations(
    service: RecommendationService = Depends(get_recommendation_service),
) -> list[RecommendationRead]:
    """Возвращает список активных рекомендаций."""
    return await service.list_recommendations()


@router.post("/recommendations/generate")
async def generate_recommendations(
    service: RecommendationService = Depends(get_recommendation_service),
) -> dict:
    """Запускает генерацию рекомендаций по текущей статистике."""
    count = await service.generate_recommendations()
    return {"status": "ok", "generated": count}