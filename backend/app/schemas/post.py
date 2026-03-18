from datetime import datetime

from pydantic import AnyHttpUrl, BaseModel, Field, model_validator


class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200, examples=["My first post"])
    text: str = Field(min_length=1, max_length=5000, examples=["Hello Trendsee!"])
    video_url: AnyHttpUrl | None = None
    poster_url: AnyHttpUrl | None = None
    source_url: AnyHttpUrl | None = None


class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    text: str | None = Field(default=None, min_length=1, max_length=5000)
    video_url: AnyHttpUrl | None = None
    poster_url: AnyHttpUrl | None = None
    source_url: AnyHttpUrl | None = None

    @model_validator(mode="after")
    def validate_payload(self) -> "PostUpdate":
        # Для PATCH хотя бы одно поле должно быть передано.
        if (
            self.title is None
            and self.text is None
            and self.video_url is None
            and self.poster_url is None
            and self.source_url is None
        ):
            raise ValueError("At least one field must be provided.")
        return self


class PostOut(BaseModel):
    id: int
    user_id: int
    user_name: str | None = None
    title: str
    text: str
    video_url: AnyHttpUrl | None = None
    poster_url: AnyHttpUrl | None = None
    source_url: AnyHttpUrl | None = None
    created_at: datetime
    updated_at: datetime
