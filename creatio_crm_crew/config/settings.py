"""
Configuration settings for the Creatio CRM Crew.
"""

import os
from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # LLM Configuration
    openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o", alias="OPENAI_MODEL")
    temperature: float = Field(default=0.7, alias="TEMPERATURE")
    
    # Alternative LLM providers
    anthropic_api_key: Optional[str] = Field(default=None, alias="ANTHROPIC_API_KEY")
    
    # Application settings
    verbose: bool = Field(default=True, alias="VERBOSE")
    max_rpm: int = Field(default=10, alias="MAX_RPM")
    
    # Creatio CRM Connection settings
    creatio_url: Optional[str] = Field(default=None, alias="CREATIO_URL")
    creatio_username: Optional[str] = Field(default=None, alias="CREATIO_USERNAME")
    creatio_password: Optional[str] = Field(default=None, alias="CREATIO_PASSWORD")
    creatio_oauth_token: Optional[str] = Field(default=None, alias="CREATIO_OAUTH_TOKEN")
    
    # Database connection (for direct DB access)
    creatio_db_host: Optional[str] = Field(default=None, alias="CREATIO_DB_HOST")
    creatio_db_port: int = Field(default=5432, alias="CREATIO_DB_PORT")
    creatio_db_name: Optional[str] = Field(default=None, alias="CREATIO_DB_NAME")
    creatio_db_user: Optional[str] = Field(default=None, alias="CREATIO_DB_USER")
    creatio_db_password: Optional[str] = Field(default=None, alias="CREATIO_DB_PASSWORD")
    
    # Schema cache settings
    schema_cache_ttl: int = Field(default=3600, alias="SCHEMA_CACHE_TTL")  # 1 hour
    
    # Output settings
    output_dir: str = Field(default="./creatio_analysis_output", alias="OUTPUT_DIR")
    
    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
