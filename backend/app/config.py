from typing import Any, Optional

from pydantic import MySQLDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    DATABASE_URL: Optional[MySQLDsn]


settings = Settings()

print(settings.model_dump())
