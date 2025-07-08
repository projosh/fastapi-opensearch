# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    opensearch_host: str ="localhost"
    opensearch_port: int = 9200

    class Config:
        env_file = ".env"

settings = Settings()
