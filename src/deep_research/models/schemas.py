"""
Data models and schemas for the Deep Research App.

This module contains all the Pydantic models used throughout the application
for type safety and data validation.
"""

from typing import List
from pydantic import BaseModel, Field


class WebSearchItem(BaseModel):
    """Represents a single web search to be performed."""

    reason: str = Field(
        description="The reasoning for why this search is important to the query."
    )
    query: str = Field(description="The search term to use for the web search.")


class WebSearchPlan(BaseModel):
    """Represents a complete plan of web searches to perform."""

    searches: List[WebSearchItem] = Field(
        description="A list of web searches to perform to best answer the query."
    )


class ReportData(BaseModel):
    """Represents the final research report data."""

    short_summary: str = Field(
        description="A short 2-3 sentence summary of the findings."
    )
    markdown_report: str = Field(
        description="The final report in markdown format. It should be lengthy and detailed. "
        "Aim for 5-10 pages of content, at least 1000 words."
    )
    follow_up_questions: List[str] = Field(
        description="Suggested topics to research further"
    )


class EmailConfig(BaseModel):
    """Configuration for email settings."""

    sendgrid_api_key: str = Field(description="SendGrid API key")
    from_email: str = Field(description="Sender email address")
    to_email: str = Field(description="Recipient email address")


class AppConfig(BaseModel):
    """Main application configuration."""

    openai_api_key: str = Field(description="OpenAI API key")
    email_config: EmailConfig = Field(description="Email configuration")
    log_level: str = Field(default="INFO", description="Logging level")
    max_searches: int = Field(
        default=5, description="Maximum number of searches to perform"
    )
