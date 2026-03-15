from fastapi import APIRouter, Depends, Response, status

from app.dependencies.services import get_user_service
from app.schemas.user import TokenResponse, UserCreate, UserOut, UserUpdate, UserWithToken
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


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
    return await user_service.create_user(name=payload.name)


@router.get(
    "/{user_id}/token",
    response_model=TokenResponse,
    summary="Get token by user id (for testing convenience)",
)
async def issue_token_by_user_id(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
) -> TokenResponse:
    return await user_service.issue_token_by_user_id(user_id=user_id)


@router.patch(
    "/{user_id}",
    response_model=UserOut,
    summary="Update user name",
)
async def update_user_name(
    user_id: int,
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
    user_id: int,
    user_service: UserService = Depends(get_user_service),
) -> Response:
    await user_service.delete_user(user_id=user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
