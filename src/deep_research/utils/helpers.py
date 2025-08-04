"""
Helper functions for the Deep Research App.

This module contains utility functions used throughout the application
for common operations like validation, sanitization, and data processing.
"""

import re
import hashlib
from typing import List, Optional
from datetime import datetime


def sanitize_query(query: str) -> str:
    """
    Sanitize a research query by removing potentially harmful characters.

    Args:
        query: Raw query string

    Returns:
        str: Sanitized query string
    """
    if not query:
        return ""

    # Remove potentially harmful characters but keep alphanumeric, spaces, and common punctuation
    sanitized = re.sub(r'[<>"\']', "", query.strip())

    # Limit length to prevent abuse
    if len(sanitized) > 500:
        sanitized = sanitized[:500]

    return sanitized


def validate_email(email: str) -> bool:
    """
    Validate email address format.

    Args:
        email: Email address to validate

    Returns:
        bool: True if email is valid, False otherwise
    """
    if not email:
        return False

    # Basic email validation regex
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def generate_trace_id() -> str:
    """
    Generate a unique trace ID for tracking research sessions.

    Returns:
        str: Unique trace ID
    """
    timestamp = datetime.now().isoformat()
    random_component = hashlib.md5(timestamp.encode()).hexdigest()[:8]
    return f"research_{timestamp}_{random_component}"


def chunk_text(text: str, max_length: int = 1000) -> List[str]:
    """
    Split text into chunks of specified maximum length.

    Args:
        text: Text to chunk
        max_length: Maximum length of each chunk

    Returns:
        List[str]: List of text chunks
    """
    if len(text) <= max_length:
        return [text]

    chunks = []
    current_chunk = ""

    for sentence in text.split("."):
        if len(current_chunk + sentence) <= max_length:
            current_chunk += sentence + "."
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + "."

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """
    Extract key terms from text for search optimization.

    Args:
        text: Text to extract keywords from
        max_keywords: Maximum number of keywords to extract

    Returns:
        List[str]: List of extracted keywords
    """
    # Remove common stop words
    stop_words = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "but",
        "in",
        "on",
        "at",
        "to",
        "for",
        "of",
        "with",
        "by",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "will",
        "would",
        "could",
        "should",
        "may",
        "might",
        "can",
        "this",
        "that",
        "these",
        "those",
    }

    # Convert to lowercase and split into words
    words = re.findall(r"\b\w+\b", text.lower())

    # Filter out stop words and short words
    keywords = [word for word in words if word not in stop_words and len(word) > 2]

    # Count frequency and return most common
    word_count = {}
    for word in keywords:
        word_count[word] = word_count.get(word, 0) + 1

    # Sort by frequency and return top keywords
    sorted_keywords = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    return [word for word, count in sorted_keywords[:max_keywords]]


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable string.

    Args:
        seconds: Duration in seconds

    Returns:
        str: Formatted duration string
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def safe_filename(filename: str) -> str:
    """
    Convert a string to a safe filename by removing invalid characters.

    Args:
        filename: Original filename

    Returns:
        str: Safe filename
    """
    # Remove or replace invalid characters
    safe = re.sub(r'[<>:"/\\|?*]', "_", filename)
    # Remove leading/trailing spaces and dots
    safe = safe.strip(". ")
    # Limit length
    if len(safe) > 255:
        safe = safe[:255]
    return safe
