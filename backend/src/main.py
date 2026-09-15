from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.api.routes import campaigns, statistics, recommendations, creatives
from src.scheduler.jobs import create_scheduler


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Старт и остановка планировщика фоновых задач."""
    scheduler = create_scheduler()
    scheduler.start()
    yield
    scheduler.shutdown(wait=False)


def create_app() -> FastAPI:
    """Создает и настраивает FastAPI-приложение."""
    app = FastAPI(
        title="Агент контекстной рекламы",
        version="0.1.0",
        description="API для автоматизации контекстной рекламы (eLama, VK Ads)",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(campaigns.router, prefix="/api/v1", tags=["campaigns"])
    app.include_router(statistics.router, prefix="/api/v1", tags=["statistics"])
    app.include_router(
        recommendations.router, prefix="/api/v1", tags=["recommendations"]
    )
    app.include_router(creatives.router, prefix="/api/v1", tags=["creatives"])

    @app.get("/health", tags=["health"])
    async def health() -> dict:
        """Проверка здоровья сервиса."""
        return {"status": "ok", "dry_run": settings.dry_run}

    return app


app = create_app()