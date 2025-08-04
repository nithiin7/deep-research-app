"""
Tests for the ResearchManager class.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from src.deep_research.core.research_manager import ResearchManager
from src.deep_research.models.schemas import WebSearchItem, WebSearchPlan, ReportData


class TestResearchManager:
    """Test cases for ResearchManager class."""

    @pytest.fixture
    def research_manager(self):
        """Create a ResearchManager instance for testing."""
        return ResearchManager()

    @pytest.fixture
    def mock_search_plan(self):
        """Create a mock search plan."""
        return WebSearchPlan(
            searches=[
                WebSearchItem(
                    query="test query 1", reason="Testing search functionality"
                ),
                WebSearchItem(query="test query 2", reason="Testing multiple searches"),
            ]
        )

    @pytest.fixture
    def mock_report_data(self):
        """Create mock report data."""
        return ReportData(
            short_summary="Test summary",
            markdown_report="# Test Report\n\nThis is a test report.",
            follow_up_questions=["Question 1", "Question 2"],
        )

    def test_research_manager_initialization(self, research_manager):
        """Test that ResearchManager initializes correctly."""
        assert research_manager is not None
        assert hasattr(research_manager, "config")
        assert hasattr(research_manager, "logger")

    @pytest.mark.asyncio
    async def test_plan_searches(self, research_manager, mock_search_plan):
        """Test search planning functionality."""
        with patch("src.deep_research.core.research_manager.Runner.run") as mock_run:
            mock_run.return_value.final_output_as.return_value = mock_search_plan

            result = await research_manager.plan_searches("test query")

            assert result == mock_search_plan
            assert len(result.searches) == 2
            mock_run.assert_called_once()

    @pytest.mark.asyncio
    async def test_perform_searches(self, research_manager, mock_search_plan):
        """Test search execution functionality."""
        with patch.object(
            research_manager, "search", new_callable=AsyncMock
        ) as mock_search:
            mock_search.return_value = "test search result"

            results = await research_manager.perform_searches(mock_search_plan)

            assert len(results) == 2
            assert all(result == "test search result" for result in results)
            assert mock_search.call_count == 2

    @pytest.mark.asyncio
    async def test_write_report(self, research_manager, mock_report_data):
        """Test report writing functionality."""
        with patch("src.deep_research.core.research_manager.Runner.run") as mock_run:
            mock_run.return_value.final_output_as.return_value = mock_report_data

            result = await research_manager.write_report(
                "test query", ["result1", "result2"]
            )

            assert result == mock_report_data
            assert result.short_summary == "Test summary"
            assert result.markdown_report.startswith("# Test Report")
            mock_run.assert_called_once()

    @pytest.mark.asyncio
    async def test_send_email(self, research_manager, mock_report_data):
        """Test email sending functionality."""
        with patch("src.deep_research.core.research_manager.Runner.run") as mock_run:
            mock_run.return_value = None

            # Should not raise an exception
            await research_manager.send_email(mock_report_data)

            mock_run.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_with_error_handling(self, research_manager):
        """Test search error handling."""
        search_item = WebSearchItem(query="test query", reason="Testing error handling")

        with patch("src.deep_research.core.research_manager.Runner.run") as mock_run:
            mock_run.side_effect = Exception("Search failed")

            result = await research_manager.search(search_item)

            assert result is None

    @pytest.mark.asyncio
    async def test_perform_searches_empty_plan(self, research_manager):
        """Test search execution with empty plan."""
        empty_plan = WebSearchPlan(searches=[])

        results = await research_manager.perform_searches(empty_plan)

        assert results == []

    def test_sanitize_query(self):
        """Test query sanitization."""
        from src.deep_research.utils.helpers import sanitize_query

        # Test normal query
        assert sanitize_query("normal query") == "normal query"

        # Test query with special characters
        assert sanitize_query("query with <script> tags") == "query with  tags"

        # Test empty query
        assert sanitize_query("") == ""

        # Test very long query
        long_query = "a" * 600
        sanitized = sanitize_query(long_query)
        assert len(sanitized) <= 500

    def test_validate_email(self):
        """Test email validation."""
        from src.deep_research.utils.helpers import validate_email

        # Valid emails
        assert validate_email("test@example.com") is True
        assert validate_email("user.name@domain.co.uk") is True

        # Invalid emails
        assert validate_email("invalid-email") is False
        assert validate_email("") is False
        assert validate_email("@domain.com") is False
