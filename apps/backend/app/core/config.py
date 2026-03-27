from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    postgres_dsn: str = "postgresql+psycopg://postgres:postgres@localhost:5432/jclaw"
    redis_url: str = "redis://localhost:6379/0"
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[4] / ".env",
        extra="ignore",
    )


settings = Settings()
