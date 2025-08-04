"""
Core research management functionality.

This module orchestrates the complete research workflow including planning,
searching, analysis, and report generation.
"""

import asyncio
from typing import AsyncGenerator, List, Optional
from agents import Runner, trace, gen_trace_id

from ..agents import search_agent, planner_agent, writer_agent, email_agent
from ..models.schemas import WebSearchItem, WebSearchPlan, ReportData
from ..utils.logging import LoggerMixin, get_logger
from ..utils.config import get_config
from ..utils.helpers import generate_trace_id, format_duration


class ResearchManager(LoggerMixin):
    """Manages the complete research workflow."""

    def __init__(self):
        """Initialize the research manager."""
        self.config = get_config()
        self.logger = get_logger(__name__)

    async def run(self, query: str) -> AsyncGenerator[str, None]:
        """
        Run the deep research process, yielding status updates and the final report.

        Args:
            query: Research query

        Yields:
            str: Status updates and final report
        """
        start_time = asyncio.get_event_loop().time()
        trace_id = gen_trace_id()

        with trace("Research trace", trace_id=trace_id):
            self.logger.info(f"Starting research for query: {query[:50]}...")
            self.logger.info(
                f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            )

            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            yield "Starting research..."

            try:
                # Step 1: Plan searches
                search_plan = await self.plan_searches(query)
                yield f"Searches planned ({len(search_plan.searches)} searches), starting to search..."

                # Step 2: Perform searches
                search_results = await self.perform_searches(search_plan)
                yield f"Searches complete ({len(search_results)} results), writing report..."

                # Step 3: Write report
                report = await self.write_report(query, search_results)
                yield "Report written, sending email..."

                # Step 4: Send email
                await self.send_email(report)
                yield "Email sent, research complete"

                # Step 5: Return final report
                yield report.markdown_report

                # Log completion
                duration = asyncio.get_event_loop().time() - start_time
                self.logger.info(f"Research completed in {format_duration(duration)}")

            except Exception as e:
                self.logger.error(f"Error during research: {e}")
                yield f"❌ Error during research: {str(e)}"
                raise

    async def plan_searches(self, query: str) -> WebSearchPlan:
        """
        Plan the searches to perform for the query.

        Args:
            query: Research query

        Returns:
            WebSearchPlan: Plan containing search items
        """
        self.logger.info("Planning searches...")

        try:
            result = await Runner.run(
                planner_agent,
                f"Query: {query}",
            )

            search_plan = result.final_output_as(WebSearchPlan)
            self.logger.info(f"Planned {len(search_plan.searches)} searches")

            return search_plan

        except Exception as e:
            self.logger.error(f"Error planning searches: {e}")
            raise

    async def perform_searches(self, search_plan: WebSearchPlan) -> List[str]:
        """
        Perform the planned searches.

        Args:
            search_plan: Search plan containing search items

        Returns:
            List[str]: List of search results
        """
        self.logger.info("Starting searches...")

        if not search_plan.searches:
            self.logger.warning("No searches to perform")
            return []

        num_completed = 0
        results = []

        # Create tasks for concurrent execution
        tasks = [
            asyncio.create_task(self.search(item)) for item in search_plan.searches
        ]

        # Process completed tasks
        for task in asyncio.as_completed(tasks):
            try:
                result = await task
                if result is not None:
                    results.append(result)
                num_completed += 1
                self.logger.info(
                    f"Search progress: {num_completed}/{len(tasks)} completed"
                )

            except Exception as e:
                self.logger.error(f"Error in search task: {e}")
                num_completed += 1

        self.logger.info(f"Completed {len(results)} successful searches")
        return results

    async def search(self, item: WebSearchItem) -> Optional[str]:
        """
        Perform a single search.

        Args:
            item: Search item containing query and reason

        Returns:
            Optional[str]: Search result or None if failed
        """
        input_text = f"Search term: {item.query}\nReason for searching: {item.reason}"

        try:
            self.logger.debug(f"Searching: {item.query}")

            result = await Runner.run(
                search_agent,
                input_text,
            )

            return str(result.final_output)

        except Exception as e:
            self.logger.error(f"Search failed for '{item.query}': {e}")
            return None

    async def write_report(self, query: str, search_results: List[str]) -> ReportData:
        """
        Write the research report.

        Args:
            query: Original research query
            search_results: List of search results

        Returns:
            ReportData: Generated report data
        """
        self.logger.info("Writing report...")

        try:
            input_text = (
                f"Original query: {query}\nSummarized search results: {search_results}"
            )

            result = await Runner.run(
                writer_agent,
                input_text,
            )

            report = result.final_output_as(ReportData)
            self.logger.info("Report written successfully")

            return report

        except Exception as e:
            self.logger.error(f"Error writing report: {e}")
            raise

    async def send_email(self, report: ReportData) -> None:
        """
        Send the research report via email.

        Args:
            report: Report data to send
        """
        self.logger.info("Sending email...")

        try:
            result = await Runner.run(
                email_agent,
                report.markdown_report,
            )

            self.logger.info("Email sent successfully")

        except Exception as e:
            self.logger.error(f"Error sending email: {e}")
            raise
