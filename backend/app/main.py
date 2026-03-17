from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.db.postgres import PostgresManager
from app.db.redis import RedisManager

postgres_manager = PostgresManager()
redis_manager = RedisManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализируем инфраструктурные клиенты один раз на старте приложения.
    await postgres_manager.connect()
    await redis_manager.connect()

    app.state.db_pool = postgres_manager.pool
    app.state.redis = redis_manager.client

    try:
        yield
    finally:
        await redis_manager.disconnect()
        await postgres_manager.disconnect()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/health", tags=["Health"])
async def healthcheck() -> dict:
    return {"status": "ok"}
