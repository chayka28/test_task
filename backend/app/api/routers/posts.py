from fastapi import APIRouter, Depends, Response, status

from app.dependencies.auth import get_current_user_id
from app.dependencies.services import get_post_service
from app.schemas.post import PostCreate, PostOut, PostUpdate
from app.services.post_service import PostService

router = APIRouter(prefix="/posts", tags=["Posts"])


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
    post_id: int,
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
    post_id: int,
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
    user_id: int,
    post_service: PostService = Depends(get_post_service),
) -> list[PostOut]:
    return await post_service.get_posts_by_user(user_id=user_id)
