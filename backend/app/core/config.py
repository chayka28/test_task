from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Settings are loaded from environment variables.
    # Local runs can use backend/.env (see .env.example).
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Trendsee Feed Service"
    app_version: str = "1.0.0"
    api_prefix: str = "/api/v1"

    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_db: str = "trendsee"
    postgres_user: str = "trendsee"
    postgres_password: str = "trendsee"
    postgres_min_pool_size: int = 1
    postgres_max_pool_size: int = 10

    redis_url: str = "redis://redis:6379/0"
    cache_ttl_seconds: int = 600

    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440

    @property
    def postgres_dsn(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
