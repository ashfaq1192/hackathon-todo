"""
Pytest configuration and fixtures for testing.

This module provides shared fixtures for all tests, including
test database engines and sessions using SQLite in-memory.
"""

import importlib
import os

import pytest
from sqlmodel import Session, SQLModel

import src.database.connection


@pytest.fixture(scope="function")
def test_engine():
    """
    Create an in-memory SQLite engine for unit tests.

    Each test function gets a fresh database that is disposed after the test.
    This ensures test isolation and fast execution.
    """
    # Set environment variables to signal connection.py to use a test engine
    os.environ["PYTEST_IN_PROGRESS"] = "1"
    os.environ["test_database_url"] = "sqlite:///:memory:"

    # Reload connection module to pick up the new environment variables
    importlib.reload(src.database.connection)

    # Reset the engine to force re-initialization with test settings
    src.database.connection.reset_engine()

    # Use the get_engine function to ensure the test engine is created
    engine = src.database.connection.get_engine()

    # Create tables
    SQLModel.metadata.create_all(engine)

    yield engine

    # Dispose the engine and clean up environment variables
    engine.dispose()
    del os.environ["PYTEST_IN_PROGRESS"]
    del os.environ["test_database_url"]
    src.database.connection.reset_engine()  # Reset again for isolation
    importlib.reload(src.database.connection)  # Reload again to reset to production config


@pytest.fixture
def test_session(test_engine):
    """
    Provide a clean database session for each test.

    The session is rolled back after each test to ensure
    no data persists between tests.
    """
    with Session(test_engine) as session:
        yield session
        session.rollback()
