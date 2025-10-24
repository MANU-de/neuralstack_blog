"""
Pytest configuration and fixtures for the Content Creator API tests.

This file contains shared fixtures and configuration for all test modules.
"""

import pytest
import os
import sys
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import app


@pytest.fixture
def client():
    """Provide a test client for FastAPI app."""
    return TestClient(app)


@pytest.fixture
def mock_env_vars():
    """Mock environment variables for testing."""
    with patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test_openai_key',
        'SERPER_API_KEY': 'test_serper_key'
    }):
        yield


@pytest.fixture
def mock_crew():
    """Mock CrewAI crew for testing."""
    mock_crew_instance = Mock()
    mock_crew_instance.kickoff.return_value = "Mock generated content"
    return mock_crew_instance


@pytest.fixture
def mock_agents():
    """Mock CrewAI agents for testing."""
    mock_researcher = Mock()
    mock_content_writer = Mock()
    return mock_researcher, mock_content_writer


@pytest.fixture
def sample_content_request():
    """Sample content request data for testing."""
    return {
        "topic": "AI in Healthcare"
    }


@pytest.fixture
def sample_content_response():
    """Sample content response data for testing."""
    return {
        "content": "This is a sample blog post about AI in Healthcare..."
    }


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up test environment before each test."""
    # Ensure we're in the test environment
    os.environ['TESTING'] = 'true'
    yield
    # Cleanup after each test
    if 'TESTING' in os.environ:
        del os.environ['TESTING']


@pytest.fixture
def mock_search_tool():
    """Mock search tool for testing."""
    mock_tool = Mock()
    mock_tool.name = "SerperDevTool"
    return mock_tool


@pytest.fixture
def mock_tasks():
    """Mock CrewAI tasks for testing."""
    mock_task1 = Mock()
    mock_task1.description = "Research task"
    mock_task1.expected_output = "Research report"
    
    mock_task2 = Mock()
    mock_task2.description = "Writing task"
    mock_task2.expected_output = "Blog post"
    
    return [mock_task1, mock_task2]


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom settings."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


# Custom test markers
pytestmark = pytest.mark.unit
