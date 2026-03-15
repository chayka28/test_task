from datetime import datetime

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100, examples=["Alice"])


class UserUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=100, examples=["Alice Cooper"])


class UserOut(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserWithToken(TokenResponse):
    user: UserOut
