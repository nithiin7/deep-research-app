#!/bin/bash

# Deep Research App Setup Script
# This script sets up the development environment

set -e

echo "🚀 Setting up Deep Research App..."

# Check if Python 3.8+ is installed
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.8 or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python version: $python_version"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
    echo "✅ uv installed successfully"
else
    echo "✅ uv is already installed"
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo "⚠️  Please edit .env file with your API keys and email addresses"
else
    echo "✅ .env file already exists"
fi

# Install dependencies
echo "📦 Installing dependencies..."
uv pip install -r requirements.txt

# Install development dependencies
echo "🔧 Installing development dependencies..."
uv pip install pytest pytest-asyncio pytest-cov black flake8 mypy pre-commit

# Install pre-commit hooks
echo "🔗 Installing pre-commit hooks..."
pre-commit install

# Create logs directory
mkdir -p logs

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys and email addresses"
echo "2. Run the application: python run.py"
echo "3. Or use Docker: docker-compose up"
echo ""
echo "Available commands:"
echo "  make help          - Show all available commands"
echo "  make run           - Run the application"
echo "  make test          - Run tests"
echo "  make format        - Format code"
echo "  make lint          - Run linting"
echo "" 