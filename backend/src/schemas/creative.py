from pydantic import BaseModel, ConfigDict, Field


class CreativeCreate(BaseModel):
    """Входные данные для генерации креатива."""

    platform: str = Field(default="elama", max_length=32)
    brand: str = Field(..., max_length=255)
    product: str = Field(..., max_length=512)
    audience: str = Field(default="", max_length=512)
    offer: str = Field(default="", max_length=512)
    tone: str = Field(default="informative", max_length=64)


class CreativeRead(BaseModel):
    """Сгенерированный креатив."""

    title: str
    body: str
    hint: str | None = None
    platform: str

    model_config = ConfigDict(from_attributes=True)