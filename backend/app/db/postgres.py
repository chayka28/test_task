import asyncpg
from fastapi import Request

from app.core.config import settings


class PostgresManager:
    def __init__(self) -> None:
        self.pool: asyncpg.Pool | None = None

    async def connect(self) -> None:
        # Pool is reused across all requests.
        self.pool = await asyncpg.create_pool(
            dsn=settings.postgres_dsn,
            min_size=settings.postgres_min_pool_size,
            max_size=settings.postgres_max_pool_size,
        )

    async def disconnect(self) -> None:
        if self.pool is not None:
            await self.pool.close()
            self.pool = None


def get_db_pool(request: Request) -> asyncpg.Pool:
    return request.app.state.db_pool
