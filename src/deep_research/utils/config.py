"""
Configuration management for the Deep Research App.

This module handles loading and validating configuration from environment variables
and provides a centralized way to access application settings.
"""

import os
from typing import Optional
from dotenv import load_dotenv
from ..models.schemas import AppConfig, EmailConfig


def load_environment() -> None:
    """Load environment variables from .env file."""
    load_dotenv(override=True)


def get_required_env_var(key: str) -> str:
    """Get a required environment variable, raising an error if not found."""
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Required environment variable {key} is not set")
    return value


def get_optional_env_var(key: str, default: Optional[str] = None) -> Optional[str]:
    """Get an optional environment variable with a default value."""
    return os.getenv(key, default)


def get_config() -> AppConfig:
    """
    Load and validate application configuration from environment variables.

    Returns:
        AppConfig: Validated configuration object

    Raises:
        ValueError: If required environment variables are missing
    """
    load_environment()

    # Load email configuration
    email_config = EmailConfig(
        sendgrid_api_key=get_required_env_var("SENDGRID_API_KEY"),
        from_email=get_required_env_var("FROM_EMAIL"),
        to_email=get_required_env_var("TO_EMAIL"),
    )

    # Load main application configuration
    config = AppConfig(
        openai_api_key=get_required_env_var("OPENAI_API_KEY"),
        email_config=email_config,
        log_level=get_optional_env_var("LOG_LEVEL", "INFO"),
        max_searches=int(get_optional_env_var("MAX_SEARCHES", "5")),
    )

    return config


def validate_config() -> bool:
    """
    Validate that all required configuration is present.

    Returns:
        bool: True if configuration is valid, False otherwise
    """
    try:
        get_config()
        return True
    except ValueError:
        return False
