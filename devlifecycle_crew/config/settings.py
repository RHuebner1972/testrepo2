"""
Configuration settings for the DevLifecycle Crew.
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
    
    # Storage settings
    database_url: str = Field(
        default="sqlite:///devlifecycle.db",
        alias="DATABASE_URL"
    )
    
    # Ticket system integration (optional)
    jira_url: Optional[str] = Field(default=None, alias="JIRA_URL")
    jira_api_token: Optional[str] = Field(default=None, alias="JIRA_API_TOKEN")
    jira_email: Optional[str] = Field(default=None, alias="JIRA_EMAIL")
    
    github_token: Optional[str] = Field(default=None, alias="GITHUB_TOKEN")
    github_repo: Optional[str] = Field(default=None, alias="GITHUB_REPO")
    
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
