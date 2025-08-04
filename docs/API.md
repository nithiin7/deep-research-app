# Deep Research App API Documentation

## Overview

The Deep Research App is a comprehensive AI-powered research assistant that performs web research, analysis, and report generation. This document describes the internal API and architecture.

## Core Components

### ResearchManager

The main orchestrator class that manages the complete research workflow.

**Location**: `src/deep_research/core/research_manager.py`

**Key Methods**:

- `run(query: str) -> AsyncGenerator[str, None]`: Main entry point for research
- `plan_searches(query: str) -> WebSearchPlan`: Plans search strategy
- `perform_searches(plan: WebSearchPlan) -> List[str]`: Executes searches
- `write_report(query: str, results: List[str]) -> ReportData`: Generates report
- `send_email(report: ReportData) -> None`: Sends report via email

### Agents

The application uses four specialized AI agents:

#### Planner Agent

- **Purpose**: Analyzes research queries and creates search strategies
- **Input**: Research query
- **Output**: `WebSearchPlan` with list of search items
- **Location**: `src/deep_research/agents/planner_agent.py`

#### Search Agent

- **Purpose**: Performs web searches and summarizes results
- **Input**: Search query and reason
- **Output**: Concise summary of search results
- **Location**: `src/deep_research/agents/search_agent.py`

#### Writer Agent

- **Purpose**: Synthesizes research findings into comprehensive reports
- **Input**: Original query and search results
- **Output**: `ReportData` with markdown report
- **Location**: `src/deep_research/agents/writer_agent.py`

#### Email Agent

- **Purpose**: Converts reports to HTML and sends via email
- **Input**: Markdown report
- **Output**: Email sent via SendGrid
- **Location**: `src/deep_research/agents/email_agent.py`

## Data Models

### WebSearchItem

```python
class WebSearchItem(BaseModel):
    reason: str = Field(description="Reasoning for this search")
    query: str = Field(description="Search term to use")
```

### WebSearchPlan

```python
class WebSearchPlan(BaseModel):
    searches: List[WebSearchItem] = Field(description="List of searches to perform")
```

### ReportData

```python
class ReportData(BaseModel):
    short_summary: str = Field(description="Brief summary of findings")
    markdown_report: str = Field(description="Full report in markdown")
    follow_up_questions: List[str] = Field(description="Suggested follow-up topics")
```

### AppConfig

```python
class AppConfig(BaseModel):
    openai_api_key: str
    email_config: EmailConfig
    log_level: str = "INFO"
    max_searches: int = 5
```

## Configuration

### Environment Variables

| Variable           | Type | Required | Description                         |
| ------------------ | ---- | -------- | ----------------------------------- |
| `OPENAI_API_KEY`   | str  | Yes      | OpenAI API key                      |
| `SENDGRID_API_KEY` | str  | Yes      | SendGrid API key                    |
| `FROM_EMAIL`       | str  | Yes      | Sender email address                |
| `TO_EMAIL`         | str  | Yes      | Recipient email address             |
| `LOG_LEVEL`        | str  | No       | Logging level (default: INFO)       |
| `MAX_SEARCHES`     | int  | No       | Max searches per query (default: 5) |

### Configuration Management

The `utils/config.py` module provides:

- `get_config() -> AppConfig`: Load and validate configuration
- `validate_config() -> bool`: Check if configuration is valid
- `load_environment() -> None`: Load environment variables

## Utilities

### Logging

- **Location**: `src/deep_research/utils/logging.py`
- **Features**: Structured logging with configurable levels
- **Usage**: `setup_logging()` and `get_logger(name)`

### Helpers

- **Location**: `src/deep_research/utils/helpers.py`
- **Functions**:
  - `sanitize_query(query: str) -> str`: Clean user input
  - `validate_email(email: str) -> bool`: Validate email format
  - `generate_trace_id() -> str`: Create unique trace IDs
  - `chunk_text(text: str, max_length: int) -> List[str]`: Split text into chunks
  - `extract_keywords(text: str, max_keywords: int) -> List[str]`: Extract key terms

## Error Handling

The application implements comprehensive error handling:

1. **Input Validation**: All user inputs are sanitized and validated
2. **API Error Handling**: Graceful handling of OpenAI and SendGrid API errors
3. **Logging**: All errors are logged with appropriate context
4. **User Feedback**: Clear error messages are provided to users

## Performance Considerations

1. **Concurrent Searches**: Multiple searches are performed concurrently using `asyncio`
2. **Rate Limiting**: Built-in rate limiting for API calls
3. **Caching**: Search results could be cached for repeated queries
4. **Resource Management**: Proper cleanup of resources and connections

## Security

1. **Input Sanitization**: All user inputs are sanitized to prevent injection attacks
2. **Environment Variables**: Sensitive data is stored in environment variables
3. **API Key Protection**: API keys are never logged or exposed
4. **Error Information**: Error messages don't expose sensitive information

## Testing

The application includes comprehensive tests:

- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow testing
- **Mock Testing**: External API mocking for reliable tests
- **Coverage**: Aim for >90% code coverage

## Deployment

### Local Development

```bash
# Install dependencies
uv pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your API keys

# Run application
python run.py
```

### Docker Deployment

```bash
# Build image
docker build -t deep-research-app .

# Run container
docker run -p 7860:7860 --env-file .env deep-research-app
```

### Production Considerations

1. **Environment**: Use production-grade environment variables
2. **Monitoring**: Implement application monitoring and alerting
3. **Scaling**: Consider horizontal scaling for high load
4. **Backup**: Implement data backup and recovery procedures
5. **Security**: Use HTTPS and proper authentication
