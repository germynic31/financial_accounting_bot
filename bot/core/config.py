from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    """Настройки проекта."""

    SECRET: str = 'SECRET'
    API_KEY: str = 'API_KEY'
    DATABASE_URL: str = 'sqlite:///./database.db'

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent / '.env',  # noqa: E501
        env_prefix='BOT_',
        extra='allow',
    )


settings = BotSettings()
