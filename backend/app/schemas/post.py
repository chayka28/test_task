from datetime import datetime

from pydantic import BaseModel, Field, model_validator


class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200, examples=["My first post"])
    text: str = Field(min_length=1, max_length=5000, examples=["Hello Trendsee!"])


class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    text: str | None = Field(default=None, min_length=1, max_length=5000)

    @model_validator(mode="after")
    def validate_payload(self) -> "PostUpdate":
        # PATCH requires at least one field to update.
        if self.title is None and self.text is None:
            raise ValueError("At least one field must be provided: title or text.")
        return self


class PostOut(BaseModel):
    id: int
    user_id: int
    title: str
    text: str
    created_at: datetime
    updated_at: datetime
