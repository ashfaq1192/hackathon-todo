"""
Configuration module for loading environment variables.

This module loads the DATABASE_URL from the .env file and validates
that it's present before the application starts.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Define the path to the .env file (one directory up from this file)
env_path = Path(__file__).parent.parent / ".env"

# Load environment variables from .env file
load_dotenv(dotenv_path=env_path)

# Get DATABASE_URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Validate that DATABASE_URL is not empty
if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL not found in environment variables. "
        "Please create a .env file with DATABASE_URL or set it in your environment. "
        "See .env.example for the required format."
    )
