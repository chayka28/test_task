from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import decode_access_token
from app.dependencies.services import get_user_service
from app.services.user_service import UserService

bearer_scheme = HTTPBearer(auto_error=True)


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    user_service: UserService = Depends(get_user_service),
) -> int:
    token = credentials.credentials
    user_id = decode_access_token(token=token)
    user = await user_service.get_user_by_id(user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token belongs to a deleted user.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id
