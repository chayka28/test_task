import asyncio
import json

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from redis.asyncio import Redis

from app.core.config import settings
from app.repositories.post_repository import PostRepository
from app.schemas.post import PostCreate, PostUpdate


class PostService:
    def __init__(self, post_repository: PostRepository, redis_client: Redis) -> None:
        self.post_repository = post_repository
        self.redis_client = redis_client

    @staticmethod
    def _cache_key(user_id: int) -> str:
        return f"user_posts:{user_id}"

    async def _save_posts_to_cache(self, user_id: int, posts: list[dict]) -> None:
        key = self._cache_key(user_id)
        # jsonable_encoder converts datetime values to ISO strings.
        payload = json.dumps(jsonable_encoder(posts))
        await self.redis_client.set(key, payload, ex=settings.cache_ttl_seconds)

    async def _get_posts_from_cache(self, user_id: int) -> list[dict] | None:
        key = self._cache_key(user_id)
        raw_payload = await self.redis_client.get(key)
        if raw_payload is None:
            return None
        return json.loads(raw_payload)

    async def _refresh_user_cache(self, user_id: int) -> None:
        posts = await self.post_repository.get_user_posts(user_id=user_id)
        await self._save_posts_to_cache(user_id=user_id, posts=posts)

    async def create_post(self, user_id: int, payload: PostCreate) -> dict:
        post = await self.post_repository.create_post(
            user_id=user_id,
            title=payload.title,
            text=payload.text,
        )
        await self._refresh_user_cache(user_id=user_id)
        return post

    async def update_post(
        self,
        post_id: int,
        current_user_id: int,
        payload: PostUpdate,
    ) -> dict:
        existing = await self.post_repository.get_by_id(post_id=post_id)
        if existing is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found.",
            )

        if existing["user_id"] != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can edit only your own posts.",
            )

        updated = await self.post_repository.update_post(
            post_id=post_id,
            title=payload.title,
            text=payload.text,
        )
        await self._refresh_user_cache(user_id=current_user_id)
        return updated

    async def delete_post(self, post_id: int, current_user_id: int) -> None:
        existing = await self.post_repository.get_by_id(post_id=post_id)
        if existing is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found.",
            )

        if existing["user_id"] != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can delete only your own posts.",
            )

        await self.post_repository.delete_post(post_id=post_id)
        await self._refresh_user_cache(user_id=current_user_id)

    async def get_posts_by_user(self, user_id: int) -> list[dict]:
        cached_posts = await self._get_posts_from_cache(user_id=user_id)
        if cached_posts is not None:
            return cached_posts

        # Required by task: Postgres path should emulate heavy query.
        await asyncio.sleep(2)
        posts = await self.post_repository.get_user_posts(user_id=user_id)
        await self._save_posts_to_cache(user_id=user_id, posts=posts)
        return posts
