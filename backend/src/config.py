from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import Field

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Настройки приложения из переменных окружения."""

    # eLama
    elama_api_token: str = Field(default="", alias="ELAMA_API_TOKEN")
    elama_base_url: str = Field(
        default="https://api.elama.ru", alias="ELAMA_BASE_URL"
    )

    # VK Ads
    vk_ads_token: str = Field(default="", alias="VK_ADS_TOKEN")
    vk_ads_app_id: str = Field(default="", alias="VK_ADS_APP_ID")

    # OpenAI
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")

    # Telegram
    telegram_bot_token: str = Field(default="", alias="TELEGRAM_BOT_TOKEN")
    telegram_chat_id: str = Field(default="", alias="TELEGRAM_CHAT_ID")

    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/ads_agent",
        alias="DATABASE_URL",
    )

    # Redis
    redis_url: str = Field(default="redis://localhost:6379", alias="REDIS_URL")

    # Режим
    dry_run: bool = Field(default=True, alias="DRY_RUN")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    allowed_origins: str = Field(
        default="http://localhost:3000", alias="ALLOWED_ORIGINS"
    )

    @property
    def cors_origins(self) -> list[str]:
        """Список origins для CORS из строки через запятую."""
        return [
            o.strip() for o in self.allowed_origins.split(",") if o.strip()
        ]

    model_config = {"env_file": str(PROJECT_ROOT / ".env"), "extra": "ignore"}


settings = Settings()
