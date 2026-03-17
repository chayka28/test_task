from fastapi import HTTPException, status
from redis.asyncio import Redis

from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        redis_client: Redis | None = None,
    ) -> None:
        self.user_repository = user_repository
        self.redis_client = redis_client

    async def create_user(
        self,
        name: str,
        email: str,
        password: str,
        avatar_data: str | None = None,
    ) -> dict:
        normalized_name = name.strip()
        normalized_email = email.strip().lower()

        existing_user = await self.user_repository.get_auth_payload_by_email(email=normalized_email)
        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists.",
            )

        user = await self.user_repository.create_user(
            name=normalized_name,
            email=normalized_email,
            password_hash=hash_password(password),
            avatar_data=avatar_data,
        )
        token = create_access_token(user_id=user["id"])
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": user,
        }

    async def authenticate_user(self, email: str, password: str) -> dict:
        normalized_email = email.strip().lower()
        auth_user = await self.user_repository.get_auth_payload_by_email(email=normalized_email)
        if auth_user is None or not verify_password(password=password, password_hash=auth_user.get("password_hash")):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        user = await self.user_repository.get_by_id(user_id=auth_user["id"])
        token = create_access_token(user_id=auth_user["id"])
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": user,
        }

    async def issue_token_by_user_id(self, user_id: int) -> dict:
        # Отдельная точка входа из ТЗ для ручного тестирования.
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

    async def get_or_create_demo_user(self, name: str = "Trendsee Open Feed") -> dict:
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

    async def update_user_profile(
        self,
        user_id: int,
        name: str | None = None,
        avatar_data: str | None = None,
    ) -> dict:
        user = await self.user_repository.update_profile(
            user_id=user_id,
            name=name,
            avatar_data=avatar_data,
        )
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
            # Держим кэш согласованным после удаления пользователя.
            await self.redis_client.delete(f"user_posts:{user_id}")
