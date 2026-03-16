from fastapi import HTTPException, status
from redis.asyncio import Redis

from app.core.security import create_access_token
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        redis_client: Redis | None = None,
    ) -> None:
        self.user_repository = user_repository
        self.redis_client = redis_client

    async def create_user(self, name: str) -> dict:
        # New user immediately gets a token to simplify first interaction with API.
        user = await self.user_repository.create_user(name=name)
        token = create_access_token(user_id=user["id"])
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": user,
        }

    async def issue_token_by_user_id(self, user_id: int) -> dict:
        # Dedicated endpoint from the task for easier manual testing.
        user = await self.user_repository.get_by_id(user_id=user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )
        token = create_access_token(user_id=user["id"])
        return {"access_token": token, "token_type": "bearer"}

    async def get_user_by_id(self, user_id: int) -> dict | None:
        return await self.user_repository.get_by_id(user_id=user_id)

    async def get_or_create_demo_user(self, name: str = "Trendsee Demo") -> dict:
        user = await self.user_repository.get_by_name(name=name)
        if user is not None:
            return user
        return await self.user_repository.create_user(name=name)

    async def update_user_name(self, user_id: int, name: str) -> dict:
        user = await self.user_repository.update_name(user_id=user_id, name=name)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )
        return user

    async def delete_user(self, user_id: int) -> None:
        deleted = await self.user_repository.delete_user(user_id=user_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        if self.redis_client is not None:
            # Keep cache coherent after user removal.
            await self.redis_client.delete(f"user_posts:{user_id}")
