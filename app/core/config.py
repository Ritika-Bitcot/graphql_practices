"""
Configuration module for application settings.

This module handles environment variable loading and provides
configuration settings for the application following the
Single Responsibility Principle.
"""

import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings class.
    
    This class encapsulates all configuration settings and provides
    type validation using Pydantic.
    """
    
    # Database Configuration
    database_url: str = Field(
        default=None,
        env="DATABASE_URL",
        description="PostgreSQL database connection URL"
    )
    db_host: str = Field(default="localhost", env="DB_HOST", description="Database host")
    db_port: int = Field(default=5432, env="DB_PORT", description="Database port")
    db_name: str = Field(default="notes_db", env="DB_NAME", description="Database name")
    db_user: str = Field(default=None, env="DB_USER", description="Database username")
    db_password: str = Field(default=None, env="DB_PASSWORD", description="Database password")
    
    # Application Configuration
    debug: bool = Field(default=False, env="DEBUG", description="Debug mode")
    secret_key: str = Field(
        default=None,
        env="SECRET_KEY",
        description="Application secret key"
    )
    app_name: str = Field(default="Notes GraphQL API", env="APP_NAME", description="Application name")
    app_version: str = Field(default="1.0.0", env="APP_VERSION", description="Application version")
    
    # GraphQL Configuration
    graphql_debug: bool = Field(default=False, env="GRAPHQL_DEBUG", description="GraphQL debug mode")
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


def get_settings() -> Settings:
    """
    Get application settings instance.
    
    Returns:
        Settings: Application settings object
    """
    return Settings()


# Global settings instance
settings = get_settings()
