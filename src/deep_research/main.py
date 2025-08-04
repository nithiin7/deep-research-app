"""
Main entry point for the Deep Research App.

This module provides the Gradio web interface for the research application
and handles the main application lifecycle.
"""

import asyncio
import gradio as gr
from typing import AsyncGenerator

from .core.research_manager import ResearchManager
from .utils.config import get_config, validate_config
from .utils.logging import setup_logging, get_logger
from .utils.helpers import sanitize_query


def run_research_app() -> None:
    """Launch the Gradio web interface for the research app."""
    # Set up logging
    logger = setup_logging()

    # Validate configuration
    if not validate_config():
        logger.error("Invalid configuration. Please check your environment variables.")
        return

    logger.info("Starting Deep Research App...")

    # Create the Gradio interface
    with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
        gr.Markdown("# Deep Research")
        gr.Markdown(
            "An AI-powered research assistant that performs comprehensive web research."
        )

        with gr.Row():
            with gr.Column(scale=3):
                query_textbox = gr.Textbox(
                    label="What topic would you like to research?",
                    placeholder="Enter your research query here...",
                    lines=3,
                )
                run_button = gr.Button("Start Research", variant="primary", size="lg")

            with gr.Column(scale=1):
                gr.Markdown("### Research Process")
                gr.Markdown("1. **Planning** - AI plans search strategy")
                gr.Markdown("2. **Searching** - Performs web searches")
                gr.Markdown("3. **Analysis** - Synthesizes findings")
                gr.Markdown("4. **Reporting** - Generates detailed report")
                gr.Markdown("5. **Email** - Sends report via email")

        with gr.Row():
            report = gr.Markdown(label="Research Report")

        # Status updates
        status = gr.Textbox(label="Status", interactive=False)

        # Set up event handlers
        run_button.click(
            fn=run_research_with_status,
            inputs=[query_textbox],
            outputs=[status, report],
        )

        query_textbox.submit(
            fn=run_research_with_status,
            inputs=[query_textbox],
            outputs=[status, report],
        )

    # Launch the interface
    ui.launch(inbrowser=True, server_name="0.0.0.0", server_port=7860, share=False)


async def run_research_with_status(query: str) -> tuple[str, str]:
    """
    Run research with status updates.

    Args:
        query: Research query

    Returns:
        tuple: (status_message, final_report)
    """
    logger = get_logger(__name__)

    if not query or not query.strip():
        return "Please enter a research query.", ""

    # Sanitize the query
    sanitized_query = sanitize_query(query)
    if not sanitized_query:
        return "Invalid query. Please try again.", ""

    try:
        status_messages = []
        final_report = ""

        # Run the research process
        async for chunk in ResearchManager().run(sanitized_query):
            if chunk.startswith("View trace:"):
                status_messages.append(chunk)
            elif chunk == "Report written, sending email...":
                status_messages.append("✅ Report generated successfully!")
            elif chunk == "Email sent, research complete":
                status_messages.append("📧 Email sent successfully!")
            else:
                status_messages.append(chunk)

            # Update status
            yield "\n".join(status_messages), final_report

        # Get the final report
        async for chunk in ResearchManager().run(sanitized_query):
            if not chunk.startswith("View trace:") and not any(
                status in chunk
                for status in [
                    "Starting research...",
                    "Searches planned",
                    "Searches complete",
                    "Report written",
                    "Email sent",
                    "research complete",
                ]
            ):
                final_report = chunk
                break

        return "\n".join(status_messages), final_report

    except Exception as e:
        logger.error(f"Error during research: {e}")
        error_msg = f"An error occurred during research: {str(e)}"
        return error_msg, ""


async def run(query: str) -> AsyncGenerator[str, None]:
    """
    Run the research process and yield status updates.

    Args:
        query: Research query

    Yields:
        str: Status updates and final report
    """
    logger = get_logger(__name__)

    if not query or not query.strip():
        yield "Please enter a research query."
        return

    # Sanitize the query
    sanitized_query = sanitize_query(query)
    if not sanitized_query:
        yield "Invalid query. Please try again."
        return

    try:
        async for chunk in ResearchManager().run(sanitized_query):
            yield chunk
    except Exception as e:
        logger.error(f"Error during research: {e}")
        yield f"An error occurred during research: {str(e)}"


if __name__ == "__main__":
    run_research_app()
