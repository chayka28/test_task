from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Response, status

from app.dependencies.auth import get_current_user_id
from app.dependencies.services import get_post_service, get_user_service
from app.schemas.post import PostCreate, PostOut, PostUpdate
from app.services.post_service import PostService
from app.services.user_service import UserService

router = APIRouter(prefix="/posts", tags=["Posts"])
PositivePostId = Annotated[int, Path(ge=1, description="Positive post id")]
PositiveUserId = Annotated[int, Path(ge=1, description="Positive user id")]


@router.post(
    "",
    response_model=PostOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create post (authorized user only)",
)
async def create_post(
    payload: PostCreate,
    current_user_id: int = Depends(get_current_user_id),
    post_service: PostService = Depends(get_post_service),
) -> PostOut:
    return await post_service.create_post(user_id=current_user_id, payload=payload)


@router.patch(
    "/{post_id}",
    response_model=PostOut,
    summary="Update post (author only)",
)
async def update_post(
    post_id: PositivePostId,
    payload: PostUpdate,
    current_user_id: int = Depends(get_current_user_id),
    post_service: PostService = Depends(get_post_service),
) -> PostOut:
    return await post_service.update_post(
        post_id=post_id,
        current_user_id=current_user_id,
        payload=payload,
    )


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete post (author only)",
)
async def delete_post(
    post_id: PositivePostId,
    current_user_id: int = Depends(get_current_user_id),
    post_service: PostService = Depends(get_post_service),
) -> Response:
    await post_service.delete_post(post_id=post_id, current_user_id=current_user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/user/{user_id}",
    response_model=list[PostOut],
    summary="Get all posts of a user (Redis 10m cache, then Postgres + 2s delay)",
)
async def get_posts_by_user(
    user_id: PositiveUserId,
    limit: int = Query(default=10, ge=1, le=50),
    offset: int = Query(default=0, ge=0),
    post_service: PostService = Depends(get_post_service),
) -> list[PostOut]:
    return await post_service.get_posts_by_user(
        user_id=user_id,
        limit=limit,
        offset=offset,
    )


@router.post(
    "/demo-seed",
    response_model=list[PostOut],
    summary="Generate starter posts for the current user",
)
async def seed_demo_posts(
    current_user_id: int = Depends(get_current_user_id),
    post_service: PostService = Depends(get_post_service),
    count: int = Query(default=12, ge=1, le=24),
    append: bool = Query(default=False),
) -> list[PostOut]:
    return await post_service.seed_demo_posts(
        user_id=current_user_id,
        count=count,
        append=append,
    )


@router.post(
    "/demo-seed/public",
    response_model=list[PostOut],
    summary="Generate or extend starter posts for the public feed",
)
async def seed_public_demo_posts(
    count: int = Query(default=12, ge=1, le=24),
    append: bool = Query(default=True),
    post_service: PostService = Depends(get_post_service),
    user_service: UserService = Depends(get_user_service),
) -> list[PostOut]:
    demo_user = await user_service.get_or_create_demo_user()
    return await post_service.seed_demo_posts(
        user_id=demo_user["id"],
        count=count,
        append=append,
    )
