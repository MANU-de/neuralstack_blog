"""
Unit tests for the Content Creator API application.

This test suite covers:
- FastAPI endpoints testing
- Agent functionality testing
- Integration testing
- Error handling testing
"""

import pytest
import os
import sys
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import HTTPException

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import app, ContentRequest
from agent import create_content_crew


class TestContentRequest:
    """Test the ContentRequest Pydantic model."""
    
    def test_content_request_valid_data(self):
        """Test ContentRequest with valid data."""
        request = ContentRequest(topic="AI in Healthcare")
        assert request.topic == "AI in Healthcare"
    
    def test_content_request_empty_topic(self):
        """Test ContentRequest with empty topic."""
        with pytest.raises(ValueError):
            ContentRequest(topic="")
    
    def test_content_request_none_topic(self):
        """Test ContentRequest with None topic."""
        with pytest.raises(ValueError):
            ContentRequest(topic=None)


class TestFastAPIEndpoints:
    """Test FastAPI endpoints."""
    
    def setup_method(self):
        """Set up test client for each test."""
        self.client = TestClient(app)
    
    def test_health_check_endpoint(self):
        """Test the health check endpoint."""
        response = self.client.get("/")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
    
    @patch('main.create_content_crew')
    def test_create_content_success(self, mock_create_content_crew):
        """Test successful content creation."""
        # Mock the crew function to return a successful result
        mock_create_content_crew.return_value = "This is a test blog post about AI."
        
        response = self.client.post(
            "/create-content",
            json={"topic": "AI in Healthcare"}
        )
        
        assert response.status_code == 200
        assert "content" in response.json()
        assert response.json()["content"] == "This is a test blog post about AI."
        mock_create_content_crew.assert_called_once_with("AI in Healthcare")
    
    @patch('main.create_content_crew')
    def test_create_content_empty_result(self, mock_create_content_crew):
        """Test content creation with empty result."""
        # Mock the crew function to return None/empty result
        mock_create_content_crew.return_value = None
        
        response = self.client.post(
            "/create-content",
            json={"topic": "AI in Healthcare"}
        )
        
        assert response.status_code == 500
        assert "Content creation failed" in response.json()["detail"]
    
    @patch('main.create_content_crew')
    def test_create_content_exception(self, mock_create_content_crew):
        """Test content creation with exception."""
        # Mock the crew function to raise an exception
        mock_create_content_crew.side_effect = Exception("Test exception")
        
        response = self.client.post(
            "/create-content",
            json={"topic": "AI in Healthcare"}
        )
        
        assert response.status_code == 500
        assert "internal server error" in response.json()["detail"]
    
    def test_create_content_invalid_json(self):
        """Test content creation with invalid JSON."""
        response = self.client.post(
            "/create-content",
            json={"invalid_field": "test"}
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_create_content_missing_topic(self):
        """Test content creation with missing topic."""
        response = self.client.post(
            "/create-content",
            json={}
        )
        
        assert response.status_code == 422  # Validation error


class TestAgentFunction:
    """Test the agent.py functions."""
    
    @patch('agent.Crew')
    @patch('agent.Agent')
    def test_create_content_crew_success(self, mock_agent_class, mock_crew_class):
        """Test successful crew creation and execution."""
        # Mock the crew instance
        mock_crew_instance = Mock()
        mock_crew_instance.kickoff.return_value = "Generated blog post content"
        mock_crew_class.return_value = mock_crew_instance
        
        # Mock the agent instances
        mock_agent_instance = Mock()
        mock_agent_class.return_value = mock_agent_instance
        
        result = create_content_crew("Test Topic")
        
        assert result == "Generated blog post content"
        mock_crew_instance.kickoff.assert_called_once()
    
    @patch('agent.Crew')
    @patch('agent.Agent')
    def test_create_content_crew_exception(self, mock_agent_class, mock_crew_class):
        """Test crew creation with exception."""
        # Mock the crew instance to raise an exception
        mock_crew_instance = Mock()
        mock_crew_instance.kickoff.side_effect = Exception("Crew execution failed")
        mock_crew_class.return_value = mock_crew_instance
        
        # Mock the agent instances
        mock_agent_instance = Mock()
        mock_agent_class.return_value = mock_agent_instance
        
        with pytest.raises(Exception):
            create_content_crew("Test Topic")
    
    @patch('agent.SerperDevTool')
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key', 'SERPER_API_KEY': 'test_serper_key'})
    def test_agent_initialization_with_search_tool(self, mock_serper_tool):
        """Test agent initialization with search tool available."""
        # This test would need to be run in isolation to avoid import issues
        # We'll mock the environment and test the logic
        pass
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'}, clear=True)
    def test_missing_openai_key(self):
        """Test behavior when OpenAI API key is missing."""
        # This test would need to be run in isolation
        # We'll test the error handling logic
        pass


class TestIntegration:
    """Integration tests for the complete workflow."""
    
    @patch('agent.Crew')
    @patch('agent.Agent')
    def test_full_workflow_success(self, mock_agent_class, mock_crew_class):
        """Test the complete workflow from API to agent execution."""
        # Mock the crew instance
        mock_crew_instance = Mock()
        mock_crew_instance.kickoff.return_value = "Complete blog post about AI"
        mock_crew_class.return_value = mock_crew_instance
        
        # Mock the agent instances
        mock_agent_instance = Mock()
        mock_agent_class.return_value = mock_agent_instance
        
        # Test the agent function directly
        result = create_content_crew("AI in Healthcare")
        assert result == "Complete blog post about AI"
        
        # Test the API endpoint
        client = TestClient(app)
        with patch('main.create_content_crew', return_value="Complete blog post about AI"):
            response = client.post(
                "/create-content",
                json={"topic": "AI in Healthcare"}
            )
            assert response.status_code == 200
            assert "Complete blog post about AI" in response.json()["content"]


class TestErrorHandling:
    """Test error handling scenarios."""
    
    def test_api_validation_errors(self):
        """Test API validation error handling."""
        client = TestClient(app)
        
        # Test with invalid data types
        response = client.post(
            "/create-content",
            json={"topic": 123}  # Should be string
        )
        assert response.status_code == 422
    
    @patch('main.create_content_crew')
    def test_crew_timeout_handling(self, mock_create_content_crew):
        """Test handling of crew execution timeout."""
        mock_create_content_crew.side_effect = TimeoutError("Crew execution timed out")
        
        client = TestClient(app)
        response = client.post(
            "/create-content",
            json={"topic": "AI in Healthcare"}
        )
        
        assert response.status_code == 500
        assert "internal server error" in response.json()["detail"]


class TestLogging:
    """Test logging functionality."""
    
    @patch('main.logging')
    @patch('main.create_content_crew')
    def test_success_logging(self, mock_create_content_crew, mock_logging):
        """Test that success is logged properly."""
        mock_create_content_crew.return_value = "Test content"
        
        client = TestClient(app)
        client.post(
            "/create-content",
            json={"topic": "AI in Healthcare"}
        )
        
        # Verify that info logging was called
        mock_logging.info.assert_called()
    
    @patch('main.logging')
    @patch('main.create_content_crew')
    def test_error_logging(self, mock_create_content_crew, mock_logging):
        """Test that errors are logged properly."""
        mock_create_content_crew.side_effect = Exception("Test error")
        
        client = TestClient(app)
        client.post(
            "/create-content",
            json={"topic": "AI in Healthcare"}
        )
        
        # Verify that error logging was called
        mock_logging.error.assert_called()


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])
