from fastapi import Depends
from redis.asyncio import Redis

from app.db.postgres import get_db_pool
from app.db.redis import get_redis_client
from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository
from app.services.post_service import PostService
from app.services.user_service import UserService


def get_user_repository(pool=Depends(get_db_pool)) -> UserRepository:
    # Провайдер DI: HTTP-слой не создает репозитории вручную.
    return UserRepository(pool=pool)


def get_post_repository(pool=Depends(get_db_pool)) -> PostRepository:
    return PostRepository(pool=pool)


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    redis_client: Redis = Depends(get_redis_client),
) -> UserService:
    return UserService(
        user_repository=user_repository,
        redis_client=redis_client,
    )


def get_post_service(
    post_repository: PostRepository = Depends(get_post_repository),
    redis_client: Redis = Depends(get_redis_client),
) -> PostService:
    return PostService(
        post_repository=post_repository,
        redis_client=redis_client,
    )
