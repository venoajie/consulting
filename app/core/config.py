# app\core\config.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Core application settings.
    Pydantic will automatically load these from environment variables.
    e.g., APP_NAME will be loaded from the APP_NAME environment variable.
    """
    APP_NAME: str = "Tax Co-Pilot"
    API_V1_STR: str = "/api/v1"

    # For local development, it's useful to set a default for the API key
    # In production, this MUST be set via an environment variable.
    STATIC_API_KEY: str = "dev-key"

    # Use model_config to specify loading from a .env file for local dev
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
