from datetime import datetime

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100, examples=["Alice"])
    email: str = Field(min_length=5, max_length=255, examples=["alice@example.com"])
    password: str = Field(min_length=8, max_length=255, examples=["strong-password"])
    avatar_data: str | None = Field(default=None)


class UserLogin(BaseModel):
    email: str = Field(min_length=5, max_length=255, examples=["alice@example.com"])
    password: str = Field(min_length=8, max_length=255, examples=["strong-password"])


class UserUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=100, examples=["Alice Cooper"])


class UserProfileUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    avatar_data: str | None = Field(default=None)


class UserOut(BaseModel):
    id: int
    name: str
    email: str | None = None
    avatar_data: str | None = None
    created_at: datetime
    updated_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserWithToken(TokenResponse):
    user: UserOut
