"""
Logging configuration for the Deep Research App.

This module sets up structured logging with appropriate formatting and levels
for different environments.
"""

import logging
import sys
from typing import Optional
from .config import get_optional_env_var


def setup_logging(
    level: Optional[str] = None, log_format: Optional[str] = None
) -> logging.Logger:
    """
    Set up logging configuration for the application.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Custom log format string

    Returns:
        logging.Logger: Configured logger instance
    """
    # Get log level from environment or use default
    if level is None:
        level = get_optional_env_var("LOG_LEVEL", "INFO")

    # Convert string to logging level
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    # Set up log format
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"

    # Configure root logger
    logging.basicConfig(
        level=numeric_level,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("deep_research.log"),
        ],
    )

    # Create and return logger for this application
    logger = logging.getLogger("deep_research")
    logger.setLevel(numeric_level)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.

    Args:
        name: Logger name (usually __name__)

    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name)


class LoggerMixin:
    """Mixin class to add logging capabilities to any class."""

    @property
    def logger(self) -> logging.Logger:
        """Get a logger instance for this class."""
        return logging.getLogger(self.__class__.__name__)
