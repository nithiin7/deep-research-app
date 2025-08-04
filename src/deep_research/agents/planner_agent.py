"""
Planner agent for research strategy.

This agent analyzes research queries and creates a strategic plan for web searches
to gather comprehensive information on the topic.
"""

from agents import Agent
from ..models.schemas import WebSearchPlan
from ..utils.config import get_config

# Get configuration for search limits
config = get_config()
HOW_MANY_SEARCHES = config.max_searches

INSTRUCTIONS = f"""You are a helpful research assistant. Given a query, come up with a set of web searches \
to perform to best answer the query. Output {HOW_MANY_SEARCHES} terms to query for.

Your searches should be:
1. **Comprehensive** - Cover different aspects of the topic
2. **Specific** - Use precise search terms for better results
3. **Diverse** - Include different perspectives and sources
4. **Relevant** - Directly related to the research query

For each search, provide a clear reason explaining why this search is important to understanding the query."""


planner_agent = Agent(
    name="PlannerAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=WebSearchPlan,
)
