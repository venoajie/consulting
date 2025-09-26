# app\core\config.py
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Tax Co-Pilot"
    API_V1_STR: str = "/api/v1"
    STATIC_API_KEY: str = "dev-key"

    # Database configuration
    # Example: "postgresql+psycopg://user:password@host:port/dbname"
    DATABASE_URL: PostgresDsn = "postgresql+psycopg://postgres:mysecretpassword@localhost:5432/postgres"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()