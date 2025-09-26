# app\core\config.py


import yaml
from pathlib import Path
from typing import List, Dict, Optional
from pydantic import BaseModel, Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

# --- Pydantic Models for Type-Safe YAML Config ---
class ServiceConfig(BaseModel):
    version: str
    log_level: str

class ApiConfig(BaseModel):
    static_key: str = Field(..., alias="STATIC_API_KEY")

class DatabaseConfig(BaseModel):
    url: PostgresDsn = Field(..., alias="DATABASE_URL")

class ProviderConfig(BaseModel):
    api_key_env: str
    models: List[str]
    api_endpoint: Optional[str] = None

class AIConfig(BaseModel):
    default_model: str
    source_language: str
    target_language: str
    providers: Dict[str, ProviderConfig]

class MergedConfig(BaseModel):
    service: ServiceConfig
    api: ApiConfig
    database: DatabaseConfig
    ai: AIConfig

# --- Main Settings Class (now much simpler) ---
class Settings(BaseSettings):
    # These are the only settings loaded directly from environment variables
    # They override the values from the YAML file.
    STATIC_API_KEY: Optional[str] = None
    DATABASE_URL: Optional[PostgresDsn] = None
    GEMINI_API_KEY: Optional[str] = None
    DEEPSEEK_API_KEY: Optional[str] = None
    
    # This will hold the fully parsed and merged config
    app: MergedConfig

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

def load_settings() -> Settings:
    config_path = Path(__file__).parent.parent.parent / "config.yml"
    with open(config_path, 'r') as f:
        config_data = yaml.safe_load(f)
    
    # Load settings from .env and create an initial instance
    env_settings = Settings(app=MergedConfig.model_validate(config_data))
    
    # Manually override YAML values with any values set in the environment
    if env_settings.STATIC_API_KEY:
        env_settings.app.api.static_key = env_settings.STATIC_API_KEY
    if env_settings.DATABASE_URL:
        env_settings.app.database.url = str(env_settings.DATABASE_URL)
        
    return env_settings

settings = load_settings()

def get_provider_info_for_model(model_name: str) -> Optional[Dict]:
    for provider_name, provider_config in settings.app.ai.providers.items():
        if model_name in provider_config.models:
            return {"provider_name": provider_name, "config": provider_config}
    return None