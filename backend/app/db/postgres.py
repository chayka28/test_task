import asyncpg
from fastapi import Request

from app.core.config import settings


USER_TABLE_MIGRATION_SQL = """
ALTER TABLE users ADD COLUMN IF NOT EXISTS email VARCHAR(255);
ALTER TABLE users ADD COLUMN IF NOT EXISTS password_hash TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS avatar_data TEXT;
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email_unique
    ON users (email)
    WHERE email IS NOT NULL;
"""


class PostgresManager:
    def __init__(self) -> None:
        self.pool: asyncpg.Pool | None = None

    async def connect(self) -> None:
        # Один пул соединений используется всеми запросами приложения.
        self.pool = await asyncpg.create_pool(
            dsn=settings.postgres_dsn,
            min_size=settings.postgres_min_pool_size,
            max_size=settings.postgres_max_pool_size,
        )
        await self.apply_runtime_migrations()

    async def apply_runtime_migrations(self) -> None:
        if self.pool is None:
            return

        async with self.pool.acquire() as connection:
            # Небольшая миграция на старте, чтобы docker compose поднимался даже на старом volume.
            await connection.execute(USER_TABLE_MIGRATION_SQL)

    async def disconnect(self) -> None:
        if self.pool is not None:
            await self.pool.close()
            self.pool = None


def get_db_pool(request: Request) -> asyncpg.Pool:
    return request.app.state.db_pool
