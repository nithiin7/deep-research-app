"""
Email agent for report delivery.

This agent converts research reports into well-formatted HTML emails and sends them
via SendGrid to the specified recipient.
"""

import os
from typing import Dict
import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content, To
from agents import Agent, function_tool
from ..utils.config import get_config
from ..utils.logging import get_logger


@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """
    Send an email with the given subject and HTML body.

    Args:
        subject: Email subject line
        html_body: HTML content of the email

    Returns:
        Dict[str, str]: Response status
    """
    logger = get_logger(__name__)

    try:
        config = get_config()
        sg = sendgrid.SendGridAPIClient(api_key=config.email_config.sendgrid_api_key)

        from_email = Email(config.email_config.from_email)
        to_email = To(config.email_config.to_email)
        content = Content("text/html", html_body)

        mail = Mail(from_email, to_email, subject, content).get()
        response = sg.client.mail.send.post(request_body=mail)

        logger.info(f"Email sent successfully. Status: {response.status_code}")
        return {"status": "success", "status_code": str(response.status_code)}

    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return {"status": "error", "message": str(e)}


INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.

**Process:**
1. Analyze the provided research report
2. Create an appropriate subject line that captures the main topic
3. Convert the markdown report into clean, well-presented HTML
4. Use your tool to send the email

**Email Guidelines:**
- **Subject**: Clear, concise, and descriptive (max 100 characters)
- **Format**: Professional HTML with proper structure
- **Content**: Include the full report with proper formatting
- **Style**: Clean, readable, and professional appearance
- **Length**: Include the complete report content

**HTML Formatting:**
- Use proper HTML tags (h1, h2, h3, p, ul, ol, etc.)
- Ensure good readability with appropriate spacing
- Use consistent formatting throughout
- Include a brief introduction before the main content"""


email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
)
