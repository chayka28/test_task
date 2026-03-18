from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.db.postgres import PostgresManager
from app.db.redis import RedisManager
from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository
from app.utils.showcase_seed import ensure_showcase_feed

postgres_manager = PostgresManager()
redis_manager = RedisManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализируем инфраструктурные клиенты один раз на старте приложения.
    await postgres_manager.connect()
    await redis_manager.connect()

    app.state.db_pool = postgres_manager.pool
    app.state.redis = redis_manager.client
    await ensure_showcase_feed(
        user_repository=UserRepository(pool=postgres_manager.pool),
        post_repository=PostRepository(pool=postgres_manager.pool),
    )

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
