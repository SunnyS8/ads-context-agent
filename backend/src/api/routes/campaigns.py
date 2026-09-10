from fastapi import APIRouter, Depends, HTTPException

from src.api.deps import get_campaign_service
from src.schemas.campaign import CampaignCreate, CampaignRead, CampaignUpdate
from src.services.campaign_service import CampaignService

router = APIRouter()


@router.get("/campaigns", response_model=list[CampaignRead])
async def list_campaigns(
    service: CampaignService = Depends(get_campaign_service),
) -> list[CampaignRead]:
    """Возвращает список кампаний."""
    return await service.list_campaigns()


@router.get("/campaigns/{campaign_id}", response_model=CampaignRead)
async def get_campaign(
    campaign_id: int,
    service: CampaignService = Depends(get_campaign_service),
) -> CampaignRead:
    """Возвращает кампанию по ID."""
    campaign = await service.get_campaign(campaign_id)
    if campaign is None:
        raise HTTPException(status_code=404, detail="Кампания не найдена")
    return campaign


@router.post("/campaigns", response_model=CampaignRead, status_code=201)
async def create_campaign(
    payload: CampaignCreate,
    service: CampaignService = Depends(get_campaign_service),
) -> CampaignRead:
    """Создает новую кампанию."""
    return await service.create_campaign(payload)


@router.patch("/campaigns/{campaign_id}", response_model=CampaignRead)
async def update_campaign(
    campaign_id: int,
    payload: CampaignUpdate,
    service: CampaignService = Depends(get_campaign_service),
) -> CampaignRead:
    """Обновляет кампанию."""
    campaign = await service.update_campaign(campaign_id, payload)
    if campaign is None:
        raise HTTPException(status_code=404, detail="Кампания не найдена")
    return campaign