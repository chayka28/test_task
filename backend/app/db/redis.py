from fastapi import Request
from redis.asyncio import Redis

from app.core.config import settings


class RedisManager:
    def __init__(self) -> None:
        self.client: Redis | None = None

    async def connect(self) -> None:
        # Просим Redis возвращать строки, чтобы не декодировать байты вручную.
        self.client = Redis.from_url(settings.redis_url, decode_responses=True)
        await self.client.ping()

    async def disconnect(self) -> None:
        if self.client is not None:
            await self.client.aclose()
            self.client = None


def get_redis_client(request: Request) -> Redis:
    return request.app.state.redis
