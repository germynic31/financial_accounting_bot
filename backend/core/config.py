from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки проекта."""

    SECRET: str = 'SECRET'
    TG_API_KEY: str = 'API_KEY'
    DATABASE_URL_DEV: str

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent / '.env',  # noqa: E501
        extra='allow',
    )


settings = Settings()
