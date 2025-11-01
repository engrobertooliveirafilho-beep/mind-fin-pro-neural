from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    REDIS_URL: str | None = Field(default=None)
    # acrescente outras configs aqui se existirem

settings = Settings()
