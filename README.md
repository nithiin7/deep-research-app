# Deep Research App

An AI-powered research assistant that performs comprehensive web research on any topic and generates detailed reports with email delivery.

## 🚀 Features

- **Intelligent Search Planning**: AI analyzes your query and creates a strategic search plan
- **Comprehensive Web Research**: Performs multiple targeted searches across the web
- **Advanced Analysis**: Synthesizes findings into detailed, well-structured reports
- **Email Delivery**: Automatically sends research reports via email
- **Real-time Updates**: Live status updates during the research process
- **Professional Reports**: 5-10 page detailed reports with analysis and recommendations

## 📋 Requirements

- Python 3.8+
- OpenAI API key
- SendGrid API key
- Email addresses for sending/receiving reports

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd deep-research-app
```

### 2. Install dependencies with uv

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv pip install -r requirements.txt
```

### 3. Set up environment variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your API keys and email addresses
nano .env
```

Required environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key
- `SENDGRID_API_KEY`: Your SendGrid API key
- `FROM_EMAIL`: Email address to send reports from
- `TO_EMAIL`: Email address to receive reports

## 🚀 Usage

### Running the Application

```bash
# Run the Gradio web interface
python -m src.deep_research.main
```

The application will start a web server at `http://localhost:7860` and open in your browser.

### Using the Web Interface

1. **Enter your research query** in the text box
2. **Click "Start Research"** to begin the process
3. **Monitor progress** through real-time status updates
4. **Receive the report** via email when complete

### Research Process

The application follows this workflow:

1. **Planning Phase**: AI analyzes your query and creates a search strategy
2. **Search Phase**: Performs multiple targeted web searches
3. **Analysis Phase**: Synthesizes findings and identifies key insights
4. **Report Generation**: Creates a comprehensive 5-10 page report
5. **Email Delivery**: Sends the report to your specified email address

## 📁 Project Structure

```
deep-research-app/
├── src/
│   └── deep_research/
│       ├── __init__.py
│       ├── main.py                 # Main application entry point
│       ├── core/
│       │   ├── __init__.py
│       │   └── research_manager.py # Core research orchestration
│       ├── agents/
│       │   ├── __init__.py
│       │   ├── planner_agent.py    # Search strategy planning
│       │   ├── search_agent.py     # Web search execution
│       │   ├── writer_agent.py     # Report generation
│       │   └── email_agent.py      # Email delivery
│       ├── models/
│       │   ├── __init__.py
│       │   └── schemas.py          # Data models and schemas
│       └── utils/
│           ├── __init__.py
│           ├── config.py           # Configuration management
│           ├── logging.py          # Logging setup
│           └── helpers.py          # Utility functions
├── tests/                          # Test suite
├── docs/                           # Documentation
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
└── README.md                       # This file
```

## 🔧 Configuration

### Environment Variables

| Variable           | Description                  | Required | Default |
| ------------------ | ---------------------------- | -------- | ------- |
| `OPENAI_API_KEY`   | OpenAI API key for AI models | Yes      | -       |
| `SENDGRID_API_KEY` | SendGrid API key for email   | Yes      | -       |
| `FROM_EMAIL`       | Sender email address         | Yes      | -       |
| `TO_EMAIL`         | Recipient email address      | Yes      | -       |
| `LOG_LEVEL`        | Logging level                | No       | INFO    |
| `MAX_SEARCHES`     | Maximum searches per query   | No       | 5       |

### Customization

You can customize the application by modifying:

- **Search Strategy**: Edit `planner_agent.py` to change how searches are planned
- **Report Format**: Modify `writer_agent.py` to adjust report structure and content
- **Email Format**: Update `email_agent.py` to change email formatting
- **Configuration**: Adjust settings in `utils/config.py`

## 🧪 Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=src/deep_research

# Run specific test file
pytest tests/test_research_manager.py
```

## 📝 Development

### Code Style

This project uses:

- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for type checking

```bash
# Format code
black src/ tests/

# Check code style
flake8 src/ tests/

# Type checking
mypy src/
```

### Adding New Features

1. **Create feature branch**: `git checkout -b feature/new-feature`
2. **Implement changes**: Follow the existing code structure
3. **Add tests**: Create tests in the `tests/` directory
4. **Update documentation**: Modify README and docstrings
5. **Submit pull request**: Ensure all tests pass

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues:

1. Check the [Issues](https://github.com/your-repo/issues) page
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

## 🔮 Roadmap

- [ ] Add support for multiple research formats
- [ ] Implement research history and caching
- [ ] Add export options (PDF, Word, etc.)
- [ ] Create API endpoints for programmatic access
- [ ] Add support for custom research templates
- [ ] Implement research collaboration features

## 🙏 Acknowledgments

- Built with [Gradio](https://gradio.app/) for the web interface
- Powered by [OpenAI](https://openai.com/) for AI capabilities
- Email delivery via [SendGrid](https://sendgrid.com/)
- Project structure inspired by modern Python best practices
