from typing import Annotated

from fastapi import APIRouter, Depends, Path, Response, status

from app.dependencies.auth import get_current_user_id
from app.dependencies.services import get_post_service, get_user_service
from app.schemas.user import (
    TokenResponse,
    UserCreate,
    UserLogin,
    UserOut,
    UserProfileUpdate,
    UserUpdate,
    UserWithToken,
)
from app.services.post_service import PostService
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])
PositiveUserId = Annotated[int, Path(ge=1, description="Positive user id")]


@router.get(
    "/demo",
    response_model=UserOut,
    summary="Get or create the public feed user",
)
async def get_demo_user(
    user_service: UserService = Depends(get_user_service),
    post_service: PostService = Depends(get_post_service),
) -> UserOut:
    user = await user_service.get_or_create_demo_user()
    await post_service.seed_demo_posts(user_id=user["id"], count=24, append=False)
    return user


@router.post(
    "",
    response_model=UserWithToken,
    status_code=status.HTTP_201_CREATED,
    summary="Create a user and return JWT token",
)
async def create_user(
    payload: UserCreate,
    user_service: UserService = Depends(get_user_service),
) -> UserWithToken:
    return await user_service.create_user(
        name=payload.name,
        email=payload.email,
        password=payload.password,
        avatar_data=payload.avatar_data,
    )


@router.post(
    "/login",
    response_model=UserWithToken,
    summary="Login by email and password",
)
async def login_user(
    payload: UserLogin,
    user_service: UserService = Depends(get_user_service),
) -> UserWithToken:
    return await user_service.authenticate_user(
        email=payload.email,
        password=payload.password,
    )


@router.get(
    "/me",
    response_model=UserOut,
    summary="Get current user profile",
)
async def get_current_user_profile(
    current_user_id: int = Depends(get_current_user_id),
    user_service: UserService = Depends(get_user_service),
) -> UserOut:
    return await user_service.get_user_by_id(user_id=current_user_id)


@router.patch(
    "/me/profile",
    response_model=UserOut,
    summary="Update current user profile",
)
async def update_current_user_profile(
    payload: UserProfileUpdate,
    current_user_id: int = Depends(get_current_user_id),
    user_service: UserService = Depends(get_user_service),
) -> UserOut:
    return await user_service.update_user_profile(
        user_id=current_user_id,
        name=payload.name,
        avatar_data=payload.avatar_data,
    )


@router.get(
    "/{user_id}/token",
    response_model=TokenResponse,
    summary="Get token by user id (for testing convenience)",
)
async def issue_token_by_user_id(
    user_id: PositiveUserId,
    user_service: UserService = Depends(get_user_service),
) -> TokenResponse:
    return await user_service.issue_token_by_user_id(user_id=user_id)


@router.patch(
    "/{user_id}",
    response_model=UserOut,
    summary="Update user name",
)
async def update_user_name(
    user_id: PositiveUserId,
    payload: UserUpdate,
    user_service: UserService = Depends(get_user_service),
) -> UserOut:
    return await user_service.update_user_name(user_id=user_id, name=payload.name)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
)
async def delete_user(
    user_id: PositiveUserId,
    user_service: UserService = Depends(get_user_service),
) -> Response:
    await user_service.delete_user(user_id=user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
