# app\core\config.py

import yaml
from pathlib import Path
from typing import List, Dict, Optional
from pydantic import BaseModel, Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

# --- Pydantic Models for Type-Safe YAML Config ---

class ProviderConfig(BaseModel):
    api_key_env: str
    models: List[str]
    api_endpoint: Optional[str] = None

class AIConfig(BaseModel):
    default_model: str
    providers: Dict[str, ProviderConfig]

# --- Main Settings Class ---

class Settings(BaseSettings):
    APP_NAME: str = "Tax Co-Pilot"
    API_V1_STR: str = "/api/v1"
    STATIC_API_KEY: str = "dev-key"
    
    # Loaded from .env
    GEMINI_API_KEY: Optional[str] = None
    DEEPSEEK_API_KEY: Optional[str] = None
    DATABASE_URL: PostgresDsn = "postgresql+psycopg://postgres:mysecretpassword@localhost:5432/postgres"
    
    # Loaded from config.yml
    ai: AIConfig

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

def load_settings() -> Settings:
    """Loads settings from .env and config.yml, then merges them."""
    # Load YAML config first
    config_path = Path(__file__).parent.parent.parent / "config.yml"
    with open(config_path, 'r') as f:
        config_data = yaml.safe_load(f)
    
    ai_config = AIConfig.model_validate(config_data)
    
    # Load settings from .env and inject the AIConfig
    return Settings(ai=ai_config)

settings = load_settings()

def get_provider_info_for_model(model_name: str) -> Optional[Dict]:
    """Finds the provider configuration for a given model name."""
    for provider_name, provider_config in settings.ai.providers.items():
        if model_name in provider_config.models:
            return {
                "provider_name": provider_name,
                "config": provider_config,
            }
    return None