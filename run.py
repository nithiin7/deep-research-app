#!/usr/bin/env python3
"""
Simple entry point for the Deep Research App.

This script provides an easy way to run the application without
having to remember the full module path.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from deep_research.main import run_research_app

if __name__ == "__main__":
    run_research_app()
